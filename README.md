# DiscordRPCtoVK
🟢 Скрипт, отображающий статус активности из Discord в VK.

Работает как фоновый браузер, обновляющий статус на странице каждые n-секунд.
Делал больше для себя, возможно кому-то тоже пригодится 💁‍♂️

## Как установить?
**[Видеоинструкция](https://www.youtube.com/watch?v=3JVHG8IAb_g "Видеоинструкция")**
1. Установить [Python](https://www.python.org/downloads/ "Python")
2. Установить библиотеки из requirements.txt
Все сразу:
`pip install -r requirements.txt`
или по отдельности
`python -m pip install [packagename]`
3. Скачать и установить [Google Chrome Portable](https://sourceforge.net/projects/portableapps/files/Google%20Chrome%20Portable/GoogleChromePortable_108.0.5359.72_online.paf.exe/download "Google Chrome Portable") в папку chromedriver
4. Получить токены [Discord (аутенфикации)](https://discordgid.ru/token/ "Discord (аутенфикации)") и [ВК (VK Admin)](https://vkhost.github.io/ "ВК (VK Admin)")
5. В файл config.ini вписать полученные токены.
6.  Запустить необходимую версию*  программы можно через командную строку `py <название файла>.py` или через соответствующий .bat файл. 

*Скрипт имеет две версии: **drpc_vk_no_activity_print.py** - при работе, программа не будет выводить информацию о смене активности в консоль и **drpc_vk_with_activity_print.py** - с выводом этого статуса.

### Выход из скрипта:
Ctrl + C, после 5 секунд закрыть окно скрипта.

------------

Тестировалось на Windows 10, 11 (x64)
###### Версии браузера, драйвера и зависимостей указаны в файле versions.txt
