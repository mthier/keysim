#!/usr/bin/env python3

from PyQt5.QtCore import QPoint, Qt, QSize
from PyQt5.QtGui  import QStandardItemModel, QStandardItem, QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QGroupBox, QComboBox, QMainWindow,QPushButton, QAbstractItemView, QVBoxLayout, QInputDialog, QMessageBox, QDesktopWidget, QLineEdit, QFileDialog, QFormLayout, QListView, QHBoxLayout, QFrame, QMenu
import os
from key_data import KeyData
from key_listener import KeyListener
import logging

class KeyEventEditor(QMainWindow):
    """KeyEventEditor GUI class.

    Main GUI to create and manage key event list

    Returns:
      KeyEventEditor: Object class
    """
    def __init__(self):
        super(KeyEventEditor, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.init_key_event_editor()
        self.logger.info('KeyEventEditor initialized')

    def init_key_event_editor(self):
        self.key_event_data = None
        self.key_event_data_handler = KeyData(os.path.normcase('./key_events.json'))

        self.setWindowTitle('KeyEventEditor')
        self.setWindowIcon(QIcon(os.path.normcase('./static/images/system_icons/favicon.ico')))
        center_point = QDesktopWidget().availableGeometry().center()
        window_size = QPoint(640,480)
        self.setGeometry(int((center_point.x() - window_size.x() * 0.5)),
                         int(center_point.y() - window_size.y() * 0.5),
                         window_size.x(),
                         window_size.y())

        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.event_list_edit_group_box = QGroupBox("Event Lists")
        self.event_view_group_box = QGroupBox("Edit Event")
        self.event_view_edit_group_box = QFrame()

        self.left_layout.addWidget(self.event_list_edit_group_box)
        self.right_layout.addWidget(self.event_view_group_box)
        self.right_layout.addWidget(self.event_view_edit_group_box)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.event_list_edit_layout = QGridLayout()
        self.event_list_edit_group_box.setMaximumHeight(150);
        self.event_list_edit_group_box.setMaximumWidth(300)
        self.event_list_edit_group_box.setLayout(self.event_list_edit_layout)

        self.event_list_combo_box = QComboBox()
        self.event_list_combo_box.addItems(self.key_event_data_handler.get_list_names())
        self.event_list_combo_box.currentIndexChanged.connect(self.onChangedList)

        self.event_list_add_button = QPushButton('New Event List')
        self.event_list_add_button.clicked.connect(self.create_new_event_list)

        self.event_list_del_button = QPushButton('Delete Event List')
        self.event_list_del_button.clicked.connect(self.remove_event_list)

        self.event_list_rename_button = QPushButton('Rename Event List')
        self.event_list_rename_button.clicked.connect(self.rename_event_list)

        self.event_list_edit_layout.addWidget(self.event_list_combo_box,1,1,1,2)
        self.event_list_edit_layout.addWidget(self.event_list_add_button,2,1)
        self.event_list_edit_layout.addWidget(self.event_list_del_button,2,2)
        self.event_list_edit_layout.addWidget(self.event_list_rename_button,3,1)

        self.event_list_view = QListView()
        self.event_list_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.event_list_view.setModel(self.get_key_events(self.key_event_data_handler.get_key_events_by_idx(0)))
        self.event_list_view.clicked.connect(self.viewItem)
        self.event_list_view.setMaximumWidth(300)
        self.event_list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.event_list_view.customContextMenuRequested.connect(self.context_menu_delete_event)

        self.left_layout.addWidget(self.event_list_view)

        self.event_view_layout = QFormLayout()
        self.event_view_group_box.setLayout(self.event_view_layout)

        self.event_name_label = QLabel()
        self.event_name_label.setText('Name:')
        self.event_name_edit = QLineEdit()

        self.event_command_label = QLabel()
        self.event_command_label.setText('Keys:')
        self.event_command_edit = QLineEdit()

        self.event_icon_button = QPushButton('Select Icon')
        self.event_icon_button.setMaximumHeight(32)
        self.event_icon_button.clicked.connect(self.set_key_event_icon)
        self.event_icon_label = QLabel()
        self.event_icon_label.setStyleSheet("border: 1px solid grey; padding :2px")
        self.event_icon_label.setMaximumWidth(32)
        self.event_icon_label.setMaximumHeight(32)
        self.event_icon_label.setMinimumWidth(32)
        self.event_icon_label.setMinimumHeight(32)
        self.event_icon_label.setScaledContents(True)
        self.event_icon_path = ""
        self.event_icon_label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.event_icon_label.customContextMenuRequested.connect(self.context_menu_delete_icon_path)

        self.event_save_button = QPushButton('Save Event')
        self.event_save_button.setMaximumWidth(100)
        self.event_save_button.clicked.connect(self.save_edit_event)

        self.event_add_button = QPushButton('New Event')
        self.event_add_button.setMaximumWidth(100)
        self.event_add_button.clicked.connect(self.add_new_event)

        self.event_delete_button = QPushButton('Delete Event')
        self.event_delete_button.setMaximumWidth(100)
        self.event_delete_button.clicked.connect(self.remove_event)

        self.event_command_frame = QFrame()
        self.event_command_layout = QHBoxLayout()
        self.event_command_layout.setContentsMargins(0,0,0,0)

        self.event_command_scan_button = QPushButton('')
        self.event_command_scan_button.setMaximumWidth(30)
        self.event_command_scan_button.clicked.connect(self.start_key_listener)
        self.event_command_scan_button.setIcon(QIcon(os.path.normcase('./static/images/system_icons/search_icon.svg')))
        self.event_command_scan_button.setIconSize(QSize(20,20))

        self.event_command_layout.addWidget(self.event_command_edit)
        self.event_command_layout.addWidget(self.event_command_scan_button)

        self.event_command_frame.setLayout(self.event_command_layout)

        self.event_view_layout.addRow(self.event_name_label, self.event_name_edit)
        self.event_view_layout.addRow(self.event_command_label, self.event_command_frame)
        self.event_view_layout.addRow(self.event_icon_button, self.event_icon_label)

        self.event_view_edit_layout = QHBoxLayout()
        self.event_view_edit_layout.addStretch()
        self.event_view_edit_layout.addWidget(self.event_delete_button)
        self.event_view_edit_layout.addWidget(self.event_add_button)
        self.event_view_edit_layout.addWidget(self.event_save_button)
        self.event_view_edit_layout.setContentsMargins(0,0,0,0)
        self.event_view_edit_group_box.setLayout(self.event_view_edit_layout)
        self.event_view_edit_group_box.setMaximumHeight(50)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)
        
        self.onChangedList(0)
        self.show()

    def start_key_listener(self):
        """Function to start the KeyListener.
        """
        key_listener = KeyListener(self)
        key_names = key_listener.exec_()
        if key_names:
            self.event_command_edit.setText(','.join(str(x) for x in key_names))
 
    def context_menu_delete_event(self, position):
        """Function to delete key event from list view.

        Args:
          position: Widget coordinate
        """
        menu = QMenu()
        delete_action = menu.addAction("Delete Event")
        action = menu.exec_(self.event_list_view.mapToGlobal(position))
        if action == delete_action:
            self.remove_event()

    def context_menu_delete_icon_path(self, position):
        """Function to delete key event icon path.

        Args:
          position: Widget coordinate
        """
        menu = QMenu()
        delete_action = menu.addAction("Delete Icon")
        action = menu.exec_(self.event_icon_label.mapToGlobal(position))
        if action == delete_action:
            self.event_icon_path = ""
            icon_pixmap = QPixmap("")
            self.event_icon_label.setPixmap(icon_pixmap)

    def add_new_event(self):
        """Function to add new key event to key event list.
        """
        # Get name of the current selected key event list
        current_list = self.event_list_combo_box.currentText()
        # Add empty key event to key event list 
        self.key_event_data_handler.add_key_event(current_list)
        # Display all key events to list view 
        self.event_list_view.setModel(self.get_key_events(self.key_event_data_handler.get_key_events_by_name(current_list)))
        # Get number of entries of the key event list
        n_last_row = self.event_list_view.model().rowCount()-1
        # Get index object of the last key event 
        index = self.event_list_view.model().index(n_last_row,0)
        # Display the new empty key event 
        self.viewItem(index)
        # Select the new empty key event in the list
        self.event_list_view.setCurrentIndex(index)

    def remove_event(self):
        """Function to remove key event from key event list.
        """
        # Get name of the current selected key event list
        current_list = self.event_list_combo_box.currentText()
        # Get index of the selected key event in the key event list
        key_event_index = self.event_list_view.currentIndex().row()
        # Remove key event from key event list
        self.key_event_data_handler.delete_key_event(current_list, key_event_index)
        # Display all key events to list view 
        self.event_list_view.setModel(self.get_key_events(self.key_event_data_handler.get_key_events_by_name(current_list)))
        # Get number of entries of the key event list
        n_last_row = self.event_list_view.model().rowCount()-1
        # Get index object of the last key event 
        index = self.event_list_view.model().index(n_last_row,0)
        # Display the new empty key event 
        self.viewItem(index)
        # Select the new empty key event in the list
        self.event_list_view.setCurrentIndex(index)

    def create_new_event_list(self):
        """Function to add new key event list.
        """
        # Get new event list name from user input dialog
        list_name, ok = QInputDialog.getText(self, 'Add New Event List', 'Event list name:')
        if ok:
            if list_name == "":
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Error!")
                dlg.setIcon(QMessageBox.Critical)
                dlg.setText("List name can't be empty!")
                dlg.exec()
            else:
                # Add new event list name
                self.key_event_data_handler.add_key_event_list(list_name)
                self.update_event_list_combo_box()

    def remove_event_list(self):
        """Function to remove key event list.
        """
        # Get name of the current selected key event list
        current_list = self.event_list_combo_box.currentText()
        # Get user confirmation to remove key event list
        do_remove_list = QMessageBox.question(self, "Remove Event List", 
                                                    """Do you really remove "{}"?""".format(current_list),
                                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if do_remove_list == QMessageBox.Yes:
            # Remove key event list
            self.key_event_data_handler.remove_key_event_list(current_list)
            self.update_event_list_combo_box()

    def rename_event_list(self):
        """Function to rename key event list.
        """
        # Get name of the current selected key event list
        current_list = self.event_list_combo_box.currentText()
        # Get new event list name from user input dialog
        list_name, ok = QInputDialog.getText(self,
                                             'Rename Event List',
                                             'Event list name:',
                                             QLineEdit.Normal,
                                             current_list)
        if ok:
            if list_name == "":
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Error!")
                dlg.setIcon(QMessageBox.Critical)
                dlg.setText("List name can't be empty!")
                dlg.exec()
            else:
                # Rename event list name
                self.key_event_data_handler.rename_key_event_list(current_list,list_name)
                self.update_event_list_combo_box()


    def update_event_list_combo_box(self):
        """Function to update event list combo box.
        """
        self.event_list_combo_box.blockSignals(True)
        self.event_list_combo_box.clear()
        self.event_list_combo_box.blockSignals(False)
        self.event_list_combo_box.addItems(self.key_event_data_handler.get_list_names())
        self.event_list_combo_box.setCurrentIndex(self.event_list_combo_box.count()-1)

    def onChangedList(self, index):
        """Function to update GUI if key event list has changed.

        Args:
          index: Index of selected key event list of the combo box
        """
        self.event_list_view.setModel(self.get_key_events(self.key_event_data_handler.get_key_events_by_idx(index)))
        index = self.event_list_view.model().index(0,0)
        self.viewItem(index)
        self.event_list_view.setCurrentIndex(index)

    def get_key_events(self, key_events):
        """Function to fill the list view with key events.

        Args:
          key_events: List of key events

        Returns:
          item_model: QStandardItemModel with key events
        """
        item_model = QStandardItemModel()
        key_event_names = self.key_event_data_handler.get_key_event_names()
        for key_event in key_events:
            item_model.appendRow(QStandardItem(key_event[key_event_names[0]]))
        return item_model

    def set_key_event_icon(self):
        """Function to set key event icon.
        """
        # Get icon path from user input dialog
        icon_path = QFileDialog.getOpenFileName(self, 'Open file',
                                                os.path.normcase('./static/images/event_icons'),
                                                'Image files (*.png *.svg)')
        if icon_path[0] != "":
            self.event_icon_path = os.path.basename(icon_path[0])
            icon_pixmap = QPixmap(os.path.join('./static/images/event_icons/',
                                               self.event_icon_path))
            self.event_icon_label.setPixmap(icon_pixmap)

    def save_edit_event(self):
        """Function to save current selected key event.
        """
        # Get name of the current selected key event list
        current_list = self.event_list_combo_box.currentText()
        # Get index of the selected key event in the key event list
        key_event_index = self.event_list_view.currentIndex().row()
        if key_event_index != -1:
            # Get key event content from GUI elements
            name = self.event_name_edit.text()
            command = self.event_command_edit.text()
            icon = self.event_icon_path
            self.key_event_data_handler.update_key_event(current_list,key_event_index,name,command,icon)
            self.event_list_view.setModel(self.get_key_events(self.key_event_data_handler.get_key_events_by_name(current_list)))
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error!")
            dlg.setIcon(QMessageBox.Critical)
            dlg.setText("Could not save key event. No item is selected!")
            dlg.exec()

    def viewItem(self, selected_item):
        """Function to update GUI with key event content if entry of the 
        key event list has changes.

        Args:
          selected_item: Model index object of selected list view entry 
        """
        # Get name of the current selected key event list
        current_list = self.event_list_combo_box.currentText()
        # Get index of the selected key event in the key event list
        key_event_index = selected_item.row()
        # Get list of key events
        key_events = self.key_event_data_handler.get_key_events_by_name(current_list)
        # Get list of key event names
        key_event_names = self.key_event_data_handler.get_key_event_names()

        # Set key event content to GUI elements
        self.event_name_edit.setText(key_events[key_event_index][key_event_names[0]])
        self.event_command_edit.setText(key_events[key_event_index][key_event_names[1]])
        icon_pixmap = QPixmap(os.path.join('./static/images/event_icons/',
                                           key_events[key_event_index][key_event_names[2]]))
        self.event_icon_label.setPixmap(icon_pixmap)
        self.event_icon_path = key_events[key_event_index][key_event_names[2]]

if __name__ == '__main__':
    pass
