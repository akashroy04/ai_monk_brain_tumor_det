import io
import cv2
import numpy as np
from PIL import Image
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile
from src.core.handler import format_output
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/my_health")
async def my_health():
    return {"status": "Service module healthy!"}


def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(i) for i in obj]
    elif isinstance(obj, tuple):
        return tuple(make_json_safe(i) for i in obj)
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    else:
        return obj


@app.post("/generate_analysis")
async def brain_tumor(img: UploadFile = File(...)):
    print("Backend Service Triggered")
    image_bytes = await img.read()
    image = Image.open(io.BytesIO(image_bytes))

    image_np = np.array(image)
    image_cv2 = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    result_dict = format_output(image_cv2)

    extracted_data = {
        "filename": img.filename,
        "meta": {"width": int(image.width), "height": int(image.height)},
        "processed_output": make_json_safe(result_dict)
    }

    return JSONResponse(content=extracted_data)
