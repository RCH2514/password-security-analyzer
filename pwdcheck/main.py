#!/usr/bin/env python3
import hashlib
import requests
import re
import os
import getpass
import sys
import time
import pyfiglet
import random
import string
import argparse

def slow_print(text, delay=0.05):
    """Print text one character at a time for a typewriter effect"""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()  # to add a new line at the end

def banner():
    # ASCII banner
    ascii_banner = pyfiglet.figlet_format("PWD-CHECK", font="slant")
    
    
    for line in ascii_banner.split("\n"):
        slow_print("\033[1;32m" + line + "\033[0m", delay=0.005)

    
    print("\033[1;32m" + "          Password Security Analyzer" + "\033[0m")
    print("\033[1;32m" + "                by QU33NR 👑" + "\033[0m")
    print("\033[1;32m" + "=======================================" + "\033[0m")
    time.sleep(0.5)
def has_unique_chars(password):
    return len(set(password)) >= len(password) * 0.6 # at least 60% unique

SPECIAL_CHARS = ["@", "$", "!", "%", "*", "?", "&", "+", "-", "_", "=", "<", ">", "#"]
MIN_LEN = 12
keyboard_layouts = {
    "qwerty": [
        "1234567890",
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm"
    ],
    "azerty": [
        "1234567890",
        "azertyuiop",
        "qsdfghjklm",
        "wxcvbn"
    ]
}
for layout in keyboard_layouts:
    keyboard_layouts[layout] += [row[::-1] for row in keyboard_layouts[layout]]
def has_keyboard_sequence(password, seq_length=4):
    pw_lower = password.lower()
    
    for layout_rows in keyboard_layouts.values():
        for row in layout_rows:
            for i in range(len(row) - seq_length + 1):
                seq = row[i:i+seq_length]
                if seq in pw_lower:
                    return True
    return False

def evaluate_rules(password):
    rules = {
        "length": len(password) >= MIN_LEN,
        "uppercase": any(c.isupper() for c in password),                  
        "lowercase": any(c.islower() for c in password),
        "digit": any(c.isdigit() for c in password),
        "special": any(c in SPECIAL_CHARS for c in password),
        "unique_chars": has_unique_chars(password),
        "keyboard_seq": not has_keyboard_sequence(password, seq_length=4) # set 3 if you want to catch '123'
    }
    return rules
def verdict_from_rules(rules):
    score = sum(rules.values())
    if score <= 4:
        return "Weak"
    elif score <= 6:
        return "Medium"
    else:
        return "Strong"
def generate_password_report(password):
    rules = evaluate_rules(password)
    verdict = verdict_from_rules(rules)

    explanations = {
        "length":      ("✅ Good length (12+).", f"❌ Too short. Use at least {MIN_LEN} characters."),
        "uppercase":   ("✅ Contains uppercase letters.", "❌ No uppercase letters. Add A–Z."),
        "lowercase":   ("✅ Contains lowercase letters.", "❌ No lowercase letters. Add a–z."),
        "digit":       ("✅ Contains digits.", "❌ No numbers. Add at least one digit (0–9)."),
        "special":     (f"✅ Contains special symbols.", f"❌ Missing special characters. Use {''.join(sorted(SPECIAL_CHARS))}"),
        "unique_chars":("✅ Characters aren’t overly repeated.", "❌ Too many repeats. Use more variety."),
        "keyboard_seq":("✅ No obvious keyboard patterns.", "❌ Contains keyboard sequences (e.g., 1234, qwer). Avoid predictable patterns."),
    }

    lines = [f"", "### Analysis of your password:", ""]
    for k, ok in rules.items():
        lines.append(explanations[k][0] if ok else explanations[k][1])

    return verdict, "\n".join(lines)
# --- HIBP Check ---
def check_hibp(password):
    sha1pwd = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1pwd[:5]
    suffix = sha1pwd[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    res = requests.get(url)
    
    if res.status_code != 200:
        raise RuntimeError("Error fetching from HIBP API")
    
    hashes = (line.split(":") for line in res.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)  # number of times found
    
    return 0
def generate_strong_password(length=16):
    if length < 12:
        length = 12  # enforce minimum length

    while True:
        # 1. Pick at least one of each type
        password_chars = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice(SPECIAL_CHARS)
        ]

        # 2. Fill the rest randomly
        all_chars = string.ascii_letters + string.digits + "".join(SPECIAL_CHARS)
        password_chars += random.choices(all_chars, k=length - 4)

        # 3. Shuffle so types aren’t predictable
        random.shuffle(password_chars)

        password = ''.join(password_chars)

        # 4. check uniqueness ratio
        if len(set(password)) / len(password) >= 0.6:
            # 5. check keyboard sequences
            if not has_keyboard_sequence(password, seq_length=4):
                return password

# --- MAIN ---
def main():
    parser = argparse.ArgumentParser(
        description="PWD-CHECK: Password Security Analyzer by QU33NR"
    )
    parser.add_argument(
        "-g", "--generate",
        action="store_true",
        help="Generate a strong password immediately"
    )
    args = parser.parse_args()
    banner()
    if args.generate:
        # If user passed -g, generate and print a strong password directly
        strong_pwd = generate_strong_password()
        print("\n🔑 Generated strong password:", strong_pwd)
        return  # exit after generating
    try:
        pwd = getpass.getpass("Enter a password to analyze: ")

    # 1. Strength
   
        verdict, report = generate_password_report(pwd)
        print(report)

    # 3. HIBP
        count = check_hibp(pwd)
        if count > 0:
            print(f"⚠️ This password was found {count} times in data breaches!")
            verdict = "Weak"
        else:
            print("✅ This password was NOT found in known leaks.")

     # Final result
        print("\n--- Final Verdict ---")
        if (verdict == "Weak")  or (count > 0):
            print(f"🔐 Password Strength: **{verdict}**")
            print("❌ NOT SAFE: Please choose another password.")
            print("Do you want us to generate a strong password for you? (y/n)")
            choice = input("> ").lower()
            if choice == 'y':
                strong_pwd = generate_strong_password()
                print("\n🔑 Suggested strong password:", strong_pwd)

        elif (verdict == "Medium"):
            print(f"🔐 Password Strength: **{verdict}**")
            print("⚠️ Improve by fixing the failed checks above (e.g., add length/specials/remove sequences).")
            print("Do you want us to generate a strong password for you? (y/n)")
            choice = input("> ").lower()
            if choice == 'y':
                strong_pwd = generate_strong_password()
                print("\n🔑 Suggested strong password:", strong_pwd)
        else:
            print(f"🔐 Password Strength: **{verdict}**")
            print("🎉 Excellent! Your password looks strong.")
            print("\n⚠️  However, keep in mind:")
            print("Even strong passwords can sometimes be predictable if they contain")
            print("personal information (birthdays, names, favorite words, etc.).")
            print("Attackers can use social engineering or leaked data to guess them.")
            print("\n🔑 To guarantee maximum security, we recommend using a randomly")
            print("generated password instead.")
            print("Do you want us to generate a strong password for you? (y/n)")
            choice = input("> ").lower()
            if choice == 'y':
                strong_pwd = generate_strong_password()
                print("\n🔑 Suggested strong password:", strong_pwd)
    except KeyboardInterrupt:
        print("\n❌ Aborted by user.")
        sys.exit(0)