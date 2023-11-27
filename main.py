from fastapi import FastAPI
import parametersReading_API
import heatmapVisualization 
import updateParameters 

app=FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "Heatmap"}