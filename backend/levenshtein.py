def levenshtein(a, b):
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current = range(n + 1)
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]


def probar_input(item, palabras):
    """Compruba que el input sea válido, utilizando la distancia Levenshtein

    Esta función fue extraída de un documento en PHP, todos los comentarios
    se refeieren a aquel dcumento"""
    cercana = ''
    while True:
        # la distancia mas corta no ha sido encontrada, aún
        dist = -1

        # loopea por las palabras hasta encontrar la mas cercana
        for palabra in palabras:
            # calcula la distnacia entre la palabra buscada,
            # y la palabra actual
            lev = levenshtein(item, palabra)

            # comprobación de coincidencia exacta
            if lev == 0:
                # este es el item más cercano (coincidencia exacta)
                cercana = palabra
                dist = 0

                # salir del bucle, hemos encontrado una coincidencia exacta
                break

            # si esta distancia es menor que la siguiente distancia más corta
            # encontrada, O si una palabra más corta siguiente aún no
            # se ha encontrad
            if lev <= dist or dist < 0:
                # establecer la coincidencia más cercana y,
                # la distancia más corta
                cercana = palabra
                dist = lev

        if dist == 0:
            return cercana
        elif not(dist <= -1 or dist > 3):
            return '¿Quizo decir' + ': ' + cercana + '? '
