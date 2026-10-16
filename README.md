# 🧠 SQL-Powered Data Retrieval Assistant Pro

A multilingual, voice-enabled intelligent SQL assistant that converts natural language questions into accurate SQL queries using the **EURI LLM API** (via the OpenAI SDK), automatically executes them against your database, and presents interactive results and data visualizations — all through a modern, responsive **Streamlit** dashboard.

---

## 🌟 Key Features

| Feature | Description |
|---|---|
| 🎙️ **Multilingual Voice Input & Auto-Execution** | Speak queries in 12+ languages (Google Speech Recognition + PyAudio). Spoken questions are transcribed and **automatically executed** with zero extra clicks. |
| 🤖 **Natural Language → SQL Synthesis** | Converts conversational questions into precise SQL queries using EURI LLM (`gpt-4.1-mini`) guided by the database schema. |
| ⚡ **Instant 1-Click Table Previews** | Browse tables and column schemas from the sidebar, and preview the first 5 records with one click (auto-executed). |
| 📊 **Interactive Visualizations Studio** | Plot query results on the fly with Plotly Express (Bar, Line, Area, Scatter, Pie, and Histogram) with auto-detected dimensions and measures. |
| 📋 **Comprehensive Results Deck** | View interactive data grids, summary metrics (row count, column count, query runtime), inspect generated SQL, and export results to CSV. |
| 📜 **Session Query History** | Tracks all queries run during the session, including SQL statements, execution duration, and record counts. |
| 🗄️ **Multi-Database Compatibility** | Connects to PostgreSQL (Neon, Supabase, AWS RDS), MySQL, SQLite, and SQL Server via SQLAlchemy 2.0. |
| 🔐 **Secure Credential Management** | Centralized, git-ignored `.env` file for API keys and database credentials with automatic connection string normalization. |

---

## 🛠️ Tech Stack

