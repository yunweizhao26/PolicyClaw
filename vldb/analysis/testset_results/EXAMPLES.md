# Examples from the 600-policy test set for the three listings of section 7.4

All rules are read from `corpus/testset/rules/<policy>.jsonl`, term relations from `rules/<policy>.terms.json`, and sentences from `corpus/testset/final_text/<policy>.json`. Candidates were enumerated by scripts that apply the same conditions as `vldb/analysis/corpus_results/queries.py` (`--set testset --terms on`); the redundancy pairs were re-checked with `queries.unit_queries`, which reports each as `("subsumed", general, specific, ["data"])`. The compliance pairs come from `out/pair_records.jsonl` (outcome `overlap_candidate`, the DENY rule being a consent promise). The coverage list is the 8 policies of `coverage["versions: collection without retention or erasure"]`. Quotes are verbatim from the section text. Rule fields are as stored: polarity, action node, data, recipient, guard. An empty recipient is shown as `""`.

## Listing 1: redundant pair (a broad rule covers a narrower one through a data term relation)

Selection criterion: both rules ALLOW, same action node, same actor, recipient, source, and purpose, both guards `{"op": "true"}`, and the data of the second is below the data of the first in the policy's term relations.

### 1a. apple-117 (recommended). App Store arm. Aviation Data Systems, Inc., "MyRadar Accurate Weather Radar", a weather app.

| | General rule | Specific rule |
|---|---|---|
| id | `apple-117#s5.9.0` | `apple-117#s5.14.0` |
| polarity, action | ALLOW, `sell@sale` | ALLOW, `sell@sale` |
| data | `personal data` | `sensitive personal data` |
| recipient, guard | `""`, `{"op": "true"}` | `""`, `{"op": "true"}` |
| section | `apple-117#s5` | `apple-117#s5` |
| quote | "We may also process your personal data for targeted advertising and sell certain personal data." | "NOTICE: We may sell your sensitive personal data." |

Relation: `terms.json`, slot data, parents: "sensitive personal data" under "personal data" (and "personal data" under "data we collect"). Redundancy kind: subsumed, broader field data.
Judgment: a careful reader agrees. Both sentences state a permission to sell, and the second kind of data is a subtype of the first. (The sentence after the second quote adds that precise geolocation is sold only with consent, a condition the rule does not carry.)

### 1b. apple-148. App Store arm. Progressive Insurance, "Progressive", a car insurer's app.

| | General rule | Specific rule |
|---|---|---|
| id | `apple-148#s11.1.0` | `apple-148#s13.6.0` |
| polarity, action | ALLOW, `use@use` | ALLOW, `use@use` |
| data | `user data` | `location of your device` |
| recipient, guard | `""`, `{"op": "true"}` (purpose `service provision` in both) | `""`, `{"op": "true"}` |
| section | `apple-148#s11` | `apple-148#s13` |
| quote | "We may also use the data we receive for purposes such as:" | "We may use the location of your device to dispatch emergency assistance." |

Relation: `terms.json`, slot data: alias "user data" = "personal data"; alias "location of your device" = "device location"; "device location" under "Geolocation Data" and "location", and the chain reaches "personal data".
Judgment: a careful reader agrees. The first sentence is a lead-in to a list of uses and the second is one instance with a narrower data item. It takes three relation steps, which shows the term relations at work.

### 1c. web-185. Website arm. coursera.org, an online learning platform.

| | General rule | Specific rule |
|---|---|---|
| id | `web-185#s2.4.0` | `web-185#s2.10.0` |
| polarity, action | ALLOW, `collect@collection` | ALLOW, `collect@collection` |
| data | `personal data` | `name` |
| source, recipient, guard | `user`, `""`, `{"op": "true"}` | `user`, `""`, `{"op": "true"}` |
| section | `web-185#s2` | `web-185#s2` |
| quote | "you may need to submit, or we may collect, "Personal Data" (i.e., information that can be used to identify you ..." | "Personal Data can include information such as your name, email address, IP address, and device identifier, among other things." |

Relation: `terms.json`, slot data: "name" under "Identity and Contact Data", "business contact information", and "personal data" (via the chain in `Q.above`).
Judgment: a careful reader agrees the second rule is covered, but both rules come from one paragraph (the stored `polarity_text` of both is "may collect"), so this is the weakest of the three as a showcase.

Also seen and rejected as a listing: apple-043 (Sonic Drive-In, a restaurant app) pairs "demographic information" with "gender", but its general rule drops the condition "If you complete a survey" (guard `true`), so the example would need an explanation. Many pairs in apple-125 and android-171 come from table cells and have one-word quotes.

## Listing 2: compliance candidate (consent promise overlapped by an unconditional permission, same practice)

