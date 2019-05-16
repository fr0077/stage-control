#!/usr/local/bin/python3

import base
import sys

base.set_communication_speed(base.AXIS[sys.argv[1]], sys.argv[2])

