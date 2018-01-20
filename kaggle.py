import requests

class Kaggle(object):

    KAGGLE_LOGIN = "https://www.kaggle.com/account/login"
    SESSION = requests.Session()

    def __init__(self, data_url, settings):
        self.data_url = data_url
        self._login()

    def _login(self):
        print("Login to Kaggle")
        return self.SESSION.post(self.KAGGLE_LOGIN, data = settings['auth'])
    
    def get_data(self):
        print("Getting datast")
        response = self.SESSION.get(self.data_url)
        print("Transform data from text to array")
        return [row.split(',') for row in response.content.split('\r\n')]