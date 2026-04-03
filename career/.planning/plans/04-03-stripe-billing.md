# 04-03: Implement Stripe Billing

**Epic**: Productization

## Goal

Integrate Stripe for subscription payments and usage-based overages.

## Acceptance Criteria

- Stripe account set up (Products: Basic $29/mo, Pro $99/mo, Enterprise custom)
- Webhook endpoint to handle invoice events (payment succeeded/failed)
- User signup flow: create tenant, generate API key, redirect to Stripe Checkout
- Customer portal to manage subscription, update payment method
- Metered usage for overages (e.g., >1000 tasks/mo → $0.10/task)

## Tasks

1. Install Stripe Python SDK
2. Create checkout session API (POST /api/checkout)
3. Build webhook handler to activate tenant on successful payment
4. Build customer portal link generation
5. Add usage reporting endpoint for Stripe metering
6. Test complete flow (test mode)

## Dependencies

04-02

## Time Estimate

12 hours
