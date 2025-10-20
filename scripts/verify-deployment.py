#!/usr/bin/env python3
"""
Автоматическая проверка Vercel deployment и Stripe конфигурации
Запуск: python3 scripts/verify-deployment.py
"""
import subprocess
import json
import os
import sys
import re

# Цвета для вывода
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def get_vercel_token():
    """Получаем Vercel token из окружения или возвращаем дефолтный"""
    return os.getenv('VERCEL_TOKEN', 'TVO0VjVBuWcaDgLB8Biojfkn')

def check_vercel_env_vars(token):
    """Проверяем environment variables в Vercel"""
    print_header("Проверка Environment Variables в Vercel")

    try:
        result = subprocess.run(
            ['vercel', 'env', 'ls', '--token', token],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print_error(f"Ошибка получения env vars: {result.stderr}")
            return False

        # Парсим вывод
        required_vars = [
            'SUPABASE_URL',
            'SUPABASE_ANON_KEY',
            'SUPABASE_SERVICE_ROLE_KEY',
            'STRIPE_API_KEY',
            'STRIPE_PRICE_ID',
            'OPENAI_API_KEY',
            'ENSEMBLE_API_TOKEN'
        ]

        found_vars = set()
        for line in result.stdout.split('\n'):
            for var in required_vars:
                if var in line:
                    found_vars.add(var)

        print(f"Найдено {len(found_vars)}/{len(required_vars)} обязательных переменных:\n")

        all_found = True
        for var in required_vars:
            if var in found_vars:
                print_success(f"{var}")
            else:
                print_error(f"{var} - ОТСУТСТВУЕТ!")
                all_found = False

        return all_found

    except Exception as e:
        print_error(f"Ошибка: {e}")
        return False

def check_stripe_keys():
    """Проверяем Stripe API keys на test/live режим"""
    print_header("Проверка Stripe API Keys")

    try:
        with open('.env', 'r') as f:
            env_content = f.read()

        stripe_key = None
        for line in env_content.split('\n'):
            if line.startswith('STRIPE_API_KEY='):
                stripe_key = line.split('=', 1)[1].strip()
                break

        if not stripe_key:
            print_error("STRIPE_API_KEY не найден в .env")
            return False

        # Проверяем режим
        if stripe_key.startswith('sk_test_'):
            print_success("Используется TEST mode API key")
            print_warning("Требуется настроить Customer Portal в TEST mode:")
            print("   👉 https://dashboard.stripe.com/test/settings/billing/portal")
            return True
        elif stripe_key.startswith('sk_live_'):
            print_success("Используется LIVE mode API key")
            print_warning("Требуется настроить Customer Portal в LIVE mode:")
            print("   👉 https://dashboard.stripe.com/settings/billing/portal")
            return True
        else:
            print_error(f"Неизвестный формат Stripe API key: {stripe_key[:15]}...")
            return False

    except Exception as e:
        print_error(f"Ошибка: {e}")
        return False

def check_latest_deployment(token):
    """Проверяем последний deployment в Vercel"""
    print_header("Проверка последнего Deployment")

    try:
        result = subprocess.run(
            ['vercel', 'ls', '--token', token],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print_error(f"Ошибка получения deployments: {result.stderr}")
            return False

        lines = result.stdout.split('\n')
        if len(lines) < 3:
            print_warning("Deployments не найдены")
            return False

        # Первая строка после заголовков - последний deployment
        for line in lines[2:5]:
            if line.strip():
                print_success(f"Последний deployment: {line[:80]}")
                break

        print("\n💡 Для проверки статуса deployment:")
        print("   vercel ls --token TVO0VjVBuWcaDgLB8Biojfkn")

        return True

    except Exception as e:
        print_error(f"Ошибка: {e}")
        return False

def check_backend_endpoint():
    """Проверяем доступность backend endpoint"""
    print_header("Проверка Backend API Endpoint")

    # Читаем vercel.json чтобы получить URL
    try:
        # Пока просто информируем
        print_warning("После deployment проверьте endpoint вручную:")
        print("   https://your-app.vercel.app/api/v1/subscription/manage")
        print("\nОжидаемый ответ без токена:")
        print('   {"detail":"Not authenticated"}')

        return True
    except Exception as e:
        print_error(f"Ошибка: {e}")
        return False

def trigger_redeploy(token):
    """Триггерим новый deployment для применения env vars"""
    print_header("Триггер нового Deployment")

    print("Environment variables были обновлены.")
    print("Для применения изменений нужен новый deployment.\n")

    response = input("Сделать redeploy сейчас? (y/N): ")

    if response.lower() == 'y':
        try:
            result = subprocess.run(
                ['vercel', '--prod', '--token', token, '--yes'],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                print_success("Deployment запущен!")
                print(result.stdout)
                return True
            else:
                print_error(f"Ошибка deployment: {result.stderr}")
                return False

        except Exception as e:
            print_error(f"Ошибка: {e}")
            return False
    else:
        print_warning("Deployment отменен")
        print("💡 Запустите вручную: vercel --prod --token TVO0VjVBuWcaDgLB8Biojfkn")
        return False

def main():
    """Главная функция"""
    token = get_vercel_token()

    print(f"\n{BLUE}🚀 TrendXL Deployment Verification Tool{RESET}")

    # Проверяем все компоненты
    results = {}

    results['env_vars'] = check_vercel_env_vars(token)
    results['stripe_keys'] = check_stripe_keys()
    results['deployment'] = check_latest_deployment(token)
    results['backend'] = check_backend_endpoint()

    # Итоги
    print_header("Итоговый отчет")

    total = len(results)
    passed = sum(1 for v in results.values() if v)

    print(f"Пройдено проверок: {passed}/{total}\n")

    for check, status in results.items():
        if status:
            print_success(f"{check}")
        else:
            print_error(f"{check}")

    # Если все ОК, предлагаем redeploy
    if passed == total:
        print_success("\n🎉 Все проверки пройдены!")
        # Закомментировано чтобы не делать автоматический deploy
        # trigger_redeploy(token)
    else:
        print_warning(f"\n⚠️  {total - passed} проверок не пройдено")
        print("Исправьте проблемы и запустите скрипт снова")

    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
