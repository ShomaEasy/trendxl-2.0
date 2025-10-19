# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**TrendXL 2.0** is a full-stack TikTok trend analysis platform that helps users discover trending content by analyzing TikTok profiles. It uses AI to extract relevant hashtags and find trending videos.

**Stack:**

- **Frontend**: React 18.2 + TypeScript 5.2 + Vite 4.5 + Chakra UI 3.26 + Tailwind CSS 3.3
- **Backend**: FastAPI 0.104 (Python) + Supabase (PostgreSQL) + Stripe
- **Deployment**: Vercel (frontend + serverless backend via Mangum)
- **Testing**: Playwright 1.55 (E2E)
- **APIs**: Ensemble Data (TikTok), OpenAI (GPT-4o), Perplexity AI

## Development Commands

### Frontend Development

```bash
npm run dev              # Start Vite dev server on port 3000 (with --host for external access)
npm run build           # Build for production (outputs to dist/)
npm run preview         # Preview production build locally
npm run lint            # Run ESLint
npm run lint:fix        # Auto-fix ESLint issues
```

### Backend Development

```bash
# From backend/ directory
python run_server.py    # Start FastAPI server on port 8000 (with uvicorn --reload)

# Or from root:
npm run backend         # Start backend server
npm run dev:full        # Run both frontend and backend concurrently (uses concurrently package)
```

### Testing

```bash
# E2E Tests (Playwright)
npx playwright test                    # Run all Playwright tests
npx playwright test --ui              # Run tests in UI mode with interactive debugging
npx playwright test --debug           # Run tests in debug mode (step-by-step)
npx playwright show-report            # View HTML test report
# Base URL: http://localhost:5173, Browser: Chromium

# Backend tests
cd backend && python test_free_trial.py <user-uuid>  # Test free trial system
```

## Project Structure

```
trendxl-2.0/
├── api/                      # Vercel serverless functions
│   └── index.py             # Main entry point (Mangum wrapper for FastAPI)
├── backend/                  # FastAPI backend
│   ├── main.py              # FastAPI app definition
│   ├── run_server.py        # Dev server launcher (uvicorn)
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic models
│   ├── services/            # Business logic services
│   │   ├── trend_analysis_service.py
│   │   ├── ensemble_service.py
│   │   ├── openai_service.py
│   │   ├── perplexity_service.py
│   │   ├── content_relevance_service.py
│   │   ├── cache_service.py
│   │   ├── auth_service_supabase.py
│   │   ├── stripe_service.py
│   │   └── supabase_client.py
│   └── *.sql                # Database migration files
├── src/                      # React frontend source
│   ├── components/          # React components
│   ├── contexts/            # React contexts (AuthContext)
│   ├── hooks/               # Custom hooks (useTrendAnalysis, useAutoRefresh)
│   ├── pages/               # Page components
│   ├── services/            # API services (backendApi, subscriptionService)
│   ├── types/               # TypeScript type definitions
│   └── main.tsx             # React entry point
├── public/                   # Static assets
├── tests/                    # Playwright E2E tests
├── dist/                     # Build output (Vite)
├── supabase/                 # Supabase configuration
├── vercel.json               # Vercel deployment config
├── vite.config.ts            # Vite build config
├── tailwind.config.js        # Tailwind CSS config
├── tsconfig.json             # TypeScript config
├── playwright.config.ts      # Playwright test config
└── package.json              # NPM dependencies and scripts
```

## Architecture

### Frontend-Backend Communication

**Development:** Frontend (localhost:3000) → Backend (localhost:8000)

**Production (Vercel):**

- Frontend and backend both deployed on same domain
- Frontend uses relative paths (no explicit backend URL)
- API routes handled via `vercel.json` rewrites to `/api/` serverless functions
- Entry point: `api/index.py` (Mangum ASGI adapter wraps FastAPI)
- Timeout: 300s (5 min) for `/api/*` endpoints
- Environment: `VITE_BACKEND_API_URL` set to empty string on Vercel

### Key Services (Backend)

**Trend Analysis Pipeline:**

