import threading
import uuid

class Thread:
    def __init__(self, target, args=None):
        thread = threading.Thread(target=target, args=args)
        # thread.daemon = True
        thread.start()
