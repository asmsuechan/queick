import time
import urllib.request
def function(arg1, arg2):
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print(arg1, "+", arg2, "=", arg1 + arg2)

def function2(arg):
    start_time = time.time()

    # with urllib.request.urlopen('https://moriokalab.com') as f:
    #     pass

    end_time = time.time()

    print("Time:", end_time - start_time)
    # time.sleep(1)
    # print(arg)
