from .resources import read_cvs, is_empty, trim
from sqlite3 import *


def process_devir(ruta, incluir_titulo=False):
    top = []
    bottom = []
    for row in read_cvs(ruta):
        if not is_empty(row) and row[0] != '':
            column = row.index('')
            a = trim(row[:column])
            b = trim(row[column+1:])
            if len(a) > 1:
                if len(a) < 6:
                    a.extend(['']*(6-len(a)))
                top.append(a)

            if len(b) > 1:
                if len(b) < 6:
                    b.extend(['']*(6-len(b)))
                bottom.append(b)

    if incluir_titulo:
        return top+bottom
    else:
        return top[1:]+bottom


def process_sd_dist(ruta, incluir_titulo=False):
    tabla = []
    for fila in read_cvs(ruta):
        lenght = len(fila[1]) == 11
        if fila[1] != '' and any([incluir_titulo, lenght]):
            f = trim(fila[1:], delete_empty=False)
            fila = f[0:4]+f[5:]
            tabla.append(fila)
    return tabla


db = connect(':memory:')
db.execute('''CREATE TABLE devir (codigo real NOT NULL,
                                    nombre text NOT NULL, 
                                    unit text NOT NULL, 
                                    sugerido text NOT NULL, 
                                    pedido text DEFAULT  " ", 
                                    otro text DEFAULT " ")
                                    ''')

db.execute('''CREATE TABLE sd_dist (codigo text NOT NULL,
                                    titulo text NOT NULL,
                                    pvp text NOT NULL,
                                    descuento text NOT NULL,
                                    isbn text NOT NULL,
                                    ean text NOT NULL,
                                    adendum text DEFAULT " ",
                                    editorial text NOT NULL,
                                    autor text NOT NULL
                                    )''')

for linea in process_devir('data/Lista_de_Precios_Devirb.csv'):
    db.execute("INSERT INTO devir VALUES ({})".format(','.join(['?' for i in range(len(linea))])), linea)

for linea in process_sd_dist('data/LISTADO_SD_DISTRIBUCIONES_19_07_2019b.csv'):
    db.execute("INSERT INTO sd_dist VALUES ({})".format(','.join(['?' for i in range(len(linea))])), linea)

db.commit()
print('success')
__all__ = [
    'db'
    ]
