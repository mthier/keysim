from flask import Flask, render_template, request
import os
import logging
from logging.handlers import RotatingFileHandler

from key_data import KeyData
from virtual_keyboard import VirtualKeyboard

class KeyServer():
    """KeyServer class to host and handle a local webserver
    
    Args:
      version: Application version
      host: IP address of the host
      port: Port number

    Returns:
      KeyServer: Object class
    """
    def __init__(self, version, host='0.0.0.0', port=55555):
        super().__init__()
        self.init_key_server(version, host, port)
        

    def init_key_server(self, version, host, port):
        self.host = host
        self.port = port
        self.version = version
        self.web_app = Flask(__name__)
        self.key_event_data = None
        self.key_event_data_handler = KeyData(os.path.normcase('./key_events.json'))
        self.virtual_keyboard = VirtualKeyboard()

        @self.web_app.route('/')
        def _index_page():
            return self.index_page()

        @self.web_app.route('/getkeyeventlist', methods=['GET', 'POST'])
        def _get_key_events():
            return self.get_key_events()

        @self.web_app.route('/sendkeyevent', methods=['GET', 'POST'])
        def _send_key_event():
            return self.send_key_event()

        self.run_server()

    def run_server(self):
        self.web_app.run(host=self.host, port=self.port, debug=True, threaded=True, use_reloader=False)

    def index_page(self):
        #Creates welcome text
        html_welcome_txt = """<p><img src="/static/images/system_icons/keysim_icon_big.svg" style="width:200px;height:auto;"/></p>""" \
                         + "<p>KeySim (Client)</p>" \
                         + "<p>Version: " \
                         + self.version \
                         + "</p>" \
                         + "<p>Author: Michael Thiermann, 2024</p>"

        #Creates a string which contain a html code for
        #the key event list in a select field with the id="keyEventList"
        html_key_events_list = """<select id="keyEventList">""" \
                               + """<option value="0" style="display:none">Select Event List</option>"""
        for list in  self.key_event_data_handler.get_list_names():
            html_key_events_list = html_key_events_list \
                                   + """<option  value=""" \
                                   + '"'  + str(list) + '"'\
                                   + """ >""" \
                                   + str(list) \
                                   + """</option>"""
        html_key_events_list = html_key_events_list + "</select>"

        return render_template('index.html', keyEventList=html_key_events_list, welcomeTxt=html_welcome_txt)

    def get_key_events(self):
        #get the the requested key event list
        key_event_list_name = request.json
        #get the ip adress from the user request
        user_ip = request.environ['REMOTE_ADDR']
        html_button_str = ""

        self.web_app.logger.info("The user: " + user_ip + " requested the list: " + key_event_list_name)

        if key_event_list_name != "0":
            #Creates a string which contain a html code for
            #the key events as buttons with the id="keyEventButton". The value of a button are the key event!
            #sorted() sort key numbers to place the buttons in desired order
            key_event_names = self.key_event_data_handler.get_key_event_names()
            for key_event in self.key_event_data_handler.get_key_events_by_name(key_event_list_name):
                key_event_icon = key_event[key_event_names[2]]
                key_event_command = key_event[key_event_names[1]]
                key_event_name = key_event[key_event_names[0]]
                if key_event_icon != "":
                    html_button_str = html_button_str \
                                      + """<button type="submit" id="keyEventButton" value=""" \
                                      + key_event_command \
                                      + """><img src=""" \
                                      + "/static/images/event_icons/" \
                                      + key_event_icon \
                                      + """ height="35"/><br>""" \
                                      + key_event_name \
                                      + "</button>"""
                else:
                    html_button_str = html_button_str \
                                    + """<button type="submit" id="keyEventButton" value=""" \
                                    + key_event_command \
                                    + """>""" \
                                    +  key_event_name \
                                    + "</button>"""
        else:
            html_button_str = ""

        return html_button_str

    def send_key_event(self):
        post_key_event = request.json #get the the post key event value
        user_ip = request.environ['REMOTE_ADDR'] #get the ip adress from the user request
        key_events = post_key_event.split(",") #split multiple key events in single key events
        self.virtual_keyboard.press_release_key(key_events)
        self.web_app.logger.info("The user: " + user_ip + " pressed " + str(key_events))
        return post_key_event

if __name__ == '__main__':
    pass
