"""
Python Extract Transform Load

EPA Dataset on Urban Waste Water Treatment Plants

"""

import requests
import pandas as pd
from sqlalchemy import create_engine

def extract()-> dict:
    """ This API extracts data from
    http://gis.epa.ie
    """
    API_URL = "http://gis.epa.ie/geoserver/EPA/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=EPA:LEMA_Facilities_UWW&maxFeatures=50&outputFormat=application%2Fjson&srsName=EPSG:4326"
    data = requests.get(API_URL).json()
    return data

def transform(data: dict) -> pd.DataFrame:
    features = data["features"]
    rows = []
    for feature in features:
        properties = feature["properties"]
        row = {
            "Name": properties["Name"],
            "County": properties["County"],
            "LocalAuthority": properties["LocalAuthority"],
            "AgglomerationPE": properties["AgglomerationPE"],
            "TreatmentType": properties["TreatmentType"],
            "LicenceStatusType": properties["LicenceStatusType"],
            "CIStatus": properties["CIStatus"]
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    return df


def load(df:pd.DataFrame)-> None:
    """ Loads data into a mysql database"""
    # Replace password with your password and govdata with your database
    # Replace root with user and localhost with hostname and port
    disk_engine = create_engine('mysql://root:password@localhost:3306/govdata') 
    df.to_sql('urban_waste_water', disk_engine, if_exists='replace')

data = extract()
df = transform(data)
load(df)