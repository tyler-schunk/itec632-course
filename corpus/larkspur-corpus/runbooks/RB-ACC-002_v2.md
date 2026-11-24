---
doc_id: RB-ACC-002
title: MFA enrollment and reset
doc_type: runbook
version: "2"
effective_date: 2025-03-03
owner: Renee Castillo
audience: internal
---

# RB-ACC-002 MFA enrollment and reset

## Purpose / When to use

Use when a user needs to enroll in multifactor authentication for the first time (new hire, or a client turning on MFA), or needs MFA reset because they got a new phone, lost their phone, reinstalled Microsoft Authenticator, or are not getting prompts.

## Standard method

- The only approved method for new enrollments is **Microsoft Authenticator push notifications with number matching**.
- **SMS text codes are not allowed for new enrollments.** Voice call is not allowed either.
- Users who cannot use a smartphone (rare): escalate to Renee Castillo, who will arrange a FIDO2 security key through the account manager.

## Prerequisites / access needed

- Harbor PSA (contact record, Authorized Contacts tab)
- Entra admin center via GDAP with Authentication Administrator (or Privileged Authentication Administrator for admin users)
- The user should have their phone with them and be at a computer

## Identity verification (required)

1. **Call the user back at the phone number on file in Harbor PSA.**
2. **For any MFA reset, also confirm with the client's designated authorized contact.** Call the authorized contact at their number on file and get approval. Record name and time.
3. For first-time enrollment of a new hire whose account we created under RB-ACC-003, the onboarding ticket approval from the authorized contact counts as confirmation; still call the user at the number on file.
4. Never verify by date of birth or SSN.

## Steps

### A. First-time enrollment

1. Complete verification.
2. Have the user install **Microsoft Authenticator** from the App Store or Google Play. Not a third-party authenticator app.
3. For a brand-new account, issue a **Temporary Access Pass** (TAP) so the user can register without a password prompt loop: Entra admin center > **Identity > Users > All users** > user > **Authentication methods** > **Add authentication method** > **Temporary Access Pass**. Lifetime 1 hour, one-time use. Read it to the user on the call. Do not email it or put it in the ticket.
4. User goes to https://aka.ms/mysecurityinfo (or https://aka.ms/mfasetup), signs in, and adds **Authenticator app**. They scan the QR code with Authenticator.
5. Microsoft sends a test notification. The user types the two-digit number shown on screen into the Authenticator app. That is number matching; confirm they saw the number prompt.
6. Confirm the method shows as **Microsoft Authenticator** (push) and is set as the default sign-in method on the Security info page.
7. If the user's Security info page shows a **Phone** method, remove it. SMS/voice should not be present on new enrollments.

### B. MFA reset (new phone, lost phone, no prompts)

1. Complete verification **including authorized contact confirmation**.
2. Entra admin center > **Identity > Users > All users** > user > **Authentication methods**.
3. Delete the old Microsoft Authenticator entry (it shows the old device name). Or select **Require re-register multifactor authentication**.
4. Select **Revoke multifactor authentication sessions** so remembered devices must prompt again.
5. Issue a Temporary Access Pass (1 hour, one-time) and read it to the user on the call.
6. Walk them through Section A steps 4-6 on the new phone.
7. Have them sign out and back in to Outlook and Teams on their phone and confirm the push arrives with a number prompt.

### C. "I'm not getting prompts"

1. Check the phone: notifications allowed for Authenticator, phone not in Focus/Do Not Disturb, date and time automatic, app updated.
2. Open Authenticator and pull down to refresh; pending requests often appear there.
3. Check Entra sign-in logs for the user (Authentication Details column) to see whether the push was sent and how it failed.
4. If the phone was restored from backup, the Authenticator registration usually does not carry over; do a reset (Section B).

## Priority guidance

- Single user unable to complete MFA: **P3**. VIP fully blocked: **P2**.
- New hire enrollment scheduled with onboarding: **P4**, part of RB-ACC-003.
- Unexpected MFA prompts the user did not trigger (MFA fatigue): **P2**, tell the user to deny, and escalate to Renee Castillo. Reset the password per RB-ACC-001.

## Escalate if

- The authorized contact cannot be reached for an MFA reset: do not reset. Note the ticket, set it to Waiting on Client, and tell Priya Raman if the user is a VIP.
- Admin accounts or break-glass accounts: Renee Castillo only.
- The client's tenant still has SMS or voice enabled in the Authentication methods policy: open a P4 for Renee Castillo to review the policy.
- User insists on SMS: explain the policy; escalate to the account manager if the client pushes back.

## Ticket notes

- Callback number used and authorized contact name and time (for resets)
- Method enrolled (Authenticator push with number matching) and old methods removed
- TAP issued (yes/no, by phone); never record the TAP value
- Test sign-in result

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2022-09-01 | Renee Castillo | Initial MFA enrollment and reset procedure. |
| 2 | 2025-03-03 | Renee Castillo | Authenticator push with number matching is the only method for new enrollments; SMS and voice removed. Added TAP, authorized contact confirmation for resets, MFA fatigue guidance. |
