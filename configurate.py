import configparser

tokens = ["zxcqwe"]

config = configparser.ConfigParser()
config.read("settings.ini")
config.set("Bot", "bot_tokens", config["Bot"]["bot_tokens"] +";" + ";".join(tokens))


with open("settings.ini", "w") as config_file:
    config.write(config_file)
