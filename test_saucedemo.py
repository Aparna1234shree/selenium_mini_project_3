import pytest
from saucedemo import SauceDemoAutomation


@pytest.fixture(scope="module")
def sauce_demo():
    # Setup: Create an instance of SauceDemoAutomation
    demo = SauceDemoAutomation()
    yield demo
    # Teardown: Close the browser after tests are done
    demo.close_browser()


def test_login(sauce_demo):
    # Print cookies before login
    sauce_demo.print_cookies("Cookies before login")

    # Perform login
    sauce_demo.login("standard_user", "secret_sauce")

    # Validate login by checking if redirected to the inventory page
    assert sauce_demo.driver.current_url == "https://www.saucedemo.com/inventory.html"

    # Print cookies after login
    sauce_demo.print_cookies("Cookies after login")

    # Validate that cookies are not empty after login
    cookies = sauce_demo.driver.get_cookies()
    assert len(cookies) > 0, "Cookies should not be empty after login"

    # Ensure session cookie exists
    session_cookie = next((cookie for cookie in cookies if cookie['name'] == 'session-username'), None)
    assert session_cookie is not None, "Session cookie 'session-username' should be present after login"


def test_logout(sauce_demo):
    # Perform logout
    sauce_demo.logout()

    # Validate logout by checking if back to login page
    assert sauce_demo.driver.current_url == "https://www.saucedemo.com/"


def test_cookies_after_logout(sauce_demo):
    # Print cookies after logout
    sauce_demo.print_cookies("Cookies after logout")

    # Validate that all cookies are cleared after logout
    cookies = sauce_demo.driver.get_cookies()
    assert cookies == [], "Cookies should be empty after logout"


# Negative test case1: Incorrect login credentials
def test_invalid_login(sauce_demo):
    # Attempt login with incorrect credentials
    sauce_demo.login("invalid_user", "invalid_password")

    # Validate that user is not redirected to the inventory page
    assert sauce_demo.driver.current_url != "https://www.saucedemo.com/inventory.html", \
        "User should not be redirected to the inventory page with invalid credentials"


# Negative test case2: Expect cookies before login (which shouldn't exist)
def test_invalid_cookies_before_login(sauce_demo):
    # Expecting cookies before login, which should fail as they are usually empty
    cookies = sauce_demo.driver.get_cookies()
    assert len(cookies) > 0, "There should be cookies before login (Negative test case, should fail)"


# Negative test case3: Logout URL remains on inventory page
def test_logout_failure(sauce_demo):
    # Perform login
    sauce_demo.login("standard_user", "secret_sauce")

    # Perform logout
    sauce_demo.logout()

    # Validate that user is incorrectly still on the inventory page after logout (should fail)
    assert sauce_demo.driver.current_url == "https://www.saucedemo.com/inventory.html", \
        "User should not remain on the inventory page after logout (Negative test case, should fail)"


# Negative test case4: Cookies should exist after logout (which they shouldn't)
def test_cookies_exist_after_logout(sauce_demo):
    # Perform logout
    sauce_demo.logout()

    # After logout, cookies should be cleared, but this test expects the opposite
    cookies = sauce_demo.driver.get_cookies()
    assert len(cookies) > 0, "Cookies should not be empty after logout (Negative test case, should fail)"