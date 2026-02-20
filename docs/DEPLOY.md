# Deploy Resume Maker for Free

Use **Render** (hosting) + **MongoDB Atlas** (database). Both free tiers.

---

## 1. Put your code on GitHub

- Create a repo at [github.com/new](https://github.com/new).
- In your project folder:
  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
  git push -u origin main
  ```
  (Use your branch name if it’s not `main`.)

---

## 2. Create a free MongoDB database

1. Sign up at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas).
2. Create a **free M0 cluster**.
3. **Database Access** → Add a user (username + password).
4. **Network Access** → Add IP → **Allow from anywhere** (0.0.0.0/0).
5. **Database** → **Connect** → **Connect your application** → copy the URI.  
   Replace `<password>` with your DB user password.  
   Example: `mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority`

---

## 3. Deploy on Render

1. Go to [render.com](https://render.com), sign up (e.g. with GitHub).
2. **New** → **Web Service**.
3. Connect GitHub and select your repo.
4. Set:
   - **Build command:** `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start command:** `cd Python && gunicorn --bind 0.0.0.0:$PORT run:app`
   - **Plan:** Free
5. In **Environment**, add:
   - `SECRET_KEY` = long random string (e.g. run: `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `MONGODB_URI` = your Atlas URI from step 2
6. Click **Create Web Service**. Wait for the first deploy.

Your app URL will be like: `https://resume-maker-xxxx.onrender.com`

---

## 4. (Optional) Google sign-in

In Google Cloud Console → your OAuth client → **Authorized redirect URIs**, add:

`https://YOUR-RENDER-URL.onrender.com/api/google/callback`

---

Done. Free deploy from Git.
