import os
import time
import base64
from icecream import ic
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import selenium_utils
from selenium_utils import Browser
import langchain


def login(driver: webdriver):
    actions = ActionChains(driver)

    email_inp = driver.find_element(By.XPATH, '//input[@placeholder="Email"]')
    pass_inp = driver.find_element(By.XPATH, '//input[@placeholder="Password"]')
    submit_btn = driver.find_element(By.XPATH, "//button[text()='Log In']")

    actions.move_to_element(email_inp).click().send_keys(
        os.environ["ANKI_EMAIL"]
    ).perform()
    actions.move_to_element(pass_inp).click().send_keys(
        base64.b64decode(
            os.environ["ANKI_PASSWORD_BASE64_ENCODED"]
        ).decode("utf-8")
    ).perform()

    actions.move_to_element(submit_btn).click().perform()


def get_space_count(string: str):
    spaces=0

    for char in string:
        if char.isspace() or (char == '\t') or (char == '\xa0'):
            spaces += 1
        else:
            break

    return spaces


def get_decks(
    decks: list,
    data: list,
    idx: int, # line to check
    spaces: int, # spaces till now
    prefix: str, # prefix till now
):
    next_ind_space = 3
    while idx != len(data):
        current_line=data[idx]
        count = get_space_count(current_line)

        diff = count - spaces

        if diff == next_ind_space:
            decks.append(f"{prefix}{current_line[count:]}")

        elif diff > next_ind_space:
            idx = get_decks(
                decks=decks, 
                data=data, 
                idx=idx, 
                spaces=spaces+next_ind_space, 
                prefix=f"{decks[-1]}::",
            )

        else:
            break

        idx = idx + 1

    return idx -1


def main():
    flashcards = {}
    e = None

    driver = driver = selenium_utils.init_driver(
        user_data_dir=selenium_utils.get_profile_path(Browser.FIREFOX),
        headless=True
    )

    try:
        driver.get("https://ankiweb.net/decks")
        time.sleep(3)

        if driver.current_url == "https://ankiweb.net/account/login":
            login(driver)

        main_cont = driver.find_element(By.TAG_NAME, 'main')
        buttons = main_cont.find_elements(
            By.XPATH, "//*[@class='btn btn-link pl-0 svelte-p9sq8d']")

        notes_structure = [button.text for button in buttons if button.text.strip() != ""]

        spaces = get_space_count(notes_structure[0])

        decks = []

        get_decks(
            decks=decks,
            data=notes_structure,
            idx=0,
            spaces=spaces-3,
            prefix="",
        )
        ic(decks)

        # time.sleep(15)

    except Exception as ex:
        e=ex

    finally:
        driver.quit()

    if e:
        raise e

if __name__ == "__main__":
    main()
