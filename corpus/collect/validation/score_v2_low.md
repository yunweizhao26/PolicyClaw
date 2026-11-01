# Verifier against labelers

Pages in the sample: 575. Labeled by the labelers: 575. Labeled by the verifier: 575. Scored (both): 575.

## complete_policy

- Precision: 469/481 = 97.5% (95% CI 95.7 to 98.6)
- Recall: 469/490 = 95.7% (95% CI 93.5 to 97.2)
- Agreement on all five labels: 537/575 = 93.4% (95% CI 91.1 to 95.1)

## Confusion matrix

Rows: labelers. Columns: verifier.

| labelers \ verifier | complete_policy | partial_policy | cookie_only | other_legal | not_policy | total |
|---|---|---|---|---|---|---|
| complete_policy | 469 | 14 | 0 | 0 | 7 | 490 |
| partial_policy | 9 | 32 | 0 | 3 | 0 | 44 |
| cookie_only | 0 | 1 | 6 | 0 | 0 | 7 |
| other_legal | 0 | 0 | 0 | 12 | 0 | 12 |
| not_policy | 3 | 0 | 1 | 0 | 18 | 22 |
| total | 481 | 47 | 7 | 15 | 25 | 575 |

## By source

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 50 | 42 | 42 | 42 | 42/42 = 100.0% (95% CI 91.6 to 100.0) | 42/42 = 100.0% (95% CI 91.6 to 100.0) | 50/50 = 100.0% (95% CI 92.9 to 100.0) |
| gplay | 100 | 84 | 85 | 82 | 82/85 = 96.5% (95% CI 90.1 to 98.8) | 82/84 = 97.6% (95% CI 91.7 to 99.3) | 95/100 = 95.0% (95% CI 88.8 to 97.8) |
| opp115 | 25 | 24 | 24 | 24 | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 25/25 = 100.0% (95% CI 86.7 to 100.0) |
| privaseer | 400 | 340 | 330 | 321 | 321/330 = 97.3% (95% CI 94.9 to 98.6) | 321/340 = 94.4% (95% CI 91.4 to 96.4) | 367/400 = 91.8% (95% CI 88.6 to 94.1) |

## By stratum

| group | pages | labelers complete | verifier complete | both complete | precision | recall | agreement (5 labels) |
|---|---|---|---|---|---|---|---|
| appstore | 50 | 42 | 42 | 42 | 42/42 = 100.0% (95% CI 91.6 to 100.0) | 42/42 = 100.0% (95% CI 91.6 to 100.0) | 50/50 = 100.0% (95% CI 92.9 to 100.0) |
| gplay | 100 | 84 | 85 | 82 | 82/85 = 96.5% (95% CI 90.1 to 98.8) | 82/84 = 97.6% (95% CI 91.7 to 99.3) | 95/100 = 95.0% (95% CI 88.8 to 97.8) |
| opp115 | 25 | 24 | 24 | 24 | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 24/24 = 100.0% (95% CI 86.2 to 100.0) | 25/25 = 100.0% (95% CI 86.7 to 100.0) |
| p_0.6_0.9 | 100 | 88 | 83 | 79 | 79/83 = 95.2% (95% CI 88.3 to 98.1) | 79/88 = 89.8% (95% CI 81.7 to 94.5) | 85/100 = 85.0% (95% CI 76.7 to 90.7) |
| p_0.9_0.99 | 100 | 95 | 91 | 89 | 89/91 = 97.8% (95% CI 92.3 to 99.4) | 89/95 = 93.7% (95% CI 86.9 to 97.1) | 91/100 = 91.0% (95% CI 83.8 to 95.2) |
| p_ge_0.99 | 100 | 100 | 99 | 99 | 99/99 = 100.0% (95% CI 96.3 to 100.0) | 99/100 = 99.0% (95% CI 94.6 to 99.8) | 99/100 = 99.0% (95% CI 94.6 to 99.8) |
| p_lt_0.6 | 100 | 57 | 57 | 54 | 54/57 = 94.7% (95% CI 85.6 to 98.2) | 54/57 = 94.7% (95% CI 85.6 to 98.2) | 92/100 = 92.0% (95% CI 85.0 to 95.9) |

## Label distribution by stratum

Each cell: labelers / verifier.

