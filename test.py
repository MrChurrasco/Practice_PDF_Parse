from methods import *


## TEST Unificación de filas si hacen alusión al mismo alumno
def main():
    test_dictA = {"Alumno": ["alumn1",
                            "alumn2A",
                            "alumn2A"],
                 "c1": [1,-5,0],
                 "c2": [1, 0,-5],
                 "c3": [0,-5,1],
                 "c4": [0,-5,0]
                 }
    test_dictB = {"Alumno": ["alumn1",
                            "alumn2A"],
                 "c1": [1, 0],
                 "c2": [1, 0],
                 "c3": [0, 1],
                 "c4": [0, 0]
                 }
    test_dfA = pd.DataFrame(test_dictA)
    test_dfB = pd.DataFrame(test_dictB)
    
    assert test_dfB.equals(fix_names(test_dfA)), f"La función fix_names no unifica los alumnos con el mismo nombre en una misma fila"

    print(f"Los archivos del {name} están digitalizados")

    print("Todo salió genial!")

if __name__=='__main__':
    main()
