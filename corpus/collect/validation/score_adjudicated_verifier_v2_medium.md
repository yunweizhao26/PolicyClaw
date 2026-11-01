# Verifier against labelers

Pages in the sample: 575. Labeled by the labelers: 575. Labeled by the verifier: 575. Scored (both): 575.

## complete_policy

- Precision: 462/470 = 98.3% (95% CI 96.7 to 99.1)
- Recall: 462/486 = 95.1% (95% CI 92.8 to 96.7)
- Agreement on all five labels: 540/575 = 93.9% (95% CI 91.7 to 95.6)

## Confusion matrix

Rows: labelers. Columns: verifier.

| labelers \ verifier | complete_policy | partial_policy | cookie_only | other_legal | not_policy | total |
|---|---|---|---|---|---|---|
| complete_policy | 462 | 23 | 0 | 0 | 1 | 486 |
| partial_policy | 6 | 33 | 0 | 2 | 0 | 41 |
| cookie_only | 0 | 0 | 7 | 0 | 0 | 7 |
| other_legal | 0 | 0 | 0 | 12 | 0 | 12 |
| not_policy | 2 | 0 | 1 | 0 | 26 | 29 |
| total | 470 | 56 | 8 | 14 | 27 | 575 |

## By source

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 50 | 42 | 40 | 40 | 40/40 = 100.0% (95% CI 91.2 to 100.0) | 40/42 = 95.2% (95% CI 84.2 to 98.7) | 48/50 = 96.0% (95% CI 86.5 to 98.9) |
| gplay | 100 | 83 | 81 | 80 | 80/81 = 98.8% (95% CI 93.3 to 99.8) | 80/83 = 96.4% (95% CI 89.9 to 98.8) | 96/100 = 96.0% (95% CI 90.2 to 98.4) |
| opp115 | 25 | 24 | 24 | 24 | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 25/25 = 100.0% (95% CI 86.7 to 100.0) |
| privaseer | 400 | 337 | 325 | 318 | 318/325 = 97.8% (95% CI 95.6 to 99.0) | 318/337 = 94.4% (95% CI 91.4 to 96.4) | 371/400 = 92.8% (95% CI 89.8 to 94.9) |

## By stratum

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 50 | 42 | 40 | 40 | 40/40 = 100.0% (95% CI 91.2 to 100.0) | 40/42 = 95.2% (95% CI 84.2 to 98.7) | 48/50 = 96.0% (95% CI 86.5 to 98.9) |
| gplay | 100 | 83 | 81 | 80 | 80/81 = 98.8% (95% CI 93.3 to 99.8) | 80/83 = 96.4% (95% CI 89.9 to 98.8) | 96/100 = 96.0% (95% CI 90.2 to 98.4) |
| opp115 | 25 | 24 | 24 | 24 | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 25/25 = 100.0% (95% CI 86.7 to 100.0) |
| p_0.6_0.9 | 100 | 86 | 85 | 82 | 82/85 = 96.5% (95% CI 90.1 to 98.8) | 82/86 = 95.3% (95% CI 88.6 to 98.2) | 92/100 = 92.0% (95% CI 85.0 to 95.9) |
| p_0.9_0.99 | 100 | 93 | 93 | 91 | 91/93 = 97.8% (95% CI 92.5 to 99.4) | 91/93 = 97.8% (95% CI 92.5 to 99.4) | 95/100 = 95.0% (95% CI 88.8 to 97.8) |
| p_ge_0.99 | 100 | 100 | 99 | 99 | 99/99 = 100.0% (95% CI 96.3 to 100.0) | 99/100 = 99.0% (95% CI 94.6 to 99.8) | 99/100 = 99.0% (95% CI 94.6 to 99.8) |
| p_lt_0.6 | 100 | 58 | 48 | 46 | 46/48 = 95.8% (95% CI 86.0 to 98.8) | 46/58 = 79.3% (95% CI 67.2 to 87.7) | 85/100 = 85.0% (95% CI 76.7 to 90.7) |

## Label distribution by stratum

Each cell: labelers / verifier.

