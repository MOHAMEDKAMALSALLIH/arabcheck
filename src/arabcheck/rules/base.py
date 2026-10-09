"""Base interface for ArabCheck rules."""

from abc import ABC, abstractmethod
from typing import List, Dict


class BaseRule(ABC):
    """Common interface for all ArabCheck scanning rules."""

    name: str = ""
    description: str = ""
    severity: str = "warning"

    @abstractmethod
    def check(self, text: str) -> List[Dict]:
        """Inspect text and return detected issues."""
        raise NotImplementedError
