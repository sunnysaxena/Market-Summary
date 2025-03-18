import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-pro-exp-02-05",
    generation_config=generation_config,
    system_instruction="You are an expert in algorithmic trading, quantitative finance, and market analysis. "
                       "Your task is to engage in conversations about trading strategies, backtesting, "
                       "real-time market behavior, and financial concepts. Explain complex topics in a clear and relatable way, "
                       "using real-world market examples and historical events. Make discussions engaging by "
                       "incorporating insights from technical analysis, statistical models, and trading psychology. "
                       "Use humor and thought-provoking questions to enhance learning. "
                       "Encourage interactive discussions by helping users connect these concepts to real trading experiences, "
                       "algorithm development, backtesting frameworks, and performance optimization."
)

chat_session = model.start_chat(
    history=[]
)

print("Bot: Hello, how can I help you?")
print()

while True:
    user_input = input("You: ")
    print()

    response = chat_session.send_message(user_input)
    model_response = response.text

    print(f'Bot: {model_response}')

    print()
    chat_session.history.append({"role": "user", "parts": [user_input]})
    chat_session.history.append({"role": "model", "parts": [model_response]})
