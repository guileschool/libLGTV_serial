# -*- coding: utf-8 -*-

import serial
import os
import time
import tempfile
from filelock import FileLock
# from pprint import pprint


actual_codes = {}
common_codes = {
    'poweroff'      : b"ka 00 00",
    'poweron'       : b"ka 00 01",
    'powerstatus'   : b"ka 00 ff",

    'aspect43'      : b"kc 00 01",
    'aspect169'     : b"kc 00 02",
    'aspectstatus'  : b"kc 00 ff",

    'mute'          : b"ke 00 00",
    'unmute'        : b"ke 00 01",
    'mutestatus'    : b"ke 00 ff",

    'volumestatus'  : b"kf 00 ff",
    'volumelevel01' : b"kf 00 01",
    'volumelevel02' : b"kf 00 02",
    'volumelevel03' : b"kf 00 03",
    'volumelevel04' : b"kf 00 04",
    'volumelevel05' : b"kf 00 05",
    'volumelevel06' : b"kf 00 06",
    'volumelevel07' : b"kf 00 07",
    'volumelevel08' : b"kf 00 08",
    'volumelevel09' : b"kf 00 09",
    'volumelevel10' : b"kf 00 0a",
    'volumelevel11' : b"kf 00 0b",
    'volumelevel12' : b"kf 00 0c",
    'volumelevel13' : b"kf 00 0d",
    'volumelevel14' : b"kf 00 0e",
    'volumelevel15' : b"kf 00 0f",
    'volumelevel16' : b"kf 00 10",
    'volumelevel17' : b"kf 00 11",
    'volumelevel18' : b"kf 00 12",
    'volumelevel19' : b"kf 00 13",
    'volumelevel20' : b"kf 00 14"
}
actual_codes['LK450_etc'] = common_codes.copy()
actual_codes['LK450_etc'].update({
    'inputdigitalantenna'   : b"xb 00 00",
    'inputdigitalcable'     : b"xb 00 01",
    'inputanalogantenna'    : b"xb 00 10",
    'inputanalogcable'      : b"xb 00 11",
    'inputav1'              : b"xb 00 20",
    'inputav2'              : b"xb 00 21",
    'inputcomp1'            : b"xb 00 40",
    'inputcomp2'            : b"xb 00 41",
    'inputrgbpc'            : b"xb 00 60",
    'inputhdmi1'            : b"xb 00 90",
    'inputhdmi2'            : b"xb 00 91",
    'inputhdmi3'            : b"xb 00 92",
    'inputhdmi4'            : b"xb 00 93",
    'inputstatus'           : b"xb 00 ff"
})
actual_codes['PJ250_etc'] = common_codes.copy()
actual_codes['PJ250_etc'].update({
    'inputdtvantenna'       : b"xb 00 00",
    'inputdtvcable'         : b"xb 00 01",
    'inputanalogantenna'    : b"xb 00 10",
    'inputanalogcable'      : b"xb 00 11",
    'inputav1'              : b"xb 00 20",
    'inputav2'              : b"xb 00 21",
    'inputcomp1'            : b"xb 00 40",
    'inputcomp2'            : b"xb 00 41",
    'inputrgbpc'            : b"xb 00 60",
    'inputhdmi1'            : b"xb 00 90",
    'inputhdmi2'            : b"xb 00 91",
    'inputhdmi3'            : b"xb 00 92",
    'inputstatus'           : b"xb 00 ff"
})
actual_codes['LE5300_etc'] = common_codes.copy()
actual_codes['LE5300_etc'].update({
    'inputdtv'              : b"xb 00 00",
    'inputanalogantenna'    : b"xb 00 10",
    'inputanalogcable'      : b"xb 00 11",
    'inputav1'              : b"xb 00 20",
    'inputav2'              : b"xb 00 21",
    'inputcomp'             : b"xb 00 40",
    'inputrgbpc'            : b"xb 00 60",
    'inputhdmi1'            : b"xb 00 90",
    'inputhdmi2'            : b"xb 00 91",
    'inputhdmi3'            : b"xb 00 92",
    'inputhdmi4'            : b"xb 00 93",
    'inputstatus'           : b"xb 00 ff"
})
actual_codes['LC7D_etc'] = common_codes.copy()
actual_codes['LC7D_etc'].update({
    'inputdtvantenna'       : b"xb 00 00",
    'inputdtvcable'         : b"xb 00 01",
    'inputanalogantenna'    : b"xb 00 10",
    'inputanalogcable'      : b"xb 00 11",
    'inputav1'              : b"xb 00 20",
    'inputav2'              : b"xb 00 21",
    'inputcomp1'            : b"xb 00 40",
    'inputcomp2'            : b"xb 00 41",
    'inputrgbpc'            : b"xb 00 60",
    'inputhdmi1'            : b"xb 00 90",
    'inputhdmi2'            : b"xb 00 91",
    'inputstatus'           : b"xb 00 ff"
})
actual_codes['01C_etc'] = common_codes.copy()
actual_codes['01C_etc'].update({
    'inputav'       : b"kb 00 02",
    'inputcomp1'    : b"kb 00 04",
    'inputcomp2'    : b"kb 00 05",
    'inputrgbdtv'   : b"kb 00 06",
    'inputrgbpc'    : b"kb 00 07",
    'inputhdmidtv'  : b"kb 00 08",
    'inputhdmipc'   : b"kb 00 09",
    'inputstatus'   : b"kb 00 ff"
})
actual_codes['02C_etc'] = common_codes.copy()
actual_codes['02C_etc'].update({
    'inputav'       : b"kb 00 02",
    'inputcomp1'    : b"kb 00 04",
    'inputcomp2'    : b"kb 00 05",
    'inputrgbpc'    : b"kb 00 07",
    'inputhdmidtv'  : b"kb 00 08",
    'inputhdmipc'   : b"kb 00 09",
    'inputstatus'   : b"kb 00 ff"
})
actual_codes['LW5700_etc'] = common_codes.copy()
actual_codes['LW5700_etc'].update({
    'lowpower0'           : b"jq 00 00",
    'lowpower1'           : b"jq 00 01",
    'lowpower2'           : b"jq 00 02",
    'lowpower3'           : b"jq 00 03",
    'lowpowerauto'        : b"jq 00 04",
    'lowpowerscreenoff'   : b"jq 00 05",
    'lowpowerstatus'      : b"jq 00 ff",

    'inputrgbpc'          : b"kb 00 07",
    'inputhdmi1'          : b"xb 00 90",
    'inputhdmi2'          : b"xb 00 91",
    'inputstatus'         : b"kb 00 ff",

    '3Doff'               : b"xt 00 01 00 00 00",
    '3Dsbslr'             : b"xt 00 00 01 00 00", #3D On (Side-by-Side, left-right)
    '3Dtbud'              : b"xt 00 00 00 00 00", #3D On (Top-Bottom, up-down)

    'screenmuteoff'       : b"kd 00 01", #Screen Mute On (Picture Off). TV will NOT show OSD
    'screenmutevideo'     : b"kd 00 10", #Video Out Mute On (Video Off). TV will show OSD
    'screenmuteon'        : b"kd 00 00", #Video-Out Mute Off (Video On) & Screen Mute Off (Picture On)
    'screenmutestatus'    : b"kd 00 ff",

#    'SendRawIR'           : b"mc 00  ", #Send IR Keycode(0-FF)
    'ir_MonitorOn'        : b"mc 00 c4", #Same as Power on
    'ir_MonitorOff'       : b"mc 00 c5", #Same as Power off
    'ir_Mute'             : b"mc 00 09",
    'ir_VolumeUp'         : b"mc 00 02",
    'ir_VolumeDown'       : b"mc 00 03",
    'ir_Play'             : b"mc 00 b0",
    'ir_Pause'            : b"mc 00 ba",
    'ir_Stop'             : b"mc 00 b1",
    'ir_Forward'          : b"mc 00 8e",
    'ir_Rewind'           : b"mc 00 8f",
    'ir_Record'           : b"mc 00 bd",
    'ir_Right'            : b"mc 00 06",
    'ir_Left'             : b"mc 00 07",
    'ir_Up'               : b"mc 00 40",
    'ir_Down'             : b"mc 00 41",
    'ir_Enter'            : b"mc 00 44",
    'ir_Exit'             : b"mc 00 5b",
    'ir_Return'           : b"mc 00 28",
    'ir_QMenu'            : b"mc 00 45",
    'ir_Info'             : b"mc 00 aa",
    'ir_Menu'             : b"mc 00 43",
    'ir_Premium'          : b"mc 00 59",
    'ir_3D'               : b"mc 00 dc",
    'ir_AVMode'           : b"mc 00 30",
    'ir_EnergySavingMode' : b"mc 00 95",
    'ir_Ratio'            : b"mc 00 79",
    'ir_SleepTimer'       : b"mc 00 0e",
    'ir_Aspect43'         : b"mc 00 76",
    'ir_Aspect169'        : b"mc 00 77",
    'ir_Teletext'         : b"mc 00 20",
    'ir_TOption'          : b"mc 00 21",
    'ir_Simplink'         : b"mc 00 7e"
})

