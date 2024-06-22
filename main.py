import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import random

# Создание глобального объекта плеера
player = QMediaPlayer()
player.setMedia(QMediaContent(QUrl.fromLocalFile("fon.mp3")))  # Загрузка файла
music_playing = False  # Состояние воспроизведения музыки

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        player.mediaStatusChanged.connect(self.loop_music)  # Подключение сигнала к слоту
    def initUI(self):
        self.setWindowTitle("Аннаграмы")
        self.showFullScreen()  # Открытие окна в полноэкранном режиме

        self.label = QLabel(self)
        self.pixmap = QPixmap('qt/path.jpg')
        self.label.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)

        # добавление заголовка игры
        self.title = QLabel("Анаграммы", self)
        title_width = 350
        title_height = 80
        title_x = (self.width() - title_width) // 2
        title_y = (self.height() - title_height) // 2 - 200  # Положение над кнопками
        self.title.setGeometry(title_x, title_y, title_width, title_height)
        self.title.setStyleSheet("font: 75 37pt \"Studio Var\";\n"
                                 "color: rgb(85, 0, 127);")
        self.title.setAlignment(Qt.AlignCenter)  # Выравнивание текста по центру
        self.title.show()

        # Добавление кнопки начала игры
        self.beginning = QPushButton('Играть', self)
        button_width = 300
        button_height = 75
        button_x = (self.width() - button_width) // 2
        button_y = (self.height() - button_height) // 2 - 85  # Положение над кнопкой "Руководство игры"
        self.beginning.setGeometry(button_x, button_y, button_width, button_height)
        self.beginning.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                            font: 75 14pt "MS Shell Dlg 2";
                                            background-color: rgb(255, 0, 0);}
                                            QPushButton:hover {background-color: rgb(200, 0, 0);} """)
        self.beginning.clicked.connect(self.Open_Level_Window)  # Подключение кнопки к функции Open_Level_Window
        self.beginning.show()

        # Добавление кнопки начала игры
        self.guide = QPushButton('Руководство игры', self)
        button_y = (self.height() - button_height) // 2  # Положение между кнопками "Играть" и "Выход"
        self.guide.setGeometry(button_x, button_y, button_width, button_height)
        self.guide.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                         font: 75 14pt \"MS Shell Dlg 2\";
                                         background-color: rgb(255, 153, 10);}
                                         QPushButton:hover {background-color: rgb(163, 109, 0);} """)
        self.guide.clicked.connect(self.Open_Rules_Window)
        self.guide.show()

        # Добавление кнопки завершения игры
        self.end = QPushButton('Выход', self)
        button_y = (self.height() - button_height) // 2 + 85  # Положение под кнопкой "Руководство игры"
        self.end.setGeometry(button_x, button_y, button_width, button_height)
        self.end.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                        font: 75 14pt \"MS Shell Dlg 2\";
                                        background-color: rgb(170, 170, 255);}
                                         QPushButton:hover {background-color: rgb(125, 125, 188);} """)
        self.end.clicked.connect(QCoreApplication.instance().quit)
        self.end.show()

        # Добавление кнопки музыки
        self.music_button = QPushButton('🔉' if music_playing else '🔇', self)
        button_size = 90
        button_x = 20  # Отступ от левого края
        button_y = self.height() - button_size - 20  # Отступ от нижнего края
        self.music_button.setGeometry(button_x, button_y, button_size, button_size)
        self.music_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                             font: 75 14pt \"MS Shell Dlg 2\";
                                             background-color: rgb(255, 255, 255);}""")  # Белый цвет
        self.music_button.clicked.connect(self.toggle_music)
        self.music_button.show()
    def loop_music(self, status):
        if status == QMediaPlayer.EndOfMedia:
            player.play()
    def toggle_music(self):
        global music_playing
        if music_playing:
            player.pause()  # Пауза, если музыка играет
            self.music_button.setText('🔇')  # Обновление иконки кнопки
        else:
            player.play()  # Воспроизведение, если музыка на паузе
            self.music_button.setText('🔉')  # Обновление иконки кнопки
        music_playing = not music_playing  # Обновление состояния воспроизведения музыки

    def Open_Rules_Window(self):
        self.rules_window = Rules_Window()
        self.setCentralWidget(self.rules_window)
    def Open_Level_Window(self):
        self.level_window = LevelWindow()
        self.setCentralWidget(self.level_window)

