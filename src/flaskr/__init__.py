import os
import logging
import pandas as pd
import datetime
import html
import requests
import markdown
import folium
from folium.plugins import GroupedLayerControl
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib
import boto3
from logging.config import dictConfig

from flask import Flask, render_template


def create_app(test_config=None):
    dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    logger = logging.getLogger('werkzeug')
    logger.setLevel(logging.INFO)

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

    # matplotlib.use("agg")

    @app.route('/')
    def index():
        return render_template('index.html',
            content=repository_readme)

    @app.route('/map')
    def map():
        return render_template('map.html',
            map=m
        )

    # @app.route('/log')
    # def log():
    #     log_path = "/var/log/Flask.err.log"
    #     with open(log_path) as f:
    #         content = f.readlines()
    #     return render_template('log.html', content=content)
    
    @app.route('/api/weather')
    def api_weather():
        return api_weather_result

    # Settings
    do_predictions = True

    # On Startup
    with app.app_context():
        app.logger.info(f"server starting...")

        today = datetime.datetime.date(datetime.datetime.today() - datetime.timedelta(days=1))

        repository_readme = markdown.markdown(requests.get(
            "https://raw.githubusercontent.com/ESMEAirPollutionPrediction/.github/main/profile/README.md").text)
    
        try: metadata_emissions = pd.read_csv("data/metadata_20230717.csv")
        except: metadata_emissions = pd.read_csv("src/data/metadata_20230717.csv")
        metadata_emissions["ActivityBegin"] = pd.to_datetime(metadata_emissions["ActivityBegin"]).dt.strftime('%d-%m-%Y')
        metadata_emissions["ActivityEnd"] = pd.to_datetime(metadata_emissions["ActivityEnd"]).dt.strftime('%d-%m-%Y')

        metadata_emissions = metadata_emissions[(metadata_emissions["Latitude"].between(-10, 60)) & 
                                (metadata_emissions["Longitude"].between(-10, 60))]
        metadata_emissions = metadata_emissions[metadata_emissions["ActivityEnd"].isna()].reset_index(drop=True)

        stations_to_query = metadata_emissions[
                (metadata_emissions["Municipality"].str.lower().str.contains("paris"))
                & (metadata_emissions["Name"] != "Damparis")
                ][[
                    "Name",
                    "Municipality",
                    "Latitude",
                    "Longitude"
                ]]
        api_weather_result = {
            "stations": stations_to_query.to_json()
        }

        m = folium.Map(location=[47, 2.2137],
                        zoom_start=6,)
        
        stations_fg = folium.FeatureGroup(name="All Station Informations").add_to(m)
        for point in range(0, len(metadata_emissions)):
            folium.CircleMarker((metadata_emissions.at[point, "Latitude"], metadata_emissions.at[point, "Longitude"]), 
                                tooltip=html.escape(metadata_emissions.at[point, "Name"]), 
                                popup=folium.Popup(
                                    pd.DataFrame(metadata_emissions.loc[point][[
                                        "NatlStationCode",
                                        "Name",
                                        "Municipality",
                                        "ActivityBegin",
                                        # "ActivityEnd",
                                        "Longitude",
                                        "Latitude",
                                        "Altitude",
                                    ]]).T.to_html(
                                        classes="table table-striped table-hover table-condensed table-responsive"
                                )),
                                radius=3,# if metadata_emissions.at[point, "Name"] in (stations_to_query["Name"].unique()) else 0.01,
                                fill=True,
                                fillOpacity=0.8,
                                color="red" if metadata_emissions.at[point, "Name"] in (stations_to_query["Name"].unique()) else "blue",
                                ).add_to(stations_fg)
        
        predictions_fg_list = []
        if do_predictions:
            for polluant in ["O3", "PM10", "PM2.5", "NO", "NO2", "NOX as NO2", "SO2", "CO", "C6H6"]:
                # try: predictions_df = pd.read_csv(f"s3://esme-pollution-bucket/predictions/prediction_{polluant}_{today}.csv")
                try: 
                    predictions_df = pd.read_csv(f"data/predictions/prediction_{polluant}_{today}.csv")
                except: 
                    app.logger.error(f"couldn't find files for day {today}")
                    predictions_df = pd.read_csv(f"data/predictions/prediction_{polluant}_2024-03-12.csv")
                    today = datetime.date(2024, 3, 12)
                predictions_df = predictions_df.merge(metadata_emissions[["Latitude", "Longitude", "Name", "Municipality"]], on=["Latitude", "Longitude"], how="left")
                predictions_df["date"] = pd.to_datetime(predictions_df["date"])
                predictions_fg = folium.FeatureGroup(name=f"Predictions {polluant} {today}").add_to(m)
                predictions_fg_list += [predictions_fg]
                for point in range(0, len(metadata_emissions)):
                    if metadata_emissions.at[point, "Name"] in (predictions_df["Name"].unique()): # and metadata_emissions.at[point, "Name"] == "Bld peripherique Est":
                        popup_html = pd.DataFrame(metadata_emissions.loc[point][[
                            "NatlStationCode",
                            "Name",
                            "Municipality",
                            "ActivityBegin",
                            # "ActivityEnd",
                            "Longitude",
                            "Latitude",
                            "Altitude",
                        ]]).T.to_html(
                            classes="table table-striped table-hover table-condensed table-responsive"
                        )
                        predictions_df[predictions_df["Name"] == metadata_emissions.at[point, "Name"]].plot(
                            x="date",
                            y="valeur brute",
                            figsize=(10, 5)
                        )
                        plt.title(f"{polluant} forecasts at Station {metadata_emissions.at[point, 'Name']}")
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        tmpfile = BytesIO()
                        plt.savefig(tmpfile, format="png")
                        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
                        popup_html += f"<img src='data:image/png;base64,{encoded}'>"
                        popup_iframe = folium.IFrame(popup_html, width="500", height="auto")
                        folium.CircleMarker((metadata_emissions.at[point, "Latitude"], metadata_emissions.at[point, "Longitude"]), 
                                            tooltip=html.escape(metadata_emissions.at[point, "Name"]), 
                                            popup=folium.Popup(popup_html),
                                            radius=3,
                                            fill=True,
                                            fillOpacity=0.8,
                                            color="red",
                                            ).add_to(predictions_fg)
                    plt.close()

        folium.LayerControl(collapsed=True).add_to(m)
        GroupedLayerControl(
            groups={"Select your data :": [stations_fg] + predictions_fg_list},
            collapsed=False
        ).add_to(m)
        m.get_root().width = "80%"
        m = m.get_root()._repr_html_()

        app.logger.info(f"server ready")
    return app
    
# To test it locally :
# flask --app src/flaskr run --debug