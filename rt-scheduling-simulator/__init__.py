from flask import Flask

UPLOAD_FOLDER = '/rt-scheduling-simulator/sim_setup_files'
ALLOWED_EXTENSIONS = {'json'}

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_FOLDER=UPLOAD_FOLDER,
        ALLOWED_EXTENSIONS=ALLOWED_EXTENSIONS,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import home
    app.register_blueprint(home.bp)

    from . import sim
    app.register_blueprint(sim.bp)

    return app