class Rules_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.showFullScreen()  # Открытие окна в полноэкранном режиме
        self.label = QLabel(self)
        self.pixmap = QPixmap('qt/path.jpg')
        self.label.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)

        # Размеры и положение текстового поля
        text_field_width = 740
        text_field_height = 500
        text_field_x = (self.width() - text_field_width) // 2
        text_field_y = (self.height() - text_field_height) // 2

        self.label = QLabel(""" 
             Как играть в "Анаграммы"?
        В "Анаграммах" ваша задача - расставить перемешанные буквы в
        правильном порядке и составить из них слово. На старте игры
        вам предоставляется набор букв, которые, хоть и образуют
        определенное слово, но расставлены в случайном порядке.
        Ваша цель - переставить их местами так, чтобы получить
        правильное слово.

             Что вам нужно знать:
        Игра разбита на три уровня сложности, от самых простых
        к самым сложным словам. С каждым уровнем слова становятся
        все интереснее и вызывающе, предоставляя вам новые вызовы.
        Чтобы выиграть, просто переставьте буквы в правильном
        порядке и угадайте слово.
        Удачи!""", self)
        self.label.setGeometry(text_field_x, text_field_y, text_field_width, text_field_height)
        self.label.setStyleSheet("font: 75 17pt \"Studio Var\";\n"
                                 "color: rgb(85, 0, 127);")
        self.label.show()

        # Создаем кнопку для возврата к основному окну
        self.close_the_rules = QPushButton('<', self)
        self.close_the_rules.setStyleSheet("""QPushButton {
             color: rgb(255, 255, 255);
             font: 14pt \"MS Shell Dlg 2\";
             background-color: rgb(170, 170, 255);
         }
         QPushButton:hover {
             background-color: rgb(125, 125, 188);
         }""")
        # Устанавливаем абсолютные координаты для кнопки
        self.close_the_rules.setGeometry(20, self.height() - 110, 90, 90)
        self.close_the_rules.show()
        self.close_the_rules.clicked.connect(self.return_main)  # Подключение кнопки к функции return_main

    def return_main(self):
        self.main_window = MainWindow()
        self.setCentralWidget(self.main_window)

class LevelWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.showFullScreen()  # Открытие окна в полноэкранном режиме
        self.label = QLabel(self)
        self.pixmap = QPixmap('qt/path.jpg')
        self.label.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)

        # Размеры и положение надписи
        label_width = 400
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = (self.height() - label_height) // 2 - 150  # Положение над кнопками

        self.label = QLabel("Выбор сложности", self)
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        self.label.setStyleSheet("font: 75 24pt \"Studio Var\";\n"
                                      "color: rgb(85, 0, 127);")
        self.label.show()

        button_width = 170
        button_height = 170
        button_spacing = 50  # Расстояние между кнопками

        # Расчет координат для центрирования кнопок
        start_x = (self.width() - 3 * button_width - 2 * button_spacing) // 2
        start_y = (self.height() - button_height) // 2

        self.button_first = QPushButton("Новичок", self)
        self.button_first.clicked.connect(self.level_one)
        self.button_first.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                                       font: 14pt \"MS Shell Dlg 2\";
                                                                       background-color: rgb(235, 146, 147);}
                                                                      QPushButton:hover {background-color: rgb(129, 80, 81);} """)
        self.button_first.setGeometry(start_x, start_y, button_width, button_height)
        self.button_first.show()

        self.second_button = QPushButton("Продвинутый", self)
        self.second_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                                font: 14pt \"MS Shell Dlg 2\";
                                                                background-color: rgb(203, 60, 148);}
                                                               QPushButton:hover {background-color: rgb(129, 38, 83);} """)
        self.second_button.clicked.connect(self.level_two)
        self.second_button.setGeometry(start_x + button_width + button_spacing, start_y, button_width, button_height)
        self.second_button.show()

        self.third_button = QPushButton("Эксперт", self)
        self.third_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                                font: 14pt \"MS Shell Dlg 2\";
                                                                background-color: rgb(127, 21, 102);}
                                                               QPushButton:hover {background-color: rgb(48, 7, 38);} """)
        self.third_button.setGeometry(start_x + 2 * button_width + 2 * button_spacing, start_y, button_width,
                                      button_height)
        self.third_button.show()
        self.third_button.clicked.connect(self.level_three)

        # Создаем кнопку для возврата к основному окну
        self.close_the_levels = QPushButton('<', self)
        self.close_the_levels.setStyleSheet("""QPushButton {
            color: rgb(255, 255, 255);
            font: 14pt \"MS Shell Dlg 2\";
            background-color: rgb(170, 170, 255);
        }
        QPushButton:hover {
            background-color: rgb(125, 125, 188);
        }""")
        # Устанавливаем абсолютные координаты для кнопки
        self.close_the_levels.setGeometry(20, self.height() - 110, 90, 90)
        self.close_the_levels.show()
        self.close_the_levels.clicked.connect(self.close)  # Подключение кнопки к функции return_main
    def level_one(self):
        self.level_one_window = Level_One()
        self.setCentralWidget(self.level_one_window)
    def level_two(self):
        self.level_two_window = Level_Two()
        self.setCentralWidget(self.level_two_window)
    def level_three(self):
            self.level_three_window = Level_Three()
            self.setCentralWidget(self.level_three_window)
    def close(self):
        self.main_window = MainWindow()
        self.setCentralWidget(self.main_window)

class Level_One(QMainWindow):
    def __init__(self):
        super().__init__()
        self.correct_word = ''
        self.initUI()
    def initUI(self):
        self.showFullScreen()  # Открываем окно в полноэкранном режиме

        # Устанавливаем изображение фона
        self.label = QLabel(self)
        self.pixmap = QPixmap('qt/morning.jpg')
        self.label.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)

        # Добавляем текстовое поле для отображения введенных букв
        self.text_field = QLineEdit(self)
        text_field_width = 600
        text_field_height = 100
        self.text_field.setGeometry((self.width() - text_field_width) // 2,
                                    (self.height() - text_field_height) // 2 - 200,
                                    text_field_width, text_field_height)
        self.text_field.setReadOnly(True)  # Отключаем ввод с клавиатуры
        self.text_field.setAlignment(Qt.AlignCenter)  # Центрируем текст
        self.text_field.setStyleSheet("""font: 55pt "MS Shell Dlg 2"; color: purple;""")  # Стилизация текстового поля
        self.text_field.show()

        # Создаем три кнопки и генерируем буквы
        self.first_button = QPushButton(self)
        self.first_button.clicked.connect(lambda: self.add_letter(self.first_button.text()))
        self.second_button = QPushButton(self)
        self.second_button.clicked.connect(lambda: self.add_letter(self.second_button.text()))
        self.third_button = QPushButton(self)
        self.third_button.clicked.connect(lambda: self.add_letter(self.third_button.text()))

        # Стилизация кнопок
        button_size = 150
        button_spacing = 50  # Расстояние между кнопками
        start_x = (self.width() - 3 * button_size - 2 * button_spacing) // 2
        start_y = (self.height() + text_field_height) // 2  # Позиция под текстовым полем

        buttons = [self.first_button, self.second_button, self.third_button]
        for i, button in enumerate(buttons):
            button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                 font: 40pt "MS Shell Dlg 2";
                                                 background-color: rgba(85, 0, 127, 128);}  /* 50% прозрачность */
                                                QPushButton:hover {background-color: rgba(33, 0, 50, 128);} """)
            button.setGeometry(start_x + i * (button_size + button_spacing), start_y, button_size, button_size)
            button.show()

        self.generate_letters()

        # Кнопка для закрытия уровня и возврата к выбору уровней
        self.close_level_one_button = QPushButton('<', self)
        self.close_level_one_button.clicked.connect(self.return_to_level_window)
        self.close_level_one_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                               font: 14pt \"MS Shell Dlg 2\";
                                                               background-color: rgb(170, 170, 255);}
                                                          QPushButton:hover {background-color: rgb(125, 125, 188);} """)
        button_size = 90
        self.close_level_one_button.setGeometry(20, self.height() - button_size - 20, button_size, button_size)
        self.close_level_one_button.show()

        # Добавляем кнопку для удаления последней введенной буквы
        self.delete_letter_button = QPushButton('Отменить', self)
        self.delete_letter_button.clicked.connect(self.delete_letter)
        self.delete_letter_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                                font: 14pt \"MS Shell Dlg 2\";
                                                                background-color: rgb(255, 85, 85);}
                                                           QPushButton:hover {background-color: rgb(188, 0, 0);} """)
        button_size = 100
        self.delete_letter_button.setGeometry(self.width() - button_size - 20, self.height() - button_size - 20, button_size, button_size)
        self.delete_letter_button.show()

    def generate_letters(self):
        words = ['дом', 'сад', 'мир', 'мак', 'сок', 'лук', 'нос', 'лес', 'год', 'бой', \
                 'рот', 'кед', 'зов', 'зуб', 'чай', 'лев', 'мед', 'газ', 'люк', 'топ', \
                 'сыр', 'жук', 'лук', 'йод', 'рис', 'жар', 'кот', 'пес', 'вес', 'час', \
                 'бор', 'лом', 'мяч', 'дуб', 'сон', 'лук', 'чиж', 'бег', 'яма', 'вор' \
                 'дым', 'акт', 'мех', 'рог', 'ток', 'зло', 'миг', 'век', 'ёрш', 'ель']
        self.correct_word = random.choice(words)
        letters = list(self.correct_word)
        random.shuffle(letters)

        self.first_button.setText(letters[0])
        self.second_button.setText(letters[1])
        self.third_button.setText(letters[2])

    def add_letter(self, letter):
        current_text = self.text_field.text()
        if letter not in current_text:  # Проверяем, что буква еще не была введена
            new_text = current_text + letter
            self.text_field.setText(new_text)

            if len(new_text) == len(self.correct_word):
                if new_text == self.correct_word:
                    self.open_victory_window()
    def open_victory_window(self):
        self.victory_window = Victory_Window()
        self.setCentralWidget(self.victory_window)

    def return_to_level_window(self):
        self.level_window = LevelWindow()
        self.setCentralWidget(self.level_window)

    def delete_letter(self):
        # Удаляем последнюю введенную букву из текстового поля
        self.text_field.setText(self.text_field.text()[:-1])
