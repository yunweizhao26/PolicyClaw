# Verifier against labelers

Pages in the sample: 575. Labeled by the labelers: 575. Labeled by the verifier: 575. Scored (both): 575.

## complete_policy

- Precision: 480/487 = 98.6% (95% CI 97.1 to 99.3)
- Recall: 480/490 = 98.0% (95% CI 96.3 to 98.9)
- Agreement on all five labels: 556/575 = 96.7% (95% CI 94.9 to 97.9)

## Confusion matrix

Rows: labelers. Columns: verifier.

| labelers \ verifier | complete_policy | partial_policy | cookie_only | other_legal | not_policy | total |
|---|---|---|---|---|---|---|
| complete_policy | 480 | 3 | 0 | 0 | 7 | 490 |
| partial_policy | 5 | 38 | 0 | 1 | 0 | 44 |
| cookie_only | 0 | 0 | 7 | 0 | 0 | 7 |
| other_legal | 0 | 0 | 0 | 12 | 0 | 12 |
| not_policy | 2 | 0 | 1 | 0 | 19 | 22 |
| total | 487 | 41 | 8 | 13 | 26 | 575 |

## By source

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 50 | 42 | 41 | 41 | 41/41 = 100.0% (95% CI 91.4 to 100.0) | 41/42 = 97.6% (95% CI 87.7 to 99.6) | 49/50 = 98.0% (95% CI 89.5 to 99.6) |
| gplay | 100 | 84 | 84 | 82 | 82/84 = 97.6% (95% CI 91.7 to 99.3) | 82/84 = 97.6% (95% CI 91.7 to 99.3) | 96/100 = 96.0% (95% CI 90.2 to 98.4) |
| opp115 | 25 | 24 | 24 | 24 | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 25/25 = 100.0% (95% CI 86.7 to 100.0) |
| privaseer | 400 | 340 | 338 | 333 | 333/338 = 98.5% (95% CI 96.6 to 99.4) | 333/340 = 97.9% (95% CI 95.8 to 99.0) | 386/400 = 96.5% (95% CI 94.2 to 97.9) |

## By stratum

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 50 | 42 | 41 | 41 | 41/41 = 100.0% (95% CI 91.4 to 100.0) | 41/42 = 97.6% (95% CI 87.7 to 99.6) | 49/50 = 98.0% (95% CI 89.5 to 99.6) |
| gplay | 100 | 84 | 84 | 82 | 82/84 = 97.6% (95% CI 91.7 to 99.3) | 82/84 = 97.6% (95% CI 91.7 to 99.3) | 96/100 = 96.0% (95% CI 90.2 to 98.4) |
| opp115 | 25 | 24 | 24 | 24 | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 25/25 = 100.0% (95% CI 86.7 to 100.0) |
| p_0.6_0.9 | 100 | 88 | 89 | 85 | 85/89 = 95.5% (95% CI 89.0 to 98.2) | 85/88 = 96.6% (95% CI 90.5 to 98.8) | 93/100 = 93.0% (95% CI 86.3 to 96.6) |
| p_0.9_0.99 | 100 | 95 | 93 | 92 | 92/93 = 98.9% (95% CI 94.2 to 99.8) | 92/95 = 96.8% (95% CI 91.1 to 98.9) | 95/100 = 95.0% (95% CI 88.8 to 97.8) |
| p_ge_0.99 | 100 | 100 | 100 | 100 | 100/100 = 100.0% (95% CI 96.3 to 100.0) | 100/100 = 100.0% (95% CI 96.3 to 100.0) | 100/100 = 100.0% (95% CI 96.3 to 100.0) |
| p_lt_0.6 | 100 | 57 | 56 | 56 | 56/56 = 100.0% (95% CI 93.6 to 100.0) | 56/57 = 98.2% (95% CI 90.7 to 99.7) | 98/100 = 98.0% (95% CI 93.0 to 99.4) |

## Label distribution by stratum

Each cell: labelers / verifier.

| stratum | complete_policy | partial_policy | cookie_only | other_legal | not_policy |
|---|---|---|---|---|---|
| appstore | 42 / 41 | 2 / 3 | 0 / 0 | 2 / 2 | 4 / 4 |
| gplay | 84 / 84 | 7 / 6 | 0 / 0 | 2 / 2 | 7 / 8 |
| opp115 | 24 / 24 | 1 / 1 | 0 / 0 | 0 / 0 | 0 / 0 |
| p_0.6_0.9 | 88 / 89 | 8 / 6 | 1 / 1 | 1 / 1 | 2 / 3 |
| p_0.9_0.99 | 95 / 93 | 5 / 3 | 0 / 0 | 0 / 1 | 0 / 3 |
| p_ge_0.99 | 100 / 100 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| p_lt_0.6 | 57 / 56 | 21 / 22 | 6 / 7 | 7 / 7 | 9 / 8 |

