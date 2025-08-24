# Bhagavad Gita Assistant 🌿

An AI-powered life advisor that provides guidance using the timeless wisdom of the **Bhagavad Gita**.  
Built with **LangChain**, **OpenAI**, **FAISS**, and **Gradio**, this project allows users to ask personal or ethical questions and receive concise, practical advice rooted in the Gita’s teachings.  
It also tracks user questions during a session and reports the total count at the end.

---

## ✨ Features
- 📖 Loads and processes the Bhagavad Gita PDF for context-based retrieval.  
- 🧠 Uses **LangChain + OpenAI embeddings** to retrieve relevant verses.  
- 🤖 Provides guidance in simple, everyday language.  
- 🛠️ Integrates tools to:
  - Record user details (email, name, notes).  
  - Record unknown/unanswered questions.  
- 📊 Tracks the number of user questions per session and reports it on exit.  
- 💬 Easy-to-use **Gradio chat interface**.  
- 🔔 Optional Pushover integration for notifications.  

---

## 🛠️ Tech Stack
- [Python](https://www.python.org/)  
- [OpenAI API](https://platform.openai.com/)  
- [LangChain](https://www.langchain.com/)  
- [FAISS](https://faiss.ai/)  
- [Gradio](https://www.gradio.app/)  
- [pypdf](https://pypi.org/project/pypdf/)  
- [Pushover](https://pushover.net/) (optional for notifications)  

---

## 🚀 Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
