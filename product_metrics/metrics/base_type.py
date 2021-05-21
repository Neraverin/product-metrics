from abc import ABC, abstractmethod
from typing import Any
from product_metrics.models.apiconnection import APIConnection


class BaseType(ABC):
    """Abstract base class for types.
    """

    @abstractmethod
    def collect_metrics(self, year: int, month: int) -> list:
        pass
