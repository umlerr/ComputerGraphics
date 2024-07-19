import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import *

N = 15


def bilinear_surface(verts):
    def get_matrix():
        dots = np.linspace(0, 1, N)
        all_verts = np.transpose([np.tile(dots, len(dots)), np.repeat(dots, len(dots))])
        for i in range(len(all_verts)):
            matrix_a = np.array([1 - all_verts[i][0], all_verts[i][0]])
            matrix_b = np.array([[1 - all_verts[i][1]], [all_verts[i][1]]])

            result[i] = np.dot(bilinear_matrix[0][0], matrix_a[0] * matrix_b[0][0]) + np.dot(bilinear_matrix[0][1], matrix_a[0] * matrix_b[1][0]) + np.dot(bilinear_matrix[1][0], matrix_a[1] * matrix_b[0][0]) + np.dot(bilinear_matrix[1][1], matrix_a[1] * matrix_b[1][0])

    result = np.zeros((N * N, 3))

    bilinear_matrix = np.array([[verts[0], verts[1]], [verts[2], verts[3]]])

    get_matrix()

    result = np.array(result)
    result_x, result_y, result_z = np.array(result[:, 0]), np.array(result[:, 1]), np.array(result[:, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    r = [-1, 1]

    np.meshgrid(r, r)

    for i in range(len(result)):
        ax.scatter(result_x[i], result_y[i], result_z[i])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


def main_window():
    res_points = [[0, 0, 1], [1, 1, 1], [1, 0, 0], [0, 1, 0]]

    def counts():
        res_points[0][0] = int(x1_field.get())
        res_points[0][1] = int(y1_field.get())
        res_points[0][2] = int(z1_field.get())

        res_points[1][0] = int(x2_field.get())
        res_points[1][1] = int(y2_field.get())
        res_points[1][2] = int(z2_field.get())

        res_points[2][0] = int(x3_field.get())
        res_points[2][1] = int(y3_field.get())
        res_points[2][2] = int(z3_field.get())

        res_points[3][0] = int(x4_field.get())
        res_points[3][1] = int(y4_field.get())
        res_points[3][2] = int(z4_field.get())

    def click():
        counts()
        bilinear_surface(res_points)

    def rotate():
        alfa = int(angle_field.get())
        cos_alfa = np.cos(alfa)
        sin_alfa = np.sin(alfa)
        np.zeros((3, 3))
        if os_combo.get() == 'x':
            matrix = np.array([[1, 0, 0], [0, cos_alfa, -sin_alfa], [0, sin_alfa, cos_alfa]])
        else:
            matrix = np.array([[cos_alfa, 0, sin_alfa], [0, 1, 0], [-sin_alfa, 0, cos_alfa]])

        for i in range(4):
            res_points[i] = np.dot(res_points[i], matrix)

        bilinear_surface(res_points)

    window = Tk()
    window.title("Лабораторная работа №3")
    window.geometry('400x400')

    Label(window, text="Координаты 1 точки:", font=("Arial", 14)).place(x=10, y=10)
    Label(window, text="x1: ").place(x=10, y=40)
    x1_field = Entry(window, width=10)
    x1_field.place(x=50, y=40)
    Label(window, text="y1: ").place(x=140, y=40)
    y1_field = Entry(window, width=10)
    y1_field.place(x=180, y=40)
    Label(window, text="z1: ").place(x=270, y=40)
    z1_field = Entry(window, width=10)
    z1_field.place(x=310, y=40)

    Label(window, text="Координаты 2 точки:", font=("Arial", 14)).place(x=10, y=70)
    Label(window, text="x2: ").place(x=10, y=100)
    x2_field = Entry(window, width=10)
    x2_field.place(x=50, y=100)
    Label(window, text="y2: ").place(x=140, y=100)
    y2_field = Entry(window, width=10)
    y2_field.place(x=180, y=100)
    Label(window, text="z2: ").place(x=270, y=100)
    z2_field = Entry(window, width=10)
    z2_field.place(x=310, y=100)

    Label(window, text="Координаты 3 точки:", font=("Arial", 14)).place(x=10, y=130)
    Label(window, text="x3: ").place(x=10, y=160)
    x3_field = Entry(window, width=10)
    x3_field.place(x=50, y=160)
    Label(window, text="y3: ").place(x=140, y=160)
    y3_field = Entry(window, width=10)
    y3_field.place(x=180, y=160)
    Label(window, text="z3: ").place(x=270, y=160)
    z3_field = Entry(window, width=10)
    z3_field.place(x=310, y=160)

    Label(window, text="Координаты 4 точки:", font=("Arial", 14)).place(x=10, y=190)
    Label(window, text="x4: ").place(x=10, y=220)
    x4_field = Entry(window, width=10)
    x4_field.place(x=50, y=220)
    Label(window, text="y4: ").place(x=140, y=220)
    y4_field = Entry(window, width=10)
    y4_field.place(x=180, y=220)
    Label(window, text="z4: ").place(x=270, y=220)
    z4_field = Entry(window, width=10)
    z4_field.place(x=310, y=220)

    ok_button = Button(window, text="Построить!", command=click)
    ok_button.place(x=180, y=260)

    Label(window, text="Ось: ", font=("Arial", 14)).place(x=10, y=330)
    os_combo = Combobox(window)
    os_combo["values"] = ("x", "y")
    os_combo.current(0)
    os_combo.place(x=80, y=330)

    Label(window, text="Угол:", font=("Arial", 14)).place(x=10, y=370)
    angle_field = Entry(window, width=10)
    angle_field.place(x=80, y=370)

    rotate_button = Button(window, text="Повернуть!", command=rotate)
    rotate_button.place(x=220, y=370)

    window.mainloop()


if __name__ == "__main__":
    main_window()
