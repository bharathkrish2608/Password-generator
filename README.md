# Password Generator

Interactive CLI tool to generate random passwords with configurable length and optional symbols, give quick strength feedback, and optionally append results to `passwords.txt`.

## Features

- Guarantees upper, lower, digit, and (optionally) symbol inclusion in each password.
- Strength assessment with actionable tips when a password is weak.
- Batch generation of multiple passwords in one run.
- Optional saving of generated passwords to `passwords.txt`.

## Requirements

- Python 3.8+

## Usage

1. Run the script:
   ```bash
   python password_generator.py
   ```
2. Follow the prompts:
   - Desired length (minimum 4).
   - Include symbols? (Y/n)
   - How many passwords to generate?
3. For each password you will see:
   - The generated password.
   - A strength label (Strong/Medium/Weak).
   - Tips when the password is considered weak.
4. Choose whether to save generated passwords to `passwords.txt` (appends).
5. Choose whether to generate again.

## Web UI

- Install Flask and start the server:
  ```bash
  pip install -r requirements.txt
  python app.py
  ```
- Open http://127.0.0.1:8000 and use the form to generate passwords.
- Length and symbol options are sent to the Python backend; nothing is stored unless you copy it.

## Notes

- Symbol set used: `!@#$%^&*()-_=+[]{};:,.?/\|`
- Saved passwords are appended to `passwords.txt` in the project directory.
- If you prefer no symbols, answer `n` when prompted.
