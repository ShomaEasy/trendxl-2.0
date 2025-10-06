# 🔧 Исправление проблемы с Free Trial (can_use_free_trial возвращает NULL)

## ❌ Проблема

1. **Эндпоинт `/api/v1/analyze-creative-center` не проверял free trial** 
   - Не требовал аутентификации
   - Не проверял подписку/free trial
   - Не записывал использование попытки
   - **Результат:** Пользователи могли использовать неограниченно

2. **Функция `can_use_free_trial` возвращает NULL**
   - Если пользователь не найден в таблице `profiles`
   - Если `stripe_subscription_status` = NULL
   - **Результат:** Фронтенд получает `can_use_free_trial: null` вместо `true/false`

## ✅ Решение

### Шаг 1: Обновить бекенд (уже сделано)

Файл `backend/main.py` обновлен:
- ✅ Добавлена аутентификация в `/api/v1/analyze-creative-center`
- ✅ Добавлена проверка `check_user_can_analyze`
- ✅ Добавлена запись `record_free_trial_usage`

### Шаг 2: Исправить SQL функции в Supabase

Выполните SQL из файла `backend/fix_free_trial_null.sql` в Supabase Dashboard:

1. Откройте Supabase Dashboard
2. Перейдите в **SQL Editor**
3. Скопируйте и выполните весь SQL из `backend/fix_free_trial_null.sql`

**Что исправляет SQL:**

1. **Обновленная `can_use_free_trial`:**
   - Проверяет существование пользователя
   - Правильно обрабатывает NULL с COALESCE
   - Всегда возвращает boolean (никогда NULL)

2. **Обновленная `get_free_trial_info`:**
   - Оборачивает результат в COALESCE
   - Возвращает `true` по умолчанию если функция вернула NULL

3. **Синхронизация profiles с auth.users:**
   - Создает записи в `profiles` для всех пользователей из `auth.users`
   - Предотвращает проблему отсутствия записи

### Шаг 3: Проверка исправлений

После выполнения SQL:

```sql
-- Тест 1: Проверить функцию для существующего пользователя
SELECT can_use_free_trial('USER_UUID_HERE');
-- Должно вернуть: true или false (не NULL)

-- Тест 2: Проверить get_free_trial_info
SELECT * FROM get_free_trial_info('USER_UUID_HERE');
-- can_use_today должно быть true или false (не NULL)

-- Тест 3: Проверить синхронизацию
SELECT 
    COUNT(*) as users_in_auth,
    (SELECT COUNT(*) FROM public.profiles) as users_in_profiles
FROM auth.users;
-- Числа должны совпадать
```

## 🚀 Деплой исправлений

### 1. Закоммитить и запушить изменения:

```bash
git add .
git commit -m "fix: Исправлена проблема с free trial в analyze-creative-center

- Добавлена аутентификация и проверка free trial в /api/v1/analyze-creative-center
- Исправлены SQL функции для правильной обработки NULL
- Добавлена синхронизация profiles с auth.users
- Создан SQL скрипт для применения исправлений"

git push origin main
```

### 2. Применить SQL в продакшен Supabase:

1. Откройте Production Supabase Dashboard
2. SQL Editor → New Query
3. Вставьте содержимое `backend/fix_free_trial_null.sql`
4. Нажмите **Run**
5. Проверьте что запрос выполнился без ошибок

### 3. Проверка на продакшене:

После деплоя проверьте:

```bash
# В браузере откройте консоль
# Должны увидеть в логах:
✅ SubscriptionBanner: Free trial info loaded {
  can_use_free_trial: true,  // или false, но НЕ null
  today_count: 0,
  ...
}
```

## 📊 Проверочный список

- [ ] SQL выполнен в Supabase
- [ ] Функция `can_use_free_trial` возвращает boolean
- [ ] Функция `get_free_trial_info` не возвращает NULL в `can_use_today`
- [ ] Таблицы `auth.users` и `profiles` синхронизированы
- [ ] Изменения бекенда задеплоены
- [ ] Эндпоинт `/api/v1/analyze-creative-center` требует аутентификации
- [ ] Free trial записывается для обоих эндпоинтов
- [ ] Повторный анализ блокируется после использования попытки

## 🧪 Тестирование после исправления

### Тест 1: Новый пользователь
1. Зарегистрироваться
2. Увидеть: `can_use_free_trial: true, today_count: 0`
3. Выполнить анализ через любой метод
4. Увидеть: `can_use_free_trial: false, today_count: 1`
5. Попытаться анализировать снова → Показывается модальное окно подписки

### Тест 2: Пользователь с подпиской
1. Войти с активной подпиской
2. Увидеть: `has_subscription: true`
3. Выполнить несколько анализов → все успешны
4. Free trial не тратится

### Тест 3: Creative Center эндпоинт
1. Использовать Creative Center анализ
2. Проверить что free trial списывается
3. Проверить что повторный анализ блокируется

## 🔍 Отладка

### Если проблема продолжается:

1. **Проверьте логи бекенда:**
```bash
# На Vercel
vercel logs
```

2. **Проверьте Supabase функции:**
```sql
-- Проверить что функции обновлены
SELECT 
    routine_name,
    routine_definition 
FROM information_schema.routines 
WHERE routine_name IN ('can_use_free_trial', 'get_free_trial_info');
```

3. **Проверьте записи в daily_free_analyses:**
```sql
SELECT * FROM daily_free_analyses 
WHERE user_id = 'USER_UUID'
ORDER BY created_at DESC
LIMIT 5;
```

## 📝 Краткое резюме изменений

**Файлы изменены:**
- ✅ `backend/main.py` - добавлены проверки в `/api/v1/analyze-creative-center`
- ✅ `backend/fix_free_trial_null.sql` - SQL для исправления функций

**Проблемы исправлены:**
1. ✅ Эндпоинт Creative Center теперь проверяет free trial
2. ✅ Функция `can_use_free_trial` не возвращает NULL
3. ✅ Таблица `profiles` синхронизирована с `auth.users`
4. ✅ Free trial записывается для всех эндпоинтов

---

**Время выполнения:** ~5-10 минут  
**Риск:** Низкий (только добавление проверок, не ломает существующую функциональность)  
**Требуется даунтайм:** Нет

