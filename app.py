from flask import Flask, render_template, request
import google.generativeai as genai
import os

# 🔐 Set your Gemini API Key
genai.configure(api_key="AIzaSyCIqYQvLOVOqmSYvBnvmFkXlkOkqKLdy_c")  # Replace with your API key

app = Flask(__name__)

# 🧠 Gemini model setup
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
            - Best practices

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
