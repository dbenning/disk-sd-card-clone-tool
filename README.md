# 🚀 SD Card Cloner for macOS

Clone your SD cards like a wizard 🧙‍♂️ — no more cryptic commands or risky terminal typos!

This project includes **two simple Python scripts** that help you:

- 🧱 **Create an image** of an SD card (`create_sd_image.py`)
- 🔁 **Write that image** to another SD card (`write_sd_image.py`)

Perfect for:
- Backing up Raspberry Pi cards 🥧
- Creating bootable duplicates 🧯
- General SD card cloning sorcery ✨

---

## ⚙️ Requirements

- **macOS** (Tested on Monterey, Ventura, and Sonoma)
- **Python 3.x**
- **Admin privileges** (used for `dd` via `sudo`)
- A basic comfort level using Terminal 🧑‍💻

> You do **not** need any Python packages beyond the standard library.

---

## 📦 Files Included

| File                | Description |
|---------------------|-------------|
| `create_sd_image.py` | Create a `.img` file from a selected disk |
| `write_sd_image.py`  | Write a `.img` file to a selected disk |

---

## 🧱 Step 1: Create an Image from an SD Card

This script reads a full SD card and clones it to a `.img` file.

### 🔧 Run the script:
```python3 create_sd_image.py```

```python3 write_sd_image.py```
