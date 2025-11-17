# Hotel POS System 🏨

A comprehensive Point-of-Sale system for five-star Indian restaurants with role-based authentication, real-time order management, and bill generation.

## Features ✨

### 🔐 Role-Based Access Control
- **Waiter Portal**: Create orders, manage menu items, edit cart
- **Kitchen Portal**: View active orders, update preparation status
- **Reception Portal**: Table statistics, order overview, bill generation

### 🍽️ Indian Restaurant Menu
- 50+ authentic dishes across 7 categories
- Appetizers, Tandoori, Curries, Biryanis, Breads, Desserts, Beverages
- Vegetarian/Vegan indicators
- Spice level indicators
- Category-organized menu display

### 📊 Reception Dashboard
- Real-time table occupancy status
- Active vs. closed orders statistics
- Table-wise order mapping
- Status breakdown by order state

### 🧾 Advanced Bill Management
- PDF bill preview before closing
- Print functionality
- Email bill option (console backend for development)
- Detailed invoice with itemized breakdown

### 🎨 Modern UI/UX
- Gradient login with quick-login buttons
- Responsive card-based design
- Real-time status updates
- Auto-refresh for kitchen and reception
- Modal dialogs for bill preview

## Tech Stack 🛠️

**Frontend:**
- React 18.2.0
- Fetch API for backend communication
- CSS Variables for theming

**Backend:**
- Django 5.2.5
- Django REST Framework
- Token Authentication
- ReportLab for PDF generation
- SQLite (development) / PostgreSQL (production)

## Installation & Setup 🚀

### Prerequisites
- Python 3.13+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Create and activate virtual environment:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. **Install dependencies:**
```powershell
cd backend
pip install -r requirements.txt
```

3. **Run migrations:**
```powershell
python manage.py migrate
```

4. **Populate database with sample data:**
```powershell
python manage.py populate_menu
```
This creates:
- Sample users (waiter1, chef1, reception1)
- 50+ Indian menu items
- Menu categories

5. **Start development server:**
```powershell
python manage.py runserver
```
Backend runs at `http://127.0.0.1:8000/`

### Frontend Setup

1. **Install dependencies:**
```powershell
cd frontend
npm install
```

2. **Start development server:**
```powershell
npm start
```
Frontend runs at `http://localhost:3000/`

## Default Login Credentials 🔑

| Role | Username | Password |
|------|----------|----------|
| Waiter | waiter1 | waiter123 |
| Chef | chef1 | chef123 |
| Reception | reception1 | reception123 |

## API Endpoints 📡

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/me/` - Current user info

### Menu
- `GET /api/menu/` - List all menu items
- `GET /api/menu/categories/` - List menu categories

### Orders
- `GET /api/orders/` - List all orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Order details
- `POST /api/orders/{id}/status/` - Update order status
- `GET /api/orders/{id}/bill/` - Get bill preview (PDF base64)
- `POST /api/orders/{id}/bill/` - Email bill

### Statistics
- `GET /api/tables/stats/` - Table occupancy and order statistics

## Project Structure 📁

```
try1(17-11-25)/
├── backend/
│   ├── backend/
│   │   ├── settings.py       # Django settings
│   │   ├── urls.py           # Main URL configuration
│   │   └── wsgi.py
│   ├── pos/
│   │   ├── models.py         # Database models
│   │   ├── serializers.py    # DRF serializers
│   │   ├── views.py          # API endpoints
│   │   ├── urls.py           # App URL routes
│   │   ├── admin.py          # Django admin config
│   │   └── management/
│   │       └── commands/
│   │           └── populate_menu.py
│   ├── db.sqlite3            # SQLite database (gitignored)
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.js          # Authentication UI
│   │   │   ├── WaiterPortal.js   # Order creation
│   │   │   ├── KitchenPortal.js  # Kitchen view
│   │   │   └── ReceptionPortal.js # Reception dashboard
│   │   ├── services/
│   │   │   └── api.js            # API communication layer
│   │   ├── App.js                # Main app component
│   │   ├── index.js              # Entry point
│   │   └── theme.css             # Global styles
│   ├── package.json
│   └── README.md
├── .gitignore
└── README.md
```

## Development Notes 📝

### CORS Configuration
- CORS enabled for `localhost:3000` and `localhost:3001`
- CSRF middleware disabled for token-based API authentication

### Email Configuration
- Uses Django console email backend for development
- Emails are printed to console instead of sent
- For production, configure SMTP in `settings.py`

### Database
- SQLite for development (included in `.gitignore`)
- PostgreSQL support via `DATABASE_URL` environment variable
- Run `populate_menu` management command after migrations

## Docker Support 🐳

```powershell
docker-compose up --build
```

Exposes:
- Backend on port 8000
- PostgreSQL database

## License 📄

This project is for educational purposes.

## Contributing 🤝

Pull requests are welcome. For major changes, please open an issue first.

