#!/usr/local/bin/python3

import base
import sys

print(int(sys.argv[2]))
base.write_speed(base.AXIS[sys.argv[1]], int(sys.argv[2]))
