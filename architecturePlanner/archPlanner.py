import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem,
    QGraphicsTextItem, QGraphicsItem, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QInputDialog, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPen


class ArchitectPlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Архитектурный планировщик")
        self.setGeometry(100, 100, 1200, 800)

        self.scale_factor = 60  # 1 метр = 100 пикселей

        # Центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Основной макет
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Создание сцены и представления
        self.current_page = 1
        self.pages = {}
        self.project_size = None
        self.rooms = []
        self.pages[self.current_page] = self.create_new_page()

        self.view = QGraphicsView(self.pages[self.current_page])
        self.layout.addWidget(self.view)

        # Панель инструментов
        self.controls_layout = QHBoxLayout()
        self.layout.addLayout(self.controls_layout)

        # Кнопки для управления страницами
        self.prev_page_button = QPushButton("Назад")
        self.prev_page_button.clicked.connect(self.previous_page)
        self.controls_layout.addWidget(self.prev_page_button)

        self.next_page_button = QPushButton("Вперёд")
        self.next_page_button.clicked.connect(self.next_page)
        self.controls_layout.addWidget(self.next_page_button)

        # Другие кнопки
        self.create_project_button = QPushButton("Создать проект")
        self.create_project_button.clicked.connect(self.create_project)
        self.controls_layout.addWidget(self.create_project_button)

        self.add_room_button = QPushButton("Добавить комнату")
        self.add_room_button.clicked.connect(self.add_room)
        self.controls_layout.addWidget(self.add_room_button)

        self.add_furniture_button = QPushButton("Добавить мебель")
        self.add_furniture_button.clicked.connect(self.add_furniture)
        self.controls_layout.addWidget(self.add_furniture_button)

        self.add_window_button = QPushButton("Добавить окно")
        self.add_window_button.clicked.connect(self.add_window)
        self.controls_layout.addWidget(self.add_window_button)

        self.add_door_button = QPushButton("Добавить дверь")
        self.add_door_button.clicked.connect(self.add_door)
        self.controls_layout.addWidget(self.add_door_button)

        self.show_areas_button = QPushButton("Показать площади")
        self.show_areas_button.clicked.connect(self.show_areas)
        self.controls_layout.addWidget(self.show_areas_button)

    def create_project(self):
        """Создать проект квартиры с заданным размером."""
        width, ok_width = QInputDialog.getDouble(self, "Ширина проекта", "Введите ширину помещения (в метрах):", 12)
        height, ok_height = QInputDialog.getDouble(self, "Длина проекта", "Введите высоту помещения (в метрах):", 7)
        if ok_width and ok_height:
            self.project_size = (width * self.scale_factor, height * self.scale_factor)  # преобразуем в пиксели
            for page in self.pages.values():
                page.clear()
                self.add_project_boundaries(page)

    def create_new_page(self):
        """Создать новую страницу проекта с границами, если размеры проекта заданы."""
        scene = QGraphicsScene()
        if self.project_size:
            self.add_project_boundaries(scene)
        return scene

    def add_project_boundaries(self, scene):
        """Добавить границы проекта на сцену."""
        width, height = self.project_size
        project_rect = QGraphicsRectItem(0, 0, width, height)
        project_rect.setPen(QPen(QColor("black"), 10))
        project_rect.setBrush(QBrush(Qt.white))
        scene.addItem(project_rect)
        self.view.setSceneRect(0, 0, width, height)

    def add_room(self):
        """Добавить комнату."""
        if not self.project_size:
            QMessageBox.warning(self, "Ошибка", "Сначала создайте проект!")
            return
        width, ok_width = QInputDialog.getDouble(self, "Ширина комнаты", "Введите ширину комнаты (в метрах):", 3)
        height, ok_height = QInputDialog.getDouble(self, "Высота комнаты", "Введите высоту комнаты (в метрах):", 4)
        name, ok_name = QInputDialog.getText(self, "Название комнаты", "Введите название комнаты:")
        if ok_width and ok_height and ok_name:
            room = Room(0, 0, width * self.scale_factor, height * self.scale_factor, name)  # преобразуем в пиксели
            self.rooms.append(room)
            self.pages[self.current_page].addItem(room)

    def add_furniture(self):
        """Добавить мебель на план."""
        if not self.project_size:
            QMessageBox.warning(self, "Ошибка", "Сначала создайте проект!")
            return
        width, ok_width = QInputDialog.getDouble(self, "Ширина мебели", "Введите ширину мебели (в метрах):", 1)
        height, ok_height = QInputDialog.getDouble(self, "Высота мебели", "Введите высоту мебели (в метрах):", 1)
        name, ok_name = QInputDialog.getText(self, "Название мебели", "Введите название мебели:")
        if ok_width and ok_height and ok_name:
            furniture = Furniture(0, 0, width * self.scale_factor, height * self.scale_factor, name)  # преобразуем в пиксели
            self.pages[self.current_page].addItem(furniture)

    def add_window(self):
        """Добавить окно на проект."""
        if not self.project_size:
            QMessageBox.warning(self, "Ошибка", "Сначала создайте проект!")
            return
        width, ok_width = QInputDialog.getDouble(self, "Ширина окна", "Введите ширину окна (в метрах):", 1)
        height, ok_height = QInputDialog.getDouble(self, "Высота окна", "Введите высоту окна (в метрах):", 1)
        if ok_width and ok_height:
            window = Window(0, 0, width * self.scale_factor, height * self.scale_factor)
            self.pages[self.current_page].addItem(window)

    def add_door(self):
        """Добавить дверь на проект."""
        if not self.project_size:
            QMessageBox.warning(self, "Ошибка", "Сначала создайте проект!")
            return
        width, ok_width = QInputDialog.getDouble(self, "Ширина двери", "Введите ширину двери (в метрах):", 1)
        height, ok_height = QInputDialog.getDouble(self, "Высота двери", "Введите высоту двери (в метрах):", 1)
        if ok_width and ok_height:
            door = Door(0, 0, width * self.scale_factor, height * self.scale_factor)
            self.pages[self.current_page].addItem(door)

    def previous_page(self):
        """Перейти на предыдущую страницу."""
        if self.current_page > 1:
            self.current_page -= 1
            self.view.setScene(self.pages[self.current_page])
        else:
            QMessageBox.warning(self, "Предупреждение", "Это первая страница!")

    def next_page(self):
        """Перейти на следующую страницу."""
        if self.current_page < len(self.pages):
            self.current_page += 1
            self.view.setScene(self.pages[self.current_page])
        else:
            # Добавить новую страницу, если она не существует
            self.current_page += 1
            self.pages[self.current_page] = self.create_new_page()
            self.view.setScene(self.pages[self.current_page])

    def show_areas(self):
        """Показать площади комнат и проекта."""
        if not self.project_size:
            QMessageBox.warning(self, "Ошибка", "Сначала создайте проект!")
            return

        project_area = (self.project_size[0] / self.scale_factor) * (self.project_size[1] / self.scale_factor)
        living_area = 0
        room_areas = []

        for room in self.rooms:
            room_area = (room.width / self.scale_factor) * (room.height / self.scale_factor)
            room_areas.append(f"{room.name}: {room_area:.2f} м²")
            if room.name.lower() in ["гостиная", "детская", "спальня"]:
                living_area += room_area

        message = (f"Общая площадь проекта: {project_area:.2f} м²\n"
                   f"Жилая площадь: {living_area:.2f} м²\n"
                   f"Площади комнат:\n" + "\n".join(room_areas))

        QMessageBox.information(self, "Площади", message)


