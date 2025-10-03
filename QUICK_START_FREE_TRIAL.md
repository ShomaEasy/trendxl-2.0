# 🚀 Быстрый старт: Бесплатные попытки

## Что это?

Теперь новые пользователи получают **1 бесплатный анализ в день** для тестирования продукта перед оформлением подписки! 🎁

## Быстрая установка (5 минут)

### 1️⃣ Применить миграцию в Supabase

1. Открыть [Supabase Dashboard](https://supabase.com/dashboard)
2. Выбрать ваш проект
3. Перейти в **SQL Editor** (левое меню)
4. Создать новый запрос
5. Скопировать весь файл `backend/supabase_free_trial_migration.sql`
6. Вставить и нажать **Run** ▶️

### 2️⃣ Деплой на Railway/Vercel

Изменения уже в коде - просто сделайте git push:

```bash
git add .
git commit -m "feat: Add 1 free daily analysis for new users"
git push origin main
```

Railway/Vercel автоматически задеплоят обновления! 🚀

### 3️⃣ Проверить работу

#### Тест 1: Первая попытка (должна работать ✅)

1. Зарегистрировать нового пользователя
2. Сделать анализ профиля
3. ✅ Должно работать!

#### Тест 2: Вторая попытка в тот же день (должна быть ошибка ❌)

1. Попробовать сделать второй анализ
2. ❌ Должна быть ошибка: "You've used your free daily analysis"

#### Тест 3: Следующий день (должна работать ✅)

1. Подождать до следующего дня
2. Попробовать сделать анализ
3. ✅ Должно работать!

## Что изменилось?

### Backend изменения:

✅ **Новая таблица в БД:** `daily_free_analyses`

- Отслеживает использование бесплатных попыток
- Автоматически сбрасывается каждый день

✅ **Обновлен endpoint `/api/v1/analyze`:**

- Теперь проверяет бесплатные попытки
- Записывает использование после анализа

✅ **Новый endpoint `/api/v1/free-trial/info`:**

- Получение статуса бесплатных попыток
- Для отображения в UI

### Логика работы:

```
Пользователь делает анализ
  ↓
Есть подписка? → Да → ✅ Разрешить
  ↓ Нет
Есть бесплатная попытка сегодня? → Да → ✅ Разрешить + записать
  ↓ Нет
❌ Показать сообщение о подписке
```

## Проверка установки

### SQL проверка:

```sql
-- Проверить таблицу
SELECT * FROM public.daily_free_analyses LIMIT 1;

-- Проверить функции
SELECT proname FROM pg_proc WHERE proname LIKE '%free_trial%';
-- Должно вернуть: can_use_free_trial, record_free_trial_usage, get_free_trial_info
```

### API проверка:

```bash
# Получить информацию о бесплатных попытках
curl -X GET "https://your-backend.railway.app/api/v1/free-trial/info" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Мониторинг

### Посмотреть статистику:

```sql
-- Сколько пользователей использовали бесплатные попытки сегодня?
SELECT COUNT(DISTINCT user_id) as free_users_today
FROM daily_free_analyses
WHERE analysis_date = CURRENT_DATE;

-- Топ активных пользователей
SELECT
    user_id,
    COUNT(*) as total_analyses
FROM daily_free_analyses
GROUP BY user_id
ORDER BY total_analyses DESC
LIMIT 10;
```

## Troubleshooting

### ❌ Ошибка: "function does not exist"

**Решение:** Миграция не применена. Повторите шаг 1.

### ❌ Backend не запускается

**Проверка:**

```bash
# Локально
cd backend
python main.py

# Railway
railway logs
```

### ❌ Пользователь не может использовать бесплатную попытку

**Сброс для тестирования:**

```sql
DELETE FROM daily_free_analyses
WHERE user_id = 'your-user-uuid'
AND analysis_date = CURRENT_DATE;
```

## Следующие шаги

1. ✅ Протестировать на production
2. 📊 Настроить мониторинг конверсии
3. 💬 Обновить UI для отображения лимитов (опционально)

## Дополнительная информация

Полная документация: `FREE_TRIAL_SETUP.md`

---

**Готово!** 🎉 Теперь новые пользователи могут тестировать ваш продукт бесплатно!
