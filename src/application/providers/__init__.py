import importlib
import inspect
import pkgutil
import sys
from pathlib import Path
from typing import List, Type

from dishka import AsyncContainer, Provider, make_async_container


class ProvidersManager:

    def __init__(self) -> None:
        self.current_dir = Path(__file__).parent
        self._providers: List[Type[Provider]] = []

    def search_providers(self) -> List[Type[Provider]]:
        self._providers = []
        parent_dir = self.current_dir.parent

        if str(parent_dir) not in sys.path:
            sys.path.insert(0, str(parent_dir))

        package = importlib.import_module(self.current_dir.name)

        for module_info in pkgutil.iter_modules([str(self.current_dir)]):
            module_name = module_info.name

            if module_name.startswith("_"):
                continue

            if hasattr(package, "__package__") and package.__package__:
                full_module_name = f"{package.__package__}.{module_name}"
            else:
                full_module_name = f"{self.current_dir.name}.{module_name}"

            module = importlib.import_module(full_module_name)

            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, Provider)
                    and obj != Provider
                    and obj.__module__ == module.__name__
                ):
                    self._providers.append(obj)
        return self._providers

    def make_container(self, **container_kwargs) -> AsyncContainer:
        self.search_providers()
        if not self._providers:
            raise ValueError("No providers found in current directory")

        provider_instances = [provider() for provider in self._providers]

        container = make_async_container(*provider_instances, **container_kwargs)
        return container
