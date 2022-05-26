# импортируем библиотеки
from tkinter import *
from tkinter import messagebox as mb
from tkinter.ttk import Combobox
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# создаём класс
class Window:

    def __init__(self, width, height, title='My_window', resizable=(False, False), icon=None):
        self.root = Tk()
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

        # при выбое числа номера тикера из выпадающего списка, запуск функции происходит не
        # через стандартную command, как при нажатии кнопки, а черз bind, в который передаем функцию

        self.numbers.bind("<<ComboboxSelected>>", self.changed)

        # кнопка - уйти/остаться
        Button(self.root, text="Quit", width=10, command=self.exit).pack()


    def changed(self, event):
        index = self.numbers.get()
        #random.seed(index)# можем зафиксировали сид рандома
        fig, ax = plt.subplots()
        [line] = ax.plot(self.y) # будет соединять точки


        def update(new_y):
            self.x.append(self.x[-1] + 1)
            self.y.append(self.y[-1] + new_y) # добавялем в списки обновляемые данные
            line.set_xdata(self.x)  # обновляем точки
            line.set_ydata(self.y)
            ax.set_title(f'Mean = {np.mean(self.y):.4f} Volatility = {np.std(self.y):.4f} \n '
                         f'Observations {self.x[-1]} Max {max(self.y)}  Min {min(self.y)} ',
                         loc='left')

            ax.set_xlabel(f'{time.ctime()}')

            ax.relim()  # обновялем пределы осей
            ax.autoscale_view(True, True, True)
            return line, ax

        # генерация случайных величин, возвращаем шаги случайного процесса +1/-1
        def generate_movement():
            yield -1 if random.random() < 0.5 else 1

        # непосредственная анимация графика, запускает функции внутри, интервал обновления раз в секунду
        ani = animation.FuncAnimation(fig, update, generate_movement, interval=1000)
        plt.show()

    def exit(self):
        choice = mb.askyesno("Quit", "Do you want to quit?")
        if choice:
            self.root.destroy()

if __name__ == '__main__':
    window = Window(400, 300, 'Realtime data')
    window.run()
    time.sleep(10)
    window.stop()


