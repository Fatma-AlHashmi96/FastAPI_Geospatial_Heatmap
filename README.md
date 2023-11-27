# FastAPI_Geospatial_Heatmap
## Install FastAPI Virtual Enviroment on the application directory to get the packages:
>> python -m venv fastapienv
>> To Activate- fastapienv\Scripts\activate.bat

##Docker Contianerization:
1.Install Docker Desktop
2. To Build Docker Type: >> docker build -t geospatial-heatmap-api .
3. To run: >> docker run -d --name your-new-container-name -p 8080:80 your-image-name
   Note: I containerization the whole application without Authentication due to the "Server Creditials Requirements"

##Login Page:
1. Run in powershall:>> uvicorn Authentication:app --reload
    * In browser address bar type after run uvicorn:  http://127.0.0.1:8000/auth/
3. I did the authetication using Microsoft SSO integration with my application actiove directory using "python-ldap3" - Adding pip python-ldap3 (Not working)

## Reading Data from API:
1. Run in powershall:>> uvicorn parametersReading_API:app --reload
2. In browser address bar type after run uvicorn: >> http://127.0.0.1:8000/docs - Will open SWAGGER UI as Servere to check the api data
   
##Geospatial Heatmap Vosualization:
1. Run in powershall:>> uvicorn heatmapVisualization:app --reload
  * In browser address bar type after run uvicorn: http://127.0.0.1:8000/heatmap/tempreture/
2.  press Next button to move to another geospatial heatmap( pressure & steam Injection)

## Implementation of Temprol Correlation to Allow user to navigete through historical data:
Run in powershall:>> uvicorn updateParameters:app --reload
  * In browser address bar type after run uvicorn: http://127.0.0.1:8000/update/temporal_correlation
  * In browser address bar type after run uvicorn for updating data in API based on Site_ID:  http://127.0.0.1:8000/update/parameters/type ID

## Packages Need to Install:
1. pip install starlette
2.  pip install fastapi
3.   pip install pydantic
4.   pip install datetime
5.   pip install python-jose
6.   pip install jwt
7.   pip install python-ldap3
8.   pip install pandas
9.   pip install seaborn
10.   pip install geopy
11.   pip install folium







