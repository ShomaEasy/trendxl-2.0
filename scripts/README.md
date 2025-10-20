# TrendXL Deployment Automation Scripts

Автоматические скрипты для проверки и deployment приложения на Vercel.

## 📋 Скрипты

### 1. `verify-deployment.py`

**Автоматическая проверка deployment и конфигурации**

Проверяет:
- ✅ Environment variables в Vercel
- ✅ Stripe API keys (test vs live mode)
- ✅ Последний deployment status
- ✅ Backend API endpoints

**Использование:**

```bash
# Запуск проверки
python3 scripts/verify-deployment.py

# Или с кастомным токеном
VERCEL_TOKEN=your_token python3 scripts/verify-deployment.py
```

**Пример вывода:**

```
🚀 TrendXL Deployment Verification Tool

============================================================
          Проверка Environment Variables в Vercel
============================================================

Найдено 7/7 обязательных переменных:

✅ SUPABASE_URL
✅ SUPABASE_ANON_KEY
✅ STRIPE_API_KEY
...

============================================================
                  Проверка Stripe API Keys
============================================================

✅ Используется LIVE mode API key
⚠️  Требуется настроить Customer Portal в LIVE mode:
   👉 https://dashboard.stripe.com/settings/billing/portal
```

---

## 🔧 Настройка Vercel Environment Variables

### Требуемые переменные:

```bash
# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# API Keys
ENSEMBLE_API_TOKEN=xxx
OPENAI_API_KEY=sk-proj-xxx
PERPLEXITY_API_KEY=pplx-xxx

# Stripe
STRIPE_API_KEY=sk_live_xxx  # или sk_test_xxx
STRIPE_PRICE_ID=price_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

### Автоматическое добавление:

Скрипт `/tmp/add_env_to_vercel.py` автоматически добавляет все переменные из `.env` в Vercel:

```bash
python3 /tmp/add_env_to_vercel.py
```

**ВАЖНО:** После добавления env vars нужно сделать redeploy!

---

## 🚀 Deployment Workflow

### 1. Проверка перед deploy

```bash
# Проверяем что все готово
python3 scripts/verify-deployment.py
```

### 2. Commit и Push

```bash
git add .
git commit -m "feat: your changes"
git push origin dev
```

### 3. Vercel Auto-Deploy

Vercel автоматически деплоит при push в `dev` или `main` ветку через GitHub integration.

**Preview URL** (для dev ветки):
```
https://trendxl-2-0-xxx-dev-shomas-projects.vercel.app
```

**Production URL** (для main ветки):
```
https://trendxl-2-0.vercel.app
```

### 4. Проверка deployment

```bash
# Список deployments
vercel ls --token TVO0VjVBuWcaDgLB8Biojfkn

# Проверка логов последнего deployment
vercel logs --token TVO0VjVBuWcaDgLB8Biojfkn
```

---

## 🔑 Stripe Customer Portal Configuration

### ВАЖНО: Test vs Live Mode

Stripe имеет **отдельные конфигурации** для test и live режимов!

#### Если используете **TEST mode** (`sk_test_xxx`):

1. Перейдите: https://dashboard.stripe.com/test/settings/billing/portal
2. Нажмите "Activate Customer Portal"
3. Настройте функции (Cancel subscription, Update payment method, etc.)
4. Сохраните

#### Если используете **LIVE mode** (`sk_live_xxx`):

1. Перейдите: https://dashboard.stripe.com/settings/billing/portal
2. Нажмите "Activate Customer Portal"
3. Настройте функции
4. Сохраните

**Проверка режима:**

```bash
# Смотрим в .env
grep STRIPE_API_KEY .env

# sk_test_xxx = Test Mode
# sk_live_xxx = Live Mode
```

---

## 🧪 Тестирование после deployment

### 1. Проверка env variables загружены

```bash
curl -I https://your-app.vercel.app/api/health
```

### 2. Проверка subscription endpoint

```bash
# Без токена - должно вернуть 401
curl https://your-app.vercel.app/api/v1/subscription/manage

# Ожидаемый ответ:
# {"detail":"Not authenticated"}
```

### 3. Проверка Stripe Customer Portal

1. Залогиньтесь на сайте
2. Перейдите в `/profile`
3. Кнопка "Manage Subscription" должна быть видна (темно-зеленая)
4. При клике должен открыться Stripe Customer Portal

**Если 404 ошибка:**
- Customer Portal не настроен в нужном режиме (test/live)
- Environment variables не применились (нужен redeploy)

---

## 📝 Troubleshooting

### Проблема: Environment variables не работают

**Решение:**
1. Проверьте что vars добавлены:
   ```bash
   vercel env ls --token TVO0VjVBuWcaDgLB8Biojfkn
   ```
2. Сделайте redeploy для применения:
   ```bash
   git commit --allow-empty -m "chore: trigger redeploy"
   git push origin dev
   ```

### Проблема: 404 на `/api/v1/subscription/manage`

**Решение:**
1. Проверьте что endpoint существует в `backend/main.py`:
   ```bash
   grep "subscription/manage" backend/main.py
   ```
2. Проверьте что последний commit задеплоен:
   ```bash
   vercel ls --token TVO0VjVBuWcaDgLB8Biojfkn
   ```

### Проблема: Customer Portal не открывается

**Решение:**
1. Проверьте режим API key (test/live):
   ```bash
   python3 scripts/verify-deployment.py
   ```
2. Настройте Portal в соответствующем режиме
3. Дождитесь завершения deployment (5-10 мин)

---

## 🤖 Автоматизация

Добавьте в CLAUDE.md инструкции:

```markdown
## Deployment Checklist

Перед каждым deployment автоматически проверяйте:

1. **Environment Variables:**
   ```bash
   python3 scripts/verify-deployment.py
   ```

2. **Stripe Configuration:**
   - Проверить test/live mode
   - Настроить Customer Portal в нужном режиме

3. **Push changes:**
   ```bash
   git push origin dev
   ```

4. **Verify deployment:**
   - Дождаться завершения build в Vercel
   - Проверить endpoint /api/v1/subscription/manage
   - Протестировать Customer Portal button
```

---

## 📚 Документация

- Vercel Deployments: https://vercel.com/docs/deployments
- Stripe Customer Portal: https://docs.stripe.com/customer-management
- GitHub Integration: https://vercel.com/docs/git/vercel-for-github
