from acrobot.envs.default import DefaultSettings


class ProductionSettings(DefaultSettings):
    def __init__(self):
        super().__init__()
        self.ENV = "prod"
