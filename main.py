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

class MainWindow(QMainWindow):  # Основное окно приложения
    def __init__(self):
        super().__init__()  # Вызов конструктора родительского класса
        self.initUI()  # Инициализация интерфейса
        player.mediaStatusChanged.connect(self.loop_music)  # Подключение сигнала изменения статуса медиа к методу loop_music

    def initUI(self):  # Метод для инициализации интерфейса
        self.setWindowTitle("Анаграммы")  # Установка заголовка окна
        self.showFullScreen()  # Открытие окна в полноэкранном режиме

        self.label = QLabel(self)  # Метка для отображения изображения
        self.pixmap = QPixmap('qt/path.jpg')  # Загрузка изображения
        self.label.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))  # Масштабирование изображения
        self.label.setScaledContents(True)  # Масштабирование содержимого метки
        self.setCentralWidget(self.label)  # Установка метки как центрального виджета

        # Заголовок игры
        self.title = QLabel("Анаграммы", self)  # Создание метки заголовка
        title_width = 350  # Ширина заголовка
        title_height = 80  # Высота заголовка
        title_x = (self.width() - title_width) // 2  # Координата X для центрирования заголовка
        title_y = (self.height() - title_height) // 2 - 200  # Координата Y для размещения заголовка
        self.title.setGeometry(title_x, title_y, title_width, title_height)  # Установка размеров и положения заголовка
        self.title.setStyleSheet("font: 75 37pt \"Studio Var\";\ncolor: rgb(85, 0, 127);")  # Стиль заголовка
        self.title.setAlignment(Qt.AlignCenter)  # Выравнивание текста по центру
        self.title.show()  # Отображение заголовка

        # Кнопка "Играть"
        self.beginning = QPushButton('Играть', self)  # Создание кнопки
        button_width = 350  # Ширина кнопки
        button_height = 95  # Высота кнопки
        button_x = (self.width() - button_width) // 2  # Координата X для центрирования кнопки
        button_y = (self.height() - button_height) // 2 - 105  # Координата Y для размещения кнопки
        self.beginning.setGeometry(button_x, button_y, button_width, button_height)  # Установка размеров и положения кнопки
        self.beginning.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                            font: 75 14pt "MS Shell Dlg 2";
                                            background-color: rgb(255, 0, 0);}
                                            QPushButton:hover {background-color: rgb(200, 0, 0);} """)  # Стиль кнопки
        self.beginning.clicked.connect(self.Open_Level_Window)  # Подключение кнопки к методу Open_Level_Window
        self.beginning.show()  # Отображение кнопки

        # Кнопка "Руководство игры"
        self.guide = QPushButton('Руководство игры', self)  # Создание кнопки
        button_y = (self.height() - button_height) // 2  # Координата Y для размещения кнопки
        self.guide.setGeometry(button_x, button_y, button_width, button_height)  # Установка размеров и положения кнопки
        self.guide.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                         font: 75 14pt "MS Shell Dlg 2";
                                         background-color: rgb(255, 153, 10);}
                                         QPushButton:hover {background-color: rgb(163, 109, 0);} """)  # Стиль кнопки
        self.guide.clicked.connect(self.Open_Rules_Window)  # Подключение кнопки к методу Open_Rules_Window
        self.guide.show()  # Отображение кнопки

        # Кнопка "Выход"
        self.end = QPushButton('Выход', self)  # Создание кнопки
        button_y = (self.height() - button_height) // 2 + 105  # Координата Y для размещения кнопки
        self.end.setGeometry(button_x, button_y, button_width, button_height)  # Установка размеров и положения кнопки
        self.end.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                        font: 75 14pt "MS Shell Dlg 2";
                                        background-color: rgb(170, 170, 255);}
                                         QPushButton:hover {background-color: rgb(125, 125, 188);} """)  # Стиль кнопки
        self.end.clicked.connect(QCoreApplication.instance().quit)  # Подключение кнопки к методу завершения приложения
        self.end.show()  # Отображение кнопки

        # Кнопка управления музыкой
        self.music_button = QPushButton('🔉' if music_playing else '🔇', self)  # Создание кнопки с иконкой в зависимости от состояния музыки
        button_size = 150  # Размер кнопки
        button_x = 20  # Отступ от левого края
        button_y = self.height() - button_size - 20  # Отступ от нижнего края
        self.music_button.setGeometry(button_x, button_y, button_size, button_size)  # Установка размеров и положения кнопки
        self.music_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                             font: 75 14pt "MS Shell Dlg 2";
                                             background-color: rgb(255, 255, 255);}""")  # Стиль кнопки
        self.music_button.clicked.connect(self.toggle_music)  # Подключение кнопки к методу toggle_music
        self.music_button.show()  # Отображение кнопки

    def loop_music(self, status):  # Метод для повторного воспроизведения музыки
        if status == QMediaPlayer.EndOfMedia:  # Если музыка дошла до конца
            player.play()  # Повторное воспроизведение

    def toggle_music(self):  # Метод для переключения воспроизведения музыки
        global music_playing  # Использование глобальной переменной для состояния музыки
        if music_playing:  # Если музыка играет
            player.pause()  # Пауза музыки
            self.music_button.setText('🔇')  # Обновление иконки на кнопке
        else:  # Если музыка на паузе
            player.play()  # Воспроизведение музыки
            self.music_button.setText('🔉')  # Обновление иконки на кнопке
        music_playing = not music_playing  # Переключение состояния музыки

    def Open_Rules_Window(self):  # Метод для открытия окна с правилами
        self.rules_window = Rules_Window()  # Создание окна с правилами
        self.setCentralWidget(self.rules_window)  # Установка окна с правилами как центрального виджета

    def Open_Level_Window(self):  # Метод для открытия окна с уровнями игры
        self.level_window = LevelWindow()  # Создание окна с уровнями
        self.setCentralWidget(self.level_window)  # Установка окна с уровнями как центрального виджета


