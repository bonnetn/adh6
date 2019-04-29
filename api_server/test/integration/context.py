# coding=utf-8
import main

main.init(main, testing=True)
app = main.app

app.app.config["TESTING"] = True