1. `ensemble_service.py` (~1500 lines) - Fetches TikTok profile/posts via Ensemble Data API
   - Official Ensemble Data SDK integration
   - Cursor pagination for posts and hashtag search
   - Rate limiting (3.0s between requests)
   - Config: max_depth=5, max_cursor=2000

2. `openai_service.py` (~300 lines) - Extracts hashtags using GPT-4o
   - GPT-4o model for text and vision analysis
   - Token counting for billing
   - Structured response parsing

3. `perplexity_service.py` (~700 lines) - Discovers Creative Center hashtags via Perplexity
   - AI-powered hashtag discovery
   - Async HTTP requests
   - Health checks and connection management

4. `content_relevance_service.py` (~650 lines) - Validates relevance of trending videos
   - GPT-4o Vision for image analysis
   - Content relevance scoring (0.0-1.0)
   - Batch image processing
   - Fallback handling for missing images

5. `trend_analysis_service.py` (~1200 lines) - Orchestrates the entire pipeline
   - Coordinates all services above
   - Token usage tracking (OpenAI, Perplexity, Ensemble)
   - Caching integration
   - Comprehensive error handling and logging

**Other Services:**

- `cache_service.py` - Redis caching (optional, falls back to in-memory)
- `advanced_creative_center_service.py` - TikTok Creative Center hashtag discovery
- `auth_service_supabase.py` - User authentication via Supabase
  - JWT token creation/validation
  - Password hashing (bcrypt)
  - User profile CRUD
- `stripe_service.py` - Subscription management via Stripe
  - Customer creation
  - Checkout sessions
  - Webhook handling
- `supabase_client.py` - Database operations
  - User management
  - Free trial tracking
  - Token usage recording
  - Subscription status

**Service Entry Points:**

- **Backend**: `backend/main.py` - FastAPI app with CORS, lifespan events, health checks
- **Dev Server**: `backend/run_server.py` - Uvicorn launcher with hot reload
- **Vercel**: `api/index.py` - Mangum ASGI adapter for serverless

### Frontend Architecture

**Key Context & Hooks:**

- **`AuthContext.tsx`** (315 lines) - Global auth state management
  - User authentication state
  - JWT token storage (localStorage)
  - Supabase session management
  - Login/logout/register logic
  - Auto-refresh token on page load

- **`useTrendAnalysis.ts`** (351 lines) - Main analysis hook
  - Free trial checking
  - Subscription validation
  - Backend API integration
  - Loading states and error handling

- **`useAutoRefresh.ts`** (83 lines) - Auto-refresh free trial status
  - Polls status every 60 seconds
  - Real-time countdown updates
  - Unsubscribes on unmount

**Key Services:**

- **`backendApi.ts`** (670 lines) - Axios HTTP client
  - Request/response interceptors
  - Token management and refresh
  - All API endpoints centralized

- **`subscriptionService.ts`** (323 lines) - Stripe integration
  - Checkout session creation
  - Subscription status checking
  - Cancel/reactivate flows

- **`scanHistoryService.ts`** (165 lines) - Scan history management
  - Save analysis results to Supabase
  - Retrieve user's saved scans
  - Delete scan history

**Key Pages:**

- `HomePage.tsx` (282 lines) - Main analysis interface
- `AnalysisResultPage.tsx` - Display trending hashtags & videos
- `MyTrends.tsx` - User's saved analyses history

**Key Components:**

- **Authentication**: `AuthModal.tsx`, `UserProfileDropdown.tsx`
- **Analysis UI**: `ProfileInput.tsx`, `TrendGrid.tsx`, `TrendCard.tsx`, `VideoModal.tsx`, `HashtagList.tsx`
- **Status/Info**: `FreeTrialCounter.tsx`, `UnifiedSubscriptionBanner.tsx`, `ApiStatusBanner.tsx`
- **Loading/Error**: `LoadingStates.tsx`, `ErrorState.tsx`
- **Visual Effects**: `Aurora.tsx` (WebGL background), `GradientText.tsx`, `DarkVeil.tsx`

