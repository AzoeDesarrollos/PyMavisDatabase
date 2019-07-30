import csv

csv.register_dialect('myCSV', delimiter=';')


def read_cvs(ruta):
    """Lee archivos CSV y los devuelve como una lista."""

    table = []
    with open(ruta, encoding='windows-1252') as file:
        data = csv.reader(file, dialect='myCSV')
        for row in data:
            table.append(row)
        if len(table) == 1:
            table = table[0]

    return table


def is_empty(line):
    return all(line[i] == '' for i in range(len(line)))


def trim(line, delete_empty=True):
    if delete_empty:
        return [item.strip() for item in line if item != '']
    else:
        return [item.strip() for item in line]
