# SMCCDhackathon

## 🧰 Project Requirements
- Python 3.10 or above
- Virtual environment recommended (venv)
- Django 5.1.7
- Git + GitHub

## 📦 Installation & Setup Guide (for team members)
### ✅ Step 0: Check Python Installation
```bash
python --version
```


If you don't have Python installed:
- Download it from the official site: https://www.python.org/downloads/
- Or use Homebrew on Mac:
```bash
brew install python@3.10
```

Once installed, verify again:
```bash
python3 --version
```

Then proceed to clone the repository.

### ✅ Step 1: Clone the Repository
### ✅ Step 2: (recommend) Create and Activate Virtual Environment
```bash
    python -m venv env
    source env/bin/activate  # Mac/Linux only
    env\Scripts\activate     # WIndows only
```
Don't upload your venv (env) to github! 
To ignore a file: we add its directory to .gitignore (so don't delete it!)

### ✅ Step 3: Install Required Packages
```bash
pip install -r requirements.txt
```
### ✅ Step 4: Testing if Django has been successfully set up
1. Apply Database Migrations
```bash
python manage.py migrate
```
2. Start Development Server
```bash
python manage.py runserver
```

3. The project is likely to be at http://127.0.0.1:8000/ 

## 📂 Project Structure
[View Project Structure](./PROJECT_STRUCTURE.md)


## 🧪 Developer Tips for GitHub
- After pulling changes from GitHub:
```bash
git pull
source env/bin/activate
pip install -r requirements.txt
```
- **Always leave a meaningful commit message** when pushing changes. 
This helps your team understand the purpose of the update. For example:
  ```bash
  git commit -m "Fix: Resolved issue with user authentication"
  ```

- **Using GitHub in VS Code**:
  If you are using VS Code, then you can just
  - Open the **Source Control** tab (`Ctrl + Shift + G`).
  - Stage your changes, write a descriptive commit message, and commit directly from VS Code.
  - Commit
  (Make sure you have the GitLens library installed)

## 🧪 Developer Tips for Django
- After modifying models:
```bash
python manage.py makemigrations
python manage.py migrate
```

- To create an admin user: 
```bash
python manage.py createsuperuser
```
( If you're unsure about what an admin user is, ask @liyixin before creating one)