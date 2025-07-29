# 🔄 Database Switch Guide (For All Teammates)

This project can use **two types of databases**:
- **Local (SQLite)** → For development on your own computer.
- **Cloud (Supabase PostgreSQL)** → Shared database for the whole team.

---

## ✅ 1. Environment Files Needed

Create these files in the project root folder:

### `.env.production` (Cloud Database)
```
DJANGO_ENV= ()
DB_NAME= ()
DB_USER= ()
DB_PASSWORD= ()
DB_HOST= ()
DB_PORT= ()
```
ask yixin for the whole file

### `.env.local` (Local Database)
```
DJANGO_ENV=local
```

> ⚠️ Do NOT upload `.env` files to GitHub. Share privately.

---

## ✅ 2. For Windows Users

### 2.1 Create a file `switch_db.ps1` with this content:(already create, you don't need to do this step)
```
param ([string]$envTarget)

if ($envTarget -eq "prod") {
    Copy-Item ".env.production" ".env" -Force
    Write-Host "✅ Switched to Cloud PostgreSQL"
}
elseif ($envTarget -eq "local") {
    Copy-Item ".env.local" ".env" -Force
    Write-Host "✅ Switched to Local SQLite"
}
else {
    Write-Host "❌ Usage: .\switch_db.ps1 local | prod"
}
```

### 2.2 How to use:
```
.\switch_db.ps1 prod    # Switch to cloud
.\switch_db.ps1 local   # Switch to local
```

---

## ✅ 3. For macOS / Linux Users

### 3.1 Create a file `switch_db.sh` with this content: (already create, you don't need to do this step)
```
#!/bin/bash

if [ "$1" == "prod" ]; then
    cp .env.production .env
    echo "✅ Switched to Cloud PostgreSQL"
elif [ "$1" == "local" ]; then
    cp .env.local .env
    echo "✅ Switched to Local SQLite"
else
    echo "❌ Usage: ./switch_db.sh [local|prod]"
fi
```

### 3.2 Make the script executable:
```
chmod +x switch_db.sh
```

### 3.3 How to use:
```
./switch_db.sh prod    # Switch to cloud
./switch_db.sh local   # Switch to local
```

---

## ✅ 4. Check if Database Works

Run:
```
python manage.py showmigrations
```
- If you see migrations with `[X]`, you are connected to Supabase.
- If you see local migrations, you are using SQLite.

---

## ✅ 5. Start the Server
```
python manage.py runserver
```

---

## ✅ 6. Notes
- First time on cloud: run `python manage.py migrate`
- You may need to create an admin account: `python manage.py createsuperuser`
- Never share your Supabase password publicly.

---

🎉 **Done!** Now everyone can easily switch between local and cloud databases.