| stratum | complete_policy | partial_policy | cookie_only | other_legal | not_policy |
|---|---|---|---|---|---|
| appstore | 42 / 42 | 2 / 2 | 0 / 0 | 2 / 2 | 4 / 4 |
| gplay | 84 / 85 | 7 / 7 | 0 / 0 | 2 / 2 | 7 / 6 |
| opp115 | 24 / 24 | 1 / 1 | 0 / 0 | 0 / 0 | 0 / 0 |
| p_0.6_0.9 | 88 / 83 | 8 / 11 | 1 / 1 | 1 / 3 | 2 / 2 |
| p_0.9_0.99 | 95 / 91 | 5 / 3 | 0 / 0 | 0 / 1 | 0 / 5 |
| p_ge_0.99 | 100 / 99 | 0 / 1 | 0 / 0 | 0 / 0 | 0 / 0 |
| p_lt_0.6 | 57 / 57 | 21 / 22 | 6 / 6 | 7 / 7 | 9 / 8 |

## Flags

- multiple_orgs agreement: 575/575 = 100.0% (95% CI 99.3 to 100.0); true for labelers 0, for verifier 0, for both 0
- language agreement: 574/575 = 99.8% (95% CI 99.0 to 100.0)

## Disagreements

### Verifier complete_policy, labelers not (false positives): 12

- **v407** (gplay) https://sites.google.com/view/captcha-work-online-job/home
  - labelers: partial_policy. App terms and conditions with privacy sections on collection, cookies and data storage inserted; it states collection and a privacy contact email but describes use and sharing of personal data only for cookies, so it is not a full policy.
  - verifier: complete_policy. The page includes terms and conditions combined with privacy policy sections that cover data collection, use, retention/transfer, and privacy contact information.
- **v414** (gplay) https://www.iscool.gr/category/apps/policy
  - labelers: not_policy. The text has lost its Greek letters and shows only punctuation, numbers and a few Latin words. A policy structure with numbered sections is visible, but none of its content is readable.
  - verifier: complete_policy. The page contains a privacy policy for FILIA LAB S.A. Despite OCR/encoding degradation removing Greek words, it states what data is collected, usage categories, and contact information.
- **v457** (gplay) http://cms.appbuild.io/cms/docs/legal/privacy.php?appcode=thisapp
  - labelers: not_policy. A generator template rendered for the placeholder app code "thisapp": the organization name is the unfilled default "This App", so no organization is identified even though the template text covers collection, use and data removal.
  - verifier: complete_policy. The page contains a complete privacy policy that covers data collection (such as GPS location and camera access), purposes of use and sharing, and user rights regarding data removal.
- **v028** (p_0.6_0.9) https://template2.shoppkg.com/PrivacyPolicy.aspx
  - labelers: not_policy. A template store page whose organization name is the placeholder "Sample Company", so it is an unfilled policy template even though the text describes collection, use and an unsubscribe choice.
  - verifier: complete_policy. The page states what personal data is collected, how it is used for promotional communications, and how users can opt out/unsubscribe.
- **v168** (p_0.6_0.9) http://www.clearcutaccounts.co.uk/privacy-policy/
  - labelers: partial_policy. A short website privacy notice built from the WordPress default with several empty sections; it covers comment data, sharing, retention and a contact email but says the full GDPR policy is available elsewhere on request.
  - verifier: complete_policy. The page is a complete privacy policy that states what personal data is collected via comments/cookies, how data is shared, and how long it is retained alongside contact information.
- **v169** (p_0.6_0.9) https://wilmingtonadventures.com/privacy-policy/
  - labelers: partial_policy. Only the interest-based advertising section of a policy; it mentions contact-form collection and an ad opt-out but does not say how the collected name and email are used, and gives no contact for privacy.
  - verifier: complete_policy. The page states what personal data is collected, how it is used/shared, and provides an opt-out choice for interest-based advertising, fulfilling all three required elements for a complete policy.
- **v301** (p_0.6_0.9) https://startuppilot.global/p/privacy
  - labelers: partial_policy. A short school policy that states collection and use, but it gives no rights, retention period or privacy contact; its only choice is declining to supply information. Item 3 is therefore missing.
  - verifier: complete_policy. The page contains a complete privacy policy covering data collection, use/sharing, and user choices/rights.
- **v285** (p_0.9_0.99) https://labelsbase.net/privacy
  - labelers: partial_policy. LabelsBase's policy states what it collects and how it uses the data, but it states no rights, choices or retention, and the page ends before giving any contact details.
  - verifier: complete_policy. The page is a complete privacy policy for LabelsBase. It details what data is collected, how it is used/shared, and provides data retention/deletion commitments for minors as well as contact instructions.
