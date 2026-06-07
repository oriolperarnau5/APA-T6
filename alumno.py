"""
ORIOL PERARNAU MONFORT

Tratamiento de notas de alumnos mediante expresiones regulares.
"""

import re


class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'


def leeAlumnos(ficAlum):
    """
    Lee un fichero de alumnos y devuelve un diccionario cuya clave es
    el nombre completo del alumno.

    >>> alumnos = leeAlumnos("alumnos.txt")
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171 Blanca Agirrebarrenetse 9.5
    23 Carles Balcell de Lara 4.9
    68 David Garcia Fuster 7.0
    """

    alumnos = {}

    patron = re.compile(
        r'^\s*(\d+)\s+([A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+?)\s+((?:\d+(?:\.\d+)?\s*)+)$'
    )

    with open(ficAlum, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()

            m = patron.match(linea)
            if not m:
                continue

            num = int(m.group(1))
            nombre = m.group(2).strip()

            notas = [
                float(n)
                for n in re.findall(r'\d+(?:\.\d+)?', m.group(3))
            ]

            alumnos[nombre] = Alumno(nombre, num, notas)

    return alumnos


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE,
                    verbose=True)