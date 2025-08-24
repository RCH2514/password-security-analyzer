# PWD-CHECK 🔐

[![Python Version](https://img.shields.io/badge/python-3.6+-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Password Security Analyzer**  
Created by **QU33NR** 👑

`pwdcheck` is a command-line tool that **analyzes password strength**, checks for **data breaches**, and can **generate strong passwords** to ensure maximum security.

---

## Features 

- Checks password strength based on:
  - Minimum length (12+ characters)
  - Uppercase & lowercase letters
  - Digits and special symbols
  - Character uniqueness
  - Detection of keyboard sequences (e.g., `1234`, `qwerty`, `azerty`)  
-  Passwords are entered **securely** — they **won’t be visible** while typing in the terminal.
-  Checks if the password has appeared in **data breaches** using [Have I Been Pwned API](https://haveibeenpwned.com/Passwords)  
-  Generates **strong, random passwords**  
-  Colorful ASCII banner & animated terminal output  
-  Simple CLI interface:
  - `pwdcheck` → analyze your password  
  - `pwdcheck -g` → generate a strong password instantly  

---

## Installation 

```bash
pip install git+https://github.com/RCH2514/password-security-analyzer.git
```
Make sure ~/.local/bin is in your $PATH:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```
## Usage 
### Analyze a password:
```bash
pwdcheck
```
- Enter your password when prompted.
- Get a detailed report with advice for improving weak points.
- See if your password has been compromised in known breaches.
- Propose to generate a random password.
### Generate a strong password:
```bash
pwdcheck -g
```
- Immediately generates a strong, random password.
- Avoids keyboard sequences and repeated characters.
## Example Output 
```yaml
$ pwdcheck
Enter a password to analyze: Hello123+
### Analysis of your password:

❌ Too short. Use at least 12 characters.
✅ Contains uppercase letters.
✅ Contains lowercase letters.
✅ Contains digits.
✅ Contains special symbols.
✅ Characters aren’t overly repeated.
✅ No obvious keyboard patterns.
⚠ This password was found 2 times in data breaches

--- Final Verdict ---
🔐 Password Strength: **Weak**
❌ NOT SAFE: Please choose another password.
Do you want us to generate a strong password for you? (y/n)
> 
```
```yaml
🔑 Generated strong password: lP+1V1dbNVhZn13y
```
## Requirements 
- Python 3.6+

- requests

- pyfiglet   
## Contributing 
Feel free to open issues or submit pull requests.
Suggestions for new features, improvements, or bug fixes are welcome!
## License 
This project is licensed under the MIT License                                          
