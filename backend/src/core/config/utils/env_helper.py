from backend.src.core.config.utils.enums import EnvFile


def get_env(x):
    return (
        EnvFile.LOCAL.value
        if x in ("linux", "darwin", "windows")
        else EnvFile.DEPLOY.value
    )
