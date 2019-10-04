from .database import cursor


def _return_value(column, table, key, value):
    cursor.execute('SELECT {c} from {t} WHERE {k}="{v}"'.format(c=column, t=table, k=key, v=value))
    return cursor.fetchone()


def devolver_todos():
    cursor.execute('SELECT nombre FROM devir')
    d = [j[0] for j in cursor.fetchall()]

    cursor.execute('SELECT titulo from sd_dist')
    d += [j[0] for j in cursor.fetchall()]
    return d


def costo_por_clave(table, value, clave):
    #  clave =  'nombre' o 'codigo'

    column = ''
    if table == 'sd_dist':
        column = 'pvp'
    elif table == 'devir':
        column = 'unit'

    return _return_value(column, table, clave, value)


__all__ = [
    'costo_por_clave',
    'devolver_todos'
    ]