class Level_Two(QMainWindow):
    def __init__(self):
        super().__init__()
        self.correct_word = ''
        self.initUI()

    def initUI(self):
        self.showFullScreen()  # Открываем окно в полноэкранном режиме

        # Устанавливаем изображение фона
        self.label = QLabel(self)
        self.pixmap = QPixmap('qt/day.jpg')
        self.label.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)

        # Добавляем текстовое поле для отображения введенных букв
        self.text_field = QLineEdit(self)
        text_field_width = 600
        text_field_height = 100
        self.text_field.setGeometry((self.width() - text_field_width) // 2,
                                    (self.height() - text_field_height) // 2 - 200,
                                    text_field_width, text_field_height)
        self.text_field.setReadOnly(True)  # Отключаем ввод с клавиатуры
        self.text_field.setAlignment(Qt.AlignCenter)  # Центрируем текст
        self.text_field.setStyleSheet("""font: 55pt "MS Shell Dlg 2"; color: purple;""")  # Стилизация текстового поля
        self.text_field.show()

        # Создаем четыре кнопки и генерируем буквы
        self.first_button = QPushButton(self)
        self.first_button.clicked.connect(lambda: self.add_letter(self.first_button))
        self.second_button = QPushButton(self)
        self.second_button.clicked.connect(lambda: self.add_letter(self.second_button))
        self.third_button = QPushButton(self)
        self.third_button.clicked.connect(lambda: self.add_letter(self.third_button))
        self.fourth_button = QPushButton(self)
        self.fourth_button.clicked.connect(lambda: self.add_letter(self.fourth_button))

        # Стилизация кнопок
        button_size = 150
        button_spacing = 50  # Расстояние между кнопками
        total_width = 4 * button_size + 3 * button_spacing
        start_x = (self.width() - total_width) // 2
        start_y = (self.height() + text_field_height) // 2  # Позиция под текстовым полем

        self.buttons = [self.first_button, self.second_button, self.third_button, self.fourth_button]
        for i, button in enumerate(self.buttons):
            button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                           font: 40pt "MS Shell Dlg 2";
                                                           background-color: rgba(85, 0, 127, 128);}  /* 50% прозрачности */
                                                          QPushButton:hover {background-color: rgba(33, 0, 50, 128);} """)
            button.setGeometry(start_x + i * (button_size + button_spacing), start_y, button_size, button_size)
            button.show()

        self.generate_letters()

        # Кнопка для закрытия уровня и возврата к выбору уровней
        self.close_level_one_button = QPushButton('<', self)
        self.close_level_one_button.clicked.connect(self.return_to_level_window)
        self.close_level_one_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                               font: 14pt \"MS Shell Dlg 2\";
                                                               background-color: rgb(170, 170, 255);}
                                                          QPushButton:hover {background-color: rgb(125, 125, 188);} """)
        button_size = 90
        self.close_level_one_button.setGeometry(20, self.height() - button_size - 20, button_size, button_size)
        self.close_level_one_button.show()

        # Добавляем кнопку для удаления последней введенной буквы
        self.delete_letter_button = QPushButton('Отменить', self)
        self.delete_letter_button.clicked.connect(self.delete_letter)
        self.delete_letter_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                                font: 14pt \"MS Shell Dlg 2\";
                                                                background-color: rgb(255, 85, 85);}
                                                           QPushButton:hover {background-color: rgb(188, 0, 0);} """)
        button_size = 100
        self.delete_letter_button.setGeometry(self.width() - button_size - 20, self.height() - button_size - 20, button_size, button_size)
        self.delete_letter_button.show()

    def generate_letters(self):
        words = ['свет', 'снег', 'луна', 'река', 'море', 'гора', 'шлюз', 'день', 'ночь', 'путь', \
                 'фара', 'игра', 'смех', 'небо', 'вода', 'йога', 'мыло', 'лень', 'лапа', 'лото', \
                 'кофе', 'енот', 'жрец', 'изба', 'стол', 'рука', 'мост', 'лист', 'лето', 'зима', \
                 'пюре', 'филе', 'крюк', 'круг', 'духи', 'щука', 'дата', 'перо', 'село', 'мода']
        self.correct_word = random.choice(words)
        letters = list(self.correct_word)
        random.shuffle(letters)

        self.first_button.setText(letters[0])
        self.second_button.setText(letters[1])
        self.third_button.setText(letters[2])
        self.fourth_button.setText(letters[3])

    def add_letter(self, button):
        letter = button.text()
        current_text = self.text_field.text()
        new_text = current_text + letter
        self.text_field.setText(new_text)
        button.setEnabled(False)  # Отключаем кнопку после нажатия

        if len(new_text) == len(self.correct_word):
            if new_text == self.correct_word:
                self.open_victory_window()

    def open_victory_window(self):
        self.victory_window = Victory_Window()
        self.setCentralWidget(self.victory_window)

    def return_to_level_window(self):
        self.level_window = LevelWindow()
        self.setCentralWidget(self.level_window)

    def delete_letter(self):
        # Удаляем последнюю введенную букву из текстового поля
        current_text = self.text_field.text()
        if current_text:
            last_letter = current_text[-1]
            self.text_field.setText(current_text[:-1])
            # Активируем кнопку с удаленной буквой
            for button in self.buttons:
                if button.text() == last_letter:
                    button.setEnabled(True)
                    break
class Level_Three(QMainWindow):
    def __init__(self):
        super().__init__()
        self.correct_word = ''
        self.initUI()
        self.button_states = [False, False, False, False, False]  # Переменные состояния кнопок: False - кнопка свободна, True - кнопка уже нажата

    def initUI(self):
        self.showFullScreen()  # Открываем окно в полноэкранном режиме

        # Устанавливаем изображение фона
        self.label = QLabel(self)
        self.pixmap = QPixmap('qt/night.jpg')
        self.label.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)

        # Добавляем текстовое поле для отображения введенных букв
        self.text_field = QLineEdit(self)
        text_field_width = 600
        text_field_height = 100
        self.text_field.setGeometry((self.width() - text_field_width) // 2,
                                    (self.height() - text_field_height) // 2 - 200,
                                    text_field_width, text_field_height)
        self.text_field.setReadOnly(True)  # Отключаем ввод с клавиатуры
        self.text_field.setAlignment(Qt.AlignCenter)  # Центрируем текст
        self.text_field.setStyleSheet("""font: 55pt "MS Shell Dlg 2"; color: purple;""")  # Стилизация текстового поля
        self.text_field.show()

        # Создаем пять кнопок и генерируем буквы
        self.first_button = QPushButton(self)
        self.first_button.clicked.connect(lambda: self.add_letter(self.first_button.text(), 0))  # Передаем индекс кнопки
        self.second_button = QPushButton(self)
        self.second_button.clicked.connect(lambda: self.add_letter(self.second_button.text(), 1))
        self.third_button = QPushButton(self)
        self.third_button.clicked.connect(lambda: self.add_letter(self.third_button.text(), 2))
        self.fourth_button = QPushButton(self)
        self.fourth_button.clicked.connect(lambda: self.add_letter(self.fourth_button.text(), 3))
        self.fifth_button = QPushButton(self)
        self.fifth_button.clicked.connect(lambda: self.add_letter(self.fifth_button.text(), 4))

        # Стилизация кнопок
        button_size = 150
        button_spacing = 50  # Расстояние между кнопками
        start_x = (self.width() - 5 * button_size - 4 * button_spacing) // 2
        start_y = (self.height() + text_field_height) // 2  # Позиция под текстовым полем

        buttons = [self.first_button, self.second_button, self.third_button, self.fourth_button, self.fifth_button]
        self.buttons = buttons  # Сохраняем кнопки в атрибут класса
        for i, button in enumerate(buttons):
            button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                 font: 40pt "MS Shell Dlg 2";
                                                 background-color: rgba(85, 0, 127, 128);}  /* 50% прозрачность */
                                                QPushButton:hover {background-color: rgba(33, 0, 50, 128);} """)
            button.setGeometry(start_x + i * (button_size + button_spacing), start_y, button_size, button_size)
            button.show()

        self.generate_letters()

        # Кнопка для закрытия уровня и возврата к выбору уровней
        self.close_level_one_button = QPushButton('<', self)
        self.close_level_one_button.clicked.connect(self.return_to_level_window)
        self.close_level_one_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                               font: 14pt \"MS Shell Dlg 2\";
                                                               background-color: rgb(170, 170, 255);}
                                                          QPushButton:hover {background-color: rgb(125, 125, 188);} """)
        button_size = 90
        self.close_level_one_button.setGeometry(20, self.height() - button_size - 20, button_size, button_size)
        self.close_level_one_button.show()

        # Добавляем кнопку для удаления последней введенной буквы
        self.delete_letter_button = QPushButton('Отменить', self)
        self.delete_letter_button.clicked.connect(self.delete_letter)
        self.delete_letter_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                                font: 14pt \"MS Shell Dlg 2\";
                                                                background-color: rgb(255, 85, 85);}
                                                           QPushButton:hover {background-color: rgb(188, 0, 0);} """)
        button_size = 100
        self.delete_letter_button.setGeometry(self.width() - button_size - 20, self.height() - button_size - 20, button_size, button_size)
        self.delete_letter_button.show()

    def generate_letters(self):
        words = ['вагон', 'багет', 'дуэль', 'башня', 'забор', 'ёршик', 'изъян', 'осень', 'весна', 'ягода',\
                 'газон', 'леший', 'зебра', 'козёл', 'ладья', 'номер', 'обида', 'океан', 'кошка', 'слеза',\
                 'чутьё', 'район', 'семья', 'приём', 'улица', 'фобия', 'хомяк', 'месяц', 'цапля', 'шпион',\
                 'пчела', 'шляпа', 'сироп', 'карта', 'пламя', 'мафия', 'чехол', 'мираж', 'юрист', 'мусор']
        self.correct_word = random.choice(words)
        letters = list(self.correct_word)
        random.shuffle(letters)

        self.first_button.setText(letters[0])
        self.second_button.setText(letters[1])
        self.third_button.setText(letters[2])
        self.fourth_button.setText(letters[3])
        self.fifth_button.setText(letters[4])

    def add_letter(self, letter, index):
        if not self.button_states[index]:  # Проверяем, была ли уже нажата кнопка
            current_text = self.text_field.text()
            new_text = current_text + letter
            self.text_field.setText(new_text)

            if len(new_text) == len(self.correct_word):
                if new_text == self.correct_word:
                    self.open_victory_window()

            self.button_states[index] = True  # Устанавливаем состояние кнопки как нажатая

    def open_victory_window(self):
        self.victory_window = Victory_Window()
        self.setCentralWidget(self.victory_window)

    def return_to_level_window(self):
        self.level_window = LevelWindow()
        self.setCentralWidget(self.level_window)

    def delete_letter(self):
        # Удаляем последнюю введенную букву из текстового поля
        current_text = self.text_field.text()
        if current_text:
            last_letter = current_text[-1]
            self.text_field.setText(current_text[:-1])  # Удаляем последнюю букву

            # Определяем индекс кнопки, соответствующей последней удаленной букве
            for i, button in enumerate(self.buttons):
                if button.text() == last_letter and self.button_states[i]:
                    self.button_states[i] = False  # Сбрасываем состояние кнопки
                    break

