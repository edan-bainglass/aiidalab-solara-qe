import os


def _app_command(port):
    os.environ["SOLARA_APP"] = "src/aiidalab_qe/main.py"
    os.environ["APP_PORT"] = str(port)
    return [
        "uvicorn",
        "aiidalab_qe.api.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        str(port),
        "--root-path",
        "/qe",
        "--reload",
    ]


def setup_app():
    icon_path = os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../assets/images",
            "icon.svg",
        )
    )
    return {
        "command": _app_command,
        "timeout": 60,
        "absolute_url": False,
        "launcher_entry": {
            "title": "AiiDAlab Quantum ESPRESSO",
            "icon_path": icon_path,
        },
    }
