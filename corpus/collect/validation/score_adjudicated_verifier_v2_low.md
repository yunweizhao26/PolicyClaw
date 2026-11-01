# Verifier against labelers

Pages in the sample: 575. Labeled by the labelers: 575. Labeled by the verifier: 575. Scored (both): 575.

## complete_policy

- Precision: 471/481 = 97.9% (95% CI 96.2 to 98.9)
- Recall: 471/486 = 96.9% (95% CI 95.0 to 98.1)
- Agreement on all five labels: 544/575 = 94.6% (95% CI 92.4 to 96.2)

## Confusion matrix

Rows: labelers. Columns: verifier.

| labelers \ verifier | complete_policy | partial_policy | cookie_only | other_legal | not_policy | total |
|---|---|---|---|---|---|---|
| complete_policy | 471 | 12 | 0 | 0 | 3 | 486 |
| partial_policy | 5 | 33 | 0 | 3 | 0 | 41 |
| cookie_only | 0 | 1 | 6 | 0 | 0 | 7 |
| other_legal | 0 | 0 | 0 | 12 | 0 | 12 |
| not_policy | 5 | 1 | 1 | 0 | 22 | 29 |
| total | 481 | 47 | 7 | 15 | 25 | 575 |

## By source

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 50 | 42 | 42 | 42 | 42/42 = 100.0% (95% CI 91.6 to 100.0) | 42/42 = 100.0% (95% CI 91.6 to 100.0) | 50/50 = 100.0% (95% CI 92.9 to 100.0) |
| gplay | 100 | 83 | 85 | 82 | 82/85 = 96.5% (95% CI 90.1 to 98.8) | 82/83 = 98.8% (95% CI 93.5 to 99.8) | 96/100 = 96.0% (95% CI 90.2 to 98.4) |
| opp115 | 25 | 24 | 24 | 24 | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 25/25 = 100.0% (95% CI 86.7 to 100.0) |
| privaseer | 400 | 337 | 330 | 323 | 323/330 = 97.9% (95% CI 95.7 to 99.0) | 323/337 = 95.8% (95% CI 93.1 to 97.5) | 373/400 = 93.2% (95% CI 90.4 to 95.3) |

## By stratum

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 50 | 42 | 42 | 42 | 42/42 = 100.0% (95% CI 91.6 to 100.0) | 42/42 = 100.0% (95% CI 91.6 to 100.0) | 50/50 = 100.0% (95% CI 92.9 to 100.0) |
| gplay | 100 | 83 | 85 | 82 | 82/85 = 96.5% (95% CI 90.1 to 98.8) | 82/83 = 98.8% (95% CI 93.5 to 99.8) | 96/100 = 96.0% (95% CI 90.2 to 98.4) |
| opp115 | 25 | 24 | 24 | 24 | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 25/25 = 100.0% (95% CI 86.7 to 100.0) |
| p_0.6_0.9 | 100 | 86 | 83 | 80 | 80/83 = 96.4% (95% CI 89.9 to 98.8) | 80/86 = 93.0% (95% CI 85.6 to 96.8) | 88/100 = 88.0% (95% CI 80.2 to 93.0) |
| p_0.9_0.99 | 100 | 93 | 91 | 89 | 89/91 = 97.8% (95% CI 92.3 to 99.4) | 89/93 = 95.7% (95% CI 89.5 to 98.3) | 93/100 = 93.0% (95% CI 86.3 to 96.6) |
| p_ge_0.99 | 100 | 100 | 99 | 99 | 99/99 = 100.0% (95% CI 96.3 to 100.0) | 99/100 = 99.0% (95% CI 94.6 to 99.8) | 99/100 = 99.0% (95% CI 94.6 to 99.8) |
| p_lt_0.6 | 100 | 58 | 57 | 55 | 55/57 = 96.5% (95% CI 88.1 to 99.0) | 55/58 = 94.8% (95% CI 85.9 to 98.2) | 93/100 = 93.0% (95% CI 86.3 to 96.6) |

## Label distribution by stratum

Each cell: labelers / verifier.

