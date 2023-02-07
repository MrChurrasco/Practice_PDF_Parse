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


def obtain_rbd_name(list_data: list) -> int:
    search_data = 0

    for data in list_data:
        if "RBD" in str(data):
            _, aux = data.split(":")
            aux, _ = aux.split("|")
            search_data += int(aux[:5])
            break
    else:
        assert False, "No existe o no se encuentra el RBD en el listado."

    return search_data


def obtain_month_course(list_data: list) -> str:
    search_data = ""

    for data in list_data:
        if 'Año Declaración' in str(data):
            aux = data.split(" ")
            search_data += aux[2]
            break
    else:
        assert False, "No existe o no se encuentra el Mes y Año en el listado."

    return search_data


def standard_table(list_data: list[str|int]) -> dict[str,np.ndarray[int]]:

    # Clean list data of unless data
    raw_data = list(map(lambda x: str(x).split(), list_data))
    meta_data = []
    i = 0
    while i < len(raw_data):
        element: list[str] = raw_data[i]
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

    df = pd.DataFrame(dict_tabla)
    
    if np.unique(df.count().to_numpy()).shape[0] == 1:

        df = df.T.reset_index()
        df.columns = np.array(["Alumno"]+[date(2022, 4, 1)+timedelta(days=i)
                              for i in range(PARSE_STR_MONTH_TO_DATA[doc_month][1])])
    return df


def parse_format1(list_blocks_parsed:list[str|int]) -> pd.DataFrame:
    
    print(0)

    list_rbd, list_format2 = slice_for_word(list_blocks_parsed,"Detalle")
    print(1)

    rbd = obtain_rbd_name(list_rbd)
    print(2)

    return parse_format2(list_format2,rbd)


def parse_format2(list_blocks_parsed: list[str|int], rbd: int) -> pd.DataFrame:

    list_month, table = slice_for_word(list_blocks_parsed,"Alumnos")
    print(3)
    month = obtain_month_course(list_month)
    print(4)
    return parse_format3(table,rbd,month)


def parse_format3(list_blocks_parsed: list[str|int], rbd: int, mes: str) -> pd.DataFrame:
   
    metadata_dict = standard_table(list_blocks_parsed)
    
    print(5)
    
    table = extract_info_table(metadata_dict, mes.title())

    print(6)
    
    return table.assign(RBD=rbd)
