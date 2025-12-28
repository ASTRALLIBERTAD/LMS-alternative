"""
DocGen Pro - Python Docstring to Docusaurus Markdown Converter

Usage:
    python docgen.py --src ./src --output ./docs
    python docgen.py --src ./src --output ./docs --generate-sidebar
    python docgen.py --file ./myfile.py --output ./docs
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class DocstringParser:
    """Parse Python docstrings into structured data."""
    
    SECTION_PATTERN = re.compile(r'^([A-Z][A-Za-z\s/]+):$')
    PARAM_PATTERN = re.compile(r'^\s*(\w+)\s*\(([^)]+)\)(?:,\s*(\w+))?\s*:\s*(.+)?')
    
    def __init__(self, code: str, filename: str):
        self.code = code
        self.filename = filename
        self.docstrings = []
        
    def extract_all(self) -> List[Dict]:
        """Extract all docstrings from Python code."""
        lines = self.code.split('\n')
        in_docstring = False
        current_docstring = []
        docstring_start = 0
        context = {'name': '', 'type': 'module', 'indent': 0}
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Detect function/class/module definition
            if stripped.startswith('class '):
                match = re.match(r'class\s+(\w+)', stripped)
                if match:
                    context = {
                        'name': match.group(1),
                        'type': 'class',
                        'indent': len(line) - len(line.lstrip())
                    }
            elif stripped.startswith('def '):
                match = re.match(r'def\s+(\w+)', stripped)
                if match:
                    context = {
                        'name': match.group(1),
                        'type': 'method' if context.get('type') == 'class' else 'function',
                        'indent': len(line) - len(line.lstrip())
                    }
            
            # Detect docstring delimiters
            if stripped.startswith('"""') or stripped.startswith("'''"):
                if not in_docstring:
                    in_docstring = True
                    docstring_start = i
                    current_docstring = [line]
                    
                    # Single line docstring
                    if stripped.count('"""') == 2 or stripped.count("'''") == 2:
                        doc = self._parse_docstring(
                            '\n'.join(current_docstring),
                            context['name'],
                            context['type'],
                            docstring_start + 1
                        )
                        if doc:
                            self.docstrings.append(doc)
                        in_docstring = False
                        current_docstring = []
                else:
                    current_docstring.append(line)
                    doc = self._parse_docstring(
                        '\n'.join(current_docstring),
                        context['name'],
                        context['type'],
                        docstring_start + 1
                    )
                    if doc:
                        self.docstrings.append(doc)
                    in_docstring = False
                    current_docstring = []
            elif in_docstring:
                current_docstring.append(line)
        
        return self.docstrings
    
    def _parse_docstring(self, text: str, name: str, doc_type: str, line_num: int) -> Optional[Dict]:
        """Parse a single docstring into structured format."""
        lines = text.split('\n')
        result = {
            'filename': self.filename,
            'name': name or 'Module',
            'type': doc_type,
            'line_number': line_num,
            'summary': '',
            'description': '',
            'sections': {},
            'metadata': {
                'has_examples': False,
                'has_algorithm': False,
                'completeness': 0
            }
        }
        
        current_section = None
        current_content = []
        in_code_block = False
        
        for line in lines:
            stripped = line.strip()
            
            # Skip docstring delimiters (both standalone and with text)
            if stripped in ['"""', "'''"]:
                continue
            # Skip lines that start with delimiter (opening docstring)
            if stripped.startswith('"""') or stripped.startswith("'''"):
                # If it's opening delimiter with text on same line, extract the text
                if stripped.startswith('"""'):
                    text_after = stripped[3:].strip()
                    if text_after and not text_after.endswith('"""'):
                        stripped = text_after
                    else:
                        continue
                elif stripped.startswith("'''"):
                    text_after = stripped[3:].strip()
                    if text_after and not text_after.endswith("'''"):
                        stripped = text_after
                    else:
                        continue
            
            # Detect section headers (but not if we're in a code block)
            # UNLESS this line itself is a section header (which means the code block ended)
            section_match = self.SECTION_PATTERN.match(stripped)
            if section_match:
                # Section header found - this ends any code block
                in_code_block = False
                
                # Save previous section
                if current_section:
                    result['sections'][current_section] = '\n'.join(current_content).strip()
                
                current_section = section_match.group(1).strip()
                current_content = []
                
                # Track metadata
                if 'example' in current_section.lower():
                    result['metadata']['has_examples'] = True
                if 'algorithm' in current_section.lower():
                    result['metadata']['has_algorithm'] = True
                    
            elif current_section:
                current_content.append(line)
                # Track code blocks within sections
                if stripped.startswith('>>>') or stripped.startswith('```'):
                    in_code_block = not in_code_block
            elif not result['summary'] and stripped:
                result['summary'] = stripped
            elif stripped and not current_section:
                result['description'] += (result['description'] and '\n' or '') + stripped
        
        # Save last section
        if current_section:
            result['sections'][current_section] = '\n'.join(current_content).strip()
        
        # Calculate completeness
        important_sections = ['Args', 'Parameters', 'Returns', 'Example', 'Examples']
        found = sum(1 for s in important_sections if s in result['sections'])
        result['metadata']['completeness'] = int((found / len(important_sections)) * 100)
        
        return result if result['summary'] or result['sections'] else None


