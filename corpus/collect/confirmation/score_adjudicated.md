# Verifier against labelers

Pages in the sample: 500. Labeled by the labelers: 500. Labeled by the verifier: 500. Scored (both): 500.

## complete_policy

- Precision: 400/409 = 97.8% (95% CI 95.9 to 98.8)
- Recall: 400/403 = 99.3% (95% CI 97.8 to 99.7)
- Agreement on all five labels: 484/500 = 96.8% (95% CI 94.9 to 98.0)

## Confusion matrix

Rows: labelers. Columns: verifier.

| labelers \ verifier | complete_policy | partial_policy | cookie_only | other_legal | not_policy | total |
|---|---|---|---|---|---|---|
| complete_policy | 400 | 0 | 0 | 0 | 3 | 403 |
| partial_policy | 2 | 23 | 0 | 0 | 0 | 25 |
| cookie_only | 0 | 0 | 4 | 0 | 0 | 4 |
| other_legal | 0 | 2 | 0 | 9 | 1 | 12 |
| not_policy | 7 | 1 | 0 | 0 | 48 | 56 |
| total | 409 | 26 | 4 | 9 | 52 | 500 |

## By source

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 75 | 64 | 62 | 62 | 62/62 = 100.0% (95% CI 94.2 to 100.0) | 62/64 = 96.9% (95% CI 89.3 to 99.1) | 73/75 = 97.3% (95% CI 90.8 to 99.3) |
| gplay | 125 | 92 | 94 | 92 | 92/94 = 97.9% (95% CI 92.6 to 99.4) | 92/92 = 100.0% (95% CI 96.0 to 100.0) | 121/125 = 96.8% (95% CI 92.1 to 98.7) |
| privaseer | 300 | 247 | 253 | 246 | 246/253 = 97.2% (95% CI 94.4 to 98.7) | 246/247 = 99.6% (95% CI 97.7 to 99.9) | 290/300 = 96.7% (95% CI 94.0 to 98.2) |

## By stratum

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 75 | 64 | 62 | 62 | 62/62 = 100.0% (95% CI 94.2 to 100.0) | 62/64 = 96.9% (95% CI 89.3 to 99.1) | 73/75 = 97.3% (95% CI 90.8 to 99.3) |
| gplay | 125 | 92 | 94 | 92 | 92/94 = 97.9% (95% CI 92.6 to 99.4) | 92/92 = 100.0% (95% CI 96.0 to 100.0) | 121/125 = 96.8% (95% CI 92.1 to 98.7) |
| p_0.6_0.9 | 111 | 90 | 92 | 90 | 90/92 = 97.8% (95% CI 92.4 to 99.4) | 90/90 = 100.0% (95% CI 95.9 to 100.0) | 107/111 = 96.4% (95% CI 91.1 to 98.6) |
| p_0.9_0.99 | 180 | 156 | 160 | 155 | 155/160 = 96.9% (95% CI 92.9 to 98.7) | 155/156 = 99.4% (95% CI 96.5 to 99.9) | 174/180 = 96.7% (95% CI 92.9 to 98.5) |
| p_lt_0.6 | 9 | 1 | 1 | 1 | 1/1 = 100.0% (95% CI 20.7 to 100.0) | 1/1 = 100.0% (95% CI 20.7 to 100.0) | 9/9 = 100.0% (95% CI 70.1 to 100.0) |

## Label distribution by stratum

Each cell: labelers / verifier.

| stratum | complete_policy | partial_policy | cookie_only | other_legal | not_policy |
|---|---|---|---|---|---|
| appstore | 64 / 62 | 4 / 4 | 0 / 0 | 1 / 1 | 6 / 8 |
| gplay | 92 / 94 | 12 / 13 | 1 / 1 | 7 / 5 | 13 / 12 |
| p_0.6_0.9 | 90 / 92 | 6 / 6 | 0 / 0 | 3 / 2 | 12 / 11 |
| p_0.9_0.99 | 156 / 160 | 1 / 1 | 0 / 0 | 0 / 0 | 23 / 19 |
| p_lt_0.6 | 1 / 1 | 2 / 2 | 3 / 3 | 1 / 1 | 2 / 2 |

## Flags

- multiple_orgs agreement: 500/500 = 100.0% (95% CI 99.2 to 100.0); true for labelers 1, for verifier 1, for both 1
- language agreement: 499/500 = 99.8% (95% CI 98.9 to 100.0)

## Disagreements

### Verifier complete_policy, labelers not (false positives): 9

