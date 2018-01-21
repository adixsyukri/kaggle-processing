import requests
import csv

class Kaggle(object):

    KAGGLE_LOGIN = "https://www.kaggle.com/account/login"
    SESSION = requests.Session()
    INDEX = 0

    def __init__(self, settings):
        self._login(settings)

    def _login(self, settings):
        print("Login to Kaggle")
        return self.SESSION.post(self.KAGGLE_LOGIN, data = settings['auth'])
    
    def get_data(self, data_url):
        print("Getting dataset")
        return self.SESSION.get(data_url)

    def to_array(self, record, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL):
        print("Transform data from text to array")
        reader = csv.reader(record, delimiter=delimiter, quotechar=quotechar, quoting=quoting)
        return [x for x in reader]