class Rules_Window(QMainWindow):  # Класс окна правил
    def __init__(self):
        super().__init__()  # Вызов конструктора родительского класса
        self.initUI()  # Инициализация интерфейса

    def initUI(self):
        self.showFullScreen()  # Полноэкранный режим

        self.label = QLabel(self)  # Создание метки
        self.pixmap = QPixmap('qt/path.jpg')  # Загрузка изображения
        self.label.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))  # Масштабирование изображения
        self.label.setScaledContents(True)  # Масштабирование содержимого метки
        self.setCentralWidget(self.label)  # Установка метки как центрального виджета

        # Настройка текстового поля
        text_field_width = 800
        text_field_height = 700
        text_field_x = (self.width() - text_field_width) // 2
        text_field_y = (self.height() - text_field_height) // 3

        # Текст правил
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
        self.label.setGeometry(text_field_x, text_field_y, text_field_width, text_field_height)  # Установка положения и размера текстового поля
        self.label.setStyleSheet("font: 75 17pt \"Studio Var\";\n"  # Стиль текста
                                 "color: rgb(85, 0, 127);")
        self.label.show()  # Показать текстовое поле

        # Кнопка возврата
        self.close_the_rules = QPushButton('<', self)  # Создание кнопки
        self.close_the_rules.setStyleSheet("""QPushButton {
             color: rgb(255, 255, 255);
             font: 14pt \"MS Shell Dlg 2\";
             background-color: rgb(170, 170, 255);}
         QPushButton:hover {background-color: rgb(125, 125, 188);}""")
        self.close_the_rules.setGeometry(20, self.height() - 160, 150, 150)  # Положение и размер кнопки
        self.close_the_rules.show()  # Показать кнопку
        self.close_the_rules.clicked.connect(self.return_main)  # Подключение к методу возврата

    def return_main(self):  # Метод возврата в главное окно
        self.main_window = MainWindow()  # Создание главного окна
        self.setCentralWidget(self.main_window)  # Установка главного окна как центрального виджета

