import re


class Utils:
    @staticmethod
    def read_lang_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def has_interpolation(text):
        return re.search(r"#\{[a-zA-Z0-9_]+\}", text)

    def replace_interpolation(text, variables):
        for key in variables:
            text = text.replace(f"#{{{key}}}", str(variables[key]))

        return text
