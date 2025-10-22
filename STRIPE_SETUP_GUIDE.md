# Stripe Configuration Guide for TrendXL 2.0

This guide explains how to configure Stripe for TrendXL subscriptions and troubleshoot common issues.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Stripe Customer Portal Setup](#stripe-customer-portal-setup)
3. [Environment Variables](#environment-variables)
4. [Testing](#testing)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Stripe account (test or live mode)
- Access to Stripe Dashboard
- Vercel account with environment variables configured

---

## Stripe Customer Portal Setup

The **Customer Portal** allows users to manage their subscriptions (update payment methods, cancel subscriptions, view invoices).

### Why You Need This

Without activating the Customer Portal:
- Users can't manage their subscriptions
- "Manage Subscription" button shows empty page
- No options to cancel or update payment methods appear

### Step-by-Step Activation

#### For Test Mode (using `sk_test_xxx` API key):

1. **Open Stripe Dashboard in Test Mode**:
   - Go to: https://dashboard.stripe.com/test/settings/billing/portal
   - Make sure you're in **Test Mode** (toggle in top right)

2. **Activate Customer Portal**:
   - Click "Activate Customer Portal" button
   - Or if already activated, click "Edit" to customize

3. **Configure Portal Settings**:
   - ✅ **Allow customers to update payment methods**
   - ✅ **Allow customers to cancel subscriptions**
     - Set cancellation behavior:
       - ☑ Cancel at end of billing period (recommended)
       - OR
       - ☐ Cancel immediately
   - ✅ **Allow customers to update billing information**
   - ✅ **Show invoices and payment history**
   - ✅ **Allow customers to switch plans** (optional)

4. **Customize Appearance** (optional):
   - Add your logo
   - Set brand colors
   - Customize email templates

5. **Save Settings**:
   - Click "Save" at the bottom

6. **Test Configuration**:
   ```bash
   # After deployment, test the portal
   curl -X POST https://your-app.vercel.app/api/v1/subscription/manage \
     -H "Authorization: Bearer YOUR_TEST_JWT_TOKEN"
   ```

#### For Live Mode (using `sk_live_xxx` API key):

**IMPORTANT**: Test and Live modes have **SEPARATE** Customer Portal configurations!

1. **Switch to Live Mode** in Stripe Dashboard (toggle in top right)
2. **Go to**: https://dashboard.stripe.com/settings/billing/portal
3. **Repeat all steps** from Test Mode setup above
4. **Test with live API key** before going to production

---

## Troubleshooting

### Problem 1: "Failed to create payment link"

**Symptoms:**
- Error when clicking "Subscribe Now"
- Alert: "Failed to create payment link. Please try again."

**Solution:**
1. Check if STRIPE_API_KEY and STRIPE_PRICE_ID are set in Vercel environment variables
2. Run verification: `python3 scripts/verify-deployment.py`
3. Check Vercel logs for detailed error messages

---

### Problem 2: Customer Portal shows empty page (no buttons)

**Symptoms:**
- Customer Portal opens
- Shows payment methods and billing info
- But no "Cancel subscription" or "Update subscription" buttons

**Cause:**
- Customer Portal is NOT activated in Stripe Dashboard for the current mode (test/live)

**Solution:**

1. **Check which mode you're using:**
   ```bash
   python3 scripts/verify-deployment.py
   # Look for "STRIPE_API_KEY: sk_test_xxx" (test) or "sk_live_xxx" (live)
   ```

2. **Activate Customer Portal in correct mode:**

   **If Test Mode:**
   - Go to: https://dashboard.stripe.com/test/settings/billing/portal
   - Click "Activate Customer Portal"
   - Enable subscription management options
   - Save

   **If Live Mode:**
   - Go to: https://dashboard.stripe.com/settings/billing/portal
   - Click "Activate Customer Portal"
   - Enable subscription management options
   - Save

---

## Quick Reference

| Action | Test Mode URL | Live Mode URL |
|--------|--------------|---------------|
| Customer Portal Settings | https://dashboard.stripe.com/test/settings/billing/portal | https://dashboard.stripe.com/settings/billing/portal |
| API Keys | https://dashboard.stripe.com/test/apikeys | https://dashboard.stripe.com/apikeys |
| Webhooks | https://dashboard.stripe.com/test/webhooks | https://dashboard.stripe.com/webhooks |
| Products & Prices | https://dashboard.stripe.com/test/products | https://dashboard.stripe.com/products |

---

**Last Updated:** 2025-10-22