class MarkdownFormatter:
    """Format parsed docstrings into Docusaurus Markdown."""
    
    # Pattern for parsing parameter lines
    PARAM_PATTERN = re.compile(r'^\s*(\w+)\s*\(([^)]+)\)(?:,\s*(\w+))?\s*:\s*(.+)?')
    
    @staticmethod
    def convert_sphinx_refs(text: str) -> str:
        """Convert Sphinx-style references to Markdown links.
        
        Converts:
        - :class:`~module.ClassName` -> [ClassName](path)
        - :meth:`method_name` -> `method_name()`
        - :func:`function_name` -> `function_name()`
        - :mod:`module` -> [module](path)
        
        Args:
            text: Text containing Sphinx-style references
            
        Returns:
            Text with markdown-style links
        """
        # Pattern for :role:`~module.path.Name` or :role:`Name`
        # Extract the display name (after last dot if ~ prefix, otherwise full path)
        def replace_ref(match):
            role = match.group(1)  # class, meth, func, mod, etc.
            path = match.group(2)  # ~module.Class or just Class
            
            # Get display name
            if path.startswith('~'):
                # Use only the last component
                display_name = path.split('.')[-1]
                full_path = path[1:]  # Remove ~
            else:
                display_name = path
                full_path = path
            
            # Add () for methods and functions
            if role in ['meth', 'func']:
                display_name = f"{display_name}()"
            
            # For now, just use code formatting without links since we don't know the actual URLs
            # In a real scenario, you'd map these to actual doc URLs
            return f"`{display_name}`"
        
        # Match :role:`path` pattern
        text = re.sub(r':(\w+):`([^`]+)`', replace_ref, text)
        
        return text
    
    @staticmethod
    def escape_mdx(text: str) -> str:
        """Escape characters that conflict with MDX/JSX syntax.
        
        MDX interprets < followed by letters/numbers as JSX tags. This causes
        errors with comparisons like <900px or expressions like >=900px.
        
        We need to escape:
        - < when followed by a digit (e.g., <900px, <100, <5)
        - > when followed by = (e.g., >=900px)
        - < when followed by = (e.g., <=100)
        
        Args:
            text: Text that may contain MDX-problematic characters
            
        Returns:
            Text with problematic patterns escaped using HTML entities
        """
        import re
        
        # Escape < followed by a digit (e.g., <900px, <5, <100)
        text = re.sub(r'<(\d)', r'&lt;\1', text)
        
        # Escape >= and <=
        text = text.replace('>=', '&gt;=')
        text = text.replace('<=', '&lt;=')
        
        # Escape < followed by a letter at word boundaries (potential JSX tags)
        # But be careful not to break intentional HTML entities or links
        text = re.sub(r'<([a-zA-Z][a-zA-Z0-9]*)', r'&lt;\1', text)
        
        return text
    
    def format(self, doc: Dict, position: int = 1, relative_path: Path = None, module_name: str = None) -> str:
        """Convert parsed docstring to Markdown.
        
        Args:
            doc: Parsed docstring dictionary
            position: Position in sidebar
            relative_path: Relative path from source root
            module_name: Module/file name without extension
        """
        md = []
        
        # Generate document ID - just the doc name, no path/slashes
        # The folder structure is already represented by the file path
        doc_name_slug = doc['name'].lower().replace(' ', '-')
        doc_id = doc_name_slug
        
        # Frontmatter
        md.append('---')
        md.append(f'id: "{doc_id}"')
        md.append('sidebar_position: {}'.format(position))
        # Properly escape and quote title to prevent YAML parsing errors
        title = doc['name'].replace('"', '\\"')
        md.append('title: "{}"'.format(title))
        md.append('---')
        md.append('')
        
        # Title with emoji
        emoji_map = {
            'class': '📦',
            'function': '⚙️',
            'method': '🔧',
            'module': '📁'
        }
        emoji = emoji_map.get(doc['type'], '📄')
        md.append('# {} {}'.format(emoji, doc['name']))
        md.append('')
        
        # Metadata badges
        badges = []
        if doc['metadata']['has_examples']:
            badges.append('![Has Examples](https://img.shields.io/badge/Examples-✓-green)')
        if doc['metadata']['has_algorithm']:
            badges.append('![Has Algorithm](https://img.shields.io/badge/Algorithm-✓-blue)')
        
        completeness = doc['metadata']['completeness']
        color = 'green' if completeness > 70 else 'orange' if completeness > 40 else 'red'
        badges.append('![Completeness](https://img.shields.io/badge/Docs-{}%25-{})'.format(completeness, color))
        
        if badges:
            md.append(' '.join(badges))
            md.append('')
        
        # Source reference - make filename clickable
        md.append(':::info Source')
        md.append('**File:** [`{}`](./{}) | **Line:** {}'.format(
            doc['filename'], 
            doc['filename'],
            doc['line_number']
        ))
        md.append(':::')
        md.append('')
        
        # Summary and description (with MDX escaping)
        if doc['summary']:
            md.append(self.escape_mdx(doc['summary']))
            md.append('')
        
        if doc['description']:
            md.append(self.escape_mdx(doc['description']))
            md.append('')
        
        # Process sections in priority order
        section_configs = {
            'Purpose': {'title': '## Purpose', 'formatter': self._format_text},
            'Attributes': {'title': '## Attributes', 'formatter': self._format_params},
            'Args': {'title': '## Parameters', 'formatter': self._format_params},
            'Parameters': {'title': '## Parameters', 'formatter': self._format_params},
            'Returns': {'title': '## Returns', 'formatter': self._format_returns},
            'Raises': {'title': '## Exceptions', 'formatter': self._format_params},
            'Yields': {'title': '## Yields', 'formatter': self._format_params},
            'Algorithm': {'title': '## Algorithm', 'formatter': self._format_algorithm},
            'Interactions': {'title': '## Interactions', 'formatter': self._format_list},
            'Example': {'title': '## Example', 'formatter': self._format_code},
            'Examples': {'title': '## Examples', 'formatter': self._format_code},
            'See Also': {'title': '## See Also', 'formatter': self._format_list},
            'Notes': {'title': '## Notes', 'formatter': self._format_list},
            'Security Considerations': {'title': '## Security Considerations', 'formatter': self._format_admonition},
            'References': {'title': '## References', 'formatter': self._format_list},
        }
        
        for section_name, config in section_configs.items():
            if section_name in doc['sections']:
                md.append(config['title'])
                md.append('')
                content = doc['sections'][section_name]
                formatted_lines = config['formatter'](content)
                md.extend(formatted_lines)
                md.append('')
        
        return '\n'.join(md)
    
    def _format_text(self, content: str) -> List[str]:
        """Format plain text with MDX escaping."""
        return [self.escape_mdx(line) for line in content.split('\n')]
    
    def _format_params(self, content: str) -> List[str]:
        """Format parameters/attributes with MDX escaping."""
        result = []
        lines = content.split('\n')
        
        current_param = None
        param_desc = []
        
        for line in lines:
            param_match = self.PARAM_PATTERN.match(line)
            if param_match:
                # Save previous parameter
                if current_param:
                    desc_text = self.escape_mdx(' '.join(param_desc))
                    result.append('- **`{}`** ({}): {}'.format(
                        current_param[0],
                        current_param[1],
                        desc_text
                    ))
                
                # Start new parameter
                name, type_info, optional, desc = param_match.groups()
                current_param = (name, type_info)
                param_desc = [desc] if desc else []
            elif line.strip() and current_param:
                param_desc.append(line.strip())
        
        # Save last parameter
        if current_param:
            desc_text = self.escape_mdx(' '.join(param_desc))
            result.append('- **`{}`** ({}): {}'.format(
                current_param[0],
                current_param[1],
                desc_text
            ))
        
        return result if result else [self.escape_mdx(content)]
    
    def _format_returns(self, content: str) -> List[str]:
        """Format return values with MDX escaping."""
        lines = content.split('\n')
        result = []
        
        if lines and ':' in lines[0]:
            # Structured return
            result.append('**Type**: `{}`'.format(lines[0].split(':')[0].strip()))
            result.append('')
            result.extend([self.escape_mdx(line) for line in lines[1:]])
        else:
            result.extend([self.escape_mdx(line) for line in lines])
        
        return result
    
    def _format_code(self, content: str) -> List[str]:
        """Format code examples, handling doctest format properly.
        
        Removes >>> and ... prompts while preserving code structure.
        Handles output lines (those without prompts) as comments.
        """
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # Skip empty lines
            if not stripped:
                formatted_lines.append('')
                continue
            
            # Check if it's a prompt line
            if stripped.startswith('>>>') or stripped.startswith('...'):
                # Remove the prompt
                code_line = re.sub(r'^\s*>>>\s*', '', line)
                code_line = re.sub(r'^\s*\.\.\.\s*', '    ', code_line)  # Indent continuation lines
                formatted_lines.append(code_line.rstrip())
            else:
                # It's an output line - add as comment
                if stripped:  # Only add non-empty output lines
                    formatted_lines.append(f"# {stripped}")
        
        return ['```python', '\n'.join(formatted_lines).strip(), '```']
    
    def _format_algorithm(self, content: str) -> List[str]:
        """Format algorithm steps with proper indentation and MDX escaping."""
        lines = []
        for line in content.split('\n'):
            if not line.strip():
                lines.append('')
                continue
                
            # Convert indentation to markdown lists
            indent = len(line) - len(line.lstrip())
            text = self.escape_mdx(line.strip())
            
            if indent >= 15:
                lines.append('      - {}'.format(text))
            elif indent >= 12:
                lines.append('    - {}'.format(text))
            elif indent >= 8:
                lines.append('  - {}'.format(text))
            elif indent >= 4:
                lines.append('- {}'.format(text))
            else:
                lines.append(text)
        
        return lines
    
    def _format_list(self, content: str) -> List[str]:
        """Format bullet lists with MDX escaping and Sphinx reference conversion."""
        lines = []
        for line in content.split('\n'):
            stripped = line.strip()
            if stripped:
                # Remove existing list markers
                text = re.sub(r'^[-*]\s*', '', stripped)
                # Convert Sphinx references to markdown
                text = self.convert_sphinx_refs(text)
                # Escape MDX problematic characters
                text = self.escape_mdx(text)
                lines.append('- {}'.format(text))
        return lines
    
    def _format_admonition(self, content: str) -> List[str]:
        """Format as Docusaurus admonition with MDX escaping."""
        return [':::note', self.escape_mdx(content.strip()), ':::']