class LevelWindow(QMainWindow):  # Окно выбора уровня
    def __init__(self):
        super().__init__()
        self.initUI()  # Инициализация интерфейса

    def initUI(self):
        self.showFullScreen()  # Полноэкранный режим
        self.label = QLabel(self)
        self.pixmap = QPixmap('qt/path.jpg')  # Загрузка изображения
        self.label.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))  # Масштабирование изображения
        self.label.setScaledContents(True)  # Масштабирование содержимого
        self.setCentralWidget(self.label)  # Установка изображения как центрального виджета

        # Параметры метки "Выбор сложности"
        label_width = 400
        label_height = 100
        label_x = (self.width() - label_width) // 2  # Центрирование по X
        label_y = (self.height() - label_height) // 2 - 150  # Центрирование по Y

        self.label = QLabel("Выбор сложности", self)  # Создание метки
        self.label.setGeometry(label_x, label_y, label_width, label_height)  # Установка размера и положения
        self.label.setStyleSheet("font: 75 24pt \"Studio Var\";\ncolor: rgb(85, 0, 127);")  # Стиль метки
        self.label.setAlignment(Qt.AlignCenter)  # Выравнивание текста по центру
        self.label.show()  # Отображение метки

        # Параметры кнопок
        button_width = 190
        button_height = 190
        button_spacing = 50  # Расстояние между кнопками

        # Расчет координат для центрирования кнопок
        start_x = (self.width() - 3 * button_width - 2 * button_spacing) // 2
        start_y = (self.height() - button_height) // 2

        # Кнопка "Новичок"
        self.button_first = QPushButton("Новичок", self)
        self.button_first.clicked.connect(self.level_one)  # Подключение кнопки к методу level_one
        self.button_first.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                                       font: 14pt \"MS Shell Dlg 2\";
                                                                       background-color: rgb(235, 146, 147);}
                                                                      QPushButton:hover {background-color: rgb(129, 80, 81);} """)  # Стиль кнопки
        self.button_first.setGeometry(start_x, start_y, button_width, button_height)  # Установка размера и положения
        self.button_first.show()  # Отображение кнопки

        # Кнопка "Продвинутый"
        self.second_button = QPushButton("Продвинутый", self)
        self.second_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                                font: 14pt \"MS Shell Dlg 2\";
                                                                background-color: rgb(203, 60, 148);}
                                                               QPushButton:hover {background-color: rgb(129, 38, 83);} """)  # Стиль кнопки
        self.second_button.clicked.connect(self.level_two)  # Подключение кнопки к методу level_two
        self.second_button.setGeometry(start_x + button_width + button_spacing, start_y, button_width, button_height)  # Установка размера и положения
        self.second_button.show()  # Отображение кнопки

        # Кнопка "Эксперт"
        self.third_button = QPushButton("Эксперт", self)
        self.third_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                                font: 14pt \"MS Shell Dlg 2\";
                                                                background-color: rgb(127, 21, 102);}
                                                               QPushButton:hover {background-color: rgb(48, 7, 38);} """)  # Стиль кнопки
        self.third_button.setGeometry(start_x + 2 * button_width + 2 * button_spacing, start_y, button_width, button_height)  # Установка размера и положения
        self.third_button.clicked.connect(self.level_three)  # Подключение кнопки к методу level_three
        self.third_button.show()  # Отображение кнопки

        # Кнопка для возврата к основному окну
        self.close_the_levels = QPushButton('<', self)
        self.close_the_levels.setStyleSheet("""QPushButton {
            color: rgb(255, 255, 255);
            font: 14pt \"MS Shell Dlg 2\";
            background-color: rgb(170, 170, 255);
        }
        QPushButton:hover {
            background-color: rgb(125, 125, 188);
        }""")  # Стиль кнопки
        self.close_the_levels.setGeometry(20, self.height() - 160, 150, 150)  # Установка размера и положения
        self.close_the_levels.clicked.connect(self.close)  # Подключение кнопки к методу close
        self.close_the_levels.show()  # Отображение кнопки

    def level_one(self):  # Метод для открытия первого уровня
        self.level_one_window = Level_One()
        self.setCentralWidget(self.level_one_window)

    def level_two(self):  # Метод для открытия второго уровня
        self.level_two_window = Level_Two()
        self.setCentralWidget(self.level_two_window)

    def level_three(self):  # Метод для открытия третьего уровня
        self.level_three_window = Level_Three()
        self.setCentralWidget(self.level_three_window)

    def close(self):  # Метод для возврата к основному окну
        self.main_window = MainWindow()
        self.setCentralWidget(self.main_window)

class Level_One(QMainWindow):  # Окно первого уровня
    def __init__(self):
        super().__init__()
        self.correct_word = ''  # Слово, которое нужно угадать
        self.initUI()  # Настройка интерфейса

    def initUI(self):
        self.showFullScreen()  # Показываем окно на весь экран

        # Устанавливаем фон
        self.label = QLabel(self)
        self.pixmap = QPixmap('qt/morning.jpg')
        self.label.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)

        # Поле для введённых букв
        self.text_field = QLineEdit(self)
        text_field_width = 600
        text_field_height = 100
        self.text_field.setGeometry((self.width() - text_field_width) // 2,
                                    (self.height() - text_field_height) // 2 - 200,
                                    text_field_width, text_field_height)
        self.text_field.setReadOnly(True)  # Нельзя вводить текст с клавиатуры
        self.text_field.setAlignment(Qt.AlignCenter)  # Текст по центру
        self.text_field.setStyleSheet("""font: 55pt "MS Shell Dlg 2"; color: purple;""")  # Стилизация текстового поля
        self.text_field.show()  # Показываем текстовое поле

        # Создаём кнопки
        self.first_button = QPushButton(self)
        self.first_button.clicked.connect(lambda: self.add_letter(self.first_button.text()))
        self.second_button = QPushButton(self)
        self.second_button.clicked.connect(lambda: self.add_letter(self.second_button.text()))
        self.third_button = QPushButton(self)
        self.third_button.clicked.connect(lambda: self.add_letter(self.third_button.text()))

        # Стилизация кнопок
        button_size = 190  # Размер кнопок
        button_spacing = 50  # Расстояние между кнопками
        start_x = (self.width() - 3 * button_size - 2 * button_spacing) // 2  # Начальная позиция по x
        start_y = (self.height() + text_field_height) // 2  # Позиция под текстовым полем

        buttons = [self.first_button, self.second_button, self.third_button]
        for i, button in enumerate(buttons):
            button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                 font: 40pt "MS Shell Dlg 2";
                                                 background-color: rgba(85, 0, 127, 128);}  /* 50% прозрачность */
                                                QPushButton:hover {background-color: rgba(33, 0, 50, 128);} """)
            button.setGeometry(start_x + i * (button_size + button_spacing), start_y, button_size, button_size)
            button.show()  # Показываем кнопки

        self.generate_letters()  # Создаём буквы для кнопок

        # Кнопка для возврата к выбору уровней
        self.close_level_one_button = QPushButton('<', self)
        self.close_level_one_button.clicked.connect(self.return_to_level_window)
        self.close_level_one_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                               font: 14pt \"MS Shell Dlg 2\";
                                                               background-color: rgb(170, 170, 255);}
                                                          QPushButton:hover {background-color: rgb(125, 125, 188);} """)
        button_size = 150  # Размер кнопки
        self.close_level_one_button.setGeometry(20, self.height() - button_size - 10, button_size, button_size)
        self.close_level_one_button.show()  # Показываем кнопку

        # Кнопка для удаления последней введённой буквы
        self.delete_letter_button = QPushButton('Отменить', self)
        self.delete_letter_button.clicked.connect(self.delete_letter)
        self.delete_letter_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                                font: 14pt \"MS Shell Dlg 2\";
                                                                background-color: rgb(255, 85, 85);}
                                                           QPushButton:hover {background-color: rgb(188, 0, 0);} """)
        button_size = 150  # Размер кнопки
        self.delete_letter_button.setGeometry(self.width() - button_size - 20, self.height() - button_size - 20, button_size, button_size)
        self.delete_letter_button.show()  # Показываем кнопку

    def generate_letters(self):  # Создаём буквы для кнопок
        words = ['дом', 'сад', 'мир', 'мак', 'сок', 'лук', 'нос', 'лес', 'год', 'бой',
                 'рот', 'кед', 'зов', 'зуб', 'чай', 'лев', 'мед', 'газ', 'люк', 'топ',
                 'сыр', 'жук', 'лук', 'йод', 'рис', 'жар', 'кот', 'пес', 'вес', 'час',
                 'бор', 'лом', 'мяч', 'дуб', 'сон', 'лук', 'чиж', 'бег', 'яма', 'вор',
                 'дым', 'акт', 'мех', 'рог', 'ток', 'зло', 'миг', 'век', 'ёрш', 'ель']
        self.correct_word = random.choice(words)  # Выбираем случайное слово
        letters = list(self.correct_word)
        random.shuffle(letters)  # Перемешиваем буквы

        self.first_button.setText(letters[0])  # Устанавливаем буквы на кнопках
        self.second_button.setText(letters[1])
        self.third_button.setText(letters[2])

    def add_letter(self, letter):  # Добавляем букву в текстовое поле
        current_text = self.text_field.text()
        if letter not in current_text:  # Проверяем, что буква ещё не введена
            new_text = current_text + letter
            self.text_field.setText(new_text)

            if len(new_text) == len(self.correct_word):  # Проверяем длину слова
                if new_text == self.correct_word:  # Проверяем правильность слова
                    self.open_victory_window()  # Показываем окно победы

    def open_victory_window(self):  # Показываем окно победы
        self.victory_window = Victory_Window()
        self.setCentralWidget(self.victory_window)

    def return_to_level_window(self):  # Возвращаемся к выбору уровней
        self.level_window = LevelWindow()
        self.setCentralWidget(self.level_window)

    def delete_letter(self):  # Удаляем последнюю введённую букву
        self.text_field.setText(self.text_field.text()[:-1])

