import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load your data into a pandas DataFrame.
# Replace 'path/to/your/data.csv' with the actual path to your data file.
df = pd.read_csv('reviews_clean.csv')

vectorizer = TfidfVectorizer(ngram_range=(1,3), max_features=1000, stop_words='english')
X = vectorizer.fit_transform(df['review'])
terms = vectorizer.get_feature_names_out()
# top terms per bank
for bank in df['bank'].unique():
    idxs = df[df['bank']==bank].index.tolist()
    bank_vec = X[idxs].sum(axis=0)
    topn = sorted(list(zip(terms, bank_vec.A1)), key=lambda x: -x[1])[:40]
    print(bank, topn[:20])
def assign_themes(text):
    themes=[]
    t = text.lower()
    if any(k in t for k in ['login','otp','password','blocked','lock']): themes.append('Account Access')
    if any(k in t for k in ['slow','loading','delay','transfer','timeout']): themes.append('Transaction Performance')
    if any(k in t for k in ['crash','crashes','freeze','hang']): themes.append('App Stability')
    if any(k in t for k in ['ui','interface','design','navigation','easy','confusing']): themes.append('UI/UX')
    if any(k in t for k in ['support','help','customer service','agent','response']): themes.append('Customer Support')
    return themes or ['Other']

df['themes'] = df['review'].apply(assign_themes)
df.to_csv('reviews_analyzed.csv', index=False)
