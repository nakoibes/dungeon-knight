from application import Application
from application.config import Config


def main(config_cls=Config):
    Application("dfigjgfh", config_cls()).run()


if __name__ == '__main__':
    main(Config)
