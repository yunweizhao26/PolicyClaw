# Verifier against labelers

Pages in the sample: 575. Labeled by the labelers: 575. Labeled by the verifier: 575. Scored (both): 575.

## complete_policy

- Precision: 482/487 = 99.0% (95% CI 97.6 to 99.6)
- Recall: 482/486 = 99.2% (95% CI 97.9 to 99.7)
- Agreement on all five labels: 564/575 = 98.1% (95% CI 96.6 to 98.9)

## Confusion matrix

Rows: labelers. Columns: verifier.

| labelers \ verifier | complete_policy | partial_policy | cookie_only | other_legal | not_policy | total |
|---|---|---|---|---|---|---|
| complete_policy | 482 | 4 | 0 | 0 | 0 | 486 |
| partial_policy | 3 | 37 | 0 | 1 | 0 | 41 |
| cookie_only | 0 | 0 | 7 | 0 | 0 | 7 |
| other_legal | 0 | 0 | 0 | 12 | 0 | 12 |
| not_policy | 2 | 0 | 1 | 0 | 26 | 29 |
| total | 487 | 41 | 8 | 13 | 26 | 575 |

## By source

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 50 | 42 | 41 | 41 | 41/41 = 100.0% (95% CI 91.4 to 100.0) | 41/42 = 97.6% (95% CI 87.7 to 99.6) | 49/50 = 98.0% (95% CI 89.5 to 99.6) |
| gplay | 100 | 83 | 84 | 83 | 83/84 = 98.8% (95% CI 93.6 to 99.8) | 83/83 = 100.0% (95% CI 95.6 to 100.0) | 99/100 = 99.0% (95% CI 94.6 to 99.8) |
| opp115 | 25 | 24 | 24 | 24 | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 25/25 = 100.0% (95% CI 86.7 to 100.0) |
| privaseer | 400 | 337 | 338 | 334 | 334/338 = 98.8% (95% CI 97.0 to 99.5) | 334/337 = 99.1% (95% CI 97.4 to 99.7) | 391/400 = 97.8% (95% CI 95.8 to 98.8) |

## By stratum

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 50 | 42 | 41 | 41 | 41/41 = 100.0% (95% CI 91.4 to 100.0) | 41/42 = 97.6% (95% CI 87.7 to 99.6) | 49/50 = 98.0% (95% CI 89.5 to 99.6) |
| gplay | 100 | 83 | 84 | 83 | 83/84 = 98.8% (95% CI 93.6 to 99.8) | 83/83 = 100.0% (95% CI 95.6 to 100.0) | 99/100 = 99.0% (95% CI 94.6 to 99.8) |
| opp115 | 25 | 24 | 24 | 24 | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 25/25 = 100.0% (95% CI 86.7 to 100.0) |
| p_0.6_0.9 | 100 | 86 | 89 | 85 | 85/89 = 95.5% (95% CI 89.0 to 98.2) | 85/86 = 98.8% (95% CI 93.7 to 99.8) | 95/100 = 95.0% (95% CI 88.8 to 97.8) |
| p_0.9_0.99 | 100 | 93 | 93 | 93 | 93/93 = 100.0% (95% CI 96.0 to 100.0) | 93/93 = 100.0% (95% CI 96.0 to 100.0) | 99/100 = 99.0% (95% CI 94.6 to 99.8) |
| p_ge_0.99 | 100 | 100 | 100 | 100 | 100/100 = 100.0% (95% CI 96.3 to 100.0) | 100/100 = 100.0% (95% CI 96.3 to 100.0) | 100/100 = 100.0% (95% CI 96.3 to 100.0) |
| p_lt_0.6 | 100 | 58 | 56 | 56 | 56/56 = 100.0% (95% CI 93.6 to 100.0) | 56/58 = 96.6% (95% CI 88.3 to 99.0) | 97/100 = 97.0% (95% CI 91.5 to 99.0) |

