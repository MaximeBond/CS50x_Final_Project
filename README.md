# **ALIEN GAME**

## 🎬 Video Demo:  
<URL HERE> https://youtu.be/npPKhyxz8l0

## 📖 Description:

**Alien Game** is a **2D arcade-style game** and an **improved version** of a project initially built with **Scratch**.  
👉 [Original Scratch Project](https://scratch.mit.edu/projects/1065060280)

The game takes place **inside a spaceship**, where a **spaceman** is trying to **escape from a deadly alien (xenomorph)**. The player controls the **spaceman**, who can move freely and **shoot lasers** to eliminate the alien before getting caught.  

### 🎮 **Gameplay Mechanics**
- The **spaceman** can move **up, down, left, and right** using the **arrow keys (↑ ↓ ← →)**.
- The **'S' key** allows the spaceman to **shoot a laser** in his current direction.
- The **alien chases** the spaceman, trying to reach and deplete his life points.
- The **spaceman starts with 100 HP**, while the **alien starts with 10 HP**.
- **Each laser hit on the alien** reduces its life points by **1**.
- **If the alien touches the spaceman**, he loses **life points** over time.
- The game ends when **either the spaceman or the alien reaches 0 HP**.

---

## 📁 **Project Structure**
This project contains several files:

| File | Description |
|------|------------|
| `alien_v1.py` | The **main script** that runs the game. |
| `testing.py` | A simple script used for testing different **images, animations (jumping), and text positions**. |
| `test_font.py` | A reusable script that **displays all available fonts in Pygame**. Useful for testing font selection. |
| `best_time.txt` | Stores the **shortest time** the player took to eliminate the alien. |
| `sup.otf` | The **font** used for the game’s title. |
| `media/` | Folder containing **images, music, and background assets**.|

---

## 🚀 **How to Run the Game**
### **1️⃣ Install Dependencies**
Ensure you have **Python** and **Pygame** installed.  
If you don’t have Pygame, install it using:

```sh
pip install pygame
```

### **2️⃣ Run the Main Script**
Execute the game script:

```sh
python alien_v1.py
```

The game window should launch automatically.

---

## 🖼️ **Game Assets**
The game uses various **images and sounds** stored in the `media/` folder, including:
- **Character Sprites:** `spaceman.png`, `alien.png`, `angry_alien.png`
- **Backgrounds:** `nostromo.jpg` (intro), `spaceship.jpg` (gameplay)
- **Music:** `game_on.mp3`, `disco-boogie.mp3`, `game_over.mp3`
- **End Screens:** `win.png`, `game_over.png`

> 📝 Note: Some images (`win.png`, `game_over2.png`) were generated with **ChatGPT**, while others were **found online**.

---

## 🛠️ **Game Functions Explained**
### **🟢 `show_intro_screen()`**
📌 **Displays the introduction screen before the game starts.**  
- Shows the **game title** and **instructions**.
- Displays the **best time** if available.
- Waits for the player to **press SPACE** to start.

### **🟢 `run_game()`**
📌 **Main game loop where the action happens.**  
- Initializes the game environment.
- Handles **player movement** and **laser shooting**.
- Controls **alien movement** and AI behavior.
- Detects **collisions between lasers and the alien**.
- Updates the **game timer and best time records**.
- Ends the game when **either the spaceman or alien loses all HP**.

### **🟢 `show_end_screen(message, integer)`**
📌 **Displays the game-over screen when the game ends.**  
- If the spaceman **wins**, it shows a **success message**.
- If the alien **wins**, it shows a **"Game Over"** screen.
- Lets the player **restart (SPACE) or quit (Q)**.

### **🟢 `check_files()`**
📌 **Ensures all necessary game files exist before launching.**  
- If a file is missing, it shows an **error message in a Pygame window**.
- Prevents the game from **crashing due to missing assets**.
- Lists the missing files and waits for user confirmation before exiting.

---

## ⏳ **Game Scoring & Best Time**
The game **records the fastest time** taken to eliminate the alien.  
- This time is **saved in `best_time.txt`**.
- On each playthrough, if the player **beats the previous record**, the new time is **saved automatically**.

---

## 🏆 **Features**
### ✅ **Pygame-Based Graphics & Animations**
- Smooth **character movement** and **collision detection**.
- High-quality **background images** and **sprite scaling**.

### ✅ **Dynamic Alien AI**
- The **alien moves towards the spaceman** dynamically.
- If shot, it **stops temporarily** before resuming the chase.

### ✅ **Enhanced Error Handling**
- **Missing files?** No problem! The game now **warns the user** instead of crashing.

---

## 🏆 **Room for improvement**
- Object Oriented Programming (OOP) instead of procedural code
- Improve the gameplay, add levels, increase difficulty ... 

---

## 📜 **License**
This project is licensed under the **MIT License**. 

### ⚠️ What This Means:
- You are **free to use, modify, and distribute** this code.
- You **must include the original license** in any distribution.
- The author **provides no warranty** for the software.

For more details, see the `LICENSE.md` file.

---

## 🔥 **Enjoy the game and have fun blasting aliens!** 👾💥
