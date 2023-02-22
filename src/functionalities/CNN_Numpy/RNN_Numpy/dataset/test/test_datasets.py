import json

import numpy as np
import pytest
from functionalities.CNN_Numpy.RNN_Numpy.dataset import imagenes
from functionalities.CNN_Numpy.RNN_Numpy.dataset.datasets import (
    convert_bytes_to_array, create_dataset, get_dataset)

bytes_aux = []
for x in imagenes.images.values():
    bytes_aux += x


@pytest.mark.parametrize(
    "b",
    bytes_aux
)
def test_convert_bytes_to_array_vanilla(b: bytes):
    assert isinstance(convert_bytes_to_array(
        b), np.ndarray), f"No lo transforma a un array de numpy."

@pytest.mark.parametrize(
    "size",
    [x for x in range(100)]
)
def test_create_datasets(size):
    # Creamos un dataset.
    create_dataset(size)
    try:
        f = open("dataset.json", "r")
    except:
        assert False, "El archivo dataset no fue creado."

    # Probamos si no esta corrupto el archivo creado.
    try:
        txt_test = f.read()
    except:
        assert False, "El archivo creado esta corrupto."
    # Probamos si es leido por JSON.
    try:
        datasets_test = json.loads(txt_test)
    except:
        assert False, "El archivo no es aceptado por JSON."
    # Verificamos si estan todos los datasets
    for df in ["train", "valid", "test"]:
        try:
            datasets_test[df]
        except:
            assert False, f"No se encuentra el datasets {df}."
    # Verificamos que los datasets estan balanceados.
    aux = 0
    for df in ["train", "valid", "test"]:
        aux += len(datasets_test[df])
    assert aux % 3 == 0, "Los datasets no estan balanceados."


@pytest.mark.parametrize(
    "dataset",
    [("train"),
     ("valid"),
     ("test"),
     ]
)
def test_get_dataset(dataset: str):
    x, y = get_dataset(dataset)
    assert isinstance(
        x, np.ndarray), "Los datos no estan en formato array de Numpy."
    for x_elem in x:
        assert isinstance(
            x_elem, np.ndarray), "Los datos no estan en formato array de Numpy."
    assert isinstance(
        y, np.ndarray), "La clase no estan en formato entero."
    for y_element in y:
        assert type(y_element) == np.int8, "La clase no estan en formato entero."
