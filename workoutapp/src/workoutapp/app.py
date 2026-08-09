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

        #Database Connection Section
        self.conn = sqlite3.connect(self.paths.data / "workoutapp.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS workouts(
            name TEXT NOT NULL UNIQUE CHECK(length(trim(name)) > 0), 
            area TEXT NOT NULL)""")

        #Box Creation Section
        self.main_box = toga.Box(style=Pack(direction=COLUMN, flex=1, background_color="#15182e")) #Using self.main_box so I can access it in other methods, not using self, widget argument in this method as no widget would passthrough on startup
        header_box = toga.Box(style=Pack(direction=COLUMN, background_color="#d6c724c1"))

        #Widget Creation Section
        header_label = toga.Label(f"Today - {datetime.now().strftime("%b %d %Y")}", style=Pack(font_size=24, font_weight="bold", padding=10, color="#182375"))
        edit_button = toga.Button("Edit", on_press=self.show_edit_view, style=Pack(width=200, height=200, background_color="#182375", color="#d6c724c1"))
        add_workout_button = toga.Button("Add Workout", on_press=self.add_workout_view, style=Pack(width=200, height=200, background_color="#182375", color="#d6c724c1"))

        #Box Build Section
        self.main_box.add(header_box)
        self.main_box.add(edit_button)
        self.main_box.add(add_workout_button)
        header_box.add(header_label)

        #Window Build Section
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

    def show_edit_view(self, widget):
        
        #Box Creation Section
        edit_box = toga.Box(style=Pack(direction=COLUMN, flex=1, background_color="#15182e"))

        #Widget Creation Section
        exit_edit_button = toga.Button(icon=toga.Icon("resources/x"), on_press=self.go_home)
        test_label = toga.Label("This is the edit view", style=Pack(font_size=24, font_weight="bold", padding=10, color="#182375"))

        #Box Build Section
        edit_box.add(exit_edit_button)
        edit_box.add(test_label)

        #Window Build Section
        self.main_window.content = edit_box

    def go_home(self, widget):
        self.main_window.content = self.main_box

    def add_workout_view(self, widget):

        #Box Creation Section
        add_workout_box = toga.Box(style=Pack(direction=COLUMN, flex=1, background_color="#15182e"))

        #Widget Creation Section
        exit_button = toga.Button(icon=toga.Icon("resources/x"), on_press=self.go_home)
        add_wo_label = toga.Label("Add workouts here, use workout name, area of body", style=Pack(font_size=24, font_weight="bold", padding=10, color="#182375"))
        self.add_wo_name = toga.TextInput(placeholder="Workout Name", style=Pack(font_size=18, padding=10, color="#ECEEF8"))
        self.add_wo_area = toga.Selection(items=["Upper", "Lower", "Cardio"], style=Pack(font_size=18, padding=10, color="#182375"))
        add_wo_button = toga.Button("Accept?", on_press=self.add_workout, style=Pack(width=200, height=200, background_color="#182375", color="#d6c724c1"))

        #Box Build Section
        add_workout_box.add(exit_button)
        add_workout_box.add(add_wo_label)
        add_workout_box.add(self.add_wo_name)
        add_workout_box.add(self.add_wo_area)
        add_workout_box.add(add_wo_button)

        #Window Build Section
        self.main_window.content = add_workout_box

    async def add_workout(self, widget):
        try:
            self.cur.execute("INSERT INTO workouts VALUES(?, ?)", (self.add_wo_name.value, self.add_wo_area.value))
        except sqlite3.IntegrityError:
            await self.main_window.info_dialog("Error", "Workout name must be unique and not empty.")
            return
        self.conn.commit()
        await self.main_window.info_dialog("Success!", "Workout added successfully!")

def main():
    return WorkoutApp()
