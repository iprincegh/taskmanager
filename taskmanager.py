import sys
from PyQt5.QtWidgets import (
    QApplication, QComboBox, QMainWindow, QVBoxLayout, QDateEdit, QWidget, QPushButton, QListWidget, QLineEdit, QHBoxLayout, QMessageBox, QCheckBox
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QColor, QBrush, QFont, QIcon

class StartPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Priority Task Manager')
        self.setGeometry(100, 100, 1920, 1280)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()

        # Add a button to start the task manager
        self.planTaskButton = QPushButton('Get Started')
        self.planTaskButton.setMinimumWidth(400)
        self.planTaskButton.setMinimumHeight(100)
        self.planTaskButton.setStyleSheet(
            'QPushButton {'
            'background-color: #FE0780; '
            'color: white; '
            'font-size: 18px; '
            'padding: 10px; '
            'border-radius: 10px;'
            '}'
            'QPushButton:hover {'
            'background-color: darkred;'
            '}'
        )
        self.planTaskButton.setCursor(Qt.PointingHandCursor)
        self.planTaskButton.clicked.connect(self.openTaskManager)



        # Add widgets to layout
        layout.addWidget(self.planTaskButton, alignment=Qt.AlignCenter)

        central_widget.setStyleSheet(
            "background-image: url('/Users/iprincetech/Documents/Intro Software Programming/taskmanager/startupImage.jpg'); background-repeat: no-repeat; background-position: center;"
        )
        central_widget.setLayout(layout)

    def openTaskManager(self):
        self.taskManager = TaskManagerGUI()
        self.taskManager.show()
        self.close()

class TaskManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Priority Task Manager')
        self.setGeometry(100, 100, 1920, 1280)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        form_layout = QHBoxLayout()

        # Widgets
        self.taskList = QListWidget()
        self.taskList.setSelectionMode(QListWidget.MultiSelection)

        self.taskName = QLineEdit()
        self.taskName.setPlaceholderText('Enter task name')

        self.taskPriority = QComboBox()
        self.taskPriority.addItem('Select task priority')
        self.taskPriority.addItem(QIcon('high.png'), 'High')
        self.taskPriority.addItem(QIcon('medium.png'), 'Medium')
        self.taskPriority.addItem(QIcon('low.png'), 'Low')

        self.taskDueDate = QDateEdit()
        self.taskDueDate.setCalendarPopup(True)
        self.taskDueDate.setDisplayFormat('yyyy-MM-dd')
        self.taskDueDate.setDateRange(QDate.currentDate(), QDate(9999, 12, 31))

        self.addTaskButton = QPushButton('Add Task')
        self.deleteTaskButton = QPushButton('Delete Selected Task')
        self.toggleStatusButton = QPushButton('Toggle Task Status')

        self.showCompletedCheckbox = QCheckBox('Show Completed Tasks')
        self.showCompletedCheckbox.setChecked(True)

        # Add widgets to layouts
        form_layout.addWidget(self.taskName)
        form_layout.addWidget(self.taskPriority)
        form_layout.addWidget(self.taskDueDate)
        form_layout.addWidget(self.addTaskButton)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.taskList)
        main_layout.addWidget(self.showCompletedCheckbox)
        main_layout.addWidget(self.deleteTaskButton)
        main_layout.addWidget(self.toggleStatusButton)

        # Set layout to central widget
        central_widget.setLayout(main_layout)

        # Connect signals and slots
        self.addTaskButton.clicked.connect(self.addTask)
        self.deleteTaskButton.clicked.connect(self.deleteTask)
        self.toggleStatusButton.clicked.connect(self.toggleStatus)
        self.showCompletedCheckbox.stateChanged.connect(self.updateTaskView)

    def addTask(self):
        taskName = self.taskName.text().strip()
        priority = self.taskPriority.currentText()
        dueDate = self.taskDueDate.date().toString('yyyy-MM-dd')

        if not taskName:
            QMessageBox.warning(self, 'Input Error', 'Task name cannot be empty!')
            return

        if priority == 'Select task priority':
            QMessageBox.warning(self, 'Input Error', 'Please select a task priority!')
            return

        if self.taskDueDate.date() < QDate.currentDate():
            QMessageBox.warning(self, 'Input Error', 'Due date cannot be in the past!')
            return

        for index in range(self.taskList.count()):
            existingTask = self.taskList.item(index).text()
            if taskName in existingTask:
                QMessageBox.warning(self, 'Duplicate Task', f"Task '{taskName}' already exists!")
                return

        taskItem = f"{taskName} | Priority: {priority} | Due: {dueDate} | Status: Pending"

        # Add task to the list
        self.taskList.addItem(taskItem)

        # Customize task appearance
        listItem = self.taskList.item(self.taskList.count() - 1)
        if priority == 'High':
            listItem.setBackground(QBrush(QColor('red')))
        elif priority == 'Medium':
            listItem.setBackground(QBrush(QColor('yellow')))
        else:
            listItem.setBackground(QBrush(QColor('green')))

        font = QFont()
        font.setBold(True)
        listItem.setFont(font)

        # Clear inputs
        self.taskName.clear()
        self.taskPriority.setCurrentIndex(0)
        self.taskDueDate.setDate(QDate.currentDate())

        QMessageBox.information(self, 'Task Added', f"Task '{taskName}' has been added successfully!")

    def deleteTask(self):
        selectedItems = self.taskList.selectedItems()
        if not selectedItems:
            QMessageBox.warning(self, 'Selection Error', 'No task selected!')
            return

        confirm = QMessageBox.question(
            self,
            'Confirm Deletion',
            'Are you sure you want to delete the selected task(s)?',
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            for item in selectedItems:
                self.taskList.takeItem(self.taskList.row(item))

            QMessageBox.information(self, 'Task Deleted', 'Selected task(s) have been deleted successfully!')

    def toggleStatus(self):
        selectedItems = self.taskList.selectedItems()
        if not selectedItems:
            QMessageBox.warning(self, 'Selection Error', 'No task selected!')
            return

        for item in selectedItems:
            text = item.text()
            if 'Pending' in text:
                item.setText(text.replace('Pending', 'Completed'))
                item.setForeground(QBrush(QColor('gray')))
            elif 'Completed' in text:
                item.setText(text.replace('Completed', 'Pending'))
                item.setForeground(QBrush(QColor('black')))

        QMessageBox.information(self, 'Status Toggled', 'Status of selected task(s) has been toggled!')

    def updateTaskView(self):
        showCompleted = self.showCompletedCheckbox.isChecked()
        for index in range(self.taskList.count()):
            item = self.taskList.item(index)
            if 'Completed' in item.text() and not showCompleted:
                item.setHidden(True)
            else:
                item.setHidden(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    startPage = StartPage()
    startPage.show()
    sys.exit(app.exec_())
