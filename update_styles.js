const fs = require('fs');

let css = fs.readFileSync('styles.css', 'utf-8');

// 1. Fix backdrop filter for iOS
css = css.replace(/backdrop-filter:\s*blur\(([^)]+)\);/g, '-webkit-backdrop-filter: blur($1);\n  backdrop-filter: blur($1);');

// 2. Add background size and attachment to body
css = css.replace(/background:\s*url\('Pics\/Background_bw\.jpg'\);/, "background: url('Pics/Background_bw.jpg') no-repeat center center fixed;\n  -webkit-background-size: cover;\n  -moz-background-size: cover;\n  -o-background-size: cover;\n  background-size: cover;");

// 3. Fix minimum touch target size for navigation links
css = css.replace(/nav\s*a\s*{[^}]*padding:\s*0\.6rem\s*1\.5rem;/, match => match.replace('padding: 0.6rem 1.5rem;', 'padding: 0.8rem 1.5rem;\n  min-height: 44px;\n  min-width: 44px;\n  display: flex;\n  align-items: center;\n  justify-content: center;'));

// 4. Update scrolled nav rules to be full width on mobile
// In @media (max-width: 768px)
css = css.replace(/@media \(max-width: 768px\) {([\s\S]*?)}/, match => {
  if (!match.includes('header.scrolled nav')) {
    const appendIndex = match.lastIndexOf('}');
    const additions = `
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
  }`;
    return match.substring(0, appendIndex) + additions + '\n}';
  }
  return match;
});

// 5. Expand touch targets directly on mobile
css = css.replace(/nav\s*a\s*{\s*padding:\s*0\.5rem\s*0\.9rem;\s*font-size:\s*0\.8rem;\s*}/, `nav a {
    padding: 0.8rem 1rem;
    font-size: 0.9rem;
    min-height: 44px;
    min-width: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
  }`);

fs.writeFileSync('styles.css', css);
console.log('updated css');
