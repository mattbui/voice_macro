import keyboard
from keyboard import KeyboardEvent
import json
import os

def restore_keyboard_events(json_filepath):
    with open(json_filepath, 'r') as json_file:
        events_json = json.load(json_file)

    events = []
    for event_json in events_json:
        event = KeyboardEvent(event_json['event_type'], \
        event_json['scan_code'], \
        event_json['name'], \
        event_json['time'], \
        event_json['device'], \
        is_keypad=event_json['is_keypad'])
        events.append(event)

    return events

def get_events_string(events):
    result = ''
    for event in events:
        if(event['event_type'] == 'down'):
            result += event['name'] + ', '
    result = result[:-2]
    return result
    
def delete_files(files):
    for file in files:
        os.remove(file)