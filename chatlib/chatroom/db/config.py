import os
import json
from pathlib import Path

def get_db_secrets():
    root_dir = Path(__file__).parents[3]
    secrets_file = os.path.join(root_dir, 'secrets.json')
    with open(secrets_file) as f:
        secrets = json.load(f)

    secrets['database_uri'] = "postgresql://{username}:{password}@{host}/{database}".format(
        username=secrets['username'],
        password=secrets['password'],
        host=secrets['host'],
        database=secrets['database']
    )
    return secrets

_secrets = get_db_secrets()

def get_db_uri():
    return _secrets['database_uri']
