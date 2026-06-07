import sys
from send2trash import send2trash
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from backend.scanner import scan_duplicates
from backend.utils import format_size
from PyQt6.QtGui import QIcon



from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QFileDialog,
    QLabel,
    QVBoxLayout,
    QListWidget,
)


class DuplicateFinder(QWidget):
    
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Duplicate")
        self.setGeometry(200,200,600,400)

        self.folder_path =""

        #Label
        self.label = QLabel("Select Folder")

        #Buttons
        self.select_button = QPushButton("Browse Folder")
        self.select_button.clicked.connect(self.select_folder)

        self.scan_button = QPushButton("Scan Duplicates")
        self.scan_button.clicked.connect(self.scan_duplicates)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_selected)


        self.image_label = QLabel("Image Preview")
        self.image_label.setMinimumSize(500 , 300)

        self.image_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        
        #List
        self.result_list = QListWidget()
        self.result_list.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )
        self.result_list.itemClicked.connect(self.show_image)

        self.setWindowIcon(
            QIcon("assets/icon.png")
        )


        #Layout
        layout = QVBoxLayout()

        layout.addWidget(self.label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.image_label)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.result_list)

        layout.addStretch()
        

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
                font-size: 14px;
            }

            #topFrame {
                background-color: #252526;
                border-radius: 15px;
                padding: 15px;
            }

            #titleLabel {
                font-size: 18px;
                font-weight: bold;
                padding-bottom: 10px;
            }

            QPushButton {
                background-color: #3a3d41;
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #4b4f54;
            }

            QListWidget {
                background-color: #2d2d30;
                border-radius: 10px;
                padding: 5px;
            }

            #preview {
                background-color: #2d2d30;
                border-radius: 10px;
                border: 2px dashed #555;
            }
        """)
    

    def select_folder(self):

        folder = QFileDialog.getExistingDirectory(self , "Select Folder")

        if folder:
            self.folder_path = folder
            self.label.setText(f"Selected: {folder}")

    def scan_duplicates(self):

        self.result_list.clear()

        result = scan_duplicates(
            self.folder_path
            
        )

        duplicates = result["duplicates"]

        size = result["size"]

        for item in duplicates:
            
            self.result_list.addItem(
                item["duplicate"]
            )

        #size 
        self.image_label.setText(
            f"Saved Space : {format_size(size)}"
        )


    
    def delete_selected(self):

        items = self.result_list.selectedItems()

        for item in items:

            file_path = item.text()

            send2trash(file_path)

            self.result_list.takeItem(
                self.result_list.row(item)
            )

        self.image_label.setText("Deleted")
            
    

    def show_image(self , item):
        file_path = item.text()

        pixmap = QPixmap(file_path)

        if pixmap.isNull():
            self.image_label.setText("Cann't Load Image")
            return

        pixmap = pixmap.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.image_label.setPixmap(pixmap)


app = QApplication(sys.argv)

app.setStyle("Fusion")

window = DuplicateFinder()
window.show()

sys.exit(app.exec())  