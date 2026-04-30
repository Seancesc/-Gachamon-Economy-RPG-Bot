import discord
from discord.ext import commands
import sqlite3
import time
import asyncio
from utils.logic import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ================= DATABASE =================
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    money INTEGER DEFAULT 500,
    last_daily INTEGER DEFAULT 0,
    last_train INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    rarity TEXT,
    level INTEGER DEFAULT 1,
    exp INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    rarity TEXT
)
""")

conn.commit()

def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()

# ================= START =================
@bot.command()
async def start(ctx):
    await ctx.send(f"""
╔════════════════════════════╗
   🎮✨ GACHAMON RPG ✨🎮
╚════════════════════════════╝

👤 {ctx.author.name}

🎰 !rollpet untuk mulai
📜 !help untuk command

💰 500 coins awal
🔥 Jadi yang terkuat!
""")

# ================= HELP =================
@bot.command()
async def help(ctx):
    await ctx.send("""
🎮 COMMAND LIST

💰 !balance !daily
🎰 !rollpet !rollitem
🐾 !pets !items
💸 !sellpet <id> !sellitem <id>
📈 !train <id> !fight <id>
🎲 !coinflip heads/tails <coin>
🎰 !jackpot <coin>
""")

# ================= ECON =================
@bot.command()
async def balance(ctx):
    get_user(ctx.author.id)
    cursor.execute("SELECT money FROM users WHERE user_id=?", (ctx.author.id,))
    await ctx.send(f"💰 {cursor.fetchone()[0]} coins")

@bot.command()
async def daily(ctx):
    get_user(ctx.author.id)
    cursor.execute("SELECT last_daily FROM users WHERE user_id=?", (ctx.author.id,))
    last = cursor.fetchone()[0]
    now = int(time.time())

    if now - last < 86400:
        await ctx.send("❌ Sudah claim")
        return

    cursor.execute("UPDATE users SET money=money+200,last_daily=? WHERE user_id=?", (now, ctx.author.id))
    conn.commit()
    await ctx.send("🎁 +200 coins")

# ================= ROLL =================
@bot.command()
async def rollpet(ctx):
    msg = await ctx.send("🎰 Rolling pet...")
    await asyncio.sleep(3)

    name, rarity, _ = roll_pet()
    cursor.execute("INSERT INTO pets (user_id,name,rarity) VALUES (?,?,?)",
                   (ctx.author.id, name, rarity))
    conn.commit()

    await msg.edit(content=f"{get_emoji(rarity)} {name} ({rarity})")

@bot.command()
async def rollitem(ctx):
    msg = await ctx.send("🎰 Rolling item...")
    await asyncio.sleep(3)

    name, rarity, _ = roll_item()
    cursor.execute("INSERT INTO items (user_id,name,rarity) VALUES (?,?,?)",
                   (ctx.author.id, name, rarity))
    conn.commit()

    await msg.edit(content=f"{get_emoji(rarity)} {name} ({rarity})")

# ================= VIEW =================
@bot.command()
async def pets(ctx):
    cursor.execute("SELECT id,name,rarity,level,exp FROM pets WHERE user_id=?", (ctx.author.id,))
    data = cursor.fetchall()

    if not data:
        await ctx.send("❌ Tidak ada pet")
        return

    msg = ""
    for p in data:
        msg += f"{get_emoji(p[2])} ID {p[0]} - {p[1]} Lv.{p[3]} ({p[4]}/100)\n"

    await ctx.send(msg)

@bot.command()
async def items(ctx):
    cursor.execute("SELECT id,name,rarity FROM items WHERE user_id=?", (ctx.author.id,))
    data = cursor.fetchall()

    if not data:
        await ctx.send("❌ Tidak ada item")
        return

    msg = ""
    for i in data:
        msg += f"{get_emoji(i[2])} ID {i[0]} - {i[1]}\n"

    await ctx.send(msg)

# ================= SELL =================
@bot.command()
async def sellpet(ctx, id:int):
    cursor.execute("SELECT rarity FROM pets WHERE id=? AND user_id=?", (id, ctx.author.id))
    pet = cursor.fetchone()

    if not pet:
        await ctx.send("❌ Tidak ada")
        return

    price = get_price(pet[0])

    cursor.execute("DELETE FROM pets WHERE id=?", (id,))
    cursor.execute("UPDATE users SET money=money+? WHERE user_id=?", (price, ctx.author.id))
    conn.commit()

    await ctx.send(f"💸 +{price}")

@bot.command()
async def sellitem(ctx, id:int):
    cursor.execute("SELECT rarity FROM items WHERE id=? AND user_id=?", (id, ctx.author.id))
    item = cursor.fetchone()

    if not item:
        await ctx.send("❌ Tidak ada")
        return

    price = get_price(item[0])

    cursor.execute("DELETE FROM items WHERE id=?", (id,))
    cursor.execute("UPDATE users SET money=money+? WHERE user_id=?", (price, ctx.author.id))
    conn.commit()

    await ctx.send(f"💸 +{price}")

# ================= COINFLIP =================
@bot.command()
async def coinflip(ctx, choice: str, amount: int):
    get_user(ctx.author.id)

    cursor.execute("SELECT money FROM users WHERE user_id=?", (ctx.author.id,))
    money = cursor.fetchone()[0]

    if amount > money:
        await ctx.send("❌ Uang kurang")
        return

    msg = await ctx.send("🪙 Melempar koin...")
    await asyncio.sleep(1)

    result = coin_flip()

    if result == choice.lower():
        change = amount
        text = "💰 MENANG!"
    else:
        change = -amount
        text = "❌ KALAH!"

    cursor.execute("UPDATE users SET money=money+? WHERE user_id=?", (change, ctx.author.id))
    conn.commit()

    await msg.edit(content=f"🪙 {result.upper()} | {text} ({change})")

# ================= JACKPOT =================
@bot.command()
async def jackpot(ctx, amount: int):
    msg = await ctx.send("🎰 Memutar...")

    for _ in range(3):
        spin = spin_slot()
        await msg.edit(content="🎰 " + " | ".join(spin))
        await asyncio.sleep(0.7)

    final = spin_slot()
    await msg.edit(content="🎰 " + " | ".join(final))

    change, text = check_jackpot(final, amount)

    cursor.execute("UPDATE users SET money=money+? WHERE user_id=?", (change, ctx.author.id))
    conn.commit()

    await ctx.send(f"{text} ({change})")

# ================= TRAIN =================
@bot.command()
async def train(ctx, id:int):
    get_user(ctx.author.id)

    cursor.execute("SELECT last_train FROM users WHERE user_id=?", (ctx.author.id,))
    last = cursor.fetchone()[0]
    now = int(time.time())

    if now - last < 180:
        await ctx.send(f"⏳ {180-(now-last)} detik lagi")
        return

    cursor.execute("SELECT name,level,exp FROM pets WHERE id=? AND user_id=?", (id, ctx.author.id))
    pet = cursor.fetchone()

    if not pet:
        await ctx.send("❌ Tidak ada")
        return

    name, level, exp = pet
    level, exp, _ = add_exp(level, exp, 50)

    evo = check_evolution(name, level)
    if evo:
        name = evo
        await ctx.send(f"✨ Evolution → {name}")

    cursor.execute("UPDATE pets SET name=?,level=?,exp=? WHERE id=?", (name, level, exp, id))
    cursor.execute("UPDATE users SET last_train=? WHERE user_id=?", (now, ctx.author.id))
    conn.commit()

    await ctx.send(f"📈 {name} Lv.{level} ({exp}/100)")

# ================= FIGHT =================
@bot.command()
async def fight(ctx, id:int):
    cursor.execute("SELECT name,level,exp FROM pets WHERE id=? AND user_id=?", (id, ctx.author.id))
    pet = cursor.fetchone()

    if not pet:
        await ctx.send("❌ Tidak ada")
        return

    name, level, exp = pet
    msg = await ctx.send("⚔️ Fighting...")
    await asyncio.sleep(2)

    win, enemy, chance = do_battle(level)

    if win:
        level, exp, _ = add_exp(level, exp, 25)

        evo = check_evolution(name, level)
        if evo:
            name = evo
            await ctx.send(f"✨ Evolution → {name}")

        cursor.execute("UPDATE pets SET name=?,level=?,exp=? WHERE id=?", (name, level, exp, id))
        conn.commit()

        await msg.edit(content=f"💥 MENANG vs Lv.{enemy}\n+25 EXP\nLv.{level} ({exp}/100)\nChance {chance}%")
    else:
        await msg.edit(content=f"❌ KALAH vs Lv.{enemy}\nChance {chance}%")

# ================= RUN =================
bot.run("Token")