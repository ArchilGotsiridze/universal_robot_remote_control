import rtde.rtde as rtde
from time import sleep
import sys


class RTDESetup():

    def _init_(self, IP, PORT, FREQUENCY):
        self._IP = IP
        self._PORT = PORT
        self._FREQUENCY = FREQUENCY
        self._states = dict()
        self._setp = (
            {'name': "input_double_register_0", 'type': "DOUBLE"},
            {'name': "input_double_register_1", 'type': "DOUBLE"},
            {'name': "input_double_register_2", 'type': "DOUBLE"},
            {'name': "input_double_register_3", 'type': "DOUBLE"},
            {'name': "input_double_register_4", 'type': "DOUBLE"},
            {'name': "input_double_register_5", 'type': "DOUBLE"},
            {'name': "input_bit_registers0_to_31", 'type': "UINT32"},
        )
        self._watchdog = (
            {'watchdog_name': 'input_int_register_0', 'watchdog_type': 'INT32'}
        )
        self._con = 'disconnected'

    def get_names(cfg):
        return [i['name'] for i in cfg]

    def get_types(cfg):
        return [i['type'] for i in cfg]

    def connect(self):
        self.con = rtde.RTDE(self._IP, self._PORT)
        connection_state = self.con.connect()

        while connection_state != 0:
            sleep(0.5)
            connection_state = self.con.connect()
        print("-------------Successfully connected to the robot RTDE-----------\n")

        self.con.get_controller_version()
        return self.con

    def setup_recipes(self):
        self.con.send_output_setup(
            self.get_names(self._states), self.get_types(self._states),
            self.FREQUENCY
        )

        # input packages
        setp = self.con.send_input_setup(
            self.get_names(self._setp), self.get_types(self._setp)
        )
        watchdog = self.con.send_input_setup(
            self.get_names(self._watchdog), self.get_types(self._watchdog)
        )

        setp.input_double_register_0 = 0
        setp.input_double_register_1 = 0
        setp.input_double_register_2 = 0
        setp.input_double_register_3 = 0
        setp.input_double_register_4 = 0
        setp.input_double_register_5 = 0

        setp.input_bit_registers0_to_31 = 0

        watchdog.input_int_register_0 = 0

    def synchronize_data(self, state_name):
        if not self.con.send_start():
            sys.exit()

        state = self.con.receive()

        state_names = ()

        if state_name in state_names:
            return state.state_name
        else:
            return f'state name: {state_name} not mentioned in config'
