# 🧪 Тестирование исправления бага с бесплатными попытками

## 📋 Быстрый старт

### Предварительные требования

1. ✅ Backend запущен: `http://localhost:8000`
2. ✅ Frontend запущен: `http://localhost:5173`
3. ✅ Redis запущен: `redis://localhost:6379`
4. ✅ Supabase настроен и доступен

---

## 🐍 Python тесты (Backend)

### Установка

```bash
# Убедитесь что backend dependencies установлены
cd backend
pip install -r requirements.txt
```

### Запуск

```bash
# Замените USER_ID на реальный UUID пользователя из Supabase
python test_free_trial_fix.py <USER_ID>

# Пример:
python test_free_trial_fix.py 12345678-1234-1234-1234-123456789012
```

### Что тестируется

✅ **TEST 1: Redis Lock Mechanism**

- Проверка приобретения блокировки
- Проверка что блокировка не может быть приобретена дважды
- Проверка освобождения блокировки

✅ **TEST 2: Free Trial Logic**

- Проверка получения информации о бесплатных попытках
- Проверка записи использования
- Проверка инкремента счетчика

✅ **TEST 3: check_user_can_analyze**

- Проверка функции проверки прав доступа
- Обработка подписки, бесплатной попытки, отсутствия доступа

✅ **TEST 4: Concurrent Requests**

- Проверка race condition
- Только один запрос должен получить блокировку

### Ожидаемый результат

```
🧪 ТЕСТИРОВАНИЕ ИСПРАВЛЕНИЯ БАГА С БЕСПЛАТНЫМИ ПОПЫТКАМИ
================================================================================

TEST 1: Redis Lock Mechanism
================================================================================

✅ Блокировка приобретена успешно
✅ Блокировка корректно занята (ожидаемое поведение)
✅ Блокировка освобождена
✅ Блокировка приобретена после освобождения
✅ TEST 1 PASSED: Redis блокировка работает корректно

[... другие тесты ...]

📊 ИТОГИ ТЕСТИРОВАНИЯ
================================================================================
Redis Lock Mechanism: ✅ PASSED
Free Trial Logic: ✅ PASSED
check_user_can_analyze: ✅ PASSED
Concurrent Requests: ✅ PASSED

Результат: 4/4 тестов пройдено
================================================================================

🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!
```

---

## 🎭 Playwright тесты (E2E)

### Установка

```bash
# Установить Playwright
npm install
npx playwright install
```

### Запуск

```bash
# Запустить все тесты
npx playwright test tests/test_free_trial_fix.spec.ts

# Запустить с UI
npx playwright test tests/test_free_trial_fix.spec.ts --ui

# Запустить конкретный тест
npx playwright test tests/test_free_trial_fix.spec.ts -g "Кэшированный результат"

# С отладкой
npx playwright test tests/test_free_trial_fix.spec.ts --debug
```

### Что тестируется

✅ **Test 1: Кэшированный результат не списывает попытку**

- Первый анализ списывает попытку
- Второй анализ того же профиля не списывает (из кэша)

✅ **Test 2: Проверка логов backend**

- Проверка сообщения "NO free trial used" в логах
- Проверка что кэшированный результат возвращается быстрее

✅ **Test 3: Race condition**

- Два запроса одновременно
- Попытка должна быть засчитана только один раз

✅ **Test 4: Сообщение об ошибке**

- Проверка корректного сообщения при исчерпании попыток

---

## 🔬 Ручное тестирование

### Сценарий 1: Кэшированный результат

1. **Войти** в систему как обычный пользователь (не админ)

2. **Проверить** начальное состояние:

   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" \
        http://localhost:8000/api/v1/free-trial/info
   ```

   Ожидается:

   ```json
   {
     "can_use_free_trial": true,
     "today_count": 0,
     "daily_limit": 1
   }
   ```

3. **Выполнить** первый анализ профиля `@charlidamelio`:
   - Frontend: Ввести @charlidamelio и нажать Analyze
   - Дождаться завершения (60-120 секунд)
4. **Проверить** что попытка засчиталась:

   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" \
        http://localhost:8000/api/v1/free-trial/info
   ```

   Ожидается:

   ```json
   {
     "can_use_free_trial": false,
     "today_count": 1,
     "daily_limit": 1
   }
   ```

5. **Выполнить** второй анализ того же профиля `@charlidamelio`:
   - Frontend: Ввести @charlidamelio и нажать Analyze
   - Должен вернуться почти мгновенно (из кэша)
