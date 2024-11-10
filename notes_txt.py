#для начала скопируй сюда интерфейс "Умных заметок" и проверь его работу

#затем запрограммируй демо-версию функционала

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, 
        QLabel, 
        QWidget, 
        QTextEdit, 
        QLineEdit, 
        QListWidget, 
        QPushButton, 
        QVBoxLayout, 
        QHBoxLayout,
        QInputDialog
        )
        
import json




























app = QApplication([])
notes_win = QWidget()




"""Интерфейс приложения"""





# Создаём виджеты:
field_text = QTextEdit()
field_tag = QLineEdit()
list_notes = QListWidget()
list_tags = QListWidget()
button_note_create = QPushButton("Создать заметку")
button_note_delete = QPushButton("Удалить заметку")
button_note_save = QPushButton("Сохранить заметку")
button_tag_add = QPushButton("Добавить к заметке")
button_tag_delete = QPushButton("Открепить от заметки")
button_tag_search = QPushButton("Искать заметки по тегу")
list_tags_label = QLabel("Список тегов")
list_notes_label = QLabel("Список заметок")

#Создаём лэйауты:
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_delete)
row_2 = QHBoxLayout()
row_2.addWidget(button_tag_add)
row_2.addWidget(button_tag_delete)
col_1 = QVBoxLayout()
col_1.addWidget(field_text)
col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
col_2.addLayout(row_1)
col_2.addWidget(button_note_save)
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
col_2.addLayout(row_2)
col_2.addWidget(button_tag_search)

main_layout = QHBoxLayout()
main_layout.addLayout(col_1)
main_layout.addLayout(col_2)
notes_win.setLayout(main_layout)

notes = []

#функционал приложения
def show_note():
    #Получаем текст из заметки с выделенным названием и отображаем его в поле
    key = list_notes.selectedItems()[0].text()
    print(key)
    print(notes)
    for note in notes:
        if key == note[0]:
            field_text.setText(note[1])
            list_tags.clear()
            list_tags.addItems(note[2])


def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "добавить заметку", "Название заметки: ")
    if ok and note_name != "":
        note = [note_name, "", []]
        notes.append(note)
        list_notes.addItem(note_name)


        with open(str(len(notes) - 1) + ".txt", "w", encoding="utf-8") as file:
            file.write(note[0] + "\n")

    
def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        index = 0
        for note in notes:
            if note[0] == key:
                note[1] = field_text.toPlainText()
                with open(str(index) + ".txt", "w", encoding = "utf-8") as file:
                    file.write(note[0] + "\n")
                    file.write(note[1] + "\n")
                    for tag in note[2]:
                        file.write(tag + "\n")
            index += 1
        print(notes)
    else:
        print("Заметка для сохранения не выбрана.")

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        notes[key]["text"] = field_text.toPlainText()
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print("Заметка для удаления не выбрана.")

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if tag not in notes[key]["tags"] and tag != '':
            notes[key]["tags"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
            with open("notes_data.json", "w", encoding="utf-8") as file:
                json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print("Заметка для добавления тега не выбрана.")

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_notes.selectedItems()[0].text()
        notes[key]["tags"].remove(tag)
        list_tags.addItem(tag)
        list_tags.addItems(notes[key]["tags"])
    else:
        print("Tег для удаления не выбран.")

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == "Искать заметки по тегу" and tag is not None:
        notes_filtered = {} #тут будут заметки с выделенным тегом
        for note in notes:
            if tag in notes[note]["tags"]:
                notes_filtered[note] = notes[note]
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        button_tag_search.setText("Сбросить поиск")
    else:
        field_tag.clear()
        list_notes.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Искать заметки по тегу")

"""Запуск приложения"""
#Подключение обработки событий
list_notes.itemClicked.connect(show_note)
list_notes.itemClicked.connect(add_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_delete.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_delete.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

name = 0
note = []
while True:
    filename = str(name) + ".txt"
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line.replace("\n", '')
                note.append(line)
        tags = note[2].split(" ")
        note[2] = tags

        notes.append(note)
        note = []
        name += 1


    except IOError:
        break

for note in notes:
    list_notes.addItem(note[0])

#запуск приложения 
notes_win.show()
app.exec_()
