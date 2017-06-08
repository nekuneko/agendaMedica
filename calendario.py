# pip3 install --upgrade httplib2 oauth2client google-api-python-client

from __future__ import print_function
import httplib2
import os

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

# Leer calendario desde fichero, en el fichero se guarda el ID de Calendar
# Este código se puede extraer desde Google Calendar, haciendo clic sobre la
# flecha a la derecha del calendario y luego en Configuracion de Calendario
# es de la forma ijdkaskdljkl32423@group.calendar.google.com
# el fichero solo debe contener una línea con este ID de calendario
with open ("calendario.txt") as file:
	str_calendarId = file.readline()



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
		credential_path = os.path.join(credential_dir,
																	 'calendar-python-quickstart.json')

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



dic_tituloEvento = {"3": "Malo", "2": "Regular", "1": "Bueno", "0": "NoValorado"}
dic_colorId = {"malo": "0", "regular": 5, "bueno": 2, "novalorado": 1} # Google API: 0 - rojo, 5 - amarillo, 2 - verde




def subirEntrada (dic_entrada):
	# Identificarse y elegir calendario
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	str_descripcion = (dic_entrada["sintomas"] +
										"\nmedicación:"  + 
										"\n  + desayuno: " + dic_entrada["medicacion"]["desayuno"] + 
										"\n  + comida:   " + dic_entrada["medicacion"]["comida"] +
										"\n  + cena:     " + dic_entrada["medicacion"]["cena"])
	
	str_fecha = dic_entrada["fecha"]
	str_fecha = str_fecha[:4] + '-' + str_fecha[4:6] + '-' + str_fecha[6:]

	str_valoracion = dic_entrada["valoracion"]


	event = {
		# Título del evento: Valoración Bueno, Malo, Regular
		'summary': dic_tituloEvento[str_valoracion].title(),
		# Descripción de los síntomas del día.
		'description': str_descripcion,
		# evento durante todo el día
		'start': {
			'date': str_fecha},
		'end': {
			'date': str_fecha},
		# color del evento en función del título
		'colorId': dic_colorId[dic_tituloEvento[str_valoracion].lower()],
	}


	# Publicar evento en calendario
	try:
		event = service.events().insert(calendarId=str_calendarId, body=event).execute()
		bool_exito = True
	except Exception as e:
		bool_exito = False

	return bool_exito



# Sube todos los registros de la agenda
def subirAgenda (str_agenda = "agenda.json"):
	# Identificarse
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	# INCOMPLETO



		

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
