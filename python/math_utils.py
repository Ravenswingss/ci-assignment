class MathUtils:
    """Utility class providing basic mathematical operations."""

    @staticmethod
    def add(a, b):
        """Return the sum of a and b."""
        return a + b 


    @staticmethod
    def subtract(a, b):
        """Return the result of subtracting b from a."""
        return a - b

    @staticmethod
    def multiply(a, b):
        """Return the product of a and b."""
        return a * b

    @staticmethod
    def divide(a, b):
        """Return the result of dividing a by b.
        If division by zero occurs, return -1.0."""
        if b == 0: 
            return -1.0
        return a / b


