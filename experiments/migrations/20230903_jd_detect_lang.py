#!/usr/bin/env python3
import time

import psycopg2
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from pgvector.psycopg2 import register_vector

#
# Set Up Postgres connection
#
connection_string = "postgresql://postgres:password@localhost:55432/ai_experiments"
conn = psycopg2.connect(connection_string)
register_vector(conn)

cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
conn.commit()


def fetch_job_descriptions():
    """Fetch all job descriptions from the database as a generator."""
    page_size = 1000
    cur.execute("SELECT COUNT(1) FROM job_description;")
    total_count = cur.fetchone()[0]
    print(f"Found {total_count} Job Descriptions")
    for offset in range(0, total_count, page_size):
        cur.execute(
            f"SELECT id, description FROM job_description ORDER BY id LIMIT {page_size} OFFSET {offset};"
        )
        results = cur.fetchall()
        for jd in results:
            yield jd


if __name__ == "__main__":
    start_time = time.time()
    for jd in fetch_job_descriptions():
        try:
            language = detect(jd[1])
        except LangDetectException:
            language = ""
        cur.execute(
            "UPDATE job_description SET language = %s WHERE id = %s;", (language, jd[0])
        )
        conn.commit()
        print(f"Updated {jd[0]} with language {language}")

    print(f"Finished in {time.time() - start_time} seconds")
