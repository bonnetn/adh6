# coding=utf-8
import os


def is_development_environment():
    return os.environ.get("ENVIRONMENT") == "dev"
