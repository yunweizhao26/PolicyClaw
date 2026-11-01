# Verifier against labelers

Pages in the sample: 575. Labeled by the labelers: 575. Labeled by the verifier: 575. Scored (both): 575.

## complete_policy

- Precision: 483/502 = 96.2% (95% CI 94.2 to 97.6)
- Recall: 483/486 = 99.4% (95% CI 98.2 to 99.8)
- Agreement on all five labels: 550/575 = 95.7% (95% CI 93.7 to 97.0)

## Confusion matrix

Rows: labelers. Columns: verifier.

| labelers \ verifier | complete_policy | partial_policy | cookie_only | other_legal | not_policy | total |
|---|---|---|---|---|---|---|
| complete_policy | 483 | 3 | 0 | 0 | 0 | 486 |
| partial_policy | 9 | 30 | 0 | 2 | 0 | 41 |
| cookie_only | 0 | 0 | 7 | 0 | 0 | 7 |
| other_legal | 0 | 0 | 0 | 12 | 0 | 12 |
| not_policy | 10 | 0 | 1 | 0 | 18 | 29 |
| total | 502 | 33 | 8 | 14 | 18 | 575 |

## By source

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 50 | 42 | 42 | 42 | 42/42 = 100.0% (95% CI 91.6 to 100.0) | 42/42 = 100.0% (95% CI 91.6 to 100.0) | 50/50 = 100.0% (95% CI 92.9 to 100.0) |
| gplay | 100 | 83 | 88 | 83 | 83/88 = 94.3% (95% CI 87.4 to 97.5) | 83/83 = 100.0% (95% CI 95.6 to 100.0) | 95/100 = 95.0% (95% CI 88.8 to 97.8) |
| opp115 | 25 | 24 | 24 | 24 | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 25/25 = 100.0% (95% CI 86.7 to 100.0) |
| privaseer | 400 | 337 | 348 | 334 | 334/348 = 96.0% (95% CI 93.4 to 97.6) | 334/337 = 99.1% (95% CI 97.4 to 99.7) | 380/400 = 95.0% (95% CI 92.4 to 96.7) |

## By stratum

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 50 | 42 | 42 | 42 | 42/42 = 100.0% (95% CI 91.6 to 100.0) | 42/42 = 100.0% (95% CI 91.6 to 100.0) | 50/50 = 100.0% (95% CI 92.9 to 100.0) |
| gplay | 100 | 83 | 88 | 83 | 83/88 = 94.3% (95% CI 87.4 to 97.5) | 83/83 = 100.0% (95% CI 95.6 to 100.0) | 95/100 = 95.0% (95% CI 88.8 to 97.8) |
| opp115 | 25 | 24 | 24 | 24 | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 25/25 = 100.0% (95% CI 86.7 to 100.0) |
| p_0.6_0.9 | 100 | 86 | 93 | 85 | 85/93 = 91.4% (95% CI 83.9 to 95.6) | 85/86 = 98.8% (95% CI 93.7 to 99.8) | 90/100 = 90.0% (95% CI 82.6 to 94.5) |
| p_0.9_0.99 | 100 | 93 | 96 | 92 | 92/96 = 95.8% (95% CI 89.8 to 98.4) | 92/93 = 98.9% (95% CI 94.2 to 99.8) | 94/100 = 94.0% (95% CI 87.5 to 97.2) |
| p_ge_0.99 | 100 | 100 | 99 | 99 | 99/99 = 100.0% (95% CI 96.3 to 100.0) | 99/100 = 99.0% (95% CI 94.6 to 99.8) | 99/100 = 99.0% (95% CI 94.6 to 99.8) |
| p_lt_0.6 | 100 | 58 | 60 | 58 | 58/60 = 96.7% (95% CI 88.6 to 99.1) | 58/58 = 100.0% (95% CI 93.8 to 100.0) | 97/100 = 97.0% (95% CI 91.5 to 99.0) |

