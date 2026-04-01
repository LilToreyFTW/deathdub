# Regenerative Addresses Tool

A GUI tool for generating and regenerating various types of addresses on Linux systems.

## Features

- **IPv4 Addresses**: Generate random IPv4 addresses
- **IPv6 Addresses**: Generate random IPv6 addresses  
- **MAC Addresses**: Generate random MAC addresses
- **Email Addresses**: Generate random email addresses
- **Phone Numbers**: Generate random phone numbers (US format)
- **UUIDs**: Generate random UUIDs
- **Bitcoin Addresses**: Generate mock Bitcoin address-like strings
- **SSH Key Fingerprints**: Generate mock SSH key fingerprints

## Options

- **Quantity**: Generate 1-100 addresses at once
- **Seed**: Optional seed for reproducible generation
- **Format**: Output in Plain, JSON, CSV, or Hex format
- **Copy to Clipboard**: Easy copying of generated addresses

## Requirements

- Python 3.x
- tkinter (usually included with Python)

## Installation & Usage

1. Make the script executable:
   ```bash
   chmod +x regenerative-addresses.py
   ```

2. Run the application:
   ```bash
   ./regenerative-addresses.py
   ```
   
   Or:
   ```bash
   python3 regenerative-addresses.py
   ```

## GUI Interface

The tool features a dark-themed GUI with:
- Address type selection dropdown
- Quantity and seed options
- Format selection
- Results display area
- Copy to clipboard functionality
- Status bar for feedback

## Security Note

- Bitcoin addresses and SSH fingerprints are mock/placeholder values
- Not suitable for production cryptographic purposes
- Use for testing, development, or educational purposes only
