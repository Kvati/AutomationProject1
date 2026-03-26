from playwright.sync_api import Page, expect

def test_testcases_page(test_cases_page):
    expect(test_cases_page.page.locator("h2.title.text-center")).to_be_visible()
    expect(test_cases_page.page.get_by_text("Below is the list of test Cases for you to practice the Automation. "
                            "Click on the scenario for detailed Test Steps:")).to_be_visible()