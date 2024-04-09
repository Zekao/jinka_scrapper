import termios
import sys
import tty
import dotenv
import requests
from logzero import logger

class Config:
    def __init__(self) -> None:
        self.EMAIL = None
        self.PASSWORD = None
        self.TOKEN = None
        self.access_token = ''
        self.auth_url = "https://api.jinka.fr/apiv2/user/auth"
        self.headers = {}

    def init_variables(self) -> None:
        self.EMAIL = dotenv.get_key(dotenv.find_dotenv(), "EMAIL")
        self.PASSWORD = dotenv.get_key(dotenv.find_dotenv(), "PASSWORD")
        self.TOKEN = dotenv.get_key(dotenv.find_dotenv(), "TOKEN")
        for key, value in self.__dict__.items():
            if value is None:
                if key == "EMAIL":
                    self.EMAIL = self.getpass_masked("Please enter your email: ")
                elif key == "PASSWORD":
                    self.PASSWORD = self.getpass_masked("Please enter your password: ")
                elif key == "TOKEN":
                    self.TOKEN = self.getpass_masked("Please enter your token: ")
                else:
                    raise Exception("Unknown variable")
                with open(".env", "a") as f:
                    f.write(f"\n{key}={self.__dict__[key]}\n")

    def getpass_masked(self, prompt="Password: ") -> str:
        print(prompt, end='', flush=True)
        password = ""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            while True:
                char = sys.stdin.read(1)
                if char == '\r' or char == '\n':
                    print()
                    break
                elif char == '\x08' or char == '\x7f':
                    if password:
                        password = password[:-1]
                        print('\b \b', end='', flush=True)
                else:
                    password += char
                    print('*', end='', flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return password

    def get(self, url) -> dict | None:
        try:
            response = requests.get(url, headers=self.headers)
            if (response.status_code != 200):
                print(response.content)
                raise Exception(f"GET request failed with status code {response.status_code}")
            return response.json()
        except Exception as e:
            logger.critical(e)
            raise Exception(e)

if __name__ == "__main__":
    config = Config()
    config.init_variables()
