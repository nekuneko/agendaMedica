# pip3 install --upgrade httplib2 oauth2client google-api-python-client

from __future__ import print_function
import httplib2
import os
import json
import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime


try:
		import argparse
		flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
		flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
# solo lectura
#SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
# lectura y escritura
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

# Traducción de valoraciones a texto
dic_valoracion = {"0": "No valorado", "1": "Bueno", "2": "Regular", "3": "Malo"}

# Google API Colors: 1 purpura, 2 verde, 3 rosa, 4 5 amarillo, 7 aguamarina, 9 azul, 11 rojo
dic_colorId = {"no valorado": 9, "bueno": 2, "regular": 5, "malo": 11} 

# Habrá que introducir previamente el ID de Calendar en el fichero client_secret.json,
# "calendario": "jdkaskdljkl32423@group.calendar.google.com"
# 
# Este código se puede extraer desde Google Calendar, haciendo clic sobre la
# flecha a la derecha del calendario y luego en Configuracion de Calendario
with open (CLIENT_SECRET_FILE) as json_file:
	json_secret = json.load(json_file)
	str_calendarId = json_secret["calendario"]
json_file.close()



# La primera vez que se ejecute se abrirá un navegador web y pedirá permisos de
# escritura en los calendarios de google
def get_credentials():
		"""Gets valid user credentials from storage.

		If nothing has been stored, or if the stored credentials are invalid,
		the OAuth2 flow is completed to obtain the new credentials.

		Returns:
				Credentials, the obtained credential.
		"""
		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		if not os.path.exists(credential_dir):
				os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')

		store = Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
				flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
				flow.user_agent = APPLICATION_NAME
				if flags:
						credentials = tools.run_flow(flow, store, flags)
				else: # Needed only for compatibility with Python 2.6
						credentials = tools.run(flow, store)
				print('Storing credentials to ' + credential_path)
		return credentials




# Sube una entrada de la agenda médica a Google Calendar
def subirEntrada (dic_entrada):
	global str_calendarId
	
	# Identificarse y elegir calendario
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	str_descripcion = "sintomas:\n" + str(dic_entrada["sintomas"])

	if (str(dic_entrada["medicacion"]["desayuno"]) != '' or
		  str(dic_entrada["medicacion"]["comida"])   != '' or
		  str(dic_entrada["medicacion"]["cena"])     != ''):
		str_descripcion += "\nmedicación:"

	if (str(dic_entrada["medicacion"]["desayuno"]) != ''):
		str_descripcion += "\n  + desayuno: " + str(dic_entrada["medicacion"]["desayuno"])

	if (str(dic_entrada["medicacion"]["comida"]) != ''):
		str_descripcion += "\n  + comida: " + str(dic_entrada["medicacion"]["comida"])

	if (str(dic_entrada["medicacion"]["cena"]) != ''):
		str_descripcion += "\n  + cena: " + str(dic_entrada["medicacion"]["cena"])

	if (int(dic_entrada["papelera"]) >=0):
		str_descripcion += "\npapelera: " + str(dic_entrada["papelera"]) + "%"
	

	str_fecha = dic_entrada["fecha"]
	str_fecha = str_fecha[:4] + '-' + str_fecha[4:6] + '-' + str_fecha[6:]

	str_valoracion = dic_entrada["valoracion"]


	event = {
		# Título del evento: Valoración Bueno, Malo, Regular
		'summary': dic_valoracion[str_valoracion],
		# Descripción de los síntomas del día.
		'description': str_descripcion,
		# evento durante todo el día
		'start': {
			'date': str_fecha},
		'end': {
			'date': str_fecha},
		# color del evento en función del título
		'colorId': dic_colorId[dic_valoracion[str_valoracion].lower()],
	}

	# print(event)
	# Publicar evento en calendario
	try:
		event = service.events().insert(calendarId=str_calendarId, body=event).execute()
		bool_exito = True
	except Exception as e:
		bool_exito = False
		raise e

	return bool_exito




# sube un evento por fecha en la agenda, en formato YYYYMMDD
def subirFecha (str_fecha = time.strftime("%Y%m%d"), str_agenda = "agenda.json"):
	bool_exito = False
	with open (str_agenda) as inputFile:
		agenda = json.load(inputFile)
		try:
			dic_entrada = agenda[str_fecha]
			bool_exito = subirEntrada(dic_entrada)
		except Exception as e:
			print("No hay ninguna entrada en la agenda con fecha " + str_fecha + ".")
			#raise e
	inputFile.close()

	return bool_exito




# Sube todos los registros de la agenda a Google Calendar
def subirAgenda (str_agenda = "agenda.json"):
	with open (str_agenda) as json_file:
		agenda = json.load(json_file)
		list_fechas = sorted(agenda)

		for fecha in list_fechas:
			bool_exito = subirEntrada(agenda[fecha])
			#print(bool_exito)
	json_file.close()



# Elimina el calendario actual de Google Calendar
def eliminarCalendario ():
	global str_calendarId
	
	# Identificarse
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	# Limpiar entradas de calendario
	service.calendars().delete(calendarId=str_calendarId).execute()




# Crea un calendario nuevo y lo añade al fichero client_secret.json
def crearCalendario ():
	global str_calendarId
	global CLIENT_SECRET_FILE

	# Identificarse
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	calendar = {
		'summary': 'alergia',
		'description': "Calendario de sintomatología de alergias creado por agendaMedica.py"}

	created_calendar = service.calendars().insert(body=calendar).execute()
	
	str_calendarId = created_calendar['id']
	print(str_calendarId)

	# Guardar en fichero secreto
	json_secret = {}
	with open (CLIENT_SECRET_FILE) as inputFile:
		json_secret = json.load(inputFile)
	inputFile.close()
	
	json_secret["calendario"] = str_calendarId

	with open (CLIENT_SECRET_FILE, 'w') as outputFile:
		json.dump(json_secret, outputFile)
	outputFile.close()





		
# Para pruebas
def main():
	"""Shows basic usage of the Google Calendar API.

	Creates a Google Calendar API service object and outputs a list of the next
	10 events on the user's calendar.
	"""
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	print('Getting the upcoming 10 events')
	eventsResult = service.events().list(
			calendarId=str_calendarId, timeMin=now, maxResults=10, singleEvents=True,
			orderBy='startTime').execute()
	events = eventsResult.get('items', [])

	if not events:
			print('No upcoming events found.')
	for event in events:
			start = event['start'].get('dateTime', event['start'].get('date'))
			print(start, event['summary'])
	


	# Listar calendarios de la cuenta
	# page_token = None
	# while True:
	# 	calendar_list = service.calendarList().list(pageToken=page_token).execute()
	# 	for calendar_list_entry in calendar_list['items']:
	# 		print (calendar_list_entry['summary'])
	# 	page_token = calendar_list.get('nextPageToken')
	# 	if not page_token:
	# 		break
	
	calendar_list_entry = service.calendarList().get(calendarId=str_calendarId).execute()
	print(calendar_list_entry)

	if (calendar_list_entry['accessRole'] not in ['writer', 'owner']):
		print("Calendario de solo lectura")
	else:
		print("Calendario con permiso de escritura.")



	

	#print (event['summary'])

	
	# print ('Event created: %s' % (event.get('htmlLink')))

	# eliminar calendario
	#service.calendarList().delete(calendarId=str_calendarId).execute()


if __name__ == '__main__':
		main()
