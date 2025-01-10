import tkinter as tk
from tkinter import messagebox
import json
import os
from tkinter import ttk

# Загрузка данных из файла
def load_data(filename, default_data):
    if not os.path.exists(filename):  # Проверяем, существует ли файл
        save_data(filename, default_data)  # Если файла нет, создаем его с начальными данными
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# Сохранение данных в файл
def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Начальные данные
default_population_data = []
default_cars_data = []  # Пустой список автомобилей на старте

# Предопределенные районы города
predefined_districts = ["", "Центральный", "Южный", "Северный", "Западный", "Восточный"]

# Валидация возраста и года
def is_valid_age(age):
    return age.isdigit() and 0 <= int(age) <= 120

def is_valid_year(year):
    return year.isdigit() and 1900 <= int(year) <= 2025

# Проверка на заполненность всех обязательных полей
def are_fields_filled(input_data):
    return all(value != "" for value in input_data.values())

# Добавление записи о населении
def add_person(data, surname, name, patronymic, age, district):
    if district not in predefined_districts:  # Проверка, что район существует
        raise ValueError("Выбран неверный район города.")
    new_person = {
        'surname': surname,
        'name': name,
        'patronymic': patronymic,
        'age': int(age),
        'district': district
    }
    data.append(new_person)
    return data

# Добавление автомобиля
def add_car(cars, make, model, year, number, district):
    new_car = {
        'make': make,
        'model': model,
        'year': int(year),
        'number': number,
        'district': district
    }
    cars.append(new_car)
    return cars

