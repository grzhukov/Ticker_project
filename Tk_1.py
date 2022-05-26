from tkinter import *
from tkinter import messagebox as mb
from tkinter.ttk import Combobox
from child_window import ChildWindow
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import random
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


class Window:

    def __init__(self, width, height, title='My_window', resizable=(False, False), icon=r'resources/IMG_1527.ico'):
        self.root = Tk() # the objecct of class tkinter window = Tk()
        self.root.title(title)
        self.root.geometry(f'{width}x{height}+200+200')
        self.root.resizable(resizable[0], resizable[1])

        if icon:
            self.root.iconbitmap(icon)

        self.a = [i for i in range(100)]
        self.numbers = Combobox(self.root, values=self.a, state="readonly")
        self.x = [0]
        self.y = [0]


    def run(self):
        self.draw_widgets()
        self.root.mainloop()

    def draw_widgets(self):
        Label(self.root, text="Choose a ticker:", justify=LEFT).pack()
        self.numbers.pack()

        # Label(self.root, text="Choose all or some tickers:", justify=LEFT).pack()
        # Combobox(self.root, values=("All", "Some"), justify=CENTER).pack()

        self.numbers.bind("<<ComboboxSelected>>", self.changed)


        #Button(self.root, text="Get", width=10, command=self.get_number).pack()

        Button(self.root, text="Quit", width=10, command=self.exit).pack()


    def changed(self, event):

        index = self.numbers.get()

        #random.seed(index)# зафиксировали сид рандома
        # self.x = [0]
        # self.y = [0]
        fig, ax = plt.subplots()
        [line] = ax.plot(self.y)


        def update(dy):
            self.x.append(self.x[-1] + 1)  # update data
            self.y.append(self.y[-1] + dy)
            #self.create_child((200, 100))
            line.set_xdata(self.x)  # update plot data
            line.set_ydata(self.y)
            ax.set_title(f'Mean = {np.mean(self.y):.4f} Volatility = {np.std(self.y):.4f} \n '
                         f'Observations {self.x[-1]} Max {max(self.y)}  Min {min(self.y)} ',
                         loc='left')

            ax.set_xlabel(f'{time.ctime()}')

            ax.relim()  # update axes limits
            ax.autoscale_view(True, True, True)
            return line, ax

        def generate_movement():
            yield -1 if random.random() < 0.5 else 1



        ani = animation.FuncAnimation(fig, update, generate_movement, interval=1000)
        plt.show()



    # def get_number(self):
    #     value = self.numbers.get()
    #     index = self.numbers.current()



    def exit(self):
        choice = mb.askyesno("Quit", "Do you want to quit?")
        if choice:
            self.root.destroy()


    def create_child(self, width, height, title='Child', resizeable=(False, False), icon=None):
        ChildWindow(self.root, width, height, title, resizeable, icon)



if __name__ == '__main__':
    window = Window(400, 300, 'Realtime data')

    #window.create_child(200, 100)

    window.run()
    time.sleep(10)
    # window.stop()