## Label distribution by stratum

Each cell: labelers / verifier.

| stratum | complete_policy | partial_policy | cookie_only | other_legal | not_policy |
|---|---|---|---|---|---|
| appstore | 42 / 42 | 2 / 2 | 0 / 0 | 2 / 2 | 4 / 4 |
| gplay | 83 / 88 | 6 / 5 | 0 / 0 | 2 / 2 | 9 / 5 |
| opp115 | 24 / 24 | 1 / 1 | 0 / 0 | 0 / 0 | 0 / 0 |
| p_0.6_0.9 | 86 / 93 | 8 / 3 | 1 / 1 | 1 / 2 | 4 / 1 |
| p_0.9_0.99 | 93 / 96 | 4 / 3 | 0 / 0 | 0 / 1 | 3 / 0 |
| p_ge_0.99 | 100 / 99 | 0 / 1 | 0 / 0 | 0 / 0 | 0 / 0 |
| p_lt_0.6 | 58 / 60 | 20 / 18 | 6 / 7 | 7 / 7 | 9 / 8 |

## Flags

- multiple_orgs agreement: 575/575 = 100.0% (95% CI 99.3 to 100.0); true for labelers 0, for verifier 0, for both 0
- language agreement: 574/575 = 99.8% (95% CI 99.0 to 100.0)

## Disagreements

### Verifier complete_policy, labelers not (false positives): 19

- **v042** (gplay) https://www.fng.ae/privacy-policy/
  - labelers: partial_policy. The page states sharing limits (no disclosure outside Fujairah National Group without consent) and choices (correction, marketing opt-out via info.mkt@fng.ae), but it never states what personal data the organization collects. A policy page that lacks one of the three items is partial_policy.
  - verifier: complete_policy. The privacy policy covers information collected, how it is used/shared, and provides user rights (correction, deletion, opt-out) along with contact information.
- **v167** (gplay) https://oldview.com/app-privacy-policy/
  - labelers: not_policy. The text states collection (names, emails, dates of birth, location, IP addresses), use and disclosure, and retention, rights and privacy@oldview.com, but the organization (Provider) is the unfilled placeholder "[Your Company Name/Legal Entity Name]", with further placeholders for company, address and ABN. Under the generator rule the policy counts only when the organization's name is filled in, and a policy template with unfilled placeholders is not_policy.
  - verifier: complete_policy. The page contains a complete privacy policy covering data collection, usage and sharing, and user rights, data retention, and contact details. Although it includes unfilled template placeholders in the definitions section, it clearly identifies the app and services (OldView) with a dedicated contact email.
- **v316** (gplay) https://www.powerbiblechurch.org/privacy-policy/
  - labelers: not_policy. The generator text states collection (email address and other details at registration), use and disclosure (personalization, hosting partners, Google AdSense) and choices (disable cookies, ad opt-outs), but it never names the organization and leaves fields unfilled, such as the email purposes, the unsubscribe method and the contact information. Under the generator rule an unnamed generator policy does not count, and a generator page with unfilled fields is not_policy.
  - verifier: complete_policy. The page is cut off or generated without the contact details ('using the information below' followed by nothing), but it satisfies partial_policy or complete_policy requirements. Notably, it describes data collection, uses/sharing, and user choices (cookie settings, email unsubscribe), making it a complete policy despite the missing contact details footer.
- **v414** (gplay) https://www.iscool.gr/category/apps/policy
  - labelers: not_policy. The Greek letters are missing, so only punctuation, numbers, the name FILIA LAB S.A., a few technical terms and an email address remain, and no statement of collection, use or sharing, or rights is readable. The rubric labels a page whose text is unreadable not_policy.
  - verifier: complete_policy. The page contains a complete privacy policy in Greek by FILIA LAB S.A., detailing data collection, processing purposes/uses, and contact information.
