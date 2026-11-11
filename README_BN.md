# MINO Augestel API — Render Deployment

এই প্রজেক্টটি Render-এ Python API হিসেবে Deploy করার জন্য প্রস্তুত।

## API endpoint

Deploy করার পর:

`https://YOUR-SERVICE.onrender.com/api/sms`

উদাহরণ:

`https://YOUR-SERVICE.onrender.com/api/sms?token=YOUR_AUGESTEL_API_KEY&start_date=2025-01-15&end_date=2025-01-15&type=a2p&per_page=50&page=1`

এখানে `token` হলো Augestel-এর API key। সার্ভার এটিকে upstream request-এর
`Authorization: Bearer ...` header-এ ব্যবহার করে।

## Render-এ Deploy

1. ZIP extract করুন।
2. সব ফাইল GitHub repository-তে upload করুন।
3. Render Dashboard → New → Web Service নির্বাচন করুন।
4. GitHub repository connect করুন।
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `gunicorn app:app`
7. Deploy করুন।

`render.yaml` ব্যবহার করলে Blueprint deployment-ও করা যাবে।

## গুরুত্বপূর্ণ

- এই API-তে `token` query parameter-এ পাঠানো হয়, যেমনটি চাওয়া হয়েছে।
- URL-এ API key থাকলে browser history, proxy/server logs বা shared links-এ প্রকাশ
  হতে পারে। API key কাউকে দেবেন না; সম্ভব হলে Authorization header-ভিত্তিক
  authentication ব্যবহার করুন।
- Augestel-এর নিজস্ব rate limit (যেমন 5 requests/minute) এই সার্ভারও অতিক্রম
  করতে পারবে না।
- Render Free service নিষ্ক্রিয় থাকলে sleep করতে পারে এবং পরের request-এ
  cold start হতে পারে। Free hosting আজীবন বা 24/7 uptime নিশ্চিত করে না।
- এই endpoint Augestel-এর response body ও HTTP status অপরিবর্তিতভাবে ফেরত দেয়।
