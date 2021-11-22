# coding: utf-8
# license: GPLv3

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить дейстующую силу.

    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        r = ((body.x - obj.x)**2 + (body.y - obj.y)**2)**0.5


        body.Fx += (obj.x - body.x) / (r**3) * gravitational_constant * obj.m * body.m
        body.Fy += (obj.y - body.y) / (r**3) * gravitational_constant * obj.m * body.m        

def move_space_object(body, dt):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """


    ax = body.Fx/body.m
    body.Vx += ax*dt
    body.x += body.Vx*dt
    

    ay = body.Fy/body.m
    body.Vy += ay*dt
    body.y += body.Vy*dt
    

def calculate_energy(space_objects):
    e = 0
    for body1 in space_objects:
        for body2 in space_objects:
            if body1 == body2:
                continue
            r = ((body1.obj.x - body2.obj.x)**2 + (body1.obj.y - body2.obj.y)**2)**(1/2)
            e -= gravitational_constant * body1.obj.m * body2.obj.m / r / 2

    for body in space_objects:
        e += body.obj.m / 2 * (body.obj.Vy**2 + body.obj.Vx**2)

    return(e)
def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.

    **dt** — шаг по времени
    """

    '''
    # вычисление энергии в начале
    e = 0
    for body in space_objects:
        for obj in space_objects:
            if obj == body:
                continue
            r = ((body.x - obj.x)**2 + (body.y - obj.y)**2)**0.5
            e -= gravitational_constant * obj.m * body.m / r / 2

    for body in space_objects:
        e += body.m / 2 * (body.Vy**2 + body.Vx**2)
    '''
    for body in space_objects:
        calculate_force(body, space_objects)
    for body in space_objects:
        move_space_object(body, dt)
    '''
    potential = 0
    for body in space_objects:
        for obj in space_objects:
            if obj == body:
                continue
            r = ((body.x - obj.x)**2 + (body.y - obj.y)**2)**0.5
            potential -= gravitational_constant * obj.m * body.m / r / 2
    
    kinetic = 0
    for body in space_objects:
        kinetic += body.m / 2 * (body.Vy**2 + body.Vx**2)

    scale = (e - potential) / kinetic
    print(scale)
    for body in space_objects:
        body.Vx = (scale**(1/2)) * body.Vx
        body.Vy = (scale**(1/2)) * body.Vy
    
    '''
    


if __name__ == "__main__":
    print("This module is not for direct call!")
