from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel
from PIL import Image
from io import BytesIO

from .process_image import preprocess_image, predict_image, process_predictions, image_to_base64

# new_session_id = 0

class ImageModel(BaseModel):
    preprocessed_image: str
    output_image: str
    total: int

# active_sessions = {}

app = FastAPI()

# @app.get("/")
# def root():
#     return {"Hello": "World"}

# items = []

# @app.post("/items")
# def create_item(item: str):
#     items.append(item)
#     return items

# @app.get("/items/{item_id}")
# def get_item(item_id: int) -> str:
#     if item_id < len(items) and item_id >= 0:
#         return items[item_id]
#     else:
#         raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

# @app.get("/start-new-session/")
# def start_new_session():
#     session_id = new_session_id
#     new_session_id = new_session_id + 1
#     return session_id

@app.post("/post-image/", response_model=ImageModel)
async def process_frame(image: UploadFile, canny_threshold_1: int, canny_threshold_2):

    if image.content_type not in ["image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PNG files are allowed.")

    image = Image.open(BytesIO(image))
    preprocessed_image_array = preprocess_image(image, canny_threshold_1, canny_threshold_2)
    boxes, scores, predictions = predict_image(preprocessed_image_array)
    outputImage, predicted_total = process_predictions(image, boxes, scores, predictions, .65)

    return ImageModel(
        preprocessed_image=image_to_base64(Image.fromarray(preprocessed_image_array)), 
        output_image=image_to_base64(outputImage), 
        total=predicted_total
    )

# @app.get("/get-processed-image")
# async def get_processed_image(id: int):
#     if id not in active_sessions:
#         raise HTTPException(status_code=404, detail="Image not found")
    
#     image = active_sessions[id]
    
#     img_byte_arr = BytesIO()
#     image.save(img_byte_arr, format='PNG')
#     img_byte_arr.seek(0)
    
#     return responses.FileResponse(img_byte_arr, media_type="image/png")