from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import time
from sys import platform

did = input("Did you copy the image to send ? \n      ( Y or N )\n")
if did == 'Y':
    options = Options()
    if platform == "win32":
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    numbers = []
    contacts = open("numbers.txt", "r")
    for num in contacts.read().splitlines():
        if num != "":
            numbers.append(num)
    contacts.close()
    total = len(numbers)
    print(str(total) + ' contacts are in the file')

    msg = open("message.txt", "r")
    text = msg.read()
    msg.close()

    delay = 10
    success = 0
    failure = 0

    driver = webdriver.Chrome(ChromeDriverManager().install())

    print('\n')
    driver.get('https://web.whatsapp.com')
    print('Please wait while whatsapp is loading')
    home = '//*[@id="app"]/div[1]/div[1]/div[4]/div/div/div[1]/span'
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, home)))
    sleep(3)
    # input("\nclick enter key after whatsapp is loaded")

    start_time = time.time()
    # cal = 0
    # succ = 0

    for idx, number in enumerate(numbers):
        number = number.strip()
        if number == "":
            continue
        print('\n{}/{} => Sending message to {}.'.format((idx + 1), total, number))
        try:
            url = 'https://web.whatsapp.com/send?phone=91' + number
            sent = False
            for i in range(1):
                if not sent:
                    driver.get(url)
                    try:
                        # start = time.time()
                        msg_box = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
                        img_send_desc_box = '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[2]'

                        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, msg_box)))
                        # print(' a success finding in seconds  ' + str(time.time() - start))
                        # now = time.time() - start
                        # cal = cal + now
                        # print(cal)
                        # succ = succ + 1
                        # print(succ)
                        # print('current average' + str(cal / succ))

                        msg_elem = driver.find_element(By.XPATH, msg_box)
                        msg_elem.send_keys(Keys.CONTROL, 'v')
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, img_send_desc_box)))

                        img_desc_elem = driver.find_element(By.XPATH, img_send_desc_box)

                        # add your custom message by editing these
                        img_desc_elem.send_keys(str(text))



                        img_desc_elem.send_keys(Keys.ENTER)


                    except Exception as e:
                        failure = failure + 1

                        with open(
                                "Failed.txt",
                                "a") as text_file:
                            text_file.write(number + '\n')

                        inv_url = '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[2]/div/div/div'
                        if EC.presence_of_element_located((By.XPATH, inv_url)):
                            print("User not on whatsapp")
                        else:
                            print("Failed to send message")
                        continue



                    else:

                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_3JXTQ')))
                        if EC.presence_of_element_located((By.CLASS_NAME, '_3JXTQ')):
                            sent = True
                            success = success + 1
                            print('Message sent to: ' + number)
                        else:
                            with open(
                                    "Failed.txt",
                                    "a") as text_file:
                                text_file.write(number + '\n')
                            print("Failed...........")


        except Exception as e:
            print('\n Failed to send message to ' + number)  # + str(e))
            input("Please review and click enter")

    print('\n')
    print("          ##############################################\n")
    print('                 Total contacts  ' + str(total) + '\n')
    print('                 ' + str(success) + '  Messages send successfully')
    print('                 ' + str(failure) + '  Messages Failed')
    print("\n          ##############################################")
    elapsed = time.time() - start_time

    # print("--- %s seconds ---" % elapsed)
    # print('average' + str(cal/succ))

    print("\nTime Elapsed -------- %s minutes" % round(elapsed / 60, 2))
    with open(
            "Failed.txt",
            "a") as text_file:
        text_file.write('                 Total contacts  ' + str(total) + '\n' +
                        '                 ' + str(success) + '  Messages send successfully \n' +
                        '                 ' + str(failure) + '  Messages Failed \n' +
                        '                 Time Elapsed ------- %s minutes' % round(elapsed / 60, 2) +
                        '\n----------------------------------------------------------------------------\n')
        text_file.close()

    input("\n\nClick ENTER key to stop")
else:
    print('Please go and copy the image & restart the program')
