import datetime
import io

import fitz
import numpy as np
import pandas as pd
from PIL import Image

import imagenes
from constants import *


def get_info_in_blocks(doc_pdf: fitz.Document) -> list:

    list_blocks = []

    for i in range(doc_pdf.page_count):
        list_blocks += doc_pdf[i].get_text("dict")["blocks"]

    return list_blocks


def name_image(image_bin: str) -> str:

    for key, value in imagenes.images.items():
        if image_bin in value:
            return key


def parse_image(image_block: dict) -> list:

    image_bin = image_block["image"]

    name = name_image(image_bin)
       
    return PARSE_TABLE.get(name, "")


def parse_text(text_block: dict) -> str:
    parse = []

    if "lines" in text_block.keys():

        for spans_block in text_block["lines"]:
            if spans_block["spans"] != []:
                parse += [spans_block["spans"][0]["text"]]
            else:
                parse += spans_block["spans"]
        


    return " ".join(parse)


def parse_blocks(list_blocks: list) -> None:

    for i, block in enumerate(list_blocks):
        if "image" in block.keys():
            list_blocks[i] = parse_image(block)
        else:
            list_blocks[i] = parse_text(block)



def slice_for_word(lista:list[str|int] ,word:str)->list[list[str|int]]:
    for i, value in enumerate(lista):
        if type(value) == int:
            continue
        if word in value:
            return [lista[:i],lista[i:]]


def obtain_rbd_name(list_data: list) -> dict:
    search_data = {"RBD": None,
                   "Nombre Escuela": None}

    for data in list_data:
        if "RBD" in str(data):
            _, aux = data.split(":")
            aux, _ = aux.split("|")
            search_data["RBD"] = int(aux[:5])
            search_data["Nombre Escuela"] = aux[6:]
            break
    else:
        assert False, "No existe o no se encuentra el RBD en el listado."

    return search_data


def obtain_month_course(list_data: list) -> dict:
    search_data = {"Mes": None,
                   "Año": None,
                   "Curso": None}

    for data in list_data:
        if 'Año Declaración' in str(data):
            aux = data.split(" ")
            search_data["Mes"] = aux[2]
            search_data["Año"] = aux[3]
            break
    else:
        assert False, "No existe o no se encuentra el Mes y Año en el listado."

    for data in list_data:
        if 'Enseñanza' in str(data):
            _, aux = data.split("[")
            aux, _ = aux.split("]")
            search_data["Curso"] = aux
            break
    else:
        assert False, "No existe o no se encuentra el Curso en el listado."

    return search_data


def standard_table(list_data: list[str|int]) -> dict[str,np.ndarray[int]]:

    # Clean list data of unless data
    raw_data = list(map(lambda x: str(x).split(), list_data))
    meta_data = []
    i = 0
    while i < len(raw_data):
        element: list[str|int] = raw_data[i]
        if element != []:
            if element[0].isnumeric() or element[0] in ["-1","-2","-3"]:
                if len(element) == 1:
                    meta_data.append(int(element[0]))
                elif element[1].isalpha():
                    meta_data.append(" ".join(element[1:]))
        i += 1
        
    dict_tabla: dict[str, np.ndarray] = dict()
    list_aux: list[int] = []
    key_aux: str = ""
    for value in meta_data:
        if type(value) == int:
            list_aux.append(value)
        elif type(value) == str:
            if key_aux == "":
                key_aux = value
            else:
                dict_tabla[key_aux] = np.array(list_aux.copy(), dtype="int8")
                list_aux.clear()
                key_aux = value
    for key, value in dict_tabla.items():
        dict_tabla[key] = np.delete(value,-1)
    return dict_tabla
    # List data clean


def extract_info_table(dict_tabla: dict[str,np.ndarray[int]], doc_month: str) -> pd.DataFrame:

    df = pd.DataFrame(dict_tabla).reset_index()
    
    if np.unique(df.count().to_numpy()).shape[0] == 1:
        
        df = df.T
        df.columns = np.array(["Alumno"]+[date(2022, 4, 1)+timedelta(days=i)
                              for i in range(PARSE_STR_MONTH_TO_DATA[doc_month][1])])
    return df


def parse_format1(doc_pdf: fitz.Document) -> pd.DataFrame:

    list_blocks = get_info_in_blocks(doc_pdf)

    parse_blocks(list_blocks)

    list_data = split_info_template(TEMPLATE_FORM_1, list_blocks)

    data = obtain_month_course(list_data[1])

    data.update(obtain_rbd_name(list_data[0]))

    clean_table(list_data[2])

    table = extract_info_table(list_data[2], data["Mes"])

    return table.assign(RBD=data["RBD"])


def parse_format2(doc_pdf: fitz.Document, rbd: int) -> pd.DataFrame:

    list_blocks = get_info_in_blocks(doc_pdf)
    print(0)
    parse_blocks(list_blocks)
    print(1)
    part_month, table = slice_for_word(list_blocks,"Alumnos")
    print(2)
    data = obtain_month_course(part_month)
    print(3)
    metadata_dict = standard_table(table)
    print(4)
    table = extract_info_table(metadata_dict, data["mes"].title())
    print(5)
    return table.assign(RBD=rbd)


def parse_format3(doc_pdf: fitz.Document, rbd: int, mes: str) -> pd.DataFrame:

    list_blocks = get_info_in_blocks(doc_pdf)

    parse_blocks(list_blocks)
    
    metadata_dict = standard_table(list_blocks)
    
    table = extract_info_table(metadata_dict, mes.title())

    return table.assign(RBD=rbd)
