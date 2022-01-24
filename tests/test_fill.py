import pytest as pytest
from pages.PaymentPage import PaymentPage


@pytest.mark.usefixtures('driver')
class Test:

    def test_fill(self):
        """
        describe
        """
        payment_page = PaymentPage(self.driver)
        payment_page.fill_field()
