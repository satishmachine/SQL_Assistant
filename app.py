# SQL-Powered Data Retrieval Assistant
import os
import html
import time
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import plotly.express as px

from config import DATABASE_URI, EURI_API_KEY, EURI_BASE_URL, MODEL_NAME
from utills import get_db_schema, get_db_tables_dict, call_euri_llm, execute_sql

# Try to import speech recognition
try:
    import speech_recognition as sr
    import pyaudio
    VOICE_AVAILABLE = True
except (ImportError, OSError, AttributeError):
    VOICE_AVAILABLE = False

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="SQL Assistant Pro | Intelligent Data Exploration",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling (Dark Glassmorphic Theme & Modern Typography)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    code, pre, [class*="stCode"] {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main background & container polish */
    .stApp {
        background: radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 85% 85%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
                    #0b0f19;
    }

    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 2rem !important;
    }

    /* Compact Top Header */
    .compact-header {
        margin-bottom: 0.85rem;
        padding-bottom: 0.45rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .compact-header-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: -0.01em;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .compact-header-sub {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 2px;
        line-height: 1.4;
    }

    /* Metric & Stats Cards */
    .stats-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .stats-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }
    .stats-title {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stats-val {
        font-size: 1.35rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-top: 0.25rem;
    }

    /* Quick Prompt Chips */
    .chip-btn {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: #cbd5e1;
        font-size: 0.85rem;
        padding: 6px 12px;
        cursor: pointer;
        transition: all 0.2s;
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0.55rem 1.25rem;
        transition: all 0.2s ease-in-out;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px -6px rgba(99, 102, 241, 0.5);
    }
    
    /* Primary Action Buttons */
    button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        border: none !important;
        color: #ffffff !important;
    }

    /* Sidebar Tweaks */
    section[data-testid="stSidebar"] {
        background-color: #0e1422;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Pill Badges */
    .col-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        background: rgba(99, 102, 241, 0.12);
        color: #c7d2fe;
        border: 1px solid rgba(99, 102, 241, 0.25);
        margin: 2px;
        font-family: 'JetBrains Mono', monospace;
    }

    .table-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        background: rgba(99, 102, 241, 0.14);
        color: #e2e8f0;
        border: 1px solid rgba(99, 102, 241, 0.3);
        font-family: 'JetBrains Mono', monospace;
    }

    /* Table & Container Polish */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Custom Alert Boxes */
    .stAlert {
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# State Initialization
# ---------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "last_sql" not in st.session_state:
    st.session_state.last_sql = ""
if "last_df" not in st.session_state:
    st.session_state.last_df = None
if "last_exec_time" not in st.session_state:
    st.session_state.last_exec_time = 0.0
if "input_query_text" not in st.session_state:
    st.session_state.input_query_text = ""
if "input_key_id" not in st.session_state:
    st.session_state.input_key_id = 0
if "auto_execute" not in st.session_state:
    st.session_state.auto_execute = False
if "db_connected" not in st.session_state:
    st.session_state.db_connected = False
if "schema_cache" not in st.session_state:
    st.session_state.schema_cache = None
if "tables_cache" not in st.session_state:
    st.session_state.tables_cache = None

# Language Mapping for Speech Recognition
LANGUAGE_MAP = {
    "🇺🇸 English (US)": "en-US",
    "🇮🇳 Hindi (India)": "hi-IN",
    "🇪🇸 Spanish": "es-ES",
    "🇫🇷 French": "fr-FR",
    "🇩🇪 German": "de-DE",
    "🇨🇳 Chinese": "zh-CN",
    "🇸🇦 Arabic": "ar-SA",
    "🇧🇩 Bengali": "bn-IN",
    "🇯🇵 Japanese": "ja-JP",
    "🇮🇳 Tamil": "ta-IN",
    "🇮🇳 Telugu": "te-IN",
    "🇮🇳 Marathi": "mr-IN"
}

# ---------------------------------------------------------
# Database Engine Initialization & Schema Caching
# ---------------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_engine(uri: str):
    if not uri:
        return None
    return create_engine(uri)

engine = None
db_error_msg = None

if DATABASE_URI:
    try:
        engine = get_engine(DATABASE_URI)
        # Test connection
        with engine.connect() as conn:
            pass
        st.session_state.db_connected = True
        
        # Cache schema
        if st.session_state.schema_cache is None or st.session_state.tables_cache is None:
            st.session_state.schema_cache = get_db_schema(engine)
            st.session_state.tables_cache = get_db_tables_dict(engine)
    except Exception as e:
        st.session_state.db_connected = False
        db_error_msg = str(e)
else:
    st.session_state.db_connected = False
    db_error_msg = "DATABASE_URI is not set in environment or .env file."

# Mask DB URI for safe UI display
def mask_uri(uri: str) -> str:
    if not uri:
        return "Not Configured"
    try:
        parts = uri.split("@")
        if len(parts) > 1:
            proto_user = parts[0].split("://")
            proto = proto_user[0]
            host_db = parts[1].split("?")[0]
            return f"{proto}://***:***@{host_db}"
        return uri.split("?")[0]
    except Exception:
        return "Configured"

# ---------------------------------------------------------
# Sidebar Layout
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:1rem;">
            <div style="background:linear-gradient(135deg, #4f46e5, #7c3aed); width:38px; height:38px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.3rem;">⚡</div>
            <div>
                <h3 style="margin:0; font-size:1.15rem; font-weight:700; color:#f8fafc;">SQL Assistant</h3>
                <span style="font-size:0.75rem; color:#818cf8; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">Enterprise AI Engine</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 1. Database Connection Status Card (Compact)
    masked_db = html.escape(mask_uri(DATABASE_URI))
    if st.session_state.db_connected:
        st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.22); border-radius: 8px; padding: 6px 10px; margin-bottom: 0.65rem;">
                <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px;">
                    <span style="font-size: 0.72rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.04em;">🔌 DB Connection</span>
                    <span style="display: inline-flex; align-items: center; gap: 4px; font-size: 0.68rem; font-weight: 600; color: #34d399; background: rgba(16, 185, 129, 0.15); padding: 1px 7px; border-radius: 9999px;">
                        <span style="width: 5px; height: 5px; border-radius: 50%; background: #10b981; display: inline-block;"></span> Connected
                    </span>
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #64748b; margin-top: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{masked_db}">
                    {masked_db}
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        escaped_err = html.escape(str(db_error_msg))
        st.markdown(f"""
            <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.22); border-radius: 8px; padding: 6px 10px; margin-bottom: 0.65rem;">
                <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px;">
                    <span style="font-size: 0.72rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.04em;">🔌 DB Connection</span>
                    <span style="display: inline-flex; align-items: center; gap: 4px; font-size: 0.68rem; font-weight: 600; color: #f87171; background: rgba(239, 68, 68, 0.15); padding: 1px 7px; border-radius: 9999px;">
                        <span style="width: 5px; height: 5px; border-radius: 50%; background: #ef4444; display: inline-block;"></span> Disconnected
                    </span>
                </div>
                <div style="font-size: 0.68rem; color: #f87171; margin-top: 3px; word-break: break-all;" title="{escaped_err}">
                    {escaped_err}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 2. Voice Input Configuration
    st.markdown("---")
    st.markdown("##### 🎙️ Voice & Language")
    selected_lang_name = st.selectbox(
        "Voice Language",
        list(LANGUAGE_MAP.keys()),
        index=0,
        help="Select spoken language for Google Speech Recognition"
    )
    language_code = LANGUAGE_MAP[selected_lang_name]

    if VOICE_AVAILABLE:
        st.caption("✅ Microphone hardware interface detected.")
    else:
        st.caption("ℹ️ Cloud/Headless environment (Text input mode active).")

    # 3. Database Schema Inspector
    st.markdown("---")
    st.markdown("##### 🗄️ Database Tables")
    if st.session_state.tables_cache:
        tables = st.session_state.tables_cache
        st.caption(f"Reflected **{len(tables)} tables** from database.")
        for table_name, cols in tables.items():
            with st.expander(f"📁 **{table_name}** ({len(cols)} cols)"):
                col_badges = "".join([f"<span class='col-badge'>{col_name}</span>" for col_name, _ in cols])
                st.markdown(f"<div style='margin-bottom:8px;'>{col_badges}</div>", unsafe_allow_html=True)
                if st.button(f"Preview `{table_name}`", key=f"prev_{table_name}", width="stretch"):
                    preview_text = f"Show the first 5 records from {table_name}"
                    st.session_state.input_query_text = preview_text
                    st.session_state.input_key_id += 1
                    st.session_state.auto_execute = True
                    st.rerun()
    else:
        st.caption("No tables loaded yet.")



# ---------------------------------------------------------
# App Header Logo
# ---------------------------------------------------------
logo_file = "assets/logo.png" if os.path.exists("assets/logo.png") else ("logo.png" if os.path.exists("logo.png") else None)
if logo_file:
    col_l1, col_l2, col_l3 = st.columns([0.45, 2.5, 0.45])
    with col_l2:
        st.image(logo_file, width="stretch")
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# Overview Metrics Cards
col_m1, col_m2 = st.columns([0.65, 2.85])
with col_m1:
    status_icon = "🟢 Active" if st.session_state.db_connected else "🔴 Offline"
    st.markdown(f"""
        <div class="stats-card" style="padding: 0.6rem 0.9rem;">
            <div class="stats-title" style="font-size: 0.72rem;">Database Status</div>
            <div style="font-size: 0.95rem; font-weight: 700; color: #f1f5f9; margin-top: 4px;">{status_icon}</div>
        </div>
    """, unsafe_allow_html=True)

with col_m2:
    table_names = list(st.session_state.tables_cache.keys()) if st.session_state.tables_cache else []
    if table_names:
        table_pills = "".join([f"<span class='table-pill'>📁 {t}</span>" for t in table_names])
    else:
        table_pills = "<span style='font-size:0.85rem; color:#94a3b8;'>No tables detected</span>"
    st.markdown(f"""
        <div class="stats-card" style="padding: 0.6rem 0.9rem;">
            <div class="stats-title" style="font-size: 0.72rem;">Connected Tables ({len(table_names)})</div>
            <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:5px;">
                {table_pills}
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Query Input Console
# ---------------------------------------------------------
st.markdown("### 💬 Ask Your Question")

input_container = st.container()
with input_container:
    col_input, col_voice = st.columns([5, 1])

    with col_input:
        query_input = st.text_input(
            "Enter question",
            value=st.session_state.input_query_text,
            placeholder="e.g., 'What are the top 5 highest value orders?' or 'Show total sales by category'",
            label_visibility="collapsed",
            key=f"user_query_input_{st.session_state.input_key_id}"
        )

    with col_voice:
        voice_clicked = False
        if VOICE_AVAILABLE:
            voice_clicked = st.button("🎤 Speak", width="stretch", help="Record query with microphone")
        else:
            st.button("🎤 Voice", disabled=True, width="stretch", help="Voice not available on headless environments")

# Voice Recognition Handler
if voice_clicked and VOICE_AVAILABLE:
    recognizer = sr.Recognizer()
    try:
        with st.spinner(f"🎙️ Listening in {selected_lang_name}... Speak into your microphone."):
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.6)
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=12)
            transcribed_text = recognizer.recognize_google(audio, language=language_code)
        
        transcribed_text = (transcribed_text or "").strip()
        if transcribed_text:
            st.session_state.input_query_text = transcribed_text
            st.session_state.input_key_id += 1
            st.session_state.auto_execute = True
            st.rerun()
        else:
            st.warning("⚠️ No words were detected. Please try speaking again.")
    except sr.WaitTimeoutError:
        st.warning("⏱️ Listening timed out. No speech was detected. Please try again.")
    except sr.UnknownValueError:
        st.error("Sorry, could not understand the speech. Please try speaking again or type your query.")
    except (OSError, AttributeError) as e:
        st.warning(f"⚠️ Microphone hardware or driver issue: {e}")
    except sr.RequestError as e:
        st.error(f"Speech recognition service error: {e}")

