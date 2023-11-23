import os
import base64
import security


def assure_dependencies():
    with open("credentials.json", "w", encoding="utf8") as f:
        f.write(
            security.get_cipher()
            .decrypt(base64.b64decode(os.environ["credentials_credentials_enc"]))
            .decode()
        )


assure_dependencies()
