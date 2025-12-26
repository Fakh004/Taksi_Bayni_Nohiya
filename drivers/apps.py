from django.apps import AppConfig


class DriversConfig(AppConfig):
    name = 'drivers'


from django.apps import AppConfig

class YourAppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drivers'

    def ready(self):
        import drivers.signals
