# ---------------------------------------------------------
# Assignment 1 - Q3
# Recursive Expression Engine with Memoization
# Python 3.10+
# ---------------------------------------------------------

import re


class ExpressionEngine:
    def __init__(self, variables):
        # Store all variable definitions
        self.variables = variables

        # Memoization dictionary.
        # Once a variable is evaluated, its value is stored here.
        self.memo = {}

        # Variables currently being evaluated.
        # Used for detecting circular dependencies.
        self.visiting = set()

        # Regular expression for valid variable names
        self.variable_pattern = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

    def tokenize(self, expression):
        """
        Convert an expression into tokens.

        Supported:
        - non-negative integers
        - variable names
        - +, -, *
        - (, )
        """

        tokens = []
        i = 0

        while i < len(expression):

            # Ignore spaces
            if expression[i].isspace():
                i += 1
                continue

            # Integer
            if expression[i].isdigit():
                j = i

                while j < len(expression) and expression[j].isdigit():
                    j += 1

                tokens.append(("NUMBER", expression[i:j]))
                i = j
                continue

            # Variable name
            if expression[i].isalpha() or expression[i] == "_":
                j = i

                while (
                    j < len(expression)
                    and (expression[j].isalnum() or expression[j] == "_")
                ):
                    j += 1

                tokens.append(("VARIABLE", expression[i:j]))
                i = j
                continue

            # Operators and parentheses
            if expression[i] in "+-*()":
                tokens.append((expression[i], expression[i]))
                i += 1
                continue

            # Anything else is invalid
            raise ValueError("Invalid character in expression.")

        return tokens

    def evaluate_variable(self, name):
        """
        Evaluate a variable recursively.

        Memoization prevents the same variable from being
        calculated repeatedly.
        """

        # If already calculated, return stored value
        if name in self.memo:
            return self.memo[name]

        # Variable doesn't exist
        if name not in self.variables:
            raise ValueError("Unknown variable.")

        # If the variable is already being evaluated,
        # we have found a cycle.
        if name in self.visiting:
            raise RuntimeError("CYCLE")

        # Mark this variable as currently being evaluated
        self.visiting.add(name)

        try:
            tokens = self.tokenize(self.variables[name])

            # Parser starts from the first token
            value, position = self.parse_expression(tokens, 0)

            # All tokens must have been consumed
            if position != len(tokens):
                raise ValueError("Invalid expression.")

            # Store result for future use
            self.memo[name] = value

            return value

        finally:
            # Remove variable after evaluation
            self.visiting.remove(name)

    def parse_expression(self, tokens, position):
        """
        Parse addition and subtraction.

        expression = term ((+ | -) term)*
        """

        value, position = self.parse_term(tokens, position)

        while position < len(tokens):

            operator = tokens[position][0]

            if operator not in ("+", "-"):
                break

            position += 1

            right_value, position = self.parse_term(tokens, position)

            if operator == "+":
                value += right_value
            else:
                value -= right_value

        return value, position

    def parse_term(self, tokens, position):
        """
        Parse multiplication.

        term = factor (* factor)*
        """

        value, position = self.parse_factor(tokens, position)

        while position < len(tokens):

            operator = tokens[position][0]

            if operator != "*":
                break

            position += 1

            right_value, position = self.parse_factor(tokens, position)

            value *= right_value

        return value, position

    def parse_factor(self, tokens, position):
        """
        Parse:
        - integer
        - variable
        - parenthesized expression
        """

        # No token available
        if position >= len(tokens):
            raise ValueError("Invalid expression.")

        token_type, token_value = tokens[position]

        # -------------------------------------------------
        # Integer
        # -------------------------------------------------
        if token_type == "NUMBER":
            return int(token_value), position + 1

        # -------------------------------------------------
        # Variable
        # -------------------------------------------------
        if token_type == "VARIABLE":

            # Check that variable exists
            if token_value not in self.variables:
                raise ValueError("Unknown variable.")

            value = self.evaluate_variable(token_value)

            return value, position + 1

        # -------------------------------------------------
        # Parenthesized expression
        # -------------------------------------------------
        if token_type == "(":

            value, position = self.parse_expression(
                tokens,
                position + 1
            )

            # A closing ')' must follow
            if (
                position >= len(tokens)
                or tokens[position][0] != ")"
            ):
                raise ValueError("Missing closing parenthesis.")

            return value, position + 1

        # Anything else is invalid
        raise ValueError("Invalid expression.")

    def evaluate(self, expression):
        """Evaluate the final expression."""

        tokens = self.tokenize(expression)

        if not tokens:
            raise ValueError("Empty expression.")

        value, position = self.parse_expression(tokens, 0)

        # If tokens remain, syntax is invalid
        if position != len(tokens):
            raise ValueError("Invalid expression.")

        return value


def main():

    # -----------------------------------------------------
    # Read number of variables
    # -----------------------------------------------------
    v = int(input().strip())

    if v < 1:
        raise ValueError("Number of variables must be at least 1.")

    variables = {}

    # -----------------------------------------------------
    # Read variable definitions
    # -----------------------------------------------------
    for _ in range(v):

        line = input().strip()

        # Variable definition must contain '='
        if "=" not in line:
            print("INVALID")
            return

        name, expression = line.split("=", 1)

        name = name.strip()
        expression = expression.strip()

        # Validate variable name
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
            print("INVALID")
            return

        if not expression:
            print("INVALID")
            return

        variables[name] = expression

    # -----------------------------------------------------
    # Read final expression
    # -----------------------------------------------------
    final_expression = input().strip()

    try:
        engine = ExpressionEngine(variables)

        result = engine.evaluate(final_expression)

        print(result)

    except RuntimeError as error:

        # Circular dependency detected
        if str(error) == "CYCLE":
            print("CYCLE")
        else:
            print("INVALID")

    except (ValueError, RecursionError):
        # Invalid syntax, unknown variable, etc.
        print("INVALID")


# ---------------------------------------------------------
# Program starts here
# ---------------------------------------------------------
if __name__ == "__main__":
    main()