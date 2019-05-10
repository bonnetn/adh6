# coding=utf-8
import sys

sys._called_from_test = True  # This will make sure we don't call 'init' anywhere else.

import main

app = main.init(testing=True)

app.app.config["TESTING"] = True
