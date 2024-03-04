from flask import Flask, render_template, request
import requests
from config import client  
app = Flask(__name__)

 

@app.route('/')
def index():
    return render_template('index.html')

completion_history = []

def add_to_completion_history(user_message, bot_message):
    completion_history.append({'user': user_message, 'bot': bot_message})

@app.route('/submit', methods=['POST'])
def submit():
    try:
        user_input = request.form['user_input']
        api_endpoint = 'https://true-suns-cry.loca.lt/milvus/search'
        response = requests.post(api_endpoint, json={'query': user_input})
        output_file_path = 'best_hit_details.txt'


        '''if response.status_code == 200:
            result = response.json()["results"]'''
        result='The total layer 2 buffer size is defined as the sum of the number of bytes that the UE is capable of storing in the RLC transmission windows and RLC reception and reassembly windows and also in PDCP reordering windows for all radio bearers.'

        completion = client.chat.completions.create(
            # model="gpt-4-turbo-preview",
            model="gpt-3.5-turbo",
            messages=[
                # {"role": "system", "content": f'You are a 3GPP specialized assistant that provides responses to the user based on the provided reference. Let the user know if the answer cannot be found in the given reference, respond "I could not find an answer." ,  Here is the reference: {result}.'},
                {"role": "system", "content": 'You are a chatbot.'},
                {"role": "user", "content": user_input}
            ],
            temperature=0.2,
            max_tokens=2000,
            stop=None
        )

 

        response_message = completion.choices[0].message
        add_to_completion_history(user_message=user_input, bot_message=response_message.content)
        return render_template('index.html', completion_history=completion_history)

 

        '''else:
            result = f"Error: {response.status_code}"
            return render_template('index.html', response=result)'''

 

    except Exception as e:
        result = f"Error: {str(e)}"
        return render_template('index.html', response=result)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)