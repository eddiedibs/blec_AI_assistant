class MongoRouter:
    """
    A router to control all database operations on models for the MongoDB database.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'api':
            return 'mongodb'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'api':
            return 'mongodb'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        db_set = {'default', 'mongodb'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'api':
            return db == 'mongodb'
        return db == 'default'
