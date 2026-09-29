"""Общий компактный словарь: грузится один раз и хранится как bytes (~30 МБ вместо ~200 МБ у set)."""
from paths import res_path

_cache = {}


class WordSet:
    def __init__(self, data):
        self._data = data  # b"\nслово1\nслово2\n...\n"

    def __contains__(self, word):
        if not isinstance(word, str) or not word or "\n" in word:
            return False
        return ("\n" + word + "\n").encode("utf-8") in self._data

    def __len__(self):
        return self._data.count(b"\n") - 1


def load_words(filename="words_dictionary.txt", fallback=()):
    if filename in _cache:
        return _cache[filename]
    ws = None
    try:
        import os
        base = filename[:-4] if filename.endswith(".txt") else filename
        chunks = []
        i = 1
        # словарь может быть разрезан на части: words_dictionary_1.txt, _2.txt, ...
        while os.path.exists(res_path("%s_%d.txt" % (base, i))):
            with open(res_path("%s_%d.txt" % (base, i)), "rb") as f:
                chunks.append(f.read().strip(b"\r\n"))
            i += 1
        if not chunks:
            with open(res_path(filename), "rb") as f:
                chunks.append(f.read())
        raw = b"\n".join(chunks)
        # Файл уже нормализован (нижний регистр, е вместо ё, переводы строк LF)
        if b"\r" in raw or raw != raw.lower():
            text = raw.decode("utf-8").replace("\r", "").lower().replace("ё", "е")
            raw = "\n".join(ln.strip() for ln in text.split("\n") if ln.strip()).encode("utf-8")
        raw = raw.strip(b"\n")
        if raw:
            ws = WordSet(b"\n" + raw + b"\n")
    except Exception as e:
        print(f"[Warning] Ошибка загрузки {filename}: {e}")
    if ws is None:
        ws = WordSet(("\n" + "\n".join(fallback) + "\n").encode("utf-8"))
    _cache[filename] = ws
    return ws
