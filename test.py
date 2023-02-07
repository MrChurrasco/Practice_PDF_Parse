from methods import *
from pathlib import Path
import os

home = Path(os.getcwd())

dir_format1 = [(path, str(path).split("\\")[-2:]) for path in Path(home,"Asistencia SIGE","Marzo-Nov","Formato 1").glob("**/*.pdf")]

dir_format2 = [(path, str(path).split("\\")[-2:] ) for path in Path(home,"Asistencia SIGE","Marzo-Nov","Formato 2").glob("**/*.pdf")]

dir_format3 = [(path, str(path).split("\\")[-2:] ) for path in Path(home,"Asistencia SIGE","Marzo-Nov","Formato 3").glob("**/*.pdf")]

## TEST FOMARTO
def main():
    for directory, name in [(dir_format1,"Formato 1"),(dir_format2,"Formato 2"), (dir_format3,"Formato 3")]:
        for dir_pdf, [rbd, name_pdf] in directory:

            doc_pdf = fitz.open(dir_pdf)
            try:
                parse_format1(doc_pdf)
            except:
                assert False, f"\nEl documento del formato: {name} de RBD: {rbd}\ny de nombre: {name_pdf} no esta siendo leído correctamente.\nRevise el archivo de path:\n{dir_pdf}"

        print(f"Los archivos del {name} están digitalizados")

    print("Todo salió genial!")

if __name__=='__main__':
    main()