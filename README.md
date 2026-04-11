# Campus IT Help Desk

Campus IT Help Desk is a small multi-user web application for reporting and managing campus IT support issues. Regular users can create tickets and track their status. Administrators can review all tickets and update ticket statuses through server-side role checks.

## Core Features
- User registration and login
- Role-based access control with `user` and `admin`
- Ticket creation with server-side validation
- User dashboard limited to owned tickets
- Ticket detail view
- Admin panel for reviewing all tickets
- Persistent storage with PostgreSQL

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
└── run.py
```

## User Roles
### User
- Register and log in
- Create tickets
- View only their own tickets

### Admin
- Log in through the default admin account
- View all tickets
- Update ticket status

## Workflows
1. User registers, logs in, submits a ticket, and views it on the dashboard.
2. Admin logs in, reviews tickets, opens a ticket, and updates its status.

## Setup
### 1. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set environment variables
```bash
export SECRET_KEY="replace-this-secret"
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/campus_helpdesk"
```

### 4. Initialize the database and create the default admin
```bash
flask --app run.py init-db
```

### 5. Start the application
```bash
python3 run.py
```

## Default Admin Account
- Email: `admin@campus.local`
- Password: `Admin123!`
