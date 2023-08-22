from starlette.config import Config


class Settings:
    USERNAME: str = "user"
    PASSWORD: str = "pass"
    VERSION = "0.1.0"
    TITLE = "asiayo testing"

    def __new__(cls, *args, **kwargs):
        config = Config(".env")
        obj = super(Settings, cls).__new__(cls, *args, **kwargs)
        for attr_name in dir(cls):
            if not attr_name.startswith("__") and not callable(getattr(cls, attr_name)):
                setattr(obj, attr_name, config.get(attr_name, default=getattr(cls, attr_name)))
        return obj


settings = Settings()
