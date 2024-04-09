from config import Config
import requests
import style
from logzero import logger
import json
from pygments import highlight, lexers, formatters
import pandas as pd
from parse_data import clean_table

def authenticate(config):
    '''
        Handle authentication to the API and set the access token

        @param config: Config Class containing different variables such as the email, password and token

    '''
    config.init_variables()
    payload = {
        "email": config.EMAIL,
        "password": config.PASSWORD
    }
    request = requests.Session()
    response = request.post(config.auth_url, json=payload)
    if response.status_code != 200:
        logger.critical(f"[{response.status_code}] | {response.json()['error']}")
        raise Exception(f"Authentication failed with status code {response.status_code}")
    logger.info(style.white.bold(f"[{response.status_code}] : User authenticated"))

    config.access_token = response.json().get("access_token")
    config.headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config.access_token}',
        'Origin': 'https://www.jinka.fr',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Sec-GPC': '1',
        'If-None-Match': 'W/f46-qWZd5Nq9sjWAv9cj3oEhFaxFuek',
        'TE': 'Trailers',
    }
    return None

def get_dashboard(config):
    '''
        Get the dashboard of the user

        Dashboard contains the following information:
        - account information: email, phone number, name, search criterias, etc...
        - ads: list of announces available for an alert (alert_id = config.TOKEN)

        @return: dict containing the dashboard that can be converted into a json or a dataframe afterwards
    '''
    return config.get(f"https://api.jinka.fr/apiv2/alert/{config.TOKEN}/dashboard")

def get_announces(config):
    '''
        Get the announces available for an alert

        @return: dict containing the announces that can be converted into a json or a dataframe afterwards
    '''
    return get_dashboard(config)['ads']


def pretty_print(dashboard):
    print(highlight(json.dumps(dashboard, indent=4), lexers.JsonLexer(), formatters.TerminalFormatter()))
    with open("data.json", "w") as f:
        f.write(json.dumps(dashboard, indent=4))

if __name__ == "__main__":
    config = Config()
    authenticate(config)
    announces_available = get_announces(config)
    dataframe = pd.DataFrame(announces_available)
    dataframe = clean_table(config.TOKEN, dataframe)
    dataframe.to_csv("announces.csv", index=False)
