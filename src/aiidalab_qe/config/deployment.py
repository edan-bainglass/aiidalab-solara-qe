import os

import solara.server.settings
from dotenv import load_dotenv

load_dotenv()


def get_token():
    return os.environ.get("JUPYTER_TOKEN", "")


def get_api_port():
    return os.environ.get("API_PORT", "")


def get_base_url():
    return solara.server.settings.main.base_url.rstrip("/")


def get_root_path():
    return solara.server.settings.main.root_path or ""


def get_api_url():
    root_path = get_root_path()
    base_url = ":".join(get_base_url().replace(root_path, "").split(":")[:2])
    api_port = get_api_port()
    return f"{base_url}:{api_port}/api/v1"
