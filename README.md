# CashFlowPulse Backend

A Django REST API for personal cash flow management, featuring:
- User registration, login, and token authentication
- Income and expense tracking (with recurring support)
- Cashflow prediction for the next 30 days
- Password reset and update endpoints
- Swagger and Redoc API documentation

## Features
- **User Auth:** Register, login (token/session), password reset/update
- **Income/Expense CRUD:** Track, update, and delete your financial records
- **Recurring Transactions:** Mark incomes/expenses as recurring monthly
- **Cashflow Prediction:** `/predict-cashflow/` endpoint projects your balance for the next 30 days
- **API Docs:** Swagger UI at `/swagger/`, Redoc at `/redoc/`

## Setup
1. **Clone the repo:**
   ```bash
   git clone https://github.com/sahelii/creditFlowPulse.git
   cd creditFlowPulse
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # Or manually: pip install django djangorestframework drf-yasg psycopg2-binary
   ```
3. **Configure PostgreSQL:**
   - Update `CashFlowPulse/settings.py` with your DB credentials.
   - Create the database in PostgreSQL.
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints
- **Register:** `POST /register/` (username, email, password)
- **Login (token):** `POST /api-token-auth/` (username, password)
- **Password Reset:** `POST /password-reset/` (email)
- **Password Update:** `POST /password-update/` (email, new_password, [old_password])
- **Income/Expense CRUD:** `/api/incomes/`, `/api/expenses/`
- **Cashflow Prediction:** `GET /predict-cashflow/`
- **Docs:** `/swagger/` (Swagger UI), `/redoc/` (Redoc)

## Notes
- All sensitive endpoints require authentication (Token in `Authorization` header).
- Recurring transactions repeat monthly on the same day.
- For password reset emails, configure Django's email backend in `settings.py`.

---

**Made with Django, DRF, and ❤️ by [sahelii](https://github.com/sahelii)** 