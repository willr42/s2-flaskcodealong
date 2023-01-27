import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        value = os.environ.get("DATABASE_URL")
        if not value:
            raise ValueError("No DATABASE_URL in environment variable")
        return value


app_config = Config()
