# Modo de uso

## Configuraciones necesarias

Es necesario establecer el entorno de la API REST en Flask:
	cd /ADBD-2425/Practica-API
	python3 -m venv ./APIrest
	source ./APIrest/bin/activate

## Actividad 1

Ejecutar los siguientes comandos:
	
	cd books
	flask run
	
Es necesario también cambiar las variables necesarias dentro de `init_db.py` y `app.py` para la conexión a la base de datos:

- `init_db.py`:
	
		conn = psycopg2.connect(
  	      host='localhost', # Cambia según tu configuración
  	      database="api_db",
  	      user="postgres", # Cambia según tu configuración
  	      password="postgres" # Cambia según tu configuración
  	  )

- `app.py`:

		def get_db_connection():
    	conn = psycopg2.connect(
      	host='localhost', # Cambia según tu configuración
      	database="api_db",
      	user=os.environ['DB_USERNAME'],
	    	user="postgres", # Cambia según tu configuración
	    	# password=os.environ['DB_PASSWORD']
      	password="postgres" # Cambia según tu configuración
    	) 
    	return conn


Si desea salir del entorno:

	deactivate

## Actividad 2

Ejecutar los siguientes comandos:

	cd home
	flask run

Es necesario también cambiar las variables necesarias dentro de `app.py` para la conexión a la base de datos:

	def get_db_connection():
    conn = psycopg2.connect(
        host='localhost', # Cambia según tu configuración
        database="myhome",
        user="postgres",  # Cambia según tu configuración
        password="postgres",  # Cambia según tu configuración
    )
    return conn


Si desea salir del entorno:

	deactivate