### Authentication Flow

1. User registers/logs in → `AuthContext.tsx` handles state
2. Auth tokens stored in localStorage and Supabase session
3. Backend validates JWT tokens via `get_current_user_from_token()`
4. Token passed via `Authorization: Bearer <token>` header
5. Supabase Auth integration provides fallback for token retrieval

### Subscription & Free Trial System

**Free Trial:**

- New users get 1 free analysis per day
- Tracked in `daily_free_analyses` table (Supabase)
- Resets daily at 00:00 UTC
- Check via `/api/v1/free-trial/info` endpoint
- **Auto-refresh system**: Frontend components auto-update every 60 seconds (`useAutoRefresh.ts`)
- **Pre-check validation**: Status checked BEFORE backend request for better UX
- **Real-time countdown**: Shows exact time until reset with auto-update

**Subscription (Stripe):**

- Checkout flow: Create session → User pays → Webhook updates Supabase
- Check subscription: `/api/v1/subscription/check`
- Admin users (`is_admin=true`) bypass all limits
- Subscription info stored in `profiles` table (`stripe_customer_id`, `subscription_status`, `subscription_end_date`)
- Price: $29/month (configured via `STRIPE_PRICE_ID`)

### Database Schema (Supabase)

**profiles table (auth.users):**

- `id` (UUID) - Primary key
- `email`, `username`, `password_hash`
- `stripe_customer_id`, `subscription_status`, `subscription_end_date`
- `is_admin` - Bypass all limits
- `full_name`, `avatar_url`, `bio`

**scan_history table:**

- Stores complete analysis results for "My Trends" feature
- `id` (UUID), `user_id` (references auth.users)
- `username` (TikTok username analyzed)
- `profile_data` (JSONB) - Complete analysis: profile, trends, hashtags, posts, tokenUsage
- `scan_type` ('free' or 'paid')
- `created_at`, `updated_at`
- RLS enabled - users can only view/edit their own scans

**daily_free_analyses table:**

- Tracks free trial usage per user per day
- Unique constraint: one user per day
- Auto-cleanup after 90 days

**token_usage table:**

- Tracks API token consumption (OpenAI, Perplexity, Ensemble)
- Used for analytics and cost tracking

## Environment Variables

### Frontend (.env or Vercel)

```bash
VITE_BACKEND_API_URL=        # Empty for Vercel, http://localhost:8000 for dev
```

### Backend (.env or Vercel)

```bash
# Required
SUPABASE_URL=                # Supabase project URL
SUPABASE_KEY=                # Supabase anon key
SUPABASE_SERVICE_KEY=        # Supabase service role key
JWT_SECRET=                  # For JWT token signing
STRIPE_API_KEY=              # Stripe secret key
STRIPE_PRICE_ID=             # Stripe subscription price ID
ENSEMBLE_API_TOKEN=          # Ensemble Data API key
OPENAI_API_KEY=              # OpenAI API key
PERPLEXITY_API_KEY=          # Perplexity API key

# Optional
REDIS_URL=                   # Redis cache (optional)
STRIPE_WEBHOOK_SECRET=       # For Stripe webhook verification
```

## Code Style & Conventions

### TypeScript/React (from .cursor/rules)

**Code Style:**
- Use functional components with TypeScript interfaces (not types)
- Prefer named exports for components
- Use descriptive variable names with auxiliary verbs (isLoading, hasError)
- Avoid enums; use maps instead
- Structure files: exported component → subcomponents → helpers → static content → types

**React Patterns:**
- Minimize 'use client', 'useEffect', 'setState' where possible
- Use functional and declarative programming patterns; avoid classes
- Prefer iteration and modularization over code duplication
- Use the "function" keyword for pure functions

**UI and Styling:**
- Use Chakra UI, Shadcn UI, and Tailwind for styling
- Mobile-first responsive design with Tailwind CSS
- Use lowercase with dashes for directories (e.g., `components/auth-wizard`)

**Performance:**
- Optimize images: WebP format, include size data, implement lazy loading
- Use dynamic loading for non-critical components
- Optimize Web Vitals (LCP, CLS, FID)

