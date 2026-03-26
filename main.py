from regex_generator import RegexGenerator
from processing_logger import ProcessingLogger

def main():
    with open("input.txt", "r", encoding="utf-8") as f:
        regexes = [line.strip() for line in f if line.strip()]

    generator = RegexGenerator()

    with open("output.txt", "w", encoding="utf-8") as out:
        for regex in regexes:
            out.write(f"Regex: {regex}\n")

            for _ in range(5):
                result = generator.generate(regex)
                out.write(f"  -> {result}\n")

            out.write("\nProcessing steps:\n")
            steps = ProcessingLogger.explain(regex)
            for step in steps:
                out.write("  " + step + "\n")

            out.write("\n----------------------\n\n")

    print("Generation complete")

if __name__ == "__main__":
    main()