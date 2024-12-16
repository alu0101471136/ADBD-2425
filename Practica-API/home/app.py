import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host='localhost', # Cambia según tu configuración
        database="myhome",
        user="postgres",  # Cambia según tu configuración
        password="postgres",  # Cambia según tu configuración
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM temperatures ORDER BY id ASC;')
        temperatures = cur.fetchall()
    except Exception as e:
        print(f"Error al seleccionar las temperaturas: {str(e)}")
        temperatures = []
    finally:
        cur.close()
        conn.close()
    return render_template('index.html', temperatures=temperatures)

@app.route('/about/')
def about():
    group_members = ["Raúl Álvarez Pérez", "Sebastián André Porto Specht"]  # Añade los nombres de tu grupo aquí
    return render_template('about.html', group_members=group_members)

@app.route('/consultas/')
def queries():
    return render_template('queries.html')

@app.route('/consultas/temperaturas', methods=['GET'])
def temperatures():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT AVG(temperature) FROM temperatures;")
        average = cur.fetchone()
        cur.execute("SELECT MAX(temperature) FROM temperatures;")
        max_temp = cur.fetchone()
    except Exception as e:
        print(f"Error al obtener la temperatura media o la máxima: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return render_template('temperatures.html', average=average, max=max_temp)

@app.route('/consultas/habitaciones/')
def rooms():
	return render_template('rooms.html')

@app.route('/consultas/habitaciones/', methods=['GET', 'POST'])
def room_queries():
    if request.method == 'POST':
        room_id = request.form['room_id']
        if room_id is None:
            return "El parámetro room_id es necesario", 400  # Si no se proporciona room_id
        try:
            room_id = int(room_id)  # Convertir room_id a entero
        except ValueError:
            return "El parámetro room_id debe ser un número entero", 400  # Si no es un número entero
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id FROM rooms")
            ids = cur.fetchall()
            if (room_id,) not in ids:
              return "El id de la habitación no existe", 404
            name = room_name(room_id)
            average = room_average_temperature(room_id)
            min_temp = room_min_temperature(room_id)
            jsonify(min_temp)
        except Exception as e:
            print(f"Error al seleccionar las habitaciones: {str(e)}")
            return "Error al obtener los datos de las habitaciones", 500
        finally:
            cur.close()
            conn.close()

        return render_template('room_queries.html', room_id=room_id, name=name, average=average, min_temp=min_temp)
    return render_template('rooms.html')

def room_name(room_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT name FROM rooms WHERE id = %s;", (room_id,))
        name = cur.fetchone()
    except Exception as e:
        print(f"Error al obtener el nombre de la habitación: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return name

def room_average_temperature(room_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT AVG(temperature) FROM temperatures WHERE room_id = %s GROUP BY room_id;", (room_id,))
        result = cur.fetchone()
        if result:
            return result[0]  # Return the average temperature
        return None
    except Exception as e:
        print(f"Error al obtener la temperatura media de la habitación: {str(e)}")
    finally:
        cur.close()
        conn.close()

def room_min_temperature(room_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT MIN(t.temperature), r.name
            FROM temperatures t
            JOIN rooms r ON t.room_id = r.id
            WHERE t.room_id = %s
            GROUP BY r.name;
        """, (room_id,))
        row = cur.fetchone()
        min_temp = {
            'temperature': row[0],
            'room_name': row[1]
        }
    except Exception as e:
        print(f"Error al obtener la temperatura mínima de la habitación: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return min_temp
