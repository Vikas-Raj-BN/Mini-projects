from flask import Flask, request, render_template, session
import pandas as pd
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Path to the Excel file
file_path = "qa_database.xlsx"

# Load the Q&A database
try:
    database = pd.read_excel(file_path)
    database.fillna("", inplace=True)  # Handle NaN values
    print("Database loaded successfully!")
except Exception as e:
    print(f"Error loading the database: {e}")
    database = None

# Function to clean text by removing special characters and punctuation
def clean_text(text):
    return re.sub(r"[^\w\s]", "", text).strip().lower()

# Function to extract user name from input
def extract_name(input_text):
    name_prefixes = ["my name is", "i am", "call me"]
    input_text_lower = input_text.lower()
    for prefix in name_prefixes:
        if prefix in input_text_lower:
            return input_text_lower.split(prefix, 1)[1].strip().title()
    return None

# Function to match user input with the database
def get_response(user_message):
    if database is not None:
        user_message_cleaned = clean_text(user_message)
        for _, row in database.iterrows():
            question_cleaned = clean_text(row["Question"])
            if question_cleaned == user_message_cleaned:
                return row["Answer"]
    return "Sorry, I don't have an answer for that question."

@app.route("/", methods=["GET", "POST"])
def chatbot():
    if "chat_history" not in session:
        session["chat_history"] = []
    if "user_name" not in session:
        session["user_name"] = None

    if request.method == "POST":
        user_message = request.form.get("user_message", "").strip()
        if user_message:
            bot_response = ""

            if user_message.lower() == "exit":
                session["chat_history"] = []
                bot_response = "Welcome! 😊 I’m here to assist you. Just ask away!?"
            elif session["user_name"] is None:
                if user_message.lower() in ["what is my name", "tell me my name"]:
                    bot_response = "I don't know your name yet. Could you please tell me your name?"
                else:
                    extracted_name = extract_name(user_message)
                    if extracted_name:
                        session["user_name"] = extracted_name
                        bot_response = f"Nice to meet you, {extracted_name}! How can I assist you today?"
                    else:
                        bot_response = get_response(user_message)
            elif user_message.lower() in ["what is my name", "tell me my name","tell my name"]:
                bot_response = f"Your name is {session['user_name']}!" if session["user_name"] else "I don't know your name yet."
            else:
                bot_response = get_response(user_message)

            session["chat_history"].append({"user": user_message, "bot": bot_response})
            session.modified = True

    return render_template(
        "index.html",
        chat_history=session.get("chat_history", []),
        user_name=session.get("user_name"),
    )

if __name__ == "__main__":
    app.run(debug=True)