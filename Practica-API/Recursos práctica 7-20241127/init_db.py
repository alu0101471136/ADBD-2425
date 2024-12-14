import os
import psycopg2

try:
    # Establecer la conexión con la base de datos
    conn = psycopg2.connect(
        host='localhost',
        database="api_db",
        user="usuario",
        password="xxxxx"
    )

    # Abrir un cursor para realizar operaciones en la base de datos
    cur = conn.cursor()

    # Manejo de excepciones en la creación de la tabla
    try:
        cur.execute('DROP TABLE IF EXISTS books;')
        cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
                    'title varchar (150) NOT NULL,'
                    'author varchar (50) NOT NULL,'
                    'pages_num integer NOT NULL,'
                    'review text,'
                    'date_added date DEFAULT CURRENT_TIMESTAMP);'
                    )
        print("Tabla 'books' creada exitosamente.")
    except Exception as e:
        print(f"Error al crear la tabla: {str(e)}")

    # Inserción de registros en la tabla con manejo de excepciones
    books = [
        ('A Tale of Two Cities', 'Charles Dickens', 489, 'A great classic!'),
        ('Anna Karenina', 'Leo Tolstoy', 864, 'Another great classic!'),
        ('1984', 'George Orwell', 328, 'A dystopian social science fiction novel and cautionary tale.'),
        ('To Kill a Mockingbird', 'Harper Lee', 281, 'A novel about the serious issues of rape and racial inequality.'),
        ('The Great Gatsby', 'F. Scott Fitzgerald', 180, 'A novel about the American dream and the roaring twenties.'),
        ('Moby Dick', 'Herman Melville', 635, 'A novel about the voyage of the whaling ship Pequod.'),
        ('War and Peace', 'Leo Tolstoy', 1225, 'A novel that chronicles the history of the French invasion of Russia.'),
        ('Pride and Prejudice', 'Jane Austen', 279, 'A romantic novel that charts the emotional development of the protagonist.'),
        ('The Catcher in the Rye', 'J.D. Salinger', 214, 'A novel about the events and circumstances that occur around the protagonist.'),
        ('The Hobbit', 'J.R.R. Tolkien', 310, 'A fantasy novel and children\'s book.'),
        ('Crime and Punishment', 'Fyodor Dostoevsky', 671, 'A novel about the mental anguish and moral dilemmas of an impoverished ex-student.')
    ]

    for book in books:
        try:
            cur.execute('INSERT INTO books (title, author, pages_num, review) VALUES (%s, %s, %s, %s)', book)
        except Exception as e:
            print(f"Error al insertar el libro {book[0]}: {str(e)}")

    # Confirmar los cambios en la base de datos
    conn.commit()
    print("Inserciones completadas con éxito.")

except psycopg2.Error as e:
    print(f"Error al conectar con la base de datos: {str(e)}")
finally:
    # Cerrar el cursor y la conexión si existen
    try:
        if cur:
            cur.close()
        if conn:
            conn.close()
            print("Conexión cerrada.")
    except Exception as e:
        print(f"Error al cerrar la conexión: {str(e)}")
