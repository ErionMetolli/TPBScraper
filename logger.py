from datetime import datetime

class Logger:
    def __init__(self, class_name):
        self.class_name = class_name

    def log(self, message):
        print('[' + str(datetime.now()) + '] ' + self.class_name + ': ' + message)
