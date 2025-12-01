
import pandas as pd

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# If `df` is not defined earlier in the notebook, create a fallback empty DataFrame.
# Replace this with your real data loading (e.g., pd.read_csv(...)) as needed.
if 'df' not in globals():
    df = pd.DataFrame({'review': []})

# Ensure reviews are strings to avoid errors on NaN or non-string values
df['vader'] = df['review'].apply(lambda t: analyzer.polarity_scores(str(t)))
df['sentiment_score'] = df['vader'].apply(lambda x: x['compound'])
def sentiment_label(s):
    if s >= 0.05: return 'positive'
    if s <= -0.05: return 'negative'
    return 'neutral'
df['sentiment_label'] = df['sentiment_score'].apply(sentiment_label)
df.to_csv('reviews_with_sentiment.csv', index=False)