def generate_sidebar_config(docs: List[Dict], output_dir: Path) -> Dict:
    """Generate Docusaurus sidebar configuration."""
    sidebar = {
        'docs': []
    }
    
    # Group by module/file
    by_file = {}
    for doc in docs:
        if doc['filename'] not in by_file:
            by_file[doc['filename']] = []
        by_file[doc['filename']].append(doc)
    
    for filename, file_docs in sorted(by_file.items()):
        module_name = Path(filename).stem
        
        if len(file_docs) == 1:
            # Single doc, add directly
            sidebar['docs'].append({
                'type': 'doc',
                'id': '{}/{}'.format(module_name, file_docs[0]['name'].lower())
            })
        else:
            # Multiple docs, create category
            sidebar['docs'].append({
                'type': 'category',
                'label': module_name.replace('_', ' ').title(),
                'items': [
                    {
                        'type': 'doc',
                        'id': '{}/{}'.format(module_name, doc['name'].lower())
                    }
                    for doc in file_docs
                ]
            })
    
    return sidebar


def process_file(py_file: Path, output_dir: Path, relative_path: Path = None) -> List[Dict]:
    """Process a single Python file and return extracted docs.
    
    Args:
        py_file: Path to Python file to process
        output_dir: Directory to write markdown files
        relative_path: Relative path from source root to maintain folder structure
        
    Returns:
        List of extracted docstring dictionaries
    """
    output_dir = Path(output_dir)
    all_docs = []
    formatter = MarkdownFormatter()
    
    try:
        print('Processing: {}...'.format(py_file.name), end=' ')
        
        with open(py_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Parse docstrings
        parser = DocstringParser(code, py_file.name)
        docstrings = parser.extract_all()
        
        if not docstrings:
            print('⚠️  No docstrings found')
            return []
        
        # Create module directory with preserved folder structure
        module_name = py_file.stem
        
        if relative_path:
            # Preserve the folder structure from source
            module_dir = output_dir / relative_path.parent / module_name
        else:
            # Default behavior: just use module name
            module_dir = output_dir / module_name
            
        module_dir.mkdir(exist_ok=True, parents=True)
        
        # Generate markdown for each docstring
        for idx, doc in enumerate(docstrings, start=1):
            markdown = formatter.format(doc, position=idx, relative_path=relative_path, module_name=module_name)
            
            # Write to file
            doc_filename = '{}.md'.format(doc['name'].lower().replace(' ', '-'))
            output_file = module_dir / doc_filename
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown)
            
            all_docs.append(doc)
        
        print('✅ {} doc(s) generated'.format(len(docstrings)))
        return all_docs
        
    except Exception as e:
        print('❌ Error: {}'.format(e))
        return []


