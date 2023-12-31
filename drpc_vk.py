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

cfg_data = ConfigParser()
cfg_data.read("config.ini", encoding="utf-8")
d_token = cfg_data.get('data', 'discord_token')
vk_token = cfg_data.get('data', 'vk_token')
def_status = cfg_data.get('settings', 'def_status')
no_act_status = cfg_data.get('settings', 'no_activity_status')
now_playing_text = cfg_data.get('settings', 'now_playing_text')
cd = int(cfg_data.get('settings', 'cooldown'))
cd_captcha = int(cfg_data.get('settings', 'cd_captcha'))
activity_output = cfg_data.get('settings', 'activity_output')
manual_captcha_input = cfg_data.get('settings', 'manual_captcha_input')
# activity_output = bool(cfg_data.get('settings', 'activity_output'))
# manual_captcha_input = bool(cfg_data.get('settings', 'manual_captcha_input'))


def print_log(log):
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    print(f"{now} >> {log}")


def vk_set_status(activity):
    try:
        api.status.set(text=activity)
    except vk_api.Captcha as captcha_error:
        print_log("Вы разбудили капчу!")
        if manual_captcha_input == "True":
            print_log("Откройте ссылку и введите код ниже!\n")
            print_log(captcha_error.url)
            captcha = input()
        else:
            sleep(cd_captcha)

def discord_to_vk_status():
    is_status_set = False
    prev_activity = ""
    while True:
        soup = bs(driver.page_source, "html.parser")
        if soup.find("div", {"class": "activityUserPopoutV2__32328 activity__20c1e"}):
            is_status_set = False
            activity_block = soup.find("div", {"class": "activityUserPopoutV2__32328 activity__20c1e"})
            buttons = activity_block.find_all('button')
            buttons_amount = len(buttons)
            texts = activity_block.findAll(string=True)
            # texts.pop(0)
            if buttons_amount > 0:
                texts = texts[:len(texts) - buttons_amount]
            activity_list = [link.string for link in texts]
            if "Spotify" in activity_list[0]:
                activity_list.pop()
                activity_list.pop()
                if "on " and "by " in activity_list:
                    activity_list.remove("by ")
                    activity_list.remove("on ")
                curr_activity = now_playing_text + f" {activity_list[0]}: {activity_list[2]} - {activity_list[1]}"
            else:
                playing_text = activity_list[0]
                activity_list.pop(0)
                playing_text = playing_text.split(' ', 1)[0]
                curr_activity = now_playing_text + f" {playing_text}: " + ', '.join(activity_list)
            if prev_activity != curr_activity:
                if activity_output == "True":
                    print_log("Активность изменилась!")
                vk_set_status(curr_activity)
                if activity_output == "True":
                    print_log(curr_activity)
                    print_log("Статус обновлен!")
            prev_activity = curr_activity
            sleep(cd)
        else:
            if not is_status_set:
                current_status = api.status.get()
                if current_status != no_act_status:
                    vk_set_status(no_act_status)
                    api.account.setOnline(voip=1)
                    if activity_output == "True":
                        print_log("Статус возвращен!")
                    is_status_set = True
                if activity_output == "True":
                    print_log("Активности нет...")
            else:
                if activity_output == "True":
                    print_log("...")
            sleep(cd)


if __name__ == "__main__":
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
