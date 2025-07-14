"""
* Name         : main.py
* Author       : Aiden Evers
* Created      : 7/18/24
* Course       : CIS189
* IDE          : VSCode
* Description  : Program that gathers exercise information and inputs it in a database, then is later recalled.  
"""
#Import section
import tkinter as tk
import datetime
import sqlite3 as sql

#Class that contains all methods
class WorkoutProgram:

    def __init__(self, win_title, width=0, height=0):
        self.win_title = win_title
        self.width = width
        self.height = height
        self.window = tk.Tk()
        self.window.minsize(width, height)
        self.window.title(win_title)
        self.window.iconphoto(False, tk.PhotoImage(file='workouticon.png'))
        self.search_icon = tk.PhotoImage(file='mag_glass.png')
    
    #Method definitions
    def create_table(self):
        #Creates connection to database
        conn = sql.connect('workoutdatabase.db') 
    
        #Creates a cursor
        c = conn.cursor()  
    
        #This uses the cursor/connection and actually makes and formats the table
        c.execute('''CREATE TABLE IF NOT EXISTS workouts (
            date text NOT NULL, 
            workout text NOT NULL, 
            set_number text NOT NULL, 
            repweight text NOT NULL )''')
    
    def add_workout(self):
        #Creates tuple from data gathered by the entry boxes on the main_window
        tup = (str(datetime.date.today()), wo_var.get(), f'Set: {set_var.get()}', f'{rep_var.get()} reps at {wei_var.get()}lbs')

        #Creates connection to database
        conn = sql.connect('workoutdatabase.db')
    
        #Using connection to database it creactes a cursor, establishes variable insert as a sql command then inputs the tup input argument and the sql code
        with conn:
            c = conn.cursor()
            insert = '''INSERT INTO workouts(date,workout,set_number,repweight)
                VALUES(?,?,?,?)'''
            c.execute(insert, tup)

    def close(self):
        #Closes main window and ends program
        self.window.destroy()

    def display(self):
        #Takes date from date search bar
        date = date_var.get()
    
        #Creates new window for table
        dis = tk.Toplevel()
        dis.title(f'Table for {date}')
        dis.iconphoto(False, self.search_icon)
        dis.minsize(400, 100)
    
        #Establishes connection
        conn = sql.connect('workoutdatabase.db')

        #This below creates a spacing effect
        spacing = tk.Label(dis, text='                                  ')
        spacing.grid(column=1)

        #Tries the connection, will raise a connection error if connection to database is not made
        try:
        
            #Uses connection and makes cursor
            with conn:
                cur = conn.cursor()
        
                #Grabs all data from database and puts it in a variable
                cur.execute(f'SELECT * FROM workouts')
                log = cur.fetchall()
        
                #Sets y value for later so new information will print row after row
                y = 0

                #Iterates over data variable
                for x in log:
                    #Finds date search term
                    if x[0] == date:
                
                        #Puts a labels into the new window for every instance of the date
                        label = tk.Label(dis, text=f'{x[1]} | {x[2]} | {x[3]}')
                        label.grid(column=2, row=y)
                        y += 1
                    else:
                        #Adds a value to y to continue the search
                        y += 1
                        
                        #Checks to see if it hit the bottom of the list without a result, returns No Data if so
                        if y == len(log):
                            none_label = tk.Label(dis, text='No Data')
                            none_label.grid(column=1, row=1)
                
        #Raises connection error and prints error message in new window
        except:
            label = tk.Label(dis, text='Connection Error')
            label.grid(column=0, row=0)
            raise ConnectionError
        
    def __str__(self):
        #Returns human readable expression of the class
        return f'The window title is {self.win_title}. The width of the window is (width={self.width}). The height of the window is (height={self.height}).'

    def __repr__(self):
        #Returns the way to reproduce the class
        return f'WorkoutProgram({self.win_title}, width={self.width}, height={self.height})'


#Instantiates class object, creates table, the main window and sizes the main window
g = WorkoutProgram('Workout Recorder', width=400, height=200)
g.create_table()


#This isntantiates the variable and asserts that they're string variables
wo_var = tk.StringVar()
set_var = tk.StringVar()
rep_var = tk.StringVar()
wei_var = tk.StringVar()
date_var = tk.StringVar()


#Below is the exhaustive list of all the workouts I currently have/know about
workouts = ("Run", "Bench-Press", "Squat")


#All the entry fields for the user to enter in values, left open to alphanumeric in case user wants to input four instead of 4, plus dropdown with workouts
wo_dropdown = tk.OptionMenu(g.window, wo_var, *workouts)
wo_dropdown.grid(column=1, row=2)

set_number = tk.Entry(g.window, textvariable=set_var, width=10)
set_number.grid(column=2, row=2)

rep_number = tk.Entry(g.window, textvariable=rep_var, width=10)
rep_number.grid(column=3, row=2)

weight = tk.Entry(g.window, textvariable=wei_var, width=10)
weight.grid(column=4, row=2)

date_var = tk.Entry(g.window, textvariable=date_var, width=10)
date_var.place(x=290, y=104)


#Main labels for each entry box
wo_label = tk.Label(g.window, text='Select Workout')
wo_label.grid(column=1, row=3)

set_label = tk.Label(g.window, text='Enter Set Number')
set_label.grid(column=2, row=3)

rep_label = tk.Label(g.window, text='How Many Reps?')
rep_label.grid(column=3, row=3)

weight_label = tk.Label(g.window, text='What Weight?')
weight_label.grid(column=4, row=3)

date_label = tk.Label(g.window, text="""Enter Date for Search
in Format YYYY-MM-DD""")
date_label.place(x=260, y=125)


#Buttons to exit / perform Add and Show Table functions
exit_button = tk.Button(g.window, text='Exit', width=5, height=1, command=g.close)
exit_button.place(x=150, y=150)

l = tk.Button(g.window, text='Add', width=5, height=1, command=g.add_workout)
l.place(x=150, y=100) 

show_tab_button = tk.Button(g.window, text='Search', width=5, height=1, command=g.display)
show_tab_button.place(x=200, y=100)


#Driver code
def main():
    g.window.mainloop()


#Execution code
if __name__ == '__main__':
    main()