import time
def function(path, text):
    with open(path, mode='a') as f:
        f.write(text)
