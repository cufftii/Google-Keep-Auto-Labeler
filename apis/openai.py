import os
import openai
from dotenv import load_dotenv

def completion(prompt, temperature=0.3, max_tokens=1000):
    load_dotenv()
    openai.api_key = os.getenv('API_KEY')
    
    engine = "text-davinci-003"
    response = openai.Completion.create(engine=engine, prompt=prompt,temperature=temperature, max_tokens=max_tokens)
    answer = response.choices[0].text
    return answer

def embeddings(input):
    response = openai.Embedding.create(input=input, model='text-embedding-ada-002')['data']
    return response