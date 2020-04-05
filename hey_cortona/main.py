from bot_interaction import api
from config.app_config import AppConfig


def main():
    api.start_server(AppConfig.from_env())


if __name__ == '__main__':
    main()
