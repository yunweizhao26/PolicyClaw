# Verifier against labelers

Pages in the sample: 575. Labeled by the labelers: 575. Labeled by the verifier: 575. Scored (both): 575.

## complete_policy

- Precision: 461/470 = 98.1% (95% CI 96.4 to 99.0)
- Recall: 461/490 = 94.1% (95% CI 91.6 to 95.8)
- Agreement on all five labels: 534/575 = 92.9% (95% CI 90.5 to 94.7)

## Confusion matrix

Rows: labelers. Columns: verifier.

| labelers \ verifier | complete_policy | partial_policy | cookie_only | other_legal | not_policy | total |
|---|---|---|---|---|---|---|
| complete_policy | 461 | 22 | 0 | 0 | 7 | 490 |
| partial_policy | 8 | 34 | 0 | 2 | 0 | 44 |
| cookie_only | 0 | 0 | 7 | 0 | 0 | 7 |
| other_legal | 0 | 0 | 0 | 12 | 0 | 12 |
| not_policy | 1 | 0 | 1 | 0 | 20 | 22 |
| total | 470 | 56 | 8 | 14 | 27 | 575 |

## By source

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 50 | 42 | 40 | 40 | 40/40 = 100.0% (95% CI 91.2 to 100.0) | 40/42 = 95.2% (95% CI 84.2 to 98.7) | 48/50 = 96.0% (95% CI 86.5 to 98.9) |
| gplay | 100 | 84 | 81 | 79 | 79/81 = 97.5% (95% CI 91.4 to 99.3) | 79/84 = 94.0% (95% CI 86.8 to 97.4) | 93/100 = 93.0% (95% CI 86.3 to 96.6) |
| opp115 | 25 | 24 | 24 | 24 | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 25/25 = 100.0% (95% CI 86.7 to 100.0) |
| privaseer | 400 | 340 | 325 | 318 | 318/325 = 97.8% (95% CI 95.6 to 99.0) | 318/340 = 93.5% (95% CI 90.4 to 95.7) | 368/400 = 92.0% (95% CI 88.9 to 94.3) |

## By stratum

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 50 | 42 | 40 | 40 | 40/40 = 100.0% (95% CI 91.2 to 100.0) | 40/42 = 95.2% (95% CI 84.2 to 98.7) | 48/50 = 96.0% (95% CI 86.5 to 98.9) |
| gplay | 100 | 84 | 81 | 79 | 79/81 = 97.5% (95% CI 91.4 to 99.3) | 79/84 = 94.0% (95% CI 86.8 to 97.4) | 93/100 = 93.0% (95% CI 86.3 to 96.6) |
| opp115 | 25 | 24 | 24 | 24 | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 25/25 = 100.0% (95% CI 86.7 to 100.0) |
| p_0.6_0.9 | 100 | 88 | 85 | 82 | 82/85 = 96.5% (95% CI 90.1 to 98.8) | 82/88 = 93.2% (95% CI 85.9 to 96.8) | 90/100 = 90.0% (95% CI 82.6 to 94.5) |
| p_0.9_0.99 | 100 | 95 | 93 | 91 | 91/93 = 97.8% (95% CI 92.5 to 99.4) | 91/95 = 95.8% (95% CI 89.7 to 98.4) | 93/100 = 93.0% (95% CI 86.3 to 96.6) |
| p_ge_0.99 | 100 | 100 | 99 | 99 | 99/99 = 100.0% (95% CI 96.3 to 100.0) | 99/100 = 99.0% (95% CI 94.6 to 99.8) | 99/100 = 99.0% (95% CI 94.6 to 99.8) |
| p_lt_0.6 | 100 | 57 | 48 | 46 | 46/48 = 95.8% (95% CI 86.0 to 98.8) | 46/57 = 80.7% (95% CI 68.7 to 88.9) | 86/100 = 86.0% (95% CI 77.9 to 91.5) |

## Label distribution by stratum

Each cell: labelers / verifier.

| stratum | complete_policy | partial_policy | cookie_only | other_legal | not_policy |
|---|---|---|---|---|---|
| appstore | 42 / 40 | 2 / 4 | 0 / 0 | 2 / 2 | 4 / 4 |
| gplay | 84 / 81 | 7 / 9 | 0 / 0 | 2 / 2 | 7 / 8 |
| opp115 | 24 / 24 | 1 / 1 | 0 / 0 | 0 / 0 | 0 / 0 |
| p_0.6_0.9 | 88 / 85 | 8 / 8 | 1 / 1 | 1 / 2 | 2 / 4 |
| p_0.9_0.99 | 95 / 93 | 5 / 3 | 0 / 0 | 0 / 1 | 0 / 3 |
| p_ge_0.99 | 100 / 99 | 0 / 1 | 0 / 0 | 0 / 0 | 0 / 0 |
| p_lt_0.6 | 57 / 48 | 21 / 30 | 6 / 7 | 7 / 7 | 9 / 8 |

