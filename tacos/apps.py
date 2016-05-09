from django.apps import AppConfig


class TacosConfig(AppConfig):
    verbose_name = 'Tacos Application'
    name = 'tacos'

    def ready(self):
        import tacos.signals
