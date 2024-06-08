class Utils:
    @staticmethod
    def read_lang_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()