import csv
from collections import defaultdict
from bs4 import BeautifulSoup

# Путь к файлам
csv_path = "guest.csv"
html_path = "template.html"
output_path = "index.html"

# Шаг 1: читаем CSV и собираем гостей по столам
table_guests = defaultdict(list)
with open(csv_path, encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        name = row['name'].strip()
        table = int(row['table'])
        table_guests[table].append(name)

# Шаг 2: парсим HTML
with open(html_path, encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Шаг 3: заменяем гостей
for table_num in range(1, 7):
    table_title = soup.find("div", class_="table-title", string=lambda s: s and f"Стол {table_num}" in s)
    if table_title:
        guest_list_div = table_title.find_next_sibling("div", class_="guest-list")
        guest_list_div.clear()  # очищаем существующих гостей

        for guest_name in table_guests.get(table_num, []):
            new_div = soup.new_tag("div", attrs={"class": "guest"})
            new_div.string = guest_name.upper()  # Имена большими буквами, как в оригинале
            guest_list_div.append(new_div)

# Шаг 4: сохраняем результат
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(str(soup.prettify(formatter="html")))