reverse_code_map = {
    'LK450_etc': ('LV2500', 'LV2520', 'LV3500', 'LV3520', 'LK330', 'LK430', 'LK450',
                    'LK520', 'PW340', 'PW350', 'PW350U', 'PW350R', 'LH20', 'LH200C',
                    'LH30', 'LF11', 'LF21', 'LU55', 'CL10', 'CL20', 'CL11', 'PZ200'),
    'PJ250_etc': ('PJ250', 'PK250', 'PK280', 'PK290', 'PJ340', 'PJ350', 'PK350',
                    'PKPK340', 'PK540', 'PJ550', 'PK550', 'PJ350C', 'PK550C'),
    'LC7D_etc': ('LC7D', 'LC7DC', 'PC5D', 'PC5DC'),
    'LE5300_etc': ('LE5300', 'LE5500', 'LE7300', 'LE530C', 'LD420', 'LD450', 'LD450C',
                    'LD520', 'LD520C', 'LD630', 'LW5600', 'LW6500', 'LW9800',
                    'LV3700', 'LV5400', 'LV5500', 'LV9500', 'LK530', 'LK550', 'PZ750',
                    'PZ950', 'PZ950U'),
    '01C_etc': ('01C', '01C-BA'),
    '02C_etc': ('02C', '02C-BA', '02C-BH'),
    'LW5700_etc': ('LW575', 'LW575S')
}
all_codes = {}
# populate model suffix lookup hash
for suffix_codes, suffixes in reverse_code_map.items():
    for suffix in suffixes:
        all_codes[suffix] = actual_codes[suffix_codes]


