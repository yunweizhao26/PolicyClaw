# Verifier against labelers

Pages in the sample: 500. Labeled by the labelers: 500. Labeled by the verifier: 500. Scored (both): 500.

## complete_policy

- Precision: 400/409 = 97.8% (95% CI 95.9 to 98.8)
- Recall: 400/407 = 98.3% (95% CI 96.5 to 99.2)
- Agreement on all five labels: 479/500 = 95.8% (95% CI 93.7 to 97.2)

## Confusion matrix

Rows: labelers. Columns: verifier.

| labelers \ verifier | complete_policy | partial_policy | cookie_only | other_legal | not_policy | total |
|---|---|---|---|---|---|---|
| complete_policy | 400 | 2 | 0 | 0 | 5 | 407 |
| partial_policy | 2 | 21 | 0 | 0 | 1 | 24 |
| cookie_only | 0 | 0 | 4 | 0 | 0 | 4 |
| other_legal | 0 | 2 | 0 | 9 | 1 | 12 |
| not_policy | 7 | 1 | 0 | 0 | 45 | 53 |
| total | 409 | 26 | 4 | 9 | 52 | 500 |

## By source

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 75 | 64 | 62 | 62 | 62/62 = 100.0% (95% CI 94.2 to 100.0) | 62/64 = 96.9% (95% CI 89.3 to 99.1) | 73/75 = 97.3% (95% CI 90.8 to 99.3) |
| gplay | 125 | 92 | 94 | 92 | 92/94 = 97.9% (95% CI 92.6 to 99.4) | 92/92 = 100.0% (95% CI 96.0 to 100.0) | 121/125 = 96.8% (95% CI 92.1 to 98.7) |
| privaseer | 300 | 251 | 253 | 246 | 246/253 = 97.2% (95% CI 94.4 to 98.7) | 246/251 = 98.0% (95% CI 95.4 to 99.1) | 285/300 = 95.0% (95% CI 91.9 to 96.9) |

## By stratum

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 75 | 64 | 62 | 62 | 62/62 = 100.0% (95% CI 94.2 to 100.0) | 62/64 = 96.9% (95% CI 89.3 to 99.1) | 73/75 = 97.3% (95% CI 90.8 to 99.3) |
| gplay | 125 | 92 | 94 | 92 | 92/94 = 97.9% (95% CI 92.6 to 99.4) | 92/92 = 100.0% (95% CI 96.0 to 100.0) | 121/125 = 96.8% (95% CI 92.1 to 98.7) |
| p_0.6_0.9 | 111 | 93 | 92 | 90 | 90/92 = 97.8% (95% CI 92.4 to 99.4) | 90/93 = 96.8% (95% CI 90.9 to 98.9) | 103/111 = 92.8% (95% CI 86.4 to 96.3) |
| p_0.9_0.99 | 180 | 157 | 160 | 155 | 155/160 = 96.9% (95% CI 92.9 to 98.7) | 155/157 = 98.7% (95% CI 95.5 to 99.6) | 173/180 = 96.1% (95% CI 92.2 to 98.1) |
| p_lt_0.6 | 9 | 1 | 1 | 1 | 1/1 = 100.0% (95% CI 20.7 to 100.0) | 1/1 = 100.0% (95% CI 20.7 to 100.0) | 9/9 = 100.0% (95% CI 70.1 to 100.0) |

## Label distribution by stratum

Each cell: labelers / verifier.

| stratum | complete_policy | partial_policy | cookie_only | other_legal | not_policy |
|---|---|---|---|---|---|
| appstore | 64 / 62 | 4 / 4 | 0 / 0 | 1 / 1 | 6 / 8 |
| gplay | 92 / 94 | 12 / 13 | 1 / 1 | 7 / 5 | 13 / 12 |
| p_0.6_0.9 | 93 / 92 | 5 / 6 | 0 / 0 | 3 / 2 | 10 / 11 |
| p_0.9_0.99 | 157 / 160 | 1 / 1 | 0 / 0 | 0 / 0 | 22 / 19 |
| p_lt_0.6 | 1 / 1 | 2 / 2 | 3 / 3 | 1 / 1 | 2 / 2 |

## Flags

- multiple_orgs agreement: 500/500 = 100.0% (95% CI 99.2 to 100.0); true for labelers 1, for verifier 1, for both 1
- language agreement: 499/500 = 99.8% (95% CI 98.9 to 100.0)

## Disagreements

### Verifier complete_policy, labelers not (false positives): 9