- **Web Dashboard**: [Streamlit](https://streamlit.io/)
- **LLM Engine**: [EURI AI](https://euron.one) (`https://api.euron.one/api/v1/euri`) via [OpenAI Python SDK](https://github.com/openai/openai-python)
- **Model**: `gpt-4.1-mini`
- **Database Engine / ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Database Drivers**:
  - PostgreSQL: `psycopg2-binary`
  - MySQL: `pymysql`
  - SQLite: Built-in Python driver
- **Speech Recognition**: [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) + [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)
- **Data Visualization & Processing**: [Plotly Express](https://plotly.com/python/plotly-express/) & [Pandas](https://pandas.pydata.org/)
- **Configuration & Environment**: `python-dotenv`, `uv` / `pip`

---

## 📁 Project Structure

```
SQL_Assistant/
├── .devcontainer/             # Dev container settings for VS Code / Codespaces
├── assets/                    # Static assets (branding, icons, logos)
├── app.py                     # Main Streamlit web application (UI, voice handler & execution)
├── config.py                  # Environment config, model settings & URI normalization
├── utills.py                  # Core utility functions: schema reflection, EURI LLM call & SQL runner
├── prompt_template.txt        # Prompt template providing DB schema & user question to the LLM
├── main.py                    # CLI entry point script
├── logo.png                   # Header logo for the dashboard
├── .env.example               # Template for required environment variables
├── .env                       # 🔒 Local secrets & credentials (git-ignored)
├── requirements.txt           # Standard pip dependency specification
├── pyproject.toml             # Project metadata and dependencies (PEP 518 / uv compatible)
├── uv.lock                    # Deterministic lockfile for uv package manager
├── packages.txt               # System-level dependencies for Linux / cloud environments (portaudio)
├── .gitignore                 # Excludes .env, .venv, caches, query exports, etc.
├── LICENSE                    # MIT License
└── README.md                  # Project documentation
```

---

## 📋 Prerequisites

- **Python 3.10+** (Python 3.11, 3.12, 3.13 supported)
- An accessible **SQL database** (PostgreSQL, MySQL, SQLite, etc.)
- A valid **EURI API key** from [euron.one](https://euron.one)
- A working **microphone** (optional; required only for voice queries)

---

## 📦 Installation & Setup

### 1. Clone or Open the Repository

```bash
cd SQL_Assistant
```

### 2. Create & Activate a Virtual Environment

**Using `uv` (Fastest):**
```bash
uv venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # macOS / Linux
```

**Using standard `python -m venv`:**
```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # macOS / Linux
```

### 3. Install Dependencies

**Using `uv`:**
```bash
uv sync
# or: uv pip install -r requirements.txt
```

**Using `pip`:**
```bash
pip install -r requirements.txt
```

### 4. Audio Input Setup (PyAudio)

If using voice input, ensure PyAudio is installed:

- **Windows**:
  ```bash
  pip install pyaudio
  ```
- **macOS**:
  ```bash
  brew install portaudio
  pip install pyaudio
  ```
- **Linux (Ubuntu / Debian)**:
  ```bash
  sudo apt-get install portaudio19-dev python3-all-dev
  pip install pyaudio
  ```

> ℹ️ **Note**: If audio hardware or PyAudio is absent, the dashboard automatically falls back to text-only input mode.

---

## ⚙️ Configuration

### 1. Set Up `.env`

Copy the included template:

```bash
# Windows PowerShell
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
# EURI LLM API Key — get yours at https://euron.one
EURI_API_KEY=your_euri_api_key_here

# Database connection string
DATABASE_URI=postgresql+psycopg2://user:password@host:5432/dbname?sslmode=require
```

> ⚠️ **Security Warning**: Never commit your `.env` file to version control. It is protected by `.gitignore`.

### 2. Database URI Examples

| Database | Connection String Format |
|---|---|
| **PostgreSQL** (Neon / Supabase) | `postgresql+psycopg2://user:password@host:5432/dbname?sslmode=require` |
| **MySQL** | `mysql+pymysql://user:password@localhost:3306/dbname` |
| **SQLite** | `sqlite:///database.db` |
| **SQL Server** | `mssql+pyodbc://user:password@server/db?driver=ODBC+Driver+17+for+SQL+Server` |

> 💡 **Automatic Normalization**: If your PostgreSQL URI starts with `postgresql://`, [`config.py`](config.py) automatically adapts it to `postgresql+psycopg2://` for driver compatibility.

### 3. Model & Endpoint Configuration

Configured centrally in [`config.py`](config.py):
```python
EURI_BASE_URL = "https://api.euron.one/api/v1/euri"
MODEL_NAME    = "gpt-4.1-mini"
```

---

## 🚀 Running the Application

Start the Streamlit dashboard:

```bash
streamlit run app.py
```

Open your browser at:
```
http://localhost:8501
```

---

## 🖥️ How to Use

1. **Verify Connection**:
   - Check the compact **🔌 DB Connection** card in the sidebar to ensure the database is active.
2. **Choose Spoken Language**:
   - Select your preferred language under **🎙️ Voice & Language** in the sidebar (supports English, Hindi, Spanish, French, etc.).
3. **Submit a Query**:
   - **Voice Input**: Click **🎤 Speak** and say your question clearly into your microphone (e.g., *"Show top 5 customers by sales"*). The app transcribes the speech, populates the input field, and **automatically executes the query**.
   - **Text Input**: Type your question into the search bar and click **🚀 Generate & Run SQL**.
   - **Sidebar Table Preview**: Click **Preview** under any table in the sidebar to automatically execute and inspect its first 5 rows.
4. **Explore the Results Deck**:
   - **📊 Data Grid**: Interactive, sortable tabular data view.
   - **📈 Visualizations**: Switch chart types (Bar, Line, Area, Scatter, Pie, Histogram) and customize axes.
   - **💻 Generated SQL**: Inspect the exact SQL synthesized by the EURI LLM.
   - **📜 Query History**: Review all queries executed during your session along with execution times.
5. **Export Data**:
   - Click **📥 Export CSV** to download the query result set to your local machine.
6. **Reset**:
   - Click **🧹 Clear Input** to reset the input bar and result views.

---

## 🎯 Supported Voice Languages

| Language | Code | Language | Code |
|---|---|---|---|
| English (US) | `en-US` | Arabic | `ar-SA` |
| Hindi (India) | `hi-IN` | Bengali | `bn-IN` |
| Spanish | `es-ES` | Japanese | `ja-JP` |
| French | `fr-FR` | Tamil | `ta-IN` |
| German | `de-DE` | Telugu | `te-IN` |
| Chinese (Mandarin) | `zh-CN` | Marathi | `mr-IN` |

---

## 📊 Visualization Options

- **Bar Chart**: Compare categorical metrics and grouped aggregations.
- **Line Chart**: Track time-series trends and sequential data.
- **Area Chart**: Observe cumulative metrics and volume trends over time.
- **Scatter Plot**: Identify correlations and distributions between two numerical fields.
- **Pie Chart**: Visualize part-to-whole proportions and share percentages.
- **Histogram**: Analyze value distributions and frequencies.

---

## 🔍 Troubleshooting

### Missing Module `pyaudio` / Microphone Error
- **Cause**: PyAudio was not installed in the active Python environment.
- **Fix**: Run `pip install pyaudio`. On Windows, prebuilt wheels are automatically installed. If no microphone is connected, the UI will safely notify you without crashing.

### Database Connection Error / `DATABASE_URI` is None
- **Cause**: `.env` file is missing or `DATABASE_URI` is empty.
- **Fix**: Copy `.env.example` to `.env` and configure your valid database connection string.

### Missing Module `psycopg`
- **Cause**: Using generic `postgresql://` URI prefix with SQLAlchemy 2.0 without psycopg 3.
- **Fix**: Use `postgresql+psycopg2://` in your `DATABASE_URI`. [`config.py`](config.py) automatically handles this normalization.

### 401 Unauthorized / EURI LLM Error
- Verify that `EURI_API_KEY` in `.env` is valid and active.
- Confirm `EURI_BASE_URL` in [`config.py`](config.py) is `https://api.euron.one/api/v1/euri`.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