- **v457** (gplay) http://cms.appbuild.io/cms/docs/legal/privacy.php?appcode=thisapp
  - labelers: not_policy. The builder text states collection (name, email, phone, location), use and legal disclosure, and data removal by emailing support, but it was rendered for app code "thisapp" and names the organization only as the default "This App". Under the generator rule an unfilled organization name does not count, so the page is an unfilled template and not_policy.
  - verifier: complete_policy. The page contains a complete privacy policy detailing collected data (name, email, phone, location), how it is used/disclosed, and rights/contact for removal.
- **v028** (p_0.6_0.9) https://template2.shoppkg.com/PrivacyPolicy.aspx
  - labelers: not_policy. The text states collection (IP address, name, address, email, payment information), use for orders and promotions, and an unsubscribe choice, but the organization is the placeholder "Sample Company" on a template demo host. The rubric's generator rule requires the organization's name to be filled in, and a template with an unfilled organization name is not_policy.
  - verifier: complete_policy. The page is a complete privacy policy that details what personal data is collected, how it is used for promotions and orders, and choices/contact options for unsubscribing.
- **v168** (p_0.6_0.9) http://www.clearcutaccounts.co.uk/privacy-policy/
  - labelers: partial_policy. The WordPress default text states collection only through comment and login cookies and comment metadata (the Contact forms and Analytics headings are empty), sharing only with permission, comment retention and the contact info@clearcutaccounts.com, but it never names the organization. The page also says the full GDPR policy is available on request, so it is a short notice that points to the full policy elsewhere: partial_policy.
  - verifier: complete_policy. The page is a complete privacy policy outlining the data collected (via comments/cookies), data sharing practices, retention periods, and contact details for the data controller.
- **v200** (p_0.6_0.9) https://www.antipesto.com/privacy-policy
  - labelers: partial_policy. The page starts mid-policy at the security section: it states sharing (trusted third parties, legal disclosure), cookie use and browser choices, and a Contacting Us heading without contact details, but the collection section is missing and credit card information appears only in the security description. A page cut by the crawl that lacks the collection item is partial_policy.
  - verifier: complete_policy. The page is a complete privacy policy detailing what information is collected, how it is shared or used, and how to contact the company, along with cookie choices and retention details.
- **v301** (p_0.6_0.9) https://startuppilot.global/p/privacy
  - labelers: partial_policy. The policy states collection (personal identification information, Student email addresses) and use (customer service, personalization, periodic emails), but its sharing heading is empty and it gives no rights, retention period or privacy contact; saying Students may refuse to supply information only describes voluntary provision. A policy page that lacks item 3 is partial_policy, and the builder text names only the School, so the generator rule also rules out complete_policy.
  - verifier: complete_policy. The page states what data is collected, how it is used, and user choices regarding providing personal identification information.
- **v302** (p_0.6_0.9) https://www.corchoproyectadosuromira.com/en/privacy-policy/
  - labelers: partial_policy. The GDPR notice of the named controller states use (handling information requests, commercial offers, profiling), sharing (only group companies), retention (while the commercial relationship lasts) and rights with a contact address, but it never says what personal data is collected beyond information provided by interested parties. The nearby form fields do not count, so the missing collection item makes it partial_policy.
  - verifier: complete_policy. The page contains a complete privacy policy that addresses data collection, purpose and sharing, retention, user rights, and contact details for the data controller.
- **v424** (p_0.6_0.9) https://rewindtv.cl/privacy-policy-2/
  - labelers: not_policy. The default WordPress policy states collection (comment data, IP address), sharing (Gravatar, spam detection), retention and export and erasure rights, but the "Who we are" section is empty and no organization name is filled in. A builder default text counts as a generator policy, and without the organization's name it is an unfilled template, so not_policy.
  - verifier: complete_policy. The page is a complete privacy policy generated from a standard WordPress template. It specifies what personal data is collected, how it is used/shared, data retention periods, and user rights.
