from app import app, db, Exercise

if __name__=="__main__":
    with app.app_context():
        db.create_all()

        # exercise1 = Exercise(name="Push-up", description="An upper body exercise", difficulty=2, progress=0)
        # exercise2 = Exercise(name="Squat", description="A lower body exercise", difficulty=2, progress=0)
        # exercise3 = Exercise(name="Plank", description="A core exercise", difficulty=3, progress=0)
        # exercise4 = Exercise(name="Jumping Jacks", description="A full body exercise", difficulty=1, progress=0)
        # exercise5 = Exercise(name="Burpees", description="A full body exercise", difficulty=3, progress=0)

        # db.session.add(exercise1)
        # db.session.add(exercise2)
        # db.session.add(exercise3)
        # db.session.add(exercise4)
        # db.session.add(exercise5)

        # db.session.commit()

