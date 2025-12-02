from google_play_scraper import reviews, Sort
import pandas as pd
apps = [
  {'bank':'CBE', 'pkg':'com.combanketh.mobilebanking'},
  {'bank':'BOA', 'pkg':'com.boa.boaMobileBanking'},
  {'bank':'Dashen', 'pkg':'com.dashen.dashensuperapp'}
]
rows=[]
for app in apps:
  count=0; token=None
  while count < 420:
    rv, token = reviews(
      app['pkg'],
      lang='en',
      country='us',
      sort=Sort.NEWEST,
      continuation_token=token
    )
    if not rv: break
    for r in rv:
      rows.append({
        'review_id': r['reviewId'],
        'review': r['content'],
        'rating': r['score'],
        'date': r['at'].strftime('%Y-%m-%d'),
        'bank': app['bank'],
        'source': 'google_play'
      })
      count += 1
    if token is None: break
df = pd.DataFrame(rows)
df.to_csv('reviews_raw.csv', index=False)
print(df.shape)
