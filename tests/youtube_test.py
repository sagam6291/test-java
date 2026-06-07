import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--lang=en-US')
    drv = webdriver.Chrome(options=options)
    drv.set_page_load_timeout(60)
    yield drv
    drv.quit()


def _save_screenshot(drv, name):
    try:
        os.makedirs('screenshots', exist_ok=True)
        path = os.path.join('screenshots', f'{name}_{int(time.time())}.png')
        drv.save_screenshot(path)
        print(f'Saved screenshot: {path}')
    except WebDriverException as e:
        print(f'Screenshot failed: {e}')


def test_youtube_navigate_subscriptions_then_movies(driver):
    wait = WebDriverWait(driver, 30)
    try:
        # Step 1: Navigate to YouTube
        driver.get('https://www.youtube.com/')
        wait.until(EC.title_contains('YouTube'))
        assert 'youtube.com' in driver.current_url.lower(), \
            f'Expected youtube.com in URL, got {driver.current_url}'

        # Step 2: Click Subscriptions in the side/guide menu
        subscriptions_xpath = (
            "//tp-yt-paper-item[.//yt-formatted-string[normalize-space()='Subscriptions']]"
            " | //a[@title='Subscriptions']"
            " | //ytd-guide-entry-renderer[.//yt-formatted-string[normalize-space()='Subscriptions']]"
        )
        subscriptions_el = wait.until(
            EC.element_to_be_clickable((By.XPATH, subscriptions_xpath))
        )
        subscriptions_el.click()

        wait.until(EC.url_contains('/feed/subscriptions'))
        wait.until(EC.title_contains('Subscriptions'))
        assert '/feed/subscriptions' in driver.current_url, \
            f'Expected subscriptions URL, got {driver.current_url}'
        assert 'Subscriptions' in driver.title, \
            f'Expected Subscriptions in title, got {driver.title}'

        # Step 3: Click Movies in the side/guide menu
        movies_xpath = (
            "//tp-yt-paper-item[.//yt-formatted-string[normalize-space()='Movies']]"
            " | //a[@title='Movies']"
            " | //ytd-guide-entry-renderer[.//yt-formatted-string[normalize-space()='Movies']]"
        )
        movies_el = wait.until(
            EC.element_to_be_clickable((By.XPATH, movies_xpath))
        )
        movies_el.click()

        wait.until(EC.url_contains('/feed/storefront'))
        wait.until(EC.title_contains('Movies'))
        assert '/feed/storefront' in driver.current_url, \
            f'Expected storefront URL, got {driver.current_url}'
        assert 'Movies' in driver.title, \
            f'Expected Movies in title, got {driver.title}'

    except (TimeoutException, AssertionError, WebDriverException) as e:
        _save_screenshot(driver, 'youtube_nav_failure')
        raise
