import json
import os
import uuid
from typing import List, Optional

import boto3
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse


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
@app.get("/", response_class=HTMLResponse)
def read_root():
    # Este é o seu JSON de exemplo como uma string
    json_example = '''
{
  "name": "Beautiful Flat in le Village Montmartre, Paris",
  "host_id": 1466919,
  "host_since": "2011-12-03",
  "host_location": "Paris, Ile-de-France, France",
  "host_response_time": null,
  "host_response_rate": null,
  "host_acceptance_rate": null,
  "host_is_superhost": "f",
  "host_total_listings_count": 1,
  "host_has_profile_pic": "t",
  "host_identity_verified": "f",
  "neighbourhood": "Buttes-Montmartre",
  "district": null,
  "city": "Paris",
  "latitude": 48.88668,
  "longitude": 2.33343,
  "property_type": "Entire apartment",
  "room_type": "Entire place",
  "accommodates": 2,
  "bedrooms": 1,
  "amenities": [
    "Heating",
    "Kitchen",
    "Washer",
    "Wifi",
    "Long term stays allowed"
  ],
  "price": 53,
  "minimum_nights": 2,
  "maximum_nights": 1125,
  "review_scores_rating": 100,
  "review_scores_accuracy": 10,
  "review_scores_cleanliness": 10,
  "review_scores_checkin": 10,
  "review_scores_communication": 10,
  "review_scores_location": 10,
  "review_scores_value": 10,
  "instant_bookable": "f"
}
'''
    formatted_json = json.dumps(json_example, indent=4)  # 'indent=4' adiciona 4 espaços de indentação

    # Construindo a resposta HTML
    content = f'''
<html>
    <head>
        <title>Bem-vindo à nossa primeira API!</title>
        <style>
            body {{
                background-color: #282c34;
                color: white;
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }}
            h1 {{
                margin-bottom: 20px;
            }}
            p {{
                margin-bottom: 5px;
            }}
            a {{
                color: #09f;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            /* Aqui estão os estilos adicionais para a textarea */
            #myJson {{
                width: 600px; /* ou qualquer largura que você preferir */
                height: 300px; /* ou qualquer altura que você preferir */
                font-size: 16px; /* opcional: ajusta o tamanho da fonte dentro da textarea */
                white-space: nowrap; /* impede que o texto quebre para a próxima linha */
                overflow-x: auto; /* adiciona uma barra de rolagem se o conteúdo for muito largo */
            }}
        </style>
        <script>
        function copyToClipboard() {{
            var copyText = document.getElementById("myJson");
            copyText.select();
            copyText.setSelectionRange(0, 99999); // Para dispositivos móveis
            document.execCommand("copy");
            alert("Copied the text: " + copyText.value);
        }}
        </script>
    </head>
    <body>
        <div>
            <h1>Nossa primeira API!</h1>
            <p>Visite <a href="https://fivedataglowup.onrender.com/docs">aqui</a> para popular o banco.</p>
            <p>Repositório do projeto: <a href="https://github.com/lvgalvao/5DataGlowUp_lvgalvaofilho" target="_blank">GitHub</a></p>
            <p>Documentação do projeto: <a href="https://lvgalvao.github.io/5DataGlowUp_lvgalvaofilho/" target="_blank">GitHub Pages</a></p>
            <p><strong>Exemplo de JSON:</strong></p>
            <textarea id="myJson" readonly style="white-space: pre-wrap;">{json_example}</textarea><br><br>
            <button onclick="copyToClipboard()">Copiar JSON</button>
        </div>
    </body>
</html>
'''

    return HTMLResponse(content=content)

if __name__ == "__main__":
    import uvicorn

    # Get the port from the environment variable or default to 10000 if it's not provided
    PORT = int(os.getenv("PORT", 10000))
    
    # Host 0.0.0.0 is used to make the server publicly available.
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, log_level="info")