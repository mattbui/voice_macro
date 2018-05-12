from flask import render_template, Flask, redirect, request, jsonify
import sqlite3
import os
import sys
import argparse
from db import Database
from recorders import SoundRecorder, KeyboardRecorder
import training_service
from listener import Listener

app = Flask(__name__)
sound_recorder = SoundRecorder()
keyboard_recorder = KeyboardRecorder()
database = Database()
sensitivity = 0.35

@app.route('/')
def index():
    global database
    sound_recorder.end()
    macros = database.get_all()
    return render_template('index.html', macros=macros)

@app.route('/new_macro_form')
def new_macro_form():
    global sound_recorder
    sound_recorder.start()
    return render_template('new_macro.html')

@app.route('/delete/<id>')
def delete(id=None):
    global listenter, database
    _, _, _, _, _, _, _, ke_path, model_path = database.get_macro(id)
    os.remove(ke_path)
    os.remove(model_path)
    database.delete_macro(id)
    try:
        listenter.stop()
    except Exception as e:
        pass
    if(len(database.get_all()) > 0):
        listenter = Listener(sensitivity=sensitivity)
        listenter.start()
    return redirect('/')

@app.route('/switch_sound_record')
def switch_sound_record():
    global sound_recorder
    return jsonify(sound_recorder.switch())

@app.route('/clear_cache', methods=["POST"])
def clear_cache():
    sound_1 = request.form.get("sound_1")
    sound_2 = request.form.get("sound_2")
    sound_3 = request.form.get("sound_3")
    keyboard_events_path = request.form.get("key_file")
    if(sound_1 != None and sound_1 != ""):
        try:
            os.remove(sound_1)
        except:
            pass
    if(sound_2 != None and sound_2 != ""):
        try:
            os.remove(sound_2)
        except:
            pass
    if(sound_3 != None and sound_3 != ""):
        try:
            os.remove(sound_3)
        except:
            pass
    if(keyboard_events_path != None and keyboard_events_path != ""):
        try:
            os.remove(keyboard_events_path)
        except:
            pass

    return jsonify({"message": "ok"})


@app.route('/keyboard_record', methods=["POST"])
def keyboard_record():
    global keyboard_recorder
    file = request.form.get("file")
    if(file != "" and file != None):
        os.remove(file)
    output_file, events_string = keyboard_recorder.start_record()
    return jsonify({"output_file": output_file, "events_string": events_string})

@app.route('/<id>')
def detail(id=None):
    global database
    macro = database.get_macro(id)
    return render_template("detail.html", macro=macro)

@app.route('/add_macro', methods=["POST"])
def add_macro():
    global database, listenter
    name = request.form.get("name")
    language = request.form.get("language")
    age_group = request.form.get("age")
    gender = request.form.get("gender")
    description = request.form.get("description")
    keyboard_events_path = request.form.get("key_file")
    event_strings = request.form.get("events_string")
    sound_1 = request.form.get("sound_1")
    sound_2 = request.form.get("sound_2")
    sound_3 = request.form.get("sound_3")

    ok, message = training_service.get_model(name, (sound_1, sound_2, sound_3), language, age_group, gender)
    if(not ok):
        return jsonify({"message": message})
    else:
        try:
            database.insert((name, language, age_group, gender, description, event_strings, keyboard_events_path, message))
            try:
                listenter.stop()
            except Exception as e:
                pass
            if(len(database.get_all()) > 0):
                listenter = Listener(sensitivity=sensitivity)
                listenter.start()
            return jsonify({"message": "ok"})
        except sqlite3.Error as e:
            return jsonify({"message": e.args[0]})

def parse_argument(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("--port", type=int, help="The port for the server run locally", default=8000)

    return parser.parse_args(argv)

args = parse_argument(sys.argv[1:])
if(len(database.get_all()) > 0):
    listenter = Listener(sensitivity=sensitivity)
    listenter.start()
app.run('0.0.0.0', args.port)
sound_recorder.end()
try:
    listenter.stop()
except:
    pass
database.close()
