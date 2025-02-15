from bottle import Bottle, request, response, template, redirect, run, static_file

app = Bottle()
books = []  # Lista de livros
users = {"admin": "1234"}  # Usuário de exemplo
sessions = {}

@app.route('/static/<filename>')
def serve_static(filename):
    return static_file(filename, root='./static')

@app.route('/')
def homepage():
    return template('index', books=books)  # Renderiza a página inicial

@app.route('/books')
def list_books():
    return template('books', books=books)

@app.route('/add_book', method=['GET', 'POST'])
def add_book():
    session_id = request.get_cookie('session_id')
    if session_id not in sessions:
        return redirect('/login')
    
    if request.method == 'POST':
        title = request.forms.get('title')
        author = request.forms.get('author')
        price = request.forms.get('price')
        books.append({'title': title, 'author': author, 'price': price})
        return redirect('/books')
    
    return template('add_book')

@app.route('/edit_book/<index>', method=['GET', 'POST'])
def edit_book(index):
    session_id = request.get_cookie('session_id')
    if session_id not in sessions:
        return redirect('/login')
    
    index = int(index)
    if index < 0 or index >= len(books):
        return redirect('/books')
    
    if request.method == 'POST':
        books[index]['title'] = request.forms.get('title')
        books[index]['author'] = request.forms.get('author')
        books[index]['price'] = request.forms.get('price')
        return redirect('/books')
    
    return template('edit_book', book=books[index], index=index)

@app.route('/login', method=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')
        if username in users and users[username] == password:
            session_id = username + "_session"
            sessions[session_id] = username
            response.set_cookie('session_id', session_id, httponly=True, max_age=3600)
            return redirect('/books')
    return template('login')

@app.route('/logout')
def logout():
    response.delete_cookie('session_id')
    return redirect('/')

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
