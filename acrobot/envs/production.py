from acrobot.envs.default import DefaultSettings


class ProductionSettings(DefaultSettings):
    def __init__(self):
        super().__init__()
        self.ENV = "prod"
        DB_PASSWORD = ""
        DB_USER = "postgres"
        DB_NAME = "acrobot"
        DB_HOST = ""
        self.SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
