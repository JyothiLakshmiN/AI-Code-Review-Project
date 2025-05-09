from flask import Flask, render_template, request
import google.generativeai as genai
import os
from dotenv import load_dotenv
import werkzeug
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
        print("request---", request.form["language"])
        code = request.form["code"]
        language = request.form["language"]
         # Handle file upload
        uploaded_file = request.files.get("code-file")
        if uploaded_file:
            filename = werkzeug.utils.secure_filename(uploaded_file.filename)
            file_extension = filename.split('.')[-1].lower()
            if file_extension == "py":
                language = "python"
            elif file_extension == "js":
                language = "javascript"
            code = uploaded_file.read().decode('utf-8')

        if not code or not language:
            review = "❌ Please enter code or upload a valid file."
        else:
            prompt = f"""
            You are an AI code reviewer. Review this {language} code for:
            Checklist:
            - Check for syntax or logic bugs
            - Suggest style or performance improvements
            - Highlight best practice violations
            - If the code is correct, say it's ✅ Correct
            - If incorrect, provide 💡 Suggestions and the corrected version
            - If `try-catch` / `try-except` blocks are missing around risky code (e.g., file I/O, API calls, division), suggest or add them.

            Code:
            {code}
            """
        try:
            response = model.generate_content(prompt)
            review = response.text
        except Exception as e:
            review = f"Error: {str(e)}"
    return render_template("index.html", review=review, code=code)

if __name__ == "__main__":
    app.run(debug=True)