- **v485** (p_0.6_0.9) https://globalcyberinstitute.org/privacy-policy
  - labelers: partial_policy. The shown beginning is terms of service and the shown end is only the closing changes paragraph of a privacy policy plus a footer and cookie banner, so the two shown parts are not one policy and the omitted middle cannot be assumed to complete it. The shown policy text states no collected data, no use or sharing, and no rights, retention or contact, so the policy fragment makes the page partial_policy.
  - verifier: complete_policy. The page includes both Terms of Service and Privacy Policy text (which continues towards the end), establishing a complete privacy policy alongside terms.
- **v533** (p_0.6_0.9) http://www.garsidelaycock.com/privacy-policy/
  - labelers: not_policy. The page states collection (comment form data, IP address, user agent), use and sharing (spam detection, Gravatar hash) and rights and retention (export, erasure, indefinite comment retention), but it is the default WordPress policy text with empty sections and no organization name filled in. Under the generator rule it cannot count as a policy, so it is an unfilled template and therefore not_policy.
  - verifier: complete_policy. The page is a complete privacy policy that details what personal data is collected, how it is used/shared, data retention periods, and user data rights.
- **v203** (p_0.9_0.99) https://www.petiteparfait.ca/privacy-policy-2/
  - labelers: not_policy. The stock WordPress text states collection (comment form data, IP address, user agent), sharing (Gravatar, spam detection service) and rights and retention (export, erasure, comments kept indefinitely), but it never names the organization and leaves several headings empty. Under the generator rule a builder default counts only with the organization's name filled in, so this unfilled template is not_policy.
  - verifier: complete_policy. The page is a complete privacy policy describing what data is collected, how it is used/shared, data retention periods, and user rights.
- **v285** (p_0.9_0.99) https://labelsbase.net/privacy
  - labelers: partial_policy. LabelsBase states collection (name, phone number, postal address, log data such as IP address) and use (contacting users, service updates, improving the service), but it states no rights, choices or retention period, and the Contact Us heading ends without any contact details. A heading alone does not supply item 3, so the page is partial_policy.
  - verifier: complete_policy. The page is a complete privacy policy covering data collection, data use and sharing, and contact information.
- **v346** (p_0.9_0.99) https://itsmoked.com/privacy-policy/
  - labelers: not_policy. The stock WordPress text states collection (comment form data, IP address, user agent), sharing (Gravatar, spam detection service) and rights and retention (export, erasure, comments kept indefinitely), but it never names the organization and leaves several headings empty. Under the generator rule a builder default counts only with the organization's name filled in, so this unfilled template is not_policy.
  - verifier: complete_policy. The page is a complete privacy policy. It outlines the personal data collected, how it is used/shared, data retention periods, and user rights to access and delete data.
- **v412** (p_0.9_0.99) https://www.gessy-verne.com/privacy-policy
  - labelers: not_policy. The text states collection (log data, cookies), use and advertising sharing, and cookie choices and contact for children's data, but it is generator text whose organization is left as "This Website" and "www.website.com". Under the generator rule an unfilled name does not count, and a policy template with unfilled placeholders is not_policy.
  - verifier: complete_policy. The page serves as a complete privacy policy, detailing the data collected (such as IP addresses and cookies), the purposes and third-party uses, and instructions/options for contact and data removal regarding children.
- **v222** (p_lt_0.6) https://www.dreambodyweightloss.com/privacy-policy/
  - labelers: partial_policy. The page states use and sharing (information used for research only, not disclosed to third parties) and a cookie choice (delete cookies in browser settings), but it never says what personal data is collected, only that identifying information is not saved. A policy page that lacks the collection item is partial_policy.
  - verifier: complete_policy. The page addresses what personal data is collected, how it is used/shared, and outlines choices regarding cookie deletion, satisfying all three required elements for a complete policy.
