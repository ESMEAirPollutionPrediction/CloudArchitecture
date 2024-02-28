import os
import logging
import folium

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    log = logging.getLogger('werkzeug')
    # log.setLevel(logging.ERROR)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/map')
    def map():
        m = folium.Map(location=[47, 2.2137],
                       zoom_start=6,
                       width=800,
                       height=600,)
        m.get_root().render()
        header = m.get_root().header.render()
        body_html = m.get_root().html.render()
        script = m.get_root().script.render()

        return render_template('map.html',
            header=header,
            body_html=body_html,
            script=script,)

    @app.route('/log')
    def log():
        log_path = "/var/log/Flask.err.log"
        with open(log_path) as f:
            content = f.readlines()
        return render_template('log.html', content=content)
    
    @app.route('/test')
    def test():
        return render_template('test.html')

    return app