## Flags

- multiple_orgs agreement: 575/575 = 100.0% (95% CI 99.3 to 100.0); true for labelers 0, for verifier 0, for both 0
- language agreement: 575/575 = 100.0% (95% CI 99.3 to 100.0)

## Disagreements

### Verifier complete_policy, labelers not (false positives): 7

- **v407** (gplay) https://sites.google.com/view/captcha-work-online-job/home
  - labelers: partial_policy. App terms and conditions with privacy sections on collection, cookies and data storage inserted; it states collection and a privacy contact email but describes use and sharing of personal data only for cookies, so it is not a full policy.
  - verifier: complete_policy. Although embedded within Terms and Conditions, the page includes a complete privacy policy covering data collection, data usage, and contact information.
- **v457** (gplay) http://cms.appbuild.io/cms/docs/legal/privacy.php?appcode=thisapp
  - labelers: not_policy. A generator template rendered for the placeholder app code "thisapp": the organization name is the unfilled default "This App", so no organization is identified even though the template text covers collection, use and data removal.
  - verifier: complete_policy. The page is a complete privacy policy that outlines personal data collection, how data is used and shared, and how users can request data removal.
- **v028** (p_0.6_0.9) https://template2.shoppkg.com/PrivacyPolicy.aspx
  - labelers: not_policy. A template store page whose organization name is the placeholder "Sample Company", so it is an unfilled policy template even though the text describes collection, use and an unsubscribe choice.
  - verifier: complete_policy. The page states what personal data is collected, how it is used for orders and promotions, and how users can exercise their choice to unsubscribe.
- **v168** (p_0.6_0.9) http://www.clearcutaccounts.co.uk/privacy-policy/
  - labelers: partial_policy. A short website privacy notice built from the WordPress default with several empty sections; it covers comment data, sharing, retention and a contact email but says the full GDPR policy is available elsewhere on request.
  - verifier: complete_policy. The page is a complete privacy policy covering data collection (name, email in cookies/comments), sharing policies, data retention, and contact details for the data controller.
- **v301** (p_0.6_0.9) https://startuppilot.global/p/privacy
  - labelers: partial_policy. A short school policy that states collection and use, but it gives no rights, retention period or privacy contact; its only choice is declining to supply information. Item 3 is therefore missing.
  - verifier: complete_policy. The page is a complete privacy policy for the School/StartupPilot Program. It describes the personal data collected, how that data is used, and users' choices regarding anonymous visits and refusing to supply information.
- **v485** (p_0.6_0.9) https://globalcyberinstitute.org/privacy-policy
  - labelers: partial_policy. The shown beginning is terms of service, and the shown end holds only the closing changes section of a privacy policy whose start is omitted. The shown policy text does not state what data is collected, how it is used or shared, or rights, retention or contact.
  - verifier: complete_policy. The page includes both the Terms of Service and the complete Privacy Policy (based on the standard Automattic legal template), covering personal data collection, use/sharing, and policy change notifications.
- **v478** (p_0.9_0.99) https://www.carnewshere.com/privacy-policy/
  - labelers: partial_policy. A short policy page that states collection and use or sharing, but it lacks the third item: no rights, no retention, and the Contact Us heading has no contact details. The only choice mentioned is refusing cookies in the browser.
  - verifier: complete_policy. The page is a complete privacy policy stating what personal information is collected (name, log data), how it is used and shared with service providers, and user choices regarding cookies.

### Labelers complete_policy, verifier not (false negatives): 10

- **v565** (appstore) http://newpub.co/privacy.html
  - labelers: complete_policy. A short full policy of NewPubCo that states collection, international transfer and interest-based advertising use, access and deletion rights, and contact details. Its statement of use is brief.
  - verifier: partial_policy. The page states what personal data is collected, user rights and choices, and contact information, but it does not state how the organization uses or shares that data.
- **v167** (gplay) https://oldview.com/app-privacy-policy/
  - labelers: complete_policy. The published policy of the OldView app with service-specific details: it states the data collected, uses and disclosures, and retention, rights and privacy@oldview.com. The legal entity name and address remain unfilled placeholders, but the service and contact are named.
  - verifier: not_policy. The document is a privacy policy template with unfilled placeholders (e.g., '[Your Company Name/Legal Entity Name]'), which falls under not_policy per the rubric.
