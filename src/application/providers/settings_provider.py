from dishka import Provider, Scope, provide

from application.settings import Settings


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_settings(self) -> Settings:
        return Settings()
