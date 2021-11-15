# coding: utf-8
# license: GPLv3

import pygame as pg
from solar_vis import *
from solar_model import *
from solar_input import *
from solar_objects import *
import thorpy
import time
import numpy as np
import os


alive = True
""" Флаг выполнения программы """

update_ui = True
""" Нужно ли обновить интерфейс пользователя"""

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

model_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

base_time_scale = 300 # ты знаешь что такое определение безумия?
"""Шаг по времени при моделировании(видимый)  в секундах по дефолту (сколько модельного времени проходит за секунду пользователя""
то есть при нулевом положении шкалы Тип: float"""

precision = 5E7 # видимо это не поможет
""" максимальный шаг по времени для программы в техническом исполнении с"""


time_scale = base_time_scale
""" Шаг времени при моделировании меняемый при изменении слайдера"""

space_objects = []
"""Список космических объектов."""


directory = 'models'
models = os.listdir(directory)
""" Список имен файлов-моделей """


chosen_file = ''  # сразу после запуска программы ни одна модель не загружена

list_of_models_is_seen = True


def execution(delta):
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    то есть расчет их скоростей и координат.
    """
    global model_time
    global precison
    i = 0
    step_time = 0.0
    if delta <= precision:
         recalculate_space_objects_positions(
             [dr.obj for dr in space_objects], delta)
         model_time += delta

    else: # if speed of time is to big will make calculations with precision(FIXME)
        while step_time <= delta:
            print(i)
            recalculate_space_objects_positions(
                [dr.obj for dr in space_objects], precision)
            i =i +1
            step_time += precision
        model_time += delta



def start_execution():
    """Обработчик события нажатия на кнопку Play.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    global list_of_models_is_seen
    global update_ui
    perform_execution = True


def pause_execution():
    """ Обработчик нажатия на кнопку  Stop
    Останвливает циклическое исполнение функции execution
    """
    global perform_execution
    perform_execution = False

def stop_execution():
    """Обработчик события нажатия на кнопку Quit.
    Выход из программы
    """
    global alive
    alive = False

def open_file(file_name):
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global model_time
    global screen
    global update_ui
    global chosen_file
    global configuration
    model_time = 0.0
    try:
        space_objects = read_space_objects_data_from_file(file_name)
        max_distance = max([max(abs(obj.obj.x), abs(obj.obj.y))
                        for obj in space_objects])
        calculate_scale_factor(max_distance)
    except IsADirectoryError:
        print('File that you try to open doesnt exist')
    pause_execution()  # когда вызывается новый файл симуляция останавливается
    update_ui = True
    chosen_file = file_name
    print(len(configuration))
    configuration.clear()
    print(len(configuration))
def show_list_of_files():
    global update_ui
    global list_of_models_is_seen
    if not list_of_models_is_seen:
        list_of_models_is_seen = True
    else:
        list_of_models_is_seen = False
    update_ui =  True

def handle_events(events, menu):
    global alive
    for event in events:
        menu.react(event)
        if event.type == pg.QUIT:
            alive = False

def slider_to_real(val):
    """
    Переводит значения в слайдере в ускорении времени
    """
    return np.exp(val) * base_time_scale

def slider_reaction(event):
    """ Изменяет шаг по времени"""
    global time_scale
    time_scale = slider_to_real(event.el.get_value())

def init_ui(screen):

    global chosen_file,list_of_models_is_seen, models


    slider = thorpy.SliderX(100, (-10, 10), "Simulation speed")
    slider.user_func = slider_reaction
    button_stop = thorpy.make_button("Quit", func=stop_execution)
    button_pause = thorpy.make_button("Pause", func=pause_execution)
    button_play = thorpy.make_button("Play", func=start_execution)
    timersec = thorpy.OneLineText("Seconds passed")
    timeryear = thorpy.OneLineText("Years passed")

    button_renew = thorpy.make_button(text="Renew Simulation",
                                     func=open_file,
                                     params={'file_name' : chosen_file})

    button_load = thorpy.make_button(text="Load File ",
                                     func=show_list_of_files)


    elements = [slider,
                button_pause,
                button_stop,
                button_play,
                button_renew, button_load,
                timersec, timeryear]
    model_buttons = []
    if list_of_models_is_seen:
        for model in models:
            model_buttons.append(thorpy.make_button(model, func=open_file, params={'file_name' : model}))

    for model_button in model_buttons:
        elements.append(model_button)

    box = thorpy.Box(elements)
    reaction1 = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=slider_reaction,
                                event_args={"id":
                                            thorpy.constants.EVENT_SLIDE},
                                params={},
                                reac_name="slider reaction")
    box.add_reaction(reaction1)

    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen

    box.set_topleft((0,0))

    return menu, box, timersec, timeryear



def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки thorpy: окно, холст,
    фрейм с кнопками, кнопки.
    """

    global perform_execution
    global timersec, timeryear
    global screen
    global update_ui
    global time_scale, base_time_scale


    print('Modelling started!')

    pg.init()

    width = 1000
    height = 900
    screen = pg.display.set_mode((width, height))
    drawer = Drawer(screen)

    while alive :
        if update_ui:
            menu, box, timersec, timeryear = init_ui(screen)
            time_scale = base_time_scale
            update_ui = False

        drawer.update(space_objects, box)
        handle_events(pg.event.get(), menu)
        cur_time = time.perf_counter()
        if perform_execution:
            execution(time_scale)
            text =  str(int(model_time)) + " seconds passed"
            timersec.set_text(text)
            years = ((model_time) / (365.25 * 24 * 3600))
            text = str(round(years, 1)) + " years passed"
            timeryear.set_text(text)

        last_time = cur_time  # что это делает и без него все работает?
        drawer.update(space_objects, box)
        time.sleep(1.0/ 60) # basically FPS
        remember_data_for_graphs([dr.obj for dr in space_objects], model_time)

    print('Modelling finished!')
    pg.quit()
    plot_graph("graphs/")

if __name__ == "__main__":
    main()
