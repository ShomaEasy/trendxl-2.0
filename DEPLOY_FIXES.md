# 🚀 Deploy Fixes to Vercel

## Что было исправлено

### 1. ❌ Redis Connection Error → ✅ Graceful Redis Disable

- Backend больше не падает без Redis
- Работает в Vercel без дополнительных настроек

### 2. ❌ JWT Token Expired 401 → ✅ Auto Token Refresh

- Автоматическое обновление токенов через Supabase
- Перехват 401 ошибок и retry с новым токеном
- Пользователи не будут разлогиниваться каждый час

---

## Как задеплоить исправления

### Вариант 1: Автоматический деплой (если настроен Git Integration)

```bash
# Просто запушьте изменения
git add .
git commit -m "fix: Redis graceful disable + JWT auto-refresh"
git push origin main
```

Vercel автоматически задеплоит изменения через 2-3 минуты.

---

### Вариант 2: Ручной деплой через Vercel CLI

```bash
# Установите Vercel CLI (если не установлен)
npm i -g vercel

# Деплой
vercel --prod
```

---

## Проверка после деплоя

### 1. Проверьте логи Vercel

Перейдите в [Vercel Dashboard](https://vercel.com/dashboard) → Ваш проект → Logs

**Хорошие логи (после исправлений):**

```
✅ ℹ️ Redis caching disabled (REDIS_URL not configured)
✅ TrendXL 2.0 Backend starting up...
✅ Supabase client initialized
```

**НЕ должно быть:**

```
❌ Error 111 connecting to localhost:6379. Connection refused.
```

### 2. Тест JWT Token Refresh

1. Откройте ваше приложение на Vercel
2. Залогиньтесь
3. Откройте DevTools → Console
4. При следующих API запросах вы должны видеть:
   ```
   🔄 Token refreshed, updating local storage
   ✅ Token verified, user: user@example.com
   ```

### 3. Тест API запросов

Попробуйте сделать анализ профиля TikTok:

- Не должно быть 401 ошибок
- При истечении токена он автоматически обновится

---

## Переменные окружения (проверьте в Vercel)

Убедитесь, что в Vercel Settings → Environment Variables установлены:

### Обязательные:

```
SUPABASE_URL=https://jynidxwtbjrxmsbfpqra.supabase.co
SUPABASE_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...
JWT_SECRET=your-secret
STRIPE_API_KEY=sk-...
STRIPE_PRICE_ID=price_...
ENSEMBLE_API_TOKEN=...
OPENAI_API_KEY=sk-...
PERPLEXITY_API_KEY=pplx-...
```

### Опциональные (можно не добавлять):

```
REDIS_URL=  # Оставьте пустым или не добавляйте вообще
```

---

## Если что-то пошло не так

### Логи показывают Redis errors:

- Проверьте, что `REDIS_URL` НЕ установлена в Vercel Environment Variables
- Или установите её в пустую строку `REDIS_URL=""`
- Редеплойте

### 401 ошибки продолжаются:

1. Проверьте JWT expiration time в Supabase Dashboard:
   - Auth → Settings → JWT Expiry (должно быть 3600 секунд = 1 час)
2. Проверьте, что Supabase JWT Secret совпадает с `JWT_SECRET` в Vercel:

   ```bash
   # В Supabase Dashboard → Settings → API → JWT Settings → JWT Secret
   ```

3. Очистите кеш браузера и попробуйте заново залогиниться

### Backend не отвечает:

- Проверьте логи Vercel
- Убедитесь, что все Environment Variables установлены
- Проверьте `vercel.json` - timeout должен быть 300s

---

## Дополнительно: Добавление Redis (optional, для ускорения)

Если хотите ускорить работу приложения, можете добавить Redis:

### Upstash Redis (рекомендуется):

1. Зарегистрируйтесь на https://upstash.com
2. Создайте Redis database (Free tier 10k commands/day)
3. Скопируйте Redis URL
4. Добавьте в Vercel Environment Variables:
   ```
   REDIS_URL=redis://default:your-password@your-region.upstash.io:6379
   ```
5. Редеплойте

После добавления Redis в логах должно появиться:

```
✅ Redis cache service initialized successfully
```

---

## Резюме

✅ **Redis** - теперь опциональный, не вызывает ошибок
✅ **JWT Tokens** - автообновление, пользователи не разлогиниваются
✅ **Production Ready** - работает в Vercel serverless без дополнительных настроек

🚀 **Просто запушьте изменения в Git, и Vercel автоматически задеплоит!**
