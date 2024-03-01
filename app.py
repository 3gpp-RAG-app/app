# app.py
from flask import Flask, render_template, request
import requests
from config import client  

app = Flask(__name__)

# Initialize an empty list for chat history
chat_history = []

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        user_input = request.form['user_input']
        api_endpoint = 'https://true-suns-cry.loca.lt/milvus/search'  # Remember to activate; my IP is 81.175.131.163
        response = requests.post(api_endpoint, json={'query': user_input})
        output_file_path = 'best_hit_details.txt'

        if response.status_code == 200:
            result = response.json()["results"]

            # Append user and bot messages to chat history
            user_message = user_input
            bot_message = f'You are a 3GPP specialized assistant... {result}'
            add_to_chat_history(user_message, bot_message)

            with open(output_file_path, 'w') as file:
                file.write(f'Best hit text: {result}\n')

            completion = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": f'You are a 3GPP specialized assistant that provides responses to the user based on the provided reference. Let the user know if the answer cannot be found in the given reference, respond "I could not find an answer." ,  Here is the reference: {result}.'},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.2,
                max_tokens=2000,
                stop=None
            )

            response_message = completion.choices[0].message
            print(response_message)
            return render_template('index.html', response=response_message, chat_history=chat_history)
        else:
            result = f"Error: {response.status_code}"
            return render_template('index.html', response=result, chat_history=chat_history)

    except Exception as e:
        result = f"Error: {str(e)}"
        return render_template('index.html', response=result, chat_history=chat_history)

# Function to add messages to chat history
def add_to_chat_history(user_message, bot_message):
    chat_history.append({'user': user_message, 'bot': bot_message})

if __name__ == '__main__':
    app.run(debug=True, port=3000)
