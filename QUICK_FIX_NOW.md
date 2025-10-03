# 🚨 Срочное исправление - Stripe Price ID

## Проблема

```
No such price: 'price_1SDjkdGfnGEnyXLEIIX4TIUc'
```

## ⚡ Быстрое решение (5 минут)

### Шаг 1: Создайте правильный Price ID

**Запустите локально:**

```bash
cd backend
python setup_stripe_product.py
```

**Вы увидите:**

```
✅ Price created successfully!
   Price ID: price_xxxxxxxxxxxxx
```

**Скопируйте этот Price ID!** ⬆️

---

### Шаг 2: Обновите Vercel

1. Откройте: https://vercel.com/dashboard
2. Выберите проект `trendxl-2-0`
3. **Settings** → **Environment Variables**
4. Найдите `STRIPE_PRICE_ID`
5. Нажмите **Edit** (карандаш справа)
6. Вставьте **новый Price ID** из Шага 1
7. Нажмите **Save**
8. Вернитесь в **Deployments**
9. Нажмите **Redeploy** на последнем деплое

---

### Шаг 3: Подождите 2-3 минуты

Vercel задеплоит новую версию с правильным Price ID.

---

### Шаг 4: Проверьте

Откройте ваш сайт и нажмите "Subscribe" - должно работать! ✅

---

## 📝 Что было сделано ранее

✅ **Проблема #1 (404)** - исправлена  
✅ **Проблема #2 (AttributeError)** - исправлена  
⚠️ **Проблема #3 (Invalid Price)** - требует вашего действия (см. выше)

---

## 🆘 Если не работает

### Проверьте режим Stripe

В Stripe Dashboard (правый верхний угол) должно быть:

- **Test mode** - для тестирования
- **Live mode** - для реальных платежей

Убедитесь, что:

- `STRIPE_API_KEY` в Vercel соответствует режиму
- `STRIPE_PRICE_ID` создан в том же режиме

### Альтернативный способ

Если скрипт не работает, используйте существующую цену:

```bash
cd backend
python list_stripe_products.py
```

Найдите Price ID для $29/month и используйте его в Vercel.

---

## 📚 Полная документация

- `FIX_STRIPE_PRICE_ID.md` - детальные инструкции
- `VERCEL_DEPLOYMENT_FIXES_COMPLETE.md` - полная история исправлений
- `STRIPE_SETUP_GUIDE.md` - настройка Stripe

---

**Всё готово! Действуйте! 🚀**
