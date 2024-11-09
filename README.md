# Vigenère Cipher TUI Tool

A powerful, interactive Vigenère Cipher tool built with Python. This tool allows for encryption, decryption, and automatic decryption of messages using various cryptanalysis techniques, all within a text-based user interface (TUI) powered by the `rich` library.

## Features

- **Encrypt**: Encrypt plaintext using a specified keyword.
- **Decrypt**: Decrypt ciphertext using a specified keyword.
- **Auto-Decrypt**: Attempt to decrypt ciphertext without a keyword using:
  - **Kasiski Examination** for identifying probable key lengths.
  - **Friedman Test** to statistically estimate the key length.
  - **Frequency Analysis** to deduce individual keyword shifts.
  
## Requirements

- Python 3
- `rich` library for TUI elements.
  
## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jasonfan06/vigenere_cipher_tool.git
   cd vigenere_cipher_tool

## Demonstration
<img width="1515" alt="Screenshot 2024-11-09 at 12 42 26 AM" src="https://github.com/user-attachments/assets/1c55e4e4-4d8e-4b7c-ab89-8f16a2ff0f7e">
