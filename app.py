from flask import Flask, render_template, request, Response, stream_with_context, session, jsonify
from chatbot_logic import stream_claude_response  # new function for SSE
import os
from summarization_logic import summarize_pdf  # assuming you modularize it

# Import or initialize your Claude/OpenAI client here
from chatbot_logic import client  # Make sure 'client' is defined in chatbot_logic.py
from rag import add_pdf_to_vector_db, retrieve_relevant_context
from tools.web_search import web_search
from tools.code_executor import run_python_code
from tools.image_generator import generate_image

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev")  # for sessions

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/summarize')
def summarize():
    return render_template('summarize.html')

from flask import session
import uuid

def save_message(session_id, role, content):
    # Use ORM instead of raw sqlite3:
    msg = Message(session_id=session_id)
    if role == 'user':
        msg.user_message = content
    else:
        msg.assistant_reply = content
    db.session.add(msg)
    db.session.commit()

def get_messages(session_id):
    return Message.query.filter_by(session_id=session_id).all()

@app.before_request
def ensure_session():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

# Add SQLAlchemy imports and setup at the top of your file (after other imports)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_logs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db_session = db.session

# Define your models if not already defined
class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(128), unique=True, nullable=False)
    messages = db.relationship('Message', backref='chat_session', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(128), db.ForeignKey('chat_session.session_id'), nullable=False)
    user_message = db.Column(db.Text)
    assistant_reply = db.Column(db.Text)

@app.route("/ask_claude", methods=["POST"])
def ask_claude():
    user_input = request.json.get("message")
    session_id = request.json.get("session_id")

    # === Orchestrate tools ===
    tool_result = None
    if "search the web" in user_input.lower():
        tool_result = web_search(user_input)
    elif "run this code" in user_input.lower():
        # simple: extract code manually or with regex
        tool_result = run_python_code(user_input)
    elif "draw an image" in user_input.lower():
        tool_result = generate_image(user_input)

    # Compose prompt:
    prompt = f"TOOL OUTPUT:\n{tool_result}\n\nUser: {user_input}" if tool_result else user_input

    # Retrieve context from DB
    conversation = db_session.query(ChatSession).filter_by(session_id=session_id).first()
    history = []
    if conversation:
        for m in conversation.messages:
            history.append({"role": "user", "content": m.user_message})
            history.append({"role": "assistant", "content": m.assistant_reply})
    history.append({"role": "user", "content": prompt})

    # Stream Claude
    try:
        stream = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            messages=history,
            stream=True
        )

        reply_text = ""
        for chunk in stream:
            if chunk.type == "content_block_delta":
                reply_text += chunk.delta.text

        # Save chat
        if not conversation:
            conversation = ChatSession(session_id=session_id)
            db_session.add(conversation)
            db_session.commit()
        db_session.add(Message(session_id=session_id, user_message=user_input, assistant_reply=reply_text))
        db_session.commit()

        return jsonify({"reply": reply_text, "tool_result": tool_result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/summarize_pdf', methods=['POST'])
def summarize_pdf_route():
    if 'pdf_file' not in request.files:
        return "No file uploaded.", 400
    pdf_file = request.files['pdf_file']
    summary = summarize_pdf(pdf_file)
    return render_template('summarize.html', summary=summary)

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']
    if file.filename == '':
        return "Empty filename", 400

    # Save temp & ingest
    pdf_path = f"uploads/{file.filename}"
    file.save(pdf_path)
    chunks = add_pdf_to_vector_db(pdf_path)

    return f"Uploaded and indexed {chunks} chunks from {file.filename}"

@app.route("/history")
def history():
    sessions = db_session.query(ChatSession).all()
    return render_template("history.html", sessions=sessions)

@app.route("/history/<session_id>")
def view_history(session_id):
    conversation = db_session.query(ChatSession).filter_by(session_id=session_id).first()
    messages = conversation.messages if conversation else []
    return render_template("view_history.html", messages=messages)

# ✅ Recommended pattern for local dev on Windows
# Keeps debug, disables reloader to avoid extra threads

if __name__ == '__main__':
    app.run(
        debug=True,          # Keep debug on for now
        use_reloader=False,  # Disable auto-reloader to avoid WinError 10038
        threaded=True        # Still allow multiple requests
    )
# Flask app for AI chatbot and PDF summarization
# To run this app, save it as app.py and run with `python app.py`
# Ensure you have Flask installed: `pip install Flask`
# Ensure you have the necessary templates in a 'templates' directory
# Ensure you have the necessary static files in a 'static' directory if needed
# Ensure you have the chatbot_logic.py and summarization_logic.py files with the necessary functions defined
# You can then access the app at http://localhost:5000
