"""
ORIOL PERARNAU MONFORT

Normalización de expresiones horarias mediante expresiones regulares.
"""

import re


def normalizaHoras(ficText, ficNorm):

    def hhmm(h, m):
        return f"{h:02d}:{m:02d}"

    def reemplazar_horas(linea):

        # 18h45m, 8h, 17h5m
        def h_m(match):
            h = int(match.group(1))
            m = match.group(2)

            if h > 23:
                return match.group(0)

            if m is None:
                return hhmm(h, 0)

            m = int(m)

            if m > 59:
                return match.group(0)

            return hhmm(h, m)

        linea = re.sub(
            r'\b([01]?\d|2[0-3])h(?:([0-5]?\d)m)?\b',
            h_m,
            linea
        )

        # hh:mm correcto
        linea = re.sub(
            r'\b([01]?\d|2[0-3]):([0-5]\d)\b',
            lambda m: hhmm(int(m.group(1)), int(m.group(2))),
            linea
        )

        # en punto
        linea = re.sub(
            r'\b([1-9]|1[0-2])\s+en\s+punto\b',
            lambda m: hhmm(int(m.group(1)) % 12, 0),
            linea
        )

        # y cuarto
        linea = re.sub(
            r'\b([1-9]|1[0-2])\s+y\s+cuarto\b',
            lambda m: hhmm(int(m.group(1)) % 12, 15),
            linea
        )

        # y media
        linea = re.sub(
            r'\b([1-9]|1[0-2])\s+y\s+media\b',
            lambda m: hhmm(int(m.group(1)) % 12, 30),
            linea
        )

        # menos cuarto
        def menos_cuarto(match):
            h = int(match.group(1))
            h = 12 if h == 1 else h - 1
            return hhmm(h % 12, 45)

        linea = re.sub(
            r'\b([1-9]|1[0-2])\s+menos\s+cuarto\b',
            menos_cuarto,
            linea
        )

        # de la mañana
        def manana(match):
            h = int(match.group(1))
            if 4 <= h <= 12:
                return hhmm(0 if h == 12 else h, 0)
            return match.group(0)

        linea = re.sub(
            r'\b([1-9]|1[0-2])(?:h)?\s+de\s+la\s+mañana\b',
            manana,
            linea
        )

        # del mediodía
        def mediodia(match):
            h = int(match.group(1))
            if h in (12, 1, 2, 3):
                return hhmm(12 if h == 12 else h + 12, 0)
            return match.group(0)

        linea = re.sub(
            r'\b([1-9]|1[0-2])\s+del\s+mediod[ií]a\b',
            mediodia,
            linea
        )

        # de la tarde
        def tarde(match):
            h = int(match.group(1))
            if 3 <= h <= 8:
                return hhmm(h + 12, 0)
            return match.group(0)

        linea = re.sub(
            r'\b([1-9]|1[0-2])\s+de\s+la\s+tarde\b',
            tarde,
            linea
        )

        # de la noche
        def noche(match):
            h = int(match.group(1))

            if h == 12:
                return "00:00"

            if 8 <= h <= 11:
                return hhmm(h + 12, 0)

            if 1 <= h <= 4:
                return hhmm(h, 0)

            return match.group(0)

        linea = re.sub(
            r'\b([1-9]|1[0-2])\s+de\s+la\s+noche\b',
            noche,
            linea
        )

        # de la madrugada
        def madrugada(match):
            h = int(match.group(1))
            if 1 <= h <= 6:
                return hhmm(h, 0)
            return match.group(0)

        linea = re.sub(
            r'\b([1-9]|1[0-2])\s+de\s+la\s+madrugada\b',
            madrugada,
            linea
        )

        return linea

    with open(ficText, encoding="utf-8") as entrada, \
         open(ficNorm, "w", encoding="utf-8") as salida:

        for linea in entrada:
            salida.write(reemplazar_horas(linea))