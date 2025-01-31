class MongoRouter:
    """
    Database router to control read and write operations for MongoDB-backed models.
    Ensures that models in the 'api' app use MongoDB while other models use the default database.
    """

    MONGO_DB = 'mongodb'
    DEFAULT_DB = 'default'
    API_APP_LABEL = 'api'
    EXCLUDED_APPS = {'sessions', 'auth', 'admin', 'contenttypes'}

    def db_for_read(self, model, **hints):
        """
        Determines the database to use for read operations.
        """
        if model._meta.app_label == self.API_APP_LABEL:
            return self.MONGO_DB
        return self.DEFAULT_DB

    def db_for_write(self, model, **hints):
        """
        Determines the database to use for write operations.
        """
        if model._meta.app_label == self.API_APP_LABEL:
            return self.MONGO_DB
        return self.DEFAULT_DB

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allows relations if both objects belong to the same database set.
        Prevents cross-database relations.
        """
        if obj1._state.db == obj2._state.db:
            return True
        return None  # Explicitly returning None allows Django to decide.

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Determines if migrations are allowed on a specific database.
        The 'api' app's models should only be migrated in MongoDB.
        """
        if app_label in self.EXCLUDED_APPS:
            return db == self.DEFAULT_DB
        if app_label == self.API_APP_LABEL:
            return db == self.MONGO_DB
        return db == self.DEFAULT_DB