| stratum | complete_policy | partial_policy | cookie_only | other_legal | not_policy |
|---|---|---|---|---|---|
| appstore | 42 / 42 | 2 / 2 | 0 / 0 | 2 / 2 | 4 / 4 |
| gplay | 83 / 85 | 6 / 7 | 0 / 0 | 2 / 2 | 9 / 6 |
| opp115 | 24 / 24 | 1 / 1 | 0 / 0 | 0 / 0 | 0 / 0 |
| p_0.6_0.9 | 86 / 83 | 8 / 11 | 1 / 1 | 1 / 3 | 4 / 2 |
| p_0.9_0.99 | 93 / 91 | 4 / 3 | 0 / 0 | 0 / 1 | 3 / 5 |
| p_ge_0.99 | 100 / 99 | 0 / 1 | 0 / 0 | 0 / 0 | 0 / 0 |
| p_lt_0.6 | 58 / 57 | 20 / 22 | 6 / 6 | 7 / 7 | 9 / 8 |

## Flags

- multiple_orgs agreement: 575/575 = 100.0% (95% CI 99.3 to 100.0); true for labelers 0, for verifier 0, for both 0
- language agreement: 574/575 = 99.8% (95% CI 99.0 to 100.0)

## Disagreements

### Verifier complete_policy, labelers not (false positives): 10

- **v316** (gplay) https://www.powerbiblechurch.org/privacy-policy/
  - labelers: not_policy. The generator text states collection (email address and other details at registration), use and disclosure (personalization, hosting partners, Google AdSense) and choices (disable cookies, ad opt-outs), but it never names the organization and leaves fields unfilled, such as the email purposes, the unsubscribe method and the contact information. Under the generator rule an unnamed generator policy does not count, and a generator page with unfilled fields is not_policy.
  - verifier: complete_policy. The page contains a privacy policy covering collection, use/sharing, and choices, but it never names the organization responsible and cuts off before providing contact details.
- **v414** (gplay) https://www.iscool.gr/category/apps/policy
  - labelers: not_policy. The Greek letters are missing, so only punctuation, numbers, the name FILIA LAB S.A., a few technical terms and an email address remain, and no statement of collection, use or sharing, or rights is readable. The rubric labels a page whose text is unreadable not_policy.
  - verifier: complete_policy. The page contains a privacy policy for FILIA LAB S.A. Despite OCR/encoding degradation removing Greek words, it states what data is collected, usage categories, and contact information.
- **v457** (gplay) http://cms.appbuild.io/cms/docs/legal/privacy.php?appcode=thisapp
  - labelers: not_policy. The builder text states collection (name, email, phone, location), use and legal disclosure, and data removal by emailing support, but it was rendered for app code "thisapp" and names the organization only as the default "This App". Under the generator rule an unfilled organization name does not count, so the page is an unfilled template and not_policy.
  - verifier: complete_policy. The page contains a complete privacy policy that covers data collection (such as GPS location and camera access), purposes of use and sharing, and user rights regarding data removal.
- **v028** (p_0.6_0.9) https://template2.shoppkg.com/PrivacyPolicy.aspx
  - labelers: not_policy. The text states collection (IP address, name, address, email, payment information), use for orders and promotions, and an unsubscribe choice, but the organization is the placeholder "Sample Company" on a template demo host. The rubric's generator rule requires the organization's name to be filled in, and a template with an unfilled organization name is not_policy.
  - verifier: complete_policy. The page states what personal data is collected, how it is used for promotional communications, and how users can opt out/unsubscribe.
- **v168** (p_0.6_0.9) http://www.clearcutaccounts.co.uk/privacy-policy/
  - labelers: partial_policy. The WordPress default text states collection only through comment and login cookies and comment metadata (the Contact forms and Analytics headings are empty), sharing only with permission, comment retention and the contact info@clearcutaccounts.com, but it never names the organization. The page also says the full GDPR policy is available on request, so it is a short notice that points to the full policy elsewhere: partial_policy.
  - verifier: complete_policy. The page is a complete privacy policy that states what personal data is collected via comments/cookies, how data is shared, and how long it is retained alongside contact information.
- **v301** (p_0.6_0.9) https://startuppilot.global/p/privacy
  - labelers: partial_policy. The policy states collection (personal identification information, Student email addresses) and use (customer service, personalization, periodic emails), but its sharing heading is empty and it gives no rights, retention period or privacy contact; saying Students may refuse to supply information only describes voluntary provision. A policy page that lacks item 3 is partial_policy, and the builder text names only the School, so the generator rule also rules out complete_policy.
  - verifier: complete_policy. The page contains a complete privacy policy covering data collection, use/sharing, and user choices/rights.
