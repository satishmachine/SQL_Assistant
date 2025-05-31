# my experiment for the sql assistent
import streamlit as st
import speech_recognition as sr
from sqlalchemy import create_engine
from config import DATABASE_URI
from utills import get_db_schema, call_euri_llm, execute_sql
import plotly.express as px

st.set_page_config(page_title="SQL Assistant", layout="wide")
st.title("🧠 SQL-Powered Data Retrieval Assistant")

# ----------------------------
# Step 1: Choose Input Language
# ----------------------------
st.subheader("🌐 Choose Language for Speech Recognition")
language_map = {
    "English (US)": "en-US",
    "Hindi (India)": "hi-IN",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Chinese (Mandarin)": "zh-CN",
    "Arabic": "ar-SA",
    "Bengali": "bn-IN",
    "Japanese": "ja-JP",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Marathi": "mr-IN"
}
selected_language = st.selectbox("Choose a language", list(language_map.keys()))
language_code = language_map[selected_language]

# ----------------------------
# Step 2: Speech Input
# ----------------------------
st.subheader("🎙️ Speak Your SQL Query")
nl_query = ""
if st.button("🎤 Start Listening"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info(f"Listening in {selected_language}... Speak now.")
        audio = recognizer.listen(source, timeout=6)

    try:
        nl_query = recognizer.recognize_google(audio, language=language_code)
        st.success(f"You said: {nl_query}")
    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand the audio.")
    except sr.RequestError as e:
        st.error(f"Speech Recognition API error: {e}")
else:
    nl_query = st.text_input("Or type your question here:")

# ----------------------------
# Step 3: Process Natural Language Query
# ----------------------------
if nl_query:
    engine = create_engine(DATABASE_URI)
    schema = get_db_schema(engine)

    with open("prompt_template.txt") as f:
        template = f.read()
    prompt = template.format(schema=schema, question=nl_query)

    with st.spinner("🧠 Generating SQL using EURI LLM..."):
        sql_query = call_euri_llm(prompt)

    st.code(sql_query, language="sql")

    try:
        results, columns = execute_sql(engine, sql_query)
        if results:
            st.dataframe(results, use_container_width=True)

            # ----------------------------
            # Step 4: Data Visualization
            # ----------------------------
            st.subheader("📊 Data Visualization")

            # Create a DataFrame for visualization
            import pandas as pd
            df = pd.DataFrame(results, columns=columns)

            # Allow user to select visualization type
            visualization_type = st.selectbox(
                "Choose a visualization type",
                ["Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot"]
            )

            # Create and display the visualization
            if visualization_type == "Bar Chart":
                x_col = st.selectbox("Select X-axis column", df.columns)
                y_col = st.selectbox("Select Y-axis column", df.columns)
                fig = px.bar(df, x=x_col, y=y_col, title=f"Bar Chart: {x_col} vs {y_col}")
                st.plotly_chart(fig, use_container_width=True)
            elif visualization_type == "Line Chart":
                x_col = st.selectbox("Select X-axis column", df.columns)
                y_col = st.selectbox("Select Y-axis column", df.columns)
                fig = px.line(df, x=x_col, y=y_col, title=f"Line Chart: {x_col} vs {y_col}")
                st.plotly_chart(fig, use_container_width=True)
            elif visualization_type == "Pie Chart":
                value_col = st.selectbox("Select value column", df.columns)
                name_col = st.selectbox("Select name column", df.columns)
                fig = px.pie(df, values=value_col, names=name_col, title=f"Pie Chart: {value_col}")
                st.plotly_chart(fig, use_container_width=True)
            elif visualization_type == "Scatter Plot":
                x_col = st.selectbox("Select X-axis column", df.columns)
                y_col = st.selectbox("Select Y-axis column", df.columns)
                fig = px.scatter(df, x=x_col, y=y_col, title=f"Scatter Plot: {x_col} vs {y_col}")
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Query executed successfully. No data returned.")
    except Exception as e:
        st.error(f"Error running query: {e}")
