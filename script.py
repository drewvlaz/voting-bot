import time
import sys
import random
import subprocess

from selenium import webdriver

URL = 'https://poll.fm/10231657'

def login():
    """ configure driver settings then go to URL and login with credentials from auth.py """

    # accessed by other objects
    global driver 

    # configure chrome to be incognito and not display a window gui
    options = webdriver.ChromeOptions()
    options.add_argument('incognito')
    options.set_headless(headless=True)
    driver = webdriver.Chrome(executable_path='chromedriver_linux64/chromedriver', chrome_options=options)

    driver.get(URL)


def vote():

    target = driver.find_element_by_xpath('//*[contains(text(), "Alejandro")]')
    target.click()
    vote_btn = driver.find_element_by_xpath('//*[contains(text(), "Vote")]')
    vote_btn.click()

    driver.delete_all_cookies()
    driver.back()
    driver.refresh()


def get_time_elapsed(start_time, end_time):

    elapsed_hours = int(end_time / 60 / 60)
    elapsed_minutes = int((end_time - elapsed_hours * 60 * 60) / 60)  
    elapsed_seconds = int(end_time - elapsed_hours * 60 * 60 - elapsed_minutes * 60)

    elapsed_time = [str(elapsed_hours), str(elapsed_minutes), str(elapsed_seconds)]

    # format output
    for i in range(len(elapsed_time)):
        if len(elapsed_time[i]) == 1:
            elapsed_time[i] = "0" + elapsed_time[i] 

    time_string = f"{elapsed_time[0]}:{elapsed_time[1]}:{elapsed_time[2]}"

    return time_string


def main():

    ITERATIONS = 200
    MAX_VOTES_PER_IP = 25
    toolbar_width = MAX_VOTES_PER_IP 
    start_time = time.time()


    for i in range(ITERATIONS):
        print(f"Iteration: {i+1}/{ITERATIONS}")
        login()
        subprocess.call(['windscribe', 'connect'])
        # setup toolbar
        toolbar_space = " " * toolbar_width
        sys.stdout.write(f"[{toolbar_space}]")
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
        for i in range(MAX_VOTES_PER_IP):
            vote()
            # update the bar
            sys.stdout.write("-")
            sys.stdout.flush()
        sys.stdout.write("\n")
        driver.quit()
        subprocess.call(['windscribe', 'disconnect'])
        end_time = time.time() - start_time 
        print(f"Time Elapsed: {get_time_elapsed(start_time, end_time)}\n")


main()
