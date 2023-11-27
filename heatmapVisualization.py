import os
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import folium
from folium.plugins import HeatMap
from parametersReading_API import reading_geo_parameters
from starlette import status
from starlette.responses import RedirectResponse


app=FastAPI()


router = APIRouter(
    prefix="/heatmap",
    tags=["todos"],
    responses={404: {"description": "Not found"}}
)


templates = Jinja2Templates(directory="templates")



async def generating_tempreture_heatmap():
    file_name="templates/tempratureheatmap.html"
    if not os.path.exists(file_name):
        readingData_API=await reading_geo_parameters()
        fig = folium.Figure() # Create a figure axises to plot the map with heatmap
        tempreture_data=[] 
        total_latitude = 0
        total_longitude = 0
        data_count = 0
    
        for temp in readingData_API:
            lat=temp["Latitude"]
            long=temp["Longitude"]
            tempList=temp["Tempreture"]
            tempreture_data.append((lat, long, tempList))  
        # Get the average of all values in Latitude and longitude to point the heatmap in the map  
            total_latitude += lat
            total_longitude += long
            data_count += 1
        average_latitude = total_latitude / data_count
        average_longitude = total_longitude / data_count
        
        create_map1=folium.Map(location=[average_latitude, average_longitude], tiles='openstreetmap', zoom_start=5) # Generate base map 
        # Add the heatmap to the base map
        HeatMap(tempreture_data, radius=15).add_to(create_map1)
    
        fig.add_child(create_map1)
        fig.save(file_name) # Save the heatmap in an HTML Template

#Generating heatmap for Pressure
async def generating_pressure_heatmap():
    file_name="templates/pressureheatmap.html"
    if not os.path.exists(file_name):
        readingData_API=await reading_geo_parameters()
        fig = folium.Figure() # Create a figure axises to plot the map with heatmap
        pressure_data=[]
        total_latitude = 0
        total_longitude = 0
        data_count = 0
        
        for press in readingData_API:
            lat=press["Latitude"]
            long=press["Longitude"]
            pressList=press["Pressure"]
            pressure_data.append((lat, long, pressList))
            total_latitude += lat
            total_longitude += long
            data_count += 1
        average_latitude = total_latitude / data_count
        average_longitude = total_longitude / data_count
        create_map2 = folium.Map(location=[average_latitude, average_longitude], tiles='openstreetmap', zoom_start=2)
        HeatMap(pressure_data, radius=15).add_to(create_map2)   
        fig.add_child(create_map2) 
        fig.save(file_name)
    
async def generating_steam_heatmap():
    file_name="templates/steamheatmap.html"
    if not os.path.exists(file_name):
        readingData_API=await reading_geo_parameters()
        fig = folium.Figure() # Create a figure axises to plot the map with heatmap
        steam_data=[]
        total_latitude = 0
        total_longitude = 0
        data_count = 0
        for steam in readingData_API:
            lat=steam["Latitude"]
            long=steam["Longitude"]
            steamList=steam["Steam_Injection"]
            steam_data.append((lat, long,  steamList)) 
            total_latitude += lat
            total_longitude += long
            data_count += 1
        average_latitude = total_latitude / data_count
        average_longitude = total_longitude / data_count
    
        create_map3=folium.Map(location=[average_latitude, average_longitude], tiles='openstreetmap', zoom_start=2)   
        HeatMap(steam_data, radius=15).add_to(create_map3)  
        
        fig = folium.Figure()
        fig.add_child(create_map3)
        #print(steam_data)
        fig.save(file_name)
    
    

@router.get('/tempreture', response_class=HTMLResponse)
async def show_tempreture_heatmap(request:Request): 
    await generating_tempreture_heatmap()
    return templates.TemplateResponse("tempratureheatmap.html", {"request":request})


@router.get('/pressure', response_class=HTMLResponse)
async def show_presssure_heatmap(request:Request): 
    await generating_pressure_heatmap()
    return templates.TemplateResponse("pressureheatmap.html", {"request":request})

@router.get('/steam', response_class=HTMLResponse)
async def show_heatmap(request:Request): 
    await generating_steam_heatmap()
    return templates.TemplateResponse("steamheatmap.html", {"request":request})
app.include_router(router)
    
        

   




      