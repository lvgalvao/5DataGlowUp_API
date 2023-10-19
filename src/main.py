import json
import os
import uuid
from typing import List, Optional

import boto3
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Recupera as variáveis de ambiente após o dotenv ter carregado os valores
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

# Definição do modelo de dados que estamos esperando no JSON
class Listing(BaseModel):
    listing_id: Optional[str] = None
    name: str
    host_id: int
    host_since: str
    host_location: str
    host_response_time: Optional[str] = None  # campos opcionais devem ser inicializados como None
    host_response_rate: Optional[str] = None
    host_acceptance_rate: Optional[str] = None
    host_is_superhost: str
    host_total_listings_count: int
    host_has_profile_pic: str
    host_identity_verified: str
    neighbourhood: str
    district: Optional[str] = None
    city: str
    latitude: float
    longitude: float
    property_type: str
    room_type: str
    accommodates: int
    bedrooms: int
    amenities: List[str] = []
    price: int
    minimum_nights: int
    maximum_nights: int
    review_scores_rating: int
    review_scores_accuracy: int
    review_scores_cleanliness: int
    review_scores_checkin: int
    review_scores_communication: int
    review_scores_location: int
    review_scores_value: int
    instant_bookable: str

# Inicializar o cliente S3
s3_client = boto3.client('s3', 
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def save_to_s3(file_content, file_name):
    try:
        s3_client.put_object(Body=file_content, Bucket=AWS_STORAGE_BUCKET_NAME, Key=file_name)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": f"Error: {e}"})


@app.post("/add_listing/", response_model=Listing, status_code=status.HTTP_201_CREATED)
async def add_listing(listing: Listing):
    unique_filename = f"{uuid.uuid4()}.json"
    listing_json = listing.json()
    
    response = save_to_s3(listing_json, unique_filename)
    if response:
        return response

    return listing

# Este método é apenas para verificação de funcionamento
@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn

    # Get the port from the environment variable or default to 10000 if it's not provided
    PORT = int(os.getenv("PORT", 10000))
    
    # Host 0.0.0.0 is used to make the server publicly available.
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, log_level="info")