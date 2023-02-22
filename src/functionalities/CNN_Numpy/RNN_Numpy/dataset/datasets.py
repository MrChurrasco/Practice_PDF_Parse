import io
import json

import numpy as np
from functionalities.CNN_Numpy.RNN_Numpy.dataset.imagenes import images
from PIL import Image


def convert_bytes_to_array(bytes: bytes, vanilla: bool = True) -> np.ndarray:
    if vanilla:
        return np.asarray(Image.open(io.BytesIO(bytes)))
    else:
        num_aux = np.random.randint(7, dtype=np.int32)
        i = np.random.randint(5, dtype=np.int32)
        j = np.random.randint(5, dtype=np.int32)
        img_array = np.asarray(Image.open(
            io.BytesIO(bytes)).transpose(num_aux))# type: ignore
        noise = np.random.binomial(n=256, p=0.5, size=img_array.shape)
        img_noise = img_array + noise
        return ((img_noise-img_noise.min())/(img_noise.max()-img_noise.min()))[i:14+i, j:14+j, :]


def create_dataset(size:int):
    # Creamos un diccionario en donde tendremos nuestro dataset
    dataset: dict[str, list] = {"train": [],
                                "valid": [],
                                "test": [],
                                }

    PARSE_TABLE: dict[str, int] = {"ausente": 0,  # "X"
                                   "presente": 1,  # "*"
                                   "dia_no_trabajado": -1,  # "N"
                                   "sin asistencia": -2,  # "S"
                                   "otros": -3}  # "O"  no matriculado, retirado o inicio de clases

    # Convertimos las imagenes en array y las incluimos en cada datasets
    for y, list_bytes_x in images.items():
        for bytes_x in np.random.choice(list_bytes_x, size):
            for key in dataset.keys():
                dataset[key].append(
                    (convert_bytes_to_array(bytes_x, vanilla=False).tolist(), PARSE_TABLE[y]))

    # Guardamos con JSON la información
    txt = json.dumps(dataset, indent=4)
    f = open("dataset.json", "w")
    f.write(txt)


def get_dataset(dataset: str) -> tuple[np.ndarray, np.ndarray]:
    f = open("dataset.json", "r")
    txt = f.read()
    datasets = json.loads(txt)
    data = datasets[dataset]
    listX, listY = zip(*data)
    X = np.array([np.array(v) for v in listX])
    Y = np.array([v for v in listY],dtype=np.int8)
    return (X, Y)
