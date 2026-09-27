import argparse
import os

from .app import create_app
from .config import default_config_path, load_config


def build_parser():
    parser = argparse.ArgumentParser(
        prog="tiefkuehlliste",
        description="Startet die lokale Vorratsliste.",
    )
    parser.add_argument(
        "--config",
        default=os.getenv("TIEFKUEHLLISTE_CONFIG", str(default_config_path())),
        help="Pfad zur YAML-Konfiguration (Standard: %(default)s)",
    )
    parser.add_argument("--host", help="Bind-Adresse; überschreibt server.host aus YAML")
    parser.add_argument(
        "--port",
        type=int,
        choices=range(1, 65536),
        metavar="PORT",
        help="TCP-Port; überschreibt server.port aus YAML",
    )
    return parser


def server_options(args):
    config = load_config(args.config)
    host = args.host or os.getenv("HOST") or config["server"]["host"]
    env_port = os.getenv("PORT")
    port = (
        args.port
        if args.port is not None
        else int(env_port)
        if env_port
        else config["server"]["port"]
    )
    return host, port


def main(argv=None):
    args = build_parser().parse_args(argv)
    host, port = server_options(args)
    app = create_app({"CONFIG_FILE": args.config})
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
