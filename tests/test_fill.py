import pytest as pytest
from pages.PaymentPage import PaymentPage


class Test:
    @allure.epic("Example")
    @allure.feature("Example")
    @allure.title("Example")
    @allure.description("Example")
    @pytest.mark.somemark
    def test_fill(self):
        """
        describe
        """
        payment_page = PaymentPage(self.driver)
        with allure.step('Заполняем поле'):
            payment_page.fill_field('test')