- **c390** (gplay) http://trigonom.al/privacy-policy/
  - labelers: partial_policy. The app policy of Trigonom sh.p.k. states collection and use and sharing, but it lacks user rights or choices, a retention period, and any contact address for privacy.
  - verifier: complete_policy. The page contains a complete privacy policy for Trigonom sh.p.k. It specifies what data is collected (anonymized usage data, email if provided), how data is used and shared, and how to contact the company or how data is deleted.
- **c412** (gplay) https://api.carrybox.ai/policies/partner/privacy
  - labelers: not_policy. The page text has lost its letters and shows only punctuation, numbers, table borders and a few Latin tokens such as IP and ADID/IDFA, so it is unreadable.
  - verifier: complete_policy. The page contains a full Korean privacy policy detailing the categories of personal data collected, how data is processed or shared, data retention periods, user rights, and contact information.
- **c465** (p_0.6_0.9) http://www.navjeevanjalandhar.org/privacy-policy.html
  - labelers: not_policy. A default shopping-site policy text that never names the organization (the name appears to have been replaced by "We"), so the rubric treats it as unfilled template text even though it covers collection, use, sharing and contact.
  - verifier: complete_policy. The page describes a full privacy policy covering data collection, data usage and sharing with delivery providers, user opt-out choices, and contact information for privacy questions.
- **c482** (p_0.6_0.9) https://karnatakagraminbank.com/others/privacy/
  - labelers: partial_policy. A short privacy promise of Pragathi Gramin Bank that states sharing and access to account information, but it lacks what personal data it collects, referring only to customer information in general.
  - verifier: complete_policy. This is a complete privacy policy for the bank. It outlines the data collected (information shared by customers), how it is used and shared (service delivery, marketing, legal requirements, and credit reporting), and customer rights to access and correct their account information.
- **c036** (p_0.9_0.99) http://soccer.scoresreport.com/privacy-policy/
  - labelers: not_policy. The text covers collection, use and sharing, and opt-out choices, but it is boilerplate default policy text posted as a blog entry that never names the operating organization. Its opt-out method is left blank.
  - verifier: complete_policy. The page is a complete privacy policy detailing collected personal data (registration info, email), how it is used and shared with third parties, and user choices regarding opting out of email messages and targeted advertising.
- **c091** (p_0.9_0.99) https://www.glendajames.com/privacy-policy
  - labelers: not_policy. The text states collection, use and sharing, and an opt-out and contact route, but it is generator or website-builder default text that refers only to "this website" and never names the organization, which the rubric places under not_policy.
  - verifier: complete_policy. The page is a complete privacy policy covering data collection, data usage and sharing, user opt-out choices, and contact information.
- **c118** (p_0.9_0.99) https://cheatersclub.net/help/privacy-policy/
  - labelers: not_policy. The page shows a default forum-software policy text that refers only to "our site" and never names the organization; the site name appears only in the footer. The rubric labels a default policy text that never names the organization not_policy, although it states collection, use and rights.
  - verifier: complete_policy. The page is a complete privacy policy for Cheatersclub. It clearly details what data is collected, how it is used, and users' rights along with how to contact the site.
- **c210** (p_0.9_0.99) https://www.bobbyrahaljaguar.com/privacy.htm
  - labelers: not_policy. The page holds a default dealership-website policy text that calls the operator only "our dealership" and never names the organization. It describes collection, use, sharing and opt-out, but the rubric treats default policy text that never names the organization as not_policy.
  - verifier: complete_policy. The page contains a complete privacy policy detailing collected data (such as contact information and browser data), how information is used and shared with partners or agents, and choices such as opting out.
- **c372** (p_0.9_0.99) https://www.keelerpreowned.com/privacy.htm
  - labelers: not_policy. A default dealer-website policy text that refers only to "our dealership" and never names the organization or gives contact details. It describes collection, use, sharing and opt-out, but the rubric places default policy text that never names the organization under not_policy.
  - verifier: complete_policy. The page contains a complete privacy policy for the dealership, detailing the personal data collected, how it is used and shared, and how users can opt out or contact the dealership.

### Labelers complete_policy, verifier not (false negatives): 7

- **c101** (appstore) https://startios.pages.dev/privacy
  - labelers: complete_policy. A full policy for one developer's apps: it states what usage and device data it collects, how it uses the data and shares it with analytics providers, and the user's rights to deletion and correction.
  - verifier: not_policy. The page is a generic or default app privacy policy that never names the organization or developer and provides no contact details. Under the rubric, default policy text that never names the organization is classified as not_policy.
- **c178** (appstore) https://cherrygamestudio.com/privacy-policy/
  - labelers: complete_policy. A generator-style app privacy policy of Cherry Game Studio, identified through its filled-in contact email. It states the log data collected, sharing with service providers, and a privacy contact.
  - verifier: not_policy. The page contains standard app privacy policy generator text that never names the organization responsible for the service, which falls under not_policy per the rubric.
