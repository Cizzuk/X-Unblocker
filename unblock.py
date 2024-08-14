import json
import os
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime

# Args
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Specifies how long to wait for a page to load if the network is slow.")
    def delay_mode(value):
        try:
            # Try to convert to an integer or a float
            return int(value) if '.' not in value else float(value)
        except ValueError:
            # If conversion fails, return the string itself
            return value
    parser.add_argument("--delay", type=delay_mode, default='normal', help="Specifies how long to wait for a page to load if the network is slow: 'slow'(5s), 'normal'(2s), 'fast'(1s), or a number in seconds. Default is 'normal'(2s).")
    args = parser.parse_args()
    
    # Set load wait time
    if args.delay == 'slow':
        load_wait = 5
    elif args.delay == 'fast':
        load_wait = 1
    elif isinstance(args.delay, (int, float)):
        load_wait = args.delay
    else:
        load_wait = 2

# Load block data
archive_file = "block.js"

if os.path.exists(archive_file):
    with open(archive_file, 'r') as file:
        data = file.read()
        block_data = json.loads(data.split('= ')[1].strip(';'))
else:
    print("You need to request an archive of your X account: https://x.com/settings/your_twitter_data/data")
    print("Please download the archive and extract the 'block.js' file to the same directory as this script.")
    raise SystemExit

driver = webdriver.Chrome()
cookie_file = "cookies.json"

# Check cookie
if os.path.exists(cookie_file):
    driver.get("https://x.com/i/flow/login")
    
    with open(cookie_file, "r") as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
else:
    print("Please log in to X manually.")
    driver.get("https://x.com/i/flow/login")
    while True:
        if "https://x.com/home" in driver.current_url:
            print("Successfully logged in.")
            break
        time.sleep(5)
    # Save cookie
    cookies = driver.get_cookies()
    with open(cookie_file, "w") as file:
        json.dump(cookies, file)

driver.get("https://x.com/home")
time.sleep(2)


### Unblock process ###
unblocked_count = 0

for block in block_data:
    unblocked_count += 1

    user_id = block['blocking']['accountId']
    user_link = f"https://x.com/i/user/{user_id}"
    
    driver.get(user_link)
    time.sleep(load_wait)

    try:
        unblock_button = driver.find_element(By.XPATH, '//span[text()="Blocked"]/..')
        unblock_button.click()
        time.sleep(0.2)

        confirm_button = driver.find_element(By.XPATH, '//span[text()="Unblock"]/..')
        confirm_button.click()
        print(f"{unblocked_count}| Unblocked user: {user_link}")
        time.sleep(load_wait)

    except Exception as e:
        print(f"{unblocked_count}| Failed unblock: {user_link}")

    # Avoid rate limit
    if unblocked_count % 80 == 0:
        current_time = datetime.now().strftime("%H:%M:%S")
        driver.get("https://x.com/settings/account")
        print(f"{current_time}| Taking a 15-minute break...")
        if unblocked_count == 80:
            print("This is a necessary cooldown to avoid X rate limit.")
        time.sleep(900)


driver.quit()
print(f"Unblocked {unblocked_count} users.")

