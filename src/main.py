from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
import json
import os
import uuid  # Usado para gerar um nome de arquivo único

app = FastAPI()

# Diretório onde os arquivos JSON serão salvos.
directory = './listings'

# Verifique se o diretório existe, se não, crie o diretório
if not os.path.exists(directory):
    os.makedirs(directory)

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

def save_listing(listing: dict):
    """Salva o anúncio em um arquivo JSON separado."""
    unique_filename = str(listing["listing_id"])
    file_path = os.path.join(directory, f'{unique_filename}.json')

    with open(file_path, 'w') as file:
        json.dump(listing, file, indent=4)  # Garante uma formatação legível.

@app.post("/add_listing/", response_model=Listing, status_code=status.HTTP_201_CREATED)
async def add_listing(listing: Listing):
    """
    Recebe os dados de um novo anúncio, salva em um arquivo JSON, e retorna os dados do anúncio.
    """
    # Gera um ID único para o listing baseado em UUID
    listing_id = uuid.uuid4().int  # Gera um número inteiro com base no UUID
    listing.listing_id = listing_id  # Atribui o ID ao anúncio

    # Converte o modelo Pydantic para um dicionário antes de salvar
    listing_dict = listing.model_dump()

    save_listing(listing_dict)  # Salva os dados do anúncio em um arquivo JSON.
    return listing  # Retorna os dados do anúncio.

# Este método é apenas para verificação de funcionamento
@app.get("/")
def read_root():
    return {"Hello": "World"}
