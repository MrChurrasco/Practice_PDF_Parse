```python
def get_alumno_id(df_asistencia: pd.DataFrame, df_alumnos: pd.DataFrame) -> pd.DataFrame:

    # Filtramos y ordenamos los datos que necesitamos de los datasets
    # para su posterior
    df_asistencia_f, df_alumnos_f = filtrado_df(df_asistencia, df_alumnos)
    
    # Calculamos un threshold para cuando queramos clasificar por la distancia
    # de Levenshtein
    
    best_threshold = np.array([best_threshold_otsu_method(df_asistencia_f["name"][df_asistencia_f["RBD"]==rbd].to_list(),
                                                          df_alumnos_f["name"][df_alumnos_f["rbd"]==rbd].to_list()) for rbd in df_asistencia_f.RBD.unique()]).mean()

    # Obtenemos el conjunto de todos los RBD del DataFrame de asistencia
    rbds = df_asistencia_f.RBD.unique()

    # Realizamos, de manera paralela, la búsqueda de los ids dado un nombre por RBD,
    # la guardaremos todos los resultados en una lista
    list_res = [get_id_for_rbd(df_asistencia_f, df_alumnos_f, rbd, best_threshold)
                for rbd in rbds]

    # Dado que los resultados están todos en listas, unimos todas las lista en una sola.
    ##
    # La lista resultante tendrá pares (nombre, id) que es lo que necesitamos para
    # identificar al alumno en el dataset de asistencias.
    #
    list_id_nombre = []
    for res_rbd in list_res:
        for res in res_rbd:
            list_id_nombre += res
    #
    # Ahora que se tienen la lista de los pares (nombre,id) podemos separarlos
    # ordenadamente, de manera que no perder nuestro trabajo.
    lista_nombre, lista_id = zip(*list_id_nombre)
    #
    # Lo guardamos en un nuevo DataFrame
    df_name_id = pd.DataFrame({"name_asist": lista_nombre,
                              "name_id": lista_id
                              })
    #
    # y retornamos el dataset de la asistencia asignándole a cada alumno su respectiva id
    
    df_aux = df_name_id.merge(right=df_asistencia_f[["name","Alumno"]],left_on="name_asist",right_on="name",how="outer")
    df_aux = df_aux.merge(right=df_alumnos_f[["name","usuario_id"]],left_on="name_id",right_on="name",how="outer").dropna()
    # return 
    return df_asistencia.merge(right=df_aux[["Alumno","usuario_id"]],on="Alumno").dropna()


def filtrado_df(df_asistencia: pd.DataFrame, df_alumnos: pd.DataFrame) -> list:

    # Filtramos el dataset de asistencias con lo que se necesita
    df_asistencia_f = df_asistencia[["RBD", "Alumno"]].sort_values(by="Alumno")

    # Filtramos y arreglamos el dataset de los ids para poder trabajar
    # eficientemente con los nombres.

    # Arreglamos los nombres y apellidos de manera que tenga el mismo formato
    # que los nombres de los alumnos del otro dataset
    df_alumnos_f = df_alumnos.assign(Alumno=lambda x: (
        x.apellido_paterno + " " + x.apellido_materno + " " + x.nombre))

    # Filtramos los datos que necesitamos
    df_alumnos_f = df_alumnos_f[["usuario_id", "Alumno", "rbd"]].sort_values(by="Alumno")

    # Normalizamos el string de los nombres de los alumnos en cada dataset
    df_asistencia_f = df_asistencia_f.assign(
        name=lambda x: x.Alumno.map(lambda y: normalizar_strings(y.lower())))
    df_alumnos_f = df_alumnos_f.assign(
        name=lambda x: x.Alumno.map(lambda y: normalizar_strings(y.lower())))
    # Retornamos los dataset filtrados y arreglados para trabajar
    return [df_asistencia_f, df_alumnos_f]


def normalizar_strings(s: str) -> str:

    # -> NFD y eliminar diacríticos
    s = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
               normalize("NFD", s), 0, re.I
               )

    # -> NFC
    return normalize('NFC', s)


def get_id_for_rbd(df_asistencia_f, df_alumnos_f, rbd, th):

    # Primero filtraremos los nombres e ids de los datasets por el RBD dado
    # Así obtendremos eficientemente la información necesaria para aplicar
    # nuestro algoritmo de NLP para identificar el id dl alumno en base a
    # su nombre.
    #
    # El resultado de los datos filtrados en cada dataset serán guardados en listas
    list_names_asist = df_asistencia_f["name"][df_asistencia_f["RBD"] == rbd].to_list()
    
    list_alumnos_idx = df_alumnos_f["name"][df_alumnos_f["rbd"] == rbd].to_list()

    # Con ambas listas de nombres obtenidas podemos aplicar una función que se encargue
    # de entregar un listado de pares (nombre_alumno, id)

    return get_id(list_names_asist, list_alumnos_idx, th)


def get_id(list_names_asist: list, list_alumnos_idx: list, th:float) -> list:

    # Para obtener el id pasaremos los nombres por una serie de algoritmos estratificados
    
    list_asist_idx = []
    
    
    for fun_in_matrix in [string_equals,string_in_other_string]:
        
        if len(list_names_asist)==0 or len(list_alumnos_idx)==0: 
            break
        
        matrix = create_matrix(list_names_asist, list_alumnos_idx, fun_in_matrix)
        
        output, list_names_asist, list_alumnos_idx = resolve_matrix_equals(matrix,list_names_asist,list_alumnos_idx)
        
        list_asist_idx.append(output)
        
    # Primero lo pasamos ambos listados por un algoritmo que relacione los nombres
    # mediante la distancia de Leviesh, retornará 3 listas. Una lista con los nombres que se logra
    # asociar, las otras 2 listas son los nombres de las listas pasadas que no lograron asociarse
    
    for fun_in_matrix in [LD,comb_min_distance]:
        
        if len(list_names_asist)==0 or len(list_alumnos_idx)==0: 
            break
    
        matrix = create_matrix(list_names_asist, list_alumnos_idx, fun_in_matrix)
    
        output, list_names_asist, list_alumnos_idx = resolve_matrix_LD(matrix,list_names_asist,list_alumnos_idx, th)
        
        list_asist_idx.append(output)
     

    return list_asist_idx

```