from django.core.management.base import BaseCommand
from django.conf import settings
import os
import subprocess
from datetime import datetime

class Command(BaseCommand):
    help = 'Backup or restore the database inside the Docker container'

    def add_arguments(self, parser):
        parser.add_argument(
            '--restore',
            action='store_true',
            help='Restore the database from a backup file'
        )
        parser.add_argument(
            '--backup-file',
            type=str,
            help='Path to the backup file (required for restore)'
        )

    def handle(self, *args, **kwargs):
        backup_dir = settings.BACKUP_DIR  # Ensure this is defined in your settings
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Define Docker container name
        container_name = "postgres_db"  # Your PostgreSQL container name

        if kwargs['restore']:
            # Handle restore functionality
            if not kwargs['backup_file']:
                self.stdout.write(self.style.ERROR("You must provide a backup file path for restoration."))
                return

            restore_file_path = kwargs['backup_file']
            if not os.path.exists(restore_file_path):
                self.stdout.write(self.style.ERROR(f"Backup file does not exist: {restore_file_path}"))
                return

            # Define the restore command
            restore_command = f"cat {restore_file_path} | docker exec -i {container_name} psql -U {settings.DATABASES['default']['USER']} -d {settings.DATABASES['default']['NAME']}"

            try:
                # Execute the restore command
                subprocess.run(restore_command, shell=True, check=True)
                self.stdout.write(self.style.SUCCESS(f"Database restore successful from: {restore_file_path}"))
            except subprocess.CalledProcessError as e:
                self.stdout.write(self.style.ERROR(f"Restore failed: {e}"))
        else:
            # Backup functionality
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_filename = f"db_backup_{timestamp}.sql"
            backup_path = os.path.join(backup_dir, backup_filename)

            # Define the pg_dump command to run inside the Docker container
            pg_dump_command = f"pg_dump -U {settings.DATABASES['default']['USER']} -d {settings.DATABASES['default']['NAME']}"

            # Run the pg_dump command inside the Docker container and redirect the output to a file
            exec_command = f"docker exec {container_name} bash -c '{pg_dump_command} > /tmp/{backup_filename}'"

            try:
                # Execute the exec command inside Docker
                subprocess.run(exec_command, shell=True, check=True)

                # Copy the backup file from the Docker container to the host
                copy_command = f"docker cp {container_name}:/tmp/{backup_filename} {backup_path}"

                # Execute the copy command
                subprocess.run(copy_command, shell=True, check=True)

                # Remove the temporary backup file from the container
                remove_command = f"docker exec {container_name} rm /tmp/{backup_filename}"
                subprocess.run(remove_command, shell=True, check=True)

                self.stdout.write(self.style.SUCCESS(f"Database backup successful: {backup_path}"))
            except subprocess.CalledProcessError as e:
                self.stdout.write(self.style.ERROR(f"Backup failed: {e}"))
