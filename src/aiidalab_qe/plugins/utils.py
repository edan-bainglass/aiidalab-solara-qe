from __future__ import annotations

import typing as t

from aiida.engine import WorkChain
from importlib_metadata import EntryPoint, entry_points

if t.TYPE_CHECKING:
    from aiidalab_qe.plugins.models import PluginResourcesModel, PluginSettingsModel
    from aiidalab_qe.plugins.types import PluginResultsComponent


def print_error(entry_point, e):
    print(f"\033[91mFailed to load plugin entry point {entry_point.name}.\033[0m")
    print(
        "\033[93mThis may be due to compatibility issues with the current QEApp version.\033[0m"
    )
    print("\033[93mPlease contact the plugin author for further assistance.\033[0m")
    print(
        "\033[93mThus, the plugin will not be available. However, you can still use the rest of the app.\033[0m"
    )
    print(f"\033[91mError message: {e}\033[0m\n")


def get_entries(entry_point_name: str) -> dict[str, dict]:
    entries = {}
    entry_point: EntryPoint
    for entry_point in entry_points(group=entry_point_name):
        try:
            if entry_point.name in entries:
                continue
            loaded_entry_point = entry_point.load()
            entries[entry_point.name] = loaded_entry_point
        except Exception as e:
            print_error(entry_point, e)
    return entries


T = t.TypeVar("T")


def get_plugin_attribute(attribute: str) -> dict[str, T]:  # type: ignore
    entries = get_entries("aiidalab_qe.properties")
    return {
        name: t.cast(T, entry_point.get(attribute))
        for name, entry_point in entries.items()
        if entry_point.get(attribute, False)
    }


def get_plugin_titles() -> dict[str, str]:
    return get_plugin_attribute("title")


def get_plugin_settings() -> dict[str, PluginSettingsModel]:
    return get_plugin_attribute("settings")


def get_plugin_resources() -> dict[str, PluginResourcesModel]:
    return get_plugin_attribute("resources")


def get_plugin_workchains() -> dict[str, WorkChain]:
    return get_plugin_attribute("workchain")


def get_plugin_results() -> dict[str, PluginResultsComponent]:
    return get_plugin_attribute("results")
