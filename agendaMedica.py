# pip3 install --upgrade pillow httplib2 oauth2client google-api-python-client

# Mejoras Pendientes
#  - Cifrar ficheros locales con contraseña.
#  - Eliminar necesidad del Oauth
#  - Comprobar si en la cuenta existe un calendario "alergia", sino crear uno nuevo
#  - Subir una agenda completa a Google Calendar

# Fe de erratas
# - Pueden crearse dos eventos el mismo día del calendario.


import json
import os
import sys
import platform 
import time, locale
import getpass # para meter contraseñas: https://docs.python.org/2/library/getpass.html#module-getpass
import calendario
from imageToString import imgToStr


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


def determinarMensajeDia ():
	str_hora = time.strftime("%H")
	if (str_hora in ["06", "07", "08", "09", "10", "11", "12"]):
		return "Buenos días"
	elif (str_hora in ["13", "14", "15", "16", "17", "18", "19", "20"]):
		return "Buenas tardes"
	else:
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



estado = {"0": "none", "1": "bueno", "2": "regular", "3": "malo"}


# Preguntar por valoración simple
char_c =  ''
while (char_c not in ['0', '1', '2', '3']):
	limpiarPantalla()
	mecanografiar("¿Cómo valoraría su estado de salud de hoy?")
	print(" 0 - Saltar valoración")
	print(" 1 - Bueno")
	print(" 2 - Regular")
	print(" 3 - Malo")
	char_c = str(input())


str_estado = char_c
if (str_estado != "0"):
	char_c = ''
	while (char_c not in ['n', 'N', 's', 'S']):
		limpiarPantalla()
		mecanografiar("Su estado de salud de hoy ha sido " + estado[str_estado].lower() + ".")
		mecanografiar("¿Es correcto?")
		print(" n - No")
		print(" s - Sí")
		char_c = str(input())


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
	"valoracion": str_estado}

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
	print("- medicacion:")
	print("   + desayuno: " + str_medicacionDesayuno)
	print("   + comida:   " + str_medicacionComida)
	print("   + cena:     " + str_medicacionCena)
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




mecanografiar("¡Que duermas bien! =^w^=")
