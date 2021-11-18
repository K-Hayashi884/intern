from django.apps import AppConfig



class MyappConfig(AppConfig):
    name = 'myapp'

    # signalsを参照してくれるよう設定を追加
    def ready(self):
        import myapp.signals
