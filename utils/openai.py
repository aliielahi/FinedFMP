from openai import OpenAI
import numpy as np
import pandas as pd


class OpenAIEmbedding:
    def __init__(self, openapikey = openapikey1):
        
        self.client = OpenAI(api_key = openapikey)

    def get_embedding(self, text, model="text-embedding-3-small"):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input = [text], model=model, dimensions = 200).data[0].embedding