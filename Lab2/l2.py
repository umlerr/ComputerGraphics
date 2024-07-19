import tkinter as tk
from tkinter.messagebox import showerror

import numpy as np


def axis_y(k):
    for i in range(457, 20, -23):
        if (i == 250): continue
        if (k == 0): k += 10
        canvas.create_line(20, i, 480, i, width=1, fill="lightgrey", dash=(2, 2))
        canvas.create_oval(250, i, 250, i, width=2)
        canvas.create_text(237, i + 5, text=k)
        k += 10


def axis_x(k):
    for i in range(43, 480, 23):
        if (i == 250): continue
        if (k == 0): k += 10
        canvas.create_line(i, 480, i, 20, width=1, fill="lightgrey", dash=(2, 2))
        canvas.create_oval(i, 250, i, 250, width=2)
        canvas.create_text(i, 260, text=k)
        k += 10


def axis():
    axis_y(-90)
    axis_x(-90)


def draw():
    # Рисуем оси координат
    canvas.create_line(250, 20, 250, 480, width=1, fill="black")  # y
    canvas.create_line(20, 250, 480, 250, width=1, fill="black")  # x
    axis()
    canvas.create_oval(250, 250, 250, 250, width=4)


def checkX(point):
    x = (point - 250) / 2.3
    if (x > 90 or x < -90):
        return False
    return True


def checkY(point):
    y = (250 - point) / 2.3
    if (y > 90 or y < -90):
        return False
    return True


def extract_numbers(s):
    parts = s.split(";")

    return 250 + float(int(parts[0])) * 2.3, 250 - float(int(parts[1])) * 2.3


def knot_values(n, k):
    t = np.zeros((1, n + k + 1))
    for i in range(0, n + k + 1):
        if i < k:
            t[0][i] = 0
        if k <= i <= n:
            t[0][i] = i - k + 1
        if i > n:
            t[0][i] = n - k + 2

    return t


def basis_spline(u, t, i, k):
    if k == 1:
        if t[0][i] <= u < t[0][i + 1]:
            sol = 1
        else:
            sol = 0
    else:
        a = (u - t[0][i]) * basis_spline(u, t, i, k - 1)
        b = t[0][i + k - 1] - t[0][i]
        c = (t[0][i + k] - u) * basis_spline(u, t, i + 1, k - 1)
        d = t[0][i + k] - t[0][i + 1]
        if b == 0:
            temp1 = 0
        else:
            temp1 = a / b

        if d == 0:
            temp2 = 0
        else:
            temp2 = c / d

        sol = temp1 + temp2

    return sol


def curve_generator(n, k, ctrl_x, ctrl_y):
    t = knot_values(n, k)
    print(t)
    u = np.arange(t[0][k - 1], t[0][n + 1], 0.001);
    length = u.shape

    x = np.zeros((1, length[0]))
    y = np.zeros((1, length[0]))

    for i in range(0, n + 1):
        for j in range(0, length[0]):
            x[0][j] = x[0][j] + basis_spline(u[j], t, i, k) * ctrl_x[i];
            y[0][j] = y[0][j] + basis_spline(u[j], t, i, k) * ctrl_y[i];

    return x, y


def draw_spline_curve(canvas, x, y):
    num_points = len(x)
    for i in range(1, num_points):
        canvas.create_line(x[i - 1], y[i - 1], x[i], y[i], fill="blue", width=2)


