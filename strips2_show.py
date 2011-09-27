from Tkinter import *
from towers3 import *
import threading

DH = 20
X = {'Pole1': 50, 'Pole2': 150, 'Pole3': 250}
W = {'Disk1': 50, 'Disk2': 60, 'Disk3': 70}
C = {'Disk1': 'red', 'Disk2': 'green', 'Disk3': 'blue'}

def get_height(state, disk):
    """ get the height of the disk given the state """
    for p in state:
        if p[0] == 'On' and p[1] == disk:
            return 1 + get_height(state - set([p]), p[2])
    return 0

def get_pole(state, disk):
    """ get the pole of the disk given the state """
    for p in state:
        if p[0] == 'On' and p[1] == disk:
            if p[2] in POLES:
                return p[2]
            else:
                return get_pole(state - set([p]), p[2])
    return None

class StripsStateViewer:
    def __init__(self, lock = None):
        self.master = Tk()
        self.master.title('Towers of Hanoi planning state')
        self.w = Canvas(self.master, width=300, height=200)
        self.w.pack()
        self.w.create_rectangle(45, 50, 55, 190, fill="grey")
        self.w.create_rectangle(145, 50, 155, 190, fill="grey")
        self.w.create_rectangle(245, 50, 255, 190, fill="grey")
        self.w.create_rectangle(10, 130, 290, 190, fill = "grey")
        self.handles = {}
        for disk in DISKS:
            self.handles[disk] = None
        self.lock = lock
        if self.lock:
            self.w.after(50, self.update_state)

    def update_state(self):
        if self.lock:
            self.w.after(50, self.update_state)
            if self.lock.locked():
                self.lock.release()

    def draw_state(self, state):
        if self.lock:
            self.lock.acquire()
        for disk in DISKS:
            if self.handles[disk]:
                self.w.delete(self.handles[disk])
                self.handles[disk] = None
            h = get_height(state, disk) * 20
            pole = get_pole(state, disk)
            if pole is not None:
                x = X[pole]
                color = C[disk]
                width = W[disk]
                self.handles[disk] = \
                    self.w.create_rectangle(x-width/2, 150-h, x+width/2, 130 - h, fill = color)

    def run(self):
        mainloop()

def show_state(state = INIT):
    viewer = StripsStateViewer()
    viewer.draw_state(state)
    mainloop()

def demo_planner(planner):
    lock = threading.Lock()
    viewer = StripsStateViewer(lock)
    viewer.draw_state(INIT)
    thread = threading.Thread(target=planner, args=[viewer.draw_state,])
    thread.start()
    mainloop()
    thread.join()

if __name__ == "__main__":
    show_state()
