#!/bin/bash

echo "🔵 نصب ربات مدیریت Hetzner..."

read -p "ایدی عددی ادمین: " admin
read -p "توکن ربات تلگرام: " bot
read -p "Hetzner API Token: " hetzner

cat > config.json <<EOF
{
    "admin_id": $admin,
    "bot_token": "$bot",
    "hetzner_token": "$hetzner"
}
EOF

echo "📦 نصب پیش‌نیازها..."
apt update -y
apt install -y python3 python3-pip

pip3 install -r requirements.txt

echo "🔄 ساخت سرویس..."
cat > /etc/systemd/system/hetznerbot.service <<EOF
[Unit]
Description=Hetzner Telegram Bot
After=network.target

[Service]
ExecStart=/usr/bin/python3 $(pwd)/bot.py
WorkingDirectory=$(pwd)
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable hetznerbot
systemctl restart hetznerbot

echo "✅ نصب کامل شد!"
