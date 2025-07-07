import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import generate_text

app = Flask(__name__)
CORS(app, origins="http://127.0.0.1:5500", methods=["POST", "GET", "OPTIONS"])

# Capture INFO logs
app.logger.setLevel(logging.INFO)

@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:5500"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}
    app.logger.info("Received /ask POST: %s", data)

    question = data.get("question", "").strip()
    difficulty = data.get("difficulty", "easy")

    if not question:
        app.logger.info("No question provided, returning 400")
        return jsonify({"error": "No question provided"}), 400

    try:
        app.logger.info("Generating answer for question: %s", question)
        answer = generate_text(question)
        app.logger.info("Answer length: %d", len(answer))

        paragraph = None
        if difficulty in ("medium", "hard", "mix"):
            paragraph = generate_text(f"Explain in-depth: {question}")
            app.logger.info("Paragraph length: %d", len(paragraph))

        mcqs = None
        if difficulty in ("easy", "medium", "hard", "mix"):
            mcq_prompt = f"Generate MCQs for: {question} (difficulty: {difficulty})"
            mcq_text = generate_text(mcq_prompt)
            app.logger.info("MCQ text length: %d", len(mcq_text))
            mcqs = [{"question": m.strip(), "options": [], "answer": ""} for m in mcq_text.split("\n") if m.strip()]

        return jsonify({"answer": answer, "paragraph": paragraph, "mcqs": mcqs}), 200

    except Exception:
        app.logger.exception("Exception while processing /ask")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
