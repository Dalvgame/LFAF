from regex_parser import RegexParser
from generator import Generator

class RegexGenerator:

    def generate(self, regex):
        parser = RegexParser(regex)
        root = parser.parse()
        generator = Generator()
        return generator.generate(root)