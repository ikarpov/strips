from Tkinter import *
from towers3 import *
import threading

DH = 10
X = {'Pole1': 25, 'Pole2': 75, 'Pole3': 125}
W = {'Disk1': 25, 'Disk2': 30, 'Disk3': 35}
C = {'Disk1': 'red', 'Disk2': 'green', 'Disk3': 'blue'}

class StripsStateViewer:
    def __init__(self, lock = None):
        self.master = Tk()
        self.master.title('Towers of Hanoi planning state')
        self.canvases = []
        self.handles = {}
        self.push_canvas()
        self.plan = None
        self.lock = lock
        if self.lock:
            self.master.after(100, self.update_state)

    def push_canvas(self):
        canvas = Canvas(self.master, width=150, height=100)
        canvas.grid(row=0,column=len(self.canvases))
        canvas.create_rectangle(45/2, 50/2, 55/2, 190/2, fill="grey")
        canvas.create_rectangle(145/2, 50/2, 155/2, 190/2, fill="grey")
        canvas.create_rectangle(245/2, 50/2, 255/2, 190/2, fill="grey")
        canvas.create_rectangle(10/2, 130/2, 290/2, 190/2, fill = "grey")
        for disk in DISKS:
            self.handles[(canvas, disk)] = None
        self.canvases.append(canvas)

    def clear_canvas(self,canvas):
        for obj in DISKS:
            h = self.handles[(canvas, obj)]
            if h:
                canvas.delete(h)
                self.handles[(canvas, h)] = None

    def update_state(self):
        if not self.plan:
            self.master.after(50, self.update_state)
        else:
            self.master.after(1000, self.quit)
        if self.lock and self.lock.locked():
            self.lock.release()

    def quit(self):
        self.master.quit()

    def show_state(self, state, depth = 0, plan = []):
        if self.lock:
            self.lock.acquire()
        while depth > len(self.canvases) - 1:
            self.push_canvas()
        for i in range(depth, len(self.canvases)):
            self.clear_canvas(self.canvases[i])
        canvas = self.canvases[depth]
        for disk in DISKS:
            if self.handles[(canvas,disk)]:
                canvas.delete(self.handles[(canvas,disk)])
                self.handles[(canvas,disk)] = None
            h = get_height(state, disk) * DH
            pole = get_pole(state, disk)
            if pole is not None:
                x = X[pole]
                color = C[disk]
                width = W[disk]
                self.handles[(canvas,disk)] = \
                    canvas.create_rectangle(x-width/2, 150/2-h, x+width/2, 130/2 - h, fill = color)

    def plan_found(self, plan):
        self.plan = plan

    def run(self):
        mainloop()

def show_state(state = INIT):
    viewer = StripsStateViewer()
    viewer.show_state(state)
    mainloop()

def demo_planner(planner):
    lock = threading.Lock()
    viewer = StripsStateViewer(lock)
    viewer.show_state(INIT)
    thread = threading.Thread(target=planner, args=[viewer,])
    thread.start()
    mainloop()
    thread.join()
    return viewer.plan

if __name__ == "__main__":
    show_state()
