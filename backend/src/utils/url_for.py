def url_for(*arg, **kwargs):
    """
    Get url for route
    """
    if not hasattr(url_for, "app"):
        from src.main import app

        url_for.app = app
    return url_for.app.url_path_for(*arg, **kwargs)
