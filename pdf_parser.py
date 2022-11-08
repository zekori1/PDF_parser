import json
import fitz
import re
from hamcrest import assert_that, has_entries


class PdfList:
    def __init__(self, path):
        self.path: str = path
        self.text: str = self.__get_text()
        self.properties: dict = self.__get_properties()

    def get_text(self):
        return self.text

    def get_properties(self):
        return self.properties

    def __get_text(self):
        text = ''
        with fitz.open(self.path) as doc:
            for elem in doc.pages():
                text += elem.get_text().strip()
        return text

    def __get_properties(self):
        text = re.findall(r'(\w+): ((?:\w+\s)+)', self.get_text())
        properties = {key: value.strip() for key, value in text}
        return properties

    def to_txt(self, path):
        with open(path, 'w') as file:
            for key, value in self.properties.items():
                file.write(f'{key}: {value}\n')

    def to_json(self, path):
        with open(path, "w") as file:
            json.dump(self.properties, file, indent=2)

    def __eq__(self, other):
        assert_that(self.properties, has_entries(other.properties))
        return self.properties == other.properties


if __name__ == '__main__':
    pdf_1 = PdfList('./files/test_task.pdf')
    pdf_2 = PdfList('./files/test_task.pdf')

    print(pdf_1.properties)
    print(pdf_1.text)
    pdf_1.to_txt('pdf_to_txt.txt')
    pdf_1.to_json('pdf_to_json.json')

    print(pdf_2.properties)
    print(pdf_2.text)
    pdf_2.to_txt('pdf_to_txt.txt')
    pdf_2.to_json('pdf_to_json.json')

    print(pdf_1 == pdf_2)

# a.to_json('asdsd.json')
# print(a.get_text())
# print(a.get_properties())
