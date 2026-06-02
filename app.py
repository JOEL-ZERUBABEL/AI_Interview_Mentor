import streamlit as st
from main import AT_Tutor
import tempfile
import pandas as pd

ai_tutor = AT_Tutor()

st.title("AI Coding Mentor (FAANG Prep)")

menu = st.sidebar.selectbox(
    "Choose Feature",
    [
        "Chat",
        "Resume Analysis",
        "Code Review",
        "Evaluation",
        "Analytics" ])

#CHAT
if menu == "Chat":
    user_input = st.text_area("Ask Anything")
    if st.button("Send"):
        reply = ai_tutor.conversation_memory(user_input)
        st.write(reply)
elif menu == "Resume Analysis":
    file = st.file_uploader(
        "Upload Resume",
        type=["pdf","docx","txt"]
    )

    improvement = st.text_input(
        "Any Improvement Needed?"
    )

    if st.button("Analyze"):
        if file:
            import os
            extension = os.path.splitext(
                file.name
            )[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=extension
            ) as tmp:
                tmp.write(
                    file.read()
                )
                path = tmp.name

            st.write(
                f"Temporary File: {path}"
            )

            result = ai_tutor.resume(
                path,
                improvement
            )

            st.write(result)
        else:
            st.warning(
                "Upload resume first"
            )

#CODE REVIEW
elif menu == "Code Review":
    code = st.text_area("Paste Code")
    if st.button("Review"):
        result = ai_tutor.code_review(code)
        st.write(result)


#EVALUATION 
elif menu == "Evaluation":
    topic = st.selectbox(
        "Topic",
        ["Array", "LinkedList", "Tree", "Graph", "DP"]
    )

    if st.button("Generate Question"):
        question = ai_tutor.generate_question(topic)
        st.session_state["question"] = question

    if "question" in st.session_state:
        st.subheader("Question")
        st.write(st.session_state["question"])
        answer = st.text_area("Your Answer")

        if st.button("Evaluate"):

            result = ai_tutor.evaluation(st.session_state["question"], answer)

            st.subheader("Evaluation Result")
            st.write(f"Technical: {result.get('technical', 0)}")
            st.write(f"Communication: {result.get('communication', 0)}")
            st.write(f"Optimization: {result.get('optimization', 0)}")
            st.write(f"Strengths: {result.get('strengths', '')}")
            st.write(f"Weaknesses: {result.get('weaknesses', '')}")
            st.write(f"Suggestions: {result.get('suggestions', '')}")


elif menu == "Analytics":
    st.subheader("Performance Dashboard")
    # Raw data
    data = ai_tutor.analytics
    st.write("Raw Data:", data)

    # Averages
    scores = ai_tutor.calculate_score(
        technical=data["technical"][-1] if data["technical"] else 0,
        communication=data["communication"][-1] if data["communication"] else 0,
        optimization=data["optimization"][-1] if data["optimization"] else 0
    )

    st.metric("Technical Avg", scores["technical"])
    st.metric("Communication Avg", scores["communication"])
    st.metric("Optimization Avg", scores["optimization"])
    st.metric("Overall Score", scores["overall"])

elif menu == "Analytics":
    st.subheader("Performance Dashboard")
    data = ai_tutor.analytics
    df = pd.DataFrame(data)
    st.line_chart(df)  