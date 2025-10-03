# 🔧 СРОЧНОЕ ИСПРАВЛЕНИЕ: Stripe Mode Mismatch

## ❌ Проблема:
В `backend/.env` используется **Live API Key**, но Stripe MCP настроен на **Test Mode**.

## ✅ Быстрое решение:

### Вариант 1: Использовать Test Mode (РЕКОМЕНДУЕТСЯ для тестирования)

Замените в `backend/.env`:

```env
# Старое (Live):
STRIPE_API_KEY=sk_live_ваш_live_ключ_здесь

# Новое (Test):
STRIPE_API_KEY=sk_test_ваш_test_ключ_здесь
```

Получите Test key здесь:
👉 https://dashboard.stripe.com/test/apikeys

---

### Вариант 2: Создать Live Price (для реальных платежей)

1. Откройте Stripe Dashboard в **Live Mode**:
   👉 https://dashboard.stripe.com/dashboard

2. Переключитесь на Live (toggle справа вверху)

3. Создайте новую цену:
   - Перейдите в Products → `TrendXL Pro`
   - Добавьте новую цену: **$49.00 / month**
   - Скопируйте новый Price ID (начинается с `price_`)

4. Обновите `backend/.env`:
   ```env
   STRIPE_PRICE_ID=price_xxxxxxxxxxxxxxxxxxxxx
   ```

---

## 🧪 Сейчас настроено для Test Mode:

```env
STRIPE_PRICE_ID=price_1SEAUHGfnGEnyXLEwLlxed1j  # Test mode, $49/month
```

**Payment Link (Test)**: https://buy.stripe.com/test_bJeeVdetsffIda5bdCefC03

### Тестовая карта:
```
Номер: 4242 4242 4242 4242
CVV: любые 3 цифры
Дата: любая будущая
```

---

## 🚀 Что делать дальше:

### Для тестирования:
1. Получите Test API key из Stripe Dashboard
2. Замените в `backend/.env`
3. Перезапустите backend
4. Тестируйте с картой `4242 4242 4242 4242`

### Для продакшена:
1. Создайте Live price в Stripe Dashboard
2. Убедитесь что используется Live API key
3. Обновите `STRIPE_PRICE_ID` на Live price ID
4. Проверьте webhooks

---

## 📝 Текущий статус:

✅ Product создан: `TrendXL Pro`
✅ Test Price создан: `$49/month`
✅ Payment Link создан (test mode)
⚠️ Нужно согласовать: Test vs Live mode

Выберите вариант 1 для тестирования или вариант 2 для реальных платежей!

