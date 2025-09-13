import os
import streamlit as st
from dotenv import load_dotenv
from agents.supervisor import Supervisor
from fpdf import FPDF

# Load environment variables first
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("GOOGLE_API_KEY not found. Add it to your .env file.")
    st.stop()

# Question Bank
CURATED_QUESTIONS = {
    "basic": [
        "What is the difference between relative and absolute references in Excel?",
        "How do you remove duplicate rows from a dataset?",
        "How do you create a simple bar chart?",
    ],
    "intermediate": [
        "Explain how VLOOKUP works with an example.",
        "What are Pivot Tables used for in Excel?",
        "How would you apply conditional formatting to highlight values greater than 100?",
    ],
    "advanced": [
        "Explain array formulas and how dynamic arrays improve analysis.",
        "How would you use Solver to optimize a business scenario?",
        "How do you protect specific cells in a shared Excel sheet?",
    ],
}

# Supervisor (multi-agent orchestrator)
supervisor = Supervisor(CURATED_QUESTIONS)

st.set_page_config(page_title="Excel Mock Interviewer", layout="wide")

st.title("🧑‍💻 Excel Mock Interviewer")
st.write(
    "An AI-powered multi-agent system that simulates an Excel interview, evaluates your answers, and gives detailed feedback."
)

st.sidebar.header("Interview Settings")
num_basic = st.sidebar.slider("Basic Questions", 0, 3, 1)
num_inter = st.sidebar.slider("Intermediate Questions", 0, 3, 1)
num_adv = st.sidebar.slider("Advanced Questions", 0, 3, 1)

if "stage" not in st.session_state:
    st.session_state.stage = "welcome"
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "evaluations" not in st.session_state:
    st.session_state.evaluations = []
if "summary" not in st.session_state:
    st.session_state.summary = ""

if st.session_state.stage == "welcome":
    st.info("Click below to begin your interview.")
    if st.button("Start Interview"):
        st.session_state.questions = supervisor.interviewer.get_questions(
            n_basic=num_basic, n_inter=num_inter, n_adv=num_adv
        )
        st.session_state.answers = []
        st.session_state.stage = "asking"
        st.rerun()

elif st.session_state.stage == "asking":
    q_index = len(st.session_state.answers)
    if q_index < len(st.session_state.questions):
        question = st.session_state.questions[q_index]
        st.subheader(f"Question {q_index+1}/{len(st.session_state.questions)}")
        st.write(question)
        answer = st.text_area("Your Answer", key=f"ans_{q_index}")
        if st.button("Submit Answer"):
            st.session_state.answers.append({"question": question, "answer": answer})
            st.rerun()
    else:
        st.session_state.stage = "evaluating"
        st.rerun()

elif st.session_state.stage == "evaluating":
    st.subheader("Evaluating your answers...")
    with st.spinner("Please wait while I review your responses..."):
        evaluations, summary = supervisor.run_interview(st.session_state.answers)
        st.session_state.evaluations = evaluations
        st.session_state.summary = summary
        st.session_state.stage = "results"
        st.rerun()

elif st.session_state.stage == "results":
    st.success("Interview complete! Here are your results:")

    scores = [
        int(ev.get("score", 0))
        for ev in st.session_state.evaluations
        if ev.get("score", "").isdigit()
    ]
    avg_score = sum(scores) / len(scores) if scores else 0
    st.metric("Average Score", f"{avg_score:.1f}/5")

    for i, (qa, ev) in enumerate(
        zip(st.session_state.answers, st.session_state.evaluations), 1
    ):
        score = int(ev.get("score", 0)) if ev.get("score", "0").isdigit() else 0
        color = "green" if score >= 4 else "orange" if score == 3 else "red"

        st.markdown(f"**Q{i}. {qa['question']}**")
        st.markdown(f"- **Your Answer:** {qa['answer']}")
        st.markdown(
            f"- **Score:** <span style='color:{color}; font-weight:bold'>{score}</span>",
            unsafe_allow_html=True,
        )
        st.markdown(f"- **Justification:** {ev.get('justification', '')}")
        st.markdown(f"- **Explanation:** {ev.get('explanation', '')}")
        st.markdown(f"- **Tip:** {ev.get('tip', '')}")

    st.subheader("📄 Final Performance Summary")
    st.write(st.session_state.summary)

    def create_pdf_report():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Excel Mock Interview Report Card", ln=True, align="C")
        pdf.ln(10)

        for i, (qa, ev) in enumerate(
            zip(st.session_state.answers, st.session_state.evaluations), 1
        ):
            pdf.multi_cell(0, 10, txt=f"Q{i}: {qa['question']}")
            pdf.multi_cell(0, 10, txt=f"Answer: {qa['answer']}")
            pdf.multi_cell(0, 10, txt=f"Score: {ev.get('score', 'N/A')}")
            pdf.multi_cell(0, 10, txt=f"Justification: {ev.get('justification', '')}")
            pdf.multi_cell(0, 10, txt=f"Explanation: {ev.get('explanation', '')}")
            pdf.multi_cell(0, 10, txt=f"Tip: {ev.get('tip', '')}")
            pdf.ln(5)

        pdf.multi_cell(0, 10, txt="Final Summary:")
        pdf.multi_cell(0, 10, txt=st.session_state.summary)

        return pdf.output(dest="S").encode("latin-1")

    st.download_button(
        "📥 Download Report Card (PDF)",
        data=create_pdf_report(),
        file_name="report_card.pdf",
        mime="application/pdf",
    )

    if st.button("Restart Interview"):
        st.session_state.stage = "welcome"
        st.rerun()
