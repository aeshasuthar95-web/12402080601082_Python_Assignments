# ---------------------------------------------------------
# Assignment 1 - Q7
# Interactive Formula Validator with Custom Exceptions
# ---------------------------------------------------------


class InvalidFormatError(Exception):
    pass


class UnknownVariableError(Exception):
    pass


class DivisionByZeroError(Exception):
    pass


class UnsupportedOperatorError(Exception):
    pass


def get_operand(value, variables):
    """
    Convert an operand into a number.

    Operand can be:
    - integer
    - decimal
    - previously stored variable
    """

    # Try number first
    try:
        return float(value)
    except ValueError:
        pass

    # Try variable
    if value in variables:
        return variables[value]

    raise UnknownVariableError(
        f"Unknown variable: {value}"
    )


def calculate(left, operator, right):

    if operator == "+":
        return left + right

    if operator == "-":
        return left - right

    if operator == "*":
        return left * right

    if operator == "/":

        if right == 0:
            raise DivisionByZeroError(
                "Cannot divide by zero."
            )

        return left / right

    if operator == "%":

        if right == 0:
            raise DivisionByZeroError(
                "Cannot use modulo with zero."
            )

        return left % right

    raise UnsupportedOperatorError(
        f"Unsupported operator: {operator}"
    )


def format_result(value):
    """Print integers without unnecessary .0."""

    if value.is_integer():
        return str(int(value))

    return str(value)


def main():

    variables = {}

    print("Interactive Calculator")
    print("Enter 'quit' to exit.")

    while True:

        try:

            line = input().strip()

            if line.lower() == "quit":
                break

            if not line:
                raise InvalidFormatError(
                    "Empty input."
                )

            # -------------------------------------------------
            # Assignment statement:
            # x = 10
            # -------------------------------------------------

            if "=" in line:

                parts = line.split("=")

                if len(parts) != 2:
                    raise InvalidFormatError(
                        "Invalid assignment format."
                    )

                variable = parts[0].strip()
                value_text = parts[1].strip()

                # Python identifier validation
                if not variable.isidentifier():
                    raise InvalidFormatError(
                        "Invalid variable name."
                    )

                if not value_text:
                    raise InvalidFormatError(
                        "Missing value."
                    )

                value = get_operand(
                    value_text,
                    variables
                )

                variables[variable] = value

                continue

            # -------------------------------------------------
            # Formula:
            # operand operator operand
            # -------------------------------------------------

            parts = line.split()

            if len(parts) != 3:
                raise InvalidFormatError(
                    "Formula must be: operand operator operand"
                )

            left_text, operator, right_text = parts

            left = get_operand(
                left_text,
                variables
            )

            right = get_operand(
                right_text,
                variables
            )

            result = calculate(
                left,
                operator,
                right
            )

            print(format_result(result))

        except DivisionByZeroError as error:

            print("DivisionByZeroError")
            print(error)

        except UnsupportedOperatorError:

            print("UnsupportedOperatorError")

        except UnknownVariableError as error:

            print("UnknownVariableError")
            print(error)

        except InvalidFormatError as error:

            print("InvalidFormatError")
            print(error)


if __name__ == "__main__":
    main()