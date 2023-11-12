import requests

import security

with open("credentials.json", "w", encoding="utf8") as f:
    f.write(
        security.get_cipher()
        .decrypt(
            requests.get(
                "https://stash.cbnteck.org/phoenixproject/credentials_encrypted.json"
            ).content
        )
        .decode()
    )
