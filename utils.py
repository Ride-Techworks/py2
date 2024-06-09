import re
import os


class Utils:
    @staticmethod
    def read_lang_file(file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found.")

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def has_interpolation(text: str) -> bool:
        return re.search(r"#\{[a-zA-Z0-9_]+\}", text)

    @staticmethod
    def replace_interpolation(text: str, variables: dict) -> str:
        for key, value in variables.items():
            text = text.replace(f"#{{{key}}}", str(value))

        return text
