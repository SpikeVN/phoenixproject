import importlib
import os
import configuration as cfg
import phoenix


def main():
    cfg.init_config_hive()
    if "credentials.json" not in os.listdir():
        with open("credentials.json", "w") as f:
            f.write(cfg.get("credentials.gcloud.sa"))
    bot = phoenix.Bot()
    for f in os.listdir("modules"):
        if f.endswith(".py"):
            m = importlib.import_module(f"modules.{f[:-3]}")
            bot.register_module(m)
    bot.run(cfg.get("credentials.email"), cfg.get("credentials.password"))


if __name__ == "__main__":
    main()
