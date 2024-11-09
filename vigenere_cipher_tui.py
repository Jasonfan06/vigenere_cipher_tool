#!/usr/bin/env python3
"""
Vigenère Cipher TUI Tool
Author: Jason Fan
Date: 2024

This tool provides encryption, decryption, and cryptanalysis (auto-decrypt) functionalities using the Vigenère Cipher.
It features a visually appealing text-based user interface (TUI) built with the Rich library.
"""

import sys
import string
from collections import Counter

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.box import ROUNDED
from rich.align import Align

console = Console()

LETTER_FREQUENCIES = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}

ALPHABET = string.ascii_uppercase

def vigenere_encrypt(plaintext, keyword):
    plaintext = ''.join([c.upper() for c in plaintext if c.isalpha()])
    keyword = keyword.upper()
    ciphertext = ''
    keyword_length = len(keyword)
    for i, char in enumerate(plaintext):
        shift = ord(keyword[i % keyword_length]) - ord('A')
        encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        ciphertext += encrypted_char
    return ciphertext

def vigenere_decrypt(ciphertext, keyword):
    ciphertext = ''.join([c.upper() for c in ciphertext if c.isalpha()])
    keyword = keyword.upper()
    plaintext = ''
    keyword_length = len(keyword)
    for i, char in enumerate(ciphertext):
        shift = ord(keyword[i % keyword_length]) - ord('A')
        decrypted_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
        plaintext += decrypted_char
    return plaintext

def get_factors(n):
    factors = set()
    for i in range(2, min(n, 21)):
        if n % i == 0:
            factors.add(i)
    return sorted(factors)

def kasiski_examination(ciphertext):
    sequences = {}
    for seq_len in range(3, 6):
        for i in range(len(ciphertext) - seq_len):
            seq = ciphertext[i:i+seq_len]
            if seq in sequences:
                sequences[seq].append(i)
            else:
                sequences[seq] = [i]
    spacings = []
    for seq, positions in sequences.items():
        if len(positions) > 1:
            for i in range(len(positions) - 1):
                spacing = positions[i+1] - positions[i]
                spacings.append(spacing)
    factors = []
    for spacing in spacings:
        factors.extend(get_factors(spacing))
    factor_counts = Counter(factors)
    probable_key_lengths = [factor for factor, count in factor_counts.items() if factor <= 20]
    probable_key_lengths = sorted(probable_key_lengths, key=lambda x: -factor_counts[x])
    return probable_key_lengths

def friedman_test(ciphertext):
    N = len(ciphertext)
    freq = Counter(ciphertext)
    IC = sum(f * (f - 1) for f in freq.values()) / (N * (N - 1)) if N > 1 else 0
    # Constants for English
    K_english = 0.065
    K_random = 0.0385
    if (IC - K_random) == 0:
        return 0
    k = (K_english - K_random) / (IC - K_random)
    return round(k)

def find_shift(segment):
    chi_squares = []
    for shift in range(26):
        decrypted = ''.join(
            [chr(((ord(c) - ord('A') - shift + 26) % 26) + ord('A')) for c in segment]
        )
        freq = Counter(decrypted)
        total = sum(freq.values())
        chi_sq = 0
        for letter in ALPHABET:
            observed = freq[letter] / total if total > 0 else 0
            expected = LETTER_FREQUENCIES[letter]
            chi_sq += ((observed - expected) ** 2) / expected if expected > 0 else 0
        chi_squares.append(chi_sq)
    min_shift = chi_squares.index(min(chi_squares))
    return min_shift

def frequency_analysis_decrypt(ciphertext, key_length):
    key = ''
    for i in range(key_length):
        nth_letters = ciphertext[i::key_length]
        shift = find_shift(nth_letters)
        key += chr(shift + ord('A'))
    plaintext = vigenere_decrypt(ciphertext, key)
    return key, plaintext

def display_banner():
    banner = """
      __     ___                   __              ____ _       _
      \\ \\   / (_) __ _  ___ _ __   \\_\\ _ __ ___   / ___(_)_ __ | |__   ___ _ __
       \\ \\ / /| |/ _` |/ _ \\ '_ \\ / _ \\ '__/ _ \\ | |   | | '_ \\| '_ \\ / _ \\ '__|
        \\ V / | | (_| |  __/ | | |  __/ | |  __/ | |___| | |_) | | | |  __/ |
         \\_/  |_|\\__, |\\___|_| |_|\\___|_|  \\___|  \\____|_| .__/|_| |_|\\___|_|
                 |___/                                   |_|
    """
    centered_banner = Align.center(Text(banner, style="bold green"))
    console.print(centered_banner)

def display_menu():
    menu = Table(show_header=False, box=ROUNDED, pad_edge=False)
    menu.add_row("[bold cyan]1.[/] Encrypt")
    menu.add_row("[bold magenta]2.[/] Decrypt")
    menu.add_row("[bold yellow]3.[/] Auto-Decrypt")
    menu.add_row("[bold red]4.[/] Exit")
    panel = Panel(
        Align.center(menu),
        title="[bold blue]Main Menu[/]",
        border_style="bright_blue",
        box=ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)

