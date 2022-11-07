import rtde.rtde as rtde
from time import sleep
import sys


class RTDESetup:

    def __init__(self, IP, PORT, frequency=125):
        self._IP = IP
        self._PORT = PORT
        self._frequency = frequency
        self.states = []
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
            {'name': 'input_int_register_0', 'type': 'INT32'},
        )
        self._con = 'disconnected'

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        if type(frequency) == int and frequency <= 500 and frequency > 0:
            self._frequency = frequency
        else:
            print("Value of frequency must be integer between 0 and 500")

    def _get_names(cfg):
        return [i['name'] for i in cfg]

    def _get_types(cfg):
        return [i['type'] for i in cfg]

    def connect(self):
        self._con = rtde.RTDE(self._IP, self._PORT)
        connection_state = self._con.connect()
        while connection_state != 0:
            sleep(0.5)
            connection_state = self._con.connect()
        print("-------------Successfully connected to the robot RTDE-----------\n")

        self._con.get_controller_version()
        return self._con

    def setup_recipes(self):

        self._con.send_output_setup(
            RTDESetup._get_names(self.states),
            RTDESetup._get_types(self.states),
            self._frequency
        )

        # input packages
        setp = self._con.send_input_setup(
            RTDESetup._get_names(self._setp), RTDESetup._get_types(self._setp)
        )
        watchdog = self._con.send_input_setup(
            RTDESetup._get_names(
                self._watchdog), RTDESetup._get_types(self._watchdog)
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
        if not self._con.send_start():
            sys.exit()

        state = self._con.receive()

        state_names = RTDESetup._get_names(self.states)

        if state_name in state_names:
            # return state.actual_TCP_pose
            return getattr(state, state_name)
        else:
            return f'state name: {state_name} not mentioned in config'