## Label distribution by stratum

Each cell: labelers / verifier.

| stratum | complete_policy | partial_policy | cookie_only | other_legal | not_policy |
|---|---|---|---|---|---|
| appstore | 42 / 41 | 2 / 3 | 0 / 0 | 2 / 2 | 4 / 4 |
| gplay | 83 / 84 | 6 / 6 | 0 / 0 | 2 / 2 | 9 / 8 |
| opp115 | 24 / 24 | 1 / 1 | 0 / 0 | 0 / 0 | 0 / 0 |
| p_0.6_0.9 | 86 / 89 | 8 / 6 | 1 / 1 | 1 / 1 | 4 / 3 |
| p_0.9_0.99 | 93 / 93 | 4 / 3 | 0 / 0 | 0 / 1 | 3 / 3 |
| p_ge_0.99 | 100 / 100 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| p_lt_0.6 | 58 / 56 | 20 / 22 | 6 / 7 | 7 / 7 | 9 / 8 |

## Flags

- multiple_orgs agreement: 575/575 = 100.0% (95% CI 99.3 to 100.0); true for labelers 0, for verifier 0, for both 0
- language agreement: 575/575 = 100.0% (95% CI 99.3 to 100.0)

## Disagreements

### Verifier complete_policy, labelers not (false positives): 5

- **v457** (gplay) http://cms.appbuild.io/cms/docs/legal/privacy.php?appcode=thisapp
  - labelers: not_policy. The builder text states collection (name, email, phone, location), use and legal disclosure, and data removal by emailing support, but it was rendered for app code "thisapp" and names the organization only as the default "This App". Under the generator rule an unfilled organization name does not count, so the page is an unfilled template and not_policy.
  - verifier: complete_policy. The page is a complete privacy policy that outlines personal data collection, how data is used and shared, and how users can request data removal.
- **v028** (p_0.6_0.9) https://template2.shoppkg.com/PrivacyPolicy.aspx
  - labelers: not_policy. The text states collection (IP address, name, address, email, payment information), use for orders and promotions, and an unsubscribe choice, but the organization is the placeholder "Sample Company" on a template demo host. The rubric's generator rule requires the organization's name to be filled in, and a template with an unfilled organization name is not_policy.
  - verifier: complete_policy. The page states what personal data is collected, how it is used for orders and promotions, and how users can exercise their choice to unsubscribe.
- **v168** (p_0.6_0.9) http://www.clearcutaccounts.co.uk/privacy-policy/
  - labelers: partial_policy. The WordPress default text states collection only through comment and login cookies and comment metadata (the Contact forms and Analytics headings are empty), sharing only with permission, comment retention and the contact info@clearcutaccounts.com, but it never names the organization. The page also says the full GDPR policy is available on request, so it is a short notice that points to the full policy elsewhere: partial_policy.
  - verifier: complete_policy. The page is a complete privacy policy covering data collection (name, email in cookies/comments), sharing policies, data retention, and contact details for the data controller.
- **v301** (p_0.6_0.9) https://startuppilot.global/p/privacy
  - labelers: partial_policy. The policy states collection (personal identification information, Student email addresses) and use (customer service, personalization, periodic emails), but its sharing heading is empty and it gives no rights, retention period or privacy contact; saying Students may refuse to supply information only describes voluntary provision. A policy page that lacks item 3 is partial_policy, and the builder text names only the School, so the generator rule also rules out complete_policy.
  - verifier: complete_policy. The page is a complete privacy policy for the School/StartupPilot Program. It describes the personal data collected, how that data is used, and users' choices regarding anonymous visits and refusing to supply information.
