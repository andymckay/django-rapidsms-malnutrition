from django.db.models.loading import AppCache

class _models:
    def __init__(self):
        app = AppCache()
        models = app.get_models()
        for m in models:
            setattr(self, m.__name__, m)

models = _models()
