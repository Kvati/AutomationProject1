# AutomationExercise Test Suite

Automated end-to-end tests for [automationexercise.com](https://automationexercise.com) built with Playwright and pytest.

## 🔧 Tech Stack
- Python 3.12
- Playwright 1.58
- pytest 9.0
- Allure Reports

## 📁 Project Structure
```
project/
├── Pages/                      # Page Object Models
│   ├── BasePage.py             # Base class with shared locators and utilities
│   ├── LoginPage.py
│   ├── SignupPage.py
│   ├── RegisterPage.py
│   ├── HomePage.py
│   ├── ProductsPage.py
│   ├── ProductDetailsPage.py
│   ├── CartPage.py
│   └── ContactUsPage.py
├── Tests/                      # Test files
│   ├── e2e/                    # End-to-end tests
│   │   ├── test_user_lifecycle.py
│   │   └── test_user_creation_and_item_checkout.py
│   ├── test_login.py
│   ├── test_signup.py
│   ├── test_register.py
│   ├── test_homepage.py
│   ├── test_products.py
│   ├── test_productdetails.py
│   ├── test_cart.py
│   ├── test_contactus.py
│   ├── test_testcases.py
│   └── conftest.py
├── Utils/
│   └── upload_test_file.txt    # File used in Contact Us upload tests
├── conftest.py                 # Root fixtures and hooks
├── pytest.ini                  # Pytest configuration
└── requirements.txt
```

## ⚙️ Setup

1. Clone the repository
   ```
   git clone https://github.com/Kvati/AutomationProject1.git
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Install browsers
   ```
   python -m playwright install
   ```

## ▶️ Running Tests

Run all tests:
```
pytest -v
```

Run a specific test file:
```
pytest Tests/test_cart.py -v
```

Run only previously failed tests:
```
pytest --lf
```

Run with Allure report:
```
pytest -v --alluredir=allure-results
allure serve allure-results
```

## 📊 Test Report
Live Allure report: https://kvati.github.io/AutomationProject1/

## ✅ Test Coverage

| Module | Test File | Scenarios |
| --- | --- | --- |
| Login | `test_login.py` | Valid login, invalid credentials, empty fields, logout |
| Signup | `test_signup.py` | Valid signup, existing email, empty fields, invalid email format |
| Registration | `test_register.py` | Valid registration, empty form, missing required field |
| Home Page | `test_homepage.py` | Page sections visible, category filtering (Women/Men/Kids), brand filtering, view product, add to cart, subscribe |
| Products | `test_products.py` | Page load, search by name, partial search, invalid search, empty search |
| Product Details | `test_productdetails.py` | Page navigation, availability/condition/brand validation, add to cart with custom quantity, invalid quantity (xfail), review form validation |
| Cart | `test_cart.py` | Empty cart, filled cart, item deletion, checkout flow, address verification, valid card payment, empty card fields, invalid card inputs (xfail) |
| Contact Us | `test_contactus.py` | Page load, valid form submission, dialog cancel, invalid/empty fields |
| Test Cases Page | `test_testcases.py` | Page load and content visibility |
| E2E — User Lifecycle | `e2e/test_user_lifecycle.py` | Register new user, delete account, verify login blocked |
| E2E — Checkout | `e2e/test_user_creation_and_item_checkout.py` | New user creation + full checkout flow, register during checkout flow |