| stratum | complete_policy | partial_policy | cookie_only | other_legal | not_policy |
|---|---|---|---|---|---|
| appstore | 42 / 40 | 2 / 4 | 0 / 0 | 2 / 2 | 4 / 4 |
| gplay | 83 / 81 | 6 / 9 | 0 / 0 | 2 / 2 | 9 / 8 |
| opp115 | 24 / 24 | 1 / 1 | 0 / 0 | 0 / 0 | 0 / 0 |
| p_0.6_0.9 | 86 / 85 | 8 / 8 | 1 / 1 | 1 / 2 | 4 / 4 |
| p_0.9_0.99 | 93 / 93 | 4 / 3 | 0 / 0 | 0 / 1 | 3 / 3 |
| p_ge_0.99 | 100 / 99 | 0 / 1 | 0 / 0 | 0 / 0 | 0 / 0 |
| p_lt_0.6 | 58 / 48 | 20 / 30 | 6 / 7 | 7 / 7 | 9 / 8 |

## Flags

- multiple_orgs agreement: 575/575 = 100.0% (95% CI 99.3 to 100.0); true for labelers 0, for verifier 0, for both 0
- language agreement: 575/575 = 100.0% (95% CI 99.3 to 100.0)

## Disagreements

### Verifier complete_policy, labelers not (false positives): 8

- **v457** (gplay) http://cms.appbuild.io/cms/docs/legal/privacy.php?appcode=thisapp
  - labelers: not_policy. The builder text states collection (name, email, phone, location), use and legal disclosure, and data removal by emailing support, but it was rendered for app code "thisapp" and names the organization only as the default "This App". Under the generator rule an unfilled organization name does not count, so the page is an unfilled template and not_policy.
  - verifier: complete_policy. The page is a complete privacy policy that identifies the organization (This App) and specifies the data collected, how it is used and shared, and the user's right to request data removal.
- **v168** (p_0.6_0.9) http://www.clearcutaccounts.co.uk/privacy-policy/
  - labelers: partial_policy. The WordPress default text states collection only through comment and login cookies and comment metadata (the Contact forms and Analytics headings are empty), sharing only with permission, comment retention and the contact info@clearcutaccounts.com, but it never names the organization. The page also says the full GDPR policy is available on request, so it is a short notice that points to the full policy elsewhere: partial_policy.
  - verifier: complete_policy. The page is a complete privacy policy describing the site's data practices. It covers data collection via cookies/comments, sharing limitations, retention, and contact details for the data controller.
- **v301** (p_0.6_0.9) https://startuppilot.global/p/privacy
  - labelers: partial_policy. The policy states collection (personal identification information, Student email addresses) and use (customer service, personalization, periodic emails), but its sharing heading is empty and it gives no rights, retention period or privacy contact; saying Students may refuse to supply information only describes voluntary provision. A policy page that lacks item 3 is partial_policy, and the builder text names only the School, so the generator rule also rules out complete_policy.
  - verifier: complete_policy. The page states what personal data is collected, how it is used, and the choice of students to refuse providing personal identification information.
- **v485** (p_0.6_0.9) https://globalcyberinstitute.org/privacy-policy
  - labelers: partial_policy. The shown beginning is terms of service and the shown end is only the closing changes paragraph of a privacy policy plus a footer and cookie banner, so the two shown parts are not one policy and the omitted middle cannot be assumed to complete it. The shown policy text states no collected data, no use or sharing, and no rights, retention or contact, so the policy fragment makes the page partial_policy.
  - verifier: complete_policy. The page contains Terms of Service followed by a full privacy policy, the body of which is contained in the omitted middle portion. Under the rubric, a page containing terms of service followed by a full privacy policy is labeled complete_policy.
- **v285** (p_0.9_0.99) https://labelsbase.net/privacy
  - labelers: partial_policy. LabelsBase states collection (name, phone number, postal address, log data such as IP address) and use (contacting users, service updates, improving the service), but it states no rights, choices or retention period, and the Contact Us heading ends without any contact details. A heading alone does not supply item 3, so the page is partial_policy.
  - verifier: complete_policy. The page is the complete privacy policy for LabelsBase. It specifies what data is collected, how it is used, and retention/deletion for data collected from children.
- **v346** (p_0.9_0.99) https://itsmoked.com/privacy-policy/
  - labelers: not_policy. The stock WordPress text states collection (comment form data, IP address, user agent), sharing (Gravatar, spam detection service) and rights and retention (export, erasure, comments kept indefinitely), but it never names the organization and leaves several headings empty. Under the generator rule a builder default counts only with the organization's name filled in, so this unfilled template is not_policy.
  - verifier: complete_policy. The page states what personal data is collected, how it is shared, and user rights and retention periods, fulfilling all three required items.
- **v092** (p_lt_0.6) https://www.childprotection.sa.gov.au/privacy
  - labelers: partial_policy. The statement gives collection (visit logs, contact emails) and use and disclosure, but states no rights, no retention period and no privacy contact. The text also ends at a bare "Service Providers" heading.
  - verifier: complete_policy. The page is a complete privacy policy describing the collection of browsing data and contact email addresses, how that information is used and shared, and specifying retention and consent requirements for disclosure.
