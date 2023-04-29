import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
import random
import time
import enum
from queue import PriorityQueue
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtGui import QPixmap, QIcon
from Project import *



class PushButton(QPushButton):
    def __init__(self, text, style, row, column, color, parent=None):
        super(PushButton, self).__init__(text, parent)
        self.setStyleSheet(style)
        self.setText(text)
        self.setMinimumSize(QSize(35, 35))
        self.setMaximumSize(QSize(35, 35))
        self.color = color




class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        width=1000
        height=700
        self.setFixedSize(width, height)


        self.row = 20
        self.column = 30

        self.Buttons = [[0 for _ in range(self.column)] for __ in range(self.row)]
        self.list_of_blocks = []
        self.list_of_foods = []
        self.pacman = []
        self.dict_of_values_buttons = {}


        self.Styles = {
            "White": """
                background-color:white;
                max-height:25px;
                max-width:25px;
                border :0.5px solid gray;
                padding-left: 0px;
                padding-right: 0px;
                """,
            "Black": """
                background-color:black;
                max-height:25px;
                max-width:25px;
                border :0.5px solid gray;
                padding-left: 0px;
                padding-right: 0px;
                """,
            }




        Widget = QWidget()
        self.vertical = QVBoxLayout()
        self.inWidget = QWidget()
        self.ButtonGroup = QButtonGroup()

        self.layout = QGridLayout(self.inWidget)
        self.vertical.addWidget(self.inWidget)

        self.form = QGridLayout()

        self.pacman_position = None

        self.objectLabel = QLabel("Object:")
        self.objectLabel.setFixedSize(150, 50)
        self.form.addWidget(self.objectLabel, 0, 0)

        self.objectCombobox = QComboBox()
        self.objectCombobox.addItems(['Pacman', 'Food', 'Block'])
        self.objectCombobox.setFixedSize(150, 30)
        self.objectCombobox.setEnabled(False)
        self.objectCombobox.activated.connect(self.object_choosing)
        self.form.addWidget(self.objectCombobox, 0, 1)

        self.density = QLabel("Density:")
        self.objectLabel.setFixedSize(150, 50)
        self.form.addWidget(self.density, 0, 2)

        self.densityCombobox = QComboBox()
        self.densityCombobox.addItems(['4', '3', '2', '1'])
        self.densityCombobox.setFixedSize(150, 30)
        self.form.addWidget(self.densityCombobox, 0, 3)

        self.clearButton = QPushButton('Clear')
        self.clearButton.setFixedSize(80, 30)
        self.clearButton.clicked.connect(self.clear_button)
        self.form.addWidget(self.clearButton, 0, 4)

        self.algorithmLabel = QLabel('Algorithm:')
        self.algorithmLabel.setFixedSize(150, 30)
        self.form.addWidget(self.algorithmLabel, 1, 0)

        self.algorithmCombobox = QComboBox()
        self.algorithmCombobox.addItems(['DFS', 'BFS', 'A*', 'UCS', "IDS" , "BiDirectional"])
        self.algorithmCombobox.setFixedSize(150, 30)
        self.form.addWidget(self.algorithmCombobox, 1, 1)

        self.animationRateLabel = QLabel('Animation Rate:')
        self.animationRateLabel.setFixedSize(150, 30)
        self.form.addWidget(self.animationRateLabel, 1, 2)

        self.animationRateCombobox = QComboBox()
        self.animationRateCombobox.addItem('Without Animation')
        self.animationRateCombobox.setFixedSize(180, 30)
        self.form.addWidget(self.animationRateCombobox, 1, 3)

        self.undoButton = QPushButton('Undo')
        self.undoButton.setFixedSize(80, 30)
        self.form.addWidget(self.undoButton, 1, 4)

        self.handyStatusLabel = QLabel('Handy Status:')
        self.handyStatusLabel.setFixedSize(150, 30)
        self.form.addWidget(self.handyStatusLabel, 2, 0)

        self.handyStatusCombobox = QComboBox()
        self.handyStatusCombobox.addItems(['UnHandy', 'Handy'])
        self.handyStatusCombobox.setFixedSize(180, 30)
        self.handyStatusCombobox.activated.connect(self.click_change_color)
        self.form.addWidget(self.handyStatusCombobox, 2, 1)

        self.generateRandomPatternButton = QPushButton('Generate Random Pattern')
        self.generateRandomPatternButton.setFixedSize(180, 30)
        self.form.addWidget(self.generateRandomPatternButton, 2, 3)
        self.generateRandomPatternButton.clicked.connect(self.generate_random_pattern_button)

        self.searchButton  = QPushButton('Search')
        self.searchButton.setFixedSize(80, 30)
        self.searchButton.clicked.connect(self.search_button)
        self.form.addWidget(self.searchButton, 2, 4)

        self.timeOfExecutionLabel = QLabel('Time Of Execution:')
        self.timeOfExecutionLabel.setFixedSize(150, 30)
        self.form.addWidget(self.timeOfExecutionLabel, 3, 1)

        self.timeOfExecutionMessageBox = QPlainTextEdit()
        self.timeOfExecutionMessageBox.setFixedSize(200, 30)
        self.timeOfExecutionMessageBox.setEnabled(False)
        self.form.addWidget(self.timeOfExecutionMessageBox, 3, 2)

        self.openedNodeLabel = QLabel('Opened Node:')
        self.openedNodeLabel.setFixedSize(150, 30)
        self.form.addWidget(self.openedNodeLabel, 3, 3)

        self.openedNodeMessageBox = QPlainTextEdit()
        self.openedNodeMessageBox.setFixedSize(150, 30)
        self.openedNodeMessageBox.setEnabled(False)
        self.form.addWidget(self.openedNodeMessageBox, 3, 4)


        self.pacmanFlag = False


        self.CreateButtons()
        self.vertical.addLayout(self.form)
        Widget.setLayout(self.vertical)
        self.setCentralWidget(Widget)


    def CreateButtons(self):
        for row in range(self.row):
            for column in range(self.column):
                if (row == 0 or row == 19) or (column == 0 or column == 29):
                    button = PushButton('', style=self.Styles["Black"], row=row, column=column, color="black")
                    button.setObjectName(f"{row}-{column}")
                    button.setObjectName(f"{row}-{column}")
                    button.setProperty('is_food', False)
                    button.setProperty('is_block', False)
                    button.setProperty('is_pacman', False)
                    self.layout.addWidget(button, row + 1, column)
                else:
                    button = PushButton('', style=self.Styles["White"], row=row, column=column, color="white")
                    button.setObjectName(f"{row}-{column}")
                    self.Buttons[row][column] = button
                    button.setProperty('is_food', False)
                    button.setProperty('is_block', False)
                    button.setProperty('is_pacman', False)
                    button.setEnabled(False)
                    if row < 10:
                        self.dict_of_values_buttons.update({f"{row}-{column}": 1})
                    elif row >= 10:
                        self.dict_of_values_buttons.update({f"{row}-{column}": 2})
                    self.layout.addWidget(button, row+1, column)
                    self.ButtonGroup.addButton(button)
                    button.clicked.connect(self.object_choosing)


    def click_change_color(self, index):
        if index == 0:
            for button in self.ButtonGroup.buttons():
                button.setEnabled(False)
            self.objectCombobox.setEnabled(False)
        elif index == 1:
            for button in self.ButtonGroup.buttons():
                button.setEnabled(True)
            self.objectCombobox.setEnabled(True)


    def click_for_block(self):
        sender = self.sender()
        sender.setProperty('text', '')
        if sender.palette().color(sender.backgroundRole()) == QColor('white'):
            sender.setStyleSheet("background-color: black;"
                                "border :0.5px solid gray;")
            self.list_of_blocks.append(sender.objectName())
            sender.setProperty('is_block', True)


        elif sender.palette().color(sender.backgroundRole()) == QColor('black'):
            sender.setStyleSheet("background-color: white;"
                                "border :0.5px solid gray;")
            self.list_of_blocks.remove(sender.objectName())
            sender.setProperty('is_block', False)




    def clear_button(self):
        for button in self.ButtonGroup.buttons():
            button.setStyleSheet("background-color: white;"
                                 "border :0.5px solid gray;")
            button.setText('')
            button.setIcon(QIcon())
            button.setProperty('is_food', False)
            button.setProperty('is_block', False)
            button.setProperty('is_pacman', False)

        self.list_of_blocks = []
        self.list_of_foods = []
        self.pacman = []
        self.pacmanFlag = False

        self.timeOfExecutionMessageBox.setPlainText("")
        self.openedNodeMessageBox.setPlainText("")



    def object_choosing(self):
        if self.objectCombobox.currentIndex() == 0:     ### for pacman
            self.click_for_pacman()

        elif self.objectCombobox.currentIndex() == 1:    ### for food
            self.click_for_food()

        elif self.objectCombobox.currentIndex() == 2:  ### for object
            self.click_for_block()


    def click_for_food(self):
        sender = self.sender()
        if sender.property('is_food') == False:
            sender.setProperty('is_food', True)
            font = QFont('Arial', 20)
            sender.setProperty('text', '•')
            sender.setFont(font)
            sender.setStyleSheet("background-color: white;"
                                 "border :0.5px solid gray;"
                                 "color: orange")
            self.list_of_foods.append(sender.objectName())

        elif sender.property('is_food') == True:
            sender.setProperty('is_food', False)
            sender.setProperty('text', '')
            sender.setStyleSheet("background-color: white;"
                                 "border :0.5px solid gray;"
                                 "color: orange")
            self.list_of_foods.remove(sender.objectName())


    def click_for_pacman(self):
        sender = self.sender()
        pixmap = QPixmap('./images/pacman_icon.png')
        sender.setProperty('text', '')

        if not self.pacmanFlag:
            pixmap = pixmap.scaled(sender.size(), aspectRatioMode=Qt.KeepAspectRatio,
                                   transformMode=Qt.SmoothTransformation)
            icon = QIcon(pixmap)
            sender.setProperty('icon', icon)
            self.pacmanFlag = True
            self.pacman.append(sender.objectName())
        else:
            sender.setProperty('icon', QIcon())
            self.pacmanFlag = False
            self.pacman.remove(sender.objectName())



    def generate_random_pattern_button(self):
        self.clear_button()

        self.density = self.densityCombobox.currentIndex() + 1  #### generate random block
        block_number = int(random.randint(0, 504) / self.density)
        for i in range(0, block_number):
            block_button = self.findChild(PushButton, f"{random.randint(1, 18)}-{random.randint(1, 27)}")
            if block_button not in self.list_of_blocks and block_button.property('is_block') == False:
                block_button.setProperty('is_block', True)
                self.list_of_blocks.append(block_button.objectName())
                block_button.setStyleSheet("background-color: black;"
                                           "border :0.5px solid gray;"
                                           "color: orange")

        for i in range(0, random.randint(1, 504 - (len(self.list_of_blocks) + 1))):  #### generate random food
            food_button = self.findChild(PushButton, f"{random.randint(1, 18)}-{random.randint(1, 28)}")
            if food_button.property('is_block') == False and food_button.property('is_food') == False:
                food_button.setProperty('is_food', True)
                food_button.setProperty('text', '•')
                font = QFont('Arial', 20)
                food_button.setFont(font)
                food_button.setStyleSheet("background-color: white;"
                                          "border :0.5px solid gray;"
                                          "color: orange")
                self.list_of_foods.append(food_button.objectName())

        while self.pacmanFlag == False:
            pacman_button = self.findChild(PushButton,
                                           f"{random.randint(1, 18)}-{random.randint(1, 28)}")  #### generate random pacman
            self.pacman = [pacman_button.objectName()]
            if pacman_button.property('is_pacman') == False and pacman_button.property('is_food') == False and \
                    pacman_button.property('is_block') == False:
                pacman_button.setStyleSheet("background-color: white;"
                                            "border :0.5px solid gray;")
                pixmap = QPixmap('./images/pacman_icon.png')
                pacman_button.setProperty('is_pacman', True)
                pixmap = pixmap.scaled(pacman_button.size(), aspectRatioMode=Qt.KeepAspectRatio,
                                       transformMode=Qt.SmoothTransformation)
                icon = QIcon(pixmap)
                self.pacmanFlag = True
                pacman_button.setIcon(icon)
                for button in self.ButtonGroup.buttons():
                    button.setEnabled(True)







    def search_button(self):

        BarricadeList = []
        Pacman = []
        Food = []

        for item in self.list_of_blocks :
            temp = 0
            temp2 = 0
            for ele in range(len(item)):
                if(item[ele]=='-'):
                    temp = int(item[:ele])
                    temp2 = int(item[ele+1:])
            BarricadeList.append((temp,temp2))
        for item in self.list_of_foods :
            temp = 0
            temp2 = 0
            for ele in range(len(item)):
                if(item[ele]=='-'):
                    temp = int(item[:ele])
                    temp2 = int(item[ele+1:])
            Food.append((temp,temp2))
        for i in range(len(self.pacman[0])):
            if(self.pacman[0][i]=='-'):
                Pacman.append((int(self.pacman[0][0:i]) , int(self.pacman[0][i+1:])))

        a = Searchalgorithm(Pacman , Food , BarricadeList,self.dict_of_values_buttons)
        list_of_opened_nodes = []
        direction_list = []


        if self.algorithmCombobox.currentIndex() == 0:
            goldlist = a.DFS()

        elif self.algorithmCombobox.currentIndex() == 1:
            goldlist = a.BFS()

        elif self.algorithmCombobox.currentIndex() == 2:
            goldlist = a.AStar()

        elif self.algorithmCombobox.currentIndex() == 3:
            goldlist = a.UCS()

        elif self.algorithmCombobox.currentIndex() == 4:
            goldlist = a.IDSCaller(20)

        elif self.algorithmCombobox.currentIndex() == 5:
            goldlist = a.bi_directional()
            for x in goldlist[0]:
                direction_list.append(f"{x[0]}-{x[1]}")
            for x in goldlist[1]:
                list_of_opened_nodes.append(f"{x[0]}-{x[1]}")


            for opened in list_of_opened_nodes:
                button = self.findChild(PushButton, opened)
                button.setStyleSheet("background-color: yellow;"
                                    "border :0.5px solid gray;"
                                    "color: orange")
            for index, value in enumerate(direction_list):
                button = self.findChild(PushButton, value)
                button.setStyleSheet("background-color: green;"
                                    "border :0.5px solid gray;"
                                    "color: orange")


        if(self.algorithmCombobox.currentIndex() != 5):
            if goldlist[2]==False:
                for x in goldlist[0]:
                    direction_list.append(f"{x[0]}-{x[1]}")
                for x in goldlist[1]:
                    list_of_opened_nodes.append(f"{x[0]}-{x[1]}")


                for opened in list_of_opened_nodes:
                    button = self.findChild(PushButton, opened)
                    button.setStyleSheet("background-color: yellow;"
                                        "border :0.5px solid gray;"
                                        "color: orange")
                for index, value in enumerate(direction_list):
                    button = self.findChild(PushButton, value)
                    button.setStyleSheet("background-color: green;"
                                        "border :0.5px solid gray;"
                                        "color: orange")
                error_box = QMessageBox.critical(None, "Error", "Couldn't Find Path For All Food", QMessageBox.Ok)
                if error_box == QMessageBox.Ok:
                    self.clear_button()


            else:

                for x in goldlist[0]:
                    direction_list.append(f"{x[0]}-{x[1]}")
                for x in goldlist[1]:
                    list_of_opened_nodes.append(f"{x[0]}-{x[1]}")


                for opened in list_of_opened_nodes:
                    button = self.findChild(PushButton, opened)
                    button.setStyleSheet("background-color: yellow;"
                                        "border :0.5px solid gray;"
                                        "color: orange")

                for index, value in enumerate(direction_list):
                    button = self.findChild(PushButton, value)
                    button.setStyleSheet("background-color: green;"
                                        "border :0.5px solid gray;"
                                        "color: orange")

                    if(index != len(direction_list)-1 and index!=0 and len(self.list_of_foods)==1):
                        button.setText(str(index))



                self.timeOfExecutionMessageBox.setPlainText(str(goldlist[3]))
                font = QFont()
                font.setPointSize(9)
                self.timeOfExecutionMessageBox.setFont(font)


                self.openedNodeMessageBox.setPlainText(str(len(list(set(list_of_opened_nodes)))))
                font = QFont()
                font.setPointSize(9)
                self.openedNodeMessageBox.setFont(font)



app = QApplication(sys.argv)
w = MyWindow()
w.setWindowTitle('Searchs Algorithm')
w.show()
sys.exit(app.exec_())