- **v203** (p_0.9_0.99) https://www.petiteparfait.ca/privacy-policy-2/
  - labelers: not_policy. The stock WordPress text states collection (comment form data, IP address, user agent), sharing (Gravatar, spam detection service) and rights and retention (export, erasure, comments kept indefinitely), but it never names the organization and leaves several headings empty. Under the generator rule a builder default counts only with the organization's name filled in, so this unfilled template is not_policy.
  - verifier: complete_policy. This is a default WordPress privacy policy template that does not name the operating organization, but it still functions as a privacy notice describing collection, use/sharing, and retention/rights.
- **v285** (p_0.9_0.99) https://labelsbase.net/privacy
  - labelers: partial_policy. LabelsBase states collection (name, phone number, postal address, log data such as IP address) and use (contacting users, service updates, improving the service), but it states no rights, choices or retention period, and the Contact Us heading ends without any contact details. A heading alone does not supply item 3, so the page is partial_policy.
  - verifier: complete_policy. The page is a complete privacy policy for LabelsBase. It details what data is collected, how it is used/shared, and provides data retention/deletion commitments for minors as well as contact instructions.
- **v073** (p_lt_0.6) https://mobilityrentals.com.au/privacy-act-provisions/
  - labelers: partial_policy. A narrow credit-reporting disclosure notice and applicant consent: it covers only credit information given to credit reporting agencies and is not a general privacy policy, with no rights, retention or contact details.
  - verifier: complete_policy. The page represents a credit privacy notice under the Australian Privacy Act 1988, stating what credit and identity information is collected, how it is disclosed/used, and providing a contact instruction.
- **v092** (p_lt_0.6) https://www.childprotection.sa.gov.au/privacy
  - labelers: partial_policy. The statement gives collection (visit logs, contact emails) and use and disclosure, but states no rights, no retention period and no privacy contact. The text also ends at a bare "Service Providers" heading.
  - verifier: complete_policy. The page is a complete privacy statement for the Department for Child Protection website. It describes what personal information is collected, how it is used/shared, and details regarding data retention.

### Labelers complete_policy, verifier not (false negatives): 15

- **v218** (gplay) https://fairytalefables.com/assets/privacy-policy.html
  - labelers: complete_policy. The privacy notice of Fairy Software CaWa Limited for the game Fairytale Fables, cut in the middle: the shown text states collection, use and sharing and gives the registered address, and the omitted middle is treated as the rest of the same notice.
  - verifier: partial_policy. The page contains the privacy notice for Fairytale Fables (Fairy Software CaWa Limited) describing data collection and sharing, but rights, retention, or contact information are not present in the visible sections due to cutting.
- **v037** (p_0.6_0.9) https://axiscloudsync.com/axis-cloudsync-privacy-policy/
  - labelers: complete_policy. The full privacy policy of AXIS CloudSync. Its data categories are thin (payment information and cookies), but it states that collection, sharing with third parties and for legal reasons, and a retention rule. It states no user rights.
  - verifier: partial_policy. The page lacks a specific statement detailing what personal data the organization collects (it only speaks generally of 'personal information' and 'sensitive/credit information' transmitted via SSL). It describes sharing/use and data retention.
- **v107** (p_0.6_0.9) https://terminatorfitness.com/privacy/
  - labelers: complete_policy. A site privacy policy followed by blog sidebar content. It states collection (server logs, cookies), use and third-party advertising tracking, a cookie choice, and a contact route.
  - verifier: partial_policy. The page contains a general privacy policy stating collection of server/cookie data, uses/sharing, and rights/contact choices. However, it does not name the operating organization, using only generic references like 'this website'.
- **v185** (p_0.6_0.9) http://americanmovingpartners.com/privacy-policy/
  - labelers: complete_policy. A short policy of American Moving Partners that states what it collects (emails and form submissions), shares it with movers and carriers, and gives a correction right and a privacy contact; a cancellation notice follows.
  - verifier: partial_policy. The page discusses how submitted information is used and shared and provides contact/correction rights, but it fails to state what specific personal data it collects.
