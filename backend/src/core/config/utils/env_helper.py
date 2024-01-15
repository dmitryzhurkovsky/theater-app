from src.core.enums import EnvFile


def get_env(x: str) -> str:
    return EnvFile.LOCAL.value if x in ("linux", "darwin", "windows") else EnvFile.PROD.value
