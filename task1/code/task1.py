def Infix2Postfix(Infix):
    """
    Convert infix logical expression to postfix (Reverse Polish notation)
    
    Operators:
    - "(": Open parenthesis
    - "~": Not
    - "&": And
    - "|": Or
    - ">": Implies
    - "=": If and only if
    - ")": Close parenthesis
    """
    # Define operator precedence
    precedence = {
        '~': 4,  # NOT (highest precedence)
        '&': 3,  # AND
        '|': 2,  # OR
        '>': 1,  # IMPLIES
        '=': 1   # IF AND ONLY IF (lowest precedence)
    }
    
    # Initialize variables
    postfix = ""
    stack = []
    
    # Process each character in the infix expression
    i = 0
    while i < len(Infix):
        char = Infix[i]
        
        # If the character is an operand (A-Z), add it to postfix
        if 'A' <= char <= 'Z':
            postfix += char
        
        # If the character is '(', push it onto the stack
        elif char == '(':
            stack.append('(')
        
        # If the character is ')', pop operators from stack and add to postfix until '(' is encountered
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()
            if stack and stack[-1] == '(':
                stack.pop()  # Remove '(' from stack
        
        # If the character is an operator, handle according to precedence
        elif char in precedence:
            # For NOT operator, just push onto stack (right associative)
            if char == '~':
                stack.append(char)
            else:
                # For other operators, pop operators with higher or equal precedence
                while stack and stack[-1] != '(' and stack[-1] in precedence and precedence[stack[-1]] >= precedence[char]:
                    postfix += stack.pop()
                stack.append(char)
        
        i += 1
    
    # Pop remaining operators from stack and add to postfix
    while stack:
        postfix += stack.pop()
    
    return postfix


def Postfix2Truthtable(Postfix):
    """
    Generate a truth table from a postfix expression
    """
    # Extract unique variables from the postfix expression (A-Z)
    variables = sorted(set([char for char in Postfix if 'A' <= char <= 'Z']))
    num_vars = len(variables)
    
    # Generate all possible combinations of True/False for variables
    num_rows = 2 ** num_vars
    table = []
    
    # Create header row
    header = variables + [Postfix]
    table.append(header)
    
    # Generate each row of the truth table
    for i in range(num_rows):
        # Generate values for variables
        values = {}
        row = []
        for j in range(num_vars):
            var_value = bool((i >> (num_vars - 1 - j)) & 1)
            values[variables[j]] = var_value
            row.append(var_value)
        
        # Evaluate the expression
        stack = []
        for char in Postfix:
            if 'A' <= char <= 'Z':
                stack.append(values[char])
            elif char == '~':
                operand = stack.pop()
                stack.append(not operand)
            elif char == '&':
                operand2 = stack.pop()
                operand1 = stack.pop()
                stack.append(operand1 and operand2)
            elif char == '|':
                operand2 = stack.pop()
                operand1 = stack.pop()
                stack.append(operand1 or operand2)
            elif char == '>':
                operand2 = stack.pop()
                operand1 = stack.pop()
                stack.append(not operand1 or operand2)
            elif char == '=':
                operand2 = stack.pop()
                operand1 = stack.pop()
                stack.append(operand1 == operand2)
        
        # Add result to the row
        result = stack.pop()
        row.append(result)
        table.append(row)
    
    return table


# Helper function to print truth table in a readable format
def print_truth_table(table):
    # Convert boolean values to T/F for better readability
    formatted_table = []
    formatted_table.append(table[0])  # Header row
    
    for row in table[1:]:
        formatted_row = []
        for value in row:
            if isinstance(value, bool):
                formatted_row.append('T' if value else 'F')
            else:
                formatted_row.append(value)
        formatted_table.append(formatted_row)
    
    # Calculate column widths
    col_widths = [max(len(str(row[i])) for row in formatted_table) for i in range(len(formatted_table[0]))]
    
    # Print table
    for i, row in enumerate(formatted_table):
        row_str = ' | '.join(str(val).center(col_widths[j]) for j, val in enumerate(row))
        print(row_str)
        if i == 0:  # Print separator after header
            print('-' * len(row_str))
    
    return formatted_table


# Test the functions with the given test cases
def main():
    test_cases = [
        "R|(P&Q)",
        "~P|(Q&R)>R",
        "P|(R&Q)",
        "(P>Q)&(Q>R)",
        "(P|~Q)>~P=(P|(~Q))>~P"
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case}")
        postfix = Infix2Postfix(test_case)
        print(f"Postfix: {postfix}")
        truth_table = Postfix2Truthtable(postfix)
        print("Truth Table:")
        print_truth_table(truth_table)


if __name__ == "__main__":
    main()
