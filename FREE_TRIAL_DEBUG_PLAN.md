# Free Trial Debug Plan

## ✅ Что уже исправлено:

1. **SERVICE_ROLE_KEY** теперь используется (вместо ANON_KEY)
2. **record_free_trial_usage()** теперь выбрасывает исключение при ошибке
3. **analyze endpoint** проверяет возвращаемое значение и обрабатывает исключения

## ✅ Диагностика показала:

- ✅ Supabase connection работает
- ✅ SERVICE_KEY загружен правильно (219 символов)
- ✅ RPC функция `can_use_free_trial` существует
- ✅ Таблица `daily_free_analyses` существует
- ⚠️ **Сегодня 0 записей** - функция НЕ вызывается при анализе!

## 🔍 Возможные причины:

### 1. Backend не запущен или не обрабатывает запросы

- Проверка: `http://localhost:8000/health`
- Должен вернуть статус "healthy"

### 2. Frontend не подключается к backend

- Проверка: Console в браузере (F12)
- Ищите ошибки "Failed to fetch" или "Network Error"

### 3. Пользователь не аутентифицирован

- Ошибка: "User not authenticated, cannot save scan history"
- Проблема: Frontend Supabase session не активна
- Решение: Перелогиниться

### 4. Backend использует старый код (до фикса)

- Возможно Vercel еще не задеплоил изменения
- Или локальный backend не перезагрузился

## 📝 Шаги для отладки:

### Шаг 1: Проверить backend

```bash
# В браузере откройте:
http://localhost:8000/health

# Должен вернуть:
{"status": "healthy", "timestamp": "..."}
```

### Шаг 2: Проверить frontend подключение

1. Откройте DevTools (F12) → Console
2. Попробуйте сделать analysis
3. Ищите в логах:
   - `🚀 BACKEND: NEW ANALYSIS REQUEST RECEIVED!`
   - `🎁 User {username} using FREE TRIAL`
   - `✅ Recorded free trial usage`

### Шаг 3: Проверить аутентификацию

**В DevTools Console выполните:**

```javascript
// Проверить Supabase session
const {
  data: { session },
} = await supabase.auth.getSession();
console.log("Session:", session);

// Проверить user
const {
  data: { user },
} = await supabase.auth.getUser();
console.log("User:", user);
```

Если `session` или `user` = null, нужно перелогиниться.

### Шаг 4: Проверить, работает ли вызов RPC

**Запустите тест:**

```bash
cd "C:\Users\ok\Desktop\timo\trendxl 2.0"
python test_free_trial_fix.py <YOUR-USER-UUID>
```

Получить UUID:

1. Откройте https://supabase.com/dashboard/project/jynidxwtbjrxmsbfpqra/auth/users
2. Найдите пользователя 'timo'
3. Скопируйте UUID (формат: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)

### Шаг 5: Если все еще не работает - проверить Vercel

Если тестируете на production (Vercel):

1. Откройте Vercel Dashboard
2. Проверьте, что последний деплой успешен
3. Проверьте Environment Variables:
   - `SUPABASE_SERVICE_ROLE_KEY` должен быть установлен
   - Значение из Supabase Dashboard → Settings → API → service_role key

## 🎯 Ожидаемый результат:

После успешного анализа:

1. **В логах backend** (консоль где запущен `python run_server.py`):

```
🎁 User timo using FREE TRIAL (1/day)
✅ Recorded free trial usage for user {uuid}
🎁 Free trial used by timo for @amazing.world
```

2. **В Supabase Dashboard** → Table Editor → daily_free_analyses:

- Должна появиться запись с:
  - `user_id`: ваш UUID
  - `analysis_date`: сегодняшняя дата
  - `analysis_count`: 1
  - `profile_analyzed`: имя профиля

3. **В UI**:

- Счетчик должен показать: `0/1 Used Today`
- При второй попытке: ошибка 403 "Analysis limit reached"

## 🐛 Если все равно не работает:

Запустите полную диагностику:

```bash
python diagnose_free_trial.py
```

И отправьте:

1. Вывод диагностики
2. Логи backend (если есть)
3. Скриншот Console в браузере (F12)
4. Скриншот Network tab при попытке analysis