### Python/FastAPI

- Async/await for all I/O operations
- Pydantic models for request/response validation
- Type hints everywhere
- Comprehensive error handling via `error_responses.py`
- Logging via Python's logging module (logger.info, logger.error)
- Rate limiting via middleware (60 requests/minute default)

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user info
- `PUT /api/v1/auth/profile` - Update user profile

### Trend Analysis

- `POST /api/v1/analyze` - Main analysis endpoint (requires auth)
  - Checks subscription/free trial before processing
  - Records token usage
  - Returns profile, posts, hashtags, trending videos

### Scan History (My Trends)

- `POST /api/v1/scan-history` - Save analysis result to user's history
- `GET /api/v1/scan-history` - Get user's saved scans
- `DELETE /api/v1/scan-history/{scan_id}` - Delete specific scan

### Subscription

- `GET /api/v1/subscription/info` - Get subscription details
- `GET /api/v1/subscription/check` - Check active subscription
- `POST /api/v1/subscription/checkout` - Create Stripe checkout session
- `POST /api/v1/subscription/create-payment-link` - Public payment link
- `POST /api/v1/subscription/cancel` - Cancel subscription
- `POST /api/v1/subscription/reactivate` - Reactivate subscription

### Free Trial

- `GET /api/v1/free-trial/info` - Get free trial status

### Health

- `GET /health` - Health check endpoint

## Common Development Tasks

### Adding a new API endpoint

1. Define Pydantic model in `backend/models.py`
2. Add route handler in `backend/main.py`
3. Add corresponding service function in `backend/services/`
4. Create frontend service function in `src/services/`
5. Update TypeScript types in `src/types/`

### Modifying the analysis pipeline

- Main orchestration: `backend/services/trend_analysis_service.py`
- Individual services in `backend/services/`
- Token usage tracking built into each service
- Caching via `cache_service.py`

### Database migrations

- SQL files in `backend/` directory
- Run via Supabase Dashboard → SQL Editor
- Test locally before production

**Migration files (run in order):**

1. `supabase_migration.sql` - Base tables (users, trend_feed, etc.)
2. `supabase_token_usage_migration.sql` - Token usage tracking
3. `supabase_stripe_migration.sql` - Stripe subscription fields
4. `supabase_free_trial_migration.sql` - Daily free trial system
5. `supabase_admin_migration.sql` - Admin user support
6. `supabase_scan_history_migration.sql` - **NEW:** My Trends history storage

**Important:** The `scan_history` table is required for the "My Trends" feature to work. Without it, analysis results won't be saved.

### Build Configuration

**Vite (vite.config.ts):**

- Dev server port: 3000 (with `--host` for external access)
- Build output: `dist/` directory
- Path alias: `@` → `src/`
- Rollup chunks: vendor (react, react-dom), ui (lucide-react)
- No sourcemaps in production

**TypeScript (tsconfig.json):**

- Target: ES2020, Module: ESNext
- Strict mode enabled (noUnusedLocals, noUnusedParameters)
- JSX: react-jsx
- Path mapping: `@/*` → `src/*`

**Tailwind (tailwind.config.js):**

- Monochromatic color scheme (white, black, grays)
- Custom fonts: Inter, Orbitron, JetBrains Mono
- Custom animations: fade-in, slide-up, gradient, float
- Rounded corners: card (16px), buttons (8px), tags (rounded)

**Playwright (playwright.config.ts):**

- Test dir: `./tests`
- Base URL: http://localhost:5173
- Browser: Chromium
- Auto-start dev server (`npm run dev`)
- Reporter: HTML with screenshots on failure

### Deployment

**Vercel (recommended):**

```bash
git push origin main  # Auto-deploys via Vercel integration
```

**Manual deploy:**

```bash
vercel --prod
```

**Vercel Configuration (vercel.json):**

- Build: `npm run build` → outputs to `dist/`
- Framework: Vite
- Rewrites: `/api/*` → `api/index.py` (300s timeout)
- Environment: `VITE_BACKEND_API_URL=""` (empty for relative paths)

