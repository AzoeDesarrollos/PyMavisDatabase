from frontend import Renderer, WidgetHandler, COLOR_FONDO
from backend.eventhandler import EventHandler


from .basewidget import BaseWidget
from pygame import font


class Label(BaseWidget):
    def __init__(self, text, x, y):
        self.x, self.y = x, y
        self.f = font.SysFont('Verdana', 16)
        render = self.f.render(text, 1, (255, 255, 255))
        rect = render.get_rect(topleft=(x, y))
        EventHandler.register(self.show, 'show_text')
        super().__init__(render, rect)
        Renderer.add_widget(self, 1)
        WidgetHandler.add_widget(self, 1)

    def show(self, event):
        txt = event.data.get('text').lstrip('$')

        self.image = self.f.render(event.data['show_price']+txt, 1, (0, 0, 0), COLOR_FONDO)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.dirty = 1

    def update(self):
        self.dirty = 1
