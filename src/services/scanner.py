import os

from models import File


class Scanner:

    @staticmethod
    def scan_dir(directory: str) -> list[File]:
        file_contents: list[File] = []
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(file_path, directory)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        file_contents.append(File(path=rel_path, content=content))
                except (UnicodeDecodeError, OSError):
                    # Skip binary or unreadable files
                    continue
        return file_contents
