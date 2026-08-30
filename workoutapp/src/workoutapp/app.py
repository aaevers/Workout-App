import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import sqlite3
from datetime import datetime


class WorkoutApp(toga.App):


#MARK: Main / Startup Method
    def startup(self):

        #Database Connection Section
        self.conn = sqlite3.connect(self.paths.data / "workoutapp.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS workouts(
            name TEXT NOT NULL UNIQUE CHECK(length(trim(name)) > 0), 
            area TEXT NOT NULL)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS recorded_wo_data(
            name TEXT NOT NULL,
            area TEXT NOT NULL,
            date TEXT NOT NULL,
            sequence INTEGER NOT NULL,
            unit_value TEXT NOT NULL,
            unit TEXT NOT NULL,
            rep_time_value TEXT NOT NULL,
            rep_time TEXT NOT NULL)""")

        #Box Creation Section
        self.main_box = toga.Box(style=Pack(direction=COLUMN, flex=1, background_color="#15182e")) #Using self.main_box so I can access it in other methods, not using self, widget argument in this method as no widget would passthrough on startup
        header_box = toga.Box(style=Pack(direction=COLUMN, background_color="#d6c724c1"))
        curr_day_box = toga.Box(style=Pack(direction=COLUMN, background_color="#38374ed7", margin=10))
        scroll_box = toga.ScrollContainer(content=curr_day_box, style=Pack(direction=COLUMN, height=250))

        #Widget Creation Section
        header_label = toga.Label(f"Today - {datetime.now().strftime("%b %d %Y")}", style=Pack(font_size=24, font_weight="bold", margin=10, color="#182375"))
        self.curr_day_label = toga.Label(self.retrieve_workout((datetime.now().strftime("%b %d %Y"),)), style=Pack(font_size=12, margin=10, color="#FFFFFF"))
        edit_button = toga.Button("Edit", on_press=self.show_edit_view, style=Pack(width=200, height=200, background_color="#182375", color="#d6c724c1"))
        add_workout_button = toga.Button("Add Workout", on_press=self.add_workout_view, style=Pack(width=200, height=200, background_color="#182375", color="#d6c724c1"))
        previous_workout_button = toga.Button("Previous Workouts", on_press=self.previous_workout_view, style=Pack(width=200, height=200, background_color="#182375", color="#d6c724c1"))

        #Box Build Section
        self.main_box.add(header_box)
        self.main_box.add(scroll_box)
        self.main_box.add(edit_button)
        self.main_box.add(add_workout_button)
        self.main_box.add(previous_workout_button)
        curr_day_box.add(self.curr_day_label)
        header_box.add(header_label)

        #Window Build Section
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()


#MARK: View / Window Methods


    #Edit window, used for editing workouts using the list from DB
    def show_edit_view(self, widget):

        #Database Query Section
        current_wo_list = self.cur.execute("SELECT name FROM workouts").fetchall()
        
        #Box Creation Section
        edit_box = toga.Box(style=Pack(direction=COLUMN, flex=1, background_color="#15182e"))

        #Widget Creation Section
        exit_edit_button = toga.Button(icon=toga.Icon("resources/x"), on_press=self.go_home)
        test_label = toga.Label("This is the edit view", style=Pack(font_size=24, font_weight="bold", margin=10, color="#ECEEF8"))
        self.wo_list = toga.Selection(items=current_wo_list, style=Pack(font_size=18, margin=10, color="#ECEEF8"))
        self.unit_value_list = toga.TextInput(placeholder="lbs/kg", style=Pack(font_size=18, margin=0, color="#ECEEF8"))
        self.unit_list = toga.Selection(items=["lbs", "kg"], style=Pack(font_size=18, margin=0, color="#ECEEF8"))
        self.rep_value_list = toga.TextInput(placeholder="Reps/Hr:Min:Sec", style=Pack(font_size=18, margin=0, color="#ECEEF8"))
        self.rep_list = toga.Selection(items=["Reps", "Hr:Min:Sec"], style=Pack(font_size=18, margin=0, color="#ECEEF8"))
        self.sequence = toga.NumberInput(value=0, min=0, step=1)
        sumbit_button = toga.Button("Sumbit", on_press=self.record_workout)

        #Box Build Section
        edit_box.add(exit_edit_button)
        edit_box.add(test_label)
        edit_box.add(self.wo_list)
        edit_box.add(self.unit_value_list)
        edit_box.add(self.unit_list)
        edit_box.add(self.rep_value_list)
        edit_box.add(self.rep_list)
        edit_box.add(self.sequence)
        edit_box.add(sumbit_button)

        #Window Build Section
        self.main_window.content = edit_box

    
    #Add workout window, used for adding workouts to the DB
    def add_workout_view(self, widget):

        #Box Creation Section
        add_workout_box = toga.Box(style=Pack(direction=COLUMN, flex=1, background_color="#15182e"))

        #Widget Creation Section
        exit_button = toga.Button(icon=toga.Icon("resources/x"), on_press=self.go_home)
        add_wo_label = toga.Label("Add workouts here, use workout name, area of body", style=Pack(font_size=24, font_weight="bold", margin=10, color="#182375"))
        self.add_wo_name = toga.TextInput(placeholder="Workout Name", style=Pack(font_size=18, margin=10, color="#ECEEF8"))
        self.add_wo_area = toga.Selection(items=["Upper", "Lower", "Cardio"], style=Pack(font_size=18, margin=10, color="#ECEEF8"))
        add_wo_button = toga.Button("Accept?", on_press=self.add_workout, style=Pack(width=200, height=200, background_color="#182375", color="#d6c724c1"))

        #Box Build Section
        add_workout_box.add(exit_button)
        add_workout_box.add(add_wo_label)
        add_workout_box.add(self.add_wo_name)
        add_workout_box.add(self.add_wo_area)
        add_workout_box.add(add_wo_button)

        #Window Build Section
        self.main_window.content = add_workout_box


    #Window to show previous workouts based on date
    def previous_workout_view(self, widget):

        #Box Creation Section
        previous_workout_box = toga.Box(style=Pack(direction=COLUMN, flex=1, background_color="#15182e"))

        #Widget Creation Seciton
        exit_button = toga.Button(icon=toga.Icon("resources/x"), on_press=self.go_home)
        self.date_selector = toga.DateInput(on_change=self.format_date_select)
        self.past_workout = toga.Label("Select a date to get started!", style=Pack(font_size=12, margin=10, color="#FFFFFF"))

        #Box Build Section
        previous_workout_box.add(exit_button)
        previous_workout_box.add(self.date_selector)
        previous_workout_box.add(self.past_workout)

        #Window Build Section
        self.main_window.content = previous_workout_box


#MARK: Utility Methods


    def format_date_select(self, widget):
        match self.date_selector.value.month:
            case 1:
                month = "Jan"
            case 2:
                month = "Feb"
            case 3:
                month = "Mar"
            case 4:
                month = "Apr"
            case 5:
                month = "May"
            case 6:
                month = "Jun"
            case 7:
                month = "Jul"
            case 8:
                month = "Aug"
            case 9:
                month = "Sep"
            case 10:
                month = "Oct"
            case 11:
                month = "Nov"
            case 12:
                month = "Dec"
            case _:
                month = ""
        match self.date_selector.value.day:
            case 1:
                day = "01"
            case 2:
                day = "02"
            case 3:
                day = "03"
            case 4:
                day = "04"
            case 5:
                day = "05"
            case 6:
                day = "06"
            case 7:
                day = "07"
            case 8:
                day = "08"
            case 9:
                day = "09"
            case _:
                day = self.date_selector.value.day
        self.past_workout.text = self.retrieve_workout(((f"{month} {day} {self.date_selector.value.year}"),))
        print(f"{month} {self.date_selector.value.day} {self.date_selector.value.year}")


    #Used as a return to home window
    def go_home(self, widget):
            self.curr_day_label.text = self.retrieve_workout((datetime.now().strftime("%b %d %Y"),)) #This is what will update the current day overview text, necesarry for updates, otherwise you'd need to close the app and reopen
            self.main_window.content = self.main_box


    #Used to add workouts to DB for selection later
    async def add_workout(self, widget):
        try:
            self.cur.execute("INSERT INTO workouts VALUES(?, ?)", (self.add_wo_name.value, self.add_wo_area.value))
        except sqlite3.IntegrityError:
            await self.main_window.info_dialog("Error", "Workout name must be unique and not empty.")
            return
        self.conn.commit()
        await self.main_window.info_dialog("Success!", "Workout added successfully!")


    #Used to record workouts on the edit page
    async def record_workout(self, widget):
        cur_name, cur_area = self.cur.execute(f"SELECT name, area FROM workouts WHERE name = ?", (self.wo_list.value,)).fetchone()
        try:
            self.cur.execute("INSERT INTO recorded_wo_data VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (cur_name, cur_area, datetime.now().strftime("%b %d %Y"), int(self.sequence.value), self.unit_value_list.value, self.unit_list.value, self.rep_value_list.value, self.rep_list.value))
        except sqlite3.IntegrityError:
            await self.main_window.info_dialog("Error", "Something is wrong with your workout data...")
            return
        self.conn.commit()
        await self.main_window.info_dialog("Success!", "Workout recorded successfully!")


    #Retrieve Workout Data, used for the search or current day info
    def retrieve_workout(self, searched_date):
        today_list = self.cur.execute(f"SELECT * FROM recorded_wo_data WHERE date = ?", searched_date).fetchall()
        return_string = ""
        for i in range(len(today_list)):
            if(i != (len(today_list) - 1)):
                return_string += f"{today_list[i][0]} | {today_list[i][1]} | {today_list[i][6]} {today_list[i][7]} @ {today_list[i][4]} {today_list[i][5]} | Sequence: {today_list[i][3]}\n\n"
            else:
                return_string += f"{today_list[i][0]} | {today_list[i][1]} | {today_list[i][6]} {today_list[i][7]} @ {today_list[i][4]} {today_list[i][5]} | Sequence: {today_list[i][3]}"
        return return_string

#MARK: Driver method
def main():
    return WorkoutApp()

