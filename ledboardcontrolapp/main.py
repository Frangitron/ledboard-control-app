__version__ = '0.0.0'

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.slider import Slider

from ledboardclientfull.serial_communication.c_structs import ControlParametersStruct
from pythonarduinoserial.usbserial.api import get_usb_serial

from ledboardclientfull.board_api import BoardApi


class LEDBoardControlApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.board_api: BoardApi = None

        self.button_dropdown_ports: Button = None
        self.dropdown_ports: DropDown = None
        self.slider: Slider = None

        self.control_parameters = ControlParametersStruct()

    def select_port(self, port: str):
        self.dropdown_ports.select(port)
        self.board_api = BoardApi(port)
        self.control_parameters = self.board_api.get_control_parameters()
        self.slider.value = self.control_parameters.noise_r

    def change_value(self, value: int):
        self.control_parameters.noise_r = value

    def send_control_parameters(self):
        if self.board_api is not None:
            self.board_api.set_control_parameters(self.control_parameters)

    def list_available_devices(self):
        for name in get_usb_serial().list_names():
            button = Button(
                text=name,
                size_hint_y=None,
                height=40
            )
            button.bind(on_release=lambda button: self.select_port(button.text))
            self.dropdown_ports.add_widget(button)

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Slider
        self.slider = Slider(min=0, max=255, value=0, step=1)
        self.slider.bind(value=lambda instance, value: self.change_value(int(value)))
        layout.add_widget(self.slider)

        # Button
        self.button_dropdown_ports = Button(
            text='Select port',
            size=(150, 50),
            size_hint=(None, None),
            pos_hint={'center_x': .5, 'top': 1}
        )
        layout.add_widget(self.button_dropdown_ports)

        # DropDown menu
        self.dropdown_ports = DropDown()
        self.list_available_devices()

        self.button_dropdown_ports.bind(on_release=self.dropdown_ports.open)
        self.button_dropdown_ports.add_widget(self.dropdown_ports)

        Clock.schedule_interval(lambda dt: self.send_control_parameters(), 0.1)

        return layout


if __name__ == '__main__':
    LEDBoardControlApp().run()