- **v478** (p_0.9_0.99) https://www.carnewshere.com/privacy-policy/
  - labelers: partial_policy. A short policy page that states collection and use or sharing, but it lacks the third item: no rights, no retention, and the Contact Us heading has no contact details. The only choice mentioned is refusing cookies in the browser.
  - verifier: complete_policy. The page is a complete privacy policy that addresses data collection, use and sharing, and rights/retention/contact instructions (including deletion of children's data and cookie refusal choices).
- **v073** (p_lt_0.6) https://mobilityrentals.com.au/privacy-act-provisions/
  - labelers: partial_policy. A narrow credit-reporting disclosure notice and applicant consent: it covers only credit information given to credit reporting agencies and is not a general privacy policy, with no rights, retention or contact details.
  - verifier: complete_policy. The page represents a credit privacy notice under the Australian Privacy Act 1988, stating what credit and identity information is collected, how it is disclosed/used, and providing a contact instruction.
- **v092** (p_lt_0.6) https://www.childprotection.sa.gov.au/privacy
  - labelers: partial_policy. The statement gives collection (visit logs, contact emails) and use and disclosure, but states no rights, no retention period and no privacy contact. The text also ends at a bare "Service Providers" heading.
  - verifier: complete_policy. The page is a complete privacy statement for the Department for Child Protection website. It describes what personal information is collected, how it is used/shared, and details regarding data retention.
- **v240** (p_lt_0.6) https://inverkipbandb.co.uk/data-privacy-statement/
  - labelers: partial_policy. Only a fragment of section 1 of a B&B's data privacy statement, starting mid-list and followed by testimonials. It mentions registration data, sharing with the booking system and retention, but the rest of the statement is missing.
  - verifier: complete_policy. The page contains Belle Vue B&B's data privacy statement, which covers data collection, sharing/use, and data retention.

### Labelers complete_policy, verifier not (false negatives): 21

- **v167** (gplay) https://oldview.com/app-privacy-policy/
  - labelers: complete_policy. The published policy of the OldView app with service-specific details: it states the data collected, uses and disclosures, and retention, rights and privacy@oldview.com. The legal entity name and address remain unfilled placeholders, but the service and contact are named.
  - verifier: not_policy. The page is a privacy policy template or draft with unfilled placeholders such as 'Provider - Means [Your Company Name/Legal Entity Name]' and 'Company: [Your Company Name]'. Because the organization's name is not filled in, it falls under not_policy according to the rubric.
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
- **v302** (p_0.6_0.9) https://www.corchoproyectadosuromira.com/en/privacy-policy/
  - labelers: complete_policy. A GDPR notice of one named controller: it states the data provided through its forms, the purposes and sharing with group companies, the retention period, the rights, and the contact address.
  - verifier: partial_policy. The page lacks a specific statement detailing what personal data is collected, referring only generically to 'information' or 'data provided'. Because it does not satisfy the collection requirement, it is a partial policy.
- **v424** (p_0.6_0.9) https://rewindtv.cl/privacy-policy-2/
  - labelers: complete_policy. The default WordPress privacy policy published on the site, with some sections left empty and no contact details. It still states collection (comment data, IP address), sharing (Gravatar, spam detection service), retention, and export and erasure rights.
  - verifier: partial_policy. This is a default WordPress privacy policy template that never specifies the name of the organization under 'Who we are' or anywhere in the body text, rendering it incomplete.
- **v433** (p_0.6_0.9) https://www.kingsworthyprimary.co.uk/page/?title=Website+Privacy+Policy&pid=62
  - labelers: complete_policy. A school's website privacy policy that states collection through forms and traffic cookies, use and sharing, and the right of access and marketing choices.
  - verifier: partial_policy. The page lacks a clear statement identifying the organization name within the text, but more importantly, it only vaguely refers to collecting personal data via online forms without specifying what personal data is collected.
- **v533** (p_0.6_0.9) http://www.garsidelaycock.com/privacy-policy/
  - labelers: complete_policy. The site's policy, in the WordPress default wording with several empty headings and no organization name in the text, states collection (comment data, IP address), use and sharing (spam detection, Gravatar), retention and export or erasure rights.
  - verifier: not_policy. The page is a generic default WordPress privacy policy template that never identifies or names the organization/site owner, meaning it is not the complete policy of an identifiable organization.
- **v343** (p_0.9_0.99) http://wickedwingsuits.com/privacy/
  - labelers: complete_policy. The full policy of Wicked Wingsuits: it states what it collects, how it uses and discloses the data, and how to opt out, request a copy or correct data by writing to the company.
  - verifier: partial_policy. The page contains a complete privacy policy for Wicked Wingsuits, detailing the information collected, how it is used and shared, and options/rights for user control along with contact information.
- **v346** (p_0.9_0.99) https://itsmoked.com/privacy-policy/
  - labelers: complete_policy. The site's stock WordPress privacy policy, with no operator name and several empty headings: it states collection of comment data and IP addresses, sharing with Gravatar and a spam service, retention and rights to export or erase data.
  - verifier: not_policy. This is a default WordPress privacy policy template that never specifies the name of the organization or site operator. Because it is an unfilled template lacking organization identification, it is classified as not_policy.
- **v412** (p_0.9_0.99) https://www.gessy-verne.com/privacy-policy
  - labelers: complete_policy. A generator-made policy deployed as the site's policy, with the generic name "This Website" and no bracketed placeholders. It states the log data collected, its use and sharing with advertising partners, and cookie choices and contact for children's data.
  - verifier: not_policy. The page is a generic boilerplate/template privacy policy that fails to name the organization or website (referring repeatedly to 'This Website', 'our website', and placeholder 'www.website.com'). Under the rubric, a template without a filled-in organization name is considered not_policy.
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
  - labelers: complete_policy. A short privacy policy of RENX: it identifies the data it holds only as subscribers' contact details and email addresses, states when that data is shared, and gives deletion on request and newsletter cancellation.
  - verifier: partial_policy. The page states how RENX shares information and provides options for deletion/contact, but it lacks a statement specifying what personal data is collected.
- **v556** (p_lt_0.6) https://www.memorylaneflowers.net/system/privacy
  - labelers: complete_policy. A brief Eflorist privacy policy shown on a florist site: it states the recipient and customer data collected, their use for delivery and recognising visits, no sharing, and the controller's contact address. It states no rights or retention, so the third item rests only on the contact address.
  - verifier: partial_policy. The page states what personal data is collected and how it is used/shared, but it lacks any mention of user rights, data retention periods, or privacy-specific contact information.

### Other disagreements: 5

- **v183** (p_0.6_0.9) https://ca-egusd-psv.edupoint.com/PXP2_Activate_Account_Privacy_Parent.aspx
  - labelers: partial_policy. A two-sentence privacy statement by the school district gives a contact number but does not state what data is collected or how it is used or shared; the rest of the page is a use agreement.
  - verifier: other_legal. The page contains a terms of use agreement with a brief privacy statement, but it lacks statements explaining what personal data is collected or how it is used or shared.
- **v485** (p_0.6_0.9) https://globalcyberinstitute.org/privacy-policy
  - labelers: partial_policy. The shown beginning is terms of service, and the shown end holds only the closing changes section of a privacy policy whose start is omitted. The shown policy text does not state what data is collected, how it is used or shared, or rights, retention or contact.
  - verifier: other_legal. The page includes both Terms of Service and an apparent Privacy Policy, but the crawl displays Terms of Service at the beginning, omits the body of the policy, and only catches the introductory and closing fragments of the Privacy Policy without showing data collection, use/sharing, or rights/contact.
- **v379** (p_0.9_0.99) https://www.perfectlyyou.com.au/termsprivacy
  - labelers: partial_policy. The shown text is website terms of use and a disclaimer containing a short privacy section that points to a separate Privacy Policy. That section states use, limited disclosure and the right to change details, but not what personal data is collected.
  - verifier: other_legal. The page contains terms and conditions with a brief privacy section that refers users to a separate Privacy Policy ('Please read our separate Privacy Policy carefully') and lacks a statement detailing what personal data is collected.
- **v133** (p_lt_0.6) https://gotgame.com/tag/privacy/
  - labelers: not_policy. A site tag archive page whose extracted text holds only site headings and a cookie consent banner. The page is not itself a policy.
  - verifier: cookie_only. The page only contains a cookie consent overview and cookie categories banner/text, focusing solely on cookies and tracking technologies.
- **v243** (p_lt_0.6) https://www.gravesthomas.com/privacy-policy/
  - labelers: cookie_only. The only privacy content is one paragraph on an ad network's cookies and an advertising opt-out; the rest is law-firm marketing and a website disclaimer.
  - verifier: partial_policy. The page contains only a brief privacy/advertising notice regarding cookies and targeted advertising opt-out, but lacks any description of what personal data the organization itself collects.

