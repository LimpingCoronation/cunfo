from pathlib import Path
from time import sleep, time

SECONDS_IN_DAY = 86400


def file_cleaner(directory: Path, days_before_deleting: int):
    while True:
        sleep(10)
        for x in directory.iterdir():
            if x.is_file():
                if round(time()-x.stat().st_mtime) > SECONDS_IN_DAY * days_before_deleting:
                    try:
                        x.unlink()
                    except Exception:
                        print(f"Не получилось удалить файл: {x}")
