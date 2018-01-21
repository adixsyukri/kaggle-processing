import boto3

class S3(object):

    def __init__(self, settings):
        self.ACCESS_KEY = settings['aws']['access']
        self.SECRET_KEY = settings['aws']['secret']
    
    def get_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=self.ACCESS_KEY,
            aws_secret_access_key=self.SECRET_KEY
        )
