import os


def isDevelopmentEnvironment():
    return os.environ.get("ENVIRONMENT") == "dev"
