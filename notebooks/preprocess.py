import pandas as pd
import re
from datetime import datetime

df = pd.read_csv('reviews_raw.csv', dtype=str)

# Keep specific columns
df = df[
    [
        'review_id',
        'review',
        'rating',
        'date',
        'bank',
        'source'
    ]
].drop_duplicates(subset='review_id')

df['rating'] = df['rating'].astype(float)


# Normalize dates to YYYY-MM-DD
def norm_date(date_str):
    try:
        return pd.to_datetime(date_str).strftime('%Y-%m-%d')
    except Exception:
        return None


df['date'] = df['date'].apply(norm_date)
df = df[df['review'].notnull()]
df = df.dropna(subset=['date'])


def clean_text(text):
    text = str(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


df['review'] = df['review'].apply(clean_text)

df.to_csv('reviews_clean.csv', index=False)
print('Saved reviews_clean.csv', df.shape)
