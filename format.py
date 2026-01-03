#!/usr/bin/env python3
"""
Algorithm Formatter - Converts nested numbered algorithms to Phase format
Usage: python format_algorithm.py < input.txt > output.txt
       or paste into the script and run directly
"""

import re
import sys

def format_algorithm(text):
    """
    Transform algorithm pseudocode from nested numbering to Phase format.
    
    Renumbering rules:
    - Letters (a, b, c) → Numbers (1, 2, 3)
    - Roman numerals (i, ii, iii) → Letters (a, b, c)
    """
    lines = text.split('\n')
    output = []
    phase_number = 0
    in_algorithm = False
    current_phase_indent = None
    step_counter = 0
    substep_counter = {}
    
    for line in lines:
        # Detect algorithm block start
        if 'Algorithm:' in line:
            output.append(line)
            in_algorithm = True
            phase_number = 0
            continue
        
        if not in_algorithm:
            output.append(line)
            continue
        
        # Match top-level numbered items with bold titles
        # Patterns: "1. **Title**:" or "    1. **Title**:"
        match = re.match(r'^(\s*)(\d+)\.\s+\*\*(.+?)\*\*:?\s*$', line)
        
        if match:
            indent = match.group(1)
            title = match.group(3)
            phase_number += 1
            step_counter = 0
            substep_counter = {}
            
            # Create phase header with reduced indent
            base_indent = ' ' * (len(indent) - 4) if len(indent) >= 4 else ''
            current_phase_indent = base_indent + '    '
            output.append('')  # Blank line before phase
            output.append(f'{base_indent}**Phase {phase_number}: {title}**')
            continue
        
        # Match letter items (a., b., c.) - these become numbers
        letter_match = re.match(r'^(\s+)([a-z])\.\s+(.+)$', line)
        if letter_match:
            indent = letter_match.group(1)
            content = letter_match.group(3)
            step_counter += 1
            
            output.append(f'{current_phase_indent}{step_counter}. {content}')
            # Reset substep counter for this step
            substep_counter[step_counter] = 0
            continue
        
        # Match roman numerals (i., ii., iii.) - these become letters
        roman_match = re.match(r'^(\s+)(i{1,3}|iv|v|vi{0,3}|ix|x)\.\s+(.+)$', line)
        if roman_match:
            indent = roman_match.group(1)
            content = roman_match.group(3)
            
            # Get current step's substep counter
            if step_counter not in substep_counter:
                substep_counter[step_counter] = 0
            substep_counter[step_counter] += 1
            
            letter = chr(96 + substep_counter[step_counter])  # 97='a', 98='b', etc.
            output.append(f'{current_phase_indent}    {letter}. {content}')
            continue
        
        # Pass through everything else (including blank lines)
        output.append(line)
    
    return '\n'.join(output)


# Sample input for testing
SAMPLE_INPUT = """
Algorithm:
            1. **Try Getting User Info**:
               a. Enter try block for error handling
               b. Call self.get_service() to get Drive service
               c. If service is None:
                  i. Not authenticated
                  ii. Return empty dict {}
            
            2. **Make API Call**:
               a. Call service.about().get(fields="user").execute()
                  i. about(): Endpoint for account info
                  ii. get(): Retrieve information
                  iii. fields="user": Request only user fields
                  iv. execute(): Perform API request
               b. Store response in about variable
            
            3. **Extract User Data**:
               a. Get 'user' field from response: about.get('user', {})
               b. Store in user variable
               c. Extract email: user.get('emailAddress', 'unknown')
               d. Print success message with email
               e. Return user dictionary
            
            4. **Handle Errors**:
               a. Catch any Exception during API call
               b. Print error message with exception details
               c. Return empty dict {} (API call failed)
"""

if __name__ == "__main__":
    # Method 1: Read from stdin
    if not sys.stdin.isatty():
        input_text = sys.stdin.read()
        print(format_algorithm(input_text))
    
    # Method 2: Use sample input for testing
    else:
        print("=== FORMATTED OUTPUT ===")
        print(format_algorithm(SAMPLE_INPUT))
        print("\n=== USAGE ===")
        print("To use with your own text:")
        print("  python format_algorithm.py < input.txt > output.txt")