import os

from acrobot.envs.development import DevelopmentSettings
from acrobot.envs.stage import StageSettings
from acrobot.envs.production import ProductionSettings


def setup_environment(app):
    # Create Environment objects which specify
    # all the things you want to configure differently in each env
    environment = os.environ.get("ENV", "dev")

    if environment == "dev":
        settings = DevelopmentSettings()
    elif environment == "stage":
        settings = StageSettings()
    elif environment == "prod":
        settings = ProductionSettings()
    else:
        raise Exception(f"Could not load environment '{environment}'")

    app.config.from_object(settings)