- **c390** (gplay) http://trigonom.al/privacy-policy/
  - labelers: partial_policy. Trigonom sh.p.k.'s app policy states collection (anonymized usage data, the e-mail address sent with feedback) and use and sharing (improving the apps, trusted third parties, no sale), but it gives no user rights or choices, no retention period and no privacy contact address. Missing the third item, it is a policy page that does not state all three items, so partial_policy.
  - verifier: complete_policy. The page contains a complete privacy policy for Trigonom sh.p.k. It specifies what data is collected (anonymized usage data, email if provided), how data is used and shared, and how to contact the company or how data is deleted.
- **c412** (gplay) https://api.carrybox.ai/policies/partner/privacy
  - labelers: not_policy. The Korean letters were lost, so only punctuation, numbers, table borders and tokens such as IP, ADID/IDFA and cs@homisoft.net remain, and no statement of collection, of use or sharing, or of rights, retention or contact can be read. A page whose text is unreadable is not_policy.
  - verifier: complete_policy. The page contains a full Korean privacy policy detailing the categories of personal data collected, how data is processed or shared, data retention periods, user rights, and contact information.
- **c465** (p_0.6_0.9) http://www.navjeevanjalandhar.org/privacy-policy.html
  - labelers: not_policy. The text states collection (name, address, phone, email, card numbers), use and sharing with the shipping company, and an email opt-out, but it is a stock shopping-site template that never names the organization ('We does not sell products for purchase by children', 'Please contact us here'). The rubric places a generator or default policy text that never names the organization under not_policy.
  - verifier: complete_policy. The page describes a full privacy policy covering data collection, data usage and sharing with delivery providers, user opt-out choices, and contact information for privacy questions.
- **c482** (p_0.6_0.9) https://karnatakagraminbank.com/others/privacy/
  - labelers: partial_policy. The bank's privacy page states use and sharing (service delivery, product information, credit reporting, disclosure when compelled by law) and a right to access and correct account information, but it never states what personal data it collects beyond 'customer information' in general. A policy page that does not state all three items is partial_policy.
  - verifier: complete_policy. This is a complete privacy policy for the bank. It outlines the data collected (information shared by customers), how it is used and shared (service delivery, marketing, legal requirements, and credit reporting), and customer rights to access and correct their account information.
- **c036** (p_0.9_0.99) http://soccer.scoresreport.com/privacy-policy/
  - labelers: not_policy. The text states collection (registration data, email addresses), use and sharing (mailings, partners, aggregate data for advertisers) and choices (email opt-out, NAI ad opt-out), but it is reused template text posted as a blog entry with an unfilled opt-out method and never names the operating organization. The rubric's rule for generator or default policy text that never names the organization makes it not_policy.
  - verifier: complete_policy. The page is a complete privacy policy detailing collected personal data (registration info, email), how it is used and shared with third parties, and user choices regarding opting out of email messages and targeted advertising.
- **c091** (p_0.9_0.99) https://www.glendajames.com/privacy-policy
  - labelers: not_policy. The text states collection (name, email, address, phone, property details), use and limited sharing, and an unsubscribe choice with an email contact link, but it is real-estate website-builder default text that refers only to 'this website' and never names the agent or brokerage. Default policy text that never names the organization is not_policy.
  - verifier: complete_policy. The page is a complete privacy policy covering data collection, data usage and sharing, user opt-out choices, and contact information.
- **c118** (p_0.9_0.99) https://cheatersclub.net/help/privacy-policy/
  - labelers: not_policy. The text states collection (name or username, IP address, profile fields), use (membership, activity emails, analytics) and rights to access, correction and erasure by contacting the site, but it is forum-software default policy text that refers only to 'our site', and 'Cheatersclub' appears only in the footer. Default policy text that never names the organization is not_policy.
  - verifier: complete_policy. The page is a complete privacy policy for Cheatersclub. It clearly details what data is collected, how it is used, and users' rights along with how to contact the site.
- **c210** (p_0.9_0.99) https://www.bobbyrahaljaguar.com/privacy.htm
  - labelers: not_policy. The text states collection (browser type, IP address, name, email), use and sharing (partners, agents, business transfers) and an opt-out choice, but it is dealer-website default text that calls the operator only 'our dealership', and its contact section gives no details. Default policy text that never names the organization is not_policy.
  - verifier: complete_policy. The page contains a complete privacy policy detailing collected data (such as contact information and browser data), how information is used and shared with partners or agents, and choices such as opting out.
