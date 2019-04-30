# coding=utf-8
import sys

sys._called_from_test = True

import main

main.init(main, testing=True)
app = main.app

app.app.config["TESTING"] = True
