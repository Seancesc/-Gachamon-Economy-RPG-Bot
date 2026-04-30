import random

# ================= PET DATA =================
pets_data = [
    ("Anjing", "Common", 60),
    ("Kucing", "Common", 60),
    ("Ayam", "Common", 60),
    ("Kambing", "Common", 60),

    ("Serigala", "Rare", 25),
    ("Harimau", "Rare", 25),
    ("Elang", "Rare", 25),
    ("Hiu", "Rare", 25),

    ("Singa", "Epic", 10),
    ("Buaya", "Epic", 10),

    ("Naga", "Legendary", 5),
    ("Phoenix", "Legendary", 5),
]

# ================= ITEM DATA =================
items_data = [
    ("Kayu", "Common", 60),
    ("Batu", "Common", 60),

    ("Besi", "Rare", 25),
    ("Emas", "Rare", 25),

    ("Diamond", "Epic", 10),

    ("Crystal", "Legendary", 5),
]

# ================= PRICE =================
rarity_price = {
    "Common": 50,
    "Rare": 150,
    "Epic": 300,
    "Legendary": 1000
}

# ================= EMOJI =================
rarity_emoji = {
    "Common": "⚪",
    "Rare": "🔵",
    "Epic": "🟣",
    "Legendary": "🟡"
}

def get_emoji(rarity):
    return rarity_emoji.get(rarity, "⚪")

def get_price(rarity):
    return rarity_price.get(rarity, 50)

# ================= GACHA (WEIGHTED) =================
def weighted_choice(data):
    total = sum(x[2] for x in data)
    r = random.randint(1, total)
    upto = 0
    for item in data:
        if upto + item[2] >= r:
            return item
        upto += item[2]

def roll_pet():
    return weighted_choice(pets_data)

def roll_item():
    return weighted_choice(items_data)

# ================= GAMBLE =================
def coin_flip():
    return random.choice(["heads", "tails"])

slot_symbols = ["🍒", "🍋", "🔔", "💎", "7️⃣"]

def spin_slot():
    return [random.choice(slot_symbols) for _ in range(3)]

def check_jackpot(result, bet):
    a, b, c = result
    if a == b == c:
        return bet * 5, "🔥 JACKPOT x5"
    elif a == b or b == c or a == c:
        return bet * 2, "✨ Win x2"
    else:
        return -bet, "❌ Lose"

# ================= LEVEL =================
def add_exp(level, exp, gained):
    exp += gained
    leveled = False

    while exp >= 100:
        exp -= 100
        level += 1
        leveled = True

    return level, exp, leveled

# ================= EVOLUTION =================
evolution_map = {
    "Anjing": ("Serigala", 5),
    "Serigala": ("Singa", 10),
    "Kucing": ("Harimau", 5),
    "Harimau": ("Naga", 15),
}

def check_evolution(name, level):
    if name in evolution_map:
        evo, req = evolution_map[name]
        if level >= req:
            return evo
    return None

# ================= BATTLE =================
def calculate_win_chance(player, enemy):
    chance = 50 + (player - enemy) * 5
    return max(20, min(80, chance))

def do_battle(player_level):
    enemy = random.randint(max(1, player_level-2), player_level+2)
    chance = calculate_win_chance(player_level, enemy)
    roll = random.randint(1, 100)
    return roll <= chance, enemy, chance