import time
def function(arg1, arg2):
    time.sleep(1)
    raise Exception("test") from None
    print(arg1, "+", arg2, "=", arg1 + arg2)

def function2(arg):
    time.sleep(1)
    raise Exception("test2") from None
