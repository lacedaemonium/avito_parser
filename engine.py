import json
import sqlite3
import requests
import time
import asyncio
import random
from pyppeteer import launch

while True:
    async def main():
        browser=await launch(options={'args': ['--no-sandbox']})
        page = await browser.newPage()
        await page.goto('https://www.avito.ru/web/1/js/items?categoryId=101&cd=1&s=104&p=1&params[483]=5023&pmax=15000&query=mikrotik')
        content = await page.evaluate('document.body.textContent', force_expr=True)
        await browser.close()
        
        file = open("/app/content.json", "w")
        file.write(content)
        file.close()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

    time.sleep(3)

    f = open("/app/content.json", "r")
    data = f.read()
    data = json.loads(data)
    items_list = data["catalog"]
    list_id = []

    def send_to_telegram(message):
        apiToken = '*****:A*****8'
        chatID = '-******'
        apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

        try:
            response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
            print(response.text)
        except Exception as e:
            print(e)


    for item in items_list["items"]:
        sqlite_connection = sqlite3.connect("/app/database.db")
        cursor = sqlite_connection.cursor()

        try:
            print("База данных подключена к SQLite")
            count = cursor.execute('''INSERT INTO mikrotik(item_id, main_image, images)
                  VALUES(:item_id, :main_image, :images)''', {'item_id':item["id"], 'main_image':item["images"][0]["864x648"],'images':json.dumps(item["images"])})
            sqlite_connection.commit()
            # сообщение в бота что запись вставлена (новое объявление в списке)
            time.sleep(3)
            send_to_telegram("https://avito.ru"+item["urlPath"])
            time.sleep(3)
            send_to_telegram(item["priceDetailed"]["fullString"])
            cursor.close()

        except sqlite3.Error as error:
            #здесь ошибка - не вставлено т.к. произошла ошибка (скорее всего уже есть)
            print("Ошибка: ", error)

        finally:
            if (sqlite_connection):
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")
    time.sleep(random.randint(400, 600)) 
