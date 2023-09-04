# AI Experiments - Python Notebooks

## Installation

```bash
pyenv install 3.10.13
sudo apt-get install libicu-dev
python -m pip install -r experiments/requirements.txt
```

## Using `pgvector`

Docker makes it easy to run postgres with pgvector. Start the database container by running:

```bash
docker-compose up -d
```

### Connect to the Database

With the database running under docker compose, you can connect to it using the following command:

```bash
psql postgresql://postgres:password@localhost:55432/ai_experiments
```

Note the weird port number. This is configured in the `docker-compose.yml` file in order to avoid conflicts with any local postgres instances you may have running.

Database migrations are included in the `migrations` directory. They are `.sql` files. You can run them directly against the database using the `psql` command line tool. For example:

```bash
psql postgresql://postgres:password@localhost:55432/ai_experiments -f migrations/20230902_set_up_db.sql
```

## Querying

```sql
SELECT 1 - (embedding <=> '[3,1,2]') AS cosine_similarity FROM items;
```

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

query = "Here's some imput data..."
query_embedding = model.encode(query)

cur.execute("SELECT 1 - (embedding <=> %s) AS cosine_similarity, content FROM jd_chunks ORDER BY cosine_similarity LIMIT 20;", (embedding_array,))
top20 = cur.fetchall()


cur.execute("""
    with matched_chunks as (
        SELECT
            1 - (embedding <=> %s) AS cosine_similarity,
            jd.id as jd_id,
            jd.title as jd_title,
            jd.description as jd_content
        FROM jd_chunk
        INNER JOIN job_description jd ON jd.id = jd_chunk.doc_id
        ORDER BY cosine_similarity
    )

    SELECT
        AVG(mc.cosine_similarity) AS avg_cosine_similarity,
        mc.jd_id,
        mc.jd_title
    FROM matched_chunks mc
    GROUP BY mc.jd_id, mc.jd_title
    ORDER BY avg_cosine_similarity
    LIMIT 25;
    """,
    (embedding_array,)
)
top = cur.fetchall()
```

## Notes

An example of getting dot products for a 'query' embedding against a series of 'passage' embeddings.

```python
query_embedding = model.encode("How big is London?")
passage_embedding = model.encode(
    ["London has 9,787,426 inhabitants at the 2011 census, and is the second most populous city in the United Kingdom, after Birmingham.",
     "London is known for its cultural diversity. With more than 300 languages spoken in the city, London is the most linguistically diverse place in the European Union.",
     "France is the largest country on mainland Europe."]
)

result_tensor = util.dot_score(query_embedding, passage_embedding)
print("Similarity:", result_tensor.data)
```
