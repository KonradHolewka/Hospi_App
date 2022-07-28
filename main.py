from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import qrscan
import psqlconnect
import psycopg2
import popup_windows
from psycopg2 import errors
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# global variables
data = 0
code = 0
user_id = ''
physician_name = ''
physician_surname = ''
spinnervalues = []
ind = ""

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# window manager class
class WindowManager(ScreenManager):
    pass

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# window classes

# log in window
class LoginWindow(Screen):
    login = ObjectProperty(None)
    password = ObjectProperty(None)
    flag = 0
    def check(self):
        try:
            global user_id, physician_name, physician_surname
            self.flag, user_id, physician_name, physician_surname = psqlconnect.authorization(self.login.text, self.password.text)
        except psycopg2.OperationalError:
            popup_windows.ConnectionFailed.connection_failed()


    def invalid(self):
        popup_windows.LoginFailed.login_failed()

# main window
class MainWindow(Screen):
    user = ObjectProperty(None)
    def update_userid(self):
        global user_id, physician_name, physician_surname
        self.user.text = "User ID: " + user_id + "\n" + \
                         "Welcome back, doctor " + physician_name + " " + physician_surname + "!"

    def start_scan(self):
        global code
        code = qrscan.start_scan()

# data display window
class DataWindow(Screen):
    graph = ObjectProperty(None)
    patient_label = ObjectProperty(None)
    flag = 1

    def get_patientdata(self):
        patient_data = psqlconnect.get_pdata(code)
        self.patient_label.text = "Patient\'s name: " + str(patient_data[1]) + " " + str(patient_data[2]) + \
                                  "          Patient\'s ID: " + str(patient_data[0])

    def get_data(self):
        global data, spinnervalues
        plt.close()
        data, spinnervalues = psqlconnect.patientcard_load(code)

        if self.flag == 1:
            self.graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            self.flag = 0
        else:
            self.graph.clear_widgets()
            self.graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))

# patient registration window
class RegisterWindow(Screen):
    pname = ObjectProperty(None)
    psurname = ObjectProperty(None)
    ppesel = ObjectProperty(None)
    pweight = ObjectProperty(None)
    pheight = ObjectProperty(None)
    psex = ObjectProperty(None)

    def register(self):
        global user_id
        try:
            psqlconnect.new_patient(
                                    self.pname.text,
                                    self.psurname.text,
                                    self.ppesel.text,
                                    self.pweight.text,
                                    self.pheight.text,
                                    self.psex.text,
                                    user_id
                                    )
            popup_windows.RegisterSuccess.register_success()
            self.clear()
        except errors.lookup("42601"):
            popup_windows.RegisterFailed.register_failed()
            self.clear()

    def clear(self):
        self.pname.text = ""
        self.psurname.text = ""
        self.ppesel.text = ""
        self.pweight.text = ""
        self.pheight.text = ""
        self.psex.text = ""

# measurement addition window
class AddMeasurementWindow(Screen):
    temp = ObjectProperty(None)
    pulse = ObjectProperty(None)
    bpressure = ObjectProperty(None)

    def add(self):
        try:
            psqlconnect.add_measurement(
                                        self.temp.text,
                                        self.pulse.text,
                                        self.bpressure.text,
                                        code
                                        )
            popup_windows.AddSuccess.add_success()
            self.clear()
        except errors.lookup("42601"):
            popup_windows.AddFailed.add_failed()
            self.clear()

    def clear(self):
        self.temp.text = ""
        self.pulse.text = ""
        self.bpressure.text = ""

# patient data edition window
class EditPatientWindow(Screen):

    pdata = ()

    pname = ObjectProperty(None)
    psurname = ObjectProperty(None)
    ppesel = ObjectProperty(None)
    pweight = ObjectProperty(None)
    pheight = ObjectProperty(None)
    psex = ObjectProperty(None)

    npname = ObjectProperty(None)
    npsurname = ObjectProperty(None)
    nppesel = ObjectProperty(None)
    npweight = ObjectProperty(None)
    npheight = ObjectProperty(None)
    npsex = ObjectProperty(None)

    def update_pdata(self):
        global code
        self.pdata = psqlconnect.get_pdata(code)
        print(self.pdata)
        self.pname.text = self.pdata[1]
        self.psurname.text = self.pdata[2]
        self.ppesel.text = str(self.pdata[3])
        self.pweight.text = self.pdata[4]
        self.pheight.text = self.pdata[5]
        self.psex.text = self.pdata[7]

    def edit(self):
        global code
        try:
            self.npdata = psqlconnect.edit_patient(
                                                    self.npname.text,
                                                    self.npsurname.text,
                                                    self.nppesel.text,
                                                    self.npweight.text,
                                                    self.npheight.text,
                                                    self.npsex.text, code
                                                    )
            popup_windows.EditPatientSuccess.edit_patient_success()
            self.clear()
        except errors.lookup("42601"):
            popup_windows.EditPatientFailed.edit_patient_failed()
            self.clear()

    def clear(self):
        self.npname.text = ""
        self.npsurname.text = ""
        self.nppesel.text = ""
        self.npweight.text = ""
        self.npheight.text = ""
        self.npsex.text = ""

# measurement selection window
class EditMeasurementWindow(Screen):
    spin = ObjectProperty(None)
    def update(self):
        global data, spinnervalues
        self.spin.values = spinnervalues
        self.spin.text = "Select a timestamp..."

    def get_ind(self):
        if self.spin.text == "Select a timestamp...":
            popup_windows.MustSelect.must_select()
        else:
            global ind
            ind = self.spin.text
            print(ind)

# measurement edition window
class EditWindow(Screen):
    temp = ObjectProperty(None)
    pulse = ObjectProperty(None)
    bpressure = ObjectProperty(None)

    def edit(self):
        global ind
        try:
            psqlconnect.edit_measurement(
                self.temp.text,
                self.pulse.text,
                self.bpressure.text,
                code,
                ind
            )
            popup_windows.EditSuccess.edit_success()
            self.clear()
        except errors.lookup("42601"):
            popup_windows.EditFailed.edit_failed()
            self.clear()

    def clear(self):
        self.temp.text = ""
        self.pulse.text = ""
        self.bpressure.text = ""

# deletion confirmation window
class Deletion_conf(Screen):
    def conf_delete(self):
        global code, ind
        psqlconnect.delete_record(ind, code)
        popup_windows.ConfirmDeletion.confirm_deletion()

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# kv file loading and app running function
kv = Builder.load_file("my.kv")

class MyMainApp(App):
    def build(self):
        return kv

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    MyMainApp().run()