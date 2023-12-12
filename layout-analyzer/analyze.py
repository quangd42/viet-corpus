import sys
from pathlib import Path


finger_map = [0, 1, 2, 3, 3, 4, 4, 5, 6, 7]

frequency = {
    "a": 9.7075,
    "n": 8.7751,
    "o": 8.6019,
    "h": 6.7599,
    "e": 6.0799,
    "i": 5.2891,
    "s": 5.0562,
    "u": 4.9363,
    "t": 4.631,
    "c": 4.465,
    "d": 4.035,
    "g": 3.9874,
    "w": 3.8605,
    "f": 3.841,
    "r": 3.7243,
    "j": 3.5479,
    "m": 2.0457,
    "x": 1.3254,
    "y": 1.2421,
    "v": 1.2119,
    "b": 1.1888,
    "l": 1.1512,
    ",": 1.147,
    "k": 0.9779,
    ".": 0.9329,
    "p": 0.887,
    "q": 0.2729,
    ";": 0.1055,
    "'": 0.0776,
    "-": 0.0721,
    "/": 0.0567,
    "z": 0.0072
}

finger_usage = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0
}

hand_usage = {'LH': 0, 'RH': 0}


genkey_layout_folder = "/Users/quang-dang/Documents/genkey/layouts"
layout = sys.argv[1]


with open(Path(genkey_layout_folder) / layout) as f:
    for current_line_no, line in enumerate(f, 1):
        if 1 < current_line_no < 5:
            print(line, end="")
            char_list = line.split()

            for char in char_list:
                char_usage = round(frequency[char], 4)
                char_pos = char_list.index(char)
                finger_no = finger_map[char_pos]

                finger_usage[finger_no] = round(
                    finger_usage[finger_no] + char_usage, 4)
                if finger_no < 4:
                    hand_usage["LH"] = round(hand_usage["LH"] + char_usage, 4)
                else:
                    hand_usage["RH"] = round(hand_usage["RH"] + char_usage, 4)


print(finger_usage)
print(hand_usage)