- **c252** (p_0.6_0.9) https://www.giovannalopalco.com/privacy-policy/
  - labelers: complete_policy. A privacy policy of Giovanna Lopalco combined with terms of use: it states that personal data is collected on the website (in general terms), its purposes and recipients, retention, and the rights of access, opposition, rectification and cancellation with a contact email.
  - verifier: partial_policy. The policy describes how data is used and shared, as well as user rights, retention periods, and contact details, but it never specifies what personal data is actually collected.
- **c411** (p_0.6_0.9) https://bestcellphonemonitor.weebly.com/privacy-policy.html
  - labelers: complete_policy. The privacy policy of ILF Mobile Corp names the data it handles (mobile device data, contact and account information), how it uses and discloses contact information, and the choice to unsubscribe or opt out. Collection is stated only through these named data types, and the Credit Card Details section is empty, so this is a borderline complete policy.
  - verifier: partial_policy. The page describes how the company uses and shares personal information and provides choices and contact details, but it does not specify what personal data is collected (an empty 'Credit Card Details' header suggests missing content).
- **c461** (p_0.6_0.9) http://www.statistified.com/privacy
  - labelers: complete_policy. A generator-style policy that names its site (www.statistified.com); it states collection, use and sharing, and the user's right to change their information, though the contact details are missing.
  - verifier: not_policy. The page contains default generated policy text that never names the organization and leaves the contact section blank, which classifies as not_policy under the rubric.
- **c131** (p_0.9_0.99) https://www.dalerbruder.com/privacy/
  - labelers: complete_policy. A full website privacy policy written for this site rather than generator text: it states the contact-form, server-log and cookie data it collects, how it uses and shares the data, and how to see, correct or delete data by contacting the site.
  - verifier: not_policy. The page contains standard default website-builder policy text that never names the organization. Under the rubric, default or generator text that never names the organization is classified as not_policy.
- **c480** (p_0.9_0.99) https://revotics.com/privacy-policy?v=a284e24d5f46
  - labelers: complete_policy. A site privacy policy that states the contact and analytics data collected, its uses, a no-sale sharing statement, and a contact form for privacy questions.
  - verifier: not_policy. The page contains a generic privacy policy text that never names the organization or site operator anywhere, classifying it as not_policy per the rubric.

### Other disagreements: 5

- **c486** (gplay) https://www.smartspace.com.au/privacy
  - labelers: other_legal. Although titled Privacy Policy, the page holds Simplly's terms of use; its one data collection clause refers readers to a separate Privacy Policy.
  - verifier: partial_policy. The page contains terms of use with a brief data collection notice that explicitly directs users to read the full privacy policy elsewhere.
- **c498** (gplay) https://autopostly.com/privacy-policy.php
  - labelers: other_legal. The main content is a service agreement covering term, scope, fees and price changes; its short data clause defers to a separate privacy policy and does not state how the data is used or shared.
  - verifier: partial_policy. The page mentions collected data (email and mobile number), retention, and contact details, but it does not specify how personal data is used or shared, referencing a separate policy instead.
- **c082** (p_0.6_0.9) https://poetry-on-call.doctorjulie.org/poetry-on-call-extended-privacy-policy-and-terms-of-use/
  - labelers: other_legal. A WebsitePolicies.com generator privacy policy that names the operator only as the default "Website Operator", so it does not count as a policy, followed by a generated terms of use agreement. The terms of use make the page other_legal under the several-documents rule.
  - verifier: not_policy. The page displays generated policy text from WebsitePolicies.com that never names the organization operating the site, referring only to 'Website Operator' and omitting contact details.
- **c233** (p_0.6_0.9) https://www.midwayoptometry.com/contents/new-patients/privacy
  - labelers: not_policy. The page reproduces the standard HHS model notice of privacy practices, which covers health information, its uses and disclosures, and patient rights. The notice never names the practice and keeps the template reference to page 1, so it is default text without the organization's name.
  - verifier: partial_policy. The page is a health privacy notice that details how health information is used and shared, as well as individual rights and choices, but it lacks a description of what personal data the organization collects.
- **c393** (p_0.6_0.9) https://www.hotelesmeraldaplaya.com/privacy/
  - labelers: partial_policy. A short unnamed policy that states collection and use and sharing. It lacks the third item: it gives no rights or choices, no retention period, and no contact details beyond "please contact us".
  - verifier: not_policy. The page contains generic default or template privacy policy text that never names the organization or site operator, which classifies it as not_policy.

