import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from tkinter import *
from tkinter.ttk import *

matrix = [
    [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5], [-0.5, -0.5, -0.5],
    [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5], [-0.5, -0.5, 0.5]
]


def plt_show(verts, res_matrix, eye):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter3D(res_matrix[:, 0], res_matrix[:, 1], res_matrix[:, 2], color='black')

    ax.add_collection3d(Poly3DCollection(verts, facecolors='lime', linewidths=1, edgecolors='black', alpha=0.25))

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.scatter(eye[0], eye[1], eye[2], color='red', s=100)

    plt.show()


def rotate_figure(matrix, os='x', angle=0):
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)

    def get_rotation_matrix(os):
        switcher = {
            'x': np.array([[1, 0, 0], [0, cos_angle, sin_angle], [0, -sin_angle, cos_angle]]),
            'y': np.array([[cos_angle, 0, -sin_angle], [0, 1, 0], [sin_angle, 0, cos_angle]]),
            'z': np.array([[cos_angle, sin_angle, 0], [-sin_angle, cos_angle, 0], [0, 0, 1]])
        }
        return switcher.get(os, np.eye(3))

    rotation_matrix = get_rotation_matrix(os)
    res_matrix = np.dot(matrix, rotation_matrix)

    verts = [[res_matrix[0], res_matrix[1], res_matrix[2], res_matrix[3]],
             [res_matrix[4], res_matrix[5], res_matrix[6], res_matrix[7]],
             [res_matrix[0], res_matrix[1], res_matrix[5], res_matrix[4]],
             [res_matrix[2], res_matrix[3], res_matrix[7], res_matrix[6]],
             [res_matrix[1], res_matrix[2], res_matrix[6], res_matrix[5]],
             [res_matrix[4], res_matrix[7], res_matrix[3], res_matrix[0]]]

    return [verts, res_matrix]

def Roberts(data, eye):
    verts = data[0]
    W = np.zeros(3)
    P = np.array(eye)
    for i in range(2):
        max_value = -10
        min_value = 10
        for point in verts:
            max_value1 = max(point[j][0] for j in range(len(point)))
            max_value = max(max_value, max_value1)
            min_value1 = min(point[j][0] for j in range(len(point)))
            min_value = min(min_value, min_value1)
        W[i] = (max_value + min_value) / 2
    new_data = []
    for vector in verts:
        Vec1_x = vector[0][0] - vector[1][0]
        Vec2_x = vector[2][0] - vector[1][0]
        Vec1_y = vector[0][1] - vector[1][1]
        Vec2_y = vector[2][1] - vector[1][1]
        Vec1_z = vector[0][2] - vector[1][2]
        Vec2_z = vector[2][2] - vector[1][2]
        A = Vec1_y * Vec2_z - Vec2_y * Vec1_z
        B = Vec1_z * Vec2_x - Vec2_z * Vec1_x
        C = Vec1_x * Vec2_y - Vec2_x * Vec1_y
        D = -(A * vector[0][0] + B * vector[0][1] + C * vector[0][2])
        m = -(A * W[0] + B * W[1] + C * W[2] + D)
        A = A * m
        B = B * m
        C = C * m
        D = D * m
        if (A * P[0] + B * P[1] + C * P[2] + D) > 0:
            new_data.append(vector)

    return new_data


def update_view():
    eye = [eye_x_slider.get(), eye_y_slider.get(), eye_z_slider.get()]
    angle = angle_slider.get()
    data = rotate_figure(matrix, axis_combo.get(), int(np.radians(angle)))
    data[0] = Roberts(data, eye)
    plt_show(data[0], data[1], eye)


# Создание окна Tkinter
window = Tk()
window.title("Лаб. работа №4")
window.geometry('500x400')
window.resizable(False, False)


Label(window, text="Выберите ось для вращения", font=("Consolas", 14)).place(x=120, y=10)
axis_combo = Combobox(window, values=["x", "y", "z"])
axis_combo.current(1)
axis_combo.place(x=175, y=40)


Label(window, text="Выберите угол вращения", font=("Consolas", 14)).place(x=135, y=70)
angle_slider = Scale(window, from_=0, to=360, orient=HORIZONTAL)
angle_slider.set(0)
angle_slider.place(x=200, y=110)
Label(window, text=f"{angle_slider['from']}", font=("Consolas", 14)).place(x=135, y=110)
Label(window, text=f"{angle_slider['to']}", font=("Consolas", 14)).place(x=335, y=110)

Label(window, text="Позиция обзора", font=("Consolas", 14)).place(x=175, y=150)
Label(window, text="X", font=("Consolas", 14)).place(x=90, y=200)
eye_x_slider = Scale(window, from_=-1, to=1, orient=HORIZONTAL, length=200)
eye_x_slider.set(0)
eye_x_slider.place(x=150, y=200)
Label(window, text=f"{eye_x_slider['from']}", font=("Consolas", 14)).place(x=120, y=200)
Label(window, text=f"{eye_x_slider['to']}", font=("Consolas", 14)).place(x=360, y=200)

Label(window, text="Y", font=("Consolas", 14)).place(x=90, y=250)
eye_y_slider = Scale(window, from_=-1, to=1, orient=HORIZONTAL, length=200)
eye_y_slider.set(0)
eye_y_slider.place(x=150, y=250)
Label(window, text=f"{eye_y_slider['from']}", font=("Consolas", 14)).place(x=120, y=250)
Label(window, text=f"{eye_y_slider['to']}", font=("Consolas", 14)).place(x=360, y=250)

Label(window, text="Z", font=("Consolas", 14)).place(x=90, y=300)
eye_z_slider = Scale(window, from_=-1, to=1, orient=HORIZONTAL, length=200)
eye_z_slider.set(1)
eye_z_slider.place(x=150, y=300)
Label(window, text=f"{eye_z_slider['from']}", font=("Consolas", 14)).place(x=120, y=300)
Label(window, text=f"{eye_z_slider['to']}", font=("Consolas", 14)).place(x=360, y=300)

Button(window, text="Показать", command=update_view).place(x=210, y=350)

window.mainloop()
