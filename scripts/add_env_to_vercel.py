#!/usr/bin/env python3
"""
Автоматическое добавление environment variables в Vercel
"""
import subprocess
import os
import re

TOKEN = "TVO0VjVBuWcaDgLB8Biojfkn"

# Читаем .env файл
env_vars = {}
with open('.env', 'r') as f:
    for line in f:
        line = line.strip()
        # Пропускаем комментарии и пустые строки
        if not line or line.startswith('#'):
            continue

        # Парсим KEY=VALUE
        match = re.match(r'([A-Z_]+)=(.+)', line)
        if match:
            key, value = match.groups()
            env_vars[key] = value.strip()

print(f"📋 Найдено {len(env_vars)} переменных в .env")
print()

# Важные переменные для Vercel (остальные не нужны на serverless)
important_vars = [
    'SUPABASE_URL',
    'SUPABASE_ANON_KEY',
    'SUPABASE_SERVICE_ROLE_KEY',
    'ENSEMBLE_API_TOKEN',
    'OPENAI_API_KEY',
    'PERPLEXITY_API_KEY',
    'STRIPE_API_KEY',
    'STRIPE_PRICE_ID',
    'STRIPE_WEBHOOK_SECRET',
]

for key in important_vars:
    if key not in env_vars:
        print(f"⚠️  {key} не найден в .env")
        continue

    value = env_vars[key]
    print(f"➕ Добавляю {key}...")

    # Добавляем для production
    try:
        proc = subprocess.Popen(
            ['vercel', 'env', 'add', key, 'production', '--token', TOKEN],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(input=f"{value}\n")

        if proc.returncode == 0:
            print(f"   ✅ Production")
        else:
            print(f"   ⚠️  Production (возможно уже существует)")

    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    # Добавляем для preview
    try:
        proc = subprocess.Popen(
            ['vercel', 'env', 'add', key, 'preview', '--token', TOKEN],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(input=f"{value}\n")

        if proc.returncode == 0:
            print(f"   ✅ Preview")
        else:
            print(f"   ⚠️  Preview (возможно уже существует)")

    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

print()
print("✅ Готово! Проверяю результат...")
print()

# Проверяем что добавилось
result = subprocess.run(
    ['vercel', 'env', 'ls', '--token', TOKEN],
    capture_output=True,
    text=True
)
print(result.stdout)
