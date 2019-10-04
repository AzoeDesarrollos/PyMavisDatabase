from .resources import read_cvs, is_empty, trim
from sqlite3 import *


def process_devir(ruta):
    top = []
    bottom = []
    for row in read_cvs(ruta):
        if not is_empty(row) and row[0] != '':
            column = row.index('')
            a = trim(row[:column])
            b = trim(row[column + 1:])
            if len(a) > 1:
                if len(a) < 6:
                    a.extend([''] * (6 - len(a)))
                top.append(a)

            if len(b) > 1:
                if len(b) < 6:
                    b.extend([''] * (6 - len(b)))
                bottom.append(b)

    table = top[1:] + bottom
    for j, row in enumerate(table):
        row = row[1:]
        for i, value in enumerate(row):
            if value.startswith('$'):
                value = value.replace('.', '').replace(',', '.')
                row[i] = float(value[1:])

    return table


def process_sd_dist(ruta):
    tabla = []
    for fila in read_cvs(ruta):
        if fila[1] != '' and len(fila[1]) == 11:
            f = trim(fila[1:], delete_empty=False)
            fila = f[0:4] + f[5:]
            tabla.append(fila)

    for row in tabla:
        for i, value in enumerate(row):
            if value.startswith('$'):
                value = value.replace('.', '').replace(',', '.')
                row[i] = float(value[1:])
            elif value.endswith('%'):
                row[i] = int(value[:value.index('%')])

    return tabla


db = connect(':memory:')
cursor = db.cursor()
cursor.execute('''CREATE TABLE devir (codigo INTEGER PRIMARY KEY ASC, 
                                    nombre text NOT NULL, 
                                    unit integer NOT NULL, 
                                    sugerido integer NOT NULL, 
                                    pedido text DEFAULT  " ", 
                                    otro text DEFAULT " ")
                                    ''')

cursor.execute('''CREATE TABLE sd_dist (codigo text PRIMARY KEY UNIQUE,
                                    titulo text NOT NULL,
                                    pvp integer NOT NULL,
                                    descuento integer NOT NULL,
                                    isbn text NOT NULL,
                                    ean text NOT NULL,
                                    adendum text DEFAULT " ",
                                    editorial text NOT NULL,
                                    autor text NOT NULL
                                    )''')

cursor.execute('''CREATE TABLE ventas (codigo integer PRIMARY KEY AUTOINCREMENT,
                                    fecha text NOT NULL,
                                    producto text NOT NULL,
                                    abonado integer NOT NULL,
                                    cliente text,
                                    cuota integer,
                                    totalcuotas integer)
                                    ''')


def cargar_db():
    for linea in process_devir('data/Lista_de_Precios_Devirb.csv'):
        try:
            linea = linea[1:]
            cursor.execute("INSERT INTO devir (nombre, unit, sugerido, pedido, otro) "
                           "VALUES ({})".format(','.join(['?' for i in range(len(linea))])), linea)
            print('valor insertado')
        except IntegrityError as error:
            print('la línea', linea, 'no se pudo agregar por', error)

    for linea in process_sd_dist('data/LISTADO_SD_DISTRIBUCIONES_19_07_2019b.csv'):
        try:
            cursor.execute("INSERT INTO sd_dist VALUES ({})".format(','.join(['?' for i in range(len(linea))])), linea)
            print('valor insertado')
        except IntegrityError as error:
            print('la línea', linea, 'no se pudo agregar por', error)


# cargar_db()
db.commit()

__all__ = [
    'cursor',
    'cargar_db'
    ]
