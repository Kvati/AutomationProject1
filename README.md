# AutomationExercise Test Suite

Automated end-to-end tests for [automationexercise.com](https://automationexercise.com) built with Playwright and pytest.

## 🔧 Tech Stack
- Python 3.12
- Playwright
- pytest
- Allure Reports

## 📁 Project Structure
project/
├── Pages/          # Page Object Models
├── Tests/          # Test files
├── Utils/          # Helper files
├── conftest.py     # Root fixtures
└── pytest.ini      # Pytest configuration

## ⚙️ Setup

1. Clone the repository
   git clone https://github.com/Kvati/AutomationProject1.git

2. Install dependencies
   pip install -r requirements.txt

3. Install browsers
   python -m playwright install

## ▶️ Running Tests

Run all tests:
   pytest -v

Run with Allure report:
   pytest -v --alluredir=allure-results
   allure serve allure-results

## 📊 Test Report
Live Allure report: https://kvati.github.io/AutomationProject1/

## ✅ Test Coverage
- Login (valid, invalid, empty fields, logout)
- Signup (valid, invalid, empty fields)
- Registration (valid, invalid, empty fields)
- Contact Us form (valid, invalid, dialog handling)
- Test Cases page
