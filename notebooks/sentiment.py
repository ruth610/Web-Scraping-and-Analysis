import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

if 'df' not in globals():
    df = pd.DataFrame({'review': []})

df['vader'] = df['review'].apply(
    lambda t: analyzer.polarity_scores(str(t))
)

df['sentiment_score'] = df['vader'].apply(
    lambda x: x['compound']
)


def sentiment_label(score):
    if score >= 0.05:
        return 'positive'
    if score <= -0.05:
        return 'negative'
    return 'neutral'


df['sentiment_label'] = df['sentiment_score'].apply(sentiment_label)

df.to_csv('reviews_with_sentiment.csv', index=False)
