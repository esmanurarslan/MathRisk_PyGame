# expression_handler.py (English Comments)

import random
import math


def generate_expression(level_config):
    """
    Generates a random mathematical expression based on the specified level configuration.

    Args:
        level_config (dict): A dictionary containing level settings (operators, operand range).

    Returns:
        tuple: A tuple containing (display_string, operator_symbol, operand_value).
               For some operators (like sqrt), operand_value may be None.
               In case of an error, a default expression (+1) is returned.
    """
    # Retrieve operators and operand range from the level configuration
    ops = level_config.get('operators', ['+', '-']) # Default: addition, subtraction
    min_op, max_op = level_config.get('operand_range', (0 , 5)) # Default: range 0-5

    # Randomly select an operator
    chosen_op = random.choice(ops)

    display_str = ""
    operator = chosen_op
    operand = None # Initially, there is no operand

    try:
        # Generate operand and construct display string based on the selected operator
        if chosen_op == '+':
            operand = random.randint(min_op, max_op)
            if random.random() < 0.25: operand *= -1 # Small chance of negative
            display_str = f"+({operand})" if operand < 0 else f"+{operand}" # Parentheses for negative
        elif chosen_op == '-':
            operand = random.randint(min_op, max_op)
            if random.random() < 0.3: # Small chance of negative
                operand *= -1
                display_str = f"-({operand})" # Display as -(x)
            else: display_str = f"-{operand}"
        elif chosen_op == '*':
            # Ensure operand is suitable for multiplication (avoiding 0 or 1 maybe)
            operand = random.randint(max(2, min_op), max(3, max_op // 2)) # Prefer integers >= 2
            display_str = f"*{operand}"
        elif chosen_op == '/':
            # Ensure operand is suitable for division (avoiding 0)
            operand = random.randint(max(2, min_op), max(4, max_op // 2)) # Prefer integers >= 2
            if operand == 0: operand = 2 # Safety check, avoid division by zero
            display_str = f"/{operand}"
        elif chosen_op == '**':
            # Choose exponent, maybe weighted
            operand = random.choices([0, 0.5, 1, 2], weights=[3, 3, 3, 2])[0] # Example weights
            display_str = f"^{operand}"
            operator = '**' # Use Python's power operator for calculation
        elif chosen_op == 'sqrt':
            operand = None # No operand needed
            display_str = "√" # Square root symbol
            operator = 'sqrt' # Special identifier
        elif chosen_op == 'pow0.5': # Alternative representation
            operand = None
            display_str = "^0.5"
            operator = 'sqrt' # Treat as square root

        # Fallback if an operand is missing for operators that require one
        if operator not in ['sqrt'] and operand is None:
             print(f"Warning: Operand remained None for '{operator}'. Using default '+1'.")
             display_str, operator, operand = "+1", '+', 1

        return display_str, operator, operand

    except Exception as e:
        # Log errors during generation and return a safe default
        print(f"Error during expression generation: {e}")
        return "+1", '+', 1

# Test the function if the script is run directly
if __name__ == '__main__':
    try:
        import settings # Need settings for LEVELS
        test_levels = settings.LEVELS
        for level_num, config in test_levels.items():
            print(f"\n--- Level {level_num} ({config['name']}) Test ---") # Use English name
            for _ in range(7):
                d_str, op, oper = generate_expression(config)
                print(f"  Display: {d_str}, Operation: {op}, Value: {oper}")
    except ImportError:
        print("Could not import 'settings.py' for testing.")
    except AttributeError:
        print("Could not find 'LEVELS' definition in 'settings.py' for testing.")