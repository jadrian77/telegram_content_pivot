
<h1 align="center">Telegram Content Pivot</h1>

<p align="center">
<a href="https://github.com/jadrian77/telegram_content_pivot/blob/master/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
<a href="https://github.com/python/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

### Overview:
Use a telegram bot to parse the received telegram message link, repackage the content of the message and send it back to the user.

### Support Table:
| Category | Support |
|--|--|
|media types| video, photo, voice, audio, document|

## Installation

```sh
git clone https://github.com/jadrian77/telegram_content_pivot.git
cd telegram_content_pivot
pip3 install -r requirements.txt
```

Using a Python virtual environment is highly recommended but not required:
before `pip3 install -r requirements.txt` use

```sh
python3 -m venv venv
source venv/bin/activate
```

## Configuration

All the configurations are passed to the Telegram Content Pivot via `config.yaml` file.

### Setup Configuration

1. Copy `config.yaml.example` to `config.yaml`:
   ```sh
   cp config.yaml.example config.yaml
   ```
2. Update the values in `config.yaml` with your specific details (API keys, Bot token, etc.).

**Getting your API Keys:**

  - **create api_id & api_hash :**
    1. Log in to [Telegram API Platform](https://my.telegram.org/)
    2. Navigate to [API Development Tools](https://my.telegram.org/apps) to create a new application
    3. Submit application details

  - **Generate bot_token**
    - Open a chat conversation with botfather, create a bot via [@BotFather](https://t.me/BotFather) and follow setup instructions  


## Execution

```sh
python3 main.py
```

### Package and exeution

```sh
bash package.sh
cd dist
./telegram_content_pivot
```

## Proxy
`socks4, socks5, http` proxies are supported in this project currently. To use it, add the following to the bottom of your `config.yaml` file

```yaml
proxy:
  scheme: socks5
  hostname: 127.0.0.1
  port: 1234
  username: your_username
  password: your_password
```
If your proxy doesn’t require authorization you can omit username and password. Then the proxy will automatically be enabled.