- **v485** (p_0.6_0.9) https://globalcyberinstitute.org/privacy-policy
  - labelers: partial_policy. The shown beginning is terms of service and the shown end is only the closing changes paragraph of a privacy policy plus a footer and cookie banner, so the two shown parts are not one policy and the omitted middle cannot be assumed to complete it. The shown policy text states no collected data, no use or sharing, and no rights, retention or contact, so the policy fragment makes the page partial_policy.
  - verifier: complete_policy. The page includes both the Terms of Service and the complete Privacy Policy (based on the standard Automattic legal template), covering personal data collection, use/sharing, and policy change notifications.

### Labelers complete_policy, verifier not (false negatives): 4

- **v565** (appstore) http://newpub.co/privacy.html
  - labelers: complete_policy. The page states collection (email, social IDs, device and advertising IDs, IP address, location, usage data), sharing through international transfer under the Data Privacy Framework or standard contractual clauses together with interest-based advertising, and rights (opt-out, copy, deletion) with contact details for NewPubCo, Inc. All three items are stated by one named organization, so it is complete_policy.
  - verifier: partial_policy. The page states what personal data is collected, user rights and choices, and contact information, but it does not state how the organization uses or shares that data.
- **v169** (p_0.6_0.9) https://wilmingtonadventures.com/privacy-policy/
  - labelers: complete_policy. The page states collection (name and email from the contact form, browsing data gathered for advertising), use and sharing (third-party advertising companies collect data for interest-based ads and retargeting), and a choice (opt-out through the DAA and NAI sites). The cookie_only rule says a page that also describes other handling of personal data and states all three items is complete_policy.
  - verifier: partial_policy. The page is an incomplete privacy notice primarily covering interest-based advertising. While it mentions collecting name and email address, it does not state how that personal data is used or shared, nor does it provide retention periods or privacy contact information.
- **v240** (p_lt_0.6) https://inverkipbandb.co.uk/data-privacy-statement/
  - labelers: complete_policy. Although the text starts mid-list, the Belle Vue B&B statement states collection (nationality, passport number and place of issue, next destination), sharing (FreeToBook holds booking data and passes card details to PayPal, no marketing sharing) and retention (guest details kept at least 12 months). The rubric makes a crawl-cut page partial only when the three items are not all present, so all three present makes it complete_policy.
  - verifier: partial_policy. The page displays only an isolated first section ('1. Tourist Accommodation Registration') of Belle Vue B&B's privacy statement before abruptly breaking into customer testimonials, making it a partial policy.
- **v548** (p_lt_0.6) https://main.dev.renxdashboard.ca.nmsrv.com/privacy-policy/
  - labelers: complete_policy. The page states the data RENX holds (subscribers' contact details, email addresses and other contact information in its records and databases), how it shares that data (only with permission, or with investors, partners and financial institutions for validation), and a right to deletion on request via contact. All three items are stated, so it is complete_policy.
  - verifier: partial_policy. The page states how user information is shared and covers deletion rights and contact details, but it lacks a description of what personal data the organization collects.

### Other disagreements: 2

- **v379** (p_0.9_0.99) https://www.perfectlyyou.com.au/termsprivacy
  - labelers: partial_policy. The shown text is website terms with a short privacy section that states use (service improvement, marketing statistics), limited disclosure (by law) and a right to change details by email, but does not state what personal data is collected. The section points to a separate Privacy Policy, so it is a short notice under partial_policy, which ranks above other_legal for a page holding both.
  - verifier: other_legal. The visible content consists of terms and conditions of use and a website disclaimer. It does not contain a full privacy policy, and its privacy section points to a separate privacy policy.
- **v133** (p_lt_0.6) https://gotgame.com/tag/privacy/
  - labelers: not_policy. The page is a /tag/privacy/ archive whose text holds only site headings, a do-not-sell link and a cookie consent banner, so the main content states no collection, no use or sharing, and no rights, retention or contact for the organization. The rubric says to judge the main content and not surrounding banners, and a tag archive page is not_policy.
  - verifier: cookie_only. The page consists solely of a cookie consent overview and preference settings detailing necessary and non-necessary cookies.

