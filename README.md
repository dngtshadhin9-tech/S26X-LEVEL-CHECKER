# S26X LEVEL CHECKER

UID + password দিয়ে level যাচাই। Result level অনুযায়ী তিনটা আলাদা JSON:
`lvl0-7`, `lvl8-20`, `lvl21plus`।

## ফোল্ডার কাঠামো
```
index.html          → website (static)
api/check.py        → Vercel Python function  POST /api/check
api/_core.py        → login + level core (minister.py থেকে)
requirements.txt    → httpx, pycryptodome, protobuf
```

## Vercel এ deploy
1. এই ফোল্ডার GitHub এ push করুন (অথবা Vercel CLI দিয়ে সরাসরি deploy করুন)।
2. Vercel → **Add New → Project** → repository import করুন। Framework: **Other**।
3. **Settings → Environment Variables** এ যোগ করুন:
   - `CHECKER_KEY` = শক্ত একটা key (এটাই site খুললে দিতে হবে)
4. **Deploy** চাপুন।

CLI দিয়ে: `npm i -g vercel` → ফোল্ডারে গিয়ে `vercel --prod`, তারপর dashboard এ `CHECKER_KEY` যোগ করে redeploy।

## নিরাপত্তা
- `CHECKER_KEY` না থাকলে server সব request বন্ধ রাখে।
- Password কোথাও store বা log হয় না, response এ password বা token ফেরত যায় না।
- Result শুধু browser এ থাকে; download করলেই file পাবেন। Server এ কিছু save হয় না।
- Site public করলে অন্যের credential যাচাইয়ের জন্য ব্যবহার হতে পারে। শুধু নিজের account এর জন্য ব্যবহার করুন।

## Local test
```
pip install -r requirements.txt
CHECKER_KEY=secret python -m http.server  # static দেখার জন্য; /api/check এর জন্য vercel dev ব্যবহার করুন
vercel dev
```
