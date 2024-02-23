#!/usr/bin/env python3

import json # Module to handle json
from collections import OrderedDict # Module to parse JSON into ordered data-structure

class KeyData():
    """KeyData class.

    Class to handle and manage key event data

    Returns:
      KeyData: Object class
    """
    def __init__(self, data_path):
        self.init_key_data(data_path)

    def init_key_data(self, data_path):
        self.data_path = data_path
        self.key_event_data = dict()
        self.list_names = ["Default"]
        self.key_event_names = ["Name", "Command", "Icon"]
        self.read_json()

    def read_json(self):
        """Function to read key event data from JSON file.
        """
        try:
            with open(self.data_path, encoding='UTF-8') as file:
                self.key_event_data = json.load(file,object_pairs_hook=OrderedDict)
                self.list_names = list(self.key_event_data.keys())
        except Exception as e:
            print("Key event data couldn't be loaded!")
            print(str(e))

    def write_json(self):
        """Function to write key event data to JSON file.
        """
        try:
            with open(self.data_path, "w") as outfile:
                outfile.write(json.dumps(self.key_event_data, indent=4))
        except Exception as e:
            print("Key event data couldn't be wrote to file!")
            print(str(e))

    def get_n_key_events(self, list_name):
        """Function to get number of key events in specific key event list.

        Args:
         list_name: Name of the key event list

        Returns:
          n_key_events: Number of key events
        """
        return len(self.key_event_data[list_name].keys())

    def get_key_events_by_name(self, list_name):
        """Function to get key event data for specific key event list.

        Args:
         list_name: Name of the key event list

        Returns:
          key_events: Dictionary with key event data
        """
        return self.key_event_data[list_name]

    def get_key_events_by_idx(self, index):
        """Function to get key event data for specific key event list.

        Args:
         index: Index of the key event list

        Returns:
          key_events: Dictionary with key event data
        """
        return self.key_event_data[self.list_names[index]]

    def get_n_key_event_list(self):
        """Function to get number of key events in specific key event list.

        Returns:
          n_key_events_list: Number of key event lists
        """
        return len(self.list_names)

    def get_list_names(self):
        """Function to get names of key event lists.

        Returns:
          list_names: List of key event list names
        """
        return self.list_names

    def get_key_event_names(self):
        """Function to get names of key events.

        Returns:
          key_event_names: List of key event names
        """
        return self.key_event_names

    def update_key_event(self, list_name, key_event_idx, name, command, icon):
        """Function to update key event and write to JSON file.

        Args:
          list_name: Name of key event list
          key_event_idx: Index of key event entry
          name: Title of key event
          command: Keys of key event
          icon: Icon path for key event 
        """
        self.key_event_data[list_name][key_event_idx][self.key_event_names[0]] = name
        self.key_event_data[list_name][key_event_idx][self.key_event_names[1]] = command
        self.key_event_data[list_name][key_event_idx][self.key_event_names[2]] = icon
        self.write_json()

    def add_key_event(self, list_name):
        """Function to add empty key event.

        Args:
          list_name: Name of key event list
        """
        self.key_event_data[list_name].append({self.key_event_names[0]: "New Entry",
                                               self.key_event_names[1]: "",
                                               self.key_event_names[2]: ""})

    def delete_key_event(self, list_name, key_event_idx):
        """Function to add empty key event.

        Args:
          list_name: Name of key event list
          key_event_idx: Index of key event entry
        """
        self.key_event_data[list_name].pop(key_event_idx)

    def add_key_event_list(self, list_name):
        """Function to add key event list.

        Args:
          list_name: Name of key event list
        """
        self.key_event_data[list_name] = list()
        self.list_names = list(self.key_event_data.keys())
        self.add_key_event(list_name)

    def remove_key_event_list(self, list_name):
        """Function to remove key event list.

        Args:
          list_name: Name of key event list
        """
        self.key_event_data.pop(list_name)
        self.list_names = list(self.key_event_data.keys())

    def rename_key_event_list(self, old_list_name, new_list_name):
        """Function to rename key event list.

        Args:
          old_list_name: Name of old key event list
          new_list_name: Name of new key event list
        """
        self.key_event_data[new_list_name] = self.key_event_data.pop(old_list_name)
        self.list_names = list(self.key_event_data.keys())

if __name__ == '__main__':
    pass