class Level_Two(QMainWindow):  # Класс для окна второго уровня
    def __init__(self):
        super().__init__()
        self.correct_word = ''  # Правильное слово, которое нужно собрать
        self.initUI()  # Инициализация интерфейса

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
        text_field_width = 600  # Ширина текстового поля
        text_field_height = 100  # Высота текстового поля
        self.text_field.setGeometry((self.width() - text_field_width) // 2,
                                    (self.height() - text_field_height) // 2 - 200,
                                    text_field_width, text_field_height)
        self.text_field.setReadOnly(True)  # Отключаем ввод с клавиатуры
        self.text_field.setAlignment(Qt.AlignCenter)  # Центрируем текст
        self.text_field.setStyleSheet("""font: 55pt "MS Shell Dlg 2"; color: purple;""")  # Стилизация текстового поля
        self.text_field.show()  # Показываем текстовое поле

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
        button_size = 190  # Размер кнопок
        button_spacing = 50  # Расстояние между кнопками
        total_width = 4 * button_size + 3 * button_spacing  # Общая ширина кнопок с учетом расстояний
        start_x = (self.width() - total_width) // 2  # Начальная позиция по горизонтали
        start_y = (self.height() + text_field_height) // 2  # Позиция под текстовым полем

        self.buttons = [self.first_button, self.second_button, self.third_button, self.fourth_button]
        for i, button in enumerate(self.buttons):
            button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                           font: 40pt "MS Shell Dlg 2";
                                                           background-color: rgba(85, 0, 127, 128);}  /* 50% прозрачности */
                                                          QPushButton:hover {background-color: rgba(33, 0, 50, 128);} """)
            button.setGeometry(start_x + i * (button_size + button_spacing), start_y, button_size, button_size)
            button.show()  # Показываем кнопку

        self.generate_letters()  # Генерируем буквы для кнопок

        # Кнопка для закрытия уровня и возврата к выбору уровней
        self.close_level_one_button = QPushButton('<', self)
        self.close_level_one_button.clicked.connect(self.return_to_level_window)
        self.close_level_one_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                               font: 14pt \"MS Shell Dlg 2\";
                                                               background-color: rgb(170, 170, 255);}
                                                          QPushButton:hover {background-color: rgb(125, 125, 188);} """)
        button_size = 150  # Размер кнопки
        self.close_level_one_button.setGeometry(20, self.height() - button_size - 10, button_size, button_size)
        self.close_level_one_button.show()  # Показываем кнопку

        # Добавляем кнопку для удаления последней введенной буквы
        self.delete_letter_button = QPushButton('Отменить', self)
        self.delete_letter_button.clicked.connect(self.delete_letter)
        self.delete_letter_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                                font: 14pt \"MS Shell Dlg 2\";
                                                                background-color: rgb(255, 85, 85);}
                                                           QPushButton:hover {background-color: rgb(188, 0, 0);} """)
        button_size = 150  # Размер кнопки
        self.delete_letter_button.setGeometry(self.width() - button_size - 20, self.height() - button_size - 20, button_size, button_size)
        self.delete_letter_button.show()  # Показываем кнопку

    def generate_letters(self):  # Генерация букв для кнопок
        words = ['свет', 'снег', 'луна', 'река', 'море', 'гора', 'шлюз', 'день', 'ночь', 'путь',
                 'фара', 'игра', 'смех', 'небо', 'вода', 'йога', 'мыло', 'лень', 'лапа', 'лото',
                 'кофе', 'енот', 'жрец', 'изба', 'стол', 'рука', 'мост', 'лист', 'лето', 'зима',
                 'пюре', 'филе', 'крюк', 'круг', 'духи', 'щука', 'дата', 'перо', 'село', 'мода']
        self.correct_word = random.choice(words)  # Выбираем случайное слово
        letters = list(self.correct_word)  # Превращаем слово в список букв
        random.shuffle(letters)  # Перемешиваем буквы

        # Устанавливаем буквы на кнопки
        self.first_button.setText(letters[0])
        self.second_button.setText(letters[1])
        self.third_button.setText(letters[2])
        self.fourth_button.setText(letters[3])

    def add_letter(self, button):  # Добавление буквы в текстовое поле
        letter = button.text()  # Получаем текст кнопки (букву)
        current_text = self.text_field.text()  # Текущий текст в текстовом поле
        new_text = current_text + letter  # Добавляем букву к текущему тексту
        self.text_field.setText(new_text)  # Устанавливаем новый текст в текстовое поле
        button.setEnabled(False)  # Отключаем кнопку после нажатия

        if len(new_text) == len(self.correct_word):  # Проверяем, если длина введенного слова совпадает с правильным словом
            if new_text == self.correct_word:  # Проверяем, если введенное слово правильное
                self.open_victory_window()  # Показываем окно победы

    def open_victory_window(self):  # Открытие окна победы
        self.victory_window = Victory_Window()  # Создаем экземпляр окна победы
        self.setCentralWidget(self.victory_window)  # Устанавливаем окно победы как центральное виджет

    def return_to_level_window(self):  # Возврат к выбору уровней
        self.level_window = LevelWindow()  # Создаем экземпляр окна выбора уровней
        self.setCentralWidget(self.level_window)  # Устанавливаем окно выбора уровней как центральное виджет

    def delete_letter(self):  # Удаление последней введенной буквы
        current_text = self.text_field.text()  # Текущий текст в текстовом поле
        if current_text:  # Проверяем, если текстовое поле не пустое
            last_letter = current_text[-1]  # Получаем последнюю букву
            self.text_field.setText(current_text[:-1])  # Удаляем последнюю букву из текстового поля
            for button in self.buttons:  # Активируем кнопку с удаленной буквой
                if button.text() == last_letter:
                    button.setEnabled(True)
                    break  # Прекращаем цикл после активации кнопки

class Level_Three(QMainWindow):  # Класс для окна третьего уровня
    def __init__(self):
        super().__init__()
        self.correct_word = ''  # Правильное слово, которое нужно собрать
        self.initUI()  # Инициализация интерфейса
        self.button_states = [False, False, False, False, False]  # Состояние кнопок: False - кнопка не нажата, True - кнопка нажата

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
        text_field_width = 600  # Ширина текстового поля
        text_field_height = 100  # Высота текстового поля
        self.text_field.setGeometry((self.width() - text_field_width) // 2,
                                    (self.height() - text_field_height) // 2 - 200,
                                    text_field_width, text_field_height)
        self.text_field.setReadOnly(True)  # Отключаем ввод с клавиатуры
        self.text_field.setAlignment(Qt.AlignCenter)  # Центрируем текст
        self.text_field.setStyleSheet("""font: 55pt "MS Shell Dlg 2"; color: purple;""")  # Стилизация текстового поля
        self.text_field.show()  # Показываем текстовое поле

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
        button_size = 190  # Размер кнопок
        button_spacing = 50  # Расстояние между кнопками
        start_x = (self.width() - 5 * button_size - 4 * button_spacing) // 2  # Начальная позиция по горизонтали
        start_y = (self.height() + text_field_height) // 2  # Позиция под текстовым полем

        buttons = [self.first_button, self.second_button, self.third_button, self.fourth_button, self.fifth_button]
        self.buttons = buttons  # Сохраняем кнопки в атрибут класса
        for i, button in enumerate(buttons):
            button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                 font: 40pt "MS Shell Dlg 2";
                                                 background-color: rgba(85, 0, 127, 128);}  /* 50% прозрачность */
                                                QPushButton:hover {background-color: rgba(33, 0, 50, 128);} """)
            button.setGeometry(start_x + i * (button_size + button_spacing), start_y, button_size, button_size)
            button.show()  # Показываем кнопку

        self.generate_letters()  # Генерируем буквы для кнопок

        # Кнопка для закрытия уровня и возврата к выбору уровней
        self.close_level_one_button = QPushButton('<', self)
        self.close_level_one_button.clicked.connect(self.return_to_level_window)
        self.close_level_one_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                               font: 14pt \"MS Shell Dlg 2\";
                                                               background-color: rgb(170, 170, 255);}
                                                          QPushButton:hover {background-color: rgb(125, 125, 188);} """)
        button_size = 150  # Размер кнопки
        self.close_level_one_button.setGeometry(20, self.height() - button_size - 10, button_size, button_size)
        self.close_level_one_button.show()  # Показываем кнопку

        # Добавляем кнопку для удаления последней введенной буквы
        self.delete_letter_button = QPushButton('Отменить', self)
        self.delete_letter_button.clicked.connect(self.delete_letter)
        self.delete_letter_button.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                                                font: 14pt \"MS Shell Dlg 2\";
                                                                background-color: rgb(255, 85, 85);}
                                                           QPushButton:hover {background-color: rgb(188, 0, 0);} """)
        button_size = 150  # Размер кнопки
        self.delete_letter_button.setGeometry(self.width() - button_size - 20, self.height() - button_size - 20, button_size, button_size)
        self.delete_letter_button.show()  # Показываем кнопку

    def generate_letters(self):  # Генерация букв для кнопок
        words = ['вагон', 'багет', 'дуэль', 'башня', 'забор', 'ёршик', 'изъян', 'осень', 'весна', 'ягода',\
                 'газон', 'леший', 'зебра', 'козёл', 'ладья', 'номер', 'обида', 'океан', 'кошка', 'слеза',\
                 'чутьё', 'район', 'семья', 'приём', 'улица', 'фобия', 'хомяк', 'месяц', 'цапля', 'шпион',\
                 'пчела', 'шляпа', 'сироп', 'карта', 'пламя', 'мафия', 'чехол', 'мираж', 'юрист', 'мусор']
        self.correct_word = random.choice(words)  # Выбираем случайное слово
        letters = list(self.correct_word)  # Превращаем слово в список букв
        random.shuffle(letters)  # Перемешиваем буквы

        # Устанавливаем буквы на кнопки
        self.first_button.setText(letters[0])
        self.second_button.setText(letters[1])
        self.third_button.setText(letters[2])
        self.fourth_button.setText(letters[3])
        self.fifth_button.setText(letters[4])

    def add_letter(self, letter, index):  # Добавление буквы в текстовое поле
        if not self.button_states[index]:  # Проверяем, была ли уже нажата кнопка
            current_text = self.text_field.text()  # Текущий текст в текстовом поле
            new_text = current_text + letter  # Добавляем букву к текущему тексту
            self.text_field.setText(new_text)  # Устанавливаем новый текст в текстовое поле

            if len(new_text) == len(self.correct_word):  # Проверяем, если длина введенного слова совпадает с правильным словом
                if new_text == self.correct_word:  # Проверяем, если введенное слово правильное
                    self.open_victory_window()  # Показываем окно победы

            self.button_states[index] = True  # Устанавливаем состояние кнопки как нажатая

    def open_victory_window(self):  # Открытие окна победы
        self.victory_window = Victory_Window()  # Создаем экземпляр окна победы
        self.setCentralWidget(self.victory_window)  # Устанавливаем окно победы как центральный виджет

    def return_to_level_window(self):  # Возврат к выбору уровней
        self.level_window = LevelWindow()  # Создаем экземпляр окна выбора уровней
        self.setCentralWidget(self.level_window)  # Устанавливаем окно выбора уровней как центральный виджет

    def delete_letter(self):  # Удаление последней введенной буквы
        current_text = self.text_field.text()  # Текущий текст в текстовом поле
        if current_text:  # Проверяем, если текстовое поле не пустое
            last_letter = current_text[-1]  # Получаем последнюю букву
            self.text_field.setText(current_text[:-1])  # Удаляем последнюю букву из текстового поля

            # Определяем индекс кнопки, соответствующей последней удаленной букве
            for i, button in enumerate(self.buttons):
                if button.text() == last_letter and self.button_states[i]:  # Проверяем состояние кнопки и текст
                    self.button_states[i] = False  # Сбрасываем состояние кнопки
                    break  # Прекращаем цикл после сброса состояния кнопки

