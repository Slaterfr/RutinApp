import requests
from bs4 import BeautifulSoup
import json
from db.database import conn

BASE_URL = "https://oss.exercisedb.dev/api/v1/exercises"

def transform(ex):
    return {
        "name" : ex.get("name").strip(),
        "muscles" : ex.get("primaryMuscles", []).replace(),
        "equipment_needed" : ex.get("equipment", ""),
        "instructions" : ex.get("instructions"),
        "category" : ex.get("category"),
        "external_id" : ex.get("id")
    }

def fetch_all_exercises():
    file = r"RutinApp\pipeline\data\exercises.json"

    with open(file, "r") as f:
        return json.load(f)

def chunked(data, size=50):
    for i in range(0, len(data), size):
        yield data[i:i + size]

def save_batch(conn, batch):
    values = [(
        ex["name"],
        ex["muscles"],
        ex["equipment_needed"],
        ex["instructions"],
        ex["category"],
        ex["external_id"]
    ) for ex in batch]
    
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO exercise(exercise_name, muscles, equipment_needed, instructions, category, external_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (external_id)
            DO UPDATE SET
                exercise_name = EXCLUDED.exercise_name,
                muscles = EXCLUDED.muscles,
                equipment_needed = EXCLUDED.equipment_needed,
                instructions = EXCLUDED.instructions,
                category = EXCLUDED.category;
            """, values
        )
    conn.commit()

def run_pipeline(conn):
    data = fetch_all_exercises()
    processed = 0
    total = len(data)
    for batch in chunked(data, size=50):
        transformed = [transform(ex) for ex in batch]

        save_batch(conn, transformed)
        processed+=len(batch)
        print(f"Processed : {processed}/{total}")


run_pipeline(conn)