def process_directory(src_dir: Path, output_dir: Path, generate_sidebar: bool = False):
    """Process all Python files in source directory."""
    src_dir = Path(src_dir)
    output_dir = Path(output_dir)
    
    if not src_dir.exists():
        print('❌ Source directory not found: {}'.format(src_dir))
        return
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all Python files
    python_files = list(src_dir.rglob('*.py'))
    
    if not python_files:
        print('❌ No Python files found in {}'.format(src_dir))
        return
    
    print('📁 Found {} Python file(s)'.format(len(python_files)))
    print('📝 Output directory: {}'.format(output_dir))
    print()
    
    all_docs = []
    
    for py_file in python_files:
        # Calculate relative path from source directory
        relative_path = py_file.relative_to(src_dir)
        docs = process_file(py_file, output_dir, relative_path)
        all_docs.extend(docs)
    
    print()
    print('✅ Generated {} documentation file(s)'.format(len(all_docs)))
    
    # Generate sidebar config
    if generate_sidebar and all_docs:
        sidebar = generate_sidebar_config(all_docs, output_dir)
        sidebar_file = output_dir / 'sidebars.json'
        
        with open(sidebar_file, 'w', encoding='utf-8') as f:
            json.dump(sidebar, f, indent=2)
        
        print('📋 Sidebar config: {}'.format(sidebar_file))


