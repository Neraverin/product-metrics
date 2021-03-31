from abc import ABC, abstractmethod
from typing import Any
from product_metrics.models.apiconnection import APIConnection


class BaseMetric(ABC):
    """Abstract base class for metrics.
    """

    def __init__(self, name: str, connection: APIConnection) -> None:
        self.__name = name
        self.__connection = connection

    @property
    def name(self) -> str:
        return self.__name

    @property
    def connection(self) -> APIConnection:
        return self.__connection

    @abstractmethod
    def value(self, year: int, month: int) -> Any:
        pass
