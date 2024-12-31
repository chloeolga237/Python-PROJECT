from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Match, Participant, Competition, User
from datetime import datetime

app = Flask(__name__)

# Database setup
engine = create_engine('sqlite:///tournament.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/add_match', methods=['POST'])
def add_match():
    data = request.json
    match = Match(
        competition_id=data['competition_id'],
        participant1_id=data['participant1_id'],
        participant2_id=data['participant2_id'],
        date=datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
    )
    session.add(match)
    session.commit()
    return jsonify({"message": "Match added successfully!"})

@app.route('/update_result', methods=['POST'])
def update_result():
    data = request.json
    match = session.query(Match).filter_by(id=data['match_id']).first()
    if not match:
        return jsonify({"error": "Match not found"}), 404

    match.result = data['result']
    if data['next_match_id']:
        next_match = session.query(Match).filter_by(id=data['next_match_id']).first()
        if data['result'] == "participant1":
            next_match.participant1_id = match.participant1_id
        elif data['result'] == "participant2":
            next_match.participant2_id = match.participant2_id

    session.commit()
    return jsonify({"message": "Result updated and bracket advanced!"})

@app.route('/get_bracket/<int:competition_id>', methods=['GET'])
def get_bracket(competition_id):
    matches = session.query(Match).filter_by(competition_id=competition_id).all()
    bracket = []
    for match in matches:
        bracket.append({
            "id": match.id,
            "participant1": match.participant1.name if match.participant1 else None,
            "participant2": match.participant2.name if match.participant2 else None,
            "date": match.date.strftime('%Y-%m-%d %H:%M:%S') if match.date else None,
            "result": match.result
        })
    return jsonify(bracket)

if __name__ == "__main__":
    app.run(debug=True)