# Основное окно приложения
class CityDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Банк данных города")

        # Установка стиля для ttk
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=8, relief="flat")
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TCombobox", font=("Arial", 12), padding=8)
        self.style.configure("highlighted.TCombobox", font=("Arial", 12), padding=8, background="#4CAF50")  # Новый стиль для выделения
        
        # Загрузка данных (если нет, то с авто-генерацией файлов при их отсутствии)
        self.population_data = load_data('population.json', default_population_data)
        self.cars_data = load_data('cars.json', default_cars_data)

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        self.header_label = tk.Label(self.root, text="Банк данных города", font=("Arial", 18, "bold"), fg="white", bg="#444444")
        self.header_label.pack(pady=20, fill="x")

        # Раздел для добавления данных
        self.add_data_frame = tk.Frame(self.root, padx=20, pady=20, bg="#333333")
        self.add_data_frame.pack(pady=10, fill='x', padx=20)

        self.add_person_button = ttk.Button(self.add_data_frame, text="Добавить жителя", command=self.add_person)
        self.add_person_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.add_car_button = ttk.Button(self.add_data_frame, text="Добавить автомобиль", command=self.add_car)
        self.add_car_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Статистика
        self.stats_frame = tk.Frame(self.root, padx=20, pady=20, bg="#333333")
        self.stats_frame.pack(pady=10, fill='x', padx=20)

        self.population_stats_button = ttk.Button(self.stats_frame, text="Статистика по населению", command=self.show_population_stats_window)
        self.population_stats_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.cars_stats_button = ttk.Button(self.stats_frame, text="Статистика по автомобилям", command=self.show_cars_stats)
        self.cars_stats_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.search_person_button = ttk.Button(self.stats_frame, text="Поиск жителя", command=self.search_person)
        self.search_person_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    def create_add_window(self, title, fields, save_callback):
        add_window = tk.Toplevel(self.root)
        add_window.title(title)

        # Применяем стиль
        add_window.configure(bg="#333333")
        
        entries = {}
        for i, (label, input_type) in enumerate(fields):
            tk.Label(add_window, text=label, font=("Arial", 12), fg="white", bg="#333333").grid(row=i, column=0, sticky="w", padx=10, pady=10)
            if input_type == 'entry':
                entry = tk.Entry(add_window, font=("Arial", 12), bg="#555555", fg="white", insertbackground="white")
                entry.grid(row=i, column=1, padx=10, pady=10)
                entries[label] = entry
            elif input_type == 'combobox':
                combobox = ttk.Combobox(add_window, values=predefined_districts, font=("Arial", 12), state="readonly")
                combobox.set(predefined_districts[0])  # Значение по умолчанию
                combobox.grid(row=i, column=1, padx=10, pady=10)

                # Выделяем поле "Район" другим цветом
                if label == "Район:":
                    combobox.config(style="highlighted.TCombobox")  # Применение выделенного стиля для поля "Район"
                else:
                    combobox.config(style="TCombobox")  # Применение стандартного стиля для остальных combobox
                    
                entries[label] = combobox

        def save():
            input_data = {label: entries[label].get() for label, _ in fields}

            # Проверка на заполненность всех полей
            if not are_fields_filled(input_data):
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
                return

            save_callback(input_data)
            add_window.destroy()

        tk.Button(add_window, text="Добавить", font=("Arial", 12), bg="#4CAF50", fg="white", command=save).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def add_person(self):
        fields = [
            ("Фамилия:", 'entry'),
            ("Имя:", 'entry'),
            ("Отчество:", 'entry'),
            ("Возраст:", 'entry'),
            ("Район:", 'combobox')
        ]

        def save_person(input_data):
            surname = input_data['Фамилия:']
            name = input_data['Имя:']
            patronymic = input_data['Отчество:']
            age = input_data['Возраст:']
            district = input_data['Район:']

            if district == "":  # Проверка на пустой район
                messagebox.showerror("Ошибка", "Выберите район для жителя.")
                return

            if not is_valid_age(age):
                messagebox.showerror("Ошибка", "Введите корректный возраст.")
                return

            try:
                self.population_data = add_person(self.population_data, surname, name, patronymic, age, district)
                save_data('population.json', self.population_data)
                messagebox.showinfo("Успех", "Житель добавлен успешно!")
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

        self.create_add_window("Добавить жителя", fields, save_person)

    def add_car(self):
        fields = [
            ("Марка:", 'entry'),
            ("Модель:", 'entry'),
            ("Год выпуска:", 'entry'),
            ("Номер:", 'entry'),
            ("Район:", 'combobox')
        ]

        def save_car(input_data):
            make = input_data['Марка:']
            model = input_data['Модель:']
            year = input_data['Год выпуска:']
            number = input_data['Номер:']
            district = input_data['Район:']

            if district == "":  # Проверка на пустой район
                messagebox.showerror("Ошибка", "Выберите район для автомобиля.")
                return

            if not is_valid_year(year):
                messagebox.showerror("Ошибка", "Введите корректный год выпуска.")
                return

            self.cars_data = add_car(self.cars_data, make, model, year, number, district)
            save_data('cars.json', self.cars_data)
            messagebox.showinfo("Успех", "Автомобиль добавлен успешно!")

        self.create_add_window("Добавить автомобиль", fields, save_car)

    def show_population_stats_window(self):
        # Окно статистики по населению
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Статистика по населению")

        # Применяем стиль фона
        stats_window.configure(bg="#333333")

        district_population = {district: {'count': 0, 'total_age': 0} for district in predefined_districts}
        total_population = 0
        for person in self.population_data:
            district_population[person['district']]['count'] += 1
            district_population[person['district']]['total_age'] += person['age']
            total_population += 1

        for district, data in district_population.items():
            if data['count'] > 0:
                avg_age = data['total_age'] / data['count']
                tk.Label(stats_window, text=f"{district}: {data['count']} человек, средний возраст: {avg_age:.2f} лет", font=("Arial", 12), fg="white", bg="#333333").pack()

        tk.Label(stats_window, text=f"Общее количество жителей: {total_population}", font=("Arial", 12, "bold"), fg="white", bg="#333333").pack()

    def show_cars_stats(self):
        # Окно статистики по автомобилям
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Статистика по автомобилям")

        # Применяем стиль фона
        stats_window.configure(bg="#333333")

        district_car_count = {district: 0 for district in predefined_districts}
        total_cars = 0
        for car in self.cars_data:
            district_car_count[car['district']] += 1
            total_cars += 1

        for district, count in district_car_count.items():
            if count > 0:
                tk.Label(stats_window, text=f"{district}: {count} автомобилей", font=("Arial", 12), fg="white", bg="#333333").pack()

        tk.Label(stats_window, text=f"Общее количество автомобилей: {total_cars}", font=("Arial", 12, "bold"), fg="white", bg="#333333").pack()

    def search_person(self):
        # Окно для поиска жителя
        search_window = tk.Toplevel(self.root)
        search_window.title("Поиск жителя")

        # Применяем стиль фона
        search_window.configure(bg="#333333")

        tk.Label(search_window, text="Фамилия:", font=("Arial", 12), fg="white", bg="#333333").grid(row=0, column=0, padx=10, pady=10)
        surname_entry = tk.Entry(search_window, font=("Arial", 12), bg="#555555", fg="white", insertbackground="white")
        surname_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(search_window, text="Имя:", font=("Arial", 12), fg="white", bg="#333333").grid(row=1, column=0, padx=10, pady=10)
        name_entry = tk.Entry(search_window, font=("Arial", 12), bg="#555555", fg="white", insertbackground="white")
        name_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(search_window, text="Отчество:", font=("Arial", 12), fg="white", bg="#333333").grid(row=2, column=0, padx=10, pady=10)
        patronymic_entry = tk.Entry(search_window, font=("Arial", 12), bg="#555555", fg="white", insertbackground="white")
        patronymic_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(search_window, text="Возраст:", font=("Arial", 12), fg="white", bg="#333333").grid(row=3, column=0, padx=10, pady=10)
        age_entry = tk.Entry(search_window, font=("Arial", 12), bg="#555555", fg="white", insertbackground="white")
        age_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(search_window, text="Район:", font=("Arial", 12), fg="white", bg="#333333").grid(row=4, column=0, padx=10, pady=10)
        district_combobox = ttk.Combobox(search_window, values=predefined_districts, font=("Arial", 12), state="readonly")
        district_combobox.grid(row=4, column=1, padx=10, pady=10)

        def search():
            surname = surname_entry.get()
            name = name_entry.get()
            patronymic = patronymic_entry.get()
            age = age_entry.get()
            district = district_combobox.get()

            result = []

            # Поиск по базе данных
            for person in self.population_data:
                if \
                        (not surname or surname.lower() in person['surname'].lower()) and \
                        (not name or name.lower() in person['name'].lower()) and \
                        (not patronymic or patronymic.lower() in person['patronymic'].lower()) and \
                        (not age or age == str(person['age'])) and \
                        (not district or district == person['district']):
                    result.append(person)

            # Показать результаты поиска
            if result:
                result_window = tk.Toplevel(search_window)
                result_window.title("Результаты поиска")

                for person in result:
                    result_label = tk.Label(result_window, text=f"{person['surname']} {person['name']} {person['patronymic']} - {person['age']} лет, район: {person['district']}",
                                            font=("Arial", 12), fg="black")
                    result_label.pack(pady=5)

                    # Кнопки редактирования и удаления
                    edit_button = ttk.Button(result_window, text="Редактировать", command=lambda p=person: self.edit_person(p))
                    edit_button.pack(pady=5)
                    delete_button = ttk.Button(result_window, text="Удалить", command=lambda p=person: self.delete_person(p, result_window))
                    delete_button.pack(pady=5)

            else:
                messagebox.showinfo("Результаты поиска", "Ничего не найдено.")

        search_button = ttk.Button(search_window, text="Найти", command=search)
        search_button.grid(row=5, column=0, columnspan=2, pady=20)

    def edit_person(self, person):
        # Окно редактирования данных жителя
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактирование данных")

        # Применяем стиль фона
        edit_window.configure(bg="#333333")
        
        # Поля ввода
        entries = {}
        for i, (label, value) in enumerate(person.items()):
            if label != 'surname' and label != 'name' and label != 'patronymic':
                tk.Label(edit_window, text=f"{label}:", font=("Arial", 12), fg="white", bg="#333333").grid(row=i, column=0, sticky="w", padx=10, pady=10)
                entry = tk.Entry(edit_window, font=("Arial", 12), bg="#555555", fg="white", insertbackground="white")
                entry.insert(0, value)
                entry.grid(row=i, column=1, padx=10, pady=10)
                entries[label] = entry

        def save_edited_person():
            edited_person = {key: int(entries[key].get()) if key == 'age' else entries[key].get() for key in entries}
            
            # Обновить данные
            index = self.population_data.index(person)
            self.population_data[index] = edited_person
            save_data('population.json', self.population_data)

            edit_window.destroy()

        tk.Button(edit_window, text="Сохранить", font=("Arial", 12), bg="#4CAF50", fg="white", command=save_edited_person).grid(row=len(person), column=0, columnspan=2, pady=10)

    def delete_person(self, person, result_window):
        # Удаление жителя
        if messagebox.askyesno("Удалить", "Вы уверены, что хотите удалить этого жителя?"):
            self.population_data.remove(person)
            save_data('population.json', self.population_data)
            messagebox.showinfo("Успех", "Житель удален.")
            result_window.destroy()

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = CityDatabaseApp(root)
    root.mainloop()
