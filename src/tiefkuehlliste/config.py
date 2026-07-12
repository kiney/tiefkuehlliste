import os
from pathlib import Path

import yaml


def default_config_path():
    return Path(__file__).resolve().parents[2] / "config/config.yaml"


def load_config(path=None):
    config_path = Path(path or os.getenv("TIEFKUEHLLISTE_CONFIG") or default_config_path())
    try:
        data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        data = {}
    if not isinstance(data, dict):
        raise ValueError(f"Konfiguration {config_path} muss ein YAML-Objekt enthalten.")
    server = data.get("server", {})
    if not isinstance(server, dict):
        raise ValueError("server muss ein YAML-Objekt sein.")
    try:
        port = int(server.get("port", 5000))
    except (TypeError, ValueError):
        raise ValueError("server.port muss eine ganze Zahl sein.") from None
    if not 1 <= port <= 65535:
        raise ValueError("server.port muss zwischen 1 und 65535 liegen.")
    data["server"] = {**server, "host": str(server.get("host", "127.0.0.1")), "port": port}
    return data
