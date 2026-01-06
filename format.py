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
            1. **Update Mode State**:
               a. Check self.mode_switch.value (True/False)
               b. If True:
                  i. Set self.current_mode = "student"
               c. If False:
                  i. Set self.current_mode = "teacher"
            
            2. **Configure Student Mode (if student)**:
               a. Set mode_label.value = "👨‍🎓 Student View"
               b. Set student_selector_row.visible = True
                  - Shows student dropdown
               c. If form_container exists:
                  i. Set form_container.visible = False
                  ii. Hides assignment creation form
               d. If manage_students_btn exists:
                  i. Set manage_students_btn.visible = False
                  ii. Hides student management button
            
            3. **Configure Teacher Mode (else teacher)**:
               a. Set mode_label.value = "👨‍🏫 Teacher View"
               b. Set student_selector_row.visible = False
                  - Hides student dropdown
               c. If form_container exists:
                  i. Set form_container.visible = True
                  ii. Shows assignment creation form
               d. If manage_students_btn exists:
                  i. Set manage_students_btn.visible = True
                  ii. Shows student management button
            
            4. **Refresh Assignment Display**:
               a. Call self.display_assignments()
               b. Updates assignment list for current mode
            
            5. **Update Page**:
               a. Call self.page.update()
               b. Renders all visibility changes

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