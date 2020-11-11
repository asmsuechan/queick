import time
def function(arg1, arg2):
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print(arg1, "+", arg2, "=", arg1 + arg2)
