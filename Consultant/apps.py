from django.apps import AppConfig

class ConsultantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Consultant'

    def ready(self):
        import Consultant.signals
