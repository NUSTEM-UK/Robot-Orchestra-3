"""Dictionary of robot IDs for inclusion in other modules.

This system isn't heavily used at present. It remains for legacy reasons, and for
possibly future expansion. It doesn't exactly get in the way.

The dictionaries allow individual D1 minis to be addressed more conveniently than
via their MAC addresses. The module identify as 'skutters' for even deeper legacy
reasons -- have you guessed that we've been hacking on the same codebase for 
several years now? """

instruments = {"00": "skutter_18:FE:34:FD:91:AD",
               "01": "skutter_5C:CF:7F:01:5B:22",
               "02": "skutter_18:FE:34:FD:92:D1",
               "03": "skutter_18:FE:34:F4:D3:BD",
               "04": "skutter_18:FE:34:FD:93:33",
               "05": "skutter_18:FE:34:F4:D6:F4",
               "06": "skutter_5C:CF:7F:01:59:76",
               "07": "skutter_5C:CF:7F:0E:35:2D",
               "08": "skutter_18:FE:34:F4:D0:7B",
               "09": "skutter_18:FE:34:F4:D4:79",
               "10": "skutter_5C:CF:7F:0E:31:16",
               "11": "skutter_5C:CF:7F:0E:2C:EA",
               "12": "skutter_5C:CF:7F:01:59:5B",
               "13": "skutter_5C:CF:7F:19:9A:5A",
               "14": "skutter_18:FE:34:FD:91:B9",
               "D00": "skutter_A0:20:A6:19:94:AB",
               "D01": "skutter_A0:20:A6:19:FB:01",
               "D02": "skutter_A0:20:A6:1A:00:DA",
               "D03": "skutter_A0:20:A6:1A:00:B9",
               "D04": "skutter_A0:20:A6:18:41:52",
               "D05": "skutter_A0:20:A6:1A:74:28",
               "D06": "skutter_A0:20:A6:19:37:A6",
               "D07": "skutter_A0:20:A6:1A:00:0D",
               "D08": "skutter_A0:20:A6:1A:81:D6",
               "D09": "skutter_A0:20:A6:19:46:44",
               "D10": "skutter_A0:20:A6:19:FC:11",
               "D11": "skutter_A0:20:A6:1A:82:15",
               "D12": "skutter_A0:20:A6:19:43:4B",
               "D13": "skutter_A0:20:A6:19:FE:B4",
               "D14": "skutter_A0:20:A6:19:3A:A1",
               "D15": "skutter_A0:20:A6:18:44:FD",
               "D16": "skutter_A0:20:A6:19:3E:24",
               "D17": "skutter_A0:20:A6:19:38:FA",
               "D18": "skutter_A0:20:A6:19:41:32",
               "D19": "skutter_A0:20:A6:19:9E:D5"
               }

ALL = ("00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
       "12", "13", "14", "D00", "D01", "D02", "D03", "D04", "D05", "D06",
       "D07", "D08", "D09", "D10", "D11", "D12", "D13", "D14", "D15", "D16",
       "D17", "D18", "D19")


# Dictionary holds name and corresponding number for each instrument.
# Note: could include multiple robots for a given name.
# (see DRUMS for an example)

PLAYERS = {"ZERO": ("00",),
           "ONE": ("01",),
           "TWO": ("02",),
           "THREE": ("03",),
           "FOUR": ("04",),
           "FIVE": ("05",),
           "SIX": ("06",),
           "SEVEN": ("07",),
           "EIGHT": ("08",),
           "NINE": ("09",),
           "TEN": ("10",),
           "ELEVEN": ("11",),
           "TWELVE": ("12",),
           "THIRTEEN": ("13",),
           "FOURTEEN": ("14",),
           "DZERO": ("D00",),
           "DONE": ("D01",),
           "DTWO": ("D02",),
           "DTHREE": ("D03",),
           "DFOUR": ("D04",),
           "DFIVE": ("D05",),
           "DSIX": ("D06",),
           "DSEVEN": ("D07",),
           "DEIGHT": ("D08",),
           "DNINE": ("D09",),
           "DTEN": ("D10",),
           "DELEVEN": ("D11",),
           "DTWELVE": ("D12",),
           "DTHIRTEEN": ("D13",),
           "DFOURTEEN": ("D14",),
           "DFIFTEEN": ("D15",),
           "DSIXTEEN": ("D16",),
           "DSEVENTEEN": ("D17",),
           "DEIGHTEEN": ("D18",),
           "DNINETEEN": ("D19",),
           "DRUMS": ("00", "01")
           }
