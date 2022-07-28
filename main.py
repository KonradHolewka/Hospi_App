from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import qrscan
import psqlconnect
import psycopg2
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
            connection_failed()


    def invalid(self):
        login_failed()

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
            register_success()
            self.clear()
        except errors.lookup("42601"):
            register_failed()
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
            add_success()
            self.clear()
        except errors.lookup("42601"):
            add_failed()
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
            edit_patient_success()
            self.clear()
        except errors.lookup("42601"):
            edit_patient_failed()
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
            must_select()
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
            edit_success()
            self.clear()
        except errors.lookup("42601"):
            edit_failed()
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
        conf_del()

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# pop-up window classes

class Login_failed(FloatLayout):
    pass

class Register_failed(FloatLayout):
    pass

class Register_success(FloatLayout):
    pass

class Add_success(FloatLayout):
    pass

class Add_failed(FloatLayout):
    pass

class Edit_patient_success(FloatLayout):
    pass

class Edit_patient_failed(FloatLayout):
    pass

class Connection_failed(FloatLayout):
    pass

class Conf_del(FloatLayout):
    pass

class Edit_success(FloatLayout):
    pass

class Edit_failed(FloatLayout):
    pass

class Must_select(FloatLayout):
    pass
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# kv file loading and app running function
kv = Builder.load_file("my.kv")

class MyMainApp(App):
    def build(self):
        return kv

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# popup functions
def login_failed():
    show = Login_failed()
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size=(400,400))
    popupWindow.open()

def register_failed():
    show = Register_failed()
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size=(400, 400))
    popupWindow.open()

def register_success():
    show = Register_success()
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size=(400, 400))
    popupWindow.open()

def add_failed():
    show = Add_failed()
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size=(400, 400))
    popupWindow.open()

def add_success():
    show = Add_success()
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size=(400, 400))
    popupWindow.open()

def edit_patient_success():
    show = Edit_patient_success()
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size=(400, 400))
    popupWindow.open()

def edit_patient_failed():
    show = Edit_patient_failed()
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size=(400, 400))
    popupWindow.open()

def connection_failed():
    show = Connection_failed()
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size=(400, 400))
    popupWindow.open()

def conf_del():
    show = Conf_del()
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size=(400, 400))
    popupWindow.open()

def edit_success():
    show = Edit_success()
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size=(400, 400))
    popupWindow.open()

def edit_failed():
    show = Edit_failed()
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size=(400, 400))
    popupWindow.open()

def must_select():
    show = Must_select()
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size=(400, 400))
    popupWindow.open()
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    MyMainApp().run()