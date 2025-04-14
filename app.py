from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from services.fft_analyzer import analyze_eeg

app = FastAPI(
    title="EEG Analysis Service",
    description="腦波 FFT 分析服務",
    version="1.0.0"
)

class AnalysisRequest(BaseModel):
    data: List[float]
    fs: float = 250.0

class AnalysisResponse(BaseModel):
    absolute_power: dict
    relative_power: dict
    alpha_theta_ratio: float
    data_info: dict

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest):
    try:
        result = analyze_eeg(request.data, request.fs)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 