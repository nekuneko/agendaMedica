# pip3 install --upgrade pillow httplib2 oauth2client google-api-python-client

# Mejoras Pendientes
#  - Cifrar ficheros locales con contraseña.
#  - Eliminar necesidad del Oauth
#  - Comprobar si en la cuenta existe un calendario "alergia", sino crear uno nuevo

# Fe de erratas
# - Pueden crearse dos eventos el mismo día del calendario.


import os
import sys
import json
import getpass # para meter contraseñas: https://docs.python.org/2/library/getpass.html#module-getpass
import platform			# determinar si es windows 
import calendario 	# módulo local, Google Calendar
import time, locale
from imageToString import imgToStr 	# módulo local, Cargador de Imágenes
from calendario import dic_valoracion # 0: No valorado, 1: Bueno, 2: Regular, 3: Malo

# Modifique esta variable con su nombre
str_nombrePaciente = "Neku"
str_nombreAgenda 	 = "agenda.json"
str_imgAsistente   = imgToStr("rem.png", 60) 



# limpiar la pantalla, independiente de cada sistema operativo
def limpiarPantalla():
	if platform.system() == 'Windows':
		os.system('cls')
	else: # Linux || OSX
		os.system('clear')
	print(str_imgAsistente)


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
	mecanografiar("¡Hasta la próxima! ^-^")
	sys.exit(0)


int_momentoDia = 0 # 0 dia, 1 tarde, 2 noche
def determinarMensajeDia ():
	global int_momentoDia

	str_hora = time.strftime("%H")
	if (str_hora in ["06", "07", "08", "09", "10", "11", "12"]):
		int_momentoDia = "0"
		return "Buenos días"
	elif (str_hora in ["13", "14", "15", "16", "17", "18", "19", "20"]):
		int_momentoDia = "1"
		return "Buenas tardes"
	else:
		int_momentoDia = "2"
		return "Buenas noches"




## MAIN
# Utilizo el locale del sistema:
locale.setlocale(locale.LC_ALL, '')


char_c = ''
while (char_c not in ['n', 'N', 's', 'S']):
	limpiarPantalla()
	#print(str_imgAsistente)
	mecanografiar(determinarMensajeDia() + ", " + str_nombrePaciente + ".")
	mecanografiar("Soy Rem, tu asistente personal.")
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
	mecanografiar("¡Vaya!, no tengo registrado nada sobre ti.")
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
		mecanografiar("- sintomas: " + str(agenda[idx_entrada]["sintomas"]))
		mecanografiar("- medicación:")
		print("   + desayuno: ", end="") 
		mecanografiar(str(agenda[idx_entrada]["medicacion"]["desayuno"]))
		print("   + comida:   ", end="") 
		mecanografiar(str(agenda[idx_entrada]["medicacion"]["comida"]))
		print("   + cena:     ", end="") 
		mecanografiar(str(agenda[idx_entrada]["medicacion"]["cena"]))
		if (int(agenda[idx_entrada]["papelera"]) >= 0):
			mecanografiar("- papelera:    " + str(agenda[idx_entrada]["papelera"]) + "%")
		mecanografiar("- valoración: " + str(dic_valoracion[agenda[idx_entrada]["valoracion"]]))
		input()

	char_c = ''
	while char_c not in ['n', 'N', 's', 'S']:
		limpiarPantalla()
		mecanografiar("¿Quieres que la sobreescriba la entrada actual?")
		print(" n - No")
		print(" s - Sí")
		char_c = str(input())

	if char_c in ['n', 'N']:
		limpiarPantalla()
		char_c = ''
		while (char_c not in ['n', 'N', 's', 'S']):
			limpiarPantalla()
			mecanografiar("¿Quieres que suba la entrada de hoy a Google Calendar?")
			print(" n - No")
			print(" s - Sí")
			char_c = str(input())

		if (char_c in ['s', 'S']):
			bool_exito = calendario.subirEntrada(agenda[idx_entrada])

			if (bool_exito):
				mecanografiar("Entrada subida correctamente.")
			else:
				mecanografiar("Se produjo un error y no pude subir la entrada.")
		else:
			limpiarPantalla()
			mecanografiar("Vale.")
			input()
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



