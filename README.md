# Campus IT Help Desk

Campus IT Help Desk is a multi-user web application for reporting and managing campus IT support issues. Regular users can create tickets, track ticket status, and post follow-up comments. Administrators can review all tickets, respond to users, and update ticket statuses through server-side role-based access control.

## Submission-Oriented Summary
This project is intentionally scoped for a security analysis handoff. It is small enough to understand in one sitting, but complete enough to provide realistic attack surface in the areas of authentication, authorization, form input handling, route protection, and persistent data storage.

## Core Features
- User registration and login
- Role-based access control with `user` and `admin`
- Ticket creation with server-side validation
- Ticket detail page with comment / reply thread
- Reopen resolved tickets with a short reason
- User dashboard limited to owned tickets
- Admin panel for all tickets, with status filtering
- Intentionally weak area for analysis: no rate limiting and minimal validation on the reopen form
- SQLite-backed persistent storage by default (Postgres supported via `DATABASE_URL`)
- CLI commands for database setup and demo data seeding

## Technology Stack
- Backend: Flask
- Database: SQLite by default (file-based, zero external deps). PostgreSQL optional via `DATABASE_URL`.
- ORM: Flask-SQLAlchemy / SQLAlchemy
- Authentication: Session-based login
- Password Storage: Werkzeug password hashing
- Frontend: Jinja templates + plain CSS

## Project Structure
```text
campus_it_help_desk/
├── app/
│   ├── __init__.py
│   ├── admin.py
│   ├── auth.py
│   ├── cli.py
│   ├── models.py
│   ├── routes.py
│   ├── utils.py
│   ├── static/
│   │   └── css/
│   │       └── styles.css
│   └── templates/
│       ├── admin_panel.html
│       ├── base.html
│       ├── dashboard.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── submit_ticket.html
│       └── ticket_detail.html
├── .env.example
├── AI_USAGE.md
├── requirements.txt
├── run.py
├── launch.command          # macOS double-click launcher (shell script)
└── HelpDesk.app/           # macOS .app bundle wrapper with custom icon
    └── Contents/
        ├── Info.plist
        ├── MacOS/HelpDesk
        └── Resources/icon.icns
```

## Data Model
### `users`
Stores account information and role assignment.
- `id`
- `username`
- `email`
- `password_hash`
- `role`
- `created_at`

### `tickets`
Stores help desk requests submitted by users.
- `id`
- `title`
- `category`
- `priority`
- `description`
- `status`
- `user_id`
- `created_at`
- `updated_at`

### `ticket_comments`
Stores replies between users and administrators on each ticket.
- `id`
- `ticket_id`
- `user_id`
- `content`
- `created_at`

## User Roles
### User
- Register and log in
- Create tickets
- View only their own tickets
- Add comments to their own tickets
- Reopen their own resolved tickets with a reason

### Admin
- Log in through the default seeded admin account
- View all tickets
- Update ticket status
- Add comments / replies to any ticket
- Filter ticket list by status
- Reopen any resolved ticket during support follow-up

## Required Forms
1. **Registration form**: stores username, email, and password hash.
2. **Login form**: validates user credentials and starts a session.
3. **Ticket submission form**: stores title, category, priority, and description.
4. **Comment form**: stores ticket replies linked to both ticket and user.
5. **Reopen form**: stores a reopen reason as a ticket comment and changes a resolved ticket back to `Open`.

## Distinct Views / Pages
- Landing page
- Login page
- Register page
- User dashboard
- Submit ticket page
- Ticket detail page
- Admin panel

## End-to-End Workflows
### Workflow 1: User submits a support ticket
1. A new user registers an account.
2. The user logs in.
3. The user opens the ticket submission page.
4. The user submits a ticket with category, priority, and description.
5. The application validates the input and writes the ticket to the database.
6. The user is redirected to the ticket detail page and later sees the ticket on the dashboard.

### Workflow 2: Admin reviews and updates a ticket
1. An admin logs in.
2. The admin opens the admin panel and reviews submitted tickets.
3. The admin opens a ticket detail page.
4. The admin updates the ticket status or posts a reply.
5. The application writes the update to the database.
6. The user later logs in and sees the updated status and comment thread.

### Workflow 3: User reopens a resolved ticket
1. A user logs in and opens a resolved ticket they own.
2. The user enters a reason in the reopen form.
3. The server confirms the user owns the ticket or is an admin.
4. The application changes the ticket status back to `Open`.
5. The reopen reason is stored as a ticket comment.
6. The updated ticket appears on the dashboard for continued follow-up.

## Security-Relevant Design Points
This project intentionally includes features that can be analyzed by another team:
- Session-based authentication
- Role-restricted routes
- Server-side authorization checks for ticket ownership
- Form input validation
- Persistent relational data storage
- Multi-step user / admin interaction flows

## Setup Instructions

### Quickest path (macOS) — double-click launcher

The repo ships with a one-click launcher so reviewers don't have to touch the terminal.

1. Clone or download the repo into a folder (e.g. `~/Desktop/it_help_desk`).
2. Double-click **`HelpDesk.app`** (preferred — has a custom icon) or **`launch.command`** in the project folder.
3. A Terminal window opens and the launcher will:
   - clear macOS quarantine on the project files,
   - create a virtual environment under `venv/`,
   - install dependencies from `requirements.txt`,
   - run `flask --app run.py init-db` to create `helpdesk.db` and the default admin,
   - start the Flask server and open `http://127.0.0.1:5000` in your browser.
4. To stop the app, press `Ctrl+C` in the Terminal window.

**First-time gotcha — Gatekeeper quarantine.** macOS may block the launcher because it was downloaded from the internet. If double-clicking does nothing, open Terminal once and run:

```bash
cd "$HOME/Desktop/it_help_desk" && chmod +x launch.command && xattr -cr launch.command 2>/dev/null; open launch.command
```

After that, double-click works for every subsequent run.

**What's in the launcher bundle:**

- `launch.command` — the shell script that does setup + run.
- `HelpDesk.app/` — a tiny macOS `.app` bundle that wraps `launch.command` so it shows a custom icon in Finder. It just calls `open -a Terminal launch.command` under the hood.

The launcher is idempotent: re-running it reuses `venv/`, re-installs any missing dependencies, and re-runs `init-db` (a no-op if the database already exists).

### Manual setup (any OS)

If you're not on macOS, or you'd rather run things by hand:

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate            # Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database and create the default admin:
   ```bash
   flask --app run.py init-db
   ```
4. Optional: seed demo data (creates Alice + sample tickets):
   ```bash
   flask --app run.py seed-demo
   ```
5. Start the application:
   ```bash
   python3 run.py
   ```

Then open `http://127.0.0.1:5000` in your browser.

### Using PostgreSQL instead of SQLite (optional)

By default the app uses SQLite — `helpdesk.db` is created in the project root, no external database required.

To use PostgreSQL instead, copy `.env.example` to `.env` and set `DATABASE_URL`:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/campus_helpdesk
```

Install the Postgres driver in the same venv:

```bash
pip install psycopg2-binary
```

Then run `flask --app run.py init-db` as above. The launcher reads `.env` automatically, so the double-click flow works for Postgres too.

## Demo Accounts
### Default admin
- Email: `admin@campus.local`
- Password: `Admin123!`

### Seeded demo user
Available after running `flask --app run.py seed-demo`:
- Email: `alice@student.local`
- Password: `Student123!`
