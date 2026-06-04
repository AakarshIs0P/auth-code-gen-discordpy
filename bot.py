import os
import json
import time

import discord
import pyotp
from cryptography.fernet import Fernet

TOKEN = "YOUR_BOT_TOKEN"
KEY_FILE = "encryption.key"
DATA_FILE = "totp_secrets.json"


def get_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()

    key = Fernet.generate_key()

    with open(KEY_FILE, "wb") as f:
        f.write(key)

    return key


cipher = Fernet(get_key())


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


def encrypt(secret):
    return cipher.encrypt(secret.encode()).decode()


def decrypt(secret):
    return cipher.decrypt(secret.encode()).decode()


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not isinstance(message.channel, discord.DMChannel):
        return

    parts = message.content.strip().split()

    if not parts:
        return

    user_id = str(message.author.id)
    command = parts[0].lower()

    data = load_data()
    entries = data.get(user_id, {})

    if command == "!add" and len(parts) == 3:
        name = parts[1].lower()
        secret = parts[2].upper()

        try:
            pyotp.TOTP(secret).now()
        except Exception:
            await message.channel.send("❌ Invalid TOTP secret.")
            return

        entries[name] = encrypt(secret)
        data[user_id] = entries
        save_data(data)

        await message.channel.send(f"✅ Saved `{name}`.")

    elif command == "!code" and len(parts) == 2:
        name = parts[1].lower()

        if name not in entries:
            await message.channel.send(f"❌ `{name}` not found.")
            return

        secret = decrypt(entries[name])
        code = pyotp.TOTP(secret).now()
        remaining = 30 - (time.time() % 30)

        await message.channel.send(
            f"🔐 **{name}**: `{code}` ({int(remaining)}s left)"
        )

    elif command == "!list":
        if not entries:
            await message.channel.send("No saved entries.")
            return

        await message.channel.send(
            "**Saved entries:**\n" +
            "\n".join(f"• `{name}`" for name in entries)
        )

    elif command == "!delete" and len(parts) == 2:
        name = parts[1].lower()

        if name not in entries:
            await message.channel.send(f"❌ `{name}` not found.")
            return

        del entries[name]
        data[user_id] = entries
        save_data(data)

        await message.channel.send(f"🗑️ Deleted `{name}`.")

    elif command == "!help":
        await message.channel.send(
            "**Commands**\n"
            "`!add <name> <secret>`\n"
            "`!code <name>`\n"
            "`!list`\n"
            "`!delete <name>`"
        )


client.run(TOKEN)