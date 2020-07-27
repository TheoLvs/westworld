from ursina import *            # import everything we need with one line.

app = Ursina()
ground = Entity(
    model = 'cube',
    color = color.magenta,
    z = -.1,
    y = -3,
    origin = (0, .5),
    scale = (50, 1, 10),
    collider = 'box'
    )

app.run()