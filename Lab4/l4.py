import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt
import matplotlib.lines
import matplotlib.patches
from tkinter import *
from tkinter.ttk import *
import random


def clipping(lines, window):
    def get_bytes_point(point, window):
        x, y = point
        x_min, x_max = sorted([window[0][0], window[1][0]])
        y_min, y_max = sorted([window[0][1], window[1][1]])

        if x_min <= x <= x_max and y_min <= y <= y_max:
            return 0
        elif x < x_min:
            return 1 if y_min <= y <= y_max else 2
        elif x > x_max:
            return 4 if y_min <= y <= y_max else 5
        else:
            return 6 if y < y_min else 8 if y > y_max else 10

    points = []
    for i in range(4):
        for j in range(2):
            points.append(get_bytes_point(lines[i][j], window))

    mas_in = []
    for i in range(0, len(points), 2):
        if 0 in points[i:i+2]:
            mas_in.append(1)
        elif points[i] == points[i+1]:
            mas_in.append(0)
        else:
            result = 2
            line = lines[(i // 2)]
            for k in range(min(line[0][0], line[1][0]), max(line[0][0], line[1][0]), 1):
                y = (k - line[0][0]) / (line[1][0] - line[0][0]) * (line[1][1] - line[0][1]) + line[0][1]
                point0 = get_bytes_point((k, y), window)
                point1 = get_bytes_point((k, y), window)
                if 0 in [point0, point1]:
                    result = 1
                    break
                elif point0 != point1:
                    result = 2
            mas_in.append(result)

    return mas_in


def draw_lines(lines, window, mas_true_points):
    colors = ['red', 'lime']

    for i in range(4):
        color = colors[0]
        if mas_true_points[i] == 1:
            color = colors[1]
        plt.plot([lines[i][0][0], lines[i][1][0]], [lines[i][0][1], lines[i][1][1]], color=color)

    plt.plot([window[0][0], window[1][0]], [window[0][1], window[0][1]], color='orange')
    plt.plot([window[0][0], window[0][0]], [window[0][1], window[1][1]], color='orange')
    plt.plot([window[0][0], window[1][0]], [window[1][1], window[1][1]], color='orange')
    plt.plot([window[1][0], window[1][0]], [window[0][1], window[1][1]], color='orange')

    plt.show()

def generate_lines():
    coordinates = np.array([[[0, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0], [0, 0]]])
    N = random.randint(5, 1000)
    for i in range(4):
        coordinates[i][0][0], coordinates[i][0][1], coordinates[i][1][0], coordinates[i][1][1] = random.randint(0, N),\
            random.randint(0, N), random.randint(0, N), random.randint(0, N)
    return coordinates


def main_window():
    res_points = generate_lines()
    window_points = np.array([[0, 0], [0, 0]])

    def counts():
        point = [0.0, 0.0]
        window_points[0][0] = float(x1_field.get())
        window_points[0][1] = float(y1_field.get())
        res_points[0] = tuple(point.copy())
        window_points[1][0] = float(x2_field.get())
        window_points[1][1] = float(y2_field.get())
        res_points[1] = tuple(point.copy())

    def click():
        counts()
        res_points = generate_lines()
        mas_true_points = clipping(res_points, window_points)
        draw_lines(res_points, window_points, mas_true_points)


    window = Tk()
    window.title("Лаб. работа №4")
    window.geometry('300x200')
    window.resizable(False, False)

    Label(window, text="Введите координаты окна", font=("Consolas", 14)).place(x=35, y=10)

    Label(window, text="x1: ", font=("Consolas", 14)).place(x=15, y=50)
    x1_field = Entry(window, width=10)
    x1_field.place(x=50, y=50)
    Label(window, text="y1: ", font=("Consolas", 14)).place(x=155, y=50)
    y1_field = Entry(window, width=10)
    y1_field.place(x=190, y=50)

    Label(window, text="x2: ", font=("Consolas", 14)).place(x=15, y=90)
    x2_field = Entry(window, width=10)
    x2_field.place(x=50, y=90)
    Label(window, text="y2: ", font=("Consolas", 14)).place(x=155, y=90)
    y2_field = Entry(window, width=10)
    y2_field.place(x=190, y=90)

    ok_button = Button(window, text="Ok",  command=click)
    ok_button.place(x=108, y=150)

    window.mainloop()


if __name__ == "__main__":
    main_window()