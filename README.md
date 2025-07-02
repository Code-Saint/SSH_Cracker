# 🔐 SSH Brute-Force Cracker – Offensive Security Tool

## 🧠 Overview

This is a custom-built **SSH brute-force attack tool** written in Python. It automates login attempts on a remote SSH server by using a **username-password wordlist**. The tool is built to help cybersecurity learners understand how brute-force attacks work, how to detect and prevent them, and how authentication over SSH can be tested in ethical environments.

> ⚠️ This project is for **educational and authorized use only**. Do not use this tool against any system without explicit permission.

---

## ⚙️ Features

- 🔁 Attempts SSH login using a **username and password list**
- 🚫 Handles incorrect credentials and **authentication exceptions**
- 🧵 **Multi-threaded** design for faster cracking
- 🧪 Logs successful login credentials
- ⚡ Supports **port customization** and optional delay

---

## 🛠️ Technologies Used

- Python 3.x
- `paramiko` – for SSH connection handling
- `threading` – to parallelize brute-force attempts
- `argparse` – for command-line argument parsing

---

## 🚀 Usage

```bash
python3 ssh_cracker.py -H 192.168.1.10 -u root -P passwords.txt -t 5
```