def touch_point():
    point1 = extract_numbers(point1_entry.get())
    point2 = extract_numbers(point2_entry.get())
    point3 = extract_numbers(point3_entry.get())
    point4 = extract_numbers(point4_entry.get())
    point5 = extract_numbers(point5_entry.get())
    point6 = extract_numbers(point6_entry.get())
    point7 = extract_numbers(point7_entry.get())
    k = int(k_entry.get())

    # Удаляем предыдущий рисунок
    canvas.delete("all")
    draw()

    # Рисуем точку
    canvas.create_oval(point1[0], point1[1], point1[0], point1[1], width=3)
    canvas.create_oval(point2[0], point2[1], point2[0], point2[1], width=3)
    canvas.create_oval(point3[0], point3[1], point3[0], point3[1], width=3)
    canvas.create_oval(point4[0], point4[1], point4[0], point4[1], width=3)
    canvas.create_oval(point5[0], point5[1], point5[0], point5[1], width=3)
    canvas.create_oval(point6[0], point6[1], point6[0], point6[1], width=3)
    canvas.create_oval(point7[0], point7[1], point7[0], point7[1], width=3)

    ctrl_x = np.array([point1[0], point2[0], point3[0], point4[0], point5[0], point6[0], point7[0]])
    ctrl_y = np.array([point1[1], point2[1], point3[1], point4[1], point5[1], point6[1], point7[1]])
    n = len(ctrl_x) - 1

    if (not checkY(point1[1]) or not checkX(point1[0])) or (not checkY(point2[1]) or not checkX(point2[0])) \
            or (not checkY(point3[1]) or not checkX(point3[0])) or (not checkY(point4[1]) or not checkX(point4[0])) \
            or (not checkY(point5[1]) or not checkX(point5[0])) or (not checkY(point6[1]) or not checkX(point6[0])) \
            or (not checkY(point7[1]) or not checkX(point7[0])):
        showerror(title="Ошибка",
                  message="Точка находится вне диапозона! Введите корректные координаты.")
        return 1

    if not (1 <= k <= 6):
        showerror(title="Ошибка",
                  message="Неккоректная степень кривой! Введите корректные данные.")
        return 1

    if len(ctrl_x) != len(set(ctrl_x)) or len(ctrl_y) != len(set(ctrl_y)):
        showerror(title="Ошибка",
                  message="Есть точки с одинаковыми координатами! Введите корректные координаты.")
        return 1

    [x, y] = curve_generator(n, k, ctrl_x, ctrl_y)

    n = x.shape
    a = [0] * n[1]
    b = [0] * n[1]
    for i in range(0, n[1]):
        a[i] = x[0][i]
        b[i] = y[0][i]

    draw_spline_curve(canvas, a, b)


# Создаем окно приложения
root = tk.Tk()
root.title("Лабораторная работа №2")
root.geometry("750x500")
root.resizable(False, False)

# Создаем поле ввода для координат центра окружности
point1_label = tk.Label(root, text="Координата 1 точки:")
point1_label.place(x=10, y=10)
point1_entry = tk.Entry(root)
point1_entry.place(x=10, y=30)

point2_label = tk.Label(root, text="Координата 2 точки:")
point2_label.place(x=10, y=50)
point2_entry = tk.Entry(root)
point2_entry.place(x=10, y=70)

point3_label = tk.Label(root, text="Координата 3 точки:")
point3_label.place(x=10, y=90)
point3_entry = tk.Entry(root)
point3_entry.place(x=10, y=110)

point4_label = tk.Label(root, text="Координата 4 точки:")
point4_label.place(x=10, y=130)
point4_entry = tk.Entry(root)
point4_entry.place(x=10, y=150)

point5_label = tk.Label(root, text="Координата 5 точки:")
point5_label.place(x=10, y=170)
point5_entry = tk.Entry(root)
point5_entry.place(x=10, y=190)

point6_label = tk.Label(root, text="Координата 6 точки:")
point6_label.place(x=10, y=210)
point6_entry = tk.Entry(root)
point6_entry.place(x=10, y=230)

point7_label = tk.Label(root, text="Координата 7 точки:")
point7_label.place(x=10, y=250)
point7_entry = tk.Entry(root)
point7_entry.place(x=10, y=270)

k_label = tk.Label(root, text="Степень кривой [1;6]:")
k_label.place(x=10, y=290)
k_entry = tk.Entry(root)
k_entry.place(x=10, y=310)

# Создаем кнопку для расчета
calculate_button = tk.Button(root, text="Рассчитать", command=touch_point)
calculate_button.place(x=10, y=350)

# Создаем canvas для отрисовки
canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack(anchor="e")

draw()

# Запускаем главный цикл приложения
root.mainloop()