6. **Проверить** что попытка НЕ засчиталась:

   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" \
        http://localhost:8000/api/v1/free-trial/info
   ```

   Ожидается:

   ```json
   {
     "can_use_free_trial": false,
     "today_count": 1, // ← Не изменилось!
     "daily_limit": 1
   }
   ```

7. **Проверить** логи backend:
   ```
   📋 Returning cached analysis for @charlidamelio (NO free trial used)
   ```

✅ **УСПЕХ:** Кэшированный результат не списал попытку!

---

### Сценарий 2: Race Condition

1. **Войти** в систему

2. **Открыть** два окна браузера с одним аккаунтом

3. **Одновременно** отправить запрос на анализ НОВОГО профиля:
   - Окно 1: @testuser1234 → Analyze
   - Окно 2: @testuser1234 → Analyze (сразу после)
4. **Ожидания:**

   - Одно окно: Выполняет полный анализ (60-120 сек)
   - Второе окно: Либо получает ошибку 409, либо ждёт и получает кэш

5. **Проверить** счётчик попыток:

   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" \
        http://localhost:8000/api/v1/free-trial/info
   ```

   Ожидается:

   ```json
   {
     "today_count": 1 // ← Только ОДНА попытка списана!
   }
   ```

✅ **УСПЕХ:** Race condition обработан корректно!

---

### Сценарий 3: Проверка Redis блокировки

1. **Подключиться** к Redis:

   ```bash
   redis-cli
   ```

2. **Выполнить** анализ профиля через frontend

3. **Во время выполнения** проверить блокировку:

   ```redis
   KEYS trendxl:v2:lock:*
   # Должна быть одна блокировка:
   # trendxl:v2:lock:analysis:USER_ID:USERNAME

   TTL trendxl:v2:lock:analysis:USER_ID:USERNAME
   # Должен быть TTL около 60 секунд
   ```

4. **После завершения** проверить что блокировка удалена:
   ```redis
   KEYS trendxl:v2:lock:*
   # Должно быть пусто
   ```

✅ **УСПЕХ:** Блокировка работает корректно!

---

## 🐛 Troubleshooting

### Redis не доступен

**Симптомы:**

```
⚠️ Redis not available, caching disabled
```

**Решение:**

```bash
# Запустить Redis через Docker
docker run -d -p 6379:6379 redis:alpine

# Или установить локально
# Windows: https://redis.io/docs/install/install-redis/install-redis-on-windows/
# Mac: brew install redis && brew services start redis
# Linux: sudo apt install redis-server && sudo service redis-server start
```

### Supabase ошибка

**Симптомы:**

```
❌ Failed to get free trial info: 404
```

**Решение:**

```bash
# Выполнить миграцию базы данных
cd backend
python setup_database.py

# Или вручную через Supabase SQL Editor:
# 1. MINIMAL_TABLES_ONLY.sql
# 2. ADD_POLICIES.sql
# 3. ADD_FUNCTIONS.sql
```

### Тест падает с timeout

**Симптомы:**

```
Test timeout of 30000ms exceeded
```

**Решение:**

```typescript
// В test_free_trial_fix.spec.ts добавить:
test.setTimeout(120000); // 2 минуты
```

### Пользователь не найден

**Симптомы:**

```
❌ TEST FAILED: User not found
```

**Решение:**

```bash
# Создать тестового пользователя через Supabase Dashboard
# Или использовать существующего пользователя
# Получить UUID через:
SELECT id FROM auth.users WHERE email = 'test@example.com';
```

---

## 📊 Метрики успеха

### ✅ Все тесты пройдены если:

1. **Python тесты:** 4/4 пройдено
2. **Playwright тесты:** Все пройдены без ошибок
3. **Ручные сценарии:**
   - Кэш не списывает попытки
   - Race condition обработан
   - Блокировка работает

### ❌ Проверить исправление если:

- Кэшированный результат списывает попытку
- Два одновременных запроса списывают попытку дважды
- Блокировка не освобождается
- Счётчик попыток неверный

---

## 🎯 Заключение

После прохождения всех тестов можно быть уверенным что:

✅ Бесплатные попытки засчитываются корректно  
✅ Кэшированные результаты не тратят попытки  
✅ Race condition обработан правильно  
✅ Блокировка работает надёжно

**Баг исправлен! 🎉**

---

## 📚 Дополнительные ресурсы

- [FREE_TRIAL_BUG_FIX.md](./FREE_TRIAL_BUG_FIX.md) - Подробное описание бага и исправления
- [backend/main.py](./backend/main.py) - Исправленный код
- [backend/services/cache_service.py](./backend/services/cache_service.py) - Redis блокировка
- [tests/test_free_trial_fix.spec.ts](./tests/test_free_trial_fix.spec.ts) - E2E тесты

---

**Дата:** 2025-10-04  
**Версия:** 2.0  
**Статус:** ✅ Готово к тестированию
