from Pages.BasePage import BasePage
from playwright.sync_api import Page

class ContactUsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.name_field = page.get_by_placeholder("Name")
        self.email_field = page.get_by_placeholder("Email", exact=True)
        self.subject_field = page.get_by_placeholder("Subject")
        self.message_field = page.get_by_placeholder("Your Message Here")
        self.submit_button = page.get_by_role("button", name = "Submit")



    def navigate_to_contactus_page(self):
        self.navigate("/contact_us")


    def contact_us_fill(self, form_fill : dict, path: str, accept_dialog: bool = True):

        self.name_field.fill(form_fill["name"])
        self.email_field.fill(form_fill["email"])
        self.subject_field.fill(form_fill["subject"])
        self.message_field.fill(form_fill["message"])
        self.page.set_input_files("input[type='file']", path)

        handler = lambda dialog: dialog.accept() if accept_dialog else dialog.dismiss()
        self.page.once("dialog", handler)  # once() is safer than on()

        self.submit_button.click(force=True) #force click needed to bypass an ad overlay on automationexercise.com


