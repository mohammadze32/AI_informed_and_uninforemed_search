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