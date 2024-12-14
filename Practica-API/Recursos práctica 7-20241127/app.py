import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
        	database="api_db",
        # user=os.environ['DB_USERNAME'],
		user="usuario",
		# password=os.environ['DB_PASSWORD']
        password="xxxxx")
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
      cur.execute('SELECT * FROM books ORDER BY id ASC;')
      books = cur.fetchall ()
    except Exception as e:
      print(f"Error al seleccionar los libros: {str(e)}")
      books = []
    finally:
      cur.close()
      conn.close()
    return render_template('index.html', books=books)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = int(request.form['pages_num'])
        review = request.form['review']

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO books (title, author, pages_num, review)'
                        'VALUES (%s, %s, %s, %s)',
                        (title, author, pages_num, review))
            conn.commit()
        except Exception as e:
            print(f"Error al insertar el libro: {str(e)}")
        finally:
            cur.close()
            conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/about/')
def about():
    group_members = ["Raúl Álvarez Pérez", "Sebastián André Porto Specht"]  # Añade los nombres de tu grupo aquí
    return render_template('about.html', group_members=group_members)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM books WHERE id = %s', (id,))
        conn.commit()
    except Exception as e:
        print(f"Error al borrar el libro: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = int(request.form['pages_num'])
        review = request.form['review']
        try:
            cur.execute('UPDATE books SET title = %s, author = %s, pages_num = %s, review = %s WHERE id = %s',
                        (title, author, pages_num, review, id))
            conn.commit()
        except Exception as e:
            print(f"Error al actualizar el libro: {str(e)}")
        finally:
            cur.close()
            conn.close()
        return redirect(url_for('index'))
    else:
        cur.execute('SELECT * FROM books WHERE id = %s', (id,))
        book = cur.fetchone()
        cur.close()
        conn.close()
        return render_template('update.html', book=book)