import sys
import random
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
)
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QIcon, QPixmap
from PyQt6.QtCore import Qt, QTimer, pyqtSignal


class SnakeGame(QWidget):
    score_updated = pyqtSignal(int)
    game_over_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = 10
        self.grid_width = 100
        self.grid_height = 80
        self.border_width = 2

        self.snake = [(50, 40), (49, 40), (48, 40)]
        self.direction = "right"
        self.food = self.generate_food()
        self.score = 0
        self.game_over_flag = False
        self.game_active = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)

        self.init_ui()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def init_ui(self):
        self.setFixedSize(
            self.grid_width * self.grid_size + 2 * self.border_width,
            self.grid_height * self.grid_size + 2 * self.border_width,
        )
        self.setStyleSheet("background-color: white;")

    def set_speed(self, speed):
        self.timer.stop()
        self.timer.start(speed)
        self.game_active = True
        print(f"Game speed set to: {speed} ms")  # Debug print

    def generate_food(self):
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                return x, y

    def update_game(self):
        if not self.game_active or self.game_over_flag:
            return

        head = self.snake[0]
        if self.direction == "right":
            new_head = (head[0] + 1, head[1])
        elif self.direction == "left":
            new_head = (head[0] - 1, head[1])
        elif self.direction == "up":
            new_head = (head[0], head[1] - 1)
        else:
            new_head = (head[0], head[1] + 1)

        if (
            new_head[0] < 0
            or new_head[0] >= self.grid_width
            or new_head[1] < 0
            or new_head[1] >= self.grid_height
            or new_head in self.snake[1:]
        ):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.food = self.generate_food()
            self.score += 1
            self.score_updated.emit(self.score)
        else:
            self.snake.pop()

        self.update()

    def game_over(self):
        self.timer.stop()
        self.game_over_flag = True
        self.game_active = False
        self.game_over_signal.emit()
        self.update()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key.Key_Escape:
            QApplication.instance().quit()

        if not self.game_active or self.game_over_flag:
            return

        if key in [Qt.Key.Key_Left, Qt.Key.Key_A] and self.direction != "right":
            self.direction = "left"
        elif key in [Qt.Key.Key_Right, Qt.Key.Key_D] and self.direction != "left":
            self.direction = "right"
        elif key in [Qt.Key.Key_Up, Qt.Key.Key_W] and self.direction != "down":
            self.direction = "up"
        elif key in [Qt.Key.Key_Down, Qt.Key.Key_S] and self.direction != "up":
            self.direction = "down"

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setPen(QPen(QColor(0, 0, 0), self.border_width))
        painter.drawRect(
            self.border_width // 2,
            self.border_width // 2,
            self.width() - self.border_width,
            self.height() - self.border_width,
        )

        painter.setPen(Qt.PenStyle.NoPen)

        painter.setBrush(QColor(0, 200, 0))
        for segment in self.snake[1:]:
            painter.drawRect(
                segment[0] * self.grid_size + self.border_width,
                segment[1] * self.grid_size + self.border_width,
                self.grid_size,
                self.grid_size,
            )

        painter.setBrush(QColor(0, 0, 0))
        head = self.snake[0]
        painter.drawRect(
            head[0] * self.grid_size + self.border_width,
            head[1] * self.grid_size + self.border_width,
            self.grid_size,
            self.grid_size,
        )

        painter.setBrush(QColor(255, 0, 0))
        painter.drawRect(
            self.food[0] * self.grid_size + self.border_width,
            self.food[1] * self.grid_size + self.border_width,
            self.grid_size,
            self.grid_size,
        )

        if self.game_over_flag:
            painter.setPen(QPen(QColor(255, 0, 0)))
            painter.setFont(QFont("Arial", 30))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "GAME OVER")

    def reset_game(self):
        self.snake = [(50, 40), (49, 40), (48, 40)]
        self.direction = "right"
        self.food = self.generate_food()
        self.score = 0
        self.game_over_flag = False
        self.game_active = False
        self.timer.stop()
        self.score_updated.emit(self.score)
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snake Game")

        icon = QIcon("D:\\我的图片\\snake.ico")
        self.setWindowIcon(icon)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.speed_selection_widget = QWidget()
        self.speed_selection_layout = QVBoxLayout()
        self.speed_selection_widget.setLayout(self.speed_selection_layout)

        self.setStyleSheet("background-color: #f0f0f0;")

        top_layout = QVBoxLayout()
        self.speed_selection_layout.addLayout(top_layout)

        icon_label = QLabel()
        icon_pixmap = QPixmap("D:\\我的图片\\snake.ico").scaled(
            100, 100, Qt.AspectRatioMode.KeepAspectRatio
        )
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(icon_label)

        title_label = QLabel("贪吃蛇")
        title_label.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        title_label.setStyleSheet("color: red;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(title_label)

        self.speed_label = QLabel("选择游戏速度")
        self.speed_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.speed_label.setStyleSheet("color: #333; margin-bottom: 20px;")
        self.speed_selection_layout.addWidget(
            self.speed_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.speeds = [
            ("很慢", 200),
            ("稍慢", 150),
            ("微快", 100),
            ("很快", 50),
            ("巨快", 25),
            ("超神", 15),
            ("单身", 10),
        ]

        self.speed_buttons = []
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(0, 0, 0, 0)

        for index, (text, speed) in enumerate(self.speeds):
            button = QPushButton(text)
            button.setFont(QFont("Arial", 16))
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: 2px solid #388E3C;
                    border-radius: 12px;
                    padding: 10px 20px;
                    margin: 5px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #388E3C;
                }
                QPushButton:focus {
                    background-color: #45a049;
                    border: 3px solid #FF4500;
                }
            """
            )
            button.clicked.connect(self.create_start_game_function(index))
            button_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
            self.speed_buttons.append(button)

        self.speed_selection_layout.addLayout(button_layout)
        self.speed_selection_layout.addStretch()

        self.game_widget = QWidget()
        self.game_layout = QVBoxLayout()
        self.game_widget.setLayout(self.game_layout)

        self.snake_game = SnakeGame(self)
        self.game_layout.addWidget(self.snake_game)

        self.score_label = QLabel("Score: 0")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setFont(QFont("Arial", 16))
        self.game_layout.addWidget(self.score_label)

        self.bottom_label = QLabel("")
        self.bottom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.game_layout.addWidget(self.bottom_label)

        self.stacked_widget.addWidget(self.speed_selection_widget)
        self.stacked_widget.addWidget(self.game_widget)

        self.stacked_widget.setCurrentWidget(self.speed_selection_widget)

        self.adjustSize()
        self.center_on_screen()

        self.snake_game.score_updated.connect(self.update_score)
        self.snake_game.game_over_signal.connect(self.show_game_over_message)

        self.current_speed_index = 0
        self.speed_buttons[self.current_speed_index].setFocus()

    def create_start_game_function(self, index):
        return lambda: self.start_game(index)

    def update_score(self, score):
        self.score_label.setText(f"Score: {score}")

    def show_game_over_message(self):
        self.bottom_label.setText("Game Over! Press Enter to restart or ESC to quit")
        self.bottom_label.setStyleSheet("color: red;")
        self.setFocus()

    def center_on_screen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2
        )

    def start_game(self, speed_index):
        self.stacked_widget.setCurrentWidget(self.game_widget)
        self.bottom_label.setText("")
        self.bottom_label.setStyleSheet("")
        self.snake_game.reset_game()
        speed = self.speeds[speed_index][1]
        print(f"Starting game with speed: {speed} ms")  # Debug print
        self.snake_game.set_speed(speed)
        self.snake_game.setFocus()
        self.current_speed_index = speed_index  # Store the current speed index

    def start_game_from_speed_selection(self):
        self.stacked_widget.setCurrentWidget(self.speed_selection_widget)
        self.bottom_label.setText("")
        self.bottom_label.setStyleSheet("")
        self.snake_game.reset_game()
        self.speed_buttons[self.current_speed_index].setFocus()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key.Key_Escape:
            QApplication.instance().quit()

        if self.stacked_widget.currentWidget() == self.game_widget:
            if self.snake_game.game_over_flag:
                if key == Qt.Key.Key_Return:
                    self.start_game_from_speed_selection()
            else:
                self.snake_game.keyPressEvent(event)
        elif self.stacked_widget.currentWidget() == self.speed_selection_widget:
            if key == Qt.Key.Key_Up:
                self.current_speed_index = (self.current_speed_index - 1) % len(
                    self.speeds
                )
                self.speed_buttons[self.current_speed_index].setFocus()
            elif key == Qt.Key.Key_Down:
                self.current_speed_index = (self.current_speed_index + 1) % len(
                    self.speeds
                )
                self.speed_buttons[self.current_speed_index].setFocus()
            elif key == Qt.Key.Key_Return:
                self.start_game(self.current_speed_index)

        super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
