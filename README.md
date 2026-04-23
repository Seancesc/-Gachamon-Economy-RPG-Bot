# 🎮 Gachamon Economy RPG Bot

A Discord game bot that combines gacha mechanics, creature collection, economy, and battle into a single RPG experience.

---

## 📖 Description

Gachamon Economy RPG is a Discord bot where users can roll gacha to obtain creatures and items, collect them, sell them for money, and use creatures to battle other players. The bot features an economy system as the core of player progression.

---

## 🚀 Main Features

### 💰 Economy System

* /balance — check your money
* /daily — claim daily rewards
* /work — earn extra money
* /transfer — send money to other users

---

### 🎰 Gacha System

* /roll pet — roll for creatures
* /roll item — roll for items
* rarity system (Common, Rare, Epic, Legendary)

---

### 🎒 Inventory & Collection

* /pets — view owned creatures
* /inventory — view items
* /index — view all discovered creatures

---

### 💸 Sell System

* /sell pet — sell creatures
* /sell item — sell items

---

### ⚔️ Battle System

* /battle — fight other users
* turn-based combat
* each creature has stats (HP ❤️, ATK ⚔️, DEF 🛡️, SPD ⚡)

---

### 🎲 Gambling

* /gamble — bet money with random outcomes

---

## 📂 Project Structure

```id="3m6y3g"
project/
│
├── main.py
├── database.db
│
├── cogs/
│   ├── economy.py
│   ├── gacha.py
│   ├── inventory.py
│   ├── battle.py
│   ├── gamble.py
│
├── data/
│   ├── pets_data.py
│   ├── items_data.py
│
├── utils/
│   ├── db.py
│   ├── gacha_logic.py
│   ├── battle_logic.py
```

---

## 🗄️ Database

Uses SQLite with main tables:

* users (user_id, money, exp, level)
* pets (id, user_id, name, rarity, stats)
* inventory (user items)
* index (creature collection log)

---

## ⚙️ How to Run

1. Install dependencies:

```id="5vfbj2"
pip install discord.py
```

2. Run the bot:

```id="gyd2y1"
python main.py
```

3. Insert your bot token in main.py

---

## 🎯 Rarity System

* Common 🟢 — 60%
* Rare 🔵 — 25%
* Epic 🟣 — 10%
* Legendary 🟡 — 5%

---

## 🔄 Gameplay Loop

roll → obtain → collect → sell or battle → earn money → roll again

---

## 🔮 Future Plans

* pet leveling 📈
* evolution system 🧬
* leaderboard 🏆
* quest system 📜
* shop system 🛒

---

## 🎯 Project Goal

To create a Discord bot that feels like a game:

* progression 📊
* collection 📚
* strategy ⚔️
* luck-based mechanics 🎰

---

## 📝 Notes

SQLite is recommended for data storage as it is more stable than JSON for larger projects.

---

## 👤 Author

This project is created for learning and developing a game-based Discord bot.
