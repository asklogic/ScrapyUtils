import signal

# Define signal handler function
def myHandler(signum, frame):
    """
    Args:
        signum:
        frame:
    """
    print("Now, it's the time")
    exit()

# register signal.SIGALRM's handler
signal.signal(signal.SIGALRM, myHandler)
signal.alarm(5)
while True:
    print('not yet')