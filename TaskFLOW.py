from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout,QVBoxLayout, QListWidget, QTextEdit,QLineEdit, QPushButton, QLabel,QComboBox, QMessageBox
from PyQt5.QtCore import Qt
import json

# ---------- Создание файла ----------
# tasks = [
#     {
#         "title": "Сделать домашку",
#         "done": False
#     }
# ]
#
# with open('tasks.json', 'w', encoding='utf-8') as file:
#     json.dump(tasks, file, ensure_ascii=False, indent=4)

app = QApplication([])
window = QWidget()
window.resize(1000, 700)
window.setWindowTitle('TaskFlow')
list_tasks = QListWidget()
task_text = QTextEdit()
task_input = QLineEdit()
task_input.setPlaceholderText('Введите задачу...')
search_input = QLineEdit()
search_input.setPlaceholderText('Поиск задачи...')
filter_box = QComboBox()
filter_box.addItems([
    'Все',
    'Выполненные',
    'Невыполненные'
])

info_label = QLabel('Количество задач: 0')

add_button = QPushButton('Добавить')
delete_button = QPushButton('Удалить')
edit_button = QPushButton('Редактировать')
done_button = QPushButton('Выполнено')

# ---------- Layout ----------
main_layout = QHBoxLayout()

left_layout = QVBoxLayout()
right_layout = QVBoxLayout()

buttons_layout = QHBoxLayout()

buttons_layout.addWidget(add_button)
buttons_layout.addWidget(delete_button)
buttons_layout.addWidget(edit_button)
buttons_layout.addWidget(done_button)

left_layout.addWidget(search_input)
left_layout.addWidget(filter_box)
left_layout.addWidget(list_tasks)
left_layout.addWidget(info_label)

right_layout.addWidget(task_input)
right_layout.addWidget(task_text)
right_layout.addLayout(buttons_layout)

main_layout.addLayout(left_layout, 3)
main_layout.addLayout(right_layout, 7)

window.setLayout(main_layout)

window.setStyleSheet("""
    background-color: black;
    color: white;
    font-size: 18px;
    font-family: Verdana;
""")


def load_tasks():
    try:
        with open('tasks.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except:
        return []


def save_tasks(tasks):
    with open('tasks.json', 'w', encoding='utf-8') as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)


def update_tasks():
    list_tasks.clear()

    tasks = load_tasks()

    search_text = search_input.text().lower()
    current_filter = filter_box.currentText()

    count = 0

    for task in tasks:

        title = task['title']
        done = task['done']

        if search_text not in title.lower():
            continue

        if current_filter == 'Выполненные' and not done:
            continue

        if current_filter == 'Невыполненные' and done:
            continue

        status = '✔' if done else '✘'

        list_tasks.addItem(f'{title} | {status}')

        count += 1

    info_label.setText(f'Количество задач: {count}')


def add_task():
    title = task_input.text()

    if title == '':
        QMessageBox.warning(
            window,
            'Ошибка',
            'Введите задачу'
        )
        return

    tasks = load_tasks()

    tasks.append({
        'title': title,
        'done': False
    })

    save_tasks(tasks)

    task_input.clear()

    update_tasks()


def delete_task():
    current = list_tasks.currentRow()
    if current == -1:
        return
    tasks = filtered_tasks()
    selected_task = tasks[current]
    all_tasks = load_tasks()
    all_tasks.remove(selected_task)
    save_tasks(all_tasks)
    update_tasks()
    task_text.clear()


def edit_task():
    current = list_tasks.currentRow()
    if current == -1:
        return
    tasks = filtered_tasks()
    selected_task = tasks[current]
    all_tasks = load_tasks()
    new_text = task_text.toPlainText()
    selected_task['title'] = new_text
    save_tasks(all_tasks)
    update_tasks()


def done_task():
    current = list_tasks.currentRow()

    if current == -1:
        return

    tasks = filtered_tasks()
    selected_task = tasks[current]

    all_tasks = load_tasks()

    for task in all_tasks:
        if task['title'] == selected_task['title']:
            task['done'] = not task['done']
            break

    save_tasks(all_tasks)

    update_tasks()


def show_task():
    current = list_tasks.currentRow()
    if current == -1:
        return
    tasks = filtered_tasks()
    selected_task = tasks[current]
    task_text.setText(selected_task['title'])

def filtered_tasks():
    tasks = load_tasks()
    search_text = search_input.text().lower()
    current_filter = filter_box.currentText()
    result = []
    for task in tasks:
        title = task['title']
        done = task['done']
        if search_text not in title.lower():
            continue
        if current_filter == 'Выполненные' and not done:
            continue
        if current_filter == 'Невыполненные' and done:
            continue
        result.append(task)
    return result

add_button.clicked.connect(add_task)
delete_button.clicked.connect(delete_task)
edit_button.clicked.connect(edit_task)
done_button.clicked.connect(done_task)

list_tasks.itemClicked.connect(show_task)

search_input.textChanged.connect(update_tasks)
filter_box.currentTextChanged.connect(update_tasks)

update_tasks()

window.show()
app.exec()