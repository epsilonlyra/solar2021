# coding: utf-8
# license: GPLv3
import numpy
import matplotlib.pyplot as plt

from solar_objects import Star, Planet
from solar_vis import DrawableObject

configuration =[]
def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open("models/" + input_filename, 'r') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем

            object_type = line.split()[0].lower()
            if object_type == "star":
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print("Unknown space object")

    return [DrawableObject(obj) for obj in objects]


def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки.

    Входная строка должна иметь слеюущий формат:

    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.

    Пример строки:

    Star 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание звезды.

    **star** — объект звезды.
    """

    useless, R, color, m, x, y, Vx, Vy = line.split()
    star.R = int(R)
    star.color = color
    star.m = float(m)
    star.x = float(x)
    star.y = float(y)
    star.Vx = float(Vx)
    star.Vy = float(Vy)
    


def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Входная строка должна иметь слеюущий формат:

    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.

    Пример строки:

    Planet 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание планеты.

    **planet** — объект планеты.
    """

    useless, R, color, m, x, y, Vx, Vy = line.split()
    planet.R = int(R)
    planet.color = color
    planet.m = float(m)
    planet.x = float(x)
    planet.y = float(y)
    planet.Vx = float(Vx)
    planet.Vy = float(Vy)
    


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.

    Строки должны иметь следующий формат:

    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла

    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'w') as out_file:
        for obj in space_objects:
            if obj.type == "star":
                first = "Star"
            else:
                first = "Planet"
            print(out_file, "%s %d %s %E %E %E %E %E" % (first, obj.R, obj.color,
                                                obj.m, obj.x, obj.y, obj.Vx, obj.Vy))
                                                



def remember_data_for_graphs(space_objects, t):
    global configuration

    if len(space_objects) == 2:
        planet, star = space_objects
        r = ((planet.x - star.x)**2 + (planet.y - star.y)**2)**(1/2)
        v = ((planet.Vx - star.Vx)**2 + (planet.Vy - star.Vy)**2)**(1/2)

        configuration.append((r, v, t))

def plot_graph(path):
    global configuration

    time = []
    r = []
    v = []
    for el in configuration:
        r_temp, v_temp, t_temp = el
        time.append(t_temp)
        r.append(r_temp)
        v.append(v_temp)

    plt.figure(1)
    plt.plot(time, r)
    plt.xlabel("Time, s")
    plt.ylabel("Distance, m")
    plt.savefig(path + 'r_t.png')
    
    plt.figure(2)
    plt.plot(time, v)
    plt.xlabel("Time, s")
    plt.ylabel("Velocity, m/s")
    plt.savefig(path + 'v_t.png')
    
    plt.figure(3)
    plt.plot(r, v)
    plt.xlabel("Distance, m")
    plt.ylabel("Velocity, m/s")
    plt.savefig(path + 'v_r.png')


    

    
        

if __name__ == "__main__":
    print("This module is not for direct call!")
