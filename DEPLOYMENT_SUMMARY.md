# 🚀 TrendXL Deployment Summary - 2025-10-20

## ✅ Выполнено автоматически

### 1. Environment Variables добавлены в Vercel ✅

**Добавлено 9 переменных** (Production + Preview):

- ✅ SUPABASE_URL
- ✅ SUPABASE_ANON_KEY
- ✅ SUPABASE_SERVICE_ROLE_KEY
- ✅ ENSEMBLE_API_TOKEN
- ✅ OPENAI_API_KEY
- ✅ PERPLEXITY_API_KEY
- ✅ STRIPE_API_KEY (sk_live_xxx)
- ✅ STRIPE_PRICE_ID
- ✅ STRIPE_WEBHOOK_SECRET

**Проверка:**
```bash
vercel env ls --token TVO0VjVBuWcaDgLB8Biojfkn
```

---

### 2. Deployment запущен ✅

**URL:** https://trendxl-20-mz94pix17-shomas-projects-2d51e250.vercel.app

**Статус:** ● Building (в процессе)

**Проверка статуса:**
```bash
vercel ls --token TVO0VjVBuWcaDgLB8Biojfkn
```

---

### 3. Автоматизация создана ✅

**Скрипты:**

1. **`scripts/verify-deployment.py`** - Автоматическая проверка перед deployment
   ```bash
   python3 scripts/verify-deployment.py
   ```

2. **`scripts/add_env_to_vercel.py`** - Добавление env vars в Vercel
   ```bash
   python3 scripts/add_env_to_vercel.py
   ```

3. **`scripts/README.md`** - Полная документация

---

### 4. Документация обновлена ✅

**CLAUDE.md** теперь содержит:
- Автоматический deployment workflow
- Проверка перед каждым push
- Stripe Customer Portal configuration
- Troubleshooting guide

---

## ⚠️ ТРЕБУЕТСЯ РУЧНАЯ НАСТРОЙКА

### ❗ Stripe Customer Portal Configuration

**КРИТИЧЕСКИ ВАЖНО для работы кнопки "Manage Subscription"!**

**Найденный режим:** LIVE mode (`sk_live_xxx`)

**Действия:**

1. Перейдите: https://dashboard.stripe.com/settings/billing/portal
2. Нажмите **"Activate Customer Portal"**
3. Настройте доступные функции:
   - ✅ Cancel subscription
   - ✅ Update payment method
   - ✅ View invoice history
4. Нажмите **"Save"**

**Проверка:**
После deployment зайдите в `/profile` → кнопка "Manage Subscription" должна открывать Stripe Portal.

---

## 🔍 Что проверить после deployment

### 1. Дождитесь завершения build (3-5 минут)

```bash
# Проверка статуса
vercel ls --token TVO0VjVBuWcaDgLB8Biojfkn

# Должно быть: ✔ Ready
```

### 2. Проверьте backend endpoint

```bash
# Должен вернуть 401 (не 404!)
curl https://trendxl-20-mz94pix17-shomas-projects-2d51e250.vercel.app/api/v1/subscription/manage

# Ожидаемый ответ:
# {"detail":"Not authenticated"}
```

### 3. Протестируйте в браузере

1. Откройте: https://trendxl-20-mz94pix17-shomas-projects-2d51e250.vercel.app/profile
2. Залогиньтесь: `aleynikov.artem@gmail.com` / `220218`
3. Проверьте:
   - ✅ Баннер подписки виден
   - ✅ Кнопка "Manage Subscription" видна (темно-зеленая)
   - ✅ При клике открывается Stripe Customer Portal (не 404!)

---

## 📊 Автоматическая проверка

**Запускайте перед каждым deployment:**

```bash
python3 scripts/verify-deployment.py
```

**Вывод:**
```
🚀 TrendXL Deployment Verification Tool

✅ SUPABASE_URL
✅ STRIPE_API_KEY
✅ Используется LIVE mode API key
⚠️  Требуется настроить Customer Portal в LIVE mode

Пройдено проверок: 3/4
```

---

## 🐛 Troubleshooting

### Проблема: Кнопка "Manage Subscription" не работает (404)

**Причина:** Customer Portal не настроен в Stripe

**Решение:**
1. Настройте Portal: https://dashboard.stripe.com/settings/billing/portal
2. Подождите 1-2 минуты обновления Stripe
3. Обновите страницу (Ctrl+F5)

### Проблема: Кнопка не видна

**Решение:** Уже исправлено! Кнопка теперь темно-зеленая (green.600) на светло-зеленом фоне.

### Проблема: 500 ошибка на /api/v1/subscription/info

**Причина:** Stripe API key не настроен или невалиден

**Решение:**
```bash
# Проверьте env vars
vercel env ls --token TVO0VjVBuWcaDgLB8Biojfkn

# Если STRIPE_API_KEY отсутствует - добавьте
python3 scripts/add_env_to_vercel.py
```

---

## 📝 Commits

```
e05267e - feat: Add automated Vercel deployment verification tools
d4edb7e - fix: Make Manage Subscription button visible with better contrast
9edd66b - docs: Update deployment instructions with GitHub auto-deploy info
d6e36fc - fix: Move subscription banner to profile page and add Portal error handling
354e29f - fix: Add graceful handling for Stripe API when not configured
```

---

## 🎯 Следующие шаги

1. ⏳ Дождитесь завершения build (~5 минут)
2. ⚙️ Настройте Stripe Customer Portal в LIVE mode
3. ✅ Протестируйте кнопку "Manage Subscription"
4. 🎉 Готово!

---

## 🤖 Автоматизация на будущее

**Перед каждым deployment:**

```bash
# 1. Проверка
python3 scripts/verify-deployment.py

# 2. Commit
git add .
git commit -m "your changes"

# 3. Push (автоматический deploy)
git push origin dev
```

**Vercel автоматически:**
- Заберёт изменения из GitHub
- Соберёт frontend (Vite)
- Задеплоит backend (FastAPI via Mangum)
- Применит environment variables

---

**Deployment URL:** https://trendxl-20-mz94pix17-shomas-projects-2d51e250.vercel.app

**Vercel Dashboard:** https://vercel.com/shomas-projects-2d51e250/trendxl-2-0

**Stripe Dashboard:** https://dashboard.stripe.com/settings/billing/portal
