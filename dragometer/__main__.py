#!/usr/bin/env python

import sys
from os import getcwd, path

from PyQt5.QtWidgets import QApplication

from dragometer.dragometer import Dragometer


def main():
    if len(sys.argv) != 2:
        print('Usage: ' + sys.argv[0] + ' <sumo application>')
        sys.exit(1)

    sys.path.append(getcwd())

    app = QApplication(sys.argv)
    main = Dragometer(path.splitext(sys.argv[1])[0])

    main.show()
    app.exec_()