## Important Notes

### Backend Configuration (config.py)

- **API rate limiting**: 60 requests/minute (MAX_REQUESTS_PER_MINUTE)
- **Free trial limit**: 1 analysis/day for non-subscribers
- **Admin users** (`is_admin=true`) bypass all limits
- **Max posts per user**: 20 (MAX_POSTS_PER_USER - optimized for Vercel timeout)
- **Max videos per hashtag**: 10 (MAX_VIDEOS_PER_HASHTAG)
- **Max hashtags to analyze**: 5 (MAX_HASHTAGS_TO_ANALYZE)

### Cache Configuration

- **Profile TTL**: 1800s (30 min) - PROFILE_TTL
- **Posts TTL**: 900s (15 min) - POSTS_TTL
- **Trends TTL**: 300s (5 min) - TRENDS_TTL
- Redis is optional; falls back to in-memory cache

### Production (Vercel)

- **Serverless timeout**: 300s (5 min) for `/api/*` endpoints
- **Entry point**: `api/index.py` (Mangum wraps FastAPI)
- **Build output**: `dist/` directory
- All external API usage tracked in `token_usage` table

### Documentation

- **README.md**: Contains TikTok API guide (Ensemble Data documentation)
- **CLAUDE.md**: This file - codebase guidance for Claude Code

## Troubleshooting

### 504 Gateway Timeout Errors

**Symptom:** `/api/v1/analyze` endpoint returns 504 error in production

**Causes:**

- Vercel serverless function timeout (default 60s, now set to 300s)
- Too many posts being fetched and analyzed
- Multiple sequential API calls (Ensemble → OpenAI → Perplexity → Ensemble)

**Solutions:**

1. ✅ Increased Vercel timeout to 300s in `vercel.json`
2. ✅ Reduced `max_posts_per_user` from 50 to 20 in `backend/config.py`
3. Enable Redis caching to speed up repeated requests
4. Consider implementing async/streaming responses for long-running analyses

### Missing Avatar/Cover Images (Warnings in Logs)

**Symptom:** Logs show `⚠️ No avatar found` or `⚠️ No cover image found`

**Not Actually an Error:**

- These are informational warnings, not failures
- System has fallback mechanisms:
  - Avatars: Returns empty string when not found
  - Cover images: Uses first image from `additional_images` array
- Profile analysis completes successfully despite warnings

**Root Cause:**

- Ensemble Data API response structure varies by profile
- Some profiles don't expose avatar URLs in expected fields
- TikTok API may return different image structures

### Creative Center 404 Errors

**Symptom:** `/api/v1/analyze-creative-center` returns 404

**Solution:**

- This endpoint may not be implemented on Vercel
- Frontend falls back to traditional analysis automatically
- Check `backend/main.py` for Creative Center endpoint implementation

## Design Patterns & Best Practices

### Frontend Patterns

- **Context API** for global state (AuthContext)
- **Custom hooks** for business logic (useTrendAnalysis, useAutoRefresh)
- **Service layer** for API calls (backendApi.ts, subscriptionService.ts)
- **Component composition** for UI reusability
- **Axios interceptors** for token management and refresh
- **Type-safe** with TypeScript interfaces (no types, no enums)

### Backend Patterns

- **Service layer** pattern (TrendAnalysisService orchestrates all services)
- **Dependency injection** via FastAPI `Depends()`
- **Async/await** for all I/O operations
- **Pydantic validation** for request/response models
- **Error handling** with custom exceptions and middleware
- **Caching** with fallback (Redis → in-memory)
- **Rate limiting** via middleware

### Performance Optimizations

- **Frontend**: Lazy loading, React memo, code splitting (vendor/ui chunks)
- **Backend**: Redis caching, reduced post limit (20 vs 50), cursor pagination
- **API**: Rate limiting (60 req/min), request batching
- **Database**: Indexes on user_id, created_at, RLS policies
- **Images**: Fallback handling, selective loading, WebP format
- **Build**: Vite tree-shaking, no sourcemaps in production
