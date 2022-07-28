from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# popup classes


class LoginFailed(FloatLayout):
    @staticmethod
    def login_failed():
        show = LoginFailed()
        popup_window = Popup(title="Login failed", content=show, size_hint=(None, None), size=(400, 400))
        popup_window.open()


class RegisterSuccess(FloatLayout):
    @staticmethod
    def register_success():
        show = RegisterSuccess()
        popup_window = Popup(title="Registration success", content=show, size_hint=(None, None), size=(400, 400))
        popup_window.open()


class RegisterFailed(FloatLayout):
    @staticmethod
    def register_failed():
        show = RegisterFailed()
        popup_window = Popup(title="Registration failed", content=show, size_hint=(None, None), size=(400, 400))
        popup_window.open()


class AddSuccess(FloatLayout):
    @staticmethod
    def add_success():
        show = AddSuccess()
        popup_window = Popup(title="Success", content=show, size_hint=(None, None), size=(400, 400))
        popup_window.open()


class AddFailed(FloatLayout):
    @staticmethod
    def add_failed():
        show = AddFailed()
        popup_window = Popup(title="Error", content=show, size_hint=(None, None), size=(400, 400))
        popup_window.open()


class EditPatientSuccess(FloatLayout):
    @staticmethod
    def edit_patient_success():
        show = EditPatientSuccess()
        popup_window = Popup(title="Success", content=show, size_hint=(None, None), size=(400, 400))
        popup_window.open()


class EditPatientFailed(FloatLayout):
    @staticmethod
    def edit_patient_failed():
        show = EditPatientFailed()
        popup_window = Popup(title="Error", content=show, size_hint=(None, None), size=(400, 400))
        popup_window.open()


class ConnectionFailed(FloatLayout):
    @staticmethod
    def connection_failed():
        show = ConnectionFailed()
        popup_window = Popup(title="Connection failure", content=show, size_hint=(None, None), size=(400, 400))
        popup_window.open()


class ConfirmDeletion(FloatLayout):
    @staticmethod
    def confirm_deletion():
        show = ConfirmDeletion()
        popup_window = Popup(title="Success", content=show, size_hint=(None, None), size=(400, 400))
        popup_window.open()


class EditSuccess(FloatLayout):
    @staticmethod
    def edit_success():
        show = EditSuccess()
        popup_window = Popup(title="Success", content=show, size_hint=(None, None), size=(400, 400))
        popup_window.open()


class EditFailed(FloatLayout):
    @staticmethod
    def edit_failed():
        show = EditFailed()
        popup_window = Popup(title="Error", content=show, size_hint=(None, None), size=(400, 400))
        popup_window.open()


class MustSelect(FloatLayout):
    @staticmethod
    def must_select():
        show = MustSelect()
        popup_window = Popup(title="Error", content=show, size_hint=(None, None), size=(400, 400))
        popup_window.open()
