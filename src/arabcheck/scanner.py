"""Composable rule scanner for ArabCheck."""

from typing import Dict, List, Optional, Sequence

from .rules.base import BaseRule
from .rules.hamza import HamzatQatRule


class Scanner:
    """Run selected audit rules without changing legacy core behavior."""

    def __init__(self, rules: Optional[Sequence[BaseRule]] = None) -> None:
        selected = list(rules) if rules is not None else [HamzatQatRule()]
        self.rules: Dict[str, BaseRule] = {}

        for rule in selected:
            if not rule.name:
                raise ValueError("Every rule must define a name.")
            if rule.name in self.rules:
                raise ValueError("Duplicate rule name: {}".format(rule.name))
            self.rules[rule.name] = rule

    def available_rules(self) -> List[str]:
        """Return the names of the registered rules."""
        return sorted(self.rules)

    def scan(
        self,
        text: str,
        rule_names: Optional[Sequence[str]] = None,
    ) -> List[dict]:
        """Run all registered rules or only the requested rules."""
        if rule_names is None:
            selected_names = self.available_rules()
        else:
            selected_names = list(rule_names)

        unknown = sorted(set(selected_names) - set(self.rules))
        if unknown:
            raise ValueError(
                "Unknown rule(s): {}".format(", ".join(unknown))
            )

        issues = []
        for name in selected_names:
            issues.extend(self.rules[name].check(text))

        return issues
