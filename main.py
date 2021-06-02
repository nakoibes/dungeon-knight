from application import Config, Application


def main(config_cls=Config):
    Application("MyApp", config_cls()).run()


if __name__ == '__main__':
    main(Config)
