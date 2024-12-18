# -*- coding: utf-8 -*-
import qdarkstyle

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QMainWindow, QPlainTextEdit,
    QPushButton, QRadioButton, QSizePolicy, QWidget, QSpinBox, QLabel, QCheckBox,
                               QScrollBar, QTabWidget, QFileDialog, QLineEdit)

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 519)
        MainWindow.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='PySide6'))
        custom_font = QFont()
        custom_font.setPointSize(11)
        QApplication.setFont(custom_font, "QLabel")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        # Tab widget
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setGeometry(0, 0, 800, 519)

        # Tab 1: Text
        self.tab_text = QWidget()
        self.tab_text.setObjectName("tab_text")
        self.groupBox = QGroupBox(self.tab_text)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 280, 471))
        self.radioButton_translate = QCheckBox(self.groupBox)
        self.radioButton_translate.setObjectName(u"radioButton")
        self.radioButton_translate.setGeometry(QRect(10, 30, 91, 22))
        self.radioButton_translate.setChecked(True)
        self.radioButton_summarize = QCheckBox(self.groupBox)
        self.radioButton_summarize.setObjectName(u"radioButton_2")
        self.radioButton_summarize.setGeometry(QRect(90, 30, 91, 22))
        self.plainTextEdit_language = QPlainTextEdit(self.groupBox)
        self.plainTextEdit_language.setObjectName(u"plainTextEdit_language")
        self.plainTextEdit_language.setGeometry(QRect(80, 70, 91, 28))
        self.plainTextEdit_language.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.label_language = QLabel(self.groupBox)
        self.label_language.setGeometry(5, 65, 70, 30)
        self.label_language.setStyleSheet('''font-size: 12px;''')
        # self.spinBox_n = QSpinBox(self.groupBox)
        # self.spinBox_n.setObjectName(u"spinBox_n")
        # self.spinBox_n.setGeometry(QRect(40, 60, 91, 25))
        # self.spinBox_n.setMaximum(10)
        # self.spinBox_n.setValue(4)
        # self.label_k = QLabel(self.groupBox)
        # self.label_k.setGeometry(10, 90, 91, 25)
        # self.spinBox_k = QSpinBox(self.groupBox)
        # self.spinBox_k.setObjectName(u"spinBox_k")
        # self.spinBox_k.setGeometry(QRect(40, 90, 91, 25))
        # self.spinBox_k.setMaximum(10)
        # self.spinBox_k.setValue(3)
        self.groupBox_seed = QGroupBox(self.groupBox)
        self.groupBox_seed.setObjectName(u"groupBox_seed")
        self.groupBox_seed.setGeometry(QRect(10, 120, 250, 150))
        self.radioButton_url = QRadioButton(self.groupBox_seed)
        self.radioButton_url.setObjectName(u"radioButton_url")
        self.radioButton_url.setGeometry(QRect(10, 10, 120, 40))

        self.plainTextEdit_url = QPlainTextEdit(self.groupBox_seed)
        self.plainTextEdit_url.setObjectName(u"plainTextEdit_language")
        self.plainTextEdit_url.setGeometry(QRect(10, 50, 200, 50))
        # self.plainTextEdit_language.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


        self.plainTextEdit_input = QPlainTextEdit(self.tab_text)
        self.plainTextEdit_input.setObjectName(u"plainTextEdit")
        self.plainTextEdit_input.setGeometry(QRect(300, 110, 431, 161))
        self.plainTextEdit_result = QPlainTextEdit(self.tab_text)
        self.plainTextEdit_result.setObjectName(u"plainTextEdit_2")
        self.plainTextEdit_result.setGeometry(QRect(300, 290, 431, 161))
        self.plainTextEdit_result.setReadOnly(True)
        self.pushButton_convert = QPushButton(self.tab_text)
        self.pushButton_convert.setObjectName(u"pushButton")
        self.pushButton_convert.setGeometry(QRect(300, 460, 80, 24))
        # self.pushButton_save_to_file = QPushButton(self.centralwidget)
        # self.pushButton_save_to_file.setObjectName(u"pushButton_2")
        #
        self.tabWidget.addTab(self.tab_text, "Text")  # Add "Text" tab

        # Tab 2: Document
        self.tab_document = QWidget()
        self.tab_document.setObjectName("tab_document")

        # Add radio buttons to the "Document" tab
        self.radioButton_student_id = QRadioButton(self.tab_document)
        self.radioButton_student_id.setObjectName("radioButton_student_id")
        self.radioButton_student_id.setGeometry(QRect(10, 50, 100, 30))  # Adjust position as needed
        self.radioButton_student_id.setText("Student ID")
        self.radioButton_student_id.setChecked(True)

        self.radioButton_invoice = QRadioButton(self.tab_document)
        self.radioButton_invoice.setObjectName("radioButton_invoice")
        self.radioButton_invoice.setGeometry(QRect(10, 90, 100, 30))  # Position below the PIT radio button
        self.radioButton_invoice.setText("Invoice")

        self.textEdit_output = QPlainTextEdit(self.tab_document)
        self.textEdit_output.setObjectName("textEdit_output")
        self.textEdit_output.setGeometry(QRect(350, 30, 400, 400))  # Positioned on the right side
        self.textEdit_output.setReadOnly(True)  # Make the output read-only

        # Add "File Browse" option under Invoice radio button
        self.fileBrowse_button = QPushButton(self.tab_document)
        self.fileBrowse_button.setObjectName("fileBrowse_button")
        self.fileBrowse_button.setText("Browse")
        self.fileBrowse_button.setGeometry(QRect(10, 170, 100, 30))  # Positioned below the Invoice button

        self.filePath_lineEdit = QLineEdit(self.tab_document)
        self.filePath_lineEdit.setObjectName("filePath_lineEdit")
        self.filePath_lineEdit.setGeometry(QRect(10, 130, 300, 30))  # Positioned next to the Browse button
        self.filePath_lineEdit.setReadOnly(True)  # Read-only to display the file path

        # Connect Browse button to a function
        self.fileBrowse_button.clicked.connect(MainWindow.browse_file)

        # Add "Analyze" button under the Browse button
        self.analyze_button = QPushButton(self.tab_document)
        self.analyze_button.setObjectName("analyze_button")
        self.analyze_button.setText("Analyze")
        self.analyze_button.setGeometry(QRect(10, 220, 100, 30))  # Positioned below the Browse button

        # Connect Analyze button to a function
        self.analyze_button.clicked.connect(MainWindow.analyze_file)

        self.tabWidget.addTab(self.tab_document, "Document")



        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

        # set signals
        self.pushButton_convert.clicked.connect(MainWindow.run)
        # self.spinBox_k.valueChanged.connect(MainWindow.spinBox_k_validate)
        # self.spinBox_n.valueChanged.connect(MainWindow.spinBox_n_validate)
        self.radioButton_url.toggled.connect(self.plainTextEdit_input.setDisabled)
        self.radioButton_url.toggled.connect(self.plainTextEdit_url.setEnabled)

        self.radioButton_translate.toggled.connect(MainWindow.translate_toggle_handler)
        # self.radioButton_combine.toggled.connect(MainWindow.combine_toggle_handler)

        self.plainTextEdit_url.setPlainText(
            'https://www.kumodigital.co.uk/a-beginners-guide-to-adding-images-to-articles/')
        self.radioButton_summarize.setChecked(True)
        self.radioButton_url.setChecked(True)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.radioButton_translate.setText(QCoreApplication.translate("MainWindow", u"Translate", None))
        self.radioButton_summarize.setText(QCoreApplication.translate("MainWindow", u"Summarize", None))
        self.plainTextEdit_input.setDocumentTitle("")
        self.plainTextEdit_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Input", None))
        self.plainTextEdit_result.setDocumentTitle("")
        self.plainTextEdit_result.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.pushButton_convert.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        # self.pushButton_save_to_file.setText(QCoreApplication.translate("MainWindow", u"Save result to file", None))
        self.radioButton_url.setText(QCoreApplication.translate("MainWindow", u"Article from URL", None))
        self.label_language.setText(QCoreApplication.translate("MainWindow", u"Language", None))
        self.textEdit_output.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Output", None))
    # retranslateUi