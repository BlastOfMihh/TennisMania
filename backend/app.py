from backhand import create_app
# run_tests()

testing=True

if __name__=="__main__":
    app, socketio=create_app()
    # if testing:
    #     from test_service_founder import run
    #     run()
        # unittest.main()
    socketio.run(app=app, debug=True, allow_unsafe_werkzeug=True, host='0.0.0.0')
    # socketio.run(app=app, allow_unsafe_werkzeug=True, host='0.0.0.0')
    # app.run(debug=True)
