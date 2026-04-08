# AutomationExercise Test Suite

Automated end-to-end tests for [automationexercise.com](https://automationexercise.com) built with Playwright and pytest.

## 🔧 Tech Stack
- Python 3.12
- Playwright 1.58
- pytest 9.0
- Requests
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
├── Tests/
│   ├── UITests/               # UI tests using Playwright
│   │   ├── test_login.py
│   │   ├── test_signup.py
│   │   ├── test_register.py
│   │   ├── test_homepage.py
│   │   ├── test_products.py
│   │   ├── test_productdetails.py
│   │   ├── test_cart.py
│   │   ├── test_contactus.py
│   │   ├── test_testcases.py
│   │   └── conftest.py
│   ├── APITests/              # API tests using Requests
│   │   ├── test_products.py
│   │   ├── test_auth.py
│   │   ├── test_users.py
│   │   └── conftest.py
│   └── E2E/                   # End-to-end tests
│       ├── test_user_lifecycle.py
│       └── test_user_creation_and_item_checkout.py
├── TestData/
│   └── user_test_data.py       # Shared test data
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

## 🐳 Docker

Run the full test suite in a container — no local Python or browser installation needed:
```
docker compose up
```

Run with a specific marker:
```
docker compose run tests pytest -m smoke -v
```

Allure results are written to `./allure-results` on your host machine via a volume mount.

## ▶️ Running Tests

Run all tests:
```
pytest -v
```

Run only UI tests:
```
pytest "Tests/UITests" -v
```

Run only API tests:
```
pytest "Tests/APITests" -v
```

Run only E2E tests:
```
pytest Tests/E2E -v
```

Run a specific test file:
```
pytest "Tests/UITests/test_cart.py" -v
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

## 🏷️ Test Markers

Every test is tagged with one of two markers:

| Marker | Purpose |
| --- | --- |
| `smoke` | Critical-path tests — one per module, fast sanity check |
| `regression` | Edge cases, negative paths, parametrized validations |

Run by marker:
```
pytest -m smoke -v
pytest -m regression -v
pytest -m "smoke or regression" -v
```

Markers are purely additive — all path/file/folder based run commands work exactly the same without `-m`.

## 📊 Test Report
Live Allure report: https://kvati.github.io/AutomationProject1/

## ✅ Test Coverage

### UITests
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

### APITests
| Module | Test File | Scenarios |
| --- | --- | --- |
| Products | `APITests/test_api_products.py` | Get all products, get all brands, search product, unsupported methods, missing parameters, no results |
| Auth | `APITests/test_auth.py` | Valid login, invalid credentials, missing email/password, unsupported method |
| Users | `APITests/test_users.py` | Create user, create with missing fields (xfail), delete user, update user, get user by email, invalid/missing email, duplicate user |

### E2E Tests
| Module | Test File | Scenarios |
| --- | --- | --- |
| User Lifecycle | `E2E/test_user_lifecycle.py` | Register new user, delete account, verify login blocked |
| Checkout | `E2E/test_user_creation_and_item_checkout.py` | New user creation + full checkout flow, register during checkout flow |

## 🔄 Real Environment Considerations

This project runs against a shared public test site, which imposes some constraints that would be handled differently in a real project:

**Credentials and configuration**
Sensitive values like email, password, and base URL are hardcoded. In a real environment these would be stored as environment variables or CI secrets and loaded via a config file or `os.environ`, so no credentials ever appear in source code.

**Test data**
Some tests depend on a pre-existing user account (`existing_user`) that must exist on the server before the suite runs. In a real environment, all test data would be created and torn down by the tests themselves — either through API calls in fixtures or against a database that resets between runs — making the suite fully self-contained.

**Test isolation**
Because multiple tests share the same live server, a failure in one test (e.g. an account left in a bad state) can affect others. In a real environment each test would run against its own isolated state, typically via database transactions that roll back after each test or a dedicated environment per CI run.

**Flakiness from third-party ads**
Several UI tests require workarounds (`dismiss_vignette_and_retry`) to handle ad overlays injected by the site. In a real environment the application under test would be fully controlled, so there would be no third-party interference and no need for retry logic of this kind.