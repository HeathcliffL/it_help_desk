# Setup.md

How to install and run the Campus IT Help Desk project.

By default the app uses SQLite — no external database is required. The database file (`helpdesk.db`) is created automatically in the project root on first run.

## Prerequisites

- Python 3.11+ (older 3.x will likely work but is untested)
- macOS, Linux, or Windows

That's it. No PostgreSQL, no system services to start.

## Option A — macOS double-click

1. Open the project folder in Finder.
2. Double-click `HelpDesk.app` (or `launch.command`).

On the first run, Terminal will open and the launcher will:
- create a virtualenv under `venv/`,
- install dependencies from `requirements.txt`,
- run `flask init-db` to create `helpdesk.db` and the default admin,
- start the Flask server and open `http://127.0.0.1:5000` in your browser.

If double-click does nothing the first time, it's almost always macOS quarantine. Open Terminal and run once:
```bash
cd "$HOME/Desktop/it_help_desk" && chmod +x launch.command && xattr -cr launch.command 2>/dev/null; open launch.command
```

## Option B — manual (any OS)

From the project root:

```bash
python3 -m venv venv
source venv/bin/activate        # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
flask --app run.py init-db
python3 run.py
```

Then open `http://127.0.0.1:5000` in a browser.

### Optional: seed demo data
```bash
flask --app run.py seed-demo
```

## Environment variables

Everything is optional. If you want to customize, copy `.env.example` to `.env` and edit.

- `SECRET_KEY` — Flask session secret. Defaults to a placeholder.
- `DATABASE_URL` — Override the database. Default is `sqlite:///helpdesk.db` in the project root. Set to a Postgres URL (e.g. `postgresql://user:pass@localhost:5432/dbname`) to use Postgres instead — you'll also need `pip install psycopg2-binary`.

## Demo accounts

### Default admin
- Email: `admin@campus.local`
- Password: `Admin123!`

### Seeded demo user
Available after `flask --app run.py seed-demo`:
- Email: `alice@student.local`
- Password: `Student123!`

## Basic workflow test

1. Register a new user.
2. Log in as that user.
3. Submit a support ticket.
4. Log out, log in as admin.
5. Open the admin panel, add a comment, set the ticket to `Resolved`.
6. Log out, log back in as the user.
7. Open the resolved ticket and submit a reopen reason.
8. Confirm the ticket status changes back to `Open`.

## Troubleshooting

### "flask: command not found"
Activate the virtualenv first: `source venv/bin/activate`.

### Reset the local database
Delete `helpdesk.db` in the project root, then re-run `flask --app run.py init-db`.

### Port 5000 already in use
Another process is listening on 5000. Kill it, or edit `run.py` to change the port.
