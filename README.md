# 🧠 SQL-Powered Data Retrieval Assistant

A multilingual, voice-enabled SQL assistant that converts natural language queries into SQL statements using the **EURI LLM API** and provides interactive data visualizations — all through a clean **Streamlit** web interface.

---

## 🌟 Features

| Feature | Description |
|---|---|
| 🎙️ **Multilingual Speech Recognition** | Supports 12+ languages via Google Speech Recognition |
| 🤖 **Natural Language → SQL** | Uses EURI LLM (`gpt-4.1-nano`) to generate SQL from plain English (or any supported language) |
| 📊 **Interactive Visualizations** | Bar, Line, Pie, and Scatter charts powered by Plotly |
| 🗄️ **Multi-Database Support** | Works with PostgreSQL, MySQL, SQLite, SQL Server, and more |
| 🔐 **Secure Config** | API keys and DB credentials stored in `.env` — never hardcoded |
| 🌐 **Streamlit Web App** | Clean, browser-based interface — no frontend setup needed |

---

## 🛠️ Tech Stack

- **Frontend / App**: [Streamlit](https://streamlit.io/)
- **LLM API**: [EURI AI](https://euron.one) — OpenAI-compatible REST API
- **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Speech Recognition**: [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) + Google Speech API
- **Visualization**: [Plotly Express](https://plotly.com/python/plotly-express/)
- **HTTP Client**: [Requests](https://docs.python-requests.org/)

---

## 📋 Prerequisites

- Python **3.10+**
- A working **microphone** (for voice input)
- A **database** accessible via connection URI
- A valid **EURI API key** from [euron.one](https://euron.one)

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "SQL_LLM_Project - Copy"
```

### 2. Create & Activate a Virtual Environment

```bash
# Create
python -m venv .venv

# Activate — Windows
.venv\Scripts\activate

# Activate — macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. PyAudio Setup (required for voice input)

#### Windows
```bash
pip install pyaudio
```

#### macOS
```bash
brew install portaudio
pip install pyaudio
```

#### Linux (Ubuntu / Debian)
```bash
sudo apt-get install portaudio19-dev python3-all-dev
pip install pyaudio
```

---

## ⚙️ Configuration

### 1. Create a `.env` File

Copy the template below and save it as `.env` in the project root:

```env
# EURI LLM API Key — get yours at https://euron.one
EURI_API_KEY=your_euri_api_key_here

# Database connection string (see examples below)
DATABASE_URI=your_database_connection_string_here
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

### 2. Database URI Examples

| Database | Connection String |
|---|---|
| **PostgreSQL** | `postgresql://user:password@host:5432/dbname?sslmode=require` |
| **MySQL** | `mysql+pymysql://user:password@localhost:3306/dbname` |
| **SQLite** | `sqlite:///path/to/database.db` |
| **SQL Server** | `mssql+pyodbc://user:password@server/db?driver=ODBC+Driver+17+for+SQL+Server` |

### 3. Model & API Endpoint (`config.py`)

These are set automatically — no manual edits needed:

```python
EURI_API_URL = "https://api.euron.one/api/v1/euri/chat/completions"
MODEL_NAME   = "gpt-4.1-nano"
```

---

## 🚀 Running the App

```bash
streamlit run app.py
```

Then open your browser at:

```
http://localhost:8501
```

---

## 🖥️ How to Use

1. **Choose a language** — select from the dropdown (English, Hindi, Spanish, etc.)
2. **Ask a question**:
   - Click **🎤 Start Listening** and speak your query, OR
   - Type your question in the text box
3. **View the generated SQL** — displayed as a syntax-highlighted code block
4. **Explore results** — query results appear as an interactive data table
5. **Visualize** — pick a chart type and select columns to plot

### Example Queries

```
Show me all customers from New York
What are the top 5 selling products?
Find the average salary by department
List all orders placed in the last 30 days
How many users signed up each month?
```

---

## 📁 Project Structure

```
SQL_LLM_Project - Copy/
│
├── app.py                 # Main Streamlit application (UI + orchestration)
├── utills.py              # Core logic: schema extraction, LLM call, SQL execution
├── config.py              # API URL, model name, DB URI loaded from env
├── prompt_template.txt    # LLM system prompt template ({schema}, {question})
├── requirements.txt       # Python package dependencies
├── pyproject.toml         # Project metadata
├── .env                   # 🔒 Your secrets (create this — never commit!)
├── .gitignore             # Excludes .env, .venv, __pycache__, etc.
├── LICENSE                # MIT License
└── README.md              # This file
```

---

## 🎯 Supported Languages

| Language | Code |
|---|---|
| English (US) | `en-US` |
| Hindi (India) | `hi-IN` |
| Spanish | `es-ES` |
| French | `fr-FR` |
| German | `de-DE` |
| Chinese (Mandarin) | `zh-CN` |
| Arabic | `ar-SA` |
| Bengali | `bn-IN` |
| Japanese | `ja-JP` |
| Tamil | `ta-IN` |
| Telugu | `te-IN` |
| Marathi | `mr-IN` |

---

## 📊 Visualization Types

| Chart | Best For |
|---|---|
| **Bar Chart** | Comparing categories (e.g., sales by region) |
| **Line Chart** | Trends over time (e.g., monthly revenue) |
| **Pie Chart** | Proportional breakdowns (e.g., market share) |
| **Scatter Plot** | Correlations between two numeric columns |

---

## 🔍 Troubleshooting

### 404 Error from EURI API
- **Cause**: Stale or incorrect API URL.
- **Fix**: Ensure `config.py` uses `https://api.euron.one/api/v1/euri/chat/completions` (no `/alpha/` segment).
- Restart Streamlit after any code changes: `Ctrl+C` → `streamlit run app.py`.

### API Key / 401 Unauthorized
- Verify `EURI_API_KEY` in your `.env` matches the key from [euron.one](https://euron.one).
- Confirm `.env` is in the **same directory** as `app.py`.

### Database Connection Errors
- Double-check your `DATABASE_URI` format (see examples above).
- Ensure the database server is reachable and credentials are correct.
- For PostgreSQL (Neon, Supabase, etc.) make sure `?sslmode=require` is appended.

### Microphone / Speech Recognition Issues
- Check OS microphone permissions for the terminal / Python process.
- Ensure PyAudio is installed correctly for your OS (see Installation section).
- Speak clearly in a quiet environment; select the correct language from the dropdown.

### Streamlit Showing Old Code After Changes
```bash
# Stop the server (Ctrl+C), then clear Python cache and restart:
Remove-Item -Recurse -Force __pycache__   # Windows PowerShell
streamlit run app.py
```

### Package-Level Fixes
```bash
pip install --upgrade streamlit sqlalchemy psycopg2 SpeechRecognition pyaudio plotly requests
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push and open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🔮 Roadmap

- [ ] Query history & saved favourites
- [ ] Multi-table JOIN query support
- [ ] Export results as CSV / Excel
- [ ] Advanced chart customisation
- [ ] Support for more LLM providers (OpenAI, Gemini, Ollama)
- [ ] Authentication layer for multi-user deployments