- **v199** (p_lt_0.6) https://ff.design/privacy-policy/
  - labelers: partial_policy. Policy sections without an introduction or organization name: they state collection of contact data and IP addresses and sharing with MailChimp and Google, but give no rights, retention period or privacy contact.
  - verifier: complete_policy. The page serves as the complete privacy policy for the site, detailing what data is collected, how it is used and shared with third parties, and retention details regarding submitted information.

### Labelers complete_policy, verifier not (false negatives): 24

- **v546** (appstore) https://rvgsoftware.com/privacy-policy
  - labelers: complete_policy. A short template policy for the Combo Trainer service that states collection of personally identifiable and device-identifying information, its use to provide the service, retention and an invitation to contact. The collection and contact statements are vague and no contact address is given.
  - verifier: partial_policy. The page is a generator-derived policy that mentions collecting device identifiers and using information to provide the service, but it does not name the organization and lacks information on user rights, data retention, or how to contact the organization.
- **v565** (appstore) http://newpub.co/privacy.html
  - labelers: complete_policy. The page states collection (email, social IDs, device and advertising IDs, IP address, location, usage data), sharing through international transfer under the Data Privacy Framework or standard contractual clauses together with interest-based advertising, and rights (opt-out, copy, deletion) with contact details for NewPubCo, Inc. All three items are stated by one named organization, so it is complete_policy.
  - verifier: partial_policy. The page states what personal data is collected and describes user rights and contact details, but it does not state how the organization uses or shares that data.
- **v132** (gplay) https://www6.webnow.com.br/mobile/privacy_policy?app=imprensafm
  - labelers: complete_policy. The full privacy policy of one radio app states that it collects no personal data and therefore neither uses nor shares any. It gives a privacy contact at Webnow Tecnologia Ltda.
  - verifier: partial_policy. The page is a privacy notice that provides contact information, but it lacks statements describing the collection of personal data (stating only that none is collected) and the use or sharing of personal data.
- **v144** (gplay) http://goggleplayprivacypolicepan.blogspot.com/
  - labelers: complete_policy. A short app policy by one developer that states it collects nothing, shares nothing with third parties, and gives a privacy contact email.
  - verifier: partial_policy. The page is a privacy policy for a mobile application, but it lacks complete sentences stating what personal data is collected and how that data is used or shared.
- **v280** (gplay) https://sites.google.com/view/codesmithtech/home
  - labelers: complete_policy. The full policy of Code Smith Tech states that it collects no personal data, that anonymous crash details serve stability and app stores govern their own data, and gives a contact email.
  - verifier: partial_policy. The page states that the organization does not collect personal data and provides contact details, but it lacks a statement describing how personal data is used or shared.
- **v006** (p_0.6_0.9) http://www.tblbrands.com/privacy-policy/
  - labelers: complete_policy. The policy of TblBrands.com. It states collection (name, survey information), uses of the data, and a choice to decline cookies plus removal of traffic data after analysis, but it gives no privacy contact.
  - verifier: partial_policy. The page does not contain a complete sentence stating what personal data is collected (only fragment bullet points), and it lacks contact information and general rights or retention details for personal data.
- **v037** (p_0.6_0.9) https://axiscloudsync.com/axis-cloudsync-privacy-policy/
  - labelers: complete_policy. The full privacy policy of AXIS CloudSync. Its data categories are thin (payment information and cookies), but it states that collection, sharing with third parties and for legal reasons, and a retention rule. It states no user rights.
  - verifier: partial_policy. The page describes sharing, security, and retention practices, but it fails to state what personal data the organization collects.
- **v169** (p_0.6_0.9) https://wilmingtonadventures.com/privacy-policy/
  - labelers: complete_policy. The page states collection (name and email from the contact form, browsing data gathered for advertising), use and sharing (third-party advertising companies collect data for interest-based ads and retargeting), and a choice (opt-out through the DAA and NAI sites). The cookie_only rule says a page that also describes other handling of personal data and states all three items is complete_policy.
  - verifier: partial_policy. This page is a single section focused on interest-based advertising rather than a complete privacy policy. While it mentions collecting personal information on the contact form and provides opt-out choices, it does not explain how that personal data is used or shared, nor does it name the organization.
