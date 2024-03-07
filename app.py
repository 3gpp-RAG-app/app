# app.py
from flask import Flask, session, render_template, request
import uuid
import requests
from datetime import datetime
from config import client, logs_endpoint, search_endpoint, secrect_key

app = Flask(__name__)
app.config["SECRET_KEY"] = secrect_key


completion_history = []


def get_session():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
        return session["session_id"]


def add_to_completion_history(user_message=None, bot_message=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {}
    if user_message is not None:
        entry["user"] = {"query": user_message, "timestamp": timestamp}
    if bot_message is not None:
        entry["bot"] = {"response": bot_message, "timestamp": timestamp}
    completion_history.append(entry)


def post_logs(messages_list):
    session_id = get_session()
    response_log = requests.post(
        logs_endpoint, json={"conversation_id": session_id, "messages": messages_list}
    )

    if response_log.status_code == 200:
        result = "Conversation logged successfully."
    else:
        result = f"Error logging conversation: {response_log.status_code}"

def inject_context(query):
    context = "in 3gpp technical specification: "
    contextualized_query = context + query
    return contextualized_query 


@app.route("/", methods=["GET", "POST"])
def index():
    try:
        user_input = request.form["user_input"]
        add_to_completion_history(user_message=user_input)

        #add_to_completion_history(bot_message="Beep Boop Beep")                         # for testing only
    
        response_search = requests.post(search_endpoint, json={"query": inject_context(user_input)})

        if response_search.status_code == 200:
            result = response_search.json()["results"]["results_text"]

            completion = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": f'You are a 3GPP specialized assistant that provides responses to the user based on the provided reference. Let the user know if the answer cannot be found in the given reference, respond "I could not find an answer." ,  Here is the reference: {result}.',
                    },
                    {"role": "user", "content": user_input},
                ],
                temperature=0.2,
                max_tokens=2000,
                stop=None,
            )

            response_message = completion.choices[0].message
            add_to_completion_history(bot_message=response_message.content)
            post_logs(completion_history)
            return render_template("index.html", completion_history=completion_history)

        else:
            result = f"Error in search request: {response_search.status_code}"
            return render_template("index.html", response=result)

    except Exception as e:
        result = f"Error: {str(e)}"
        #return render_template("index.html", completion_history=completion_history)     # for testing only
        return render_template("index.html", response=result)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, port=3000)
