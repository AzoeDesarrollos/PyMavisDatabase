from frontend import Renderer, WidgetHandler
from backend import EventHandler
from frontend.widgets import *

b = Button(205, 50)
e = Entry(0, 50, b)
label = Label('', 0, 100)

while True:
    EventHandler.process()
    WidgetHandler.update()
    Renderer.update()