col_act1, col_act2, _ = st.columns([1.5, 1.5, 5])
with col_act1:
    submit_button = st.button("🚀 Generate & Run SQL", type="primary", width="stretch")
with col_act2:
    if st.button("🧹 Clear Input", width="stretch"):
        st.session_state.input_query_text = ""
        st.session_state.input_key_id += 1
        st.session_state.last_df = None
        st.session_state.last_sql = ""
        st.rerun()

# ---------------------------------------------------------
# Execution Pipeline
# ---------------------------------------------------------
active_query = query_input.strip() if query_input else ""

should_execute = (submit_button or st.session_state.get("auto_execute", False)) and bool(active_query)
if st.session_state.get("auto_execute", False):
    st.session_state.auto_execute = False

if should_execute:
    if not st.session_state.db_connected or not engine:
        st.error("❌ Cannot execute query: Database is disconnected. Please verify DATABASE_URI in `.env`.")
        st.stop()

    if not EURI_API_KEY:
        st.error("❌ Cannot execute query: EURI_API_KEY is not configured in `.env`.")
        st.stop()

    start_time = time.time()
    schema_str = st.session_state.schema_cache or get_db_schema(engine)

    # 1. Read Prompt Template
    template_path = "prompt_template.txt"
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    else:
        template = "Schema:\n{schema}\n\nQuestion:\n{question}\n\nReturn only valid SQL query."

    full_prompt = template.format(schema=schema_str, question=active_query)

    # 2. Call EURI LLM
    with st.spinner("🧠 Synthesizing SQL via EURI LLM..."):
        try:
            generated_sql = call_euri_llm(full_prompt)
        except Exception as e:
            st.error(f"Error communicating with EURI LLM API: {e}")
            st.stop()

    # 3. Execute SQL Query
    with st.spinner("⚡ Executing SQL against database..."):
        try:
            results, columns = execute_sql(engine, generated_sql)
            exec_duration = time.time() - start_time
            
            df = pd.DataFrame(results, columns=columns)
            st.session_state.last_query = active_query
            st.session_state.last_sql = generated_sql
            st.session_state.last_df = df
            st.session_state.last_exec_time = exec_duration

            # Append to history
            st.session_state.history.append({
                "query": active_query,
                "sql": generated_sql,
                "rows": len(df),
                "time": exec_duration,
                "timestamp": time.strftime("%H:%M:%S")
            })

        except Exception as e:
            st.session_state.last_sql = generated_sql
            st.session_state.last_df = None
            st.error(f"❌ SQL Execution Error:\n\n```\n{e}\n```")
            with st.expander("View Generated SQL that caused error"):
                st.code(generated_sql, language="sql")
            st.stop()