## Flags

- multiple_orgs agreement: 575/575 = 100.0% (95% CI 99.3 to 100.0); true for labelers 0, for verifier 0, for both 0
- language agreement: 575/575 = 100.0% (95% CI 99.3 to 100.0)

## Disagreements

### Verifier complete_policy, labelers not (false positives): 9

- **v407** (gplay) https://sites.google.com/view/captcha-work-online-job/home
  - labelers: partial_policy. App terms and conditions with privacy sections on collection, cookies and data storage inserted; it states collection and a privacy contact email but describes use and sharing of personal data only for cookies, so it is not a full policy.
  - verifier: complete_policy. Although framed as terms and conditions, the page contains a complete privacy policy covering what data is collected, how personal data is processed, and how to contact the provider about privacy.
- **v457** (gplay) http://cms.appbuild.io/cms/docs/legal/privacy.php?appcode=thisapp
  - labelers: not_policy. A generator template rendered for the placeholder app code "thisapp": the organization name is the unfilled default "This App", so no organization is identified even though the template text covers collection, use and data removal.
  - verifier: complete_policy. The page is a complete privacy policy that identifies the organization (This App) and specifies the data collected, how it is used and shared, and the user's right to request data removal.
- **v168** (p_0.6_0.9) http://www.clearcutaccounts.co.uk/privacy-policy/
  - labelers: partial_policy. A short website privacy notice built from the WordPress default with several empty sections; it covers comment data, sharing, retention and a contact email but says the full GDPR policy is available elsewhere on request.
  - verifier: complete_policy. The page is a complete privacy policy describing the site's data practices. It covers data collection via cookies/comments, sharing limitations, retention, and contact details for the data controller.
- **v301** (p_0.6_0.9) https://startuppilot.global/p/privacy
  - labelers: partial_policy. A short school policy that states collection and use, but it gives no rights, retention period or privacy contact; its only choice is declining to supply information. Item 3 is therefore missing.
  - verifier: complete_policy. The page states what personal data is collected, how it is used, and the choice of students to refuse providing personal identification information.
- **v485** (p_0.6_0.9) https://globalcyberinstitute.org/privacy-policy
  - labelers: partial_policy. The shown beginning is terms of service, and the shown end holds only the closing changes section of a privacy policy whose start is omitted. The shown policy text does not state what data is collected, how it is used or shared, or rights, retention or contact.
  - verifier: complete_policy. The page contains Terms of Service followed by a full privacy policy, the body of which is contained in the omitted middle portion. Under the rubric, a page containing terms of service followed by a full privacy policy is labeled complete_policy.
- **v285** (p_0.9_0.99) https://labelsbase.net/privacy
  - labelers: partial_policy. LabelsBase's policy states what it collects and how it uses the data, but it states no rights, choices or retention, and the page ends before giving any contact details.
  - verifier: complete_policy. The page is the complete privacy policy for LabelsBase. It specifies what data is collected, how it is used, and retention/deletion for data collected from children.
- **v478** (p_0.9_0.99) https://www.carnewshere.com/privacy-policy/
  - labelers: partial_policy. A short policy page that states collection and use or sharing, but it lacks the third item: no rights, no retention, and the Contact Us heading has no contact details. The only choice mentioned is refusing cookies in the browser.
  - verifier: complete_policy. The page is a complete privacy policy that addresses personal data collection, use and sharing, and user choices regarding cookies.
- **v092** (p_lt_0.6) https://www.childprotection.sa.gov.au/privacy
  - labelers: partial_policy. The statement gives collection (visit logs, contact emails) and use and disclosure, but states no rights, no retention period and no privacy contact. The text also ends at a bare "Service Providers" heading.
  - verifier: complete_policy. The page is a complete privacy policy describing the collection of browsing data and contact email addresses, how that information is used and shared, and specifying retention and consent requirements for disclosure.
- **v199** (p_lt_0.6) https://ff.design/privacy-policy/
  - labelers: partial_policy. Policy sections without an introduction or organization name: they state collection of contact data and IP addresses and sharing with MailChimp and Google, but give no rights, retention period or privacy contact.
  - verifier: complete_policy. The page serves as the complete privacy policy for the site, detailing what data is collected, how it is used and shared with third parties, and retention details regarding submitted information.

### Labelers complete_policy, verifier not (false negatives): 29