- **v498** (p_lt_0.6) https://salmo.ee/en/content/1-privacy
  - labelers: partial_policy. The Zumzum OÜ fragment lists data sources without a collection statement and states use (website activities, invoicing, accounting) and sharing (couriers, authorities), but states no rights, retention period or privacy contact. The phone number belongs to the shop footer, so the policy lacks the third item and is partial_policy.
  - verifier: complete_policy. The page serves as a privacy policy detailing data collection, use and sharing with third parties/authorities, and provides a contact phone number.

### Labelers complete_policy, verifier not (false negatives): 3

- **v340** (p_0.6_0.9) https://campus.study/privacy-policy
  - labelers: complete_policy. The CAMPUS app policy states collection (name, age, email, location, phone, password, transaction data), use and sharing (payment data shared with payment processors, service alerts by email and phone, public forum posts) and a choice to disable cookies in browser settings. A choice satisfies item 3 even without rights, retention or contact details, and the terms content on the same page does not change the label, so it is complete_policy.
  - verifier: partial_policy. The policy describes what data is collected and how it is used/shared, but it fails to provide any contact information, user privacy rights/choices, or data retention details.
- **v478** (p_0.9_0.99) https://www.carnewshere.com/privacy-policy/
  - labelers: complete_policy. The policy states collection (name, log data, cookies), use for providing the Service and sharing with service providers, and the person's choice to set the browser to refuse cookies, while the empty Contact Us heading does not count. The site address carnewshere.com is filled into the generator text, so all three items are present and the label is complete_policy.
  - verifier: partial_policy. The page is a partial policy because it appears truncated at the end under 'Contact Us', failing to provide contact details, user rights, or data retention schedules (outside the specific mention of deleting children's data).
- **v007** (p_ge_0.99) https://www.compackage.com/privacy-policy.asp
  - labelers: complete_policy. The page states collection (email address, phone number, usage data, cookies), use (provide and improve the Service) and sharing (service providers, Google Analytics, legal disclosure), and choices (refusing cookies in the browser, the Google Analytics opt-out add-on), so the empty Contact Us heading is not needed for the third item. A generator policy with the organization's name, COMPackage Corp., filled in counts as complete_policy.
  - verifier: partial_policy. The page states what data is collected and how it is used or disclosed, but it is cut off at the heading 'Contact Us' and lacks the third required element (rights, retention details, or contact information).

### Other disagreements: 3

- **v183** (p_0.6_0.9) https://ca-egusd-psv.edupoint.com/PXP2_Activate_Account_Privacy_Parent.aspx
  - labelers: partial_policy. The two-sentence privacy statement states only safeguards and a contact phone number, and it does not state what personal data the district collects or how it uses or shares that data; the rest of the page is a use agreement. Under the hard-case order the short privacy statement (partial_policy) ranks before the use agreement (other_legal).
  - verifier: other_legal. The page is a user agreement and terms of use with a brief privacy statement that fails to specify what personal data is collected or how it is used and shared.
- **v379** (p_0.9_0.99) https://www.perfectlyyou.com.au/termsprivacy
  - labelers: partial_policy. The shown text is website terms with a short privacy section that states use (service improvement, marketing statistics), limited disclosure (by law) and a right to change details by email, but does not state what personal data is collected. The section points to a separate Privacy Policy, so it is a short notice under partial_policy, which ranks above other_legal for a page holding both.
  - verifier: other_legal. The page consists of terms and conditions of use, disclaimers, and copyright notices. It refers users to a separate privacy policy rather than containing a privacy policy itself.
- **v133** (p_lt_0.6) https://gotgame.com/tag/privacy/
  - labelers: not_policy. The page is a /tag/privacy/ archive whose text holds only site headings, a do-not-sell link and a cookie consent banner, so the main content states no collection, no use or sharing, and no rights, retention or contact for the organization. The rubric says to judge the main content and not surrounding banners, and a tag archive page is not_policy.
  - verifier: cookie_only. The page is a cookie consent overview dialog discussing necessary and non-necessary cookies and opt-out choices, focusing exclusively on cookies and tracking technologies.

