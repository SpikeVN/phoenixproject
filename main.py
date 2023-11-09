# Copyright (C) 2023  Nguyễn Tri Phương
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import importlib
import os
import configuration as cfg
import phoenix


def main():
    if "credentials.json" not in os.listdir():
        with open("credentials.json", "w") as f:
            f.write(os.environ.get("credentials_gcloud_sa"))
            print(f"written {os.environ.get('credentials_gcloud_sa')}")
    print(os.listdir())
    cfg.init_config_hive()
    bot = phoenix.Bot()
    for f in os.listdir("modules"):
        if f.endswith(".py"):
            m = importlib.import_module(f"modules.{f[:-3]}")
            bot.register_module(m)
    bot.run(cfg.get("credentials.email"), cfg.get("credentials.password"))


if __name__ == "__main__":
    main()