- **v230** (p_0.6_0.9) https://senergyconsultants.com/terms-service-privacy-policy/
  - labelers: complete_policy. Terms of service followed by the same site's privacy policy, whose start falls in the omitted middle. The shown end states sharing in a business transfer and the choice to refuse cookies; collection is not in the shown text, and the omitted middle is treated as the rest of the policy.
  - verifier: partial_policy. The page includes both Terms of Service and a Privacy Policy, but the visible portions do not state what personal data is collected or user rights, retention, or contact details (the middle is omitted and the shown sections lack these statements). Therefore, it qualifies as a partial policy based on what is visible.
- **v286** (p_0.6_0.9) https://pivotfurniture.com/privacy-policy/
  - labelers: complete_policy. A generator policy with pivotfurniture.com filled in: it states the log data collected, its use and the ad partners that receive data, and the choices to opt out of the DART cookie or disable cookies, plus a contact line.
  - verifier: partial_policy. The page is a complete privacy policy for pivotfurniture.com. It describes the data collected, how it is used, and provides contact details and choices regarding cookies.
- **v433** (p_0.6_0.9) https://www.kingsworthyprimary.co.uk/page/?title=Website+Privacy+Policy&pid=62
  - labelers: complete_policy. A school's website privacy policy that states collection through forms and traffic cookies, use and sharing, and the right of access and marketing choices.
  - verifier: partial_policy. The page lacks a clear statement identifying the organization name within the text, but more importantly, it only vaguely refers to collecting personal data via online forms without specifying what personal data is collected.
- **v343** (p_0.9_0.99) http://wickedwingsuits.com/privacy/
  - labelers: complete_policy. The full policy of Wicked Wingsuits: it states what it collects, how it uses and discloses the data, and how to opt out, request a copy or correct data by writing to the company.
  - verifier: partial_policy. The page contains a complete privacy policy for Wicked Wingsuits, detailing the information collected, how it is used and shared, and options/rights for user control along with contact information.
- **v419** (p_0.9_0.99) https://www.globalsk.com/privacy-policy/
  - labelers: complete_policy. The default WordPress privacy policy deployed on the site, with several empty headings and no organization name. It states the comment and login data collected, sharing with Gravatar and a spam detection service, retention periods, and export and erasure rights.
  - verifier: not_policy. This is a default WordPress privacy policy template that has not named the organization operating the site and includes unmodified boilerplate headers. Because the organization is not identified, it is treated as not_policy.
- **v524** (p_0.9_0.99) https://www.freakfaucet.com/privacy-policy/
  - labelers: complete_policy. A full policy of the site operator (the site name is missing from the text): it states what it collects, how it uses and shares data, and how users can correct or delete their information.
  - verifier: not_policy. The page contains a template privacy policy where the organization name was left as '(the Site)' rather than being specified, making it an unfilled policy template.
- **v558** (p_0.9_0.99) https://thebouquetresidence.com/privacy-policy/
  - labelers: complete_policy. The site's WordPress-style privacy policy with several empty headings: it states the comment and cookie data collected, its use and sending to spam detection and Gravatar, retention periods and rights to export or erase data.
  - verifier: not_policy. This is a default WordPress privacy policy template that has not been configured with the organization's name, leaving empty placeholder sections. Because it is an uncompleted template lacking an identified organization, it is labeled not_policy.
- **v013** (p_ge_0.99) http://sportsplexbc.com/privacy-policy
  - labelers: complete_policy. The policy of Langley Sportsplex states collection, use and sharing, and gives an unsubscribe choice and a contact phone number.
  - verifier: partial_policy. The page is a complete privacy policy for Langley Sportsplex. It identifies what data is collected, how it is used and shared, and provides contact information.
- **v354** (p_lt_0.6) https://wideeyes.ai/privacypolicy/
  - labelers: complete_policy. A full GDPR policy of Wide Eyes Technologies: it states collection in general terms (information contributed by persons and data from website forms), uses and recipients, retention, and rights with a contact email.
  - verifier: partial_policy. The page describes data use, retention, rights, and contact information, but it never specifically identifies what categories or types of personal data it collects.
