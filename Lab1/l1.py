import tkinter as tk
from math import *
from tkinter.messagebox import showerror


def axis_y(k):
    for i in range(457, 20, -23):
        if (i == 250): continue
        if (k == 0): k +=10
        canvas.create_line(20, i, 480, i, width=1, fill="lightgrey", dash=(2, 2))
        canvas.create_oval(250, i, 250, i, width=2)
        canvas.create_text(237, i+5, text=k)
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
    canvas.create_line(250, 20, 250, 480, width=1, fill="black") #y
    canvas.create_line(20, 250, 480, 250, width=1, fill="black") #x

    axis()

    # Маркер в начале координат
    canvas.create_oval(250, 250, 250, 250, width=4)

def checkX(point):
    x = (point-250)/2.3
    if (x > 90 or x < -90):
        return False
    return True


def checkY(point):
    y = (250 - point) / 2.3
    if (y > 90 or y < -90):
        return False
    return True


def touch_point():
    # Получаем введенные пользователем значения
    circle1_x = 250 + float(circle_x_entry.get()) * 2.3
    circle1_y = 250 - float(circle_y_entry.get()) * 2.3
    circle1_radius = float(circle_radius_entry.get()) * 2.3
    pointA_x = 250 + float(point_x_entry.get()) * 2.3
    pointA_y = 250 - float(point_y_entry.get()) * 2.3

    if (not checkY(circle1_y) or not checkX(circle1_x)):
        showerror(title="Ошибка",
                  message="Центр окружности находится вне диапазона! Введите корректные координаты центра окружности.")
        return 1

    if pointA_x > 457 or pointA_x < 43 or pointA_y > 457 or pointA_y < 43:
        showerror(title="Ошибка", message="Точка находится вне диапазона! Введите корректные координаты точки.")
        return 1

    dist_pA = sqrt((pointA_x - circle1_x) ** 2 + (pointA_y - circle1_y) ** 2)
    if dist_pA <= circle1_radius:
        showerror(title="Ошибка", message="Точка лежит в/на окружности! Введите корректные координаты точки.")
        return 1

    dist_b = sqrt((pointA_x - circle1_x) ** 2 + (pointA_y - circle1_y) ** 2)
    print("Расстояние dist_b между точкой pointA и центром окружности circle1: ", dist_b/2.3)
    angle_theta = acos(circle1_radius / dist_b)
    print("Угол angle_theta, который используется для определения точек касания с окружностью: ", angle_theta)
    angle = atan2(pointA_y - circle1_y, pointA_x - circle1_x)
    print("Угол angle между точкой pointA и центром окружности circle1 с помощью функции atan2, которая возвращает "
          "угол в радианах между положительным направлением оси x и точкой (pointA_x, pointA_y).: ", angle)
    angle1 = angle + angle_theta
    print(angle1)
    angle2 = angle - angle_theta
    print(angle2)

    touch_x1 = circle1_x + circle1_radius * cos(angle1)
    touch_y1 = circle1_y + circle1_radius * sin(angle1)
    touch_x2 = circle1_x + circle1_radius * cos(angle2)
    touch_y2 = circle1_y + circle1_radius * sin(angle2)

    # Обновляем значения в интерфейсе
    touch_x_label.config(text=f"Точка касания по x: {(touch_x1-250)/2.3:.2f}")
    touch_y_label.config(text=f"Точка касания по y: {(250-touch_y1)/2.3:.2f}")
    touch_x2_label.config(text=f"Точка касания по x: {(touch_x2-250)/2.3:.2f}")
    touch_y2_label.config(text=f"Точка касания по y: {(250-touch_y2)/2.3:.2f}")

    # Удаляем предыдущий рисунок
    canvas.delete("all")
    draw()

    # Рисуем окружность
    canvas.create_oval([circle1_x - circle1_radius, circle1_y + circle1_radius],
                       [circle1_x + circle1_radius, circle1_y - circle1_radius], width=1)
    canvas.create_oval(circle1_x, circle1_y, circle1_x, circle1_y, width=3)
    canvas.create_text(circle1_x + 10, circle1_y + 10, text="O")

    # Рисуем точку
    canvas.create_oval(pointA_x, pointA_y, pointA_x, pointA_y, width=3)
    canvas.create_text(pointA_x + 10, pointA_y + 10, text="A")

    # Рисуем точку касания
    canvas.create_oval(touch_x1, touch_y1, touch_x1, touch_y1, fill="green", width=3)
    canvas.create_text(touch_x1 + 10, touch_y1 + 10, text="K1")
    canvas.create_oval(touch_x2, touch_y2, touch_x2, touch_y2, fill="green", width=3)
    canvas.create_text(touch_x2 + 10, touch_y2 + 10, text="K2")

    # Рисуем отрезок до точки касания
    canvas.create_line(pointA_x, pointA_y, touch_x1, touch_y1, fill="orange", width=1)
    canvas.create_line(pointA_x, pointA_y, touch_x2, touch_y2, fill="orange", width=1)


# Создаем окно приложения
root = tk.Tk()
root.title("Лабораторная работа №1")
root.geometry("750x500")
root.resizable(False, False)

# Создаем поле ввода для координат центра окружности
circle_x_label = tk.Label(root, text="Координата по x центра окружности:")
circle_x_label.place(x=10, y=10)
circle_x_entry = tk.Entry(root)
circle_x_entry.place(x=10, y=30)

circle_y_label = tk.Label(root, text="Координата по y центра окружности:")
circle_y_label.place(x=10, y=60)
circle_y_entry = tk.Entry(root)
circle_y_entry.place(x=10, y=80)

circle_radius_label = tk.Label(root, text="Радиус окружности:")
circle_radius_label.place(x=10, y=110)
circle_radius_entry = tk.Entry(root)
circle_radius_entry.place(x=10, y=130)

# Создаем поле ввода для координат точки
point_x_label = tk.Label(root, text="Координата по x точки:")
point_x_label.place(x=10, y=160)
point_x_entry = tk.Entry(root)
point_x_entry.place(x=10, y=180)

point_y_label = tk.Label(root, text="Координата по y точки:")
point_y_label.place(x=10, y=210)
point_y_entry = tk.Entry(root)
point_y_entry.place(x=10, y=230)

# Создаем кнопку для расчета
calculate_button = tk.Button(root, text="Рассчитать", command=touch_point)
calculate_button.place(x=10, y=260)

# Создаем метки для вывода координат точки касания
touch_x_label = tk.Label(root, text="Точка касания 1 по x:")
touch_x_label.place(x=10, y=290)

touch_y_label = tk.Label(root, text="Точка касания 1 по y:")
touch_y_label.place(x=10, y=320)

touch_x2_label = tk.Label(root, text="Точка касания 2 по x:")
touch_x2_label.place(x=10, y=350)

touch_y2_label = tk.Label(root, text="Точка касания 2 по y:")
touch_y2_label.place(x=10, y=380)

# Создаем canvas для отрисовки
canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack(anchor="e")

draw()

# Запускаем главный цикл приложения
root.mainloop()
