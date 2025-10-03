# Админ-аккаунт - Руководство по настройке

## Описание

Система админ-аккаунтов позволяет определенным пользователям обходить все ограничения подписки и использовать все функции сервиса без лимитов.

## Возможности админ-аккаунта

✅ **Полный доступ ко всем API endpoints без подписки**
✅ **Обход всех проверок активной подписки**
✅ **Неограниченное использование trend analysis**
✅ **Неограниченное использование Creative Center**
✅ **Доступ ко всем функциям без каких-либо ограничений**

## Установка администраторов

### 1. Применить миграцию базы данных

Сначала нужно применить миграцию для добавления поля `is_admin` в таблицу `profiles`:

```bash
# Войдите в Supabase Dashboard
# https://supabase.com/dashboard/project/jynidxwtbjrxmsbfpqra/editor

# Выполните SQL из файла: supabase_admin_migration.sql
```

Или выполните этот SQL напрямую в Supabase SQL Editor:

```sql
-- Add is_admin column to profiles table
ALTER TABLE profiles
ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE;

-- Create index for quick admin lookups
CREATE INDEX IF NOT EXISTS idx_profiles_is_admin ON profiles(is_admin) WHERE is_admin = TRUE;

-- Add comment explaining the field
COMMENT ON COLUMN profiles.is_admin IS 'Admin users have full access to all services without subscription limits';
```

### 2. Установить админ-статус для пользователей

#### Способ 1: Через Python скрипт (Рекомендуется)

```bash
cd backend

# Установить администратора
python set_admin.py your-email@example.com

# Удалить админ-статус
python set_admin.py your-email@example.com --remove
```

#### Способ 2: Через Supabase SQL Editor

```sql
-- Установить админ-статус по email
UPDATE profiles
SET is_admin = TRUE
WHERE email = 'your-email@example.com';

-- Проверить администраторов
SELECT id, email, username, is_admin
FROM profiles
WHERE is_admin = TRUE;
```

#### Способ 3: Автоматически при регистрации (для разработчиков)

Добавьте в `.env`:

```env
# Список email-адресов администраторов (через запятую)
ADMIN_EMAILS=admin@example.com,partner@example.com
```

Затем обновите код регистрации, чтобы автоматически назначать админ-роль при регистрации с этими email.

## Настройка ваших админ-аккаунтов

### Для вас и вашего партнера:

1. **Зарегистрируйте аккаунты** (если еще не зарегистрированы):

   - Зайдите на сайт
   - Создайте аккаунты с вашими email-адресами

2. **Примените миграцию** в Supabase (см. раздел выше)

3. **Установите админ-статус** для обоих аккаунтов:

```bash
cd backend
python set_admin.py your-email@example.com
python set_admin.py partner-email@example.com
```

4. **Проверьте статус**:

```bash
# Войдите на сайт с вашим аккаунтом
# При логине вы увидите в консоли:
# 🔑 Admin user <username> bypassing subscription check
```

## Проверка работы

После установки админ-статуса:

1. Залогиньтесь с админ-аккаунтом
2. Попробуйте использовать trend analysis без подписки
3. В логах бэкенда вы должны увидеть:
   ```
   🔑 Admin user <username> bypassing subscription check
   ```

## Безопасность

⚠️ **ВАЖНО:**

- Никогда не делитесь админ-доступом с другими людьми
- Не коммитьте список админ-email в публичные репозитории
- Регулярно проверяйте список администраторов:

```sql
SELECT id, email, username, is_admin, created_at
FROM profiles
WHERE is_admin = TRUE;
```

## Технические детали

### Архитектура

- **База данных**: Поле `is_admin` в таблице `profiles`
- **Аутентификация**: Проверка в `auth_service_supabase.py`
- **Авторизация**: Обход проверки подписки в `main.py`

### API Response

При логине/регистрации админ-аккаунта:

```json
{
  "access_token": "...",
  "token_type": "bearer",
  "user": {
    "id": "...",
    "email": "admin@example.com",
    "username": "admin",
    "is_admin": true
  }
}
```

### Функции для работы с админ-статусом

```python
from auth_service_supabase import (
    get_user_admin_status,      # Проверить статус
    set_user_admin_status,       # Установить по user_id
    set_user_admin_by_email      # Установить по email
)

# Проверить статус
is_admin = await get_user_admin_status(user_id)

# Установить админ-статус
success = await set_user_admin_by_email("admin@example.com", True)

# Удалить админ-статус
success = await set_user_admin_by_email("admin@example.com", False)
```

## Troubleshooting

### Проблема: Скрипт не работает

```bash
# Проверьте переменные окружения
cd backend
source .env  # или используйте python-dotenv

# Проверьте подключение к Supabase
python -c "from supabase_client import get_supabase; print(get_supabase())"
```

### Проблема: Админ-статус не применяется

1. Проверьте, что миграция применена:

   ```sql
   SELECT column_name
   FROM information_schema.columns
   WHERE table_name = 'profiles' AND column_name = 'is_admin';
   ```

2. Проверьте статус в базе:

   ```sql
   SELECT email, is_admin FROM profiles WHERE email = 'your-email@example.com';
   ```

3. Перезапустите бэкенд после изменений

### Проблема: Логин не возвращает is_admin

Убедитесь, что все функции в `auth_service_supabase.py` обновлены и вызывают `get_user_admin_status()`.

## Дополнительные возможности

### Endpoint для проверки админ-статуса

Можно добавить в `main.py`:

```python
@app.get("/api/v1/auth/check-admin")
async def check_admin_status(current_user: UserProfile = Depends(require_auth)):
    """Check if current user is admin"""
    return {
        "is_admin": current_user.is_admin,
        "message": "You have full admin access" if current_user.is_admin else "Regular user access"
    }
```

### Middleware для админ-логирования

Можно добавить middleware для логирования всех действий администраторов.

---

**Создано**: 2 января 2025  
**Версия**: 1.0  
**Статус**: ✅ Готово к использованию
