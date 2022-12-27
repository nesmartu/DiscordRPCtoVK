# DiscordRPCtoVK

Скрипт, отображающий статус активности из Discord в VK.
Работает как фоновый браузер, обновляющий статус на странице каждые n-секунд.
Делал больше для себя, возможно кому-то тоже пригодится 💁‍♂️

**Как установить?***
1. Установить [Python](https://www.python.org/ "Python")
2. Установить библиотеки из requirements.txt
Все сразу:
`pip install -r requirements.txt`
или по отдельности
`python -m pip install [packagename]`
3. Скачать [Google Chrome Portable](https://cloud.mail.ru/public/zhrz/32xGCUDrV "Google Chrome Portable") и поместить в папку chromedriver/Chrome
4. Получить токены [Discord (аутенфикации)](https://discordgid.ru/token/ "Discord (аутенфикации)") и [ВК (VK Admin)](https://vkhost.github.io/ "ВК (VK Admin)")
5. В файл config.ini вписать полученные токены.
6. Запустить программу через командную строку `py main.py` или через .bat файл launch_drpc_vk.bat

**Позже сделаю видеоинструкцию...*