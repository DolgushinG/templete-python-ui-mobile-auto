import main
from locators import PaymentPageLocators
from pages.BasePage import BasePage



class PaymentPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        for k, v in PaymentPageLocators[self.app].items():
            setattr(self, k, v)

    def fill_field(self):
        main.wait_element(self.driver, self.FIELD)
        main.fill_field(self.driver, self.FIELD, "")
