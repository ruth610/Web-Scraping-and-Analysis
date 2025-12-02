import pandas as pd
import re
from datetime import datetime

df = pd.read_csv('reviews_raw.csv', dtype=str)
# Keep cols review_id, review, rating, date, bank, source
df = df[['review_id',
        'review',
        'rating',
        'date',
        'bank',
        'source'
    ]].drop_duplicates(subset='review_id')
df['rating'] = df['rating'].astype(float)
# normalize dates to YYYY-MM-DD
def norm_date(d):
    try:
        return pd.to_datetime(d).strftime('%Y-%m-%d')
    except:
        return None
df['date'] = df['date'].apply(norm_date)
df = df[df['review'].notnull()]
df = df.dropna(subset=['date'])  
def clean_text(s):
    s = str(s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s
df['review'] = df['review'].apply(clean_text)
df.to_csv('reviews_clean.csv', index=False)
print('Saved reviews_clean.csv', df.shape)
