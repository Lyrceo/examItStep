import requests
from bs4 import BeautifulSoup
import sqlite3

class SearchEngine:
    def __init__(self, db_name="search_db.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS websites
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                url TEXT,
                                content TEXT)''')
        self.connection.commit()

    def add_website(self, link):
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')

            if "sinoptik.ua" in link:
                data = soup.find_all('div', class_='max')
                data1 = soup.find_all('p', class_='day-link')
                data2 = soup.find_all('a', class_='day-link')
            elif "auto.ria.com" in link:
                data = soup.find_all('span', class_='bold size22 green')
                data1 = soup.find_all('span', class_='blue bold')
            elif "privatbank.ua" in link:
                data = soup.find_all('div')
            else:
                data = []

            content = "\n".join([item.get_text() for item in data + data1 + data2])

            self.cursor.execute("INSERT INTO websites (url, content) VALUES (?, ?)", (link, content))
            self.connection.commit()
            print(f"Сайт {link} успішной доданий.")
        except Exception as e:
            print(f"Не вийшло додати {link}. Помилка: {e}")

    def clear_database(self):
        self.cursor.execute("DELETE FROM websites")
        self.connection.commit()
        print("База даних очіщена")

    def view_websites(self):
        self.cursor.execute("SELECT id, url FROM websites")
        websites = self.cursor.fetchall()
        print("\nСайти в бази даних:")
        for website in websites:
            print(f"{website[0]}. {website[1]}")

    def view_website_content(self, website_id):
        self.cursor.execute("SELECT url, content FROM websites WHERE id=?", (website_id,))
        result = self.cursor.fetchone()
        if result:
            print(f"\nКонтент {result[0]}:\n")
            print(result[1])
        else:
            print(f"Сайт з номером {website_id} не знайден в бази даних")

search_engine = SearchEngine()
websites_to_add = [
    "https://sinoptik.ua/",
    "https://auto.ria.com/uk/legkovie/lamborghini/?page=1",
    "https://privatbank.ua/rates-archive"
]

for website in websites_to_add:
    search_engine.add_website(website)

while True:
    print("\nМеню:")
    print("1. Додати новий сайт")
    print("2. Почищити базу даних")
    print("3. Номера Вебсайтів")
    print("4. Подивитися Вебсайти")
    print("5. Вийти")

    choice = input("Ваш вибір: ")

    if choice == '1':
        link = input("Напишіть посилання на сайт: ")
        search_engine.add_website(link)
    elif choice == '2':
        search_engine.clear_database()
        print("База даних очіщена")
    elif choice == '3':
        search_engine.view_websites()
    elif choice == '4':
        website_id_to_view = input("Напишіть номер вебсайту (номера можна подивитись в пункті 3 меню): ")
        search_engine.view_website_content(website_id_to_view)
    elif choice == '5':
        break
    else:
        print("Такого номеру нема в меню. Напишіть інший")




