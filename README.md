# Voice Macro
This is a keyboard macro program using voice command project, using `keyboard` and [`snowboy`](https://snowboy.kitt.ai/) package.

![home_page](screenshots/home.png)

## Installation
Basic requirements:
- Python2.7
- Snowboy for python (check out their [github](https://github.com/kitt-ai/snowboy) for installation)

After compile snowboy, replace `snowboydetect.py` and `_snowboydetect.so` with your compiled version.

```bash
pip install -r requirements.txt
```

## Usage

### Running server
**Note:** The keyboard package need **root** permission to run.
```bash
sudo python server.py --port *your_port*
```
For more optional arguments `python server.py --help`
The server will be run at `localhost:*your_port*`. Ex: `sudo python server.py --port 8000` then the server will be running at `localhost:8000`.
To run it automatically when the OS start add the script to /etc/init.d as described [here](https://askubuntu.com/questions/290099/how-to-run-a-script-during-boot-as-root)

### Manage macros
You will be able to manage your macros via web interface at `localhost:<your_port>`

![form_page](screenshots/form.png)

## Author
Minh Bui.

Contact me via buicongminh2717@gmail.com



