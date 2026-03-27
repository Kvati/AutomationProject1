import pytest
import uuid
from Pages.ContactUsPage import ContactUsPage
from Pages.HomePage import HomePage
from Pages.LoginPage import LoginPage
from playwright.sync_api import Page
from Pages.ProductDetailsPage import ProductsDetailsPage
from Pages.ProductsPage import ProductsPage
from Pages.RegisterPage import RegisterPage
from Pages.SignupPage import SignUpPage
from Pages.BasePage import BasePage
import allure


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080
        }
    }
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)

        if page is None:
            for fixture_name in item.funcargs:
                fixture_value = item.funcargs[fixture_name]
                if hasattr(fixture_value, "page"):
                    page = fixture_value.page
                    break

        if page is not None:
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )

@pytest.fixture
def login_page(page: Page):
    login_page = LoginPage(page)
    login_page.navigate_to_login_page()
    return login_page

@pytest.fixture
def signup_page(page: Page):
    signup_page = SignUpPage(page)
    signup_page.navigate_to_signup_page()
    return signup_page

@pytest.fixture
def contact_page(page: Page):
    contact_us_page = ContactUsPage(page)
    contact_us_page.navigate_to_contactus_page()
    return contact_us_page

@pytest.fixture
def register_page(page: Page, signup_page, register_user):
    signup_page.signup(username=register_user["username"], email=register_user["email"])
    return RegisterPage(page)

@pytest.fixture
def test_cases_page(page: Page):
    base_page = BasePage(page)
    base_page.navigate("/test_cases")
    return base_page

@pytest.fixture
def home_page(page: Page):
    home_page = HomePage(page)
    home_page.navigate("/")
    return home_page

@pytest.fixture
def products_page(page: Page):
    products_page = ProductsPage(page)
    products_page.navigate("/products")
    return products_page

@pytest.fixture
def product_details_page(page: Page):
    product_details_page = ProductsDetailsPage(page)
    product_details_page.navigate("/products")
    random_product_vars = product_details_page.view_random_product()
    return product_details_page, random_product_vars


@pytest.fixture
def random_user():
    return {
        "username": "user_" + uuid.uuid4().hex[:6],
        "email": f"{uuid.uuid4().hex[:8]}@test.com",
    }


