from frontend import Renderer, WidgetHandler
from backend import EventHandler, cargar_db
from frontend.widgets import *

Label('etq', 'Producto:', 0, 50)
Label('version', "v0.1", 600, 0)
Button(0, 0, 'Recargar DBs', cargar_db)
e = Entry(80, 50)
Button(e.rect.right + 10, 50, 'Consulta', e.button_trigger)
Label('precio', '', 0, 100)

while True:
    EventHandler.process()
    WidgetHandler.update()
    Renderer.update()
