#!/usr/bin/env python3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout
from PyQt5.QtGui  import QIcon
import os

class KeyListener(QDialog):
    """KeyListener GUI class.

    Main GUI to listen on pressed keys on the keyboard

    Returns:
      KeyListener: Object class
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("KeyListener")
        self.setWindowIcon(QIcon(os.path.normcase('./static/images/system_icons/favicon.ico')))
        self.resize(300,100)
        self.main_layout = QVBoxLayout()
        self.info_text_label = QLabel("Press your desired keys...")
        self.info_text_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.info_text_label)
        self.setLayout(self.main_layout)
        self.show()
        self.setFocusPolicy(Qt.StrongFocus)
        self.pressed_key_codes = list()
        self.pressed_key_names = list()
        self.key_events = [{'win_native_scan_code': '0x1e', 'win_directx_key_name': 'A'},
                           {'win_native_scan_code': '0x30', 'win_directx_key_name': 'B'},
                           {'win_native_scan_code': '0x2e', 'win_directx_key_name': 'C'},
                           {'win_native_scan_code': '0x20', 'win_directx_key_name': 'D'},
                           {'win_native_scan_code': '0x12', 'win_directx_key_name': 'E'},
                           {'win_native_scan_code': '0x21', 'win_directx_key_name': 'F'},
                           {'win_native_scan_code': '0x22', 'win_directx_key_name': 'G'},
                           {'win_native_scan_code': '0x23', 'win_directx_key_name': 'H'},
                           {'win_native_scan_code': '0x17', 'win_directx_key_name': 'I'},
                           {'win_native_scan_code': '0x24', 'win_directx_key_name': 'J'},
                           {'win_native_scan_code': '0x25', 'win_directx_key_name': 'K'},
                           {'win_native_scan_code': '0x26', 'win_directx_key_name': 'L'},
                           {'win_native_scan_code': '0x32', 'win_directx_key_name': 'M'},
                           {'win_native_scan_code': '0x31', 'win_directx_key_name': 'N'},
                           {'win_native_scan_code': '0x18', 'win_directx_key_name': 'O'},
                           {'win_native_scan_code': '0x19', 'win_directx_key_name': 'P'},
                           {'win_native_scan_code': '0x10', 'win_directx_key_name': 'Q'},
                           {'win_native_scan_code': '0x13', 'win_directx_key_name': 'R'},
                           {'win_native_scan_code': '0x1f', 'win_directx_key_name': 'S'},
                           {'win_native_scan_code': '0x14', 'win_directx_key_name': 'T'},
                           {'win_native_scan_code': '0x16', 'win_directx_key_name': 'U'},
                           {'win_native_scan_code': '0x2f', 'win_directx_key_name': 'V'},
                           {'win_native_scan_code': '0x11', 'win_directx_key_name': 'W'},
                           {'win_native_scan_code': '0x2d', 'win_directx_key_name': 'X'},
                           {'win_native_scan_code': '0x15', 'win_directx_key_name': 'Y'},
                           {'win_native_scan_code': '0x2c', 'win_directx_key_name': 'Z'},
                           {'win_native_scan_code': '0xb', 'win_directx_key_name': '0'},
                           {'win_native_scan_code': '0x2', 'win_directx_key_name': '1'},
                           {'win_native_scan_code': '0x3', 'win_directx_key_name': '2'},
                           {'win_native_scan_code': '0x4', 'win_directx_key_name': '3'},
                           {'win_native_scan_code': '0x5', 'win_directx_key_name': '4'},
                           {'win_native_scan_code': '0x6', 'win_directx_key_name': '5'},
                           {'win_native_scan_code': '0x7', 'win_directx_key_name': '6'},
                           {'win_native_scan_code': '0x8', 'win_directx_key_name': '7'},
                           {'win_native_scan_code': '0x9', 'win_directx_key_name': '8'},
                           {'win_native_scan_code': '0xa', 'win_directx_key_name': '9'},
                           {'win_native_scan_code': '0x29', 'win_directx_key_name': 'GRAVE'},
                           {'win_native_scan_code': '0xc', 'win_directx_key_name': 'MINUS'},
                           {'win_native_scan_code': '0xd', 'win_directx_key_name': 'EQUALS'},
                           {'win_native_scan_code': '0x2b', 'win_directx_key_name': 'BACKSLASH'},
                           {'win_native_scan_code': '0xe', 'win_directx_key_name': 'BACKSPACE'},
                           {'win_native_scan_code': '0x39', 'win_directx_key_name': 'SPACE'},
                           {'win_native_scan_code': '0xf', 'win_directx_key_name': 'TAB'},
                           {'win_native_scan_code': '0x3a', 'win_directx_key_name': 'CAPITAL'},
                           {'win_native_scan_code': '0x2a', 'win_directx_key_name': 'LSHIFT'},
                           {'win_native_scan_code': '0x1d', 'win_directx_key_name': 'LCTRL'},
                           {'win_native_scan_code': '0x15b', 'win_directx_key_name': ''},
                           {'win_native_scan_code': '0x38', 'win_directx_key_name': 'LALT'},
                           {'win_native_scan_code': '0x36', 'win_directx_key_name': 'RSHIFT'},
                           {'win_native_scan_code': '0x11d', 'win_directx_key_name': 'RCTRL'},
                           {'win_native_scan_code': '0x15c', 'win_directx_key_name': ''},
                           {'win_native_scan_code': '0x138', 'win_directx_key_name': 'RALT'},
                           {'win_native_scan_code': '0x15d', 'win_directx_key_name': 'APPS'},
                           {'win_native_scan_code': '0x1c', 'win_directx_key_name': 'RETURN'},
                           {'win_native_scan_code': '0x1', 'win_directx_key_name': 'ESCAPE'},
                           {'win_native_scan_code': '0x3b', 'win_directx_key_name': 'F1'},
                           {'win_native_scan_code': '0x3c', 'win_directx_key_name': 'F2'},
                           {'win_native_scan_code': '0x3d', 'win_directx_key_name': 'F3'},
                           {'win_native_scan_code': '0x3e', 'win_directx_key_name': 'F4'},
                           {'win_native_scan_code': '0x3f', 'win_directx_key_name': 'F5'},
                           {'win_native_scan_code': '0x40', 'win_directx_key_name': 'F6'},
                           {'win_native_scan_code': '0x41', 'win_directx_key_name': 'F7'},
                           {'win_native_scan_code': '0x42', 'win_directx_key_name': 'F8'},
                           {'win_native_scan_code': '0x43', 'win_directx_key_name': 'F9'},
                           {'win_native_scan_code': '0x44', 'win_directx_key_name': 'F10'},
                           {'win_native_scan_code': '0x57', 'win_directx_key_name': 'F11'},
                           {'win_native_scan_code': '0x58', 'win_directx_key_name': 'F12'},
                           {'win_native_scan_code': '0x0', 'win_directx_key_name': ''},
                           {'win_native_scan_code': '0x46', 'win_directx_key_name': 'SCROLL'},
                           {'win_native_scan_code': '0x0', 'win_directx_key_name': ''},
                           {'win_native_scan_code': '0x1a', 'win_directx_key_name': 'LBRACKET'},
                           {'win_native_scan_code': '0x152', 'win_directx_key_name': 'INSERT'},
                           {'win_native_scan_code': '0x147', 'win_directx_key_name': 'HOME'},
                           {'win_native_scan_code': '0x149', 'win_directx_key_name': 'PGUP'},
                           {'win_native_scan_code': '0x153', 'win_directx_key_name': 'DELETE'},
                           {'win_native_scan_code': '0x14f', 'win_directx_key_name': 'END'},
                           {'win_native_scan_code': '0x151', 'win_directx_key_name': 'PGDN'},
                           {'win_native_scan_code': '0x148', 'win_directx_key_name': 'UP'},
                           {'win_native_scan_code': '0x14b', 'win_directx_key_name': 'LEFT'},
                           {'win_native_scan_code': '0x150', 'win_directx_key_name': 'DOWN'},
                           {'win_native_scan_code': '0x14d', 'win_directx_key_name': 'RIGHT'},
                           {'win_native_scan_code': '0x45', 'win_directx_key_name': 'NUMLOCK'},
                           {'win_native_scan_code': '0x135', 'win_directx_key_name': 'DIVIDE'},
                           {'win_native_scan_code': '0x37', 'win_directx_key_name': 'MULTIPLY'},
                           {'win_native_scan_code': '0x0', 'win_directx_key_name': 'SUBTRACT'},
                           {'win_native_scan_code': '0x0', 'win_directx_key_name': 'ADD'},
                           {'win_native_scan_code': '0x11c', 'win_directx_key_name': ''},
                           {'win_native_scan_code': '0x53', 'win_directx_key_name': 'DECIMAL'},
                           {'win_native_scan_code': '0x52', 'win_directx_key_name': 'NUMPAD0'},
                           {'win_native_scan_code': '0x4f', 'win_directx_key_name': 'NUMPAD1'},
                           {'win_native_scan_code': '0x50', 'win_directx_key_name': 'NUMPAD2'},
                           {'win_native_scan_code': '0x51', 'win_directx_key_name': 'NUMPAD3'},
                           {'win_native_scan_code': '0x4b', 'win_directx_key_name': 'NUMPAD4'},
                           {'win_native_scan_code': '0x4c', 'win_directx_key_name': 'NUMPAD5'},
                           {'win_native_scan_code': '0x4d', 'win_directx_key_name': 'NUMPAD6'},
                           {'win_native_scan_code': '0x47', 'win_directx_key_name': 'NUMPAD7'},
                           {'win_native_scan_code': '0x48', 'win_directx_key_name': 'NUMPAD8'},
                           {'win_native_scan_code': '0x49', 'win_directx_key_name': 'NUMPAD9'},
                           {'win_native_scan_code': '0x1b', 'win_directx_key_name': 'RBRACKET'},
                           {'win_native_scan_code': '0x27', 'win_directx_key_name': 'SEMICOLON'},
                           {'win_native_scan_code': '0x28', 'win_directx_key_name': 'APOSTROPHE'},
                           {'win_native_scan_code': '0x33', 'win_directx_key_name': 'COMMA'},
                           {'win_native_scan_code': '0x34', 'win_directx_key_name': 'PERIOD'},
                           {'win_native_scan_code': '0x35', 'win_directx_key_name': 'SLASH'},
                           {'win_native_scan_code': '0x119', 'win_directx_key_name': 'MEDIA_NEXT_TRACK'},
                           {'win_native_scan_code': '0x110', 'win_directx_key_name': 'MEDIA_PREV_TRACK'},
                           {'win_native_scan_code': '0x124', 'win_directx_key_name': 'MEDIA_STOP'},
                           {'win_native_scan_code': '0x122', 'win_directx_key_name': 'MEDIA_PLAY_PAUSE'},
                           {'win_native_scan_code': '0x120', 'win_directx_key_name': ''},
                           {'win_native_scan_code': '0x130', 'win_directx_key_name': 'VOLUME_UP'},
                           {'win_native_scan_code': '0x12e', 'win_directx_key_name': 'VOLUME_DOWN'},
                           {'win_native_scan_code': '0x16d', 'win_directx_key_name': 'LAUNCH_MEDIA_SELECT'},
                           {'win_native_scan_code': '0x16c', 'win_directx_key_name': 'LAUNCH_MAIL '},
                           {'win_native_scan_code': '0x121', 'win_directx_key_name': ''},
                           {'win_native_scan_code': '0x16b', 'win_directx_key_name': ''},
                           {'win_native_scan_code': '0x165', 'win_directx_key_name': 'BROWSER_SEARCH'},
                           {'win_native_scan_code': '0x132', 'win_directx_key_name': 'BROWSER_HOME'},
                           {'win_native_scan_code': '0x16a', 'win_directx_key_name': 'BROWSER_BACK'},
                           {'win_native_scan_code': '0x169', 'win_directx_key_name': 'BROWSER_FORWARD'},
                           {'win_native_scan_code': '0x168', 'win_directx_key_name': 'BROWSER_STOP'},
                           {'win_native_scan_code': '0x167', 'win_directx_key_name': 'BROWSER_REFRESH'}]

    def keyPressEvent(self, event):
        self.pressed_key_codes.append(event.nativeScanCode())

    def keyReleaseEvent(self, event):
        key_names = self.search_key_event(self.pressed_key_codes)
        if(len(key_names)==len(self.pressed_key_codes)):
            self.pressed_key_names = key_names
            self.accept()
            self.close()
        else:
            self.pressed_key_codes = list()
            self.info_text_label.setText('Pressed keys are not allowed, try again!')

    def search_key_event(self, key_codes):
        key_comands = []
        for key_code in key_codes:
            for key_event in self.key_events:
                if key_event['win_native_scan_code'] == hex(key_code):
                    key_comands.append(key_event['win_directx_key_name'])
        return key_comands

    def exec_(self):
        super().exec_()
        return self.pressed_key_names

if __name__ == '__main__':
    pass
