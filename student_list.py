import json

class Student:
    def __init__(self, id, name, age):
        self.id = id 
        self.name = name
        self.age = age

class StudentManager:
    def load_from_file(self, path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            with open(path, "w") as f:
                json.dump([], f)
            return []

    def save_to_file(self, path, data): 
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def add_student(self, path, student):
        data = self.load_from_file(path)
        data.append({
            "id": student.id,
            "name": student.name,
            "age": student.age
        })
        self.save_to_file(path, data)

    def show_students(self, path):
        return self.load_from_file(path)

def menu():
    print("\nМеню:")
    print("1: показать всех студентов")
    print("2: добавить студента")
    print("3: сохранить в файл")
    print("0: выход")
    choice = input("Выберите действие: ")
    return choice

def main():
    path = "students.json"
    manager = StudentManager()
    
    while True:
        choice = menu()
        if choice == "1":
            students = manager.show_students(path)
            if not students:
                print("Список студентов пуст")
            else:
                for item in students:
                    print(f"ID: {item['id']}, Имя: {item['name']}, Возраст: {item['age']}")
        
        elif choice == "2":
            try:
                id = int(input("Введите ID студента: "))
                name = input("Введите имя студента: ")
                age = int(input("Введите возраст студента: "))
                student = Student(id, name, age)
                manager.add_student(path, student)
                print("Студент добавлен")
            except ValueError:
                print("Ошибка! ID и возраст должны быть числами.")

        elif choice == "3":
            students = manager.show_students(path)
            manager.save_to_file(path, students)
            print("Сохранено")

        elif choice == "0":
            students = manager.show_students(path)
            manager.save_to_file(path, students)
            print("Выход из программы")
            break
        else:
            print("Неверный выбор, Попробуйте снова")

    main()