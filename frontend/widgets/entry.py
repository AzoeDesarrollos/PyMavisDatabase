from pygame import Surface, font, key, draw, K_LSHIFT, K_RSHIFT, KMOD_CAPS
from backend.eventhandler import EventHandler
from backend.event_functions import costo_por_clave, devolver_todos
from backend.levenshtein import probar_input
from frontend import Renderer, WidgetHandler
from .basewidget import BaseWidget


class Entry(BaseWidget):
    f = None
    color_fondo = 255, 255, 255
    color_texto = 0, 0, 0
    lenght = 0
    ticks = 0
    active = True

    def __init__(self, x, y):
        self.f = font.SysFont('Verdana', 16)
        self.empty_f = font.SysFont('Verdana', 16, italic=True)
        self.w, self.h = 310, 23
        image = Surface((self.w, self.h))
        image.fill(self.color_fondo, (1, 1, self.w - 2, self.h - 2))
        rect = image.get_rect(topleft=(x, y))
        super().__init__(image, rect)
        Renderer.add_widget(self, 1)
        WidgetHandler.add_widget(self, 1)

        self.input = []

    def button_trigger(self):
        nombre = ''.join(self.input).upper()
        txt = costo_por_clave('devir', nombre, 'nombre')
        if txt is None:
            txt = costo_por_clave('sd_dist', nombre, 'titulo')
        try:
            EventHandler.trigger('show_text', 'input', {'label': 'precio', 'text': str(txt[0]), "show_price": '$'})
        except TypeError:
            text = probar_input(nombre, devolver_todos())
            EventHandler.trigger('show_text', 'input', {'label': 'precio', 'text': str(text), "show_price": ''})

    def on_keydown(self, tecla):
        mods = key.get_mods()
        shift = mods & K_LSHIFT or mods & K_RSHIFT or mods & KMOD_CAPS
        name = key.name(tecla).strip('[]')
        if name == 'space':
            self.input_character(' ')
        elif name == 'backspace':
            self.del_character()
        elif name == 'enter' or name == 'return':
            pass
        elif name.isalnum():
            if shift:
                name = name.upper()
            self.input_character(name)

    def on_mousebuttondown(self, button):
        if button == 1:
            self.active = True

    def input_character(self, char):
        self.input.append(char)
        self.lenght += 1

    def del_character(self):
        if self.lenght > 0:
            del self.input[-1]
            self.lenght -= 1

    def update(self):
        self.ticks += 1
        self.image.fill(self.color_fondo, (1, 1, self.w - 2, self.h - 2))
        if len(self.input):
            t = ''.join(self.input)
            color = self.color_texto
            fuente = self.f
        else:
            t = 'Ingrese el nombre de un producto'
            color = 125, 125, 125
            fuente = self.empty_f

        r = fuente.render(t, 1, color, self.color_fondo)
        rr = r.get_rect(topleft=(self.rect.x + 1, self.rect.y + 1))

        if self.rect.contains(rr):
            self.image.blit(r, (1, 1))
            self.dirty = 1

        if 10 < self.ticks < 30 and len(self.input) and self.active:
            draw.aaline(self.image, self.color_texto, (rr.right-80 + 2, 3), (rr.right-80 + 2, self.h - 3))
        elif self.ticks > 40:
            self.ticks = 0
