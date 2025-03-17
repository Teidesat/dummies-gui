# Transmitter GUI
This README.md explains the structure that the transmitter GUI is using, so mantaining and adding functionalities is clearer.

- `callbacks.py`. Used to write the functions that are going to be used as callbacks for events on the program. The functions defined are going to be used with two parameters: window and values (of the window's fields)
- `keys.py`. Contains unique IDs to identify the elements of the layouts.
- `layout.py`. Contains the layout of the application, using PySimpleGUI elements.
- `utils.py`. Various functions used in the app.

Finally, `transmitter-gui.py` is the main script. It runs the IM loop of PySimpleGUI and is made by a dictionary of keys (from `keys.py`) and their respective callbacks. This way the loop is simplified to a check in this dict. If there is any special event (like saving settings) which doesn't work the same way as other events, you may still write it in the loop.