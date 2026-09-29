import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def res_path(name):
    """Абсолютный путь к файлу ресурса рядом с кодом (работает и на ПК, и на Android)."""
    return os.path.join(BASE_DIR, name)
