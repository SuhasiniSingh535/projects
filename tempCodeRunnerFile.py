import json
import openai
import os
import model
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

print("Loading model...")
model, tokenizer = model.load_model("quant_falcon_lora_new_30_june")
print("Model loaded.")

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_images(prompts):
    urls = []
    for prompt in prompts:
        try:
            resp = openai.Image.create(model="dall-e-3", prompt=prompt, n=1, size="512x512")
            urls.append(resp["data"][0]["url"])
        except Exception as e:
            print("Image gen failed:", e)
            urls.append(None)
    return urls

def generate_deeper_paragraph(answer_text: str):
    prompt = f"""You are an NCERT expert. Based on the following answer, write an insightful paragraph (about 160–180 words, medium–hard level) expanding the concept and its importance:

Answer:
\"\"\"{answer_text}\"\"\"

Paragraph:"""
    resp = openai.ChatCompletion.create(
        model="falcon-7b-instruct",
        messages=[
            {"role": "system", "content": "NCERT detailed explainer"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=400,
    )
    return resp.choices[0].message.content.strip()

def generate_ncert_mcqs(answer_text: str, difficulty: str):
    prompt = f"""You are an NCERT expert. Based on the following answer text, generate 10 MCQs aligned to it. Return JSON list:
[
  {{
    "question": "...",
    "options": ["A","B","C","D"],
    "answer": "B"
  }}
]
Difficulty: {difficulty}.
Answer text:
\"\"\"{answer_text}\"\"\""""
    resp = openai.ChatCompletion.create(
        model="falcon-7b-instruct",
        messages=[
            {"role": "system", "content": "NCERT MCQ generator"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1500,
    )
    return json.loads(resp.choices[0].message.content)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    q = data.get("question", "").strip()
    diff = data.get("difficulty", "easy")
    if not q:
        return jsonify({"error": "Please provide a question."}), 400

    text_ans = model.answer_question((model_obj, tokenizer), q)

    answer_prompts = [f"Illustration for: {q}", f"Diagram of key concept in: {q}", f"Visual summary: {q}"]
    answer_images = generate_images(answer_prompts)

    paragraph = None
    try:
        paragraph = generate_deeper_paragraph(text_ans)
    except Exception as e:
        print("Paragraph gen failed:", e)

    paragraph_prompts = [
        f"Explanatory diagram for: {text_ans}",
        f"Engaging visual for concept: {text_ans}",
        f"Detailed flowchart: {text_ans}"
    ]
    paragraph_images = generate_images(paragraph_prompts)

    mcqs = None
    try:
        mcqs = generate_ncert_mcqs(text_ans, diff)
    except Exception as e:
        print("MCQ gen failed:", e)

    return jsonify({
        "answer": text_ans,
        "answer_images": answer_images,
        "paragraph": paragraph,
        "paragraph_images": paragraph_images,
        "mcqs": mcqs
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