All pairs below are in the 498 same-practice pairs: the DENY rule is a disclosure rule whose guard uses `consent.*`, the ALLOW rule is a disclosure rule with guard `true`, and the decision procedure reports `overlap_candidate` with relation `incomparable` (the prohibition wins on the overlap). The general ALLOW rule has an empty purpose, which covers the promise's purpose `marketing`.

### 2a. web-018 (recommended). Website arm. paypal.com, an online payments service.

| | DENY rule (promise) | ALLOW rule |
|---|---|---|
| id | `web-018#s24.8.0` | `web-018#s10.10.0` |
| action | `disclose@disclosure by transmission` | `disclose@disclosure by transmission` |
| data | `Personal Information` | `personal data` (alias of "Personal Information") |
| recipient | `third party` (purpose `marketing`) | `third party` (purpose `""`) |
| guard | `{"op":"and","args":[{"op":"eq","var":"user.jurisdiction","value":"Vermont"},{"op":"eq","var":"user.jurisdiction","value":"Vermont"},{"op":"not","arg":{"op":"bool","var":"law.permitted"}},{"op":"not","arg":{"op":"bool","var":"consent.share_information"}}]}` | `{"op":"true"}` |
| section | `web-018#s24` | `web-018#s10` |
| quote | "Vermont: If your PayPal, Xoom account or Fastlane profile has a Vermont mailing address, we will not disclose information about your creditworthiness to our affiliates and will not disclose your Personal Information, financial information, credit report, or health information to nonaffiliated third parties to market to you, other than as permitted by Vermont law, unl[ess ...]" | "We may disclose Personal Information with other third parties. For example, we disclose Personal Information to advertising platforms, at your direction." |

Relation: `terms.json`, slot data: alias "personal data" = "Personal Information". Outcome: `overlap_candidate`, `incomparable`.
Judgment: a careful reader agrees it is worth a review. The unconditional permission to disclose to third parties and to advertising platforms has no Vermont exception in its own sentence, while the Vermont paragraph promises no marketing disclosure without consent. The policy may intend the Vermont paragraph to override, which the rule pair cannot show.

### 2b. apple-132. App Store arm. Sonos, Inc., "Sonos", a wireless speaker app.

| | DENY rule (promise) | ALLOW rule |
|---|---|---|
| id | `apple-132#s30.4.0` | `apple-132#s27.2.0` |
| action | `share@disclosure by transmission` | `disclose@disclosure by transmission` |
| data | `personal information` | `personal data` (alias) |
| recipient, purpose | `third party`, `marketing` | `third party`, `services` |
| guard | `{"op":"and","args":[{"op":"eq","var":"user.jurisdiction","value":"California"},{"op":"not","arg":{"op":"or","args":[{"op":"bool","var":"opt_in.share_third_party_direct_marketing"},{"op":"not","arg":{"op":"bool","var":"opt_out.share_third_party_direct_marketing"}}]}}]}` | `{"op":"true"}` |
| section | `apple-132#s30` | `apple-132#s27` |
| quote | "Sonos does not share personal information with third parties for their direct marketing purposes (as defined by California Civil Code Section 1798.83) unless we give you choice (to opt in or opt-out) before sharing with those third parties." | "The disclosure of your personal information to these third parties to assist us in providing these services may be considered a "sale" of personal information under the CCPA, or the "sharing" of your personal information for purposes of "cross-context behavioral advertising."" |

Relation: `terms.json`: alias "personal information" = "personal data". Outcome: `overlap_candidate`, `incomparable`.
Judgment: partly. The preceding sentences say Sonos provided a hashed email address and cookie data to advertising providers for targeted advertising, which is close to the promised practice, and the policy offers an opt-out in the same section, so a reader would call it a candidate to check, not a clear violation.

### 2c. apple-140. App Store arm. Zip Co US, Inc., "Zip - Buy Now, Pay Later", a consumer-credit app.

| | DENY rule (promise) | ALLOW rule |
|---|---|---|
| id | `apple-140#s10.5.0` | `apple-140#s10.2.0` |
| action | `disclose@disclosure by transmission` | `share@disclosure by transmission` |
| data | `personal data` | `data` (alias of "information") |
| recipient, purpose | `third party`, `marketing` | `""`, `service provision` |
| guard | `{"op":"and","args":[{"op":"eq","var":"user.jurisdiction","value":"Vermont"},{"op":"not","arg":{"op":"bool","var":"law.permitted"}},{"op":"not","arg":{"op":"bool","var":"consent.share_information"}}]}` | `{"op":"true"}` |
| section | `apple-140#s10` | `apple-140#s10` |
| quote | "...we will not disclose your personal information, financial information, credit report, or health information to nonaffiliated third parties to market to you, other than as permitted by Vermont law, unl[ess ...]" | "Please note that certain exceptions may apply under applicable laws and regulations that allow us to share your information without your consent for specific purposes, such as processing transactions and servicing your accounts." |

