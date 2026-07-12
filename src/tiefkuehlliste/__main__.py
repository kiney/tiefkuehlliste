import os

from .app import create_app


def main():
    app = create_app()
    app.run(host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", "5000")))


if __name__ == "__main__":
    main()
