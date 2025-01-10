from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'  # Nécessaire pour utiliser les sessions

# Informations d'authentification
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# Liste pour stocker les tournois
tournois = []

@app.route('/')
def index():
    return render_template('index.html', tournois=tournois)

@app.route('/statistiques')  # Route pour accéder à statistiques.html
def statistiques():
    return render_template('statistiques.html')  # Assurez-vous d'avoir ce fichier

@app.route('/classement')  # Route pour accéder à classement.html
def classement():
    return render_template('classement.html', tournois=tournois)  # Passez les tournois à classement

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True  # Marquer l'utilisateur comme connecté
            return redirect(url_for('create_tournament'))  # Rediriger vers la page de création de tournoi
        else:
            return "Nom d'utilisateur ou mot de passe incorrect", 401
    return render_template('login.html')  # Affichage du formulaire de connexion pour GET

@app.route('/create_tournament', methods=['GET', 'POST'])
def create_tournament():
    if 'logged_in' in session:
        if request.method == 'POST':
            tournament_name = request.form['tournament_name']
            team_count = int(request.form['team_count'])
            team_names = [name.strip() for name in request.form['team_names'].split(',')]  # Nettoyer les noms
            scores = ['0'] * team_count  # Initialiser les scores à 0

            # Ajouter le tournoi à la liste
            tournois.append({
                'nom': tournament_name,
                'nombre_equipes': team_count,
                'noms_equipes': team_names,
                'scores': scores,
                'jeux': []  # Initialiser la liste des jeux
            })

            # Rediriger vers la page de planification avec les données du tournoi
            return redirect(url_for('schedule_match', tournament_index=len(tournois)-1))
        
        return render_template('create_tournament.html')  # Affiche le formulaire
    else:
        return redirect(url_for('index'))  # Rediriger vers la page d'accueil si non connecté

@app.route('/schedule_match/<int:tournament_index>', methods=['GET', 'POST'])
def schedule_match(tournament_index):
    if 'logged_in' in session:
        if request.method == 'POST':
            # Log of received data
            print(request.form)  # Log des données reçues

            team1_index = request.form.get('team1_index')
            team2_index = request.form.get('team2_index')
            score1 = request.form.get('score1')
            score2 = request.form.get('score2')
            game_date = request.form.get('game_date')

            # Vérifier que toutes les données nécessaires sont présentes
            if team1_index is None or team2_index is None or score1 is None or score2 is None or game_date is None:
                return "Certaines données sont manquantes", 400

            # Convertir les indices en entiers
            team1_index = int(team1_index)
            team2_index = int(team2_index)

            # Enregistrer les informations du match
            tournois[tournament_index]['jeux'].append({
                'team1': tournois[tournament_index]['noms_equipes'][team1_index],
                'team2': tournois[tournament_index]['noms_equipes'][team2_index],
                'score1': score1,
                'score2': score2,
                'date': game_date
            })

            return redirect(url_for('index'))  # Rediriger vers la page d'accueil

        # Si la méthode est GET, renvoyer le formulaire de planification
        tournament = tournois[tournament_index]  # Récupérer le tournoi correspondant
        return render_template('schedule_match.html', tournament=tournament, tournament_index=tournament_index)  # Passer le tournoi et l'index au template
    else:
        return redirect(url_for('login'))  # Redirige vers la page de connexion si l'utilisateur n'est pas connecté

@app.route('/signup', methods=['POST'])
def signup():
    fullname = request.form['fullname']
    email = request.form['email']
    new_password = request.form['new_password']
    
    # Logique pour créer un nouveau compte (sauvegarde dans la base de données)
    # ...

    # Rediriger vers la page d'accueil avec un message de succès
    return '''
        <script>
            alert("Compte créé avec succès !");
            window.location.href = "/";
        </script>
    '''

@app.route('/modify_tournament/<int:tournament_index>', methods=['GET', 'POST'])
def modify_tournament(tournament_index):
    if 'logged_in' in session:
        if request.method == 'POST':
            tournois[tournament_index]['nom'] = request.form['tournament_name']
            tournois[tournament_index]['nombre_equipes'] = int(request.form['team_count'])
            tournois[tournament_index]['noms_equipes'] = [name.strip() for name in request.form['team_names'].split(',')]
            tournois[tournament_index]['scores'] = request.form['scores'].split(',')
            return redirect(url_for('classement'))  # Rediriger vers le classement après modification
            
        tournament = tournois[tournament_index]  # Récupérer le tournoi à modifier
        return render_template('modify_tournament.html', tournament=tournament, index=tournament_index)
    else:
        return redirect(url_for('index'))

@app.route('/delete_tournament/<int:tournament_index>')
def delete_tournament(tournament_index):
    if 'logged_in' in session:
        if 0 <= tournament_index < len(tournois):
            del tournois[tournament_index]
        return redirect(url_for('classement'))  # Rediriger vers le classement après suppression
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Déconnecter l'utilisateur
    return redirect(url_for('index'))  # Rediriger vers la page d'accueil

if __name__ == '__main__':
    app.run(debug=True)  # Démarre l'application en mode debug