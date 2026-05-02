from __future__ import annotations

from collections.abc import Callable
from typing import Any

from app.data.cards import (
    get_card_config_editor_payload,
    reload_card_catalog,
    reset_card_config,
    save_card_config,
)

BalanceApplier = Callable[[dict[str, Any], dict[str, Any]], list[str]]
PayloadProvider = Callable[[], dict[str, Any]]
SyncHook = Callable[[], None]


class CardConfigService:
    def __init__(
        self,
        *,
        get_tuning_values: PayloadProvider,
        get_tuning_specs: PayloadProvider,
        apply_balance_values: BalanceApplier,
        sync_balance_globals: SyncHook,
    ) -> None:
        self._get_tuning_values = get_tuning_values
        self._get_tuning_specs = get_tuning_specs
        self._apply_balance_values = apply_balance_values
        self._sync_balance_globals = sync_balance_globals

    def reload_live_config(self) -> list[str]:
        errors = reload_card_catalog()
        if errors:
            return errors
        errors = self._apply_balance_values(
            self._get_tuning_values(),
            self._get_tuning_specs(),
        )
        if errors:
            return errors
        self._sync_balance_globals()
        return []

    def get_payload(self) -> dict[str, Any]:
        self.reload_live_config()
        return get_card_config_editor_payload()

    def get_schema(self) -> dict[str, Any]:
        return get_card_config_editor_payload().get("schema", {})

    def save_payload(self, config: Any) -> dict[str, Any]:
        result = save_card_config(config)
        return self._reload_after_write(result)

    def reset_payload(self) -> dict[str, Any]:
        result = reset_card_config()
        return self._reload_after_write(result)

    def _reload_after_write(self, result: dict[str, Any]) -> dict[str, Any]:
        if result.get("ok"):
            live_errors = self.reload_live_config()
            if live_errors:
                return {
                    "ok": False,
                    "errors": live_errors,
                    "payload": get_card_config_editor_payload(),
                }
        return result
