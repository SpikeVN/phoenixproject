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
import base64
import importlib
import os
import pickle
import ensuredeps
import api
import database

import requests

import configuration as cfg

import logutils
import phoenix
import security


def main():
    logutils.set_min_level(logutils.INFO)
    cfg.init_config_hive()
    api.do_stuff()
    bot = phoenix.Bot()
    for f in os.listdir("modules"):
        if f.endswith(".py"):
            m = importlib.import_module(f"modules.{f[:-3]}")
            bot.register_module(m)
    session = pickle.loads(
        security.get_cipher().decrypt(
            base64.b64decode(
                database.DB.collection("phoenixfb")
                .document("encryptedSession")
                .get()
                .get("value")
            )
        )
    )
    bot.run(
        cfg.get("credentials.email"),
        cfg.get("credentials.password"),
        # use_selenium=True
        session=session,
    )


if __name__ == "__main__":
    main()
