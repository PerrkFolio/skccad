import configparser


def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Connect")
    config.set("Connect", "db_host", "localhost")
    config.set("Connect", "db_name", "skccad")
    config.set("Connect", "db_user", "goofy")
    config.set("Connect", "db_pass", "L0l!k1510")

    with open(path, "w") as config_file:
        config.write(config_file)


if __name__ == "__main__":
    path = "database.ini"
    createConfig(path)