class Room(QGraphicsRectItem):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height)
        self.name = name
        self.width = width
        self.height = height
        self.setBrush(QBrush(QColor("lightgray")))
        self.setPen(QPen(QColor("black"), 6))
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.text = QGraphicsTextItem(self)
        self.update_text()

    def update_text(self):
        """Обновить текст с размерами и названием комнаты."""
        room_width_m = self.width / 60  # Преобразование в метры
        room_height_m = self.height / 60  # Преобразование в метры
        self.text.setPlainText(f"{self.name}\n{room_width_m} м x {room_height_m} м")
        self.text.setDefaultTextColor(Qt.black)

        # Центрируем текст
        self.text.setPos(
            self.rect().width() / 2 - self.text.boundingRect().width() / 2,
            self.rect().height() / 2 - self.text.boundingRect().height() / 2
        )

class Furniture(QGraphicsRectItem):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height)
        self.name = name
        self.width = width
        self.height = height
        self.setBrush(QBrush(QColor("brown")))
        self.setPen(QPen(QColor("black"), 1))
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.text = QGraphicsTextItem(self)
        self.update_text()

    def update_text(self):
        """Обновить текст с размерами и названием мебели."""
        furniture_width_m = self.width / 60  # Преобразование в метры
        furniture_height_m = self.height / 60  # Преобразование в метры
        self.text.setPlainText(f"{self.name}\n{furniture_width_m} м x {furniture_height_m} м")
        self.text.setDefaultTextColor(Qt.white)

        # Центрируем текст
        self.text.setPos(
            self.rect().width() / 2 - self.text.boundingRect().width() / 2,
            self.rect().height() / 2 - self.text.boundingRect().height() / 2
        )

class Window(QGraphicsRectItem):
    def __init__(self, x, y, width, height, name="Окно"):
        super().__init__(x, y, width, height)
        self.name = name
        self.width = width
        self.height = height
        self.setBrush(QBrush(QColor("blue")))  # Цвет для окон
        self.setPen(QPen(QColor("black"), 2))
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

class Door(QGraphicsRectItem):
    def __init__(self, x, y, width, height, name="Дверь"):
        super().__init__(x, y, width, height)
        self.name = name
        self.width = width
        self.height = height
        self.setBrush(QBrush(QColor("darkgray")))  # Цвет для дверей
        self.setPen(QPen(QColor("black"), 2))
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArchitectPlanner()
    window.show()
    sys.exit(app.exec_())