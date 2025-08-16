import chainlit as cl
import requests 

@cl.on_chat_start
async def start_chat():
    await cl.Message(
        content="Welcome to the Chatbot! I am your Cryptocurrency agent and will show you the top 10 cryptocurrency rates.\n\n"
    ).send()
    
@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content.strip().upper()
    
    if user_input == "TOP 10 CRYPTO":
        url = "https://api.binance.com/api/v3/ticker/price"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            # Filter for USDT pairs and get top 10
            usdt_pairs = [c for c in data if c['symbol'].endswith('USDT')][:10]
            top_10 = "\n".join([f"{c['symbol']}: {float(c['price']):,.2f} USDT" for c in usdt_pairs])
            await cl.Message(content=f"Top 10 Cryptocurrency Rates:\n{top_10}").send()
        except Exception as e:
            await cl.Message(
                content=f"An error occurred while fetching data: {str(e)}"
            ).send()
    else:
        # Ensure the symbol is in the correct format (add USDT if needed)
        symbol = user_input if user_input.endswith('USDT') else f"{user_input}USDT"
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                await cl.Message(
                    content=f"{data['symbol']} Price: {float(data['price']):,.2f} USDT"
                ).send()
            else:
                await cl.Message(
                    content=f"Could not retrieve data for {symbol}. Please check the symbol and try again. Status code: {response.status_code}"
                ).send()
        except Exception as e:
            await cl.Message(
                content=f"An error occurred while fetching data: {str(e)}"
            ).send()