- **v185** (p_0.6_0.9) http://americanmovingpartners.com/privacy-policy/
  - labelers: complete_policy. A short policy of American Moving Partners that states what it collects (emails and form submissions), shares it with movers and carriers, and gives a correction right and a privacy contact; a cancellation notice follows.
  - verifier: partial_policy. The page describes data use, sharing, and contact details for inquiries, but it does not state what personal data the organization collects.
- **v143** (p_0.9_0.99) http://besthamstercage.com/privacy-policy/
  - labelers: complete_policy. The policy of BestHamsterCage.com states what it collects, sharing with third-party ad networks, cookie opt-out choices and a contact address.
  - verifier: partial_policy. The page states what personal data is collected and provides contact information, but it fails to state how the organization uses or shares that personal data. Because one of the three required items is missing, it is labeled a partial policy.
- **v419** (p_0.9_0.99) https://www.globalsk.com/privacy-policy/
  - labelers: complete_policy. The default WordPress privacy policy deployed on the site, with several empty headings and no organization name. It states the comment and login data collected, sharing with Gravatar and a spam detection service, retention periods, and export and erasure rights.
  - verifier: not_policy. The page is a default WordPress privacy policy template published with empty sections and without the organization's name filled in. Under the rubric, unfilled policy templates are not_policy.
- **v058** (p_ge_0.99) https://apexwindowcleaning.net/privacy-policy/
  - labelers: complete_policy. A generator-based policy of Apex Window Cleaning, LLC: it states collection, use and disclosure, and choices to refuse cookies and opt out of Google Analytics; the Contact Us section is empty.
  - verifier: partial_policy. The page is a complete privacy policy for Apex Window Cleaning, LLC. It states the types of data collected, how the data is used and shared, and choices available to users regarding cookies.
- **v010** (p_lt_0.6) http://feedtrucks.com/about-us/privacy-policy/
  - labelers: complete_policy. A short policy of Warren Manufacturing, Inc. It states collection (name, demographic and survey information), use and non-disclosure to outside parties, and a postal contact for questions.
  - verifier: partial_policy. The page states how data is used/shared and provides contact details, but it lacks a complete sentence stating what personal data the organization collects.
- **v105** (p_lt_0.6) https://www.jhmbuttco.com/privacy-policy/
  - labelers: complete_policy. A short whole policy of one shop. It states collection (cart contents, delivery addresses, login details), use and sharing for delivery, and one choice (blocking cookies), but gives no rights, retention or contact details.
  - verifier: partial_policy. The page states how data is used and shared as well as a choice regarding cookies, but it does not specify what personal data the organization collects.
- **v240** (p_lt_0.6) https://inverkipbandb.co.uk/data-privacy-statement/
  - labelers: complete_policy. Although the text starts mid-list, the Belle Vue B&B statement states collection (nationality, passport number and place of issue, next destination), sharing (FreeToBook holds booking data and passes card details to PayPal, no marketing sharing) and retention (guest details kept at least 12 months). The rubric makes a crawl-cut page partial only when the three items are not all present, so all three present makes it complete_policy.
  - verifier: partial_policy. The page contains only a single section ('1. TOURIST ACCOMMODATION REGISTRATION') rather than a full privacy policy covering data handling in general, and lacks a complete sentence stating what personal data is collected.
- **v270** (p_lt_0.6) https://browncountygives.org/bcgives/privacy-policy/
  - labelers: complete_policy. A short privacy statement of Brown County Community Foundation. It states collection through registrations and forms (including email address), use for mailings without sharing, and a contact for questions, though the collection item is thin and the postal address is missing.
  - verifier: partial_policy. The page describes how personal data is used and shared, and welcomes questions on the policy, but it does not specify what personal data the foundation collects.
- **v295** (p_lt_0.6) https://ellengelbin.com/privacy.htm
  - labelers: complete_policy. The privacy statement of attorney Ellen Gelbin states collection, internal use and no transfer to third parties. Item three rests only on the choice to call instead of using the online scheduling service, so the page is a thin case.
  - verifier: partial_policy. The page states what personal data is collected and how it is used and shared, but it does not state any user rights or choices, data retention periods, or contact details for privacy inquiries.
- **v331** (p_lt_0.6) https://distresscentredurham.com/privacy-statement/
  - labelers: complete_policy. The privacy statement of one distress centre: it states that it collects personal information and call records, how it uses the information, a one-year retention period, an opt-out, and the Executive Director as privacy contact. The description of collected data is general.
  - verifier: partial_policy. The page describes how personal information is used and shared, retention periods, and contact details, but it does not specify what categories or types of personal data the organization collects.
