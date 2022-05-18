from selenium.webdriver.common.by import By

from main import select_element


class PaymentPageLocators:
    """
    FIRST ARGUMENT IOS
    SECOND ARGUMENT ANDROID
    """
    # TITLE
    # ====================================  IOS  ================================= ANDROID ================
    PAYMENT_FIELD = select_element((By.XPATH, 'SELECTOR'),
                                 (By.XPATH, 'SELECTOR'))

"""
    " = (By.XPATH, ''),
    " = (By.ID, ''),

//*[@text="foo"]
//*[contains(@text, "f")] (find any element which contains the letter "f").
//*[@text="foo" or @label="foo"] (find any element whose text (Android) or label (iOS) attribute is "foo").
//*[@content-desc="foo" or @name="foo"]//*[@content-desc="bar" or @name="bar"] 
(a cross-platform accessibility label search for elements called bar that descend from elements called foo).
//ancestor::*[*[@text="foo"]][@text="bar"] (find the ancestor of a node with text "foo"; the ancestor must also have text "bar").
"""
