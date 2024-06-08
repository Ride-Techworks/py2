import re
import os


class Utils:
    @staticmethod
    def read_lang_file(file_path):
        if os.path.exists(file_path) == False:
            raise Exception(f"File {file_path} not found.")

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def has_interpolation(text):
        return re.search(r"#\{[a-zA-Z0-9_]+\}", text)

    def replace_interpolation(text, variables):
        for key in variables:
            text = text.replace(f"#{{{key}}}", str(variables[key]))

        return text