class LGTV:
    def __init__(self, model, port):
        self.model = model.upper()

        # Ignore digits which indicate the TV's screen size
        if model.startswith('M'):
            self.codes = all_codes[self.model[3:]]  # Ignore the leading 'M' too
        else:
            self.codes = all_codes[self.model[2:]]

        self.port = port
        self.connection = None
        self.toggles = {
            'togglepower': ('poweron', 'poweroff'),
            'togglemute': ('mute', 'unmute'),
        }
        self.debounces = {}

    #this next line sets up the serial port to allow for communication
    #and opens the serial port you may need to change
    #ttyS0 to S1, S2, ect. The rest shouldn't need to change.
    def get_port(self):
        return serial.Serial(self.port, 9600, 8, serial.PARITY_NONE,
                serial.STOPBITS_ONE, xonxoff=0, rtscts=0, timeout=1)

    def get_port_ensured(self):
        ser = None
        while ser == None:
            try:
                ser = self.get_port()
            except serial.serialutil.SerialException:
                time.sleep(0.07)
        return ser

    def status_code(self, code):
        return code[:-2] + b'ff'

    def lookup(self, command):
        if command.startswith('toggle'):
            states = self.toggles.get(command)
            state_codes = (self.codes[states[0]], self.codes[states[1]])
            return self.toggle(self.status_code(state_codes[0]), state_codes)
        elif command.endswith('up'):
            key = command[:-2] + 'level'
            return self.increment(self.status_code(self.codes[key]))
        elif command.endswith('down'):
            key = command[:-4] + 'level'
            return self.decrement(self.status_code(self.codes[key]))
        else:
            return self.codes[command]

    # Returns None on error, full response otherwise
    def query_full(self, code):
        self.connection.write(code + b'\r')
        response = self.connection.read(10)
        if self.is_success(response):
            return response

    def query_data(self, code):
        response = self.query_full(code)
        return response and response[-3:-1]

    # returns None on error, 2-char status for status commands, and True otherwise
    def query(self, command):
        if self.is_status(command):
            return self.query_data(self.lookup(command))
        else:
            return self.query_full(self.lookup(command)) and True

    def is_status(self, command):
        return command.endswith('status') or command.endswith('level')

    def is_success(self, response):
        return response[-5:-3] == b'OK'

    def hex_bytes_delta(self, hex_bytes, delta):
        return bytearray(hex(int(hex_bytes, 16) + delta)[2:4], 'ascii')

    def delta(self, code, delta):
        level = self.query_data(code)
        return code[0:6] + self.hex_bytes_delta(level, delta)

    def increment(self, code):
        return self.delta(code, +1)

    def decrement(self, code):
        return self.delta(code, -1)

    def toggle(self, code, togglecommands):
        level = self.query_data(code)
        toggledata = (togglecommands[0][-2:], togglecommands[1][-2:])
        data = toggledata[0]
        if level == toggledata[0]:
            data = toggledata[1]
        return code[0:6] + data



# ======= These are the methods you'll most probably want to use ==========

    def send(self, command):
        if command in self.debounces:
            wait_secs = self.debounces[command]
            if self.connection == None:
                self.connection = self.get_port()
            lock_path = os.path.join(tempfile.gettempdir(), '.' + command + '_lock')
            with FileLock(lock_path, timeout=0) as lock:
                response = self.query(command)
                time.sleep(wait_secs)
        else:
            if self.connection == None:
                self.connection = self.get_port_ensured()
            response = self.query(command)
        self.connection.close()
        return response

    def available_commands(self):
        print("Some features (such as a 4th HDMI port) might not be available for your TV model")
        commands = self.codes.copy()
        commands.update(self.toggles)
        for command in commands.keys():
            code = commands[command]
            if command.endswith('level'):
                print("%s : %s" % (command[:-5] + 'up', code[:-2] + b'??'))
                print("%s : %s" % (command[:-5] + 'down', code[:-2] + b'??'))
            else:
                print("{0} : {1}".format(command, code))

    def add_toggle(self, command, state0, state1):
        self.toggles['toggle' + command] = (state0, state1)

    def debounce(self, command, wait_secs=0.5):
        self.debounces[command] = wait_secs

# end class LGTV
