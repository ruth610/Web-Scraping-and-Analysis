from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine("postgresql+psycopg2://rutha:mypassword@localhost:5432/bank_reviews")
df = pd.read_csv("reviews_analyzed.csv")

# ----------- UPSERT BANKS -----------
banks = df["bank"].unique()

with engine.begin() as conn:
    stmt = text("""
        INSERT INTO banks (bank_name)
        VALUES (:name)
        ON CONFLICT (bank_name) DO NOTHING
    """)
    for b in banks:
        conn.execute(stmt, {"name": b})


# ----------- FETCH BANK IDS -----------
with engine.connect() as conn:
    result = conn.execute(text("SELECT bank_name, bank_id FROM banks"))
    bank_map = {name: bid for name, bid in result.fetchall()}


# ----------- INSERT REVIEWS -----------
insert_review = text("""
    INSERT INTO reviews (
        review_id, bank_id, review_text, rating, review_date,
        sentiment_label, sentiment_score, themes, source
    )
    VALUES (
        :review_id, :bank_id, :review_text, :rating, :review_date,
        :sentiment_label, :sentiment_score, :themes, :source
    )
    ON CONFLICT (review_id) DO NOTHING
""")

with engine.begin() as conn:
    for _, row in df.iterrows():

        # ---- THEMES ----
        themes = row["themes"]
        if not isinstance(themes, list):
            themes = [themes]

        # ---- SENTIMENT SCORE ----
        score_raw = row.get("sent_score_transformer") or row.get("sentiment_score")
        sentiment_score = float(score_raw) if score_raw is not None else None

        # ---- SENTIMENT LABEL ----
        sentiment_label = (
            row.get("sentiment_label") or
            row.get("sent_label_transformer")
        )

        # ---- INSERT ----
        conn.execute(
            insert_review,
            {
                "review_id": row["review_id"],
                "bank_id": bank_map[row["bank"]],
                "review_text": row["review"],
                "rating": int(row["rating"]),
                "review_date": row["date"],
                "sentiment_label": sentiment_label,
                "sentiment_score": sentiment_score,
                "themes": themes,
                "source": row["source"]
            }
        )
