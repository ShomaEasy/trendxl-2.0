# 🎯 ВЫПОЛНИТЕ В СТРОГОМ ПОРЯДКЕ!

## ⚠️ ВАЖНО: Запускайте по одному файлу за раз!

---

## 📍 Откройте Supabase SQL Editor:

👉 https://supabase.com/dashboard/project/jynidxwtbjrxmsbfpqra/editor

---

## 🥇 ШАГ 1: Создайте таблицы

### Файл: `MINIMAL_TABLES_ONLY.sql`

Скопируйте ВЕСЬ код из файла и нажмите **RUN**

Этот шаг создает:

- ✅ Таблицу `scan_history`
- ✅ Таблицу `daily_free_analyses`
- ✅ Индексы
- ✅ Включает RLS
- ✅ Дает права доступа

**ЖДИТЕ УСПЕШНОГО ВЫПОЛНЕНИЯ!**

---

## 🥈 ШАГ 2: Добавьте политики безопасности

### Файл: `ADD_POLICIES.sql`

Скопируйте ВЕСЬ код из файла и нажмите **RUN**

Этот шаг создает:

- ✅ RLS политики для `scan_history` (3 политики)
- ✅ RLS политики для `daily_free_analyses` (3 политики)

**ЖДИТЕ УСПЕШНОГО ВЫПОЛНЕНИЯ!**

---

## 🥉 ШАГ 3: Добавьте функции

### Файл: `ADD_FUNCTIONS.sql`

Скопируйте ВЕСЬ код из файла и нажмите **RUN**

Этот шаг создает:

- ✅ Функцию `can_use_free_trial()`
- ✅ Функцию `record_free_trial_usage()`
- ✅ Функцию `get_free_trial_info()` ⭐ **Это исправит ошибку 404!**

**ЖДИТЕ УСПЕШНОГО ВЫПОЛНЕНИЯ!**

---

## ✅ ПРОВЕРКА

После выполнения всех 3 шагов, выполните:

```sql
-- Проверка таблиц
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('scan_history', 'daily_free_analyses');

-- Проверка функций
SELECT proname
FROM pg_proc
WHERE proname IN ('can_use_free_trial', 'get_free_trial_info', 'record_free_trial_usage');

-- Проверка политик
SELECT tablename, policyname
FROM pg_policies
WHERE tablename IN ('scan_history', 'daily_free_analyses');
```

Вы должны увидеть:

- 2 таблицы
- 3 функции
- 6 политик (3 для каждой таблицы)

---

## 🎉 ГОТОВО!

После этого:

- ✅ Ошибка 404 исчезнет
- ✅ Free trial counter заработает
- ✅ My Trends покажет историю
- ✅ Все API эндпоинты заработают

**Перезапустите backend и frontend!**
