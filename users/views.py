from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.core.management import call_command
from django.http import HttpResponse
from django.conf import settings
import os

# Custom admin views to trigger backup/restore actions
def backup_restore_view(request):
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "backup":
            try:
                # Trigger the backup command
                call_command('backup_db')
                message = "Database backup started successfully!"
            except Exception as e:
                message = f"Database backup failed: {str(e)}"
        
        elif action == "restore":
            # You need to pass the backup file path for restore
            backup_file = settings.BACKUP_DIR
            if not os.path.exists(backup_file):
                message = "No backup file found."
            else:
                try:
                    backup_file_path = os.path.join(backup_file, "db_backup_latest.sql")  # Modify if needed
                    call_command('backup_db', restore=True, backup_file=backup_file_path)  # Trigger restore
                    message = f"Database restore started successfully from: {backup_file_path}"
                except Exception as e:
                    message = f"Database restore failed: {str(e)}"
        
            return render(request, "admin/backup_restore.html", {"message": message})

    return render(request, "admin/backup_restore.html", {"message": None})

