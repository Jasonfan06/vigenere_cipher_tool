# Vigenère Cipher TUI Tool

A no-nonsense, interactive tool for encrypting, decrypting, and breaking Vigenère ciphers. Built with Python and the `rich` library for a smooth text-based user interface (TUI). Perfect for anyone interested in cryptography or just looking to mess around with ciphers.

## Features

- **Encrypt**: Give it some text and a keyword, and it’ll spit out the encrypted result.
- **Decrypt**: Feed it an encrypted message with the correct keyword, and it’ll decrypt it for you.
- **Auto-Decryption**: Don’t have the keyword? No problem. This tool will take a shot at breaking the cipher for you using:
  - **Kasiski Examination**: Finds repeating patterns to guess the key length.
  - **Friedman Test**: Statistical analysis to estimate key length.
  - **Frequency Analysis**: Uses English letter frequency to figure out the keyword shifts.
  - **NOTE**: This doesn’t guarantee 100% decryption. Generally, the longer the ciphertext, the better the chances of finding the correct text.
## Requirements

- **Python 3**
- **rich** library for the TUI display.
  
## Setup

1. **Clone This Repository**
   ```bash
   git clone https://github.com/jasonfan06/vigenere_cipher_tool.git
   cd vigenere_cipher_tool

## Demonstration
<img width="1515" alt="Screenshot 2024-11-09 at 12 42 26 AM" src="https://github.com/user-attachments/assets/1c55e4e4-4d8e-4b7c-ab89-8f16a2ff0f7e">
