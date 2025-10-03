# Исправление ошибки Stripe Price ID

## ❌ Проблема

```
No such price: 'price_1SDjkdGfnGEnyXLEIIX4TIUc'
```

Это означает, что переменная окружения `STRIPE_PRICE_ID` в Vercel указывает на **несуществующую цену** в вашем Stripe аккаунте.

---

## ✅ Решение 1: Автоматическое создание (Рекомендуется)

### Шаг 1: Запустите скрипт локально

```bash
cd backend
python setup_stripe_product.py
```

**Что делает скрипт:**

- ✅ Создает продукт "TrendXL Pro" в Stripe
- ✅ Создает цену $29/месяц
- ✅ Выводит новый Price ID
- ✅ Автоматически обновляет `.env` файл

**Вывод будет примерно таким:**

```
🚀 CREATING STRIPE PRODUCT & PRICE
================================================================================

1️⃣ Creating Product...
✅ Product created successfully!
   Product ID: prod_xxxxxxxxxxxxx
   Name: TrendXL Pro
   Description: Unlimited trend analysis and AI insights for TikTok creators

2️⃣ Creating Price ($29/month)...
✅ Price created successfully!
   Price ID: price_xxxxxxxxxxxxx
   Amount: $29.0 USD
   Interval: monthly

✅ SETUP COMPLETE!
```

### Шаг 2: Скопируйте новый Price ID

Из вывода скрипта скопируйте:

```
price_xxxxxxxxxxxxx
```

### Шаг 3: Обновите переменную окружения в Vercel

1. Откройте [Vercel Dashboard](https://vercel.com/dashboard)
2. Выберите ваш проект
3. Перейдите в **Settings → Environment Variables**
4. Найдите `STRIPE_PRICE_ID`
5. Нажмите **Edit**
6. Вставьте новый Price ID
7. Нажмите **Save**
8. **Redeploy** проект

---

## ✅ Решение 2: Использовать существующую цену

### Шаг 1: Посмотрите существующие цены

```bash
cd backend
python list_stripe_products.py
```

**Вывод покажет:**

- Все ваши продукты в Stripe
- Все цены для каждого продукта
- Какой Price ID сейчас настроен
- Активен ли он

### Шаг 2: Выберите цену из списка

Найдите подходящую цену (например, $29/month recurring) и скопируйте её `Price ID`:

```
🔄 Active Recurring Prices (2):
   • price_1QHmcUGfnGEnyXLE6ZPMvOXH  ← Скопируйте это
     Product: TrendXL Pro
     Price: $29.0 USD/month
```

### Шаг 3: Обновите Vercel

Та же процедура, что и в Решении 1, Шаг 3.

---

## ✅ Решение 3: Создать вручную в Stripe Dashboard

### Шаг 1: Откройте Stripe Dashboard

Перейдите на: https://dashboard.stripe.com/products

### Шаг 2: Создайте продукт

1. Нажмите **"+ Add product"**
2. Заполните форму:
   - **Name:** `TrendXL Pro`
   - **Description:** `Unlimited trend analysis and AI insights for TikTok creators`

### Шаг 3: Добавьте цену

1. В разделе **Pricing** нажмите **"Add price"**
2. Настройте:
   - **Price:** `29.00`
   - **Currency:** `USD`
   - **Billing period:** `Monthly`
   - **Type:** `Recurring`

### Шаг 4: Скопируйте Price ID

После создания:

1. Откройте созданный продукт
2. В секции **Pricing** найдите цену
3. Нажмите на неё
4. Скопируйте **Price ID** (начинается с `price_`)

### Шаг 5: Обновите Vercel

Та же процедура, что и в Решении 1, Шаг 3.

---

## 🔍 Проверка после исправления

### 1. Проверьте локально

```bash
cd backend
python -c "from config import settings; print(f'STRIPE_PRICE_ID: {settings.stripe_price_id}')"
```

### 2. Проверьте в Vercel (после redeploy)

Откройте: `https://your-app.vercel.app/api/v1/subscription/create-payment-link?user_email=test@example.com`

**Ожидается:**

```json
{
  "success": true,
  "payment_url": "https://checkout.stripe.com/...",
  "session_id": "cs_...",
  "expires_at": "..."
}
```

**Не должно быть:**

```json
{
  "detail": "No such price: 'price_...'"
}
```

---

## 📝 Пошаговая инструкция (полная)

### Локально:

```bash
# 1. Перейдите в папку backend
cd backend

# 2. Создайте продукт и цену автоматически
python setup_stripe_product.py

# 3. Скопируйте Price ID из вывода
# Пример: price_1QHmcUGfnGEnyXLE6ZPMvOXH

# 4. (Опционально) Проверьте что всё создалось
python list_stripe_products.py
```

### В Vercel Dashboard:

```
1. Откройте https://vercel.com/dashboard
2. Выберите проект "trendxl-2-0"
3. Settings → Environment Variables
4. Найдите STRIPE_PRICE_ID
5. Edit → Вставьте новый Price ID
6. Save
7. Deployments → Latest → Redeploy
```

### Проверка:

```bash
# После redeploy откройте в браузере:
https://your-app.vercel.app/

# Попробуйте кнопку "Subscribe"
# Должно перенаправить на Stripe Checkout
```

---

## ⚠️ Важные моменты

### Test vs Live Mode

**Stripe работает в двух режимах:**

- **Test Mode** - для тестирования (ключи начинаются с `sk_test_`)

  - Можно использовать тестовую карту: `4242 4242 4242 4242`
  - Реальные деньги НЕ списываются

- **Live Mode** - реальные платежи (ключи начинаются с `sk_live_`)
  - Списываются реальные деньги!

**Убедитесь, что используете правильный режим!**

### Переключение между режимами

В Stripe Dashboard есть переключатель **Test mode / Live mode** в правом верхнем углу.

Для разработки используйте **Test mode**.

### Price ID уникальны для режима

Price ID созданный в Test mode **НЕ будет работать** в Live mode и наоборот.

Если переключаетесь между режимами - создавайте новый продукт и цену!

---

## 🎯 Итоговый чеклист

- [ ] Запущен `setup_stripe_product.py` или создан продукт вручную
- [ ] Скопирован новый `STRIPE_PRICE_ID`
- [ ] Обновлена переменная в Vercel Environment Variables
- [ ] Сделан Redeploy проекта в Vercel
- [ ] Проверена работа кнопки Subscribe на сайте
- [ ] Payment link создается без ошибок
- [ ] Перенаправление на Stripe Checkout работает

---

**После выполнения всех шагов ошибка должна исчезнуть!** ✅