- **v546** (appstore) https://rvgsoftware.com/privacy-policy
  - labelers: complete_policy. A short template policy for the Combo Trainer service that states collection of personally identifiable and device-identifying information, its use to provide the service, retention and an invitation to contact. The collection and contact statements are vague and no contact address is given.
  - verifier: partial_policy. The page is a generator-derived policy that mentions collecting device identifiers and using information to provide the service, but it does not name the organization and lacks information on user rights, data retention, or how to contact the organization.
- **v565** (appstore) http://newpub.co/privacy.html
  - labelers: complete_policy. A short full policy of NewPubCo that states collection, international transfer and interest-based advertising use, access and deletion rights, and contact details. Its statement of use is brief.
  - verifier: partial_policy. The page states what personal data is collected and describes user rights and contact details, but it does not state how the organization uses or shares that data.
- **v132** (gplay) https://www6.webnow.com.br/mobile/privacy_policy?app=imprensafm
  - labelers: complete_policy. The full privacy policy of one radio app states that it collects no personal data and therefore neither uses nor shares any. It gives a privacy contact at Webnow Tecnologia Ltda.
  - verifier: partial_policy. The page is a privacy notice that provides contact information, but it lacks statements describing the collection of personal data (stating only that none is collected) and the use or sharing of personal data.
- **v144** (gplay) http://goggleplayprivacypolicepan.blogspot.com/
  - labelers: complete_policy. A short app policy by one developer that states it collects nothing, shares nothing with third parties, and gives a privacy contact email.
  - verifier: partial_policy. The page is a privacy policy for a mobile application, but it lacks complete sentences stating what personal data is collected and how that data is used or shared.
- **v167** (gplay) https://oldview.com/app-privacy-policy/
  - labelers: complete_policy. The published policy of the OldView app with service-specific details: it states the data collected, uses and disclosures, and retention, rights and privacy@oldview.com. The legal entity name and address remain unfilled placeholders, but the service and contact are named.
  - verifier: not_policy. The page is a privacy policy template containing unfilled placeholders such as [Your Company Name/Legal Entity Name] and [Your Business Address], classifying it as not_policy under the rubric.
- **v280** (gplay) https://sites.google.com/view/codesmithtech/home
  - labelers: complete_policy. The full policy of Code Smith Tech states that it collects no personal data, that anonymous crash details serve stability and app stores govern their own data, and gives a contact email.
  - verifier: partial_policy. The page states that the organization does not collect personal data and provides contact details, but it lacks a statement describing how personal data is used or shared.
- **v316** (gplay) https://www.powerbiblechurch.org/privacy-policy/
  - labelers: complete_policy. A generator-based policy on the church site that states collection (email), use and third-party disclosure, and choices for cookies, ad opt-out and unsubscribing. The page ends before the contact details and never names the organization in the text.
  - verifier: not_policy. This is an unfilled policy generator template where the organization's name and details were never provided, leaving blank sections and missing contact information.
- **v006** (p_0.6_0.9) http://www.tblbrands.com/privacy-policy/
  - labelers: complete_policy. The policy of TblBrands.com. It states collection (name, survey information), uses of the data, and a choice to decline cookies plus removal of traffic data after analysis, but it gives no privacy contact.
  - verifier: partial_policy. The page does not contain a complete sentence stating what personal data is collected (only fragment bullet points), and it lacks contact information and general rights or retention details for personal data.
- **v037** (p_0.6_0.9) https://axiscloudsync.com/axis-cloudsync-privacy-policy/
  - labelers: complete_policy. The full privacy policy of AXIS CloudSync. Its data categories are thin (payment information and cookies), but it states that collection, sharing with third parties and for legal reasons, and a retention rule. It states no user rights.
  - verifier: partial_policy. The page describes sharing, security, and retention practices, but it fails to state what personal data the organization collects.
- **v185** (p_0.6_0.9) http://americanmovingpartners.com/privacy-policy/
  - labelers: complete_policy. A short policy of American Moving Partners that states what it collects (emails and form submissions), shares it with movers and carriers, and gives a correction right and a privacy contact; a cancellation notice follows.
  - verifier: partial_policy. The page describes data use, sharing, and contact details for inquiries, but it does not state what personal data the organization collects.
- **v302** (p_0.6_0.9) https://www.corchoproyectadosuromira.com/en/privacy-policy/
  - labelers: complete_policy. A GDPR notice of one named controller: it states the data provided through its forms, the purposes and sharing with group companies, the retention period, the rights, and the contact address.
  - verifier: partial_policy. The page describes data use, sharing, and data subject rights, but it fails to state what categories of personal data are collected.
