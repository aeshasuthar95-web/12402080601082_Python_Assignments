import re
from collections import defaultdict

def main():
    filename = input("Enter text file path: ").strip()
    pattern = re.compile(r'(?<![\w.+-])[\w.+-]+@[\w.-]+\.(?:com|edu|org)\b')
    emails = defaultdict(set)

    try:
        with open(filename, encoding="utf-8") as f:
            for line in f:
                for email in pattern.findall(line):
                    domain = email.split("@", 1)[1]
                    emails[domain].add(email)

        for domain in sorted(emails):
            values = sorted(emails[domain])
            print(domain, len(values), values[0])

    except FileNotFoundError:
        print("File not found.")

if __name__ == "__main__":
    main()