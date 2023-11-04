# Importation de Flask et d'autres dépendances
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyodbc
from werkzeug.security import generate_password_hash, check_password_hash

# Création d'une instance de l'application Flask
app = Flask(__name__)

app.secret_key = 'votre_clé_secrète'
# Configuration de la connexion à SQL Server
app.config['SQL_SERVER_CONNECTION_STRING'] = """
    Driver={SQL Server};
    Server=DESKTOP-JK6D8G9\\SQLEXPRESS;
    Database=zoro;
    Trusted_Connection=yes;"""





@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        mail = request.form['mail']
        nom = request.form['nom']
        prenom = request.form['prenom']
        password = request.form['password']

        # Hacher le mot de passe
        hashed_password = generate_password_hash(password)

        connection = pyodbc.connect(app.config['SQL_SERVER_CONNECTION_STRING'])
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (mail, Nom, prenom, password) VALUES (?, ?, ?, ?)", (mail, nom, prenom, hashed_password))
        connection.commit()
        session['user'] = mail
        flash('Inscription réussie et connexion automatique !')
        cursor.close()
        connection.close()
        
        return redirect(url_for('index'))
    
    return render_template('./auth/register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']


        connection = pyodbc.connect(app.config['SQL_SERVER_CONNECTION_STRING'])
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE mail = ?", (mail,))
        user = cursor.fetchone()

        if user and check_password_hash(user.password, password):  # Accès au mot de passe directement par le nom de colonne
            session['user'] = user.mail
            flash('Connexion réussie !')
            return redirect(url_for('index'))
        else:
            flash('Mauvaise adresse e-mail ou mot de passe.')

    return render_template('./auth/login.html')


# Définition d'une route '/index'
@app.route('/')
def index():
    return render_template('index.html')

# Définition d'une route '/Produit'
@app.route('/Produit')
def Produit():
    # Cette fonction est exécutée lorsque l'URL '/Produit' est consultée.
    # Établissement d'une connexion à la base de données SQL Server en utilisant la chaîne de connexion
    connection = pyodbc.connect(app.config['SQL_SERVER_CONNECTION_STRING'])
    # Création d'un curseur pour exécuter des requêtes SQL
    cursor = connection.cursor()
    # Exécution d'une requête SQL qui sélectionne toutes les lignes de la table 'Produit'
    cursor.execute("SELECT * FROM Produit")
    # Récupération de tous les résultats de la requête dans une liste
    result = cursor.fetchall()
    # Fermeture du curseur et de la connexion à la base de données
    cursor.close()
    connection.close()
    # Renvoi d'une page HTML ('Produit.html') en passant les résultats de la requête en tant que variable 'result'
    return render_template('Produit.html', result=result)


# Définition d'une route '/add_Produit' qui gère les méthodes GET et POST
@app.route('/add_Produit', methods=['GET', 'POST'])
def add_Produit():
    # Cette partie du code s'exécute lorsque le formulaire est soumis via la méthode POST.
    if request.method == 'POST':
        
        # Récupération des informations du formulaire
        Nom = request.form.get('Nom')  # Obtient la valeur du champ 'Nom' dans le formulaire
        Description = request.form.get('Description')  # Obtient la valeur du champ 'Description' dans le formulaire
        PrixUnitaire = request.form.get('PrixUnitaire')  # Obtient la valeur du champ 'PrixUnitaire' dans le formulaire

        # Établissement d'une connexion à la base de données SQL Server en utilisant la chaîne de connexion
        connection = pyodbc.connect(app.config['SQL_SERVER_CONNECTION_STRING'])
        # Création d'un curseur pour exécuter des requêtes SQL
        cursor = connection.cursor()
        # Exécution d'une requête SQL pour insérer les données du Produit dans la table 'Produit'
        cursor.execute("INSERT INTO Produit (Nom, Description, PrixUnitaire) VALUES (?, ?, ?)", (Nom, Description, PrixUnitaire))
        # Validation de la transaction en enregistrant les modifications dans la base de données
        connection.commit()
        # Fermeture du curseur et de la connexion à la base de données
        cursor.close()
        connection.close()

        # Redirection vers la page 'Produit' après l'ajout du Produit dans la base de données
        return redirect(url_for('Produit'))

    # Si la méthode HTTP est GET, cela signifie qu'il s'agit d'une première visite à la page.
    # Dans ce cas, on renvoie le modèle HTML 'add_Produit.html' pour afficher le formulaire.
    return render_template('add_Produit.html')


# Définition d'une route '/upd_Produit/<int:id>' qui gère les méthodes GET et POST
@app.route('/upd_Produit/<int:id>', methods=["GET", "POST"])
def upd_Produit(id):
    # Cette fonction est exécutée lorsque l'URL '/upd_Produit/id' est consultée, où 'id' est un entier passé en tant que paramètre.
    connection = pyodbc.connect(app.config['SQL_SERVER_CONNECTION_STRING'])
    cursor = connection.cursor()
    # Exécution d'une requête SQL SELECT pour récupérer les informations du Produit spécifié par son ID
    cursor.execute("SELECT * FROM Produit WHERE id_produit=?", (id,))
    Produit = cursor.fetchone()  # Utilisez fetchone() pour obtenir une seule ligne correspondant à l'ID spécifié
    cursor.close()
    connection.close()

    if request.method == "POST":
        Nom = request.form['Nom']
        Description = request.form['Description']
        PrixUnitaire = request.form['PrixUnitaire']

        connection = pyodbc.connect(app.config['SQL_SERVER_CONNECTION_STRING'])
        cursor = connection.cursor()
        # Exécution d'une requête SQL pour modifier les données du Produit dans la table 'Produit'
        cursor.execute("UPDATE Produit SET Nom=?, Description=?, PrixUnitaire=? WHERE id_produit=?", (Nom, Description, PrixUnitaire, id))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('Produit'))

    return render_template('upd_Produit.html', Produit=Produit)


@app.route('/delete_Produit/<int:id>', methods=['GET'])
def delete_Produit(id):
    connection = pyodbc.connect(app.config['SQL_SERVER_CONNECTION_STRING'])
    cursor = connection.cursor()
    
    # Utilisez le nom de colonne correct dans la requête DELETE
    cursor.execute("DELETE FROM Produit WHERE id_produit = ?", id)
    
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('Produit'))



###########################################################################################################################################

@app.route('/magasin')
def magasin():
    return render_template('magasin.html')


# L'application Flask doit être exécutée pour que cette route soit accessible.
if __name__ == '__main__':
    app.run(debug=True)