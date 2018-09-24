from datetime import datetime

class Logger:
    def __init__(self, class_name):
        self.class_name = class_name

    def log(self, message):
        text = '[' + str(datetime.now()) + '] ' + self.class_name + ': ' + message
        print(text)
        with open('log.txt', 'a') as f:
            f.write(text + '\n')
