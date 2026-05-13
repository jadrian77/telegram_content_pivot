import safe_load_config
from app import app as App


def get_config():
    config = safe_load_config.load_config()
    print("config check finish.")
    return config


def stop():
    print("exit.")


def main():
    print("start running...")
    config = get_config()
    app = App()
    app.run(config)
    stop()


if __name__ == "__main__":
    main()
