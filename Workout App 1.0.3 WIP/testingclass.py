"""
* Name         : testingclass.py
* Author       : Aiden Evers
* Created      : 7/25/24
* Course       : CIS189
* IDE          : VSCode
* Description  : Program that gathers exercise information and inputs it in a database, then is later recalled.
*
* Academic Honesty: I attest that this is my original work.
* I have not used unauthorized source code, either modified or
* unmodified.       
"""
#Import section
import unittest
import _tkinter
from main import WorkoutProgram

#Making test class
class MyTestCase(unittest.TestCase):

    #Construct test
    def setUp(self):
        self.wptest = WorkoutProgram('Workout Recorder', width=400, height=200)

    #Tears down when done testing
    def tearDown(self):
        del self.wptest

    #Makes sure that class attributes are crated properly
    def test_object_created_attributes(self):
        self.assertEqual(self.wptest.win_title, 'Workout Recorder')
        self.assertEqual(self.wptest.width, 400)
        self.assertEqual(self.wptest.height, 200)

    #Makes sure str function returns correctly
    def test_str(self):
        self.assertEqual(str(self.wptest), 'The window title is Workout Recorder. The width of the window is (width=400). The height of the window is (height=200).')

    #Makes sure that repr returns correctly
    def test_repr(self):
        self.assertEqual(repr(self.wptest), 'WorkoutProgram(Workout Recorder, width=400, height=200)')

    #Checks instance with bad width input
    def test_err_width_value(self):
        with self.assertRaises(_tkinter.TclError):
            wo = WorkoutProgram('Workout Recorder', width='frog', height=120)

    #Checks instance with bad height input
    def test_err_height_value(self):
        with self.assertRaises(_tkinter.TclError):
            wo = WorkoutProgram('Workout Recorder', width=3, height='dog')


#Executes test
if __name__ == '__main__':
    unittest.main()