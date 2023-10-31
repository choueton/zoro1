# Importation de Flask et d'autres dépendances
from flask import Flask, render_template, request, redirect, url_for
import pyodbc

# Création d'une instance de l'application Flask
app = Flask(__name__)

# Configuration de la connexion à SQL Server
app.config['SQL_SERVER_CONNECTION_STRING'] = """
    Driver={SQL Server};
    Server=DESKTOP-JK6D8G9\\SQLEXPRESS;
    Database=zoro;
    Trusted_Connection=yes;"""



# Définition d'une route '/client'
@app.route('/client')
def client():
    # Cette fonction est exécutée lorsque l'URL '/client' est consultée.
    # Établissement d'une connexion à la base de données SQL Server en utilisant la chaîne de connexion
    connection = pyodbc.connect(app.config['SQL_SERVER_CONNECTION_STRING'])
    # Création d'un curseur pour exécuter des requêtes SQL
    cursor = connection.cursor()
    # Exécution d'une requête SQL qui sélectionne toutes les lignes de la table 'client'
    cursor.execute("SELECT * FROM client")
    # Récupération de tous les résultats de la requête dans une liste
    result = cursor.fetchall()
    # Fermeture du curseur et de la connexion à la base de données
    cursor.close()
    connection.close()
    # Renvoi d'une page HTML ('client.html') en passant les résultats de la requête en tant que variable 'result'
    return render_template('client.html', result=result)


# Définition d'une route '/add_client' qui gère les méthodes GET et POST
@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    # Cette partie du code s'exécute lorsque le formulaire est soumis via la méthode POST.
    if request.method == 'POST':
        
        # Récupération des informations du formulaire
        Nomclient = request.form.get('Nomclient')  # Obtient la valeur du champ 'Nomclient' dans le formulaire
        adresseClient = request.form.get('AdresseClient')  # Obtient la valeur du champ 'AdresseClient' dans le formulaire
        telephone = request.form.get('telephone')  # Obtient la valeur du champ 'telephone' dans le formulaire

        # Établissement d'une connexion à la base de données SQL Server en utilisant la chaîne de connexion
        connection = pyodbc.connect(app.config['SQL_SERVER_CONNECTION_STRING'])
        # Création d'un curseur pour exécuter des requêtes SQL
        cursor = connection.cursor()
        # Exécution d'une requête SQL pour insérer les données du client dans la table 'client'
        cursor.execute("INSERT INTO client (Nomclient, AdresseClient, telephone) VALUES (?, ?, ?)", (Nomclient, adresseClient, telephone))
        # Validation de la transaction en enregistrant les modifications dans la base de données
        connection.commit()
        # Fermeture du curseur et de la connexion à la base de données
        cursor.close()
        connection.close()

        # Redirection vers la page 'client' après l'ajout du client dans la base de données
        return redirect(url_for('client'))

    # Si la méthode HTTP est GET, cela signifie qu'il s'agit d'une première visite à la page.
    # Dans ce cas, on renvoie le modèle HTML 'add_client.html' pour afficher le formulaire.
    return render_template('add_client.html')


# Définition d'une route '/upd_client/<int:id>' qui gère les méthodes GET et POST
@app.route('/upd_client/<int:id>', methods=["GET", "POST"])
def upd_client(id):
    # Cette fonction est exécutée lorsque l'URL '/upd_client/id' est consultée, où 'id' est un entier passé en tant que paramètre.
    connection = pyodbc.connect(app.config['SQL_SERVER_CONNECTION_STRING'])
    cursor = connection.cursor()
    # Exécution d'une requête SQL SELECT pour récupérer les informations du client spécifié par son ID
    cursor.execute("SELECT * FROM client WHERE CodeClient=?", (id,))
    client = cursor.fetchone()  # Utilisez fetchone() pour obtenir une seule ligne correspondant à l'ID spécifié
    cursor.close()
    connection.close()

    if request.method == "POST":
        Nomclient = request.form['Nomclient']
        AdresseClient = request.form['AdresseClient']
        telephone = request.form['telephone']

        connection = pyodbc.connect(app.config['SQL_SERVER_CONNECTION_STRING'])
        cursor = connection.cursor()
        # Exécution d'une requête SQL pour modifier les données du client dans la table 'client'
        cursor.execute("UPDATE client SET Nomclient=?, AdresseClient=?, telephone=? WHERE CodeClient=?", (Nomclient, AdresseClient, telephone, id))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('client'))

    return render_template('upd_client.html', client=client)


@app.route('/delete_client/<int:id>', methods=['GET'])
def delete_client(id):
    connection = pyodbc.connect(app.config['SQL_SERVER_CONNECTION_STRING'])
    cursor = connection.cursor()
    
    # Utilisez le nom de colonne correct dans la requête DELETE
    cursor.execute("DELETE FROM client WHERE CodeClient = ?", id)
    
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('client'))



# L'application Flask doit être exécutée pour que cette route soit accessible.
if __name__ == '__main__':
    app.run(debug=True)