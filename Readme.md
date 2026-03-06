# 🧑‍💻 Excel Mock Interviewer – Multi-Agent LLM System

An AI-powered interview simulator that evaluates Excel knowledge using a **multi-agent architecture powered by Google's Gemini LLM**.

The system simulates a technical interview by generating questions, evaluating responses, and providing detailed feedback — all coordinated by a **Supervisor agent** that orchestrates specialized agents.

Built using **Python, Streamlit, and Gemini API**.

---

# 🚀 Features

- 🤖 Multi-Agent AI System
- 🧠 LLM-Powered Evaluation using Gemini
- 🎯 Adaptive Question Selection
- 📊 Detailed Answer Evaluation
- 📄 Performance Summary
- 🖥 Interactive Streamlit Interface

---

# 🧠 Multi-Agent System Architecture

This project follows a **Supervisor-Agent architecture**, where a central orchestrator manages specialized agents.
User
│
Streamlit UI
│
Supervisor Agent
│
├── Interviewer Agent → Selects interview questions
│
├── Evaluator Agent → Uses Gemini LLM to evaluate answers
│
└── Feedback Agent → Generates final performance summary


### Why Multi-Agent?

Instead of using a single LLM call, responsibilities are separated into **specialized agents**, making the system:

- Modular
- Scalable
- Easier to maintain
- Closer to real-world AI system design

---

# 🤖 Agents in the System

## 1️⃣ Supervisor Agent

The **Supervisor** coordinates the entire interview workflow.

Responsibilities:
- Orchestrates the agents
- Passes answers to the evaluator
- Collects evaluations
- Generates final interview summary

---

## 2️⃣ Interviewer Agent

Responsible for **selecting questions** based on difficulty levels.

Question categories:
- Basic
- Intermediate
- Advanced

Example topics include:
- Excel formulas
- Pivot tables
- Data validation
- Lookup functions
- Excel automation concepts

---

## 3️⃣ Evaluator Agent

Uses **Gemini LLM** to evaluate user answers.

Each answer is scored on a **1-5 scale** with structured feedback.

Example evaluation output:
{
"score": "4",
"justification": "...",
"explanation": "...",
"tip": "..."
}


This allows the system to provide **AI-driven interview feedback** similar to a real interviewer.

---

## 4️⃣ Feedback Agent

After all answers are evaluated, the **Feedback Agent** generates a **final performance summary** highlighting:

- Overall strengths
- Areas for improvement
- Suggested learning directions

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|--------|
| Python | Core logic |
| Streamlit | Interactive UI |
| Google Gemini API | LLM evaluation |
| dotenv | Environment variable management |
| Multi-Agent Architecture | Modular AI system |

---
---

# 🎯 Use Cases

- Excel skill practice
- Interview preparation
- AI-based learning assistants
- Demonstrating multi-agent LLM architectures

---

# 🔮 Future Improvements

- Conversational interview mode
- Voice-based interview interaction
- Adaptive question difficulty
- Interview performance analytics
- Support for other technical domains

---

# 👩‍💻 Author

**Kriti Arora**
