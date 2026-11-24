---
doc_id: RB-ACC-002
title: MFA enrollment and reset
doc_type: runbook
version: "1"
effective_date: 2022-09-01
owner: Renee Castillo
audience: internal
---

# RB-ACC-002 MFA enrollment and reset

## Purpose / When to use

Use when a user needs to set up multifactor authentication for Microsoft 365, or needs MFA reset after getting a new phone or losing access to their method.

## Approved methods

- **Primary:** Microsoft Authenticator app (push notification).
- **Backup:** SMS text codes to the user's mobile phone are acceptable as a backup method during enrollment. Users who do not want the app on their phone may enroll with SMS only.
- Encourage the Authenticator app but do not hold up enrollment over it.

## Prerequisites / access needed

- Harbor PSA (user contact record)
- Azure AD (Entra) admin access to the client tenant with Authentication Administrator
- User should have their phone in hand

## Identity verification

Verify the user per RB-ACC-001 before any reset.

## Steps

### A. First-time enrollment

1. Have the user install Microsoft Authenticator.
2. User signs in at https://aka.ms/mfasetup.
3. Choose **Mobile app** > **Receive notifications for verification**, and scan the QR code.
4. Approve the test notification.
5. Add a backup method: **Authentication phone** with **Send me a code by text message**, using the user's mobile number. Have the user enter the code to confirm.
6. If the user declines the app, set **Authentication phone** (text message) as the default method.

### B. MFA reset

1. Verify the user.
2. Azure AD admin center > **Users** > user > **Authentication methods**.
3. Select **Require re-register multifactor authentication**.
4. Select **Revoke multifactor authentication sessions**.
5. Have the user sign in again and complete Section A.
6. If they are in a hurry, have them register a text message method first and add the app later.

### C. No prompts arriving

1. Check notifications are on for Authenticator and the phone has data.
2. Have the user choose **Sign in another way** and use the text code backup.
3. If neither works, reset (Section B).

## Priority guidance

- Single user blocked: P3. Executive blocked: P2.
- Enrollment as part of a new user setup: P4.

## Escalate if

- Admin accounts: Renee Castillo.
- Repeated unexpected prompts: Renee Castillo.
- Client wants MFA turned off for a user: account manager and Renee Castillo.

## Ticket notes

- How the user was verified
- Methods enrolled (app, text message)
- Test sign-in result

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2022-09-01 | Renee Castillo | Initial MFA enrollment and reset procedure. |
