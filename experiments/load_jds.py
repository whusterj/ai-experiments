#!/usr/bin/env python3
import csv
import glob
import time

import psycopg2
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from pgvector.psycopg2 import register_vector
from psycopg2.extras import execute_values

#
# Set Up Postgres connection
#
connection_string = "postgresql://postgres:password@localhost:55432/ai_experiments"
conn = psycopg2.connect(connection_string)
register_vector(conn)

cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
conn.commit()


#
# Helper functions to load jobs
#
def get_jobs_csv():
    """Find all the CSV files in the jobs directory and return them as a generator"""
    csv_paths = glob.glob("../data/jobs/*.csv")
    for csv_path in csv_paths:
        with open(csv_path, "r") as f:
            yield f


def load_all_job_descriptions():
    """Load all jobs from each CSV at a time."""
    for csvfile in get_jobs_csv():
        print(f"Loading {csvfile.name}...")
        start_time = time.time()

        csvreader = csv.DictReader(csvfile, delimiter=",")

        data = []
        for row in csvreader:
            try:
                language = detect(row["description"])
            except LangDetectException:
                language = ""
            data.append(
                [
                    row["title"],
                    row["company"],
                    row["location"],
                    row["description"],
                    language,
                ]
            )

        execute_values(
            cur,
            """INSERT INTO job_description_tmp (
                title,
                company,
                location,
                description,
                language
            ) VALUES %s;
            """,
            data,
        )
        conn.commit()
        print(f"    Loaded in {time.time() - start_time} seconds.")


if __name__ == "__main__":
    start_time = time.time()
    load_all_job_descriptions()
    print(f"Import finished after: {time.time() - start_time} seconds.")
