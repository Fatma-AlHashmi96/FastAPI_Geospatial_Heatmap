from fastapi import FastAPI, Body, APIRouter, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.responses import RedirectResponse
from pydantic import BaseModel, validator
import numpy as np
from datetime import date
from typing import Optional
import geopy
#Using for passing open statment data by passing some name and address
from geopy.geocoders import Nominatim 

# Instance to implement fat api web application
app=FastAPI()

app = FastAPI()
router = APIRouter(
    prefix="/create",
    tags=["create"],
    responses={404: {"description": "Not found"}}
)


templates = Jinja2Templates(directory="templates")

geolocator= Nominatim(user_agent='app') # Establish connection to the location 

   
geospatial_parameters = [{"Date": date.today(), "Site_ID":1,"Site_Name": "Oman", "Tempreture": 50, "Pressure": 140, "Steam_Injection":11},
                   {"Date": date.today(), "Site_ID":1,"Site_Name": "India", "Tempreture": 40, "Pressure": 230, "Steam_Injection":19}]  
async def creating_parameters():

# Specify the Latitude and Longitude of the site
    for loc in geospatial_parameters:
        location=geolocator.geocode(loc["Site_Name"])
        if loc["Site_Name"] is None:
            latitude=np.nan
            longitude=np.nan
        else:
            loc["Latitude"]=location.latitude
            loc["Longitude"]=location.longitude

    return geospatial_parameters


@app.get('/temp_press_steam')
async def reading_geo_parameters():
    read_API_Data= await creating_parameters()
    return read_API_Data






