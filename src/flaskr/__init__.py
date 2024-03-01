import os
import logging
import folium
import pandas as pd
from datetime import datetime
import html

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
        return render_template('map.html',
            map=m.get_root()._repr_html_())

    @app.route('/log')
    def log():
        log_path = "/var/log/Flask.err.log"
        with open(log_path) as f:
            content = f.readlines()
        return render_template('log.html', content=content)
    
    @app.route('/test')
    def test():
        return render_template('test.html')

    # On Startup
    with app.app_context():
        print(datetime.now())
    
        metadata_emissions = pd.read_csv("src/data/metadata_20230717.csv")
        maps = []
        m = folium.Map(location=[47, 2.2137],
                        zoom_start=6,)

        stations_fg = folium.FeatureGroup(name="Stations").add_to(m)
        for point in range(0, len(metadata_emissions)):
            folium.CircleMarker((metadata_emissions.at[point, "Latitude"], metadata_emissions.at[point, "Longitude"]), 
                                tooltip=html.escape(metadata_emissions.at[point, "Name"]), 
                                radius=1.5,
                                color="red",).add_to(stations_fg)
        folium.LayerControl().add_to(m)
        m.get_root().width = "75%"

    return app