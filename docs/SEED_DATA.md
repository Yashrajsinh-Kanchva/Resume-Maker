# Dummy Data Seed Script

Use this to **clear** the database and **insert dummy users, resumes, and feedbacks** with timestamps spread over time so the **admin Analytics** charts show realistic data.

## What it does

1. **Deletes all** documents from:
   - `users`
   - `resumes`
   - `feedbacks`

2. **Inserts one admin user** (so you can still log in to admin):
   - Email: `admin@gmail.com`
   - Password: `Admin123!@#`
   - Change this password after first login if you use it in a real environment.

3. **Inserts dummy data** with `created_at` spread over the **last 45 days**:
   - **~15 users** (mix of local and Google provider)
   - **~25–60 resumes** (1–4 per user, random dates)
   - **15 feedbacks** (ratings 2–5, random dates)

Analytics uses:
- **Users over time** → grouped by date (`created_at`)
- **Resumes over time** → grouped by date (`created_at`)
- **Top users** → by resume count

So varied timestamps make the line charts and bar chart look correct.

## How to run

From the **project root**:

```bash
# Bash / cmd
cd Python && python scripts/seed_dummy_data.py

# PowerShell (use ; instead of &&)
cd Python; python scripts/seed_dummy_data.py
```

From the **Python** folder:

```bash
python scripts/seed_dummy_data.py
```

**Requirements:**

- `MONGODB_URI` set in `.env` (project root)
- Dependencies installed (`pip install -r requirements.txt`)

## After running

1. Log in to the admin UI with `admin@gmail.com` / `Admin123!@#`.
2. Open **Analytics** to see users over time, resumes over time, and top users by resume count.
3. **Dashboard** will show total users, resumes, feedbacks, and provider breakdown.

## Customization

Edit **Python/scripts/seed_dummy_data.py**:

- `DAYS_BACK = 45` — change to spread data over more/fewer days.
- `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `ADMIN_NAME` — change default admin.
- `dummy_users` — add/remove or rename dummy users.
- `feedback_entries` — add/remove or change feedback text and ratings.
