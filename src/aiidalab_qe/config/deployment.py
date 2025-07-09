import os

import solara.server.settings


def get_token():
    return os.environ.get("JUPYTER_TOKEN", "")

def get_base_url():
    return solara.server.settings.main.base_url.rstrip("/")


def get_root_path():
    return solara.server.settings.main.root_path or ""
