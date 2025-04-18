from flask import Flask, render_template, request
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
# Set your Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

# Gemini model setup
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/", methods=["GET", "POST"])
def index():
    review = ""
    code = ""
    if request.method == "POST":
        code = request.form["code"]
        try:
            prompt = f"""
            You are an AI code reviewer. Review this Python code for:
            - Bugs
            - Code style
            - Optimization suggestions
            - Best practices if the code is correct don't give suggestions
            - give the correct code if the code is incorrect
            - Give me in few lines correct or not, if not git me the suggestions

            Code:
            {code}
            """
            response = model.generate_content(prompt)
            review = response.text
        except Exception as e:
            review = f"Error: {str(e)}"
    return render_template("index.html", review=review, code=code)

if __name__ == "__main__":
    app.run(debug=True)
