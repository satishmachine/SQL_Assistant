# 🧠 SQL-Powered Data Retrieval Assistant

A multilingual voice-enabled SQL assistant that converts natural language queries into SQL statements using AI and provides interactive data visualizations.

## 🌟 Features

- **Multilingual Speech Recognition**: Supports 12+ languages including English, Hindi, Spanish, French, German, Chinese, Arabic, Bengali, Japanese, Tamil, Telugu, and Marathi
- **Natural Language to SQL**: Converts spoken or typed queries into SQL using  LLM API
- **Interactive Data Visualization**: Generate bar charts, line charts, pie charts, and scatter plots from query results
- **Database Connectivity**: Supports multiple database types (MySQL, PostgreSQL, SQLite, etc.)
- **Real-time Voice Input**: Voice-to-text conversion with Google Speech Recognition
- **Streamlit Web Interface**: User-friendly web application

## 🛠️ Prerequisites

- Python 3.10
- Microphone (for voice input)
- Database connection (MySQL, PostgreSQL, SQLite, etc.)
- API key for LLM services

## 📦 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd SQL_LLM_Project
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv 

# Activate virtual environment
# On Windows:
sql_assis\Scripts\activate
# On macOS/Linux:
source sql_assis/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Additional Setup for Speech Recognition

#### Windows:
```bash
pip install pyaudio
```

#### macOS:
```bash
brew install portaudio
pip install pyaudio
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get install python3-pyaudio
# or
sudo apt-get install portaudio19-dev python3-all-dev
pip install pyaudio
```

## ⚙️ Configuration

### 1. Environment Variables

Create a `.env` file in the project root directory:

```env
#LLM API Configuration
API_KEY=your_LLM_api_key_here

# Database Configuration
DATABASE_URI=your_database_connection_string_here
```

### 2. Database URI Examples

Choose the appropriate connection string for your database:

#### MySQL:
```
DATABASE_URI=mysql+pymysql://username:password@localhost:3306/database_name
```

#### PostgreSQL:
```
DATABASE_URI=postgresql+psycopg2://username:password@localhost:5432/database_name
```

#### SQLite:
```
DATABASE_URI=sqlite:///path/to/your/database.db
```

#### SQL Server:
```
DATABASE_URI=mssql+pyodbc://username:password@server:port/database?driver=ODBC+Driver+17+for+SQL+Server
```



## 🚀 Usage

### 1. Start the Application
```bash
streamlit run app.py
```

### 2. Access the Web Interface
Open your browser and navigate to:
```
http://localhost:8501
```

### 3. Using the Assistant

1. **Select Language**: Choose your preferred language for speech recognition
2. **Input Query**: 
   - Click "🎤 Start Listening" to speak your query
   - Or type your question in the text input
3. **View Results**: 
   - See the generated SQL query
   - View query results in a data table
   - Create interactive visualizations

### 4. Example Queries

- "Show me all customers from New York"
- "What are the top 5 selling products?"
- "Find the average salary by department"
- "List orders placed in the last month"

## 📁 Project Structure

```
SQL_LLM_Project/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration settings
├── utills.py             # Utility functions
├── prompt_template.txt   # LLM prompt template
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## 🔧 Configuration Files

### config.py
Contains API endpoints and model configuration:
- EURI API URL: `https://api.euron.one/api/v1/euri/alpha/chat/completions`
- Model: `gpt-4.1-nano`

### prompt_template.txt
Template for generating SQL queries from natural language input.

## 🎯 Supported Languages

- English (US)
- Hindi (India)
- Spanish
- French
- German
- Chinese (Mandarin)
- Arabic
- Bengali
- Japanese
- Tamil
- Telugu
- Marathi

## 📊 Visualization Options

- **Bar Chart**: Compare categorical data
- **Line Chart**: Show trends over time
- **Pie Chart**: Display proportional data
- **Scatter Plot**: Explore relationships between variables

## 🔍 Troubleshooting

### Common Issues

1. **Microphone not working**:
   - Check microphone permissions
   - Ensure PyAudio is properly installed
   - Test microphone with other applications

2. **Database connection errors**:
   - Verify DATABASE_URI format
   - Check database credentials
   - Ensure database server is running

3. **EURI API errors**:
   - Verify API key is correct
   - Check internet connection
   - Ensure API quota is not exceeded

4. **Speech recognition errors**:
   - Speak clearly and at moderate pace
   - Ensure quiet environment
   - Check selected language matches spoken language

### Dependencies Issues

If you encounter issues with specific packages:

```bash
# For speech recognition issues
pip install --upgrade SpeechRecognition

# For audio issues
pip install --upgrade pyaudio

# For database connectivity
pip install --upgrade sqlalchemy pymysql psycopg2
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
1. Check the troubleshooting section
2. Review the configuration settings
3. Ensure all dependencies are properly installed
4. Verify environment variables are set correctly

## 🔮 Future Enhancements

- Support for more database types
- Advanced visualization options
- Query history and favorites
- Multi-table join query support
- Export functionality for results and visualizations
