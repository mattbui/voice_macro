from lib import snowboydecoder
import signal
import keyboard
import utils
from db import Database
import threading

class Listener(threading.Thread):

    def __init__(self, sensitivity=0.5):
        threading.Thread.__init__(self)
        self.sensitivity = sensitivity
        self.interrupted = False

    def _interrupt_callback(self):
        return self.interrupted

    def stop(self):

        self.interrupted = True

    def _key_action(self, index):
        events = utils.restore_keyboard_events(self.keyboard_jsons[index])
        keyboard.play(events)
    
    def run(self):
        database = Database()
        data = database.get_list_model_keyboard()

        self.models = []
        self.keyboard_jsons = []
        for model, keyboard_json in data:
            self.models.append(model)
            self.keyboard_jsons.append(keyboard_json)
        
        self.interrupted = False
        sensitivities = [self.sensitivity]*len(self.models)
        callbacks = [lambda index=i: self._key_action(index) for i in range(len(self.models))]

        detector = snowboydecoder.HotwordDetector(self.models, sensitivity=sensitivities)
        print('Listener listening .... ({} models)'.format(len(self.models)))
        detector.start(detected_callback=callbacks,
               interrupt_check=self._interrupt_callback,
               sleep_time=0.01)

        detector.terminate()