class Victory_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.showFullScreen()  # Открываем окно в полноэкранном режиме
        self.label = QLabel(self)
        self.pixmap = QPixmap('qt/victory.png')
        self.label.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)

        # Добавляем надпись "Победа"
        self.victory_label = QLabel("Победа!", self)
        self.victory_label.setStyleSheet("font: 75 56pt \"Studio Var\";\n"
                                         "color: rgb(85, 0, 127);")
        self.victory_label.setAlignment(Qt.AlignCenter)  # Выравнивание текста по центру
        self.victory_label.setGeometry((self.width() - 270) // 2, (self.height() - 80) // 2 - 100, 300, 100)
        self.victory_label.show()

        # Создаем кнопку "На главное меню"
        self.forever = QPushButton('На главное меню', self)
        self.forever.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                        font: 14pt \"MS Shell Dlg 2\";
                                        background-color: rgba(235, 146, 147, 0.8);}
                                        QPushButton:hover {background-color: rgba(129, 80, 81, 0.8);} """)
        self.forever.resize(350, 50)
        self.forever.clicked.connect(self.level_selection_Window)

        # Устанавливаем позицию кнопки
        self.forever.move((self.width() - self.forever.width()) // 2, (self.height() - self.forever.height()) // 2 + 20)
        self.forever.show()
    def level_selection_Window(self):
        self.main_window = MainWindow()
        self.setCentralWidget(self.main_window)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())