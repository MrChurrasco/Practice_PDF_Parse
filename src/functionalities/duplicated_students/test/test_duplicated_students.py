import pandas as pd
import pytest
from functionalities.duplicated_students.duplicated_students import \
    join_students


# FUNCIONALITY
@pytest.mark.parametrize(
    "dict_data",
    [
        (dict()),  # Vacio.
        ({"A": [-5],  # Solo hay nan.
          "Alumno": ["José Rodríguez"]
          }),
        ({"A": [-5],  # Solo hay nan y varias columnas.
          "B": [-5],
          "C": [-5],
          "D": [-5],
          "E": [-5],
          "F": [-5],
          "Alumno": ["José Rodríguez"]
          }),
        ({"A": [-5 for _ in range(100)],  # Solo hay nan, pese a haber 100 filas.
          "Alumno": [f"José Rodríguez {i}" for i in range(100)]
          }),
        ({"A": [-5 for _ in range(100)],  # Solo hay nan, 100 filas y varias columnas.
          "B": [-5 for _ in range(100)],
          "C": [-5 for _ in range(100)],
          "D": [-5 for _ in range(100)],
          "E": [-5 for _ in range(100)],
          "F": [-5 for _ in range(100)],
          "Alumno": [f"José Rodríguez {i}" for i in range(100)]
          }),
    ]
)
def test_empty(dict_data: dict[str, list[int | str]]):
    df_test = pd.DataFrame(dict_data)
    assert join_students(
        df_test).empty, "Este archivo debería ser vacío, si tiene solo NaN (-5)."

# Hay una fila con información y solo un alumno, tiene que retornar una sola fila


def test_all_duplicated_one_data():
    df_test = pd.DataFrame({"Alumno": ["José Rodríguez" for _ in range(100)],
                            "A": [-5 for _ in range(99)] + [-3],
                            })
    df_assert = pd.DataFrame({"Alumno": "José Rodríguez",
                              "A": -3,
                              })
    assert df_assert.equals(join_students(
        df_test)), "No recupera el dato de la última fila (-3)."

    df_test = pd.DataFrame({"Alumno": ["José Rodríguez" for _ in range(100)],
                            "A": [-5 for _ in range(99)] + [-2],
                            })
    df_assert = pd.DataFrame({"Alumno": "José Rodríguez",
                              "A": -2,
                              })
    assert df_assert.equals(join_students(
        df_test)), "No recupera el dato de la última fila (-2)."

    df_test = pd.DataFrame({"Alumno": ["José Rodríguez" for _ in range(100)],
                            "A": [-5 for _ in range(99)] + [-1],
                            })
    df_assert = pd.DataFrame({"Alumno": "José Rodríguez",
                              "A": -1,
                              })
    assert df_assert.equals(join_students(
        df_test)), "No recupera el dato de la última fila (-1)."

    df_test = pd.DataFrame({"Alumno": ["José Rodríguez" for _ in range(100)],
                            "A": [-5 for _ in range(99)] + [0],
                            })
    df_assert = pd.DataFrame({"Alumno": "José Rodríguez",
                              "A": 0,
                              })
    assert df_assert.equals(join_students(
        df_test)), "No recupera el dato de la última fila (0)."

    df_test = pd.DataFrame({"Alumno": ["José Rodríguez" for _ in range(100)],
                            "A": [-5 for _ in range(99)] + [1],
                            })
    df_assert = pd.DataFrame({"Alumno": "José Rodríguez",
                              "A": 1,
                              })
    assert df_assert.equals(join_students(
        df_test)), "No recupera el dato de la última fila (1)."


def all_duplicate_multiple_data():
    assert True
