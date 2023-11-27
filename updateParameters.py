from fastapi import FastAPI, Body, APIRouter, Request
from parametersReading_API import reading_geo_parameters
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.responses import RedirectResponse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pydantic import BaseModel

app = FastAPI()
router = APIRouter(
    prefix="/update",
    tags=["update"],
    responses={404: {"description": "Not found"}}
)


templates = Jinja2Templates(directory="templates")

# Create Model class to store the variable in the api to utilize for updating the value
class UpdateParametersModel(BaseModel):
    Site_Name: str
    Temperature: int
    Pressure: int
    Steam_Injection: int

@router.post("/parameters/{site_id}", response_model=UpdateParametersModel)
async def update_parameters(site_id: int, update_params: UpdateParametersModel):
    # Fetch the data and find the specific site
    reading_API = await reading_geo_parameters()
    for item in reading_API:
        if item['Site_ID'] == site_id:
            item['Site_Name'] = update_params.Site_Name
            item['Temperature'] = update_params.Temperature
            item['Pressure'] = update_params.Pressure
            item['Steam_Injection'] = update_params.Steam_Injection
            # return item
        else:
            return {"message": "Site ID not found"}          
    return {"message": "Site ID not found"}


@router.get('/parameters/{site_id}', response_class=HTMLResponse)
async def read_updating_parameters(request: Request, site_id: int):
    parameters_data = await reading_geo_parameters()
    site_data = next((item for item in parameters_data if item["Site_ID"] == site_id), None)
    return templates.TemplateResponse('update_parametersForm.html', {"request": request, "site_data": site_data})

@router.get('/temporal_correlation')
async def temporal_correlation(request: Request):
     # Load or generate your historical data
    historical_data = await reading_geo_parameters()
    historical_df = pd.DataFrame(historical_data)
    
#     # Exclude  date columns and delete the id column
    numerical_df =historical_df.drop(columns=['Site_ID']).select_dtypes(include=[np.number])

#     # Generate a correlation plot and save as picture
    plt.figure(figsize=(10, 8))
    sns.heatmap(numerical_df.corr(), annot=True, cmap='coolwarm')
    plt.title('Temporal Correlation of Parameters')
    plot_filename = 'temporal_correlation_plot.png'
    plt.savefig(plot_filename)

#     # Serve the plot as a static file
    return FileResponse(plot_filename)
app.include_router(router)