# ---------------------------------------------------------
# Results Deck & Visualization Studio
# ---------------------------------------------------------
if st.session_state.last_df is not None:
    df = st.session_state.last_df
    sql = st.session_state.last_sql
    
    st.markdown("---")
    st.markdown(f"### 📋 Results for: *\"{st.session_state.last_query}\"*")

    # Quick Summary Metrics
    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    with col_r1:
        st.metric("Total Records", f"{len(df):,}")
    with col_r2:
        st.metric("Columns Returned", len(df.columns))
    with col_r3:
        st.metric("Execution Time", f"{st.session_state.last_exec_time:.2f}s")
    with col_r4:
        # Download CSV
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export CSV",
            data=csv_bytes,
            file_name=f"query_result_{int(time.time())}.csv",
            mime="text/csv",
            width="stretch"
        )

    # Multi-tab view
    tab_data, tab_charts, tab_sql, tab_history = st.tabs([
        "📊 Data Grid",
        "📈 Visualizations",
        "💻 Generated SQL",
        "📜 Query History"
    ])

    # Tab 1: Data Grid
    with tab_data:
        if len(df) > 0:
            st.dataframe(df, width="stretch", height=380)
        else:
            st.info("Query executed successfully, but returned 0 records.")

    # Tab 2: Visualizations Studio
    with tab_charts:
        if len(df) == 0:
            st.info("No data available to plot.")
        elif len(df.columns) < 1:
            st.warning("Insufficient columns to generate a chart.")
        else:
            st.markdown("##### 🎨 Chart Designer")
            chart_col1, chart_col2, chart_col3 = st.columns(3)

            with chart_col1:
                chart_type = st.selectbox(
                    "Chart Type",
                    ["Bar Chart", "Line Chart", "Area Chart", "Scatter Plot", "Pie Chart", "Histogram"]
                )

            # Auto-detect numeric and categorical columns
            numeric_cols = list(df.select_dtypes(include=['number']).columns)
            non_numeric_cols = [c for c in df.columns if c not in numeric_cols]

            default_x = non_numeric_cols[0] if non_numeric_cols else df.columns[0]
            default_y = numeric_cols[0] if numeric_cols else (df.columns[1] if len(df.columns) > 1 else df.columns[0])

            with chart_col2:
                x_axis = st.selectbox("X-Axis (Dimension)", df.columns, index=df.columns.get_loc(default_x))

            with chart_col3:
                y_axis = st.selectbox("Y-Axis (Measure)", df.columns, index=df.columns.get_loc(default_y))

            # Modern Plotly Dark Theme
            colorway = ["#6366f1", "#ec4899", "#8b5cf6", "#10b981", "#f59e0b", "#3b82f6"]

            try:
                fig = None
                if chart_type == "Bar Chart":
                    fig = px.bar(
                        df, x=x_axis, y=y_axis,
                        title=f"{y_axis} by {x_axis}",
                        template="plotly_dark",
                        color_discrete_sequence=colorway
                    )
                elif chart_type == "Line Chart":
                    fig = px.line(
                        df, x=x_axis, y=y_axis,
                        title=f"{y_axis} Trend over {x_axis}",
                        template="plotly_dark",
                        markers=True,
                        color_discrete_sequence=colorway
                    )
                elif chart_type == "Area Chart":
                    fig = px.area(
                        df, x=x_axis, y=y_axis,
                        title=f"{y_axis} Distribution across {x_axis}",
                        template="plotly_dark",
                        color_discrete_sequence=colorway
                    )
                elif chart_type == "Scatter Plot":
                    fig = px.scatter(
                        df, x=x_axis, y=y_axis,
                        title=f"{x_axis} vs {y_axis}",
                        template="plotly_dark",
                        size_max=15,
                        color_discrete_sequence=colorway
                    )
                elif chart_type == "Pie Chart":
                    fig = px.pie(
                        df, names=x_axis, values=y_axis if y_axis in numeric_cols else None,
                        title=f"Proportion of {x_axis}",
                        template="plotly_dark",
                        color_discrete_sequence=colorway
                    )
                elif chart_type == "Histogram":
                    fig = px.histogram(
                        df, x=x_axis,
                        title=f"Distribution of {x_axis}",
                        template="plotly_dark",
                        color_discrete_sequence=colorway
                    )

                if fig:
                    fig.update_layout(
                        paper_bgcolor="rgba(15, 23, 42, 0.4)",
                        plot_bgcolor="rgba(15, 23, 42, 0.2)",
                        font=dict(family="Plus Jakarta Sans", color="#e2e8f0"),
                        margin=dict(l=40, r=40, t=50, b=40),
                        hoverlabel=dict(bgcolor="#1e293b", font_size=13, font_family="Plus Jakarta Sans")
                    )
                    st.plotly_chart(fig, width="stretch")

            except Exception as chart_err:
                st.warning(f"Unable to render chart with selected columns: {chart_err}")

    # Tab 3: Generated SQL
    with tab_sql:
        st.markdown("##### ⚡ Optimized SQL Query")
        st.code(sql, language="sql")
        
        with st.expander("🔍 Inspect Full Prompt Sent to EURI LLM"):
            st.code(full_prompt if 'full_prompt' in locals() else "Prompt loaded on demand", language="text")

    # Tab 4: Query History
    with tab_history:
        if st.session_state.history:
            st.markdown("##### 📜 Recent Queries This Session")
            for h in reversed(st.session_state.history):
                with st.container():
                    st.markdown(f"""
                        <div style="background:rgba(30, 41, 59, 0.5); border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:12px; margin-bottom:10px;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <b style="color:#f8fafc; font-size:0.95rem;">{h['query']}</b>
                                <span style="font-size:0.75rem; color:#94a3b8;">⏱️ {h['timestamp']} ({h['time']:.2f}s, {h['rows']} rows)</span>
                            </div>
                            <pre style="margin-top:8px; padding:8px; background:rgba(15,23,42,0.8); border-radius:6px; color:#38bdf8; font-size:0.8rem; overflow-x:auto;">{h['sql']}</pre>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No query history recorded yet.")