- **v316** (gplay) https://www.powerbiblechurch.org/privacy-policy/
  - labelers: complete_policy. A generator-based policy on the church site that states collection (email), use and third-party disclosure, and choices for cookies, ad opt-out and unsubscribing. The page ends before the contact details and never names the organization in the text.
  - verifier: not_policy. The page is an uncompleted privacy policy generator template with missing fields, empty placeholders, and no organization name specified.
- **v302** (p_0.6_0.9) https://www.corchoproyectadosuromira.com/en/privacy-policy/
  - labelers: complete_policy. A GDPR notice of one named controller: it states the data provided through its forms, the purposes and sharing with group companies, the retention period, the rights, and the contact address.
  - verifier: partial_policy. The privacy policy describes purposes of use, sharing, retention, and user rights, but it does not specify what categories of personal data the organization collects.
- **v424** (p_0.6_0.9) https://rewindtv.cl/privacy-policy-2/
  - labelers: complete_policy. The default WordPress privacy policy published on the site, with some sections left empty and no contact details. It still states collection (comment data, IP address), sharing (Gravatar, spam detection service), retention, and export and erasure rights.
  - verifier: not_policy. This is a default WordPress policy template with unfilled sections and no organization name provided, which classifies it as not_policy under the rubric.
- **v533** (p_0.6_0.9) http://www.garsidelaycock.com/privacy-policy/
  - labelers: complete_policy. The site's policy, in the WordPress default wording with several empty headings and no organization name in the text, states collection (comment data, IP address), use and sharing (spam detection, Gravatar), retention and export or erasure rights.
  - verifier: not_policy. The page contains the default WordPress privacy policy template published with empty sections and without the organization's name filled in, making it an unfilled policy template.
- **v203** (p_0.9_0.99) https://www.petiteparfait.ca/privacy-policy-2/
  - labelers: complete_policy. The site's privacy page uses the standard WordPress policy text without an organization name, and several headings are empty. It still states collection, use and sharing (spam detection, Gravatar), retention and erasure rights.
  - verifier: not_policy. This is an uncustomized default WordPress privacy policy template with empty placeholder headings and no organization name filled in, classifying it as not_policy.
- **v346** (p_0.9_0.99) https://itsmoked.com/privacy-policy/
  - labelers: complete_policy. The site's stock WordPress privacy policy, with no operator name and several empty headings: it states collection of comment data and IP addresses, sharing with Gravatar and a spam service, retention and rights to export or erase data.
  - verifier: not_policy. This is an uncustomized WordPress policy template published with empty placeholder sections and without the organization's name filled in, which falls under not_policy.
- **v412** (p_0.9_0.99) https://www.gessy-verne.com/privacy-policy
  - labelers: complete_policy. A generator-made policy deployed as the site's policy, with the generic name "This Website" and no bracketed placeholders. It states the log data collected, its use and sharing with advertising partners, and cookie choices and contact for children's data.
  - verifier: not_policy. The page contains boilerplate generated from a privacy policy template where the organization's name was never filled in, using generic placeholders like 'This Website' and 'www.website.com'. Under the rubric, a policy from a generator only counts as a complete policy when the organization's name is filled in.
- **v548** (p_lt_0.6) https://main.dev.renxdashboard.ca.nmsrv.com/privacy-policy/
  - labelers: complete_policy. A short privacy policy of RENX: it identifies the data it holds only as subscribers' contact details and email addresses, states when that data is shared, and gives deletion on request and newsletter cancellation.
  - verifier: partial_policy. The page states how user information is shared and covers deletion rights and contact details, but it lacks a description of what personal data the organization collects.

### Other disagreements: 2

- **v379** (p_0.9_0.99) https://www.perfectlyyou.com.au/termsprivacy
  - labelers: partial_policy. The shown text is website terms of use and a disclaimer containing a short privacy section that points to a separate Privacy Policy. That section states use, limited disclosure and the right to change details, but not what personal data is collected.
  - verifier: other_legal. The visible content consists of terms and conditions of use and a website disclaimer. It does not contain a full privacy policy, and its privacy section points to a separate privacy policy.
- **v133** (p_lt_0.6) https://gotgame.com/tag/privacy/
  - labelers: not_policy. A site tag archive page whose extracted text holds only site headings and a cookie consent banner. The page is not itself a policy.
  - verifier: cookie_only. The page consists solely of a cookie consent overview and preference settings detailing necessary and non-necessary cookies.

