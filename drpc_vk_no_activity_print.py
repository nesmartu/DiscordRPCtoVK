import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs
from time import sleep
import vk_api
from configparser import ConfigParser


def print_log(log):
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    print(f"{now} >> {log}")


def vk_set_status(activity):
    try:
        api.status.set(text=activity)
    except vk_api.Captcha as captcha_error:
        print_log("Вы разбудили капчу!\n"
                  "Откройте ссылку и введите код ниже!\n"
                  )
        print_log(captcha_error.url)
        captcha = input()


def discord_to_vk_status():
    is_status_set = False
    prev_activity = ""
    while True:
        soup = bs(driver.page_source, "html.parser")
        if soup.find("div", {"class": "activityUserPopoutV2-3eKqzY activity-3uaYny"}):
            is_status_set = False
            activity_block = soup.find("div", {"class": "activityUserPopoutV2-3eKqzY activity-3uaYny"})
            buttons = activity_block.find_all('button')
            buttons_amount = len(buttons)
            texts = activity_block.findAll(text=True)
            texts.pop(0)
            if buttons_amount > 0:
                texts = texts[:len(texts) - buttons_amount]
            activity_list = [link.string for link in texts]
            curr_activity = now_playing_text + ' ' + ', '.join(activity_list)
            if prev_activity != curr_activity:
                vk_set_status(curr_activity)
            prev_activity = curr_activity
            sleep(cd)
        else:
            if not is_status_set:
                current_status = api.status.get()
                if current_status != no_act_status:
                    vk_set_status(no_act_status)
                    is_status_set = True
            sleep(cd)


if __name__ == "__main__":
    cfg_data = ConfigParser()
    cfg_data.read("config.ini", encoding="utf-8")
    d_token = cfg_data.get('data', 'd_token')
    vk_token = cfg_data.get('data', 'vk_token')
    def_status = cfg_data.get('status', 'def_status')
    no_act_status = cfg_data.get('status', 'no_activity_status')
    now_playing_text = cfg_data.get('status', 'now_playing_text')
    cd = int(cfg_data.get('status', 'cooldown'))
    api = vk_api.VkApi(token=vk_token).get_api()

    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument('log-level=3')
    options.binary_location = "chromedriver\\GoogleChromePortable\\App\\Chrome-bin\\chrome.exe"
    options.add_argument("--headless")

    driver_service = Service(executable_path=r'chromedriver\\chromedriver.exe')
    driver = webdriver.Chrome(service=driver_service, options=options)
    # driver.set_window_size(1024, 768)

    print_log("Браузер запущен!")

    driver.get('https://discord.com/login')
    script = f"setInterval(() => {{document.body.appendChild" \
             f"(document.createElement `iframe`)." \
             f"contentWindow.localStorage.token = `\"{d_token}\"`}}, 50);" \
             f"setTimeout(() => {{location.reload();}}, 2500);"
    driver.execute_script(script)
    print_log("Вход произошел успешно!")
    sleep(12)

    try:
        profile_popup = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div[1]/section/div[2]/div[1]")
        profile_popup.click()
        sleep(1)
        print_log("Скрипт готов!")
    except NoSuchElementException as e:
        print("Произошла ошибка! Попробуйте перезапустить скрипт!",
              file=sys.stderr
              )
        driver.quit()
        exit(1)

    try:
        discord_to_vk_status()
    except KeyboardInterrupt:
        print("Вы решили завершить работу скрипта. \n"
              "Подождите 5 секунд и закройте окно консоли!")
        vk_set_status(def_status)
        driver.quit()
        sys.exit(0)
