# Email Unsubscribe Automation

A Python script that automatically finds and triggers unsubscribe links from emails in your Gmail inbox.

## Prerequisites

First, install the required dependencies:
```bash
pip install python-dotenv
pip install beautifulsoup4
pip install requests
```

## Setup

1. Create a `.env` file in your project root with your Gmail credentials:
```
EMAIL=your.email@gmail.com
PASSWORD=your_app_specific_password
```

**Important**: For security, you must use an App-Specific Password from Google:
1. Enable 2-Step Verification in your Google Account
2. Go to [Google Account Security](https://myaccount.google.com/security)
3. Generate an App Password under "2-Step Verification"
4. Use this generated password in your `.env` file

## How It Works

The script performs the following operations:
1. Connects to Gmail using IMAP
2. Searches for emails containing "unsubscribe"
3. Extracts unsubscribe links from HTML content
4. Automatically visits each unsubscribe link
5. Saves all found links to `links.txt`

## Usage

Simply run the script:
```bash
python main.py
```

## Features

- Secure credential management using environment variables
- Handles both multipart and single-part emails
- Supports multiple character encodings (UTF-8, Latin-1, CP1252)
- Saves all unsubscribe links for reference
- Error handling for failed link visits

## File Structure
```
├── main.py
├── .env
└── links.txt (generated)
```

## Security Notes

- Never commit your `.env` file to version control
- Add it to your `.gitignore`:
```
.env
links.txt
```

## Limitations

- Only works with Gmail accounts
- Requires "Less secure app access" or App-Specific Password
- Some unsubscribe links may require manual interaction
- Some websites may block automated requests

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
