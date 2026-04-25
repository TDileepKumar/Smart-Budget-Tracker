# Smart Budget Tracker

A full-stack web application to track income, expenses, budgets, and financial insights with a clean and interactive dashboard.

---

## Features

- User Authentication (Signup/Login)
- Dashboard with:
  - Total income, expense, and balance
  - Monthly summary
  - Expense breakdown chart
- Add / Edit / Delete Transactions
- Transaction History with filters
- Analytics Page:
  - Expense distribution
  - Monthly trends
  - Top spending category
- Budget Management:
  - Set category-wise budgets
  - Track spending vs budget
- AI Assistant (Rule-based fallback):
  - Answers financial queries
  - Provides spending insights
- Export transactions as CSV

---

## 🛠️ Tech Stack

**Frontend:**
- HTML5
- CSS3 (Glassmorphism UI)
- JavaScript
- Chart.js

**Backend:**
- Python
- Flask

**Database:**
- SQLite

**Other Tools:**
- Jinja2 Templates
- python-dotenv

---

## Project Structure

    Smart-Budget-Tracker/
    |
    ├── routes/              # Application routes
    ├── services/            # Business logic
    ├── templates/           # HTML pages
    ├── static/              # Static files (CSS, JS)
    │
    ├── app.py               # Main application
    ├── database.py          # Database setup
    ├── requirements.txt     # Dependencies
    ├── render.yaml          # Deployment config
    └── README.md
    
---

## Installation & Setup

### 1. Clone the repository:

```
  git clone https://github.com/TDileepKumar/Smart-Budget-Tracker.git
  cd Smart-Budget-Tracker
```

### 2. Create virtual environment:

```
  python -m venv venv
```

#### Activate it:
- Windows:
  - ``` venv\Scripts\activate ```
- Mac/Linux:
  - ``` source venv/bin/activate ```

### 3. Install Dependencies:

``` bash
pip install -r requirements.txt
```

### 4. Run the application:

``` bash
python app.py
```

#### Open in browser:
``` bash
http://127.0.0.1:5000/
```

## Key Highlights

  - Clean UI with modern glassmorphism design
  - Modular architecture (routes + services)
  - Real-time analytics and charts
  - Secure user-based data handling
  - Scalable structure for future enhancements

## Futhur Enhancements

  - Advanced AI financial recommendations
  - Mobile responsive improvements
  - Recurring transactions
  - Email notifications
  - Multi-user dashboards

## Screenshots

## Author
Dileep Kumar
