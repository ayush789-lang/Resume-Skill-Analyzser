import streamlit as st
import PyPDF2
import re
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Resume Skill Analyzer",
    page_icon="📄",
    layout="centered"
)

# ---------------- TITLE ----------------
st.title("📄 Resume Skill Analyzer")
st.write("Analyze your resume and get job-specific career guidance.")
st.divider()

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

# ---------------- CLEAN TEXT ----------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

# ---------------- SKILL DATABASE ----------------
skill_database = {
    "python": ["python"],
    "java": ["java"],
    "sql": ["sql"],
    "excel": ["excel", "ms excel", "microsoft excel"],
    "pandas": ["pandas"],
    "machine learning": ["machine learning"],
    "html": ["html"],
    "css": ["css"],
    "javascript": ["javascript", "js"],
    "react": ["react"],
    "aws": ["aws"],
    "linux": ["linux"],
    "testing": ["testing", "qa"]
}

# ---------------- JOB ROLES ----------------
job_roles = {
    "Data Analyst": ["python", "sql", "excel", "pandas"],
    "Python Developer": ["python", "sql"],
    "Web Developer": ["html", "css", "javascript"],
    "Full Stack Developer": ["html", "css", "javascript", "react", "python"],
    "Cloud Engineer": ["aws", "linux"],
    "QA / Software Tester": ["testing"]
}

# ---------------- LEARNING GUIDE ----------------
learning_guide = {
    "python": "Learn core Python, OOP concepts, and build small projects.",
    "sql": "Practice SELECT, JOIN, GROUP BY using sample databases.",
    "excel": "Learn formulas, pivot tables, charts, and reports.",
    "pandas": "Practice DataFrames, CSV files, and Kaggle datasets.",
    "html": "Learn HTML tags, forms, and page structure.",
    "css": "Learn layouts, flexbox, grid, and responsive design.",
    "javascript": "Learn DOM manipulation and basic scripting.",
    "react": "Learn components, state, and hooks.",
    "aws": "Learn EC2, S3, IAM basics.",
    "linux": "Practice Linux commands and file system.",
    "testing": "Learn manual testing concepts and test cases."
}

job_role = st.selectbox("Select Target Job Role", list(job_roles.keys()))

# ---------------- MAIN LOGIC ----------------
if uploaded_file:

    with st.spinner("Analyzing resume..."):
        time.sleep(1)

        reader = PyPDF2.PdfReader(uploaded_file)
        resume_text = ""

        for page in reader.pages:
            resume_text += page.extract_text()

        resume_text = clean_text(resume_text)

        detected_skills = []
        for skill, keys in skill_database.items():
            for k in keys:
                if k in resume_text:
                    detected_skills.append(skill)
                    break

        required_skills = job_roles[job_role]
        matched_skills = [s for s in required_skills if s in detected_skills]
        missing_skills = [s for s in required_skills if s not in detected_skills]

        score = int((len(matched_skills) / len(required_skills)) * 100)

    st.success("Resume analysis completed successfully!")
    st.divider()

    # ---------------- MATCHED & MISSING (FIXED DISPLAY) ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Skills")
        if matched_skills:
            for skill in matched_skills:
                st.write(f"✔ {skill}")
        else:
            st.write("No matched skills")

    with col2:
        st.subheader("❌ Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.write(f"✖ {skill}")
        else:
            st.write("No missing skills")

    # ---------------- PROS ----------------
    st.subheader("👍 Pros (Strengths)")
    if matched_skills:
        for skill in matched_skills:
            st.success(f"You already have **{skill}**, which is important for a {job_role} role.")
    else:
        st.warning("No strong skills detected yet.")

    # ---------------- CONS ----------------
    st.subheader("⚠️ Cons (Skill Gaps)")
    if missing_skills:
        for skill in missing_skills:
            st.error(f"You are missing **{skill}**, which reduces job readiness.")
    else:
        st.success("No major skill gaps found.")

    # ---------------- LEARNING ----------------
    st.subheader("📘 What You Should Learn Next")
    if missing_skills:
        for skill in missing_skills:
            st.info(learning_guide.get(skill, f"Start learning {skill}."))
    else:
        st.success("You already meet all required skills!")

    # ---------------- JOB FIT SCORE (LAST) ----------------
    st.divider()
    st.subheader("⭐ Job Fit Score")
    st.progress(score)
    st.write(f"**{score}% Match**")

    if score >= 80:
        st.balloons()
        st.success("Excellent! You are job-ready.")
    elif score >= 50:
        st.warning("Good profile. Improve missing skills.")
    else:
        st.error("Low match. Focus on learning fundamentals.")

# ---------------- CONTACT / FEEDBACK ----------------
st.divider()
st.subheader("📩 Contact / Feedback")

with st.form("feedback_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    feedback = st.text_area("Your Feedback / Query")
    submit = st.form_submit_button("Submit")

    if submit:
        st.success("Thank you! Your feedback has been submitted.")

# ---------------- ABOUT US ----------------
st.divider()
st.subheader("ℹ️ About Us")

st.write("""
Resume Skill Analyzer is a career guidance application designed to help students 
and job seekers understand how well their resume matches different job roles.

🔹 Analyzes resume content  
🔹 Identifies matched and missing skills  
🔹 Provides learning guidance  
🔹 Calculates job-fit score  

Built using **Python and Streamlit** for academic and learning purposes.
""")
