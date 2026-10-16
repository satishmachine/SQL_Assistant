from openai import OpenAI
from sqlalchemy import text, MetaData
from config import EURI_API_KEY, EURI_BASE_URL, MODEL_NAME
from dotenv import load_dotenv
load_dotenv()

def get_db_schema(engine):
    meta = MetaData()
    meta.reflect(bind=engine)
    schema = ""
    for table in meta.tables.values():
        schema += f"\nTable: {table.name}\nColumns: {', '.join([col.name + ' (' + str(col.type) + ')' for col in table.columns])}\n"
    return schema.strip()


def get_db_tables_dict(engine):
    meta = MetaData()
    meta.reflect(bind=engine)
    tables = {}
    for table in meta.tables.values():
        tables[table.name] = [(col.name, str(col.type)) for col in table.columns]
    return tables


def call_euri_llm(prompt: str) -> str:
    client = OpenAI(api_key=EURI_API_KEY, base_url=EURI_BASE_URL)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=300
    )
    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        lines = content.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        content = "\n".join(lines).strip()
    return content


def execute_sql(engine, query):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall(), result.keys()
