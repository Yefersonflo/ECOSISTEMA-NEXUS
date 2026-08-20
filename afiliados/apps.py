from django.apps import AppConfig


class AfiliadosConfig(AppConfig):
    name = 'afiliados'

    def ready(self):
        import afiliados.signals
