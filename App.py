# moral_world.py
import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv(override=True)

# ----------------------
# Helper functions / tools
# ----------------------
def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )

def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

# JSON schema for tools
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if provided"},
            "notes": {"type": "string", "description": "Additional context about the conversation"}
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Record any question that couldn't be answered",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"}
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json}
]

# ----------------------
# Moral_world Class
# ----------------------
class Moral_world:
    def __init__(self):
        self.openai = OpenAI()
        self.name = "Bhagavad Gita Assistant"
        self.question_count = 0

        # 1. Load the PDF
        reader = PdfReader("Source/The Bhagavad Gita.pdf")
        self.Geta_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.Geta_text += text

        # 2. Split into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(self.Geta_text)

        # 3. Create embeddings + FAISS vectorstore
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorstore = FAISS.from_texts(chunks, embeddings)

        # Optional assistant summary
        self.summary = "This assistant uses the Bhagavad Gita’s wisdom to guide humans in life decisions."

    # Retrieve relevant Gita context
    def retrieve_context(self, query, k=3):
        docs = self.vectorstore.similarity_search(query, k=k)
        return "\n\n".join([d.page_content for d in docs])

    # Handle tool calls
    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })
        return results

    # System prompt for OpenAI
    def system_prompt(self, context=""):
        return f"""
You are {self.name}, the Bhagavad Gita Advisor. 
You provide guidance using the wisdom of the Bhagavad Gita in a simple and easy-to-understand way.

Instructions:
- Choose one course of action per life situation.
- Explain briefly why it's better.
- Give a simple example.
- Mention what could go wrong if the other option is chosen.
- Suggest one practical coping method.
- Keep responses concise (max 4–5 sentences).
- If unsure, use the `record_unknown_question` tool.

Here is relevant context from the Bhagavad Gita:\n{context}\n
"""

    # Chat interface for Gradio
    def chat(self, message, history):
        self.question_count += 1
        context = self.retrieve_context(message)
        messages = [{"role": "system", "content": self.system_prompt(context)}] \
                   + history + [{"role": "user", "content": message}]

        done = False
        while not done:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools
            )
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True

        return response.choices[0].message.content
