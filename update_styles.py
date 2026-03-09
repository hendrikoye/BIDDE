import re
import sys

with open('styles.css', 'r') as f:
    css = f.read()

# 1. Fix backdrop filter for iOS
css = re.sub(r'backdrop-filter:\s*blur\(([^)]+)\);', r'-webkit-backdrop-filter: blur(\1);\n  backdrop-filter: blur(\1);', css)

# 2. Add background size and attachment to body
css = re.sub(r"background:\s*url\('Pics/Background_bw\.jpg'\);", "background: url('Pics/Background_bw.jpg') no-repeat center center fixed;\n  -webkit-background-size: cover;\n  -moz-background-size: cover;\n  -o-background-size: cover;\n  background-size: cover;", css)

# 3. Fix minimum touch target size for navigation links
css = re.sub(r'(nav\s*a\s*{[^}]*)padding:\s*0\.6rem\s*1\.5rem;', r'\1padding: 0.8rem 1.5rem;\n  min-height: 44px;\n  min-width: 44px;\n  display: flex;\n  align-items: center;\n  justify-content: center;', css)

# 4. Update scrolled nav rules to be full width on mobile
def replace_mobile(match):
    m = match.group(0)
    if 'header.scrolled nav' not in m:
        append_index = m.rfind('}')
        if append_index != -1:
            additions = """
  header.scrolled nav {
    position: fixed;
    top: 60px;
    left: 1rem;
    right: 1rem;
    width: calc(100% - 2rem);
    background: white;
    padding: 1rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    z-index: 99;
  }
  
  header.scrolled nav a {
    padding: 1rem;
    text-align: center;
    width: 100%;
    box-sizing: border-box;
  }"""
            return m[:append_index] + additions + '\n}'
    return m

css = re.sub(r'@media \(max-width: 768px\) \{[\s\S]*?^\}', replace_mobile, css, flags=re.MULTILINE)

# 5. Expand touch targets directly on mobile
css = re.sub(r'nav\s*a\s*\{\s*padding:\s*0\.5rem\s*0\.9rem;\s*font-size:\s*0\.8rem;\s*\}', r"""nav a {
    padding: 0.8rem 1rem;
    font-size: 0.9rem;
    min-height: 44px;
    min-width: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
  }""", css)

with open('styles.css', 'w') as f:
    f.write(css)
print('updated css')
