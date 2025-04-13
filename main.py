import os
from PIL import Image
from PIL.ImageQt import ImageQt
from itertools import product
import sys
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QFileDialog, QLabel, QWidget, QVBoxLayout
)

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("mainwindow.ui", self)
        self.currentFile = None
        self.pushButton_open.clicked.connect(self.open)
        self.pushButton_gen.clicked.connect(self.generate)
        self.statusbar = self.statusBar()

        self.label_image = QLabel("")
        self.statusbar.addPermanentWidget(self.label_image)

        self.outputContainer = QWidget()
        self.outputLayout = QVBoxLayout(self.outputContainer)
        self.scrollArea_output.setWidget(self.outputContainer)
        self.scrollArea_output.setWidgetResizable(True)

    def open(self):
        dialog, _ = QFileDialog.getOpenFileName(
            self, "Otwórz Plik", "", "All Files (*);; Images (*.png;*.jpg;*.ico)"
        )
        if dialog:
            self.currentFile = dialog
            self.label_image.setText(dialog)
            pixmap = QPixmap(dialog)
            height = self.label_input.height()
            scaled = pixmap.scaledToHeight(height, Qt.TransformationMode.SmoothTransformation)
            self.label_input.setPixmap(scaled)

    def generate(self):
        if not self.currentFile:
            return

        image_path = self.currentFile
        folder_path = os.path.dirname(image_path)
        image_filename = os.path.basename(image_path)

        output_dir = os.path.join(folder_path, f"{os.path.splitext(image_filename)[0]}_output")
        os.makedirs(output_dir, exist_ok=True)

        image = Image.open(image_path)

        has_alpha = image.mode in ("RGBA", "LA")
        image = image.convert("RGBA") if has_alpha else image.convert("RGB")

        data = list(image.getdata())

        letters = ['r', 'g', 'b']
        combinations = [combo for combo in product(letters, repeat=3) if combo != ('r', 'g', 'b')]

        original_name = os.path.splitext(image_filename)[0]

        color_index = {'r': 0, 'g': 1, 'b': 2}
        checkboxes = {
            'r': self.checkBox_r.isChecked(),
            'g': self.checkBox_g.isChecked(),
            'b': self.checkBox_b.isChecked(),
        }

        total_tasks = len(combinations) * sum(checkboxes.values())
        current_task = 0
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(total_tasks)

        for i in reversed(range(self.outputLayout.count())):
            widgetToRemove = self.outputLayout.itemAt(i).widget()
            self.outputLayout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)

        for color_to_replace, is_checked in checkboxes.items():
            if not is_checked:
                continue

            replace_idx = color_index[color_to_replace]

            modified_images = [image]

            for combo in combinations:
                new_data = []

                for item in data:
                    r, g, b = item[:3]
                    a = item[3] if has_alpha else 255

                    color_values = [r, g, b]
                    if color_values[replace_idx] > max(color_values[:replace_idx] + color_values[replace_idx + 1:]):
                        new_r = r if combo[0] == 'r' else g if combo[0] == 'g' else b
                        new_g = r if combo[1] == 'r' else g if combo[1] == 'g' else b
                        new_b = r if combo[2] == 'r' else g if combo[2] == 'g' else b
                        new_data.append((new_r, new_g, new_b, a) if has_alpha else (new_r, new_g, new_b))
                    else:
                        new_data.append(item)

                new_image = image.copy()
                new_image.putdata(new_data)
                modified_images.append(new_image)

                filename_suffix = "".join(combo)
                file_extension = os.path.splitext(image_filename)[1]
                modified_image_path = os.path.join(output_dir,
                                                   f'{original_name}_{color_to_replace}_{filename_suffix}{file_extension}')
                new_image.save(modified_image_path)

                current_task += 1
                self.progressBar.setValue(current_task)
                QApplication.processEvents()

            grid_width = 9
            grid_height = 3
            image_width, image_height = image.size
            grid_image = Image.new("RGBA" if has_alpha else "RGB",
                                   (grid_width * image_width, grid_height * image_height))

            for index, img in enumerate(modified_images):
                x_offset = (index % grid_width) * image_width
                y_offset = (index // grid_width) * image_height
                grid_image.paste(img, (x_offset, y_offset))

            grid_image_path = os.path.join(output_dir, f"{original_name}_{color_to_replace}_all{file_extension}")
            grid_image.save(grid_image_path)

            qt_image = ImageQt(grid_image)
            pixmap = QPixmap.fromImage(qt_image)
            pixmap = pixmap.scaledToWidth(720)

            grid_label = QLabel()
            grid_label.setPixmap(pixmap)
            grid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.outputLayout.addWidget(grid_label)

        self.progressBar.setValue(self.progressBar.maximum())


app = QApplication(sys.argv)
window = Window()
window.show()

app.exec()
