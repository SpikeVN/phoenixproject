import os

with open("credentials.json", "w", encoding="utf8") as f:
    f.write(os.environ["credentials_gcloud_sa"])
#
# if not os.path.exists("tmp"):
#     os.mkdir("tmp")
# os.system(
#     "cd tmp && wget https://stash.cbnteck.org/phoenixproject/geckodriver-v0.33.0-linux64.tar.gz"
# )
# if not os.path.exists("bin"):
#     os.mkdir("bin")
# os.system("cd bin && tar -xf ../tmp/geckodriver-v0.33.0-linux64.tar.gz")
