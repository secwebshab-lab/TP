from flask import Flask, request, render_template_string, session, redirect, url_for
import pymysql

app = Flask(__name__)
app.secret_key = "super_secret_session_key" 

DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "P@ssw0rd_Admin!" # À modifier selon votre environnement local
DB_NAME = "ecommerce_demo"

def get_db_connection():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME, cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def index():
    return '''
        <h1>Bienvenue sur notre E-commerce</h1>
        <a href="/login">Se connecter</a> | <a href="/register">Créer un compte</a> | <a href="/shop">Boutique</a>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        # Insertion basique sans validation d'email
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return redirect(url_for('login'))
        
    return '''
        <h2>Inscription</h2>
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="S'inscrire">
        </form>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('shop'))
        return "Identifiants invalides."
        
    return '''
        <h2>Connexion</h2>
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Se connecter">
        </form>
    '''

@app.route('/shop')
def shop():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()
    
    search_query = request.args.get('search', '')
    
    html = f"<h2>Boutique</h2><p>Connecté en tant que: {session['username']}</p>"
    if search_query:
        html += f"<p>Résultats de recherche pour : <b>{search_query}</b></p>"
        
    for article in articles:
        html += f"<li>{article['name']} - {article['price']}€ <a href='/order/{article['id']}'>Commander</a></li>"
        
    html += f"<br><a href='/my_orders/{session['user_id']}'>Voir mes commandes</a>"
    return render_template_string(html)

@app.route('/order/<int:article_id>')
def order(article_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM articles WHERE id = %s", (article_id,))
    article = cursor.fetchone()
    
    if article:
        cursor.execute("INSERT INTO orders (user_id, article_name) VALUES (%s, %s)", (session['user_id'], article['name']))
        conn.commit()
        return redirect(url_for('shop'))

@app.route('/my_orders/<int:user_id>')
def my_orders(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # Faille : Nous devrions vérifier si session['user_id'] == user_id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
    orders = cursor.fetchall()
    
    html = f"<h2>Commandes de l'utilisateur {user_id}</h2>"
    for order in orders:
        html += f"<li>{order['article_name']}</li>"
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
