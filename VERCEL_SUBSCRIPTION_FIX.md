# Vercel Subscription Endpoints Fix

## 🔧 Проблема

При работе с деплоем на Vercel возникали ошибки 404 для эндпоинтов подписки:

```
POST /api/v1/subscription/create-payment-link 404 (Not Found)
Error starting checkout: Failed to start checkout process
```

### Причина

В файле `api/main.py` (который используется для деплоя на Vercel) **отсутствовали** все эндпоинты для работы с подписками Stripe. Эти эндпоинты были только в `backend/main.py` (для локальной разработки).

## ✅ Решение

Добавлены все недостающие эндпоинты подписки в `api/main.py`:

### Добавленные эндпоинты:

1. **GET `/api/v1/subscription/info`** - получение информации о подписке пользователя
2. **POST `/api/v1/subscription/checkout`** - создание Checkout сессии Stripe
3. **POST `/api/v1/subscription/create-payment-link`** - создание публичной ссылки на оплату (без авторизации)
4. **GET `/api/v1/subscription/check`** - проверка активной подписки
5. **POST `/api/v1/subscription/cancel`** - отмена подписки
6. **POST `/api/v1/subscription/reactivate`** - реактивация подписки
7. **POST `/api/v1/webhook/stripe`** - webhook для обработки событий Stripe

### Ключевой эндпоинт для фронтенда

```python
@app.post("/api/v1/subscription/create-payment-link")
async def create_payment_link_public(
    user_email: Optional[str] = None,
    success_url: Optional[str] = None,
    cancel_url: Optional[str] = None
):
    """
    Create a public payment link for subscription
    Anyone can use this to subscribe - no authentication required
    """
```

Этот эндпоинт создает публичную ссылку для оплаты подписки, которую может использовать любой пользователь без необходимости авторизации.

## 📋 Что было сделано

1. Скопированы все эндпоинты подписки из `backend/main.py` в `api/main.py`
2. Добавлен обработчик Stripe webhook для автоматической синхронизации статуса подписки
3. Обновлен корневой эндпоинт `/` с перечислением всех доступных эндпоинтов
4. Проверены импорты - все необходимые функции уже были импортированы из `stripe_service.py` и `supabase_client.py`

## 🚀 Деплой

После коммита изменений Vercel автоматически:

- Подхватит обновленный `api/main.py`
- Задеплоит новую версию API
- Сделает доступными все эндпоинты подписки

### Проверка работы

После деплоя проверьте:

1. **Health check**: `GET /health` → должен вернуть статус "healthy"
2. **Root endpoint**: `GET /` → должен показать все эндпоинты включая subscription\_\*
3. **Payment link**: `POST /api/v1/subscription/create-payment-link` → должен вернуть `payment_url`

## 📝 Структура API

```
/api/v1/
├── auth/
│   ├── register          ✅ Регистрация
│   ├── login            ✅ Вход
│   ├── me               ✅ Текущий пользователь
│   └── profile          ✅ Обновление профиля
├── subscription/
│   ├── info             ✅ Информация о подписке
│   ├── checkout         ✅ Checkout сессия
│   ├── create-payment-link  ✅ Публичная ссылка на оплату
│   ├── check            ✅ Проверка статуса
│   ├── cancel           ✅ Отмена подписки
│   └── reactivate       ✅ Реактивация
├── webhook/
│   └── stripe           ✅ Stripe webhook
└── [другие эндпоинты]
```

## 🔐 Авторизация

- **Требуют авторизацию**: `/info`, `/checkout`, `/check`, `/cancel`, `/reactivate`
- **Публичные**: `/create-payment-link` (можно вызывать без токена)

## 📊 Интеграция со Stripe

Эндпоинты работают с:

- **Stripe Checkout** - для создания сессий оплаты
- **Stripe Customer** - для привязки пользователей
- **Stripe Subscription** - для управления подписками
- **Stripe Webhooks** - для автоматической синхронизации

## ⚙️ Переменные окружения

Убедитесь, что в Vercel настроены:

```env
STRIPE_API_KEY=sk_...
STRIPE_PRICE_ID=price_...
SUPABASE_URL=https://...
SUPABASE_KEY=eyJ...
```

## 🎯 Результат

- ✅ Все эндпоинты подписки доступны на Vercel
- ✅ Фронтенд может создавать payment links
- ✅ Пользователи могут оформить подписку
- ✅ Webhook автоматически обновляет статусы
- ✅ `api/main.py` и `backend/main.py` синхронизированы

## 📌 Commit

```
071b1e3 - fix: Add missing Stripe subscription endpoints to api/main.py for Vercel deployment
```

---

**Дата:** 2025-10-02  
**Статус:** ✅ Исправлено и задеплоено
