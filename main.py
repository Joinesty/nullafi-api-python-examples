"""
Nullafi API example
"""

import urllib.request
import os
import ast
import json

def load_env(filepath=None):
    if filepath and os.path.exists(filepath):
        pass
    else:
        if not os.path.exists('.env'):
            return False
        filepath = os.path.join('.env')

    for key, value in _get_line_(filepath):
        os.environ.setdefault(key, str(value))
    return True

def _get_line_(filepath):
    for line in open(filepath):
        line = line.strip()
        if line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip().upper()
        value = value.strip()

        if not (key and value):
            continue

        try:
            value = ast.literal_eval(value)
        except (ValueError, SyntaxError):
            pass

        yield (key, value)

def authenticate():
    req_data = {
        "apiKey" : os.environ["NULLAFI_API_KEY"]
    }

    req = urllib.request.Request(url=os.environ["NULLAFI_API_URL"] + "/authentication/token", 
        data=bytes(json.dumps(req_data), 
        encoding="utf-8"), 
        method='POST', 
        headers={'content-type': 'application/json'}
    )

    with urllib.request.urlopen(req, timeout=5) as f:
        if (f.status == 200):
            res_body = f.read()
            res_json = json.loads(res_body.decode("utf-8"))
            return res_json['token']

def list_vaults(api_token):
    req = urllib.request.Request(url=os.environ["NULLAFI_API_URL"] + "/v2/vault", 
        method='GET', 
        headers={'Authorization': api_token}
    )

    with urllib.request.urlopen(req, timeout=5) as f:
        if (f.status == 200):
            res_body = f.read()
            res_json = json.loads(res_body.decode("utf-8"))
            return res_json

    
if __name__ == "__main__":
    """
    Loading environment varibles from .env file
    Please confirm you have a .env file in the place
    """
    load_env()

    """
    Doing API authentication using the API KEY from env file
    """
    api_token = authenticate()
    print(f"Your token is: {api_token}")

    """
    Getting the list of vaults available
    After sign up on the dashboard you have 1 Communication vaults and 1 Static vault enabled by default.
    """
    vault_list = list_vaults(api_token)
    print(f"List of vaults is: {vault_list}")