from abc import ABC, abstractmethod


class Base(ABC):
    def __init__(self, host) -> None:
        self.current_host = host

    @abstractmethod
    def run(self) -> None:
        """Runs the module"""
        pass

    @abstractmethod
    def log(self) -> list:
        """Returns the results of the module"""
        """Data should be new or changed since the last run"""
        return []
