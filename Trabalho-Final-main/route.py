from bottle import Bottle, request, response, redirect, template, run
import sqlite3

app = Bottle()
conn = sqlite3.connect('marketplace.db')
cursor = conn.cursor()

# Criando tabelas
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, price REAL, category TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY, user_id INTEGER, book_id INTEGER)''')
conn.commit()

sessions = {}

@app.route('/')
def homepage():
    return template("""
    <h1>Bem-vindo ao Marketplace de Livros!</h1>
    <a href='/books'>Ver Livros</a> | <a href='/portal'>Login</a>
    """)

@app.route('/books')
def list_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return template("""
    <h2>Livros disponíveis:</h2>
    <ul>
        % for book in books:
            <li>{{book[1]}} - {{book[2]}} - R${{book[3]}} - Categoria: {{book[4]}} <a href='/add_to_cart/{{book[0]}}'>Adicionar ao Carrinho</a></li>
        % end
    </ul>
    <a href='/add_book'>Adicionar Livro</a>
    """, books=books)

@app.route('/add_book', method=['GET', 'POST'])
def add_book():
    session_id = request.get_cookie('session_id')
    if session_id not in sessions:
        return redirect('/portal')
    
    if request.method == 'POST':
        title = request.forms.get('title')
        author = request.forms.get('author')
        price = request.forms.get('price')
        category = request.forms.get('category')
        cursor.execute("INSERT INTO books (title, author, price, category) VALUES (?, ?, ?, ?)", (title, author, price, category))
        conn.commit()
        return redirect('/books')
    
    return template("""
    <h2>Adicionar Livro</h2>
    <form method='post'>
        Título: <input name='title'><br>
        Autor: <input name='author'><br>
        Preço: <input name='price'><br>
        Categoria: <input name='category'><br>
        <input type='submit' value='Adicionar'>
    </form>
    """)

@app.route('/add_to_cart/<book_id>')
def add_to_cart(book_id):
    session_id = request.get_cookie('session_id')
    if session_id not in sessions:
        return redirect('/portal')
    user_id = sessions[session_id]
    cursor.execute("INSERT INTO cart (user_id, book_id) VALUES (?, ?)", (user_id, book_id))
    conn.commit()
    return redirect('/cart')

@app.route('/cart')
def view_cart():
    session_id = request.get_cookie('session_id')
    if session_id not in sessions:
        return redirect('/portal')
    user_id = sessions[session_id]
    cursor.execute("SELECT books.id, books.title, books.author, books.price FROM books JOIN cart ON books.id = cart.book_id WHERE cart.user_id = ?", (user_id,))
    cart_items = cursor.fetchall()
    return template("""
    <h2>Seu Carrinho:</h2>
    <ul>
        % for item in cart_items:
            <li>{{item[1]}} - {{item[2]}} - R${{item[3]}}</li>
        % end
    </ul>
    <a href='/books'>Continuar Comprando</a>
    """, cart_items=cart_items)

@app.route('/portal', method=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')
        cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            session_id = username + "_session"
            sessions[session_id] = user[0]
            response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
            return redirect('/books')
    return template("""
    <h2>Login</h2>
    <form method='post'>
        Usuário: <input name='username'><br>
        Senha: <input name='password' type='password'><br>
        <input type='submit' value='Login'>
    </form>
    """)

@app.route('/logout')
def logout():
    response.delete_cookie('session_id')
    return redirect('/')

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)

