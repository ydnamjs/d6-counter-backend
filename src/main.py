from fastapi import FastAPI, HTTPException, Response, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
from io import BytesIO
from PIL import Image

from process_image import preprocess_image, predict_image, process_predictions, image_to_base64

class OutputModel(BaseModel):
    preprocessed_image: str
    output_image: str
    total: int

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/post-image/")
async def process_frame(image: Annotated[UploadFile, Form()], canny_threshold_1: Annotated[int, Form()], canny_threshold_2: Annotated[int, Form()]):


    if image.content_type not in ["image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PNG files are allowed.")

    image = Image.open(BytesIO(await image.read()))
    preprocessed_image_array = preprocess_image(image, canny_threshold_1, canny_threshold_2)
    boxes, scores, predictions = predict_image(preprocessed_image_array)
    outputImage, predicted_total = process_predictions(image, boxes, scores, predictions, .65)

    img_byte_arr = BytesIO()
    outputImage.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return OutputModel(
        preprocessed_image=image_to_base64(Image.fromarray(preprocessed_image_array)), 
        output_image=image_to_base64(outputImage), 
        total=predicted_total
    )