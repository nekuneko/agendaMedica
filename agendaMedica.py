import json
import os
import sys
import platform 
import time

# Modifique esta variable con su nombre
str_nombrePaciente = "Neku"
str_nombreAgenda 	 = "agenda.json"




# limpiar la pantalla, independiente de cada sistema operativo
def limpiarPantalla():
	if platform.system() == 'Windows':
		os.system('cls')
	else: # Linux || OSX
		os.system('clear')


def mecanografiar(texto, velocidad=0.10):
	lista = texto.split()
	for palabra in lista:
		sys.stdout.write(palabra + " ")
		sys.stdout.flush()
		time.sleep(velocidad)
	sys.stdout.flush() # limpiar el buffer final
	print(end='\n')


def salirPrograma ():
	limpiarPantalla()
	print("¡Hasta la próxima! ^^")
	sys.exit(0)







## MAIN
char_c = ''
while (char_c not in ['n', 'N', 's', 'S']):
	limpiarPantalla()
	mecanografiar("Buenas noches, " + str_nombrePaciente + ".")
	mecanografiar("Soy ")
	mecanografiar("Hoy es " + time.strftime("%A %d de %B de %Y")) # Miércoles 07 de Junio de 2017 
	input()	# getch
	mecanografiar("¿Quieres abrir una entrada?")
	print(" n - No")
	print(" s - Sí")
	char_c = str(input())


# Salir del programa si no quiere abrir una etnrada
if (char_c in ['n', 'N']):
	salirPrograma()


# Cargar fichero agenda con los registros
try:
	limpiarPantalla()
	mecanografiar("Estoy cargando los registros anteriores...")
	with open(str_nombreAgenda) as json_file:  
		agenda = json.load(json_file)
	bool_hayRegistros = True
except Exception as e:
	limpiarPantalla()
	mecanografiar("No tengo registrado nada sobre ti.")
	mecanografiar("No te preocupes, ahora mismo te creo una ficha.")
	input()
	agenda = {}
	bool_hayRegistros = False

if (bool_hayRegistros):
	limpiarPantalla()
	mecanografiar("He cargado los registros anteriores, podemos continuar.")
	input() #getch


# Registrar timestamp, indice de la entrada en la agenda, una por día
idx_entrada = time.strftime("%Y%m%d") # 2017 06 07 AÑO MES DIA

# Comprobar si ya se ha escrito una entrada hoy
if idx_entrada in list(agenda.keys()):
	char_c = ''
	while char_c not in ['n', 'N', 's', 'S']:
		limpiarPantalla()
		mecanografiar("Parece que hoy ya habías registrado una entrada.")
		mecanografiar("¿Quieres verla?")
		print(" n - No")
		print(" s - Sí")
		char_c = str(input())

	if (char_c in ['s', 'S']):
		limpiarPantalla()
		mecanografiar("Estos son los datos que tengo registrados...")
		mecanografiar("- sintomas: " + agenda[idx_entrada]["sintomas"])
		mecanografiar("- medicación:")
		print("   + desayuno: ", end="") 
		mecanografiar(agenda[idx_entrada]["medicacion"]["desayuno"])
		print("   + comida:   ", end="") 
		mecanografiar(agenda[idx_entrada]["medicacion"]["comida"])
		print("   + cena:     ", end="") 
		mecanografiar(agenda[idx_entrada]["medicacion"]["cena"])
		input()

	char_c = ''
	while char_c not in ['n', 'N', 's', 'S']:
		limpiarPantalla()
		mecanografiar("¿Quieres que la sobreescriba la entrada actual?")
		print(" n - No")
		print(" s - Sí")
		char_c = str(input())

	if char_c in ['n', 'N']:
		salirPrograma()


# Incorporar sintomatología
limpiarPantalla()
print("¿Cómo ha sido el día? (Describe sintomas)")
str_sintomasDia = str(input())

limpiarPantalla()
mecanografiar("Gracias, tomo nota.")
input() # getch


# Preguntar por medicación
char_c = ''
while (char_c not in ['n', 'N', 's', 'S']):
	limpiarPantalla()
	mecanografiar("¿Hoy has tomado medicación?")
	print(" n - No")
	print(" s - Sí")
	char_c = str(input())

if (char_c in ['s', 'S']):
	limpiarPantalla()
	mecanografiar("Desayuno:")
	str_medicacionDesayuno = str(input())

	limpiarPantalla()
	mecanografiar("Comida:")
	str_medicacionComida = str(input())

	limpiarPantalla()
	mecanografiar("Cena:")
	str_medicacionCena = str(input())
else:
	str_medicacionDesayuno 	= ''
	str_medicacionComida		= ''
	str_medicacionCena 			= ''





# Añadir datos a la agenda
limpiarPantalla()
mecanografiar("Estoy insertando los nuevos datos en la agenda, espera un segundo.")
# formateo de la entrada
dic_entrada = {"sintomas": str_sintomasDia, 
							 "medicacion": {
							 		"desayuno": str_medicacionDesayuno, 
							 		"comida": 	str_medicacionComida, 
							 		"cena": 		str_medicacionCena}}

# insertar
agenda[idx_entrada] = dic_entrada
	
# Guardar fichero agenda
try:
	limpiarPantalla()
	mecanografiar("Ahora estoy guardando la agenda en un fichero. No te vayas todavía.")
	with open(str_nombreAgenda, 'w') as outfile:  
		json.dump(agenda, outfile)
except Exception as e:
	limpiarPantalla()
	mecanografiar("Ha ocurrido un error mientras guardaba los datos.")
	mecanografiar("Lo siento muchísimo, esto es lo que sé al respecto:")
	raise e

limpiarPantalla()
mecanografiar("Entrada registrada, informe completo por hoy.")
mecanografiar("¡Que duermas bien! =^w^=")
input()
