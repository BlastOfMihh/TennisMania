from backhand import create_app

if __name__=="__main__":
    app, socketio, db = create_app()
    with app.app_context():
        db.create_all()
        db.session.commit()