def encrypt_flow():
    console.print("\n[bold green]Encryption Process[/]", style="bold green")
    plaintext = Prompt.ask("\n[bold]Enter the plaintext to encrypt[/]")
    if not plaintext.strip():
        console.print("[bold red]Error:[/] Plaintext cannot be empty.", style="bold red")
        return
    keyword = Prompt.ask("[bold]Enter the keyword (letters only)[/]")
    if not keyword.isalpha():
        console.print("[bold red]Error:[/] Invalid keyword. Please enter letters only.", style="bold red")
        return
    ciphertext = vigenere_encrypt(plaintext, keyword)
    result_panel = Panel(
        Text(ciphertext, justify="center", style="bold blue"),
        title="[bold blue]Result[/]",
        border_style="bright_blue",
        padding=(1, 2)
    )
    console.print(result_panel)

def decrypt_flow():
    console.print("\n[bold green]Decryption Process[/]", style="bold green")
    ciphertext = Prompt.ask("\n[bold]Enter the ciphertext to decrypt[/]")
    if not ciphertext.strip():
        console.print("[bold red]Error:[/] Ciphertext cannot be empty.", style="bold red")
        return
    keyword = Prompt.ask("[bold]Enter the keyword (letters only)[/]")
    if not keyword.isalpha():
        console.print("[bold red]Error:[/] Invalid keyword. Please enter letters only.", style="bold red")
        return
    plaintext = vigenere_decrypt(ciphertext, keyword)
    result_panel = Panel(
        Text(plaintext, justify="center", style="bold blue"),
        title="[bold blue]Result[/]",
        border_style="bright_blue",
        padding=(1, 2)
    )
    console.print(result_panel)

def auto_decrypt_flow():
    console.print("\n[bold green]Auto-Decryption Process[/]", style="bold green")
    ciphertext = Prompt.ask("\n[bold]Enter the ciphertext to auto-decrypt[/]")
    if not ciphertext.strip():
        console.print("[bold red]Error:[/] Ciphertext cannot be empty.", style="bold red")
        return
    ciphertext = ''.join([c.upper() for c in ciphertext if c.isalpha()])
    if not ciphertext:
        console.print("[bold red]Error:[/] Ciphertext must contain alphabetic characters.", style="bold red")
        return

    console.print("\n[bold cyan]Performing Kasiski Examination...[/]", style="bold cyan")
    probable_key_lengths = kasiski_examination(ciphertext)
    if not probable_key_lengths:
        console.print("[bold yellow]Kasiski Examination failed to find repeating sequences.[/]", style="bold yellow")
        console.print("[bold cyan]Attempting Friedman Test...[/]", style="bold cyan")
        estimated_length = friedman_test(ciphertext)
        if estimated_length > 1:
            probable_key_lengths = [estimated_length]
            console.print(f"[bold green]Friedman Test estimated key length: {estimated_length}[/]", style="bold green")
        else:
            console.print("[bold red]Friedman Test failed to estimate key length.[/]", style="bold red")
            console.print("[bold red]Auto-Decryption unsuccessful.[/]", style="bold red")
            return
    else:
        console.print(f"[bold green]Probable key lengths from Kasiski Examination: {probable_key_lengths}[/]", style="bold green")

    console.print("\n[bold cyan]Attempting frequency analysis to deduce the key and decrypt the text...[/]", style="bold cyan")
    for key_length in probable_key_lengths:
        key, plaintext = frequency_analysis_decrypt(ciphertext, key_length)
        console.print(f"\n[bold blue]Attempting with key length {key_length}:[/]", style="bold blue")
        console.print(f"[bold magenta]Possible Key:[/] {key}", style="bold magenta")
        console.print(f"[bold magenta]Decrypted Text:[/]\n{plaintext}", style="bold magenta")
        confirmation = Prompt.ask("\n[bold]Does the decrypted text make sense? (y/n)[/]", choices=["y", "n"], default="n")
        if confirmation.lower() == 'y':
            console.print("\n[bold green]Auto-Decryption successful![/]", style="bold green")
            result_panel = Panel(
                Text(plaintext, justify="center", style="bold blue"),
                title=f"[bold blue]Result[/]",
                border_style="bright_blue",
                padding=(1, 2)
            )
            console.print(result_panel)
            return
    console.print("\n[bold red]Auto-Decryption unsuccessful. Unable to determine the correct key.[/]", style="bold red")

def main():
    display_banner()
    display_menu()
    choice = Prompt.ask("\n[bold]Please select an option (1-4):[/]", choices=["1", "2", "3", "4"])
    if choice == '1':
        encrypt_flow()
    elif choice == '2':
        decrypt_flow()
    elif choice == '3':
        auto_decrypt_flow()
    elif choice == '4':
        console.print("\n[bold red]Exiting the Vigenère Cipher Tool. Goodbye![/]", style="bold red")
        sys.exit()

    while True:
        again = Prompt.ask("\n[bold]Would you like to perform another action? (y/n)[/]", choices=["y", "n"], default="y")
        if again.lower() == 'y':
            display_menu()
            choice = Prompt.ask("\n[bold]Please select an option (1-4):[/]", choices=["1", "2", "3", "4"])
            if choice == '1':
                encrypt_flow()
            elif choice == '2':
                decrypt_flow()
            elif choice == '3':
                auto_decrypt_flow()
            elif choice == '4':
                console.print("\n[bold red]Exiting the Vigenère Cipher Tool. Goodbye![/]", style="bold red")
                sys.exit()
        else:
            console.print("\n[bold red]Exiting the Vigenère Cipher Tool. Goodbye![/]", style="bold red")
            sys.exit()

if __name__ == "__main__":
    main()
