# ---------------------------------------------------------
# Assignment 1 - Q8
# Compressed Log Index using Pickle and Zip
# ---------------------------------------------------------

import os
import re
import pickle
import zipfile


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+")


def tokenize(line):
    """
    Extract normalized tokens from a line.
    Tokens are converted to lowercase.
    """

    return [
        token.lower()
        for token in TOKEN_PATTERN.findall(line)
    ]


def build_index(folder_path, zip_name):
    """Build inverted index and compress files."""

    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return

    index = {}

    total_files = 0
    total_lines = 0

    # -----------------------------------------------------
    # Scan every file in the folder
    # -----------------------------------------------------

    for filename in os.listdir(folder_path):

        full_path = os.path.join(
            folder_path,
            filename
        )

        # Only process regular files
        if not os.path.isfile(full_path):
            continue

        total_files += 1

        try:

            with open(
                full_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                for line_number, line in enumerate(
                    file,
                    start=1
                ):

                    total_lines += 1

                    tokens = tokenize(line)

                    # Use a set so a token appearing multiple
                    # times on the same line is stored once.
                    for token in set(tokens):

                        if token not in index:
                            index[token] = []

                        index[token].append(
                            (filename, line_number)
                        )

        except OSError:
            # Ignore files that cannot be read
            continue

    # -----------------------------------------------------
    # Save index using pickle
    # -----------------------------------------------------

    pickle_path = os.path.join(
        folder_path,
        "index.pkl"
    )

    with open(pickle_path, "wb") as file:
        pickle.dump(index, file)

    # -----------------------------------------------------
    # Create ZIP archive
    # -----------------------------------------------------

    with zipfile.ZipFile(
        zip_name,
        "w",
        zipfile.ZIP_DEFLATED
    ) as archive:

        # Add original log files
        for filename in os.listdir(folder_path):

            full_path = os.path.join(
                folder_path,
                filename
            )

            if os.path.isfile(full_path):

                # Do not include an existing zip file
                if os.path.abspath(full_path) == os.path.abspath(
                    zip_name
                ):
                    continue

                archive.write(
                    full_path,
                    arcname=filename
                )

    print(f"FILES {total_files}")
    print(f"LINES {total_lines}")
    print(f"TOKENS {len(index)}")


def search_index(pickle_path, queries):
    """Load pickle index and search for tokens."""

    try:

        with open(pickle_path, "rb") as file:
            index = pickle.load(file)

    except FileNotFoundError:
        print("Pickle index not found.")
        return

    for query in queries:

        token = query.lower()

        matches = index.get(token, [])

        print(f"{token}:")

        for filename, line_number in matches:
            print(f"{filename}:{line_number}")


def main():

    mode = input().strip().upper()

    # -----------------------------------------------------
    # BUILD mode
    # -----------------------------------------------------

    if mode == "BUILD":

        parts = input().split()

        if len(parts) != 2:
            print("Invalid BUILD format.")
            return

        folder_path = parts[0]
        zip_name = parts[1]

        build_index(
            folder_path,
            zip_name
        )

    # -----------------------------------------------------
    # SEARCH mode
    # -----------------------------------------------------

    elif mode == "SEARCH":

        parts = input().split()

        if len(parts) < 2:
            print("Invalid SEARCH format.")
            return

        pickle_path = parts[0]
        q = int(parts[1])

        queries = []

        for _ in range(q):
            queries.append(input().strip())

        search_index(
            pickle_path,
            queries
        )

    else:

        print("Invalid mode. Use BUILD or SEARCH.")


if __name__ == "__main__":
    main()