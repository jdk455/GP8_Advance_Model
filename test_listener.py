from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class MyHandler(FileSystemEventHandler):
    def __init__(self, target_file):
        self.target_file = target_file
        self.last_content = self.read_file_content()

    def read_file_content(self):
        try:
            with open(self.target_file, 'r',encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return None

    def on_modified(self, event):
        if event.src_path == self.target_file:
            new_content = self.read_file_content()
            if new_content != self.last_content:
                print(f'File {event.src_path} content has been modified, new content is:')
                print(new_content)
                self.last_content = new_content

def watch_file(file_path):
    event_handler = MyHandler(file_path)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(file_path))
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Example usage
watch_file(r'D:\Code\GP8_Advance_Model\motor_command.txt')