class Victory_Window(QMainWindow):  # Класс для окна победы
    def __init__(self):
        super().__init__()
        self.initUI()  # Инициализация интерфейса

    def initUI(self):
        self.showFullScreen()  # Открываем окно в полноэкранном режиме

        # Устанавливаем изображение фона
        self.label = QLabel(self)
        self.pixmap = QPixmap('qt/victory.png')
        self.label.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)  # Устанавливаем изображение как центральный виджет

        # Добавляем надпись "Победа".
        self.victory_label = QLabel("Победа!", self)
        self.victory_label.setStyleSheet("font: 75 56pt \"Studio Var\";\n"
                                         "color: rgb(85, 0, 127);")  # Стилизация надписи
        self.victory_label.setAlignment(Qt.AlignCenter)  # Выравнивание текста по центру
        # Устанавливаем координаты для надписи "Победа!"
        self.victory_label.setGeometry((self.width() - 200) // 2 - 115, (self.height() - 70) // 2 - 150, 450, 160)
        self.victory_label.show()  # Показываем надпись

        # Создаем кнопку "На главное меню"
        self.forever = QPushButton('На главное меню', self)
        self.forever.setStyleSheet("""QPushButton {color: rgb(255, 255, 255);
                                        font: 14pt \"MS Shell Dlg 2\";
                                        background-color: rgba(235, 146, 147, 0.8);}
                                        QPushButton:hover {background-color: rgba(129, 80, 81, 0.8);} """)  # Стилизация кнопки
        self.forever.resize(350, 90)  # Устанавливаем размер кнопки
        self.forever.clicked.connect(
            self.level_selection_Window)  # Подключаем кнопку к функции возврата на главное меню

        # Устанавливаем позицию кнопки
        self.forever.move((self.width() - self.forever.width()) // 2, (self.height() - self.forever.height()) // 2 + 30)
        self.forever.show()  # Показываем кнопку

    def level_selection_Window(self):  # Возврат на главное меню
        self.main_window = MainWindow()  # Создаем экземпляр главного окна
        self.setCentralWidget(self.main_window)  # Устанавливаем главное окно как центральный виджет

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
