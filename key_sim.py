from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton, QVBoxLayout, QDesktopWidget
from PyQt5.QtGui  import QPixmap, QIcon
from PyQt5.QtCore import QPoint, Qt
import sys
from multiprocessing import Process
import multiprocessing
import os
import socket
from key_event_editor import KeyEventEditor
from key_server import KeyServer
import logging
from logging.handlers import RotatingFileHandler
import traceback
import qrcode
from PIL.ImageQt import ImageQt
import sys

class StdLogger(object):
    """Standard stream (input, output and error) logger.
    
    Args:
      file_path: Path to log file

    Returns:
      StdLogger: Object class
    """

    def __init__(self, file_path):
        self.file_path = file_path
   
    def write(self, message):
        log = open(self.file_path, "a")
        log.write(message)
        log.close()

    def flush(self):
        # This flush method is needed for python 3 compatibility.
        pass

class KeySim(QMainWindow):
    """KeySim GUI class.

    Main GUI to start the web server and open the KeyEventEditor

    Returns:
      KeySim: Object class
    """
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.init_key_sim()
        self.logger.info('Application initialized')

    def init_key_sim(self):
        self.version = 'v0.1.0'
        self.port = 8080
        self.host = '0.0.0.0'

        self.server_process = None
        self.key_event_editor = None
        self.setWindowTitle('KeySim - Server')
        self.setWindowIcon(QIcon(os.path.normcase('./static/images/system_icons/favicon.ico')))
        center_point = QDesktopWidget().availableGeometry().center()
        window_size = QPoint(250,200)
        self.setGeometry(int((center_point.x() - window_size.x() * 0.5)),
                         int(center_point.y() - window_size.y() * 0.5),
                         window_size.x(),
                         window_size.y())

        self.main_layout = QVBoxLayout()

        self.icon_label = QLabel()
        self.icon_pixmap = QPixmap(os.path.normcase('./static/images/system_icons/keysim_icon_big.svg'))
        self.icon_label.setFixedWidth(128)
        self.icon_label.setFixedHeight(60)
        self.icon_label.setScaledContents(True)
        self.icon_label.setPixmap(self.icon_pixmap)
        self.main_layout.addWidget(self.icon_label,alignment=Qt.AlignCenter)

        self.version_label = QLabel()
        self.version_label.setText('KeySim ' + self.version)
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setMaximumHeight(20)
        self.main_layout.addWidget(self.version_label)

        self.server_status_label = QLabel()
        self.server_status_label.setText('Server Status: Offline')
        self.server_status_label.setStyleSheet('color: red')
        self.server_status_label.setAlignment(Qt.AlignCenter)
        self.server_status_label.setMaximumHeight(20)
        self.main_layout.addWidget(self.server_status_label)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip_address = sock.getsockname()[0]

        self.server_adress_label = QLabel()
        server_adress = ip_address + ":" + str(self.port)
        server_adress_link = "<a href=\"http://" \
                             + server_adress \
                             + "\">" \
                             + "http://"  \
                             + server_adress \
                             + "</a>"
        self.server_adress_label.setText("Server Address: " + server_adress_link)
        self.server_adress_label.setOpenExternalLinks(True)
        self.server_adress_label.setAlignment(Qt.AlignCenter)
        self.server_adress_label.setMaximumHeight(20)
        self.server_adress_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.main_layout.addWidget(self.server_adress_label)
        
        # Create QR image with the server address
        qr_image = qrcode.make("http://"+ip_address + ':'+str(self.port))
        qr_image = qr_image.convert("RGBA")
        qr_data = qr_image.load()
        width, height = qr_image.size
        for y in range(height):
            for x in range(width):
                if qr_data[x, y] == (255, 255, 255, 255):
                     qr_data[x, y] = (255, 255, 255, 0)
        image_qt_qr = ImageQt(qr_image)
        self.qr_label = QLabel()
        self.qr_pixmap = QPixmap.fromImage(image_qt_qr)
        self.qr_label.setFixedWidth(128)
        self.qr_label.setFixedHeight(128)
        self.qr_label.setScaledContents(True)
        self.qr_label.setPixmap(self.qr_pixmap)
        self.main_layout.addWidget(self.qr_label,alignment=Qt.AlignCenter)

        self.server_button = QPushButton()
        self.server_button.setText("Start Server")
        self.server_button.setFixedWidth(128)
        self.server_button.clicked.connect(self.start_server)

        self.keyevent_editor_button = QPushButton("Key Event Editor")
        self.keyevent_editor_button.setFixedWidth(128)
        self.keyevent_editor_button.clicked.connect(self.start_key_event_editor)

        self.main_layout.addWidget(self.server_button, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.keyevent_editor_button, alignment=Qt.AlignCenter)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.show()

    def start_server(self):
        """Function to start the KeyServer
        """
        try:
            # Run the KeyServer on a different process, otherwise the start 
            # function will stock here, because the server run in a loop until
            # a terminate signal.
            self.server_process = Process(target=KeyServer,
                                          args=(self.version, self.host, self.port))
            self.server_process.daemon = True
            self.server_process.start()
            self.server_status_label.setText('Server status: Online')
            self.server_status_label.setStyleSheet('color: green')
            self.server_button.setText("Stop Server")
            self.server_button.clicked.disconnect()
            self.server_button.clicked.connect(self.stop_server)
        except Exception as ex:
            self.logger.error("Server couldn't started: " + traceback.format_exc())

    def stop_server(self):
        """Function to stop the running KeyServer
        """
        self.server_process.terminate()
        self.server_process = None
        self.server_status_label.setText('Server Status: Offline')
        self.server_status_label.setStyleSheet('color: red')
        self.server_button.setText("Start Server")
        self.server_button.clicked.disconnect()
        self.server_button.clicked.connect(self.start_server)

    def start_key_event_editor(self):
        if self.key_event_editor != None:
            if not self.key_event_editor.isVisible():
                self.key_event_editor = KeyEventEditor()
        else:
            self.key_event_editor = KeyEventEditor()

    def closeEvent(self, event):
        if self.server_process != None:
            self.server_process.terminate()

def main():
    """Main function to open the KeySim GUI
    """
    # Configure logging
    if not os.path.exists(os.path.normcase("logs")):
        os.makedirs(os.path.normcase("logs"))

    stdout_file_path = os.path.normcase("logs/stdout.log")
    stderr_file_path = os.path.normcase("logs/stderr.log")
    app_log_file_path = os.path.normcase("logs/app.log")

    if os.path.exists(stdout_file_path):
        os.remove(stdout_file_path)
    if os.path.exists(stderr_file_path):
        os.remove(stderr_file_path)
    sys.stdout = StdLogger(stdout_file_path)
    sys.stderr = StdLogger(stderr_file_path)

    file_handler = RotatingFileHandler(filename=app_log_file_path,
                                       mode='a',
                                       encoding='utf-8',
                                       maxBytes=int(1e7),
                                       backupCount=2)
    logging.basicConfig(level=logging.DEBUG,
                        handlers = [file_handler])
    
    # Add freeze support for Windows executable
    multiprocessing.freeze_support()

    app = QApplication([])
    keysim = KeySim()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
