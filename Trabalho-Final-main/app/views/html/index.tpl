<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Marketplace de Livros</title>
    <link rel="stylesheet" href="/static/pagina.css">
    <link rel="stylesheet" href="/static/helper.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
</head>
<body>
    <header class="object_centered">
        <div class="logo">
            <h1>Marketplace de Livros</h1>
        </div>
        <nav>
            <ul>
                <li><a href="/">Início</a></li>
                <li><a href="/books">Livros</a></li>
                <li><a href="/portal">Login</a></li>
                <li><a href="/cart">Carrinho</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <section id="banner" class="object_centered">
            <h2>Descubra os melhores livros para você!</h2>
        </section>
        <section id="books-list" class="object_centered">
            <h2>Livros Disponíveis</h2>
            <div id="book-container" class="book-grid">
                % for book in books:
                    <p>{{ book.title }} - {{ book.author }} - R${{ book.price }}</p>
                % end
            </div>
            
            <button id="add-book-btn" onclick="window.location.href='/add_book'">Adicionar Livro</button>
        </section>
    </main>
    <footer class="object_centered">
        <p>&copy; 2025 Marketplace de Livros. Todos os direitos reservados.</p>
    </footer>
    <script>
        async function fetchBooks() {
            try {
                const response = await fetch('/books');
                if (!response.ok) throw new Error('Erro ao carregar os livros');
                const text = await response.text();
                document.getElementById('book-container').innerHTML = text;
            } catch (error) {
                document.getElementById('book-container').innerHTML = '<p>Erro ao carregar os livros. Tente novamente mais tarde.</p>';
            }
        }
        fetchBooks();
    </script>
</body>
</html>