- **v349** (p_lt_0.6) https://www.affidata.com/sh/menu_event;jsessionid=978FD8D2C74FA2915EBEC756EFF7A3BB?cmd=footer&page=privacy
  - labelers: complete_policy. A short full policy of Affidata: it states, in general terms, the personal and technical data collected, its use and non-disclosure, and a choice to opt out of advertising cookies, but gives no contact or retention.
  - verifier: partial_policy. The page describes use and sharing of personal data as well as an opt-out choice, but it does not specify what personal data the organization collects.
- **v354** (p_lt_0.6) https://wideeyes.ai/privacypolicy/
  - labelers: complete_policy. A full GDPR policy of Wide Eyes Technologies: it states collection in general terms (information contributed by persons and data from website forms), uses and recipients, retention, and rights with a contact email.
  - verifier: partial_policy. The page describes data use, data retention, and user rights, but fails to specify what personal data the organization collects.
- **v380** (p_lt_0.6) https://www.pocketrocketconsultancy.co.uk/privacy-policy
  - labelers: complete_policy. The short policy of Pocket Rocket Marketing states that it collects contact form data such as a telephone number, uses it only to answer enquiries and does not share it. It also gives a 12-month retention period and rights to view, amend or delete data by email.
  - verifier: partial_policy. The page describes data use, sharing, retention, and user rights, but it lacks a complete sentence stating what personal data the organization collects.
- **v392** (p_lt_0.6) https://nicolaholdsworth.com/privacy-policy/
  - labelers: complete_policy. A short policy of one site operator with some empty headings: it states the data collected through the contact form, cookies and payments, how that data is used and shared with PayPal, and the right to erasure.
  - verifier: partial_policy. The page states how personal data is shared and describes user erasure rights, but it does not specify what personal data is collected.
- **v548** (p_lt_0.6) https://main.dev.renxdashboard.ca.nmsrv.com/privacy-policy/
  - labelers: complete_policy. The page states the data RENX holds (subscribers' contact details, email addresses and other contact information in its records and databases), how it shares that data (only with permission, or with investors, partners and financial institutions for validation), and a right to deletion on request via contact. All three items are stated, so it is complete_policy.
  - verifier: partial_policy. The page describes how subscriber information is shared and how to cancel subscriptions or request data deletion, but it does not specify what personal data the organization collects.
- **v556** (p_lt_0.6) https://www.memorylaneflowers.net/system/privacy
  - labelers: complete_policy. A brief Eflorist privacy policy shown on a florist site: it states the recipient and customer data collected, their use for delivery and recognising visits, no sharing, and the controller's contact address. It states no rights or retention, so the third item rests only on the contact address.
  - verifier: partial_policy. The page states what data is collected and how it is used or shared, but it does not specify user rights, data retention periods, or how to contact the organization regarding privacy.

### Other disagreements: 3

- **v183** (p_0.6_0.9) https://ca-egusd-psv.edupoint.com/PXP2_Activate_Account_Privacy_Parent.aspx
  - labelers: partial_policy. The two-sentence privacy statement states only safeguards and a contact phone number, and it does not state what personal data the district collects or how it uses or shares that data; the rest of the page is a use agreement. Under the hard-case order the short privacy statement (partial_policy) ranks before the use agreement (other_legal).
  - verifier: other_legal. The page is primarily a terms of use and acceptable use agreement for the ParentVUE and StudentVUE portal rather than a privacy policy. It does not state what personal data is collected or how data is used or shared.
- **v379** (p_0.9_0.99) https://www.perfectlyyou.com.au/termsprivacy
  - labelers: partial_policy. The shown text is website terms with a short privacy section that states use (service improvement, marketing statistics), limited disclosure (by law) and a right to change details by email, but does not state what personal data is collected. The section points to a separate Privacy Policy, so it is a short notice under partial_policy, which ranks above other_legal for a page holding both.
  - verifier: other_legal. The page contains the website terms and conditions of use and a disclaimer, and explicitly directs users to read a separate privacy policy. It does not state what personal data is collected.
- **v133** (p_lt_0.6) https://gotgame.com/tag/privacy/
  - labelers: not_policy. The page is a /tag/privacy/ archive whose text holds only site headings, a do-not-sell link and a cookie consent banner, so the main content states no collection, no use or sharing, and no rights, retention or contact for the organization. The rubric says to judge the main content and not surrounding banners, and a tag archive page is not_policy.
  - verifier: cookie_only. The page is a cookie consent and preference notice explaining necessary versus non-necessary cookies and opt-out choices, with no broader privacy policy.