Judgment: weak. The permission names legal exceptions and service purposes, not marketing, so a careful reader would call this a false alarm. It is useful as a contrast with 2a.

Also seen: web-062 (paloaltonetworks.com, network security) pairs a direct-marketing promise with "We may disclose personal information to a third party during negotiation of, in connection with or as an asset in such a corporate business transaction." The purposes differ, so a reader would disagree (the overlap comes from the rule's `legal claims` purpose being judged compatible). android-158 (Facemoji keyboard) pairs "We do not sell the personal information of consumers we know to be less than 16 years of age, unless we receive affirmative authorization" with "we may sell your personal information to third parties, subject to your right to opt out", a specific exception inside a general rule, also a false alarm.

## Listing 3: coverage (collection rule, no retention or erasure rule)

The query (`unit_queries`): the policy has an ALLOW rule under the operation "collection" and no rule under "storage" or "erasure or destruction" (action network, with the policy's terms). 8 of 600 policies: 2 website, 4 Google Play, 2 App Store. Counting a retention time in a guard gives the same 8. I read the full section texts of each policy (they are short; USAA and GM are the longest at about 7,000 to 8,600 characters).

| Policy | Arm | Organization and sector | Rules, ALLOW collection rules | A collection rule (id, data, guard) | Does the text mention retention or deletion? |
|---|---|---|---|---|---|
| android-094 | Google Play | Neron's Brother, "Supreme Duelist", a mobile game | 7, 3 | `android-094#s2.1.0` `collect@collection`, `data`, guard `event.submit_requests`: "When you submit requests to us, we collect and process data from you to facilitate a response." | No. No retention period, no deletion. The only related text is "please contact us so that we will be able to do necessary actions" about children's data. Real gap. |
| android-114 | Google Play | Chess Prince, "Chess", a board game | 13, 4 | `android-114#s1.0.0` `personal data`, guard `event.use_service`: "...the collection, use, and disclosure of Personal Information..." | Barely. "The information that I request will be retained on your device and is not collected by me in any way." concerns local storage only. No retention period or deletion right. Real gap. |
| android-136 | Google Play | a Korean developer (MP3 Video Converter), a music and audio tool | 52, 13 | `android-136#s1.16.0` `precise location data`, guard `event.app_in_use or event.app_running_in_background`: "When this app is in use (or running in the background) we collect and share with our business partners certain device and location data..." | No. Real gap. |
| android-172 | Google Play | Sofeh, "ORG 24: Your Music", a music keyboard app | 7, 1 | `android-172#s1.5.0` `identifying information`, actor `third party`, guard `true`: "The app uses third-party services that may collect information to identify you." | No. Real gap, although the only collector is a third party. |
| apple-050 | App Store | USAA, "USAA Mobile", a bank and insurer | 36, 11 | `apple-050#s1.0.0` `personal information`, guard `residual("depend on the product or service you have with us")`: "The types of personal information we collect and share depend on the product or service you have with us." | No retention period or deletion. It says "When you are no longer our customer, we continue to share your information as described in this notice", which is continued use after the relationship ends, not a retention statement. Real gap. |
| apple-124 | App Store | General Motors, "myChevrolet", a connected-vehicle app | 64, 30 | `apple-124#s1.0.0` `information`, guard `event.download_application and event.use_application_services`: "We collect information from you as described in the OnStar Privacy Statement." | No in this text. It defers to the OnStar Privacy Statement ("We collect and treat this information as described in the OnStar Privacy Statement"), which is not in the policy text, so the gap may be filled elsewhere. |
| web-180 | Website | dafont.com, a font download site | 10, 1 | `web-180#s1.0.0` `enter@collection`, `email address`, guard `residual("On some pages")`: "On some pages, you may enter your email address (to register for a member account)." | No. Real gap. |
| web-184 | Website | theconversation.com, an online news and analysis publisher | 10, 1 | `web-184#s1.0.0` `personal information`, guard `true`: "The Conversation will, from time to time, collect and use personal information." | Yes, in a list of principles: "Processed for a limited time" and "Not kept longer than necessary". They are stated as principles of the Data Protection Act 1998, with no period and no rule. The query misses them because the extractor produced no storage or erasure rule from a bullet list. Partial miss. |

Summary: 6 of the 8 have no mention of retention or deletion (android-094, android-136, android-172, apple-050, web-180, and android-114 apart from local storage). apple-124 depends on an external document. web-184 names retention principles in a list that produced no rule.

Recommended for the paper: android-094 (short, `collect` with a clear guard, no retention text anywhere) or web-180 (shortest text, 1,382 characters). web-184 is the honest counter-example if the paper discusses misses.
