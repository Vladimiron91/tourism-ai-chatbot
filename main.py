import os
from dotenv import load_dotenv
from openai import OpenAI


#Variablen aus der .env Datei

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

