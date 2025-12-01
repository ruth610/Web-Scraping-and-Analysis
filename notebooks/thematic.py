from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(ngram_range=(1,3), max_features=1000, stop_words='english')
X = vectorizer.fit_transform(df['review'])
terms = vectorizer.get_feature_names_out()
# top terms per bank
for bank in df['bank'].unique():
    idxs = df[df['bank']==bank].index.tolist()
    bank_vec = X[idxs].sum(axis=0)
    topn = sorted(list(zip(terms, bank_vec.A1)), key=lambda x: -x[1])[:40]
    print(bank, topn[:20])
