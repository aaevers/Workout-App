"""
My first application
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import sqlite3
from datetime import datetime

def greeting(name):
        if name:
            return f"Hello, {name}!"
        else:
            return "Hey pookie"

class WorkoutApp(toga.App):
    def startup(self):

        #Box Creation Section
        main_box = toga.Box(style=Pack(direction=COLUMN, flex=1, background_color="#15182e"))
        header_box = toga.Box(style=Pack(direction=COLUMN, background_color="#d6c724c1"))

        #Widget Creation Section
        header_label = toga.Label(f"Today - {datetime.now().strftime("%b %d %Y")}", style=Pack(font_size=24, font_weight="bold", padding=10, color="#182375"))
        edit_button = toga.Button("Edit", on_press=self.show_edit_view, style=Pack(width=200, height=200, background_color="#182375", color="#d6c724c1"))

        #Box Build Section
        main_box.add(header_box)
        main_box.add(edit_button)
        header_box.add(header_label)

        #Window Build Section
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def show_edit_view(self, widget):
        
        #Box Creation Section
        edit_box = toga.Box(style=Pack(direction=COLUMN, flex=1, background_color="#15182e"))

        #Widget Creation Section
        test_label = toga.Label("This is the edit view", style=Pack(font_size=24, font_weight="bold", padding=10, color="#182375"))

        #Box Build Section
        edit_box.add(test_label)

        #Window Build Section
        self.main_window.content = edit_box

def main():
    return WorkoutApp()
