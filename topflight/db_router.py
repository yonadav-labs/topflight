class DBRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['mlb']:
            return model._meta.app_label
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ['mlb']:
            return model._meta.app_label
        return None
