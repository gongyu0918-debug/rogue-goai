"""Avoid Windows WMI stalls during frozen application startup.

Some Python and packaging helpers ask ``platform.win32_ver()`` while the
application is still booting. On affected Windows installs, the stdlib WMI
query can hang before our server prints logs or binds a port. Returning an
empty WMI result keeps ``platform`` on its registry/version fallback path.
"""

from __future__ import annotations

import platform


def _skip_wmi_query(*_args, **_kwargs):
    raise OSError("WMI query skipped during frozen startup")


if hasattr(platform, "_wmi_query"):
    platform._wmi_query = _skip_wmi_query