- **v424** (p_0.6_0.9) https://rewindtv.cl/privacy-policy-2/
  - labelers: complete_policy. The default WordPress privacy policy published on the site, with some sections left empty and no contact details. It still states collection (comment data, IP address), sharing (Gravatar, spam detection service), retention, and export and erasure rights.
  - verifier: not_policy. This is an unedited WordPress privacy policy template with blank template headings and no organization name filled in, falling under not_policy.
- **v533** (p_0.6_0.9) http://www.garsidelaycock.com/privacy-policy/
  - labelers: complete_policy. The site's policy, in the WordPress default wording with several empty headings and no organization name in the text, states collection (comment data, IP address), use and sharing (spam detection, Gravatar), retention and export or erasure rights.
  - verifier: not_policy. This is an uncustomized default WordPress privacy policy template that never identifies the organization and leaves several template sections empty. Under the rubric, an unfilled policy template is classified as not_policy.
- **v143** (p_0.9_0.99) http://besthamstercage.com/privacy-policy/
  - labelers: complete_policy. The policy of BestHamsterCage.com states what it collects, sharing with third-party ad networks, cookie opt-out choices and a contact address.
  - verifier: partial_policy. The page states what personal data is collected and provides contact information, but it fails to state how the organization uses or shares that personal data. Because one of the three required items is missing, it is labeled a partial policy.
- **v203** (p_0.9_0.99) https://www.petiteparfait.ca/privacy-policy-2/
  - labelers: complete_policy. The site's privacy page uses the standard WordPress policy text without an organization name, and several headings are empty. It still states collection, use and sharing (spam detection, Gravatar), retention and erasure rights.
  - verifier: not_policy. The page is an uncustomized WordPress privacy policy template that leaves template sections empty and does not name an organization. Policy generator or template pages only count as policies when the organization's name is filled in, so an unfilled template is not_policy.
- **v412** (p_0.9_0.99) https://www.gessy-verne.com/privacy-policy
  - labelers: complete_policy. A generator-made policy deployed as the site's policy, with the generic name "This Website" and no bracketed placeholders. It states the log data collected, its use and sharing with advertising partners, and cookie choices and contact for children's data.
  - verifier: not_policy. The page is a generic policy template where the organization's name was never filled in (using placeholder text such as 'This Website' and 'www.website.com'). Under the rubric, generator pages and templates without the organization's name are classified as not_policy.
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
  - labelers: complete_policy. A short privacy policy of RENX: it identifies the data it holds only as subscribers' contact details and email addresses, states when that data is shared, and gives deletion on request and newsletter cancellation.
  - verifier: partial_policy. The page describes how subscriber information is shared and how to cancel subscriptions or request data deletion, but it does not specify what personal data the organization collects.
- **v556** (p_lt_0.6) https://www.memorylaneflowers.net/system/privacy
  - labelers: complete_policy. A brief Eflorist privacy policy shown on a florist site: it states the recipient and customer data collected, their use for delivery and recognising visits, no sharing, and the controller's contact address. It states no rights or retention, so the third item rests only on the contact address.
  - verifier: partial_policy. The page states what data is collected and how it is used or shared, but it does not specify user rights, data retention periods, or how to contact the organization regarding privacy.

### Other disagreements: 3

- **v183** (p_0.6_0.9) https://ca-egusd-psv.edupoint.com/PXP2_Activate_Account_Privacy_Parent.aspx
  - labelers: partial_policy. A two-sentence privacy statement by the school district gives a contact number but does not state what data is collected or how it is used or shared; the rest of the page is a use agreement.
  - verifier: other_legal. The page is primarily a terms of use and acceptable use agreement for the ParentVUE and StudentVUE portal rather than a privacy policy. It does not state what personal data is collected or how data is used or shared.
- **v379** (p_0.9_0.99) https://www.perfectlyyou.com.au/termsprivacy
  - labelers: partial_policy. The shown text is website terms of use and a disclaimer containing a short privacy section that points to a separate Privacy Policy. That section states use, limited disclosure and the right to change details, but not what personal data is collected.
  - verifier: other_legal. The page contains the website terms and conditions of use and a disclaimer, and explicitly directs users to read a separate privacy policy. It does not state what personal data is collected.
- **v133** (p_lt_0.6) https://gotgame.com/tag/privacy/
  - labelers: not_policy. A site tag archive page whose extracted text holds only site headings and a cookie consent banner. The page is not itself a policy.
  - verifier: cookie_only. The page is a cookie consent and preference notice explaining necessary versus non-necessary cookies and opt-out choices, with no broader privacy policy.

