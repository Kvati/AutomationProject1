from Pages.BasePage import BasePage
from playwright.sync_api import Page

class ContactUsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.navigate("https://automationexercise.com/contact_us")

        self.name_field = page.get_by_placeholder("Name")
        self.email_field = page.get_by_placeholder("Email")
        self.subject_field = page.get_by_placeholder("Subject")
        self.message_field = page.get_by_placeholder("Your Message Here")
        self.submit_button = page.get_by_role("button", name = "Submit")



    def contact_us_fill(self, form_fill : dict, path: str):

        self.name_field.fill(form_fill["Name"])
        self.email_field.fill(form_fill["Email"])
        self.subject_field.fill(form_fill["Subject"])
        self.message_field.fill(form_fill["Message"])
        self.page.set_input_files("input[type='file']", path)

        self.submit_button.click()