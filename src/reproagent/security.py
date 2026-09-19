"""Shared guards that keep credential-shaped data out of durable records."""

from __future__ import annotations

import re
from collections.abc import Mapping

_SENSITIVE_KEY = re.compile(
    r"^(api_?key|access_?token|authorization|password|client_?secret|"
    r"private_?key|ssh_?key|credentials?)$",
    re.IGNORECASE,
)


def reject_sensitive_mapping(value: Mapping[str, object]) -> None:
    """Reject nested mappings whose keys indicate credential material."""

    for key, item in value.items():
        normalized = key.replace("-", "_").strip()
        if _SENSITIVE_KEY.fullmatch(normalized):
            raise ValueError(f"Sensitive field {key!r} is not allowed.")
        if isinstance(item, Mapping):
            reject_sensitive_mapping(item)
        elif isinstance(item, list):
            for nested in item:
                if isinstance(nested, Mapping):
                    reject_sensitive_mapping(nested)


def response_contains_secret(response_text: str, secret: str) -> bool:
    """Return whether a provider echoed its credential in response content."""

    return bool(secret) and secret in response_text