def main():
    parser = argparse.ArgumentParser(
        description='Convert Python docstrings to Docusaurus Markdown',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process entire directory
  python docgen.py --src ./src --output ./docs
  
  # Process single file
  python docgen.py --file ./dashboard.py --output ./docs
  
  # Generate with sidebar
  python docgen.py --src ./myproject --output ./website/docs --generate-sidebar
        """
    )
    
    parser.add_argument(
        '--src',
        type=str,
        help='Source directory containing Python files'
    )
    
    parser.add_argument(
        '--file',
        type=str,
        help='Single Python file to process'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='Output directory for generated Markdown files'
    )
    
    parser.add_argument(
        '--generate-sidebar',
        action='store_true',
        help='Generate sidebars.json configuration file'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.src and not args.file:
        parser.error('Either --src or --file must be specified')
    
    if args.src and args.file:
        parser.error('Cannot specify both --src and --file')
    
    print('=' * 60)
    print('  DocGen Pro - Docstring to Docusaurus Converter')
    print('=' * 60)
    print()
    
    if args.file:
        # Process single file
        py_file = Path(args.file)
        if not py_file.exists():
            print('❌ File not found: {}'.format(py_file))
            return
        
        print('📄 Processing single file: {}'.format(py_file))
        print('📝 Output directory: {}'.format(args.output))
        print()
        
        all_docs = process_file(py_file, Path(args.output))
        
        if args.generate_sidebar and all_docs:
            sidebar = generate_sidebar_config(all_docs, Path(args.output))
            sidebar_file = Path(args.output) / 'sidebars.json'
            
            with open(sidebar_file, 'w', encoding='utf-8') as f:
                json.dump(sidebar, f, indent=2)
            
            print('📋 Sidebar config: {}'.format(sidebar_file))
    else:
        # Process directory
        process_directory(
            Path(args.src),
            Path(args.output),
            args.generate_sidebar
        )
    
    print()
    print('=' * 60)
    print('  Done!')
    print('=' * 60)


if __name__ == '__main__':
    main()