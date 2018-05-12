from __future__ import print_function
import sys
import keyboard
from keyboard import KeyboardEvent
import pyaudio
import wave
import os
import time
from time import gmtime, strftime
import shutil
import json
import utils

class SoundRecorder:

    def __init__(self, output_dir='sound_files'):
        self.is_recording = False
        self.enable_trigger_record = True
        self.output_dir = output_dir
        self.data_buffer = []
        self.saved_files = []
        self.file_index = 0
        self.p = None
        self.stream = None

    def _change_recording_state(self):
        if((not self.is_recording) and self.enable_trigger_record):
            self.is_recording = True
            print('Recording...')
        elif(self.is_recording):
            self.is_recording = False
            # self.num_record_file -= 1
            print('stopped')

    def _callback(self, in_data, frame_count, time_info, status):
        if(self.is_recording):
            self.data_buffer.append(in_data)
            self.enable_trigger_record = False

        elif(len(self.data_buffer) > 0):
            file_path = self._write_to_file()
            print('recorded file at : {}'.format(file_path))
            self.saved_files.append(file_path)
            self.data_buffer = []
        self.enable_trigger_record = True
        
        return (in_data, pyaudio.paContinue)

    def _write_to_file(self):
        timestamp = strftime("%m-%d-%Y-%H:%M:%S", gmtime())
        out_filename = os.path.join(self.output_dir + '/' + timestamp + ".wav")
        
        file = wave.open(out_filename, 'wb')
        file.setnchannels(1)
        file.setsampwidth(4)
        file.setframerate(16000)

        file.writeframes(b''.join(self.data_buffer))
        file.close()
        return out_filename

    def start(self):
        if(not os.path.exists(self.output_dir)):
            os.makedirs(self.output_dir)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt32,
            channels=1,
            rate=16000,
            input=True,
            stream_callback=self._callback
        )
        self.stream.start_stream()

    def switch(self):
        if(self.is_recording == False):
            self._change_recording_state()
            return {"message": "recording"}
        else:
            self._change_recording_state()
            while(len(self.saved_files) == self.file_index):
                pass
            saved_file = self.saved_files[self.file_index]
            self.file_index += 1
            return {"message": saved_file}

    def end(self):

        shutil.rmtree(self.output_dir, ignore_errors=True)
        if(self.stream != None and self.p != None):
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            self.p = None
            self.stream = None

class KeyboardRecorder:

    def __init__(self, output_dir='keyboard_events'):
        self.output_dir = output_dir
        self.stop_key = 'esc'
        if(not os.path.exists(self.output_dir)):
            os.makedirs(self.output_dir)

    def start_record(self):
        print("Start record keyboard events, press {} to stop record....".format(self.stop_key))
        recorded_events = keyboard.record(until=self.stop_key)
        events_json = []
        for event in recorded_events:
            events_json.append(json.loads(event.to_json()))
        events_json = events_json[:-1]
        events_string = utils.get_events_string(events_json)
        out_filename = self._write_to_file(events_json)

        print('\nSaved keyboard events at {}'.format(out_filename))

        return out_filename, events_string
    
    def _write_to_file(self, events_json):
        timestamp = strftime("%m-%d-%Y-%H:%M:%S", gmtime())
        out_filename = os.path.join(self.output_dir + '/' + timestamp + ".json")

        with open(out_filename, 'w') as file:
            json.dump(events_json, file)
        return out_filename