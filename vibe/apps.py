from django.apps import AppConfig
import beeline


class VibeConfig(AppConfig):
    name = 'vibe'
    def ready(self):
        beeline.init(
            writekey='',
            dataset='vibes',
            service_name='vibes',
            debug=True,
        )