# Preguntar por porcentaje de papelera
limpiarPantalla()
mecanografiar("¿Cuál ha sido el porcentaje de la papelera?")
print("Introduzca un valor numérico de 0 a 150, o negativo si quiere saltar la valoración")
try:
	int_porcentaje = int(input())
except Exception as e:
	int_porcentaje = -1

if (int_porcentaje < 0):
	int_porcentaje = -1
elif (int_porcentaje > 150):
	int_porcentaje = 150




# Preguntar por valoración simple
char_valoracion =  ''
while (char_valoracion not in ['0', '1', '2', '3']):
	limpiarPantalla()
	mecanografiar("¿Cómo valoraría su estado de salud de hoy?")
	print(" 0 - Saltar valoración")
	print(" 1 - " + dic_valoracion['1']) # Bueno
	print(" 2 - " + dic_valoracion['2']) # Regular
	print(" 3 - " + dic_valoracion['3']) # Malo
	char_valoracion = str(input())

	if (char_valoracion in ['1', '2', '3']):
		char_c = ''
		while (char_c not in ['n', 'N', 's', 'S']):
			limpiarPantalla()
			mecanografiar("Su estado de salud de hoy ha sido " + dic_valoracion[char_valoracion].lower() + ".")
			mecanografiar("¿Es correcto?")
			print(" n - No")
			print(" s - Sí")
			char_c = str(input())

		if (char_c in ['n', 'N']):
			char_valoracion = ''


# Añadir datos a la agenda
limpiarPantalla()
mecanografiar("Estoy insertando los nuevos datos en la agenda, espera un segundo.")
# formateo de la entrada
dic_entrada = {
	"fecha": idx_entrada,
	"sintomas": str_sintomasDia, 
	"medicacion": {
		"desayuno": str_medicacionDesayuno, 
		"comida": 	str_medicacionComida, 
		"cena": 		str_medicacionCena},
	"papelera":   int_porcentaje,
	"valoracion": char_valoracion}

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
	mecanografiar("Estos son los datos que me has proporcionado, cópialos para que no se pierdan.")
	print("- sintomas:" + str_sintomasDia)
	print("- medicación:")
	print("   + desayuno: " + str_medicacionDesayuno)
	print("   + comida:   " + str_medicacionComida)
	print("   + cena:     " + str_medicacionCena)
	print("- papelera:    " + str(int_porcentaje))
	print("- valoración: "  + dic_valoracion[char_valoracion])
	mecanografiar("\nPulsa cualquier tecla para continuar")
	input()

	limpiarPantalla()
	mecanografiar("Lo siento muchísimo, esto es lo que sé al respecto sobre el error:")
	raise e

limpiarPantalla()
mecanografiar("Entrada registrada, informe completo por hoy.")
input()





char_c = ''
while (char_c not in ['n', 'N', 's', 'S']):
	limpiarPantalla()
	mecanografiar("¿Quieres que suba la entrada de hoy a Google Calendar?")
	print(" n - No")
	print(" s - Sí")
	char_c = str(input())

if (char_c in ['s', 'S']):
	bool_exito = calendario.subirEntrada(dic_entrada)

	if (bool_exito):
		mecanografiar("Entrada subida correctamente.")
	else:
		mecanografiar("Se produjo un error y no pude subir la entrada.")



# Despedida
dic_momentoDia = {
	'0': "¡Que pases un buen día!", 
	'1': "¡Aprovecha la tarde!",
	'2': "¡Que duermas bien!"}

limpiarPantalla()
mecanografiar(str(dic_momentoDia[int_momentoDia]) + " =^w^=")
