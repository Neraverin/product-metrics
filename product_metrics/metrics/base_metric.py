from abc import ABC, abstractmethod


class BaseMetric(ABC):
    """Abstract base class for metrics.
    """

    def __init__(self, name: str, row: int) -> None:
        self.__name = name
        self.__row = row

    @property
    def name(self) -> str:
        return self.__name

    @property
    def row(self) -> int:
        return self.__row

    @abstractmethod
    def value(self) -> int:
        pass
