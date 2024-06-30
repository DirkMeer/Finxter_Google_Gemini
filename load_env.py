import os

import google.generativeai as genai
from dotenv import load_dotenv


def configure_genai():
    load_dotenv()
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    return genai