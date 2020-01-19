from acrobot.envs.default import DefaultSettings


class StageSettings(DefaultSettings):
    def __init__(self):
        super().__init__()
        self.ENV = "stage"
