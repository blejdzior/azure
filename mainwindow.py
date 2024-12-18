from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from ui_mainwindow import Ui_MainWindow
from translator import *
from article import *
from documents import *
import json

import time
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_translate = None
        self.is_summarize = None
        self.is_url = None
        self.url = None
        self.input = None
        self.language = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def run(self):
        self.set_data()
        if self.is_url:
            self.run_url()
        else:
            self.run_plain()



    def run_url(self):

        if self.is_summarize:
            result = summarize_article_from_url(self.url)
        if self.is_translate:
            result = translate_text(result, self.language)
        save_summary_to_pdf(result, 'markdown/result.pdf')

    def run_plain(self):
        result = self.input
        if self.is_summarize:
            result = summarize_plain_text(result)
        if self.is_translate:
            result = translate_text(result, self.language)
        self.ui.plainTextEdit_result.insertPlainText(result)

    # saves input from GUI
    def set_data(self):
        self.input = self.ui.plainTextEdit_input.toPlainText()
        self.is_url = self.ui.radioButton_url.isChecked()
        self.is_translate = self.ui.radioButton_translate.isChecked()
        self.is_summarize = self.ui.radioButton_summarize.isChecked()

        if self.is_url:
            self.url = self.ui.plainTextEdit_url.toPlainText()
        if self.is_translate:
            self.language = self.ui.plainTextEdit_language.toPlainText()



    def translate_toggle_handler(self):
        state = self.ui.radioButton_translate.isChecked()
        self.ui.plainTextEdit_language.setEnabled(state)

    def combine_toggle_handler(self):
        self.ui.spinBox_k.setEnabled(False)
        self.ui.spinBox_n.setEnabled(False)
        self.ui.groupBox_seed.setEnabled(False)


    def browse_file(self):
        # Open a file dialog to select the file
        file_path, _ = QFileDialog.getOpenFileName(None, "Select File", "", "All Files (*)")

        if file_path:  # If a file is selected
            self.ui.filePath_lineEdit.setText(file_path)  # Display the file path in the QLineEdit

    def analyze_file(self):
        # Get the file path from the QLineEdit
        file_path = self.ui.filePath_lineEdit.text()
        result = None
        if file_path:
            self.ui.textEdit_output.setPlainText(f"Analyzing file:\n{file_path}")
            if self.ui.radioButton_student_id.isChecked():
                result = analyze_student_id(file_path)
            elif self.ui.radioButton_invoice.isChecked():
                result = analyze_invoice(file_path)
            else:
                self.ui.textEdit_output.setPlainText("Check either PIT or Invoice type of file")
                return
            result = json.dumps(result, indent=4, sort_keys=True, default=str)
            self.ui.textEdit_output.setPlainText(result)
            with open('result.json', 'w') as f:
                f.write(result)
        else:
            self.ui.textEdit_output.setPlainText("No file selected. Please select a file to analyze.")
