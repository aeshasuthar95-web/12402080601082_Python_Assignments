
# Assignment 1 - Q2
import re


class TrieNode:
    """Represents one node of the Trie."""

    def __init__(self):
        # Dictionary stores character -> next TrieNode
        self.children = {}

        # True if a banned word ends at this node
        self.is_end = False


class Trie:
    """Trie used to efficiently store and search banned words."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Insert a banned word into the Trie."""

        node = self.root

        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_end = True

    def contains_banned_word(self, password):
        """
        Check whether any banned word occurs as a
        contiguous substring of the password.
        """

        password = password.lower()

        # Start checking from every character
        for start in range(len(password)):

            node = self.root

            # Follow the Trie from this position
            for end in range(start, len(password)):

                char = password[end]

                # Character is not present in Trie,
                # so no banned word can continue here.
                if char not in node.children:
                    break

                node = node.children[char]

                # A complete banned word was found
                if node.is_end:
                    return True

        return False


def has_required_characters(password):
    """
    Check whether password contains:
    - at least one lowercase letter
    - at least one uppercase letter
    - at least one digit
    - at least one special symbol from $#@
    """

    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False

    for char in password:

        if char.islower():
            has_lower = True

        elif char.isupper():
            has_upper = True

        elif char.isdigit():
            has_digit = True

        elif char in "$#@":
            has_special = True

    return has_lower and has_upper and has_digit and has_special


def has_repeated_character(password):
    """
    Check whether the same character occurs
    more than 3 times consecutively.

    Example:
    AAAA1@b -> True
    AA1@bb -> False
    """

    if not password:
        return False

    consecutive_count = 1

    for i in range(1, len(password)):

        if password[i] == password[i - 1]:
            consecutive_count += 1

            # More than 3 consecutive occurrences
            if consecutive_count > 3:
                return True

        else:
            # Character changed, so reset the count
            consecutive_count = 1

    return False


def classify_password(password, banned_trie):
    """
    Classify a password according to the assignment rules.
    """

    # -----------------------------------------------------
    # Step 1: Check length
    # -----------------------------------------------------
    if len(password) < 6 or len(password) > 12:
        return "WEAK_LENGTH"

    # -----------------------------------------------------
    # Step 2: Check required character pattern
    # -----------------------------------------------------
    if not has_required_characters(password):
        return "WEAK_PATTERN"

    # -----------------------------------------------------
    # Step 3: Check repeated characters
    # -----------------------------------------------------
    if has_repeated_character(password):
        return "WEAK_PATTERN"

    # -----------------------------------------------------
    # Step 4: Check banned words
    # -----------------------------------------------------
    if banned_trie.contains_banned_word(password):
        return "COMPROMISED"

    # If all checks pass
    return "STRONG"


def main():

    # -----------------------------------------------------
    # Read number of banned words
    # -----------------------------------------------------
    b = int(input().strip())

    if not (1 <= b <= 10000):
        raise ValueError("Number of banned words must be between 1 and 10000.")

    # Create Trie
    banned_trie = Trie()

    # -----------------------------------------------------
    # Read and insert banned words
    # -----------------------------------------------------
    for _ in range(b):
        word = input().strip()

        if word:
            banned_trie.insert(word)

    # -----------------------------------------------------
    # Read number of passwords
    # -----------------------------------------------------
    n = int(input().strip())

    if not (1 <= n <= 100000):
        raise ValueError("Number of passwords must be between 1 and 100000.")

    # Process every password
    
    for index in range(1, n + 1):

        password = input().rstrip("\n")

        result = classify_password(password, banned_trie)

        # Required output format:
        # password_index: classification
        print(f"{index}: {result}")


# Program starts here

if __name__ == "__main__":
    main()