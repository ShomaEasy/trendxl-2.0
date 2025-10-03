# ⚠️ СРОЧНО: ЗАПУСТИТЕ ПЕРЕД ИСПОЛЬЗОВАНИЕМ!

## 🔴 Проблема

Ошибка `404` на `/api/v1/free-trial/info` означает, что таблицы в Supabase НЕ СОЗДАНЫ!

---

## ✅ РЕШЕНИЕ (2 минуты)

### Вариант 1: Через Supabase Dashboard (РЕКОМЕНДУЕТСЯ)

#### Шаг 1: Откройте SQL Editor
👉 https://supabase.com/dashboard/project/jynidxwtbjrxmsbfpqra/editor

#### Шаг 2: Скопируйте и запустите
Откройте файл **`WORKING_MIGRATION.sql`** (в корне проекта)

Скопируйте ВЕСЬ его содержимое и вставьте в SQL Editor

Нажмите **RUN** (или Ctrl+Enter)

#### Шаг 3: Ждите успех
Вы должны увидеть результат без ошибок!

---

### Вариант 2: По шагам (если вариант 1 не работает)

Выполните по очереди:

1. **MINIMAL_TABLES_ONLY.sql** - создаст таблицы
2. **ADD_POLICIES.sql** - добавит политики безопасности
3. **ADD_FUNCTIONS.sql** - создаст функции

---

## 📋 Проверка

После выполнения, запустите в SQL Editor:

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('scan_history', 'daily_free_analyses');
```

Должны увидеть обе таблицы!

---

## 🎉 После успешного выполнения:

✅ Ошибка 404 исчезнет
✅ Счетчик free scans заработает  
✅ My Trends покажет историю
✅ Сохранение попыток будет работать

---

## ❓ Если есть проблемы

Откройте файл **`EXECUTE_IN_ORDER.md`** для подробных инструкций

