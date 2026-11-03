from playwright.sync_api import Page, expect
from consts import REGISTRATION_FORM, SUBMIT_MESSAGES

FILE_PATH = "file:///C:/Users/user1/Documents/Projects/MyTest/playwright_qa/registration_form.html"

def test_registration_form(page: Page):
    # Navigate to the local registration form
    page.goto(FILE_PATH)
    printAccessibilityTree(page)

    page.pause()

    fillInFullForm(page)
    fillInPreferences(page)
    validateResetForm(page)
    fillInFullForm(page)      
    fillInPreferences(page)    
    validateSubmitForm(page)
    pass

def test_header(page: Page):
    page.goto(FILE_PATH)
    checkRegistrationLink(page)
    # testPreferencesLink(page)
    checkHelpLink(page)
    checkPlaywrightDocsLink(page)   # תוקן: הוסרה ההערה, והקישור החיצוני אחרון

def fillInFullForm(page):
    #TODO: Fill in the first name
    fillInFirstName(page, "John")

    #TODO: Fill in the last name
    fillInLastName(page, "Ohayon")

    #TODO: Fill in the email
    fillInEmail(page, "your@email.com")

    #TODO: Fill in the email confirmation
    fillInEmailConfirmation(page, "your@email.com")

    #TODO: Fill in the password
    fillInPassword(page, "yourpassword")

    #TODO: Fill in the phone number
    fillInPhoneNumber(page, "+972-54-4746095")

    #TODO: Fill in the date of birth
    fillInDateOfBirth(page, "1990-01-01")

    #TODO: Select the country
    selectCountry(page, "Israel")

    #TODO: Fill in the city
    fillInCity(page, "Beer-Sheva")

    #TODO: Select the gender
    selectGender(page, "Female")

def printAccessibilityTree(page):
    pageAccesibility = page.locator("body").aria_snapshot()
    print(f"pageAccesibility: {pageAccesibility}")

def fillInFirstName(page, firstName):
    #By role, preferred method
    page.get_by_role("textbox", name="First name").fill(firstName)

def fillInLastName(page, lastName):
    #By role, preferred method
    page.get_by_role("textbox", name="Last name").fill(lastName)

def fillInEmail(page, email):
    page.get_by_role("textbox", name="Email address *", exact=True).fill(email)

def fillInEmailConfirmation(page, email):
    page.get_by_role("textbox", name="Confirm email address *", exact=True).fill(email)

def fillInPassword(page, password):
    page.get_by_role("textbox", name="Password *").fill(password)

def fillInPhoneNumber(page, phone):
    page.get_by_role("textbox", name="Phone number").fill(phone)

def fillInDateOfBirth(page, dateOfBirth):
    #By label, preferred method
    datePicker = page.get_by_label("Date of birth")
    datePicker.fill(dateOfBirth)
    datePicker.scroll_into_view_if_needed()
    datePicker.highlight()

def selectCountry(page, country):
    page.get_by_role("combobox", name="Country *").select_option(country)

def fillInCity(page, city):
    page.get_by_role("textbox", name="City").fill(city)

def selectGender(page, gender):
    page.get_by_role("radio", name=gender, exact=True).check()

def goToPreferences(page):
    page.get_by_role("link", name="Preferences").click()
    expect(page.get_by_role("heading", name="Preferences", level=3)).to_be_visible()


def selectYearsOfExperience(page, yearsIndex):
    # בחירה לפי מיקום (0=Select, 1=Less than 1 year, 2=1-2, 3=3-5, 4=6+)
    page.get_by_role("combobox", name="Years of experience").select_option(index=yearsIndex)

def selectFavoriteBrowser(page, browser):
    page.get_by_role("combobox", name="Favorite browser").select_option(browser)

def checkTopic(page, topic):
    page.get_by_role("checkbox", name=topic, exact=True).check()

def selectContactMethod(page, method):
    page.get_by_role("radio", name=method, exact=True).check()

def checkNewsletter(page):
    page.get_by_role("checkbox", name="Subscribe to the monthly QA newsletter").check()

def checkTerms(page):
    page.get_by_role("checkbox", name="I agree to the terms and conditions *", exact=True).check()

def fillInPreferences(page):
    goToPreferences(page)
    selectYearsOfExperience(page, 3)
    selectFavoriteBrowser(page, "Chromium")
    checkTopic(page, "Test automation")
    checkTopic(page, "API testing")
    selectContactMethod(page, "Phone")
    checkNewsletter(page)
    checkTerms(page)


def checkRegistrationLink(page):
    registrationLink = page.get_by_role("link", name="Registration")
    registrationLink.scroll_into_view_if_needed()
    registrationLink.highlight()
    registrationLink.click()

   
    expect(page.get_by_role("heading", name="Registration details", level=2)).to_be_visible()



def validateSubmitForm(page):
    page.get_by_role("button", name="Submit registration").click()
    expect(page.get_by_role("status")).to_have_text(SUBMIT_MESSAGES["success"])


def validateResetForm(page):
    page.get_by_role("button", name="Reset form").click()
    expect(page.get_by_role("textbox", name="First name")).to_have_value("")
    expect(page.get_by_role("textbox", name="Last name")).to_have_value("")
    expect(page.get_by_role("textbox", name="City")).to_have_value("")


def checkHelpLink(page):
    helpLink = page.get_by_role("link", name="Help")
    helpLink.scroll_into_view_if_needed()
    helpLink.highlight()
    helpLink.click()

    printAccessibilityTree(page)
    dialog = page.get_by_role("dialog", name=REGISTRATION_FORM["modalHeaderText"])
    expect(dialog).to_be_visible()
    expect(dialog.get_by_role("heading", level=2, name=REGISTRATION_FORM["modalHeaderText"])).to_be_visible()

    
    expect(dialog.get_by_text("Complete all required fields")).to_be_visible()

    dialogOkButton = dialog.get_by_role("button", name=REGISTRATION_FORM["modalButtonText"])
    expect(dialogOkButton).to_be_visible()
    expect(dialogOkButton).to_be_enabled()
    dialogOkButton.click()
    expect(dialog).to_be_hidden()


def checkPlaywrightDocsLink(page):
    link = page.get_by_role("link", name="Playwright documentation")
    expect(link).to_be_visible()
    expect(link).to_have_attribute("href", "https://playwright.dev/")