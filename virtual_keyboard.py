import ctypes

# Use `winuser.h` to synthesizes keystrokes, mouse motions, and button clicks.

# Predefine C structures where are later used from `SendInput` function in `winuser.h`

# Definition of `tagKEYBDINPUT` structure,
# see: https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

# Definition of `tagHARDWAREINPUT` structure,
# see: https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-hardwareinput
class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

# Definition of `tagMOUSEINPUT` structure,
# see: https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mouseinput
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

# Definition of union which is reguired to define `tagINPUT` structure,
# see: https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input#members
class InputUnion(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

# Definition of `tagINPUT` structure,
# see: https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", InputUnion)]

class VirtualKeyboard():
    def __init__(self):
        super().__init__()
        # Flags for `tagKEYBDINPUT` structure,
        # definition see: https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput#members
        self.keyeventf_scancode = 0x0008
        self.keyeventf_keyup = 0x0002

        self.win_scan_codes = {'A': 0x1e,
                               'B': 0x30,
                               'C': 0x2e,
                               'D': 0x20,
                               'E': 0x12,
                               'F': 0x21,
                               'G': 0x22,
                               'H': 0x23,
                               'I': 0x17,
                               'J': 0x24,
                               'K': 0x25,
                               'L': 0x26,
                               'M': 0x32,
                               'N': 0x31,
                               'O': 0x18,
                               'P': 0x19,
                               'Q': 0x10,
                               'R': 0x13,
                               'S': 0x1f,
                               'T': 0x14,
                               'U': 0x16,
                               'V': 0x2f,
                               'W': 0x11,
                               'X': 0x2d,
                               'Y': 0x15,
                               'Z': 0x2c,
                               '0': 0xb, 
                               '1': 0x2, 
                               '2': 0x3, 
                               '3': 0x4, 
                               '4': 0x5, 
                               '5': 0x6, 
                               '6': 0x7, 
                               '7': 0x8, 
                               '8': 0x9, 
                               '9': 0xa, 
                               'GRAVE': 0x29,
                               'MINUS': 0xc, 
                               'EQUALS': 0xd,
                               'BACKSLASH': 0x2b,
                               'BACKSPACE': 0xe,
                               'SPACE': 0x39,
                               'TAB': 0xf,
                               'CAPITAL': 0x3a,
                               'LSHIFT': 0x2a,
                               'LCTRL': 0x1d,
                               'LALT': 0x38,
                               'RSHIFT': 0x36,
                               'RCTRL': 0x11d,
                               'RALT': 0x138,
                               'APPS': 0x15d,
                               'RETURN': 0x1c,
                               'ESCAPE': 0x1, 
                               'F1': 0x3b,
                               'F2': 0x3c,
                               'F3': 0x3d,
                               'F4': 0x3e,
                               'F5': 0x3f,
                               'F6': 0x40,
                               'F7': 0x41,
                               'F8': 0x42,
                               'F9': 0x43,
                               'F10': 0x44, 
                               'F11': 0x57, 
                               'F12': 0x58, 
                               'SCROLL': 0x46,
                               'LBRACKET': 0x1a,
                               'INSERT': 0x152,
                               'HOME': 0x147,
                               'PGUP': 0x149,
                               'DELETE': 0x153, 
                               'END': 0x14f, 
                               'PGDN': 0x151,
                               'UP': 0x148,
                               'LEFT': 0x14b, 
                               'DOWN': 0x150, 
                               'RIGHT': 0x14d,
                               'NUMLOCK': 0x45,
                               'DIVIDE': 0x135,
                               'MULTIPLY': 0x37,
                               'SUBTRACT': 0x0,
                               'ADD': 0x0, 
                               'DECIMAL': 0x53,
                               'NUMPAD0': 0x52,
                               'NUMPAD1': 0x4f,
                               'NUMPAD2': 0x50,
                               'NUMPAD3': 0x51,
                               'NUMPAD4': 0x4b,
                               'NUMPAD5': 0x4c,
                               'NUMPAD6': 0x4d,
                               'NUMPAD7': 0x47,
                               'NUMPAD8': 0x48,
                               'NUMPAD9': 0x49,
                               'RBRACKET': 0x1b, 
                               'SEMICOLON': 0x27,
                               'APOSTROPHE': 0x28,
                               'COMMA': 0x33,
                               'PERIOD': 0x34,
                               'SLASH': 0x35,
                               'MEDIA_NEXT_TRACK': 0x119,
                               'MEDIA_PREV_TRACK': 0x110,
                               'MEDIA_STOP': 0x124,
                               'MEDIA_PLAY_PAUSE': 0x122, 
                               'VOLUME_UP': 0x130, 
                               'VOLUME_DOWN': 0x12e,
                               'LAUNCH_MEDIA_SELECT': 0x16d,
                               'LAUNCH_MAIL': 0x16c,
                               'BROWSER_SEARCH': 0x165,
                               'BROWSER_HOME': 0x132,
                               'BROWSER_BACK': 0x16a,
                               'BROWSER_FORWARD': 0x169,
                               'BROWSER_STOP': 0x168,
                               'BROWSER_REFRESH': 0x167}
        
    def send_pressed_key_event(self, key_scan_code):
        """Function to send key event as pressed key.

        Args:
          key_scan_code: Hex key scan code
        """
        dw_extra_info = ctypes.c_ulong(0)
        key_bd_input_struct = KeyBdInput(0, key_scan_code,
                                         self.keyeventf_scancode , 0,
                                         ctypes.pointer(dw_extra_info))
        input_union = InputUnion()
        input_union.ki = key_bd_input_struct
        input_struct = Input(ctypes.c_ulong(1), input_union)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(input_struct), 
                                       ctypes.sizeof(input_struct))

    def send_released_key_event(self, key_scan_code):
        """Function to send key event as released key.

        Args:
          key_scan_code: Hex key scan code
        """
        dw_extra_info = ctypes.c_ulong(0)
        key_bd_input_struct = KeyBdInput(0, key_scan_code,
                                         self.keyeventf_scancode  | self.keyeventf_keyup,
                                         0, ctypes.pointer(dw_extra_info))
        input_union = InputUnion()
        input_union.ki = key_bd_input_struct
        input_struct = Input(ctypes.c_ulong(1), input_union)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(input_struct),
                                       ctypes.sizeof(input_struct))
        
    def press_release_key(self, keys):
        """Function to press and release keys.

        Args:
          keys: List of keys
        """
        for key in keys:
            try:
                self.send_pressed_key_event(self.win_scan_codes[key])
            except KeyError:
                print('Key ', key, ' was not defined')

        for key in keys:
            try:
                self.send_released_key_event(self.win_scan_codes[key])
            except KeyError:
                print('Key ', key, ' was not defined')
