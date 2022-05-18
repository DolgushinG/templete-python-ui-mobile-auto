import main
from locators import PaymentPageLocators
from pages.BasePage import BasePage



class PaymentPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # singletone
        # for k, v in PaymentPageLocators[self.app].items():
        #     setattr(self, k, v)

    def fill_field(self, text):
        main.fill_field(self.driver, PaymentPageLocators.FIELD, text)
