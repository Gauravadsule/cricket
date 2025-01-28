from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cricket.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models for Teams, Players, and Matches
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    players = db.relationship('Player', backref='team', lazy=True)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    date = db.Column(db.String(50), nullable=False)

db.create_all()

@app.route('/teams', methods=['GET', 'POST'])
def manage_teams():
    if request.method == 'GET':
        teams = Team.query.all()
        return jsonify([team.name for team in teams])
    elif request.method == 'POST':
        data = request.json
        new_team = Team(name=data['name'])
        db.session.add(new_team)
        db.session.commit()
        return jsonify({"message": "Team added successfully!"}), 201

@app.route('/players', methods=['GET', 'POST'])
def manage_players():
    if request.method == 'GET':
        players = Player.query.all()
        return jsonify([{'name': player.name, 'team': player.team.name} for player in players])
    elif request.method == 'POST':
        data = request.json
        team = Team.query.filter_by(name=data['team']).first()
        if not team:
            return jsonify({"message": "Team not found"}), 404
        new_player = Player(name=data['name'], team_id=team.id)
        db.session.add(new_player)
        db.session.commit()
        return jsonify({"message": "Player added successfully!"}), 201

@app.route('/matches', methods=['GET', 'POST'])
def manage_matches():
    if request.method == 'GET':
        matches = Match.query.all()
        return jsonify([{'team1': match.team1.name, 'team2': match.team2.name, 'date': match.date} for match in matches])
    elif request.method == 'POST':
        data = request.json
        team1 = Team.query.filter_by(name=data['team1']).first()
        team2 = Team.query.filter_by(name=data['team2']).first()
        if not team1 or not team2:
            return jsonify({"message": "One or both teams not found"}), 404
        new_match = Match(team1_id=team1.id, team2_id=team2.id, date=data['date'])
        db.session.add(new_match)
        db.session.commit()
        return jsonify({"message": "Match added successfully!"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)