- **c372** (p_0.9_0.99) https://www.keelerpreowned.com/privacy.htm
  - labelers: not_policy. The text states collection (browser, IP address, name, e-mail), use and sharing with partners and agents, and opt-out choices, but it is default dealer-website text that refers only to 'our dealership' and ends with 'you may contact us' without any details, so the organization is never named. Under the rule for website-builder default text, an unnamed default policy is not_policy.
  - verifier: complete_policy. The page contains a complete privacy policy for the dealership, detailing the personal data collected, how it is used and shared, and how users can opt out or contact the dealership.

### Labelers complete_policy, verifier not (false negatives): 3

- **c101** (appstore) https://startios.pages.dev/privacy
  - labelers: complete_policy. The page states collection (usage data, device information), use (performance, bug fixing) and sharing with analytics providers, and rights to deletion and correction. Nothing on the page marks it as generator or website-builder default text, so the naming rule does not apply and the three items make it complete_policy.
  - verifier: not_policy. The page is a generic or default app privacy policy that never names the organization or developer and provides no contact details. Under the rubric, default policy text that never names the organization is classified as not_policy.
- **c178** (appstore) https://cherrygamestudio.com/privacy-policy/
  - labelers: complete_policy. This app privacy policy generator text identifies the organization through the contact email support@cherrygamestudio.com at its own domain. It states collection (log data such as IP address, device name and OS version), sharing with service providers, and a privacy contact, so the generator rule is met and the label is complete_policy.
  - verifier: not_policy. The page contains standard app privacy policy generator text that never names the organization responsible for the service, which falls under not_policy per the rubric.
- **c480** (p_0.9_0.99) https://revotics.com/privacy-policy?v=a284e24d5f46
  - labelers: complete_policy. The policy states collection (Google Analytics web log data; name, address, phone, email), use (services, transactions, marketing) and sharing (no sale or rental), and a contact form for privacy questions. It never names the operator, but its site-specific edits (Google Analytics, Stripe or PayPal checkout, 'Financial information – None') show a customized policy rather than unfilled generator text, so with all three items it is complete_policy.
  - verifier: not_policy. The page contains a generic privacy policy text that never names the organization or site operator anywhere, classifying it as not_policy per the rubric.

### Other disagreements: 4

- **c486** (gplay) https://www.smartspace.com.au/privacy
  - labelers: other_legal. The main content is Simplly's terms of use (liability, licensing, payments, support); its one data clause states collection of email addresses, use for support and promotions, an unsubscribe choice and a support email, but it sends readers to a separate Privacy Policy for data collection. The page is a terms-of-use document whose data clause is not the organization's privacy policy, so it is other_legal.
  - verifier: partial_policy. The page contains terms of use with a brief data collection notice that explicitly directs users to read the full privacy policy elsewhere.
- **c498** (gplay) https://autopostly.com/privacy-policy.php
  - labelers: other_legal. The page is a service agreement (term, scope, fees, price changes) whose data clauses state collection of email and mobile number, deletion on account deactivation and a contact line, but they never state how the data is used or shared and defer to a separate Company privacy policy. An agreement whose main content is service terms is other_legal.
  - verifier: partial_policy. The page mentions collected data (email and mobile number), retention, and contact details, but it does not specify how personal data is used or shared, referencing a separate policy instead.
- **c082** (p_0.6_0.9) https://poetry-on-call.doctorjulie.org/poetry-on-call-extended-privacy-policy-and-terms-of-use/
  - labelers: other_legal. The privacy part states collection (form data, IP address, browser data), use and user rights, but it is WebsitePolicies.com generator text that names the operator only as the default 'Website Operator' and leaves the contact section empty, so it does not count as a policy. The page then holds a generated terms of use agreement, and the several-documents rule selects other_legal.
  - verifier: not_policy. The page displays generated policy text from WebsitePolicies.com that never names the organization operating the site, referring only to 'Website Operator' and omitting contact details.
- **c233** (p_0.6_0.9) https://www.midwayoptometry.com/contents/new-patients/privacy
  - labelers: not_policy. The HHS model notice of privacy practices states the health information and medical records held, their uses and disclosures, and patient rights, but it never names the practice and points to contact details 'on page 1' that the page does not show. The practice's phone and address appear only in the site's location footer, so this template text without the organization's name is not_policy.
  - verifier: partial_policy. The page is a health privacy notice that details how health information is used and shared, as well as individual rights and choices, but it lacks a description of what personal data the organization collects.

