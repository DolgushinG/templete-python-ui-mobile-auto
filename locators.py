from selenium.webdriver.common.by import By

PaymentPageLocators = {
    'ios': {
        "TEST": (By.NAME, 'TEST'),

    },
    'android': {
        "TEST": (By.XPATH, 'TEST'),
    }
}
"""
    "": (By.XPATH, ''),
    "": (By.ID, ''),

//*[@text="foo"]
//*[contains(@text, "f")] (find any element which contains the letter "f").
//*[@text="foo" or @label="foo"] (find any element whose text (Android) or label (iOS) attribute is "foo").
//*[@content-desc="foo" or @name="foo"]//*[@content-desc="bar" or @name="bar"] 
(a cross-platform accessibility label search for elements called bar that descend from elements called foo).
//ancestor::*[*[@text="foo"]][@text="bar"] (find the ancestor of a node with text "foo"; the ancestor must also have text "bar").
"""