- **v548** (p_lt_0.6) https://main.dev.renxdashboard.ca.nmsrv.com/privacy-policy/
  - labelers: complete_policy. The page states the data RENX holds (subscribers' contact details, email addresses and other contact information in its records and databases), how it shares that data (only with permission, or with investors, partners and financial institutions for validation), and a right to deletion on request via contact. All three items are stated, so it is complete_policy.
  - verifier: partial_policy. The page states how RENX shares information and provides options for deletion/contact, but it lacks a statement specifying what personal data is collected.
- **v556** (p_lt_0.6) https://www.memorylaneflowers.net/system/privacy
  - labelers: complete_policy. A brief Eflorist privacy policy shown on a florist site: it states the recipient and customer data collected, their use for delivery and recognising visits, no sharing, and the controller's contact address. It states no rights or retention, so the third item rests only on the contact address.
  - verifier: partial_policy. The page states what personal data is collected and how it is used/shared, but it lacks any mention of user rights, data retention periods, or privacy-specific contact information.

### Other disagreements: 6

- **v183** (p_0.6_0.9) https://ca-egusd-psv.edupoint.com/PXP2_Activate_Account_Privacy_Parent.aspx
  - labelers: partial_policy. The two-sentence privacy statement states only safeguards and a contact phone number, and it does not state what personal data the district collects or how it uses or shares that data; the rest of the page is a use agreement. Under the hard-case order the short privacy statement (partial_policy) ranks before the use agreement (other_legal).
  - verifier: other_legal. The page contains a terms of use agreement with a brief privacy statement, but it lacks statements explaining what personal data is collected or how it is used or shared.
- **v424** (p_0.6_0.9) https://rewindtv.cl/privacy-policy-2/
  - labelers: not_policy. The default WordPress policy states collection (comment data, IP address), sharing (Gravatar, spam detection), retention and export and erasure rights, but the "Who we are" section is empty and no organization name is filled in. A builder default text counts as a generator policy, and without the organization's name it is an unfilled template, so not_policy.
  - verifier: partial_policy. This is a default WordPress privacy policy template that never specifies the name of the organization under 'Who we are' or anywhere in the body text, rendering it incomplete.
- **v485** (p_0.6_0.9) https://globalcyberinstitute.org/privacy-policy
  - labelers: partial_policy. The shown beginning is terms of service and the shown end is only the closing changes paragraph of a privacy policy plus a footer and cookie banner, so the two shown parts are not one policy and the omitted middle cannot be assumed to complete it. The shown policy text states no collected data, no use or sharing, and no rights, retention or contact, so the policy fragment makes the page partial_policy.
  - verifier: other_legal. The page includes both Terms of Service and an apparent Privacy Policy, but the crawl displays Terms of Service at the beginning, omits the body of the policy, and only catches the introductory and closing fragments of the Privacy Policy without showing data collection, use/sharing, or rights/contact.
- **v379** (p_0.9_0.99) https://www.perfectlyyou.com.au/termsprivacy
  - labelers: partial_policy. The shown text is website terms with a short privacy section that states use (service improvement, marketing statistics), limited disclosure (by law) and a right to change details by email, but does not state what personal data is collected. The section points to a separate Privacy Policy, so it is a short notice under partial_policy, which ranks above other_legal for a page holding both.
  - verifier: other_legal. The page contains terms and conditions with a brief privacy section that refers users to a separate Privacy Policy ('Please read our separate Privacy Policy carefully') and lacks a statement detailing what personal data is collected.
- **v133** (p_lt_0.6) https://gotgame.com/tag/privacy/
  - labelers: not_policy. The page is a /tag/privacy/ archive whose text holds only site headings, a do-not-sell link and a cookie consent banner, so the main content states no collection, no use or sharing, and no rights, retention or contact for the organization. The rubric says to judge the main content and not surrounding banners, and a tag archive page is not_policy.
  - verifier: cookie_only. The page only contains a cookie consent overview and cookie categories banner/text, focusing solely on cookies and tracking technologies.
- **v243** (p_lt_0.6) https://www.gravesthomas.com/privacy-policy/
  - labelers: cookie_only. The only privacy content is one paragraph on an ad network's cookies and an advertising opt-out; the rest is law-firm marketing and a website disclaimer.
  - verifier: partial_policy. The page contains only a brief privacy/advertising notice regarding cookies and targeted advertising opt-out, but lacks any description of what personal data the organization itself collects.

