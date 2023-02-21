import pandas as pd
import pytest
from duplicated_students.duplicated_students import join_students


## FUNCIONALITY
@pytest.mark.parametrize(
    "dict_data",
    [
        (dict()), # Vacio
        ({"A": [-5], # Solo hay nan
          "Alumno": ["José Rodríguez"]
          }),
        ({"A": [-5], # Solo hay nan
          "B": [-5],
          "C": [-5],
          "D": [-5],
          "E": [-5],
          "F": [-5],
          "Alumno": ["José Rodríguez"]
          }),
        ({"A": [-5 for _ in range(100)], # Solo hay nan, pese a haber 100 alumnos
          "Alumno": [f"José Rodríguez {i}" for i in range(100)]
          }),
        ({"A": [-5 for _ in range(100)], # Solo hay nan
          "B": [-5 for _ in range(100)],
          "C": [-5 for _ in range(100)],
          "D": [-5 for _ in range(100)],
          "E": [-5 for _ in range(100)],
          "F": [-5 for _ in range(100)],
          "Alumno": [f"José Rodríguez {i}" for i in range(100)]
          }),
    ]
)
def test_empty(dict_data:dict[str,list[int|str]]):
    df_test = pd.DataFrame(dict_data)
    res_test = join_students(df_test)
    assert res_test.empty, "Este archivo debería ser vacío, si tiene solo NaN (-5)."



def test_all_duplicated():
    pass
