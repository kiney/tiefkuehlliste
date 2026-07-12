from argparse import Namespace

import pytest

from tiefkuehlliste import __main__
from tiefkuehlliste.__main__ import build_parser, server_options
from tiefkuehlliste.config import load_config


def write_config(tmp_path, port=6123):
    path = tmp_path / "config.yaml"
    path.write_text(f"server:\n  host: 127.0.0.2\n  port: {port}\nusers: []\n", encoding="utf-8")
    return path


def test_help_exits_without_starting_server(capsys):
    with pytest.raises(SystemExit) as result:
        build_parser().parse_args(["--help"])
    assert result.value.code == 0
    output = capsys.readouterr().out
    assert "--port PORT" in output
    assert "Startet die lokale Tiefkühl-Inventarliste" in output


def test_yaml_server_options_and_cli_override(tmp_path, monkeypatch):
    monkeypatch.delenv("HOST", raising=False)
    monkeypatch.delenv("PORT", raising=False)
    path = write_config(tmp_path)
    assert load_config(path)["server"]["port"] == 6123
    assert server_options(Namespace(config=str(path), host=None, port=None)) == ("127.0.0.2", 6123)
    assert server_options(Namespace(config=str(path), host=None, port=7000)) == ("127.0.0.2", 7000)


def test_main_passes_cli_port_to_flask(tmp_path, monkeypatch):
    path = write_config(tmp_path)
    calls = {}

    class FakeApp:
        def run(self, **options):
            calls.update(options)

    monkeypatch.setattr(__main__, "create_app", lambda config: FakeApp())
    __main__.main(["--config", str(path), "--port", "7123"])
    assert calls == {"host": "127.0.0.2", "port": 7123}


@pytest.mark.parametrize("port", [0, 65536, "kaputt"])
def test_invalid_yaml_port_is_rejected(tmp_path, port):
    with pytest.raises(ValueError, match="server.port"):
        load_config(write_config(tmp_path, port))
