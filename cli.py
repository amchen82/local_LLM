# Example: reuse your existing OpenAI setup
from openai import OpenAI
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import yfinance as yf   
import pandas as pd
import json
import functools
import webbrowser
# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
# define scheme of tools
tools = [
    {
        "type":"function" ,
        "function":{
            "name": "get_stock_price",
            "description": "Get the stock price of a company",
            "parameters": {
                "type": "string",
                "properties": {   
                    "symbol": { 
                        "type": "string",
                        "description": "The stock symbol"
                    }
            }
        },
            "required": ["symbol"],
            
            }
        }
    
]


def  get_stock_price(symbol: str) -> str:
    print(f"Getting stock price for {symbol}")
    shock = yf.Ticker(symbol)
    history = shock.history(period="1mo")
    current_price = history["Close"].iloc[-1]
    print(f"The current price of {symbol} is {current_price}")
    return json.dumps({'price':current_price})
    

completion = client.chat.completions.create(
  model="TheBloke/dolphin-2.6-mistral-7B-GGUF/dolphin-2.6-mistral-7b.Q2_K.gguf",
  messages=[
    {"role": "system", "content": """
     you help to extract ticker symbol from user question ,
     output in json format {ticker : {ticket symbol}}, only output json info. 

    for example, 

    user question: what is the stock price for Apple
    output: {ticker:{AAPL}}

    user question : can you find the stock price for tesla
    output: {ticker:{TSLA}}
    
 """},
        {"role": "user", "content": "what is stock price for ford."}

  ],
  
)

response = completion.choices[0].message.content
json.loads(response)
print(response) # {"ticker":"F"}
print(get_stock_price(json.loads(completion.choices[0].message.content)['ticker']))
import webbrowser

query =" gogle cloud next "
url = "https://www.google.com/search?q=" + query

webbrowser.open_new_tab(url)

