from django import http
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from Fase2.Estructuras.ArbolB import arbolB
from Fase2.Graficar.graficar import *
from Fase2.CargaArchivos.CargaMasiva import *
from Fase2.Estructuras.ArbolAVL import *
from Fase2.Estructuras.matriz_dispersa import *
import json,gc

from Fase2.Objetos import estudiante
from Fase2.Objetos.tareas import Tarea

arbolEstudiantes = arbolAVL()
arbol_cursos_pensum = arbolB(5)
indice_reporte=0



@csrf_exempt
def cargaMasiva(request):    
    
    global arbolEstudiantes, arbol_cursos_pensum

    if request.method=="POST":        
        instrucciones_json = json.loads(request.body)
        if "tipo" in instrucciones_json[0].keys():
            #Carga de estudiantes dentro del arbol AVL
            if str.lower(instrucciones_json[0].get("tipo")) == "estudiante":                
                cargaMasivaEstudiantes(instrucciones_json[0].get("path"), arbolEstudiantes)               
            #Carga de cursos de pensum dentro de arbol B                
            elif str.lower(instrucciones_json[0].get("tipo")) == "cursos_pensum":
                cargaMasicaCursosPensum(instrucciones_json[0].get("path"), arbol_cursos_pensum)                
            elif str.lower(instrucciones_json[0].get("tipo")) == "curso":
                cargaMasivaCursos(instrucciones_json[0].get("path"), arbolEstudiantes)
                
        else:
            print("MALA CARGA")


    return HttpResponse("Cargado con exito")

@csrf_exempt
def reportes(request):  

    global arbolEstudiantes, arbol_cursos_pensum, indice_reporte

    if request.method=="GET":        
        instrucciones_json = json.loads(request.body)
        if "tipo" in instrucciones_json[0].keys():
            #Reporte ArbolAVL
            if instrucciones_json[0].get("tipo") == 0:
                indice_reporte=+1
                graficarArbolAVL(arbolEstudiantes.raiz,indice_reporte)
            elif instrucciones_json[0].get("tipo") == 1:

                carnet = instrucciones_json[0].get("carnet")
                anio = instrucciones_json[0].get("año")
                mes = instrucciones_json[0].get("mes")

                est = buscar_dentro_AVL(arbolEstudiantes.raiz,int(carnet))

                if est != None:                    
                    matr = buscar_matriz_dispersa(est,int(anio),int(mes))
                    if matr != None:
                        indice_reporte=+1
                        graficar_matriz_dispersa(matr,indice_reporte)
                    else:
                        print("No se encontro la matriz")
                else:
                    print("No se encontro al estudiante")

            elif instrucciones_json[0].get("tipo") == 2:
                carnet = instrucciones_json[0].get("carnet")
                anio = instrucciones_json[0].get("año")
                mes = instrucciones_json[0].get("mes")
                dia = instrucciones_json[0].get("dia")
                hora = instrucciones_json[0].get("hora")

                est = buscar_dentro_AVL(arbolEstudiantes.raiz,int(carnet))

                if est != None:                    
                    matr = buscar_matriz_dispersa(est,int(anio),int(mes))
                    if matr != None:
                        lista = matr.buscar(int(hora),int(dia))
                        if lista != None:
                            indice_reporte=+1
                            graficarLD(lista.cabeza,indice_reporte)
                        else:
                            print("No se encontro ninguna tarea en el dia y la hora dados")
                    else:
                        print("No se encontro la matriz")
                else:
                    print("No se encontro al estudiante")
        
            elif instrucciones_json[0].get("tipo") == 3:
                indice_reporte+=1
                graficar_arbol_b(arbol_cursos_pensum,indice_reporte)

            elif instrucciones_json[0].get("tipo") == 4:
                carnet = instrucciones_json[0].get("carnet")
                anio = instrucciones_json[0].get("año")
                semestre = instrucciones_json[0].get("semestre")
                
                est = buscar_dentro_AVL(arbolEstudiantes.raiz,int(carnet))

                if est != None:
                    if est.yearList != None:
                        nodo_anio = est.yearList.buscar(int(anio))
                        if nodo_anio != None:
                            if nodo_anio.conexion1 != None:
                                nodo_semestre = nodo_anio.conexion1.buscar(int(semestre))
                                if nodo_semestre != None:
                                    if nodo_semestre.conexion1!=None:
                                        indice_reporte+=1
                                        graficar_arbol_b(nodo_semestre.conexion1,indice_reporte)
                                    else:
                                        print("No hay cursos en el semestre dado")
                                else:
                                    print("No existe el semestre dado")
                            else:
                                print("No hay semestres registrados")
                        else:
                            print("No existe informacion del año dado")
                    else:
                        print("No hay años ingresados")
                else:
                    print("No existe el estudiante")
        else:
            print("MAL REPORTE")


    return HttpResponse("Reporte con exito")


@csrf_exempt
def crud_estudiantes(request): 

    global arbolEstudiantes, arbol_cursos_pensum

    if request.method=="POST": 
        instrucciones_json = json.loads(request.body)
        est = Estudiantes()
        est.carnet=instrucciones_json.get("carnet")
        est.dpi=instrucciones_json.get("DPI")
        est.nombre=instrucciones_json.get("nombre")
        est.carrera=instrucciones_json.get("carrera")
        est.correo=instrucciones_json.get("correo")
        est.password=instrucciones_json.get("password")
        est.creditos=instrucciones_json.get("creditos")
        est.edad=instrucciones_json.get("edad")
        
        arbolEstudiantes.agregar(int(est.carnet),est)
        return HttpResponse("Estudiante agregado con exito")
    elif request.method=="PUT": 
        instrucciones_json = json.loads(request.body)   
        carnet=instrucciones_json.get("carnet")             
        est = buscar_dentro_AVL(arbolEstudiantes.raiz,int(carnet))

        if est != None:
            est.carnet=instrucciones_json.get("carnet")
            est.dpi=instrucciones_json.get("DPI")
            est.nombre=instrucciones_json.get("nombre")
            est.carrera=instrucciones_json.get("carrera")
            est.correo=instrucciones_json.get("correo")
            est.password=instrucciones_json.get("password")
            est.creditos=instrucciones_json.get("creditos")
            est.edad=instrucciones_json.get("edad")
            return HttpResponse("Estudiante modificado con exito")
        else:
            return HttpResponse("No se encontro al estudiante")
    elif request.method=="GET": 
        instrucciones_json = json.loads(request.body) 
        carnet=instrucciones_json.get("carnet")             
        est = buscar_dentro_AVL(arbolEstudiantes.raiz,int(carnet))

        if est != None:
            tag = "Estudiante: \n "
            tag += "Carnet: " + str(est.carnet) + "\n"
            tag += "DPI: " + str(est.dpi) + "\n"
            tag += "Nombre: " + str(est.nombre) + "\n"
            tag += "Carrera: " + str(est.carrera) + "\n"
            tag += "Correo: " + str(est.correo) + "\n"
            tag += "Password: " + str(est.password) + "\n"
            tag += "Creditos: " + str(est.creditos) + "\n"
            tag += "Edad: " + str(est.edad)
            return HttpResponse(tag)
        else:
            return HttpResponse("No se encontro al estudiante")
    elif request.method=="DELETE": 
        instrucciones_json = json.loads(request.body) 
        carnet=instrucciones_json.get("carnet")             
        est = borrar_nodo(arbolEstudiantes.raiz,int(carnet))

        if est!= None:                        
            return HttpResponse("Eliminado con exito")
        else:
            return HttpResponse("No se encontro al estudiante")


@csrf_exempt
def crud_recordatorios(request): 

    global arbolEstudiantes

    if request.method=="POST":
        instrucciones_json = json.loads(request.body)   
        carnet=instrucciones_json.get("Carnet")             
        est = buscar_dentro_AVL(arbolEstudiantes.raiz,int(carnet))
        if est != None:
            if est.yearList == None:
                est.yearList = listaDoble()

            tar = Tarea()

            tar.carnet  = instrucciones_json.get("Carnet")  
            tar.nombre  = instrucciones_json.get("Nombre")  
            tar.descripcion  = instrucciones_json.get("Descripcion")  
            tar.materia  = instrucciones_json.get("Materia")  
            #FECHA 
            separacion = re.split("/",instrucciones_json.get("Fecha"))
            tar.dia=separacion[0]
            tar.mes=separacion[1]
            tar.anio=separacion[2]
            #HORA         
            separacion = re.split(":",instrucciones_json.get("Hora"))
            tar.hora=separacion[0]

            tar.estado  = instrucciones_json.get("Estado")  
            
            buscar_y_agregar_tarea(est.yearList , copy.copy(int(tar.anio))
                                            ,copy.copy(int(tar.mes)),copy.copy(int(tar.dia))
                                            ,copy.copy(int(tar.hora)),copy.deepcopy(tar))

            return HttpResponse("Recordatorio agregado con exito")
        else:
            return HttpResponse("Estudiante no existe")
    elif request.method=="PUT":
        instrucciones_json = json.loads(request.body)   
        carnet=instrucciones_json.get("Carnet")             
        est = buscar_dentro_AVL(arbolEstudiantes.raiz,int(carnet))

        if est != None:
            if est.yearList == None:
                est.yearList = listaDoble()

        #FECHA 
            separacion = re.split("/",instrucciones_json.get("Fecha"))
            dia=separacion[0]
            mes=separacion[1]
            anio=separacion[2]
            #HORA         
            separacion = re.split(":",instrucciones_json.get("Hora"))
            hora=separacion[0]

            pos = instrucciones_json.get("Posicion")

            mat = buscar_matriz_dispersa(est,int(anio),int(mes))

            if mat != None:
                lista_tareas=mat.buscar(int(hora),int(dia))
                if lista_tareas !=None:                    
                    nodo= lista_tareas.buscar_posicion(int(pos))
                                        
                    nodo.carnet = instrucciones_json.get("Carnet") 
                    nodo.nombre = instrucciones_json.get("Nombre") 
                    nodo.descripcion = instrucciones_json.get("Descripcion") 
                    nodo.materia = instrucciones_json.get("Materia") 
                    nodo.anio = anio
                    nodo.mes = mes
                    nodo.dia = dia 
                    nodo.hora = hora 
                    nodo.estado = instrucciones_json.get("Estado")                     
                    return HttpResponse("Se ha modificado con exito")
                else:
                    return HttpResponse("No hay tareas en esa dia y hora")
            else:
                return HttpResponse("No hay tareas en ese mes")
        else:
            return HttpResponse("No se encontro al estudiante")
                
            
    elif request.method=="GET":
        instrucciones_json = json.loads(request.body)   
        carnet=instrucciones_json.get("Carnet")             
        est = buscar_dentro_AVL(arbolEstudiantes.raiz,int(carnet))

        if est != None:
            if est.yearList == None:
                est.yearList = listaDoble()

        #FECHA 
            separacion = re.split("/",instrucciones_json.get("Fecha"))
            dia=separacion[0]
            mes=separacion[1]
            anio=separacion[2]
            #HORA         
            separacion = re.split(":",instrucciones_json.get("Hora"))
            hora=separacion[0]

            pos = instrucciones_json.get("Posicion")

            mat = buscar_matriz_dispersa(est,int(anio),int(mes))

            if mat != None:
                lista_tareas=mat.buscar(int(hora),int(dia))
                if lista_tareas !=None:                    
                    nodo= lista_tareas.buscar_posicion(int(pos))
                                        

                    tag = "Carnet: " + str(nodo.carnet) + "\n"
                    tag += "Nombre: " + str(nodo.nombre) + "\n"
                    tag += "Descripcion: " + str(nodo.descripcion) + "\n"
                    tag += "Materia: " + str(nodo.materia) + "\n"
                    tag += "Fecha: " + str(nodo.dia) +"/"+ str(nodo.mes) +"/"+ str(nodo.anio) + "\n"                    
                    tag += "Hora: " + str(nodo.hora) + ":00" + "\n"
                    tag += "Estado: " + str(nodo.estado) + "\n"
                    return HttpResponse(tag)
                else:
                    return HttpResponse("No hay tareas en esa dia y hora")
            else:
                return HttpResponse("No hay tareas en ese mes")
        else:
            return HttpResponse("No se encontro al estudiante") 

@csrf_exempt
def crud_cursosEstudiante(request):
    return HttpResponse("buenas")


@csrf_exempt
def crud_cursosPensum(request):
    global arbol_cursos_pensum
    instrucciones_json = json.loads(request.body)    

    if request.method=="POST":
        listaCursos = instrucciones_json.get("Cursos")
        
        for i in listaCursos:            
            nuevo_curso = Curso()
            nuevo_curso.codigo = int(i.get("Codigo"))
            nuevo_curso.nombre = i.get("Nombre")
            nuevo_curso.creditos = i.get("Creditos")
            nuevo_curso.pre_requisitos = i.get("Prerequisitos")
            nuevo_curso.obligatorio = i.get("Obligatorio")
            arbol_cursos_pensum.agregar(nodoArbolB(int(nuevo_curso.codigo),nuevo_curso))
        

    return HttpResponse("buenas")

@csrf_exempt
def pruebas(request):    
    if request.method=="POST":        
        #instrucciones_json = json.loads(request.body)
        matriz_prueba.agregar(1,1,1)
        matriz_prueba.agregar(1,1,122)
        matriz_prueba.agregar(1,1,133)
        matriz_prueba.agregar(1,3,2)
        matriz_prueba.agregar(1,2,3)
        matriz_prueba.agregar(2,8,4)
        matriz_prueba.agregar(3,4,5)
        matriz_prueba.agregar(7,3,6)
        graficar_matriz_dispersa(matriz_prueba,0)

    return HttpResponse("Buenas")