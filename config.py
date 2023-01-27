import os


class Config:
    # Set this otherwise we get annoying errors
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Rather than just defining this as a variable (as above, use a property)
    # Property lets Python treat it as a static value but we actually run a function when it's accessed
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # Get the environment variable from .env
        value = os.environ.get("DATABASE_URL")
        if not value:
            # if it doesn't exist, raise an error, we can't run the app
            raise ValueError("No DATABASE_URL in environment variable")
        # otherwise, return
        return value


app_config = Config()
