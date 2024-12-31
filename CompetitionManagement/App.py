from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User, Competition, Participant, Match

# Setup the database connection
engine = create_engine('sqlite:///tournament.db')
Session = sessionmaker(bind=engine)
session = Session()

def add_user():
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    user = User(username=username, email=email, password=password)
    session.add(user)
    session.commit()
    print("User added successfully!")

def add_competition():
    name = input("Enter competition name: ")
    created_by = int(input("Enter user ID of creator: "))
    competition = Competition(name=name, created_by=created_by)
    session.add(competition)
    session.commit()
    print("Competition added successfully!")

def view_users():
    users = session.query(User).all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")

def view_competitions():
    competitions = session.query(Competition).all()
    for comp in competitions:
        print(f"ID: {comp.id}, Name: {comp.name}, Created By: {comp.created_by}")

def main():
    while True:
        print("\n1. Add User")
        print("2. Add Competition")
        print("3. View Users")
        print("4. View Competitions")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_user()
        elif choice == '2':
            add_competition()
        elif choice == '3':
            view_users()
        elif choice == '4':
            view_competitions()
        elif choice == '5':
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
