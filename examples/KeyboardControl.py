#!/usr/bin/env python3

from usbroboarm import Arm
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import time
import os

# to run program
# go into command line in the correct folder
# enter 'sudo python3 Keyboard.py' to run

# this line changes a global setting to prevent the TK window
# from queueing too many events, so when you stop pressing a key the arm will stop
os.system("xset r off")

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Keyboard Control of Robot Arm")
        self.arm = Arm()
##        self.arm.command_timeout = 50 # if arm still timeout's then uncomment this line and increase value

        f = tk.Frame(self)
        f.pack(side="top", expand=True, fill="x")

        f1 = tk.Frame(f, bd=1, relief="sunken")
        f1.pack(side="left")

        tk.Label(f1, text="Function:")       .grid(column=1, row=1, sticky="w")
        tk.Label(f1, text="Key:")            .grid(column=2, row=1, sticky="w")
        
        tk.Label(f1, text="Base Left:")      .grid(column=1, row=2, sticky="w")
        tk.Label(f1, text="Left")            .grid(column=2, row=2, sticky="w")
        tk.Label(f1, text="Base Right:")     .grid(column=1, row=3, sticky="w")
        tk.Label(f1, text="Right")           .grid(column=2, row=3, sticky="w")
        tk.Label(f1, text="Shoulder Up:")    .grid(column=1, row=4, sticky="w")
        tk.Label(f1, text="Up")              .grid(column=2, row=4, sticky="w")
        tk.Label(f1, text="Shoulder Down:")  .grid(column=1, row=5, sticky="w")
        tk.Label(f1, text="Down")            .grid(column=2, row=5, sticky="w")

        f2 = tk.Frame(f, bd=1, relief="sunken")
        f2.pack(side="left")
        
        tk.Label(f2, text="Function:")       .grid(column=3, row=1, sticky="w")
        tk.Label(f2, text="Key:")            .grid(column=4, row=1, sticky="w")
        
        tk.Label(f2, text="Elbow Up:")       .grid(column=3, row=2, sticky="w")
        tk.Label(f2, text="Home")            .grid(column=4, row=2, sticky="w")
        tk.Label(f2, text="Elbow Down:")     .grid(column=3, row=3, sticky="w")
        tk.Label(f2, text="End")             .grid(column=4, row=3, sticky="w")
        tk.Label(f2, text="Wrist Up:")       .grid(column=3, row=4, sticky="w")
        tk.Label(f2, text="Insert")          .grid(column=4, row=4, sticky="w")
        tk.Label(f2, text="Wrist Down:")     .grid(column=3, row=5, sticky="w")
        tk.Label(f2, text="Delete")          .grid(column=4, row=5, sticky="w")

        f3 = tk.Frame(f, bd=1, relief="sunken")
        f3.pack(side="left", fill="y")
        
        tk.Label(f3, text="Function:")       .grid(column=5, row=1, sticky="w")
        tk.Label(f3, text="Key:")            .grid(column=6, row=1, sticky="w")
        
        tk.Label(f3, text="Grip Open:")      .grid(column=5, row=2, sticky="w")
        tk.Label(f3, text="Page-Up")         .grid(column=6, row=2, sticky="w")
        tk.Label(f3, text="Grip Close:")     .grid(column=5, row=3, sticky="w")
        tk.Label(f3, text="Page-Down")       .grid(column=6, row=3, sticky="w")
        tk.Label(f3, text="Toggle Light:")   .grid(column=5, row=4, sticky="w")
        tk.Label(f3, text="L")               .grid(column=6, row=4, sticky="w")
        
        self.c_window = ScrolledText(self, width=20, height=20)
        self.c_window.pack(side="top", expand=True, fill="both")

        self.count = 1

        self.lit = False

        self.bind("<FocusOut>", self.stop_all)
        self.bind("<Escape>", self.stop_all)
        self.bind("<l>", self.toggle_light)
        self.bind("<KeyPress-Prior>", self.grip_open) # page up key
        self.bind("<KeyRelease-Prior>", self.grip_stop) # page up key
        self.bind("<KeyPress-Next>", self.grip_close) # page down key
        self.bind("<KeyRelease-Next>", self.grip_stop) # page down key
        
        self.bind("<KeyPress-Left>", self.base_left)
        self.bind("<KeyRelease-Left>", self.base_stop)
        self.bind("<KeyPress-Right>", self.base_right)
        self.bind("<KeyRelease-Right>", self.base_stop)

        self.bind("<KeyPress-Up>", self.shoulder_up)
        self.bind("<KeyRelease-Up>", self.shoulder_stop)
        self.bind("<KeyPress-Down>", self.shoulder_down)
        self.bind("<KeyRelease-Down>", self.shoulder_stop)

        self.bind("<KeyPress-Home>", self.elbow_up)
        self.bind("<KeyRelease-Home>", self.elbow_stop)
        self.bind("<KeyPress-End>", self.elbow_down)
        self.bind("<KeyRelease-End>", self.elbow_stop)

        self.bind("<KeyPress-Insert>", self.wrist_up)
        self.bind("<KeyRelease-Insert>", self.wrist_stop)
        self.bind("<KeyPress-Delete>", self.wrist_down)
        self.bind("<KeyRelease-Delete>", self.wrist_stop)

    def message(self, message):
        if (self.count == 1):
            pass
        else:
            self.c_window.insert("end", "\n")
        self.c_window.insert("end", str(self.count) + "\t" + message)
        self.c_window.see("end")
        self.count += 1

    def stop_all(self, event=None):
        self.message("Stop All")
        self.arm.stop_moving()

    def base_left(self, event=None):
        self.message("Base Left")
        self.arm.base_left()

    def base_right(self, event=None):
        self.message("Base Right")
        self.arm.base_right()

    def base_stop(self, event=None):
        self.message("Base Stop")
        time.sleep(0.1)
        self.arm.stop_moving()

    def shoulder_up(self, event=None):
        self.message("Shoulder Up")
        self.arm.shoulder_up()

    def shoulder_down(self, event=None):
        self.message("Shoulder Down")
        self.arm.shoulder_down()

    def shoulder_stop(self, event=None):
        self.message("Shoulder Stop")
        time.sleep(0.1)
        self.arm.stop_moving()

    def elbow_up(self, event=None):
        self.message("Elbow Up")
        self.arm.elbow_up()

    def elbow_down(self, event=None):
        self.message("Elbow Down")
        self.arm.elbow_down()
        
    def elbow_stop(self, event=None):
        self.message("Elbow Stop")
        time.sleep(0.1)
        self.arm.stop_moving()

    def wrist_up(self, event=None):
        self.message("Wrist Up")
        self.arm.wrist_up()

    def wrist_down(self, event=None):
        self.message("Wrist Down")
        self.arm.wrist_down()

    def wrist_stop(self, event=None):
        self.message("Wrist Stop")
        time.sleep(0.1)
        self.arm.stop_moving()

    def grip_open(self, event=None):
        self.message("Grip Open")
        self.arm.grip_open()

    def grip_close(self, event=None):
        self.message("Grip Close")
        self.arm.grip_close()

    def grip_stop(self, event=None):
        self.message("Grip Stop")
        time.sleep(0.1)
        self.arm.stop_moving()

    def toggle_light(self, event=None):
        self.message("Toggle Light")
        if self.lit:
            self.arm.light_off()
            self.lit = False
        else:
            self.arm.light_on()
            self.lit = True
    
if __name__ == "__main__":
    app = App()
    app.mainloop()
    os.system("xset r on") # change the queue setting back
