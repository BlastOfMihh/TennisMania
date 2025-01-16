from app import app, db, Exercise

if __name__=="__main__":
    with app.app_context():
        db.create_all()

       # book1 = Book(title="The Divine Comedy", author="Dante Alighieri", state="Read", description="d1", rating=4)
       # book2 = Book(title="The Dreaming Tree", author="C. J. Cherryh", state="Currently Reading", description='d2')
       # book3 = Book(title="Moby Dick", author="Herman Melville", state="Want To Read")
       # book4 = Book(title="Martin Eden", author="Jack London", state="Read", description="d4", rating=5)
       # book5 = Book(title="The Name of the Wind", author="Patrick Rothfuss", state="Read", description="d5", rating=5)
#
#        db.session.add(book1)
#        db.session.add(book2)
#        db.session.add(book3)
#        db.session.add(book4)
#        db.session.add(book5)

        exercise1 = Exercise(name="Push-up", description="An upper body exercise", difficulty=2, progress=0)
        exercise2 = Exercise(name="Squat", description="A lower body exercise", difficulty=2, progress=0)
        exercise3 = Exercise(name="Plank", description="A core exercise", difficulty=3, progress=0)
        exercise4 = Exercise(name="Jumping Jacks", description="A full body exercise", difficulty=1, progress=0)
        exercise5 = Exercise(name="Burpees", description="A full body exercise", difficulty=3, progress=0)

        db.session.add(exercise1)
        db.session.add(exercise2)
        db.session.add(exercise3)
        db.session.add(exercise4)
        db.session.add(exercise5)

        db.session.commit()

