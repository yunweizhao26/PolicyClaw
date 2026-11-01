# Privacy-policy page rubric

This rubric defines the page labels for the PolicyClaw corpus. The LLM verifier (`corpus/collect/verify.py`) and the human-style labelers use the same rubric and see the same view of each page.

## What you see

Each page shows its source URL (when known), its length in words, and its text. The text was extracted from a web page, so it can contain menus, headers, footers and cookie banners around the main content. Very long lines are wrapped.

A page longer than 1,800 words is cut: you see its first 1,500 words and its last 300 words, and a marker line between them gives the number of omitted words. When the shown beginning and the shown end belong to one policy, treat the omitted middle as the rest of that policy. Do not label a page partial_policy only because its middle is omitted.

## Labels

Choose exactly one label for the main content of the page.

### complete_policy

The full privacy policy or privacy notice of one organization (a company, institution, app developer or site operator) that describes its handling of personal data in general. The page must state all three of:

1. what personal data the organization collects;
2. how it uses or shares that data;
3. at least one of: the person's rights or choices, how long data is kept, or how to contact the organization about privacy.

A combined privacy-and-cookie policy counts. A policy that covers the organization's affiliates or several of its own products counts. A sector notice, such as a health provider's notice of privacy practices or a bank's privacy notice, counts when it states the three items. A policy made with a policy generator, or a default policy text supplied by a website builder or plugin (for example the suggested WordPress privacy policy), counts only when the organization's name is filled in. A page that also holds other documents (for example terms of service followed by a full privacy policy) counts. The label does not depend on the page's language, on its formatting, or on whether the policy belongs to the organization the URL suggests.

### partial_policy

Part of a privacy policy, or a policy page that does not state all three items:

- a single section or chapter of a policy (for example only the rights section or only the children's section);
- a page cut off by the crawl, so that it starts or ends in the middle of a policy and the three items are not all present;
- a summary, highlights page or short notice that points to the full policy elsewhere;
- a supplement or addendum that says it adds to a main policy (for example a notice for the residents of one state or country).

### cookie_only

A notice about cookies or similar tracking technologies only: a cookie policy, a cookie table, a cookie consent or preference page, or an advertising opt-out page. A page that also describes other handling of personal data and states all three items is complete_policy.

### other_legal

A legal page other than a privacy policy: terms of service or use, an end-user license agreement, an imprint or legal notice, a disclaimer, a copyright policy, a data processing agreement or addendum, an accessibility statement, or a legal hub page that only links to other legal documents.

### not_policy

Anything else: an article, blog post, news item or guide about privacy; a home, product or app-store page; a help article about privacy settings; a login or sign-up page; an error, page-not-found, access-denied or bot-check page; a policy template or generator page with unfilled placeholders such as [COMPANY NAME], or a generator or default policy text that never names the organization; a page whose text is unreadable; an empty or nearly empty page.

## Flags

- `multiple_orgs` (true or false): true when the page holds the separate privacy policies of two or more different organizations, for example a directory page that reproduces several companies' policies. A single policy that names its service providers, partners or affiliates is false.
- `language`: the ISO 639-1 code of the main content (`en`, `de`, `fr`, `zh`, ...), or `und` when the page has no readable text. Non-English pages receive the same labels as English pages; this flag records their language.

## Hard cases

- When a page holds several documents, choose the first label in this order that one of them meets: complete_policy, partial_policy, cookie_only, other_legal, not_policy. Set `multiple_orgs` when the policies belong to different organizations.
- Judge the main content, not menu items or links. A link to a privacy policy is not a policy.
- Quote evidence exactly as it appears on the page.

## Examples

These examples were written for this rubric.

**complete_policy**

1. "Privacy Policy of Fernhill Garden Supply Ltd. Updated 12 January 2024. We collect your name, delivery address, email address and order history, and our servers record your IP address. We use this information to deliver your orders and, if you agree, to send you offers. We share delivery details with our courier and card details with our payment processor. We keep order records for six years. To see, correct or delete your data, write to privacy@fernhill.example." All three items are present. Language `en`.
2. "Datenschutzerklärung der Brunnwald GmbH. Wenn Sie uns kontaktieren, speichern wir Ihren Namen und Ihre E-Mail-Adresse und verwenden sie nur zur Bearbeitung Ihrer Anfrage. Eine Weitergabe an Dritte erfolgt nicht. Sie haben das Recht auf Auskunft, Berichtigung und Löschung Ihrer Daten." All three items are present. Language `de`.

**partial_policy**

1. "Your Privacy Choices. You can unsubscribe from marketing emails with the link at the bottom of each email, and you can ask us to delete your account from the Settings page. For the information we collect and how we use it, see our Privacy Policy." A choices section that points to the full policy.
2. "Privacy Policy of Orbit Taxi. 1. Information we collect. When you book a ride, we collect your pickup location, your phone number and" (the text ends here). The crawl cut the policy off before it describes use, sharing, rights or contact.

**cookie_only**

1. "Cookie Notice. We use strictly necessary cookies to keep you signed in, analytics cookies to count visits, and advertising cookies set by our partners. The table below lists each cookie, its provider and how long it lasts. You can change your choices at any time under Cookie Settings."

**other_legal**

1. "Terms of Use. By using this website you agree to these terms. You may not copy its content for commercial purposes. We are not liable for indirect damages. These terms are governed by the laws of Ontario."
2. "Legal Center. Privacy Policy | Terms of Service | Cookie Policy | Imprint" with no further text: a hub page that only links to other documents.

**not_policy**

1. "Five ways to protect your privacy online. First, use a password manager. Second, turn on two-factor authentication for your email account." An article about privacy.
2. "Verifying you are human. This may take a few seconds. Enable JavaScript and cookies to continue." A bot-check page.
