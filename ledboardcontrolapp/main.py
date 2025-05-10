__version__ = '0.0.0'

from serial.tools.list_ports import comports

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label

from usb4a import usb


class LEDBoardControlApp(App):

    def list_com_ports(self, label: Label):

        label.text = '\n'.join([device.getDeviceName() for device in usb.get_usb_device_list()])

    def build(self):
        label = Label(text='', font_size=100)
        Clock.schedule_interval(lambda dt: self.list_com_ports(label), 1)
        return label


if __name__ == '__main__':
    LEDBoardControlApp().run()
