#!/usr/bin/env python3
"""Fix recipe post pages: strip garbled UTF-8 chars, fix image paths, clean up HTML"""

import os, re
from pathlib import Path

POSTS_DIR = Path('/home/kodaagentmt/tag-soup-blog-clone/docs/posts')

# Replacement map for problematic chars
REPLACEMENTS = {
    '🔥': '[*]',  # fire - used in brand banner and footer
    '🫏': '[!]',  # what you'll need
    '💡': '[TIP]',  # pro tip
    '←': '<-',     # back arrow
    # Fix common garbled patterns
    'M-bM-^@M-^T': "'",  # apostrophe encoding
    'M-bM-^FM-^P': '<-', # left arrow
    'M-pM-^_M-^TM-%': '[!]', # mixed garbage for fire
    'M-pM-^_M-^RM-!': '[TIP]', # garbage for lightbulb
    'M-bM-^@M-^T': "'",
    'M-pM-^_M-+M-^O': '[!]', # garbage for what
}

def fix_text(text):
    """Remove/replace garbled UTF-8 sequences and problematic chars"""
    # Replace known emojis first
    for bad, good in REPLACEMENTS.items():
        text = text.replace(bad, good)
    # Remove any remaining M-b/M-p sequences (garbled UTF-8 artifacts)
    text = re.sub(r'M-[b-p][A-Z@`\[\]]-[A-Z@`\[\]]-[A-Z@`\[\]]', '', text)
    return text

def fix_file(filepath):
    html = filepath.read_text(encoding='utf-8', errors='replace')
    
    # Fix image path ../images/ -> images/
    html = html.replace('src="../images/', 'src="images/')
    
    # Fix double .html in og:url
    html = html.replace('.html.html"', '.html"')
    
    # Fix brand banner and footer - replace emojis with plain text
    html = html.replace('🔥', '[*]')
    html = html.replace('🫏', '[!]')
    html = html.replace('💡', '[TIP]')
    html = html.replace('←', '<-')
    
    # Fix garbled sequences that sometimes appear
    html = re.sub(r'M-bM-\^@M-\^T', "'", html)
    html = re.sub(r'M-bM-\^FM-\^P', '<-', html)
    
    # Clean up any remaining weird UTF-8 artifacts in visible text only
    # Get all text nodes by stripping HTML tags, clean, put back
    def clean_text_in_tags(match):
        tag = match.group(1)
        content = match.group(2)
        # Only clean text inside certain tags
        if tag in ('title', 'h1', 'h3', 'p', 'a', 'span', 'div'):
            # Remove any residual UTF-8 artifacts
            content = re.sub(r'M-[b-p][A-Z`\[\]]-[A-Z`\[\]]-[A-Z`\[\]]', '', content)
        return f'<{tag}>{content}</{match.group(3)}>'
    
    # Simpler approach - just find text between tags and clean
    def clean_visible_text(html):
        # Replace the garbled sequences wherever they appear
        patterns = [
            (r'M-bM-\^@M-\^T', "'"),
            (r'M-bM-\^FM-\^P', '<-'),
            (r'M-pM-\^_M-\^TM-\%', '[*]'),
            (r'M-pM-\^_M-\^RM-\!', '[TIP]'),
            (r'M-bM-\^@M-\^T', "'"),
        ]
        for pat, repl in patterns:
            html = re.sub(pat, repl, html)
        return html
    
    html = clean_visible_text(html)
    
    filepath.write_text(html, encoding='utf-8')
    return html != filepath.read_text(encoding='utf-8', errors='replace')

# Process all post files
files = list(POSTS_DIR.glob('*.html'))
fixed = 0
for f in files:
    if fix_file(f):
        fixed += 1

print(f'Fixed {fixed}/{len(files)} post pages')
print(f'All files in {POSTS_DIR}')