from acrobot.envs.default import DefaultSettings


class DevelopmentSettings(DefaultSettings):
    def __init__(self):
        super().__init__()
        self.ENV = "dev"
