import csv

class Translator:
    translations = {}

    def load_translation_file(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file, delimiter=';', quotechar='"')

            for row in csv_reader:
                self.translations[row[0]] = row[1]

    def translate_text(self, text_str):
        return self.translations.get(text_str, text_str)