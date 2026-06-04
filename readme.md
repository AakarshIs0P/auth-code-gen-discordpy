Discord TOTP Bot

A simple Discord bot that stores encrypted TOTP secrets and generates 2FA authentication codes through direct messages.

Features

- Store multiple TOTP secrets
- Per-user encrypted storage
- Generate current 6-digit authentication codes
- List saved entries
- Delete saved entries
- DM-only access for privacy

Requirements

- Python 3.10+
- Discord Bot Token

Installation

Clone the repository:

git clone <repository-url>
cd <repository-name>

Install dependencies:

pip install -r requirements.txt

Edit the bot token inside the source code:

TOKEN = "YOUR_BOT_TOKEN"

Run the bot:

python bot.py

Commands

Add a TOTP Secret

!add <name> <secret>

Example:

!add github JBSWY3DPEHPK3PXP

Generate a Code

!code <name>

Example:

!code github

List Saved Entries

!list

Delete an Entry

!delete <name>

Example:

!delete github

Help

!help

Files

File| Purpose
bot.py| Main bot file
encryption.key| Encryption key used for stored secrets
totp_secrets.json| Encrypted user data

Security Notes

- Secrets are encrypted before being stored.
- The encryption key is stored locally in "encryption.key".
- Anyone with access to both "encryption.key" and "totp_secrets.json" can decrypt stored secrets.
- Keep these files secure and never share them publicly.

Dependencies

discord.py
pyotp
cryptography

Disclaimer

This project is intended for personal use and educational purposes. Review the code and security model before using it to store important authentication secrets.