# Setup.md

This guide explains how to install and run the Campus IT Help Desk project from a clean Ubuntu environment.

## Prerequisites

- Ubuntu Linux
- Python 3
- Python virtual environment support
- PostgreSQL
- Git or another way to download/extract the project files

## 1. Install system packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip postgresql postgresql-contrib
```

Start PostgreSQL:

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl status postgresql
```

The service should show `active (running)`.

## 2. Create the PostgreSQL database

Open the PostgreSQL shell:

```bash
sudo -u postgres psql
```

Run the following commands:

```sql
ALTER USER postgres WITH PASSWORD 'postgres';
DROP DATABASE IF EXISTS campus_helpdesk;
CREATE DATABASE campus_helpdesk;
\q
```

The `DROP DATABASE` command is useful for a clean local test. Do not use it if you want to preserve existing local test data.

## 3. Create and activate a Python virtual environment

From the project root directory:

```bash
python3 -m venv venv
source venv/bin/activate
```

Upgrade pip and install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure environment variables

For local testing, run:

```bash
export SECRET_KEY="local-test-secret"
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/campus_helpdesk"
```

Optional: copy `.env.example` and use it as a reference for your local environment settings.

## 5. Initialize the database

```bash
flask --app run.py init-db
```

This creates the database tables and the default admin account.

## 6. Optional: seed demo data

```bash
flask --app run.py seed-demo
```

This creates a demo user and sample tickets for testing.

## 7. Run the application

```bash
python3 run.py
```

Open the application in a browser:

```text
http://127.0.0.1:5000
```

## Demo Accounts

### Default admin

- Email: `admin@campus.local`
- Password: `Admin123!`

### Seeded demo user

Available after running `flask --app run.py seed-demo`:

- Email: `alice@student.local`
- Password: `Student123!`

## Basic Workflow Test

1. Register a new user.
2. Log in as that user.
3. Submit a support ticket.
4. Log out.
5. Log in as admin.
6. Open the admin panel.
7. Add a comment and update the ticket status to `Resolved`.
8. Log out.
9. Log back in as the user.
10. Open the resolved ticket and submit a reopen reason.
11. Confirm the ticket status changes back to `Open` and the reopen reason appears as a comment.

## Troubleshooting

### PostgreSQL connection failed

```bash
sudo systemctl restart postgresql
```

Then confirm `DATABASE_URL` is set correctly:

```bash
echo $DATABASE_URL
```

### Flask command not found

Activate the virtual environment:

```bash
source venv/bin/activate
```

Then retry the command.

### Database already exists or contains old data

Reset the database manually:

```bash
sudo -u postgres psql
```

```sql
DROP DATABASE IF EXISTS campus_helpdesk;
CREATE DATABASE campus_helpdesk;
\q
```

Then rerun:

```bash
flask --app run.py init-db
flask --app run.py seed-demo
```
