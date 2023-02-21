import fitz
import numpy as np

from constants import *
from methods import *


def main(list_doc_pdf: list, template: int = 1) -> list:

    res = []
    error = []

    if type(list_doc_pdf) == str:

        list_doc_pdf = [list_doc_pdf]

    for doc_pdf in list_doc_pdf:
        try:
            ####
            if template == 1:
                pdf = fitz.open(doc_pdf)
                res.append(parse_format1(pdf))
            else:
                pdf = fitz.open(doc_pdf)
                res.append(parse_format2(pdf), 0)
        except:
            error.append(doc_pdf)

    res = pd.concat(res)

    res["RBD"] = pd.to_numeric(res["RBD"], downcast="unsigned")

    res["Asistencia"] = pd.to_numeric(res["Asistencia"], downcast="signed")

    res["Fecha"] = pd.to_datetime(res["Fecha"])

    res = res.astype({"Alumno": "string",
                      "Curso": "string"
                      })

    falla = res[res["Alumno"] == ""]["RBD"].unique()

    res = res[res["Alumno"] != ""]

    return {"data": res,
            "error": error,
            "RBD_falla": falla
            }


if __name__ == '__main__':
    a = input()
    print(main(a))
