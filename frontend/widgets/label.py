from frontend import Renderer, WidgetHandler, COLOR_FONDO, COLOR_TEXTO
from frontend.globals.textrect import render_textrect
from backend.eventhandler import EventHandler
from .basewidget import BaseWidget
from pygame import font, Rect


class Label(BaseWidget):
    def __init__(self, name, text, x, y):
        self.x, self.y = x, y
        self.name = name
        self.f = font.SysFont('Verdana', 16)
        render = self.f.render(text, 1, (0, 0, 0))
        rect = render.get_rect(topleft=(x, y))
        EventHandler.register(self.show, 'show_text')
        super().__init__(render, rect)
        Renderer.add_widget(self, 1)
        WidgetHandler.add_widget(self, 1)

    def show(self, event):
        if event.data['label'] == self.name:
            txt = event.data.get('text').lstrip('$')
            if event.data['show_price']:
                self.image = self.f.render('Precio:' + event.data['show_price'] + txt, 1, COLOR_TEXTO, COLOR_FONDO)
            else:
                r = Rect(0, 0, 640, 480 // 2)
                self.image = render_textrect(txt, self.f, r, COLOR_TEXTO, COLOR_FONDO)
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.dirty = 1

    def update(self):
        self.dirty = 1
