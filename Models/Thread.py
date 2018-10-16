import threading
import uuid

class Thread:
    def __init__(self, target, args=None):
        thread = threading.Thread(target=target, args=args)
        # thread.daemon = True
        thread.start()
#
# class ID:
#     def __init(self):
#         pass
#     def get(self):
#         return str(uuid.uuid4())

class Cache:
    def __init__(self):
        pass
    def get(self, key, val):
        return self.client.hget(key, val)

    def set(self, key, subKey, newVal):
        return self.client.hset(key, subKey, newVal)
