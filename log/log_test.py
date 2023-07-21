import sys

class Logger(object):
    def __init__(self, filename="Default.log", cache_size=10):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
        self.cache_size = cache_size
        self.cache = []

    def write(self, message):
        self.terminal.write(message)
        self.cache.append(message)
        if len(self.cache) >= self.cache_size:
            self.flush()

    def flush(self):
        self.log.write(''.join(self.cache))
        self.log.flush()  # 强制写入文件
        self.cache = []

    def __del__(self):
        self.flush()
        self.log.close()

sys.stdout = Logger("yourlog.txt")
for i in range(100):
    print(f"Hello, world! {i}")