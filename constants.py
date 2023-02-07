from datetime import date, timedelta

PARSE_TABLE: dict[str, int] = {"ausente": 0,  # "X"
                               "presente": 1,  # "*"
                               "dia_no_trabajado": -1,  # "N"
                               "sin asistencia": -2,  # "S"
                               "otros": -3}  # "O"  no matriculado, retirado o inicio de clases

PARSE_STR_MONTH_TO_DATA: dict[str, tuple[int, int]] = {"Enero": (1, 31),
                                                       "Febrero": (2, 28),
                                                       "Marzo": (3, 31),
                                                       "Abril": (4, 30),
                                                       "Mayo": (5, 31),
                                                       "Junio": (6, 30),
                                                       "Julio": (7, 31),
                                                       "Agosto": (8, 31),
                                                       "Septiembre": (9, 30),
                                                       "Octubre": (10, 31),
                                                       "Noviembre": (11, 30),
                                                       "Diciembre": (12, 31)
                                                       }

PARSE_INT_TO_MONTH: list[str] = ["Enero",
                                 "Febrero",
                                 "Marzo",
                                 "Abril",
                                 "Mayo",
                                 "Junio",
                                 "Julio",
                                 "Agosto",
                                 "Septiembre",
                                 "Octubre",
                                 "Noviembre",
                                 "Diciembre",
                                 ]


SORT_COLUMNS: list[date] = [
    date(2022, 3, 1)+timedelta(days=i) for i in range(1, 274+1)]

TEMPLATE_FORM_1: list[str] = ["RBD", 'Detalle Selección',
                              "Alumnos", 'Registrar Asistencia']

TEMPLATE_FORM_2: list[str] = [
    'Detalle Selección', "Alumnos", 'Registrar Asistencia']

TEMPLATE_FORM_3: list[str] = ["Alumnos"]
