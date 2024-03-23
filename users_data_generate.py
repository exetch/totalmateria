import pandas as pd
from faker import Faker
import random

def generate_name_and_surname(gender):
    if gender == "male":
        name = random.choice(russian_names["male"])
        surname = name + random.choice(["ов", "ев", "ин"])
    else:
        name = random.choice(russian_names["female"])
        surname = name + random.choice(["ова", "ева", "ина"])

    return name, surname

if __name__ == "__main__":
    fake = Faker('ru_RU')

    russian_names = {
        "male": [
            "Александр", "Дмитрий", "Максим", "Сергей", "Андрей",
            "Алексей", "Артем", "Илья", "Кирилл", "Михаил",
            "Никита", "Матвей", "Роман", "Егор", "Арсений",
            "Иван", "Денис", "Евгений", "Даниил", "Тимофей"
        ],
        "female": [
            "Анна", "Мария", "Елена", "Дарья", "Алина",
            "Ирина", "Екатерина", "Наталья", "Марина", "Виктория",
            "Светлана", "Ольга", "Юлия", "Татьяна", "Анастасия",
            "Ксения", "Елизавета", "Александра", "Валерия", "Полина"
        ]
    }

    cities_base_postcodes = {
        "Москва": "101",
        "Санкт-Петербург": "190",
        "Новосибирск": "630",
        "Екатеринбург": "620",
        "Казань": "420",
        "Нижний Новгород": "603",
        "Челябинск": "454",
        "Самара": "443",
        "Омск": "644",
        "Ростов-на-Дону": "344",
        "Уфа": "450",
        "Красноярск": "660",
        "Воронеж": "394",
        "Пермь": "614",
        "Волгоград": "400",
        "Краснодар": "350",
        "Саратов": "410",
        "Тюмень": "625",
        "Тольятти": "445",
        "Ижевск": "426",
    }

    users_data = []

    for _ in range(100):
        gender = random.choice(["male", "female"])
        if gender == "male":
            name = random.choice(russian_names["male"])
            surname = fake.last_name_male()
        else:
            name = random.choice(russian_names["female"])
            surname = fake.last_name_female()
        city, base_postcode = random.choice(list(cities_base_postcodes.items()))
        full_postcode = f"{base_postcode}{random.randint(100, 999)}"
        user = {
            "Name": name,
            "Surname": surname,
            "Company": fake.company(),
            "City": city,
            "Postcode": full_postcode,
            "Phone Number": fake.bothify(text='+7 (9##) ###-####'),
        }
        users_data.append(user)

    users_df = pd.DataFrame(users_data)

users_df.to_excel("users_data.xlsx", index=False)
