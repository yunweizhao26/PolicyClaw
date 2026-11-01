# PolicyClaw evaluation set: revised selection

**600 policies; audit passed.**

Tranco: Y8JGG (2026-10-15). PSL: 2026-10-21; SHA-256 `3e6ca639b7ef33f86ec0e6fe9a475857cf2585f28fdf485f38f14d5f00c1c2a4`.

The first selection is preserved in `v1/`. App metadata and stored policy fetches are reused. Web policies come from the first eligible privacy link among the first three on the final homepage. All domain identities use the pinned PSL, including private rules. OPP-115 is not excluded.

## Funnel

| Arm | Organizations | Excluded | Candidates | Walked | Policy links | 2xx | >=100 chars | Verified | Complete/en | Selected | Not walked |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web | 137028 | 37 | 136991 | 537 | 479 | 462 | 449 | 449 | 249 | 200 | 136454 |
| android | 1202799 | 20 | 1202779 | 417 | 417 | 385 | 337 | 337 | 282 | 200 | 1202362 |
| apple | 437955 | 10 | 437945 | 450 | 450 | 380 | 338 | 338 | 272 | 200 | 437495 |

Policy-link counts include failed alternatives for websites; web-link rejections are nested within organization decisions. Full frame counters are in `report.json` and `frame_*.json`.

| Arm | Stage | Reason | Count |
| --- | --- | --- | --- |
| web | frame | development_domain | 34 |
| web | frame | policyie_test_site_domain | 3 |
| web | selection | home_page_not_fetched | 119 |
| web | selection | no_eligible_link_among_first_three | 129 |
| web | selection | no_privacy_link | 89 |
| web | web_link | duplicate_registered_domain | 41 |
| web | web_link | duplicate_visible_text_jaccard_ge_0.5 | 4 |
| web | web_link | http_not_2xx | 17 |
| web | web_link | not_english | 6 |
| web | web_link | policyie_containment_ge_0.5 | 4 |
| web | web_link | verifier_cookie_only | 9 |
| web | web_link | verifier_not_policy | 104 |
| web | web_link | verifier_other_legal | 23 |
| web | web_link | verifier_partial_policy | 58 |
| web | web_link | visible_text_under_100_chars | 13 |
| android | frame | development_domain | 17 |
| android | frame | policyie_test_app_id | 1 |
| android | frame | policyie_test_site_domain | 2 |
| android | selection | development_domain | 1 |
| android | selection | duplicate_registered_domain | 66 |
| android | selection | duplicate_visible_text_jaccard_ge_0.5 | 13 |
| android | selection | http_not_2xx | 32 |
| android | selection | not_english | 9 |
| android | selection | policyie_containment_ge_0.5 | 2 |
| android | selection | verifier_not_policy | 20 |
| android | selection | verifier_other_legal | 12 |
| android | selection | verifier_partial_policy | 14 |
| android | selection | visible_text_under_100_chars | 48 |
| apple | frame | development_domain | 9 |
| apple | frame | policyie_test_site_domain | 1 |
| apple | selection | development_domain | 1 |
| apple | selection | duplicate_registered_domain | 57 |
| apple | selection | duplicate_visible_text_jaccard_ge_0.5 | 14 |
| apple | selection | http_not_2xx | 70 |
| apple | selection | not_english | 1 |
| apple | selection | verifier_not_policy | 31 |
| apple | selection | verifier_other_legal | 22 |
| apple | selection | verifier_partial_policy | 12 |
| apple | selection | visible_text_under_100_chars | 42 |

## First and last selected

| Arm | Position | Rank | Organization | Size proxy | Value |
| --- | --- | --- | --- | --- | --- |
| web | first | 1 | google.com | Tranco rank | 1.0 |
| web | last | 537 | bbb.org | Tranco rank | 1340.0 |
| android | first | 6 | Microsoft Corporation | realInstalls | 6098360230.0 |
| android | last | 417 | Sketchbook | realInstalls | 192639322.0 |
| apple | first | 2 | Spotify | userRatingCount | 42587623.0 |
| apple | last | 450 | Locket Labs, Inc. | userRatingCount | 579159.0 |

## Checks and new verification cost

Maximum pairwise Jaccard: 0.49082834524039387; pair: ['android-065', 'android-108']. Maximum PolicyIE containment: 0.45191992123400065; match: `{"id": "android-040", "policyie_containment": 0.45191992123400065, "policyie_policy": "sanitized_split/train/week8/com_bagelcode_slots1", "policyie_intersection": 1377, "policyie_denominator": 3047}`.

Both use lowercase Unicode `\w+` tokens and exact 5-word shingle sets. Containment divides by the PolicyIE set size; both rejection thresholds are >=0.5.

New Gemini responses: 311; input tokens: 1341753; answer tokens: 50940; thinking tokens: 106962; observed cost: $1.59844725. Rates retained from v1: $0.75/M input, $3.75/M answer plus thinking. Responses missing usage: 0; API errors without usage: 0. Only the v2 usage ledger is counted. Cache reuse adds no model tokens.

Cross-arm organizations: `cross_arm_organizations.tsv`. Per-link reasons: `rejected_links.tsv`. Raw bodies and both texts: `fetch/`; selected texts: `texts/`; provenance: `audit.json`, `code_provenance.json`, and `policyie_source_audit.json`.

## Resources

CPU includes reaped descendants. Peak process RSS is the process high-water mark; tree RSS is sampled every 0.5 seconds. All workloads require Slurm. Per-step commands and measurements are in `metrics/v2_*.json`.

| Step | Job | CPU s | Elapsed s | Process MiB | Tree MiB | Exit |
| --- | --- | --- | --- | --- | --- | --- |
| v2_selfcheck | 20495716 | 0.506 | 5.009 | 86.93 | 79.746 | 0 |
| v2_archive | 20495716 | 2.398 | 13.017 | 645.047 | 647.375 | 0 |
| v2_psl | 20495716 | 0.216 | 2.005 | 70.457 | 66.488 | 0 |
| v2_exclusions | 20495716 | 25.391 | 29.531 | 247.656 | 237.176 | 0 |
| v2_app_frames | 20495716 | 153.386 | 157.266 | 6071.059 | 5989.77 | 0 |
| v2_web_frame | 20495716 | 236.421 | 293.859 | 1940.879 | 1916.363 | 0 |
| v2_selection | 20495716 | 169.429 | 4491.271 | 6554.746 | 6337.09 | 0 |
| v2_audit | 20495716 | 101.862 | 156.772 | 6384.828 | 6391.883 | 1 |
| v2_report | 20495716 | 0.528 | 4.006 | 147.418 | 110.109 | 0 |
| v2_audit | 20501447 | 172.395 | 239.457 | 7842.664 | 7818.738 | 0 |
| v2_report | 20501447 | 0.545 | 4.006 | 146.723 | 138.113 | 0 |

## Selected web policies

`selected_web_policies.tsv`

| Site | Tranco rank | Final homepage | Anchor text | Chosen link | Final policy |
| --- | --- | --- | --- | --- | --- |
| google.com | 1.0 | https://www.google.com/ | Privacy | https://policies.google.com/privacy?hl=en&fg=1 | https://policies.google.com/privacy?hl=en&fg=1 |
| cloudflare.com | 2.0 | https://www.cloudflare.com/ | Privacy policy | https://www.cloudflare.com/policies/privacy/ | https://www.cloudflare.com/policies/privacy/ |
| twitter.com | 15.0 | https://x.com/ | Privacy Policy | https://x.com/privacy | https://x.com/en/privacy |
| linkedin.com | 18.0 | https://www.linkedin.com/ | Privacy Policy | https://www.linkedin.com/legal/privacy-policy/ | https://www.linkedin.com/legal/privacy-policy/ |
| github.com | 30.0 | https://github.com/ | Privacy | https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement | https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement |
| gandi.net | 43.0 | https://www.gandi.net/en-US | Privacy Policy | https://www.gandi.net/en-US/contracts/privacy-policy | https://www.gandi.net/en-US/contracts/privacy-policy |
| wordpress.org | 50.0 | https://wordpress.org/ | Privacy | https://wordpress.org/about/privacy/ | https://wordpress.org/about/privacy/ |
| opera.com | 74.0 | https://www.opera.com/ | Privacy | https://www.opera.com/legal/privacy | https://www.opera.com/legal/privacy |
| vimeo.com | 88.0 | https://vimeo.com/ | Privacy | https://vimeo.com/privacy | https://vimeo.com/legal/privacy/policy |
| f5.com | 89.0 | https://www.f5.com/ | California Privacy | https://www.f5.com/company/policies/privacy-notice | https://www.f5.com/company/policies/privacy-notice |
| b-cdn.net | 93.0 | https://bunny.net | Privacy & Data Policy | https://bunny.net/privacy/ | https://bunny.net/privacy/ |
| yuga.com | 98.0 | https://yuga.com/ | Privacy Policy | https://yuga.com/privacy | https://yuga.com/privacy/ |
| sentry.io | 101.0 | https://sentry.io/welcome/ | Check out our Privacy Policy | https://sentry.io/privacy/ | https://sentry.io/privacy/ |
| ui.com | 110.0 | https://ui.com/ | Privacy Policy | https://www.ui.com/legal/privacypolicy/ | https://www.ui.com/legal/privacypolicy/ |
| lencr.org | 121.0 | https://letsencrypt.org/docs/lencr.org/ | Privacy Policy | https://letsencrypt.org/privacy/ | https://letsencrypt.org/privacy/ |
| apache.org | 133.0 | https://apache.org/ | Privacy Policy | https://privacy.apache.org/policies/privacy-policy-public.html | https://privacy.apache.org/policies/privacy-policy-public.html |
| kaspersky.com | 150.0 | https://www.kaspersky.com/ | Privacy Policy | https://www.kaspersky.com/web-privacy-policy | https://www.kaspersky.com/web-privacy-policy |
| paypal.com | 170.0 | https://www.paypal.com/us/home | Privacy Statement | https://www.paypal.com/us/legalhub/privacy-full | https://www.paypal.com/us/legalhub/paypal/privacy-full |
| criteo.com | 176.0 | https://www.criteo.com/ | Privacy Policy | https://www.criteo.com/privacy/ | https://www.criteo.com/privacy/ |
| discord.com | 177.0 | https://discord.com/ | Privacy | https://discord.com/privacy | https://discord.com/privacy |
| flickr.com | 183.0 | https://flickr.com/ | Privacy | https://www.flickr.com/help/privacy | https://www.flickr.com/help/privacy |
| ubuntu.com | 185.0 | https://ubuntu.com/ | Privacy Policy | https://canonical.com/legal/data-privacy | https://canonical.com/legal/data-privacy |
| doi.org | 208.0 | https://www.doi.org/ | Privacy Policy | https://www.doi.org/privacy-policy/ | https://www.doi.org/privacy-policy/ |
| forbes.com | 213.0 | https://www.forbes.com/ | Privacy Statement | https://www.forbes.com/fdc/privacy.html | https://www.forbes.com/privacy/english/ |
| bbc.com | 215.0 | https://www.bbc.com/ | Privacy Policy | https://www.bbc.com/pages/privacy-policy | https://www.bbc.com/pages/privacy-policy |
| mit.edu | 219.0 | https://web.mit.edu/ | Privacy | https://web.mit.edu/privacy | https://web.mit.edu/privacy/ |
| stripe.com | 220.0 | https://stripe.com/ | Privacy Policy | https://stripe.com/privacy | https://stripe.com/privacy |
| cpanel.net | 224.0 | https://www.cpanel.net/ | Privacy Policy | https://www.cpanel.net/legal-notices/ | https://www.cpanel.net/legal-notices/ |
| nist.gov | 234.0 | https://www.nist.gov/ | Site Privacy | https://www.nist.gov/privacy-policy | https://www.nist.gov/admr/oism/site-privacy |
| hubspot.com | 253.0 | https://www.hubspot.com/ | Privacy Policy | https://legal.hubspot.com/privacy-policy | https://legal.hubspot.com/privacy-policy |
| linktr.ee | 260.0 | https://linktr.ee/ | Privacy Notice | https://linktr.ee/s/privacy | https://linktr.ee/s/privacy |
| who.int | 262.0 | https://www.who.int/ | Privacy policy | https://www.who.int/about/policies/privacy | https://www.who.int/about/policies/privacy |
| hcaptcha.com | 263.0 | https://www.hcaptcha.com/ | Privacy | https://www.hcaptcha.com/privacy | https://www.hcaptcha.com/privacy |
| vungle.com | 269.0 | https://liftoff.ai/ | Privacy | https://liftoff.ai/privacy-policy/ | https://liftoff.ai/privacy-policy/ |
| rubiconproject.com | 270.0 | https://www.magnite.com/ | Website Privacy | https://www.magnite.com/legal/magnite-website-privacy-policy/ | https://www.magnite.com/legal/magnite-website-privacy-policy/ |
| amplitude.com | 272.0 | https://amplitude.com/ | Privacy Notice | https://amplitude.com/privacy | https://amplitude.com/privacy |
| taboola.com | 286.0 | https://www.taboola.com/ | Opt Out | https://www.taboola.com/policies/privacy-policy | https://policies.taboola.com/privacy-policy/ |
| www.gov.uk | 292.0 | https://www.gov.uk/ | Privacy | https://www.gov.uk/help/privacy-notice | https://www.gov.uk/help/privacy-notice |
| salesforce.com | 293.0 | https://www.salesforce.com/?bc=OTH | Privacy Info | https://www.salesforce.com/company/legal/privacy/ | https://www.salesforce.com/company/legal/privacy/?bc=OTH |
| nature.com | 296.0 | https://www.nature.com | Privacy Policy | https://www.nature.com/info/privacy | https://www.nature.com/info/privacy |
| steampowered.com | 298.0 | https://store.steampowered.com/ | Privacy Policy | https://store.steampowered.com/privacy_agreement/?snr=1_4_4__global-responsive-menu | https://store.steampowered.com/privacy_agreement/?snr=1_4_4__global-responsive-menu |
| wiley.com | 320.0 | https://www.wiley.com/en-us | Privacy policy | https://www.wiley.com/legal/privacy | https://www.wiley.com/en-us/legal/privacy |
| weebly.com | 332.0 | https://www.weebly.com/ | Privacy Policy | https://squareup.com/privacy | https://squareup.com/us/en/legal/general/privacy |
| slack.com | 338.0 | https://slack.com/ | Privacy | https://slack.com/trust/privacy/privacy-policy | https://slack.com/trust/privacy/privacy-policy |
| brave.com | 341.0 | https://brave.com/ | Brave Browser | https://brave.com/privacy/browser/ | https://brave.com/privacy/browser/ |
| nasa.gov | 352.0 | https://www.nasa.gov/ | Privacy Policy | https://www.nasa.gov/privacy/ | https://www.nasa.gov/privacy/ |
| dell.com | 354.0 | https://www.dell.com/en-us | Privacy Statement | https://www.dell.com/en-us/legal/lp/policies-privacy | https://www.dell.com/en-us/legal/lp/policies-privacy |
| appsflyer.com | 355.0 | https://www.appsflyer.com:443/ | Privacy policy | https://www.appsflyer.com/legal/privacy-policy/ | https://www.appsflyer.com/legal/privacy-policy/ |
| tp-link.com | 356.0 | https://www.tp-link.com/us/ | TP-Link's Privacy Policy | https://privacy.tp-link.com/web/official/privacy-policy?region=US | https://privacy.tp-link.com/web/official/privacy-policy?region=US |
| datadoghq.com | 363.0 | https://www.datadoghq.com/ | Privacy | https://www.datadoghq.com/legal/privacy/ | https://www.datadoghq.com/legal/privacy/ |
| checkpoint.com | 364.0 | https://www.checkpoint.com/ | Privacy Policy | https://www.checkpoint.com/privacy/ | https://www.checkpoint.com/privacy/ |
| tradingview.com | 365.0 | https://www.tradingview.com/ | Privacy Policy | https://www.tradingview.com/privacy-policy/ | https://www.tradingview.com/privacy-policy/ |
| gitlab.com | 366.0 | https://about.gitlab.com/ | Privacy statement | https://about.gitlab.com/privacy/ | https://about.gitlab.com/privacy/ |
| zendesk.com | 367.0 | https://www.zendesk.com/ | Privacy Notice | https://www.zendesk.com/company/agreements-and-terms/privacy-notice/ | https://www.zendesk.com/company/agreements-and-terms/privacy-notice/ |
| cm.com | 368.0 | https://www.cm.com/ | Privacy Statement | https://www.cm.com/app/legal/miscellaneous/privacy-statement/ | https://www.cm.com/app/legal/miscellaneous/privacy-statement/ |
| opendns.com | 374.0 | https://www.opendns.com:443/ | Cisco Online Privacy Statement | https://www.opendns.com:443/privacy-policy/ | https://www.opendns.com:443/privacy-policy/ |
| nvidia.com | 379.0 | https://www.nvidia.com/en-us/ | Privacy Policy | https://www.nvidia.com/en-us/about-nvidia/privacy-policy/ | https://www.nvidia.com/en-us/about-nvidia/privacy-policy/ |
| issuu.com | 381.0 | https://issuu.com/ | Privacy | https://issuu.com/legal/privacy | https://issuu.com/legal/privacy |
| stanford.edu | 384.0 | https://www.stanford.edu/ | Privacy | https://www.stanford.edu/privacy | https://www.stanford.edu/privacy |
| calendly.com | 406.0 | https://calendly.com/ | Privacy Policy | https://calendly.com/legal/privacy-notice | https://calendly.com/legal/privacy-notice |
| doubleverify.com | 430.0 | https://doubleverify.com/ | Privacy Notice | https://doubleverify.com/privacy-notice | https://doubleverify.com/privacy-notice |
| paloaltonetworks.com | 438.0 | https://www.paloaltonetworks.com | Palo Alto Networks Privacy Statement | https://www.paloaltonetworks.com/legal-notices/privacy | https://www.paloaltonetworks.com/legal-notices/privacy |
| branch.io | 443.0 | https://www.branch.io/ | Privacy Policy | https://legal.branch.io/saas/privacy-policy/ | https://legal.branch.io/saas/privacy-policy/ |
| grammarly.com | 444.0 | https://www.grammarly.com/ | Privacy Policy | https://www.grammarly.com/privacy-policy | https://superhuman.com/legal/privacy-policy |
| businessinsider.com | 457.0 | https://www.businessinsider.com/ | Privacy Policy | https://www.businessinsider.com/privacy-policy | https://www.businessinsider.com/privacy-policy |
| arxiv.org | 459.0 | https://arxiv.org/ | Privacy | https://info.arxiv.org/help/policies/privacy_policy.html | https://info.arxiv.org/help/policies/privacy_policy.html |
| okta.com | 461.0 | https://www.okta.com/ | Privacy Policy | https://www.okta.com/privacy-policy/ | https://www.okta.com/legal/privacy-policy/ |
| mozilla.com | 462.0 | https://www.firefox.com/en-US/ | Firefox Privacy Notice | https://www.mozilla.org/en-US/privacy/firefox/ | https://www.mozilla.org/en-US/privacy/firefox/ |
| media.net | 464.0 | https://www.media.net/ | Privacy Policy | https://www.media.net/privacy-policy/ | https://www.media.net/privacy-policy/ |
| speedtest.net | 465.0 | https://www.speedtest.net/ | Privacy Policy | https://www.ookla.com/privacy | https://www.ookla.com/privacy |
| walmart.com | 473.0 | https://www.walmart.com/ | Privacy Notice | https://corporate.walmart.com/privacy-security/walmart-privacy-notice | https://corporate.walmart.com/privacy-security/walmart-privacy-notice |
| ietf.org | 481.0 | https://www.ietf.org/ | IETF/IRTF/IAB Privacy Statement | https://www.ietf.org/privacy-statement/ | https://www.ietf.org/privacy-statement/ |
| statista.com | 484.0 | https://www.statista.com/ | Privacy | https://www.statista.com/imprint/ | https://www.statista.com/imprint/ |
| atlassian.net | 492.0 | https://www.atlassian.com/software | Privacy policy | https://www.atlassian.com/legal/privacy-policy | https://www.atlassian.com/legal/privacy-policy |
| addtoany.com | 493.0 | https://www.addtoany.com/ | Privacy | https://www.addtoany.com/privacy | https://www.addtoany.com/privacy |
| noaa.gov | 498.0 | https://www.noaa.gov/ | Protecting Your Privacy | https://www.noaa.gov/protecting-your-privacy | https://www.noaa.gov/protecting-your-privacy |
| npr.org | 500.0 | https://www.npr.org/ | Privacy | https://www.npr.org/about-npr/179878450/privacy-policy | https://www.npr.org/about-npr/179878450/privacy-policy |
| newrelic.com | 502.0 | https://newrelic.com/ | Privacy | https://newrelic.com/termsandconditions/privacy | https://newrelic.com/termsandconditions/privacy |
| scribd.com | 512.0 | https://www.scribd.com/ | AdChoices | https://support.scribd.com/hc/en-us/articles/210129366-Global-Privacy-Policy | https://support.scribd.com/hc/en-us/articles/210129366-Global-Privacy-Policy |
| foxnews.com | 516.0 | https://www.foxnews.com/ | New Privacy Policy | https://www.foxnews.com/privacy-policy | https://www.foxnews.com/privacy-policy |
| indiatimes.com | 517.0 | https://www.indiatimes.com/ | Privacy Policy | https://www.indiatimes.com/privacy-policy | https://www.indiatimes.com/privacy-policy |
| docker.com | 518.0 | https://www.docker.com/ | Privacy | https://www.docker.com/legal/privacy | https://www.docker.com/legal/privacy/ |
| mediatek.com | 532.0 | https://www.mediatek.com/ | Privacy Policy | https://www.mediatek.com/privacy-policy | https://www.mediatek.com/privacy-policy |
| oup.com | 547.0 | https://corp.oup.com | Privacy Policy | https://corp.oup.com/privacy-policy/ | https://corp.oup.com/privacy-policy/ |
| squarespace.com | 548.0 | https://www.squarespace.com/ | Privacy | https://www.squarespace.com/privacy | https://www.squarespace.com/privacy |
| wired.com | 555.0 | https://www.wired.com/ | Privacy Policy | http://www.condenast.com/privacy-policy | https://www.condenast.com/privacy-policy |
| dreamhost.com | 557.0 | https://www.dreamhost.com/ | Privacy Policy | https://www.dreamhost.com/legal/privacy-policy/ | https://www.dreamhost.com/legal/privacy-policy/ |
| digitalocean.com | 564.0 | https://www.digitalocean.com/ | Privacy Policy | https://www.digitalocean.com/legal/privacy-policy | https://www.digitalocean.com/legal/privacy-policy |
| time.com | 569.0 | https://time.com/ | Privacy Policy | https://legal.time.com/us-privacy-policy/ | https://legal.time.com/us-privacy-policy/ |
| deviantart.com | 575.0 | https://www.deviantart.com/ | Privacy Policy | https://www.deviantart.com/about/policy/privacy | https://www.deviantart.com/about/policy/privacy |
| braze.com | 579.0 | https://www.braze.com/ | Privacy Policy | https://www.braze.com/company/legal/privacy | https://www.braze.com/company/legal/privacy |
| eset.com | 588.0 | https://www.eset.com/us/ | Privacy | https://www.eset.com/us/policy-hub/privacy/ | https://www.eset.com/us/policy-hub/privacy/ |
| teamviewer.com | 595.0 | https://www.teamviewer.com/en-us/ | Privacy and Cookies | https://www.teamviewer.com/en-us/legal/privacy-and-cookies/ | https://www.teamviewer.com/en-us/legal/privacy-and-cookies/ |
| ca.gov | 598.0 | https://www.ca.gov/ | Privacy policy | https://www.ca.gov/legal/privacy-policy/ | https://www.ca.gov/legal/privacy-policy/ |
| playstation.com | 603.0 | https://www.playstation.com/en-us/ | Privacy policy | https://www.playstation.com/en-us/legal/privacy-policy/ | https://www.playstation.com/en-us/legal/privacy-policy/ |
| unesco.org | 622.0 | https://www.unesco.org/en | Privacy Notice | https://www.unesco.org/en/privacy-notice | https://www.unesco.org/en/privacy-notice |
| berkeley.edu | 623.0 | https://www.berkeley.edu/ | Privacy policy | https://www.berkeley.edu/privacy-policy/ | https://www.berkeley.edu/privacy-policy/ |
| wix.com | 626.0 | https://www.wix.com/ | Privacy Policy | https://www.wix.com/about/privacy | https://www.wix.com/about/privacy |
| verisign.com | 630.0 | https://www.verisign.com/ | Privacy | https://www.verisign.com/legal-center/privacy/ | https://www.verisign.com/legal-center/privacy/ |
| ikea.com | 636.0 | https://www.ikea.com/ | Privacy & Cookie statement | https://www.ikea.com/global/en/legal/privacy-cookie-statement/ | https://www.ikea.com/global/en/legal/privacy-cookie-statement/ |
| nintendo.com | 638.0 | https://www.nintendo.com/us/ | Privacy | https://www.nintendo.com/privacy-policy/ | https://www.nintendo.com/us/privacy-policy/ |
| techcrunch.com | 644.0 | https://techcrunch.com/ | Privacy Notice | https://techcrunch.com/privacy-policy/ | https://techcrunch.com/privacy-policy/ |
| jotform.com | 651.0 | https://www.jotform.com/ | Privacy Policy | https://www.jotform.com/privacy/ | https://www.jotform.com/privacy/ |
| stackadapt.com | 667.0 | https://www.stackadapt.com/ | Privacy Policy | https://www.stackadapt.com/legal-document-centre/platform-and-services-privacy-policy | https://www.stackadapt.com/legal-document-centre/platform-and-services-privacy-policy |
| nike.com | 669.0 | https://www.nike.com/ | .css-72ek4j{font:var(--podium-cds-typography-body2-strong);display:undefined;}@media all and (-ms-high-contrast:none),(-ms-high-contrast:active){.css-72ek4j{text-align:left;}[dir="rtl"] .css-72ek4j{text-align:right;}}Nike Privacy Policy | https://agreementservice.svs.nike.com/rest/agreement?agreementType=privacyPolicy&uxId=com.nike.commerce.nikedotcom.web&country=US&language=en&requestType=redirect | https://agreementservice.svs.nike.com/rest/agreement?agreementType=privacyPolicy&uxId=com.nike.commerce.nikedotcom.web&country=US&language=en&requestType=redirect |
| redhat.com | 677.0 | https://www.redhat.com/en | Privacy statement | https://www.redhat.com/en/about/privacy-policy | https://www.redhat.com/en/about/privacy-policy |
| ipinfo.io | 683.0 | https://ipinfo.io/ | Privacy Policy | https://ipinfo.io/privacy-policy | https://ipinfo.io/privacy-policy |
| surveymonkey.com | 684.0 | https://www.surveymonkey.com/ | Privacy notice | https://www.surveymonkey.com/mp/legal/privacy/ | https://www.surveymonkey.com/mp/legal/privacy/ |
| optimizely.com | 686.0 | https://www.optimizely.com/ | Privacy | https://www.optimizely.com/legal/privacy-notice | https://www.optimizely.com/legal/privacy-notice |
| xhamster.com | 693.0 | https://xhamster.com/ | Privacy policy | https://xhamster.com/info/privacy | https://xhamster.com/info/privacy |
| parklogic.com | 703.0 | https://parklogic.com/ | Privacy Policy | https://parklogic.com/legal/Privacy-Policy | https://parklogic.com/legal/Privacy-Policy |
| outbrain.com | 710.0 | https://www.outbrain.com/ | Privacy Policy | https://www.outbrain.com/privacy | https://www.outbrain.com/privacy/ |
| bandcamp.com | 728.0 | https://bandcamp.com/ | Privacy | https://bandcamp.com/privacy?from=footer | https://bandcamp.com/privacy?from=footer |
| itch.io | 729.0 | https://itch.io/ | Privacy | https://itch.io/docs/legal/privacy-policy | https://itch.io/docs/legal/privacy-policy |
| bugsnag.com | 738.0 | https://www.bugsnag.com/ | Privacy | https://smartbear.com/privacy/ | https://smartbear.com/privacy/ |
| independent.co.uk | 739.0 | https://www.independent.co.uk/us | Privacy policy | https://www.independent.co.uk/service/privacy-notice-a6184181.html | https://www.independent.co.uk/service/privacy-policy-a6184181.html |
| asus.com | 746.0 | https://www.asus.com/ | Privacy Policy | https://www.asus.com/terms_of_use_notice_privacy_policy/privacy_policy/ | https://www.asus.com/terms_of_use_notice_privacy_policy/privacy_policy/ |
| mailchimp.com | 747.0 | https://mailchimp.com/ | Privacy | https://www.intuit.com/privacy/statement | https://www.intuit.com/privacy/statement/ |
| globalsign.com | 748.0 | https://www.globalsign.com/en | Privacy Policy | https://www.globalsign.com/en/repository/GlobalSign-Privacy-Policy.pdf | https://www.globalsign.com/en/repository/GlobalSign-Privacy-Policy.pdf |
| mediafire.com | 758.0 | https://www.mediafire.com/ | Privacy Policy | https://www.mediafire.com/policies/privacy_policy.php | https://www.mediafire.com/policies/privacy_policy.php |
| oxylabs.io | 767.0 | https://oxylabs.io/ | Privacy Policy | https://oxylabs.io/legal/privacy | https://oxylabs.io/legal/privacy |
| porkbun.com | 768.0 | https://porkbun.com/ | Privacy Policy | https://porkbun.com/legal/agreement/privacy_policy | https://porkbun.com/legal/agreement/privacy_policy |
| gumgum.com | 769.0 | https://gumgum.com/ | Privacy Policy | https://gumgum.com/terms-and-policies/privacy-policy | https://gumgum.com/terms-and-policies/privacy-policy |
| craigslist.org | 788.0 | https://www.craigslist.org/about/sites | privacy | https://www.craigslist.org/about/privacy.policy | https://www.craigslist.org/about/privacy.policy |
| singular.net | 789.0 | https://www.singular.net/ | Privacy policy | https://www.singular.net/privacy-policy | https://www.singular.net/privacy-policy/ |
| hugedomains.com | 800.0 | https://www.hugedomains.com/ | Privacy policy | https://www.HugeDomains.com/privacy_policy.cfm | https://www.hugedomains.com/privacy_policy.cfm |
| mixpanel.com | 810.0 | https://mixpanel.com/home/ | Legal | https://mixpanel.com/legal/privacy-policy/ | https://mixpanel.com/legal/privacy-policy/ |
| ted.com | 811.0 | https://www.ted.com/ | TED's Privacy Policy | https://www.ted.com/about/our-organization/our-policies-terms/privacy-policy | https://www.ted.com/about/our-organization/our-policies-terms/privacy-policy |
| rakuten.com | 812.0 | https://www.rakuten.com/ | Privacy Policy | https://www.rakuten.com/help/article/rakuten-privacy-policy-360002101688 | https://www.rakuten.com/help/article/rakuten-privacy-policy-360002101688 |
| prnewswire.com | 817.0 | https://www.prnewswire.com/ | Privacy Policy | https://privacy.cision.com/dataprivacynotice_customersprospects | https://privacy.cision.com/dataprivacynotice_customersprospects |
| deepl.com | 833.0 | https://www.deepl.com/en | Privacy Policy | https://www.deepl.com/en/privacy | https://www.deepl.com/en/privacy |
| pendo.io | 849.0 | https://www.pendo.io:443/ | Privacy Policy | https://www.pendo.io/legal/privacy-policy/ | https://www.pendo.io/legal/privacy-policy/ |
| cloudinary.com | 851.0 | https://cloudinary.com/ | Privacy Policy | https://cloudinary.com/privacy | https://cloudinary.com/privacy |
| blackberry.com | 854.0 | https://www.blackberry.com/en | Privacy Policy | https://www.blackberry.com/en/legal/privacy-notice | https://www.blackberry.com/en/legal/privacy-notice |
| theverge.com | 860.0 | https://www.theverge.com/ | Privacy Policy | https://www.pmc.com/privacy-policy/ | https://www.pmc.com/privacy-policy |
| myspace.com | 866.0 | https://myspace.com/ | Privacy | https://myspace.com/pages/privacy | https://myspace.com/pages/privacy |
| chess.com | 869.0 | https://www.chess.com/ | Privacy Policy | https://www.chess.com/legal/privacy | https://www.chess.com/legal/privacy |
| synology.com | 874.0 | https://www.synology.com/en-us | Privacy Policy | https://www.synology.com/company/legal/privacy | https://www.synology.com/en-us/company/legal/privacy |
| jetbrains.com | 890.0 | https://www.jetbrains.com/ | Privacy Notice | https://www.jetbrains.com/legal/docs/privacy/privacy/ | https://www.jetbrains.com/legal/docs/privacy/privacy/ |
| pornhub.com | 896.0 | https://www.pornhub.com/ | Privacy Notice | https://www.pornhub.com/information/privacy | https://www.pornhub.com/information/privacy |
| agora.io | 899.0 | https://www.agora.io/en/ | Privacy Policy | https://www.agora.io/en/privacy-policy/ | https://www.agora.io/en/privacy-policy/ |
| stackexchange.com | 913.0 | https://stackexchange.com/ | Privacy Policy | https://stackoverflow.com/legal/privacy-policy | https://stackoverflow.com/legal/privacy-policy |
| latimes.com | 924.0 | https://www.latimes.com:443/ | Privacy Policy | https://www.latimes.com/privacy-policy | https://www.latimes.com/privacy-policy |
| qualtrics.com | 926.0 | https://www.qualtrics.com/ | Privacy Statement | https://www.qualtrics.com/privacy-statement/ | https://www.qualtrics.com/privacy-statement/ |
| epa.gov | 927.0 | https://www.epa.gov/ | Privacy and Security Notice | https://www.epa.gov/privacy/privacy-and-security-notice | https://www.epa.gov/privacy/privacy-and-security-notice |
| classlink.com | 932.0 | https://www.classlink.com/ | Privacy | https://www.classlink.com/company/privacy | https://www.classlink.com/company/privacy |
| odoo.com | 939.0 | https://www.odoo.com/ | Privacy | https://www.odoo.com/privacy | https://www.odoo.com/privacy |
| state.gov | 946.0 | https://www.state.gov/ | Privacy Policy | https://www.state.gov/privacy-policy | https://www.state.gov/privacy-policy |
| washington.edu | 948.0 | https://www.washington.edu/ | Privacy | https://www.washington.edu/online/privacy/ | https://www.washington.edu/online/privacy/ |
| tailscale.com | 950.0 | https://tailscale.com/ | Privacy Policy | https://tailscale.com/privacy | https://tailscale.com/privacy-policy |
| chaturbate.com | 953.0 | https://chaturbate.com/ | Privacy Policy | https://chaturbate.com/privacy/ | https://chaturbate.com/privacy/ |
| poki.com | 956.0 | https://poki.com/ | Privacy Statement | https://poki.com/en/c/privacy-statement | https://poki.com/en/c/privacy-statement |
| xnxx.com | 981.0 | https://www.xnxx.com/ | Privacy policy | https://info.xnxx.com/legal/privacy | https://info.xnxx.com/legal/privacy |
| change.org | 983.0 | https://www.change.org/ | Privacy policy | https://www.change.org/policies/privacy | https://www.change.org/policies/privacy |
| pixiv.net | 1002.0 | https://www.pixiv.net/en/ | Privacy Policy | https://policies.pixiv.net/en/privacy_policy.html | https://policies.pixiv.net/en/privacy_policy.html |
| clever.com | 1016.0 | https://www.clever.com/ | Click Here | https://clever.com/trust/privacy/policy?_gl=1*1dve0kl*_ga*MTM1NzgwMjExNi4xNzg1Nzc1Nzky*_ga_RKDHZLJBH6*czE3ODg0NDc0NzIkbzMzJGcxJHQxNzg4NDUzMzE4JGo2MCRsMCRoMA.. | https://www.clever.com/trust/privacy/policy?_gl=1*1dve0kl*_ga*MTM1NzgwMjExNi4xNzg1Nzc1Nzky*_ga_RKDHZLJBH6*czE3ODg0NDc0NzIkbzMzJGcxJHQxNzg4NDUzMzE4JGo2MCRsMCRoMA.. |
| webmd.com | 1024.0 | https://www.webmd.com/ | Privacy Policy | https://www.webmd.com/about-webmd-policies/about-privacy-policy | https://www.webmd.com/about-webmd-policies/about-privacy-policy |
| nextcloud.com | 1036.0 | https://nextcloud.com/ | Privacy | https://nextcloud.com/privacy/ | https://nextcloud.com/privacy/ |
| xerox.com | 1040.0 | https://www.xerox.com/en-us | Privacy | https://www.xerox.com/en-us/about/privacy-policy | https://www.xerox.com/en-us/about/privacy-policy |
| huffpost.com | 1041.0 | https://www.huffpost.com/ | Privacy Policy | https://www.huffpost.com/static/privacy-policy | https://www.huffpost.com/static/privacy-policy |
| whitehouse.gov | 1050.0 | https://www.whitehouse.gov/ | Privacy Policy | https://www.whitehouse.gov/privacy/ | https://www.whitehouse.gov/privacy/ |
| faphouse.com | 1056.0 | https://faphouse.com/ | Privacy Policy | https://faphouse.com/pages/privacy-policy | https://faphouse.com/pages/privacy-policy |
| pbs.org | 1063.0 | https://www.pbs.org/ | Privacy Policy | https://www.pbs.org/about/about-pbs/privacy-policy/ | https://www.pbs.org/about/about-pbs/privacy-policy/ |
| bidmachine.io | 1064.0 | https://www.bidmachine.com/ | Privacy policy | https://www.bidmachine.com/privacy-policy | https://www.bidmachine.com/privacy-policy |
| moneycontrol.com | 1065.0 | https://www.moneycontrol.com/ | Privacy Policy | https://www.moneycontrol.com/cdata/privacypolicy.php | https://www.moneycontrol.com/cdata/privacypolicy.php |
| netgear.com | 1077.0 | https://www.netgear.com:443/ | Privacy Policy | https://www.netgear.com:443/about/privacy-policy/ | https://www.netgear.com:443/about/privacy-policy/ |
| goal.com | 1079.0 | https://www.goal.com/en-us | Privacy policy | https://www.goal.com/en-us/legal/privacy-policy | https://www.goal.com/en-us/legal/privacy-policy |
| adblockplus.org | 1082.0 | https://adblockplus.org/ | Privacy Policy | https://adblockplus.org/en/privacy | https://adblockplus.org/en/privacy |
| auvik.com | 1094.0 | https://www.auvik.com/ | privacy policy | https://www.auvik.com/privacy-and-legal/privacy-policy/ | https://www.auvik.com/privacy-and-legal/privacy-policy/ |
| crazygames.com | 1100.0 | https://www.crazygames.com/ | Privacy | https://www.crazygames.com/privacy-policy | https://www.crazygames.com/privacy-policy |
| huggingface.co | 1117.0 | https://huggingface.co/ | Privacy | https://huggingface.co/privacy | https://huggingface.co/privacy |
| gsmarena.com | 1124.0 | https://www.gsmarena.com/ | Privacy | https://www.gsmarena.com/privacy-policy.php3 | https://www.gsmarena.com/privacy-policy.php3 |
| gofundme.com | 1125.0 | https://www.gofundme.com/ | Privacy Notice | https://www.gofundme.com/c/privacy | https://www.gofundme.com/c/privacy |
| amd.com | 1131.0 | https://www.amd.com/en.html | Privacy | https://www.amd.com/en/legal/privacy.html | https://www.amd.com/en/legal/privacy.html |
| tnaflix.com | 1133.0 | https://www.tnaflix.com/ | Privacy Policy | https://www.tnaflix.com/privacy | https://www.tnaflix.com/privacy |
| yale.edu | 1143.0 | https://www.yale.edu/ | Privacy Policy | https://privacy.yale.edu/resources/privacy-statement | https://privacy.yale.edu/resources/privacy-statement |
| meethue.com | 1154.0 | https://www.philips-hue.com/en-us | Philips Hue Privacy Notice | https://www.philips-hue.com/en-us/support/legal/privacy-policy | https://www.philips-hue.com/en-us/support/legal/privacy-policy |
| riotgames.com | 1156.0 | https://www.riotgames.com/en | Candidate Privacy | https://www.riotgames.com/en/candidate-privacy | https://www.riotgames.com/en/candidate-privacy |
| one.com | 1164.0 | https://www.one.com/en-gb/ | Privacy Policy | https://www.one.com/en-gb/legal/privacy/ | https://www.one.com/en-gb/legal/privacy/ |
| dafont.com | 1171.0 | https://www.dafont.com/ | Privacy Policy | https://www.dafont.com/privacy.php | https://www.dafont.com/privacy.php |
| economist.com | 1174.0 | https://www.economist.com/ | Privacy | https://www.economistgroup.com/privacy-policy | https://www.economistgroup.com/privacy-policy |
| plos.org | 1186.0 | https://plos.org/ | Privacy Policy | https://plos.org/privacy-policy/ | https://plos.org/privacy-policy/ |
| jw.org | 1189.0 | https://www.jw.org/en/ | PRIVACY POLICY | https://www.jw.org/open?docid=1011512&prefer=content | https://www.jw.org/en/privacy-policy/ |
| theconversation.com | 1197.0 | https://theconversation.com/us | Privacy policy | https://theconversation.com/us/privacy-policy | https://theconversation.com/us/privacy-policy |
| coursera.org | 1220.0 | https://www.coursera.org/ | Privacy | https://www.coursera.org/about/privacy | https://www.coursera.org/about/privacy |
| lichess.org | 1224.0 | https://lichess.org/ | Privacy | https://lichess.org/privacy | https://lichess.org/privacy |
| rightmove.co.uk | 1231.0 | https://www.rightmove.co.uk/ | Privacy Policy | https://www.rightmove.co.uk/c/privacy-policy/ | https://www.rightmove.co.uk/c/privacy-policy/ |
| furaffinity.net | 1240.0 | https://www.furaffinity.net/ | Privacy | https://www.furaffinity.net/privacy | https://www.furaffinity.net/privacy |
| fetlife.com | 1250.0 | https://fetlife.com/ | Privacy Policy | https://fetlife.com/legal/privacy-policy-zvlij | https://fetlife.com/legal/privacy-policy-zvlij |
| sectigo.com | 1264.0 | https://www.sectigo.com/ | Privacy policy | https://www.sectigo.com/privacy-policy | https://www.sectigo.com/privacy-policy |
| youporn.com | 1283.0 | https://www.youporn.com/ | Privacy Notice | https://www.youporn.com/information/privacy/ | https://www.youporn.com/information/privacy/ |
| litnet.com | 1289.0 | https://litnet.com/ | Privacy policy | https://litnet.com/ru/info/privacy-policy-gdpr | https://litnet.com/ru/info/privacy-policy-gdpr |
| ucla.edu | 1298.0 | https://www.ucla.edu:443/ | Privacy & Terms of Use | https://www.ucla.edu:443/terms-of-use | https://www.ucla.edu:443/terms-of-use |
| psu.edu | 1308.0 | https://www.psu.edu:443/ | Privacy Statements | https://www.psu.edu:443/web-privacy-statement | https://www.psu.edu:443/web-privacy-statement |
| psychologytoday.com | 1311.0 | https://www.psychologytoday.com:443/us | Privacy | https://docs.psychologytoday.com/contentweb/privacy-policy/en/latest | https://docs.psychologytoday.com/contentweb/privacy-policy/en/v1.0.14 |
| hola.com | 1313.0 | https://www.hola.com/us/ | Privacy Policy | https://www.hola.com/us/privacy-policy/ | https://www.hola.com/us/privacy-policy/ |
| irs.gov | 1322.0 | https://www.irs.gov/ | Privacy Policy | https://www.irs.gov/privacy-disclosure/irs-privacy-policy | https://www.irs.gov/privacy-disclosure/irs-privacy-policy |
| fortune.com | 1329.0 | https://fortune.com/ | Privacy Policy | https://fortune.com/privacy-policy/ | https://fortune.com/privacy-policy/ |
| twilio.com | 1338.0 | https://www.twilio.com/en-us | Privacy Policy | https://www.twilio.com/en-us/legal/privacy | https://www.twilio.com/en-us/legal/privacy |
| bbb.org | 1340.0 | https://www.bbb.org/ | Privacy Policy | https://www.bbb.org/all/privacy-policy | https://www.bbb.org/privacy-policy |

## Duplicate registered-domain rejections

`duplicate_registered_domains.tsv`; includes failed web links even if a later link was selected.

| Arm | Rejected organization | Rejected final URL | Selected organization | Selected final URL | Shared domain |
| --- | --- | --- | --- | --- | --- |
| apple | TikTok Ltd. | https://www.tiktok.com/legal/page/us/privacy-policy/en | TikTok Pte. Ltd. | https://www.tiktok.com/legal/page/us/privacy-policy/en | tiktok.com |
| android | Xiaomi Inc. | https://www.mi.com/global/about/privacy/ | Mi Music | https://privacy.mi.com/all/en_US | mi.com |
| android | Spotify AB | https://www.spotify.com/us/legal/privacy-policy/ | Spotify | https://www.spotify.com/us/legal/privacy-policy/ | spotify.com |
| android | LinkedIn | https://www.linkedin.com/legal/privacy-policy | linkedin.com | https://www.linkedin.com/legal/privacy-policy/ | linkedin.com |
| apple | X Corp. | https://x.com/en/privacy | twitter.com | https://x.com/en/privacy | x.com |
| android | SwiftKey | https://www.microsoft.com/en-us/privacy/privacystatement | Microsoft Corporation | https://www.microsoft.com/en-us/privacy/privacystatement | microsoft.com |
| apple | Netflix, Inc. | https://help.netflix.com/legal/privacy | Netflix, Inc. | https://help.netflix.com/legal/privacy | netflix.com |
| android | Zhigu Corporation Limited | https://privacy.mi.com/all/en_US/ | Mi Music | https://privacy.mi.com/all/en_US | mi.com |
| apple | PayPal, Inc. | https://www.paypal.com/us/legalhub/paypal/privacy-full | paypal.com | https://www.paypal.com/us/legalhub/paypal/privacy-full | paypal.com |
| apple | Snap, Inc. | https://values.snap.com/privacy/privacy-policy?lang=en-US | Snap Inc | https://values.snap.com/privacy/privacy-policy?lang=en-US | snap.com |
| apple | Pinterest, Inc. | https://policy.pinterest.com/en/privacy-policy | Pinterest | https://policy.pinterest.com/en/privacy-policy | pinterest.com |
| apple | Miniclip.com | https://www.miniclip.com/privacy-policy | Miniclip.com | https://www.miniclip.com/privacy-policy | miniclip.com |
| android | Uber Technologies, Inc. | https://www.uber.com/global/en/privacy-notice-riders-order-recipients/ | Uber Technologies, Inc. | https://www.uber.com/global/en/privacy-notice-riders-order-recipients/ | uber.com |
| apple | King | https://www.king.com/privacyPolicy | King | https://www.king.com/privacyPolicy | king.com |
| apple | Sybo Games ApS | https://sybogames.com/privacy-policy/ | SYBO Games | https://sybogames.com/privacy-policy/ | sybogames.com |
| android | Snap AR | https://values.snap.com/privacy/privacy-policy?lang=en-US | Snap Inc | https://values.snap.com/privacy/privacy-policy?lang=en-US | snap.com |
| apple | Discord Inc. | https://discord.com/privacy/ | discord.com | https://discord.com/privacy | discord.com |
| android | Opera | https://www.opera.com/legal/privacy | opera.com | https://www.opera.com/legal/privacy | opera.com |
| android | Alibaba Mobile | https://terms.alicdn.com/legal-agreement/terms/suit_bu1_aliexpress/suit_bu1_aliexpress201909171350_82407.html | UCWeb Singapore Pte. Ltd. | https://terms.alicdn.com/legal-agreement/terms/suit_bu1_uc/suit_bu1_uc202007241608_71682.html | alicdn.com |
| android | Supercell | https://supercell.com/en/privacy-policy/ | Supercell | https://supercell.com/en/privacy-policy/ | supercell.com |
| apple | Waze Inc. | https://support.google.com/waze/answer/12075406?dark=0 | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| android | TexAI | https://sites.google.com/view/hi-translate/%E9%A6%96%E9%A1%B5 | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| android | Canva | https://www.canva.com/policies/privacy-policy/ | Canva | https://www.canva.com/policies/privacy-policy/ | canva.com |
| apple | Hungry Studio | https://hungrystudio.com/privacyus.html | HungryStudio | https://hungrystudio.com/privacyus.html | hungrystudio.com |
| apple | Electronic Arts | http://tos.ea.com/legalapp/WEBPRIVACY/US/en/PC | ELECTRONIC ARTS | https://www.ea.com/legal/privacy-and-cookie-policy | ea.com |
| android | Discord Inc. | https://discord.com/privacy/ | discord.com | https://discord.com/privacy | discord.com |
| android | Waze | https://support.google.com/waze/answer/12075406?dark=0 | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| android | SAMSUNG INDIA ELECTRONICS PRIVATE LIMITED | https://www.samsung.com/in/info/privacy/ | Samsung R&D Institute India Noida | https://www.samsung.com/in/info/privacy/ | samsung.com |
| apple | Temu | https://www.temu.com/privacy-and-cookie-policy.html | Temu | https://www.temu.com/privacy-and-cookie-policy.html | temu.com |
| android | Disney | https://privacy.thewaltdisneycompany.com/en/current-privacy-policy/ | Disney | https://privacy.thewaltdisneycompany.com/en/current-privacy-policy/ | thewaltdisneycompany.com |
| android | Sigmoid Labs and its affiliates | https://policies.google.com/privacy?fid=D8A50C0E8D6E6AD1E46A | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| android | AIM TOP GAME TECHNOLOGY LIMITED - pool | https://sites.google.com/site/billiardscityprivacy/ | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| apple | INTSIG Information Co., Ltd | https://v3.camscanner.com/iOS/privacy | INTSIG PTE | https://v3.camscanner.com/android/privacy?language=en-us | camscanner.com |
| android | Playgendary Limited | https://newplg.dev/privacy-policy | Playgendary Limited | https://newplg.dev/privacy-policy | newplg.dev |
| android | Mozilla | https://www.mozilla.org/en-US/privacy/firefox/ | mozilla.com | https://www.mozilla.org/en-US/privacy/firefox/ | mozilla.org |
| apple | FaceApp Technology Limited | https://www.faceapp.com/en/privacy/ | FaceApp Technology Ltd | https://www.faceapp.com/en/privacy/ | faceapp.com |
| android | PayPal Mobile | https://www.paypal.com/us/legalhub/paypal/privacy-full | paypal.com | https://www.paypal.com/us/legalhub/paypal/privacy-full | paypal.com |
| apple | Tinder LLC | https://policies.tinder.com/privacy/intl/en/ | Tinder LLC | https://policies.tinder.com/privacy/intl/en/ | tinder.com |
| android | VOODOO | https://voodoo.io/privacy | Voodoo | https://voodoo.io/privacy | voodoo.io |
| apple | 2K | https://www.take2games.com/privacy/en-US/ | Peak Games | https://www.take2games.com/privacy/en-US/ | take2games.com |
| apple | Skype Communications S.a.r.l | https://www.microsoft.com/en-us/privacy/privacystatement | Microsoft Corporation | https://www.microsoft.com/en-us/privacy/privacystatement | microsoft.com |
| apple | Socialpoint | https://www.take2games.com/privacy/en-US/ | Peak Games | https://www.take2games.com/privacy/en-US/ | take2games.com |
| android | Activision Publishing, Inc. | https://www.activision.com/legal/privacy-policy | Activision Publishing, Inc. | https://www.activision.com/legal/privacy-policy | activision.com |
| android | InShot Inc. | https://inshotapp.com:443/website/policy.html | InShot Video Editor | https://inshotapp.com:443/website/InShotAndroid/privacypolicy.html | inshotapp.com |
| android | Vita Studio. | https://vitastudio.ai/pp.html | Vita Studio | https://www.vitastudio.ai/pp.html | vitastudio.ai |
| apple | Hulu, LLC | https://privacy.thewaltdisneycompany.com/en/current-privacy-policy/ | Disney | https://privacy.thewaltdisneycompany.com/en/current-privacy-policy/ | thewaltdisneycompany.com |
| android | EASY PLAY GAME TECHNOLOGY LIMITED-huawei | https://sites.google.com/site/blockpuzzlejewel/ | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| android | Unico Studio | https://unicostudio.co/privacy | UNICO STUDIO | https://unicostudio.co/privacy | unicostudio.co |
| android | Mojang | https://www.microsoft.com/en-us/privacy/privacystatement | Microsoft Corporation | https://www.microsoft.com/en-us/privacy/privacystatement | microsoft.com |
| android | Shopsy | https://www.flipkart.com/pages/shopsy-privacy-policy | Flipkart | https://www.flipkart.com/pages/privacypolicy | flipkart.com |
| android | Focus apps | https://sites.google.com/view/focus-apps-privacy-policy/ | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| apple | PicsArt, Inc. | https://picsart.com/privacy-policy/ | PicsArt, Inc. | https://picsart.com/privacy-policy/ | picsart.com |
| android | Cloudflare, Inc. | https://www.cloudflare.com/application/privacypolicy/ | cloudflare.com | https://www.cloudflare.com/policies/privacy/ | cloudflare.com |
| apple | Bytedance Pte. Ltd | https://www.capcut.com/clause/privacy-policy | Bytedance Pte. Ltd. | https://www.capcut.com/clause/privacy-policy | capcut.com |
| android | Rovio Entertainment Oy | https://www.rovio.com/privacy/ | Rovio Entertainment Oyj | https://www.rovio.com/privacy/ | rovio.com |
| android | X-FLOW | https://xflowgames.com/privacy-policy.html | X-Flow | https://xflowgames.com/privacy-policy.html | xflowgames.com |
| android | Ubiquiti Labs, LLC | https://www.ui.com/legal/privacypolicy/ | ui.com | https://www.ui.com/legal/privacypolicy/ | ui.com |
| android | CrazyLabs LTD | https://www.crazylabs.com/apps-pps/ | Crazy Labs | https://www.crazylabs.com/apps-pps/ | crazylabs.com |
| apple | Gameloft | https://www.gameloft.com/en/privacy-notice/ | Gameloft SE | https://www.gameloft.com/en/privacy-notice/ | gameloft.com |
| apple | Mosaic S.r.l. | https://support.bendingspoons.com/privacy?app=749133753 | Bending Spoons | https://support.bendingspoons.com/privacy?app=1470373330 | bendingspoons.com |
| apple | SUPERSONIC STUDIOS LTD | https://supersonic.com/privacy/ | Supersonic Studios LTD | https://supersonic.com/privacy/ | supersonic.com |
| apple | Depop Ltd | https://depophelp.zendesk.com/hc/en-gb/articles/360001792147-Privacy-Policy | zendesk.com | https://www.zendesk.com/company/agreements-and-terms/privacy-notice/ | zendesk.com |
| apple | FUGO BILISIM TEKNOLOJILERI VE YAZILIM TICARET ANONIM SIRKETI | https://fugo.com.tr/privacypolicy-wordsofwonders.html | Fugo Games | https://fugo.com.tr/privacypolicy-wordsofwonders.html | fugo.com.tr |
| android | Bitmoji | https://values.snap.com/privacy/privacy-policy?lang=en-US | Snap Inc | https://values.snap.com/privacy/privacy-policy?lang=en-US | snap.com |
| android | Pandora | http://www.pandora.com/privacy | Pandora Media, LLC | http://www.pandora.com/privacy | pandora.com |
| android | Life.Church | https://www.bible.com/privacy | Life.Church | https://www.bible.com/privacy | bible.com |
| apple | Intuit Inc. | https://www.intuit.com/privacy/statement/ | mailchimp.com | https://www.intuit.com/privacy/statement/ | intuit.com |
| apple | CBS Interactive | https://privacy.paramount.com/en/policy | Pluto.tv | https://privacy.paramount.com/en/policy | paramount.com |
| android | ZenLife Games Ltd | https://www.zenlifegames.com/privacy/ | ZenLife Games Pte. Ltd. | https://www.zenlifegames.com/privacy/ | zenlifegames.com |
| apple | Dropbox, Inc. | https://www.dropbox.com/privacy | Dropbox, Inc. | https://www.dropbox.com/privacy?mobile=1 | dropbox.com |
| apple | Zynga Inc. | https://www.take2games.com/privacy/en-US/ | Peak Games | https://www.take2games.com/privacy/en-US/ | take2games.com |
| apple | Toca Boca AB | https://www.tocaboca.com/docs/en/privacy-policy | Toca Boca | https://www.tocaboca.com/docs/en/privacy-policy | tocaboca.com |
| apple | STORYMATRIX PTE. LTD. | https://support.dramaboxdb.com/privacy.html | STORYMATRIX | https://support.dramaboxdb.com/privacy.html | dramaboxdb.com |
| android | Brave Software | https://brave.com/privacy/browser/ | brave.com | https://brave.com/privacy/browser/ | brave.com |
| android | Smart Utils Dev Team | https://sites.google.com/view/hideu-privacypolicy/ | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| android | Apple | https://www.apple.com/legal/privacy/en-ww/ | Apple | https://www.apple.com/legal/privacy/en-ww/ | apple.com |
| android | Ookla | https://www.ookla.com/privacy | speedtest.net | https://www.ookla.com/privacy | ookla.com |
| apple | Outfit7 Limited | https://talkingtomandfriends.com/privacy-policy-games/en | Outfit7 Limited | https://talkingtomandfriends.com/privacy-policy-games/en | talkingtomandfriends.com |
| apple | Score Media and Gaming Inc. | https://thescoresupport.zendesk.com/hc/en-us/articles/13873304224397-Privacy-Policy | zendesk.com | https://www.zendesk.com/company/agreements-and-terms/privacy-notice/ | zendesk.com |
| android | Budge Studios | https://budgestudios.com/en/legal/privacy-policy/?lg=en | Budge Studios | https://budgestudios.com/en/legal/privacy-policy/?lg=en | budgestudios.com |
| android | Pazu Games | https://pazugames.com/privacy-policy/ | Pazu Games Ltd | https://pazugames.com/privacy-policy | pazugames.com |
| apple | InnerSloth LLC | https://www.innersloth.com/privacy-policy/ | Innersloth LLC | https://www.innersloth.com/privacy-policy/ | innersloth.com |
| apple | Mojang | https://www.microsoft.com/en-us/privacy/privacystatement | Microsoft Corporation | https://www.microsoft.com/en-us/privacy/privacystatement | microsoft.com |
| apple | AI Games FZ | https://aigames.ae/policy#privacy | CASUAL AZUR GAMES | https://www.aigames.ae/policy | aigames.ae |
| apple | Amanotes Pte. Ltd. | https://www.amanotes.com/privacy-policy | AMANOTES PTE. LTD. | https://www.amanotes.com/privacy-policy | amanotes.com |
| apple | Viber Media SARL. | https://www.viber.com/en/terms/viber-privacy-policy/ | Viber Media | https://www.viber.com/en/terms/viber-privacy-policy/ | viber.com |
| android | Azur Interactive Games Limited | https://azurgames.com/privacy-policy/ | Azur Interactive Games Limited | https://azurgames.com/privacy-policy/ | azurgames.com |
| android | VPN Super Inc | https://vpnsuper.com/privacy-notice | Mobile Jump Pte Ltd | https://vpnsuper.com/privacy-notice | vpnsuper.com |
| android | Crunchyroll, LLC | https://www.sonypictures.com/corp/privacy.html | Crunchyroll, LLC | https://www.sonypictures.com/corp/privacy.html | sonypictures.com |
| android | Easybrain | https://easybrain.com/privacy | Easybrain Ltd | https://easybrain.com/privacy | easybrain.com |
| apple | Supercent, Inc. | https://supercent.io/PrivacyPolicy | Supercent, Inc. | https://supercent.io/PrivacyPolicy | supercent.io |
| apple | Glassdoor | https://hrtechprivacy.com/brands/glassdoor | Indeed Inc. | https://hrtechprivacy.com/brands/indeed#privacypolicy | hrtechprivacy.com |
| apple | Etermax | https://www.etermax.com/privacy | etermax | https://www.etermax.com/privacy | etermax.com |
| apple | SayGames LTD | https://say.games/privacy-policy | SayGames Ltd | https://say.games/privacy-policy | say.games |
| android | Mivo studio | http://res.ufotosoft.com/aboutus/src/policy.snap.html | Selfie Camera & Photo Editor & Beauty Snap | http://res.ufotosoft.com/aboutus/src/selfie.policy.html | ufotosoft.com |
| android | DS tools | https://sites.google.com/view/proxy-browser-privacy-policy/ | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| android | ixigo - IRCTC Authorised Partner, Flight Tickets | https://www.iubenda.com/privacy-policy/696667 | JindoBlu | https://www.iubenda.com/privacy-policy/96847333 | iubenda.com |
| android | Tubi TV | https://tubitv.com/static/privacy | Tubi, Inc | https://tubitv.com/static/privacy | tubitv.com |
| apple | First Touch Games Ltd. | https://www.ftgames.com/privacy-policy | First Touch Games Ltd. | https://www.ftgames.com/privacy-policy | ftgames.com |
| android | Ketchapp | https://www.ubisoft.com/legal/documents/privacypolicy/en-US | Ubisoft Entertainment | https://www.ubisoft.com/legal/documents/privacypolicy/en-US | ubisoft.com |
| apple | NETGEAR | https://www.netgear.com/about/privacy-policy/ | netgear.com | https://www.netgear.com:443/about/privacy-policy/ | netgear.com |
| apple | AOL Media LLC | https://legal.yahoo.com/us/en/yahoo/privacy/index.html | Yahoo | https://legal.yahoo.com/us/en/yahoo/privacy/index.html | yahoo.com |
| apple | Wattpad Corp | https://policies.wattpad.com/privacy/ | Wattpad.com | https://policies.wattpad.com/privacy/ | wattpad.com |
| android | AI Dreamweaver | http://res.ufotosoft.com/aboutus/src/policy.beat.html | Selfie Camera & Photo Editor & Beauty Snap | http://res.ufotosoft.com/aboutus/src/selfie.policy.html | ufotosoft.com |
| android | Samsung Electronics Co. Ltd | https://www.samsung.com/in/info/privacy/ | Samsung R&D Institute India Noida | https://www.samsung.com/in/info/privacy/ | samsung.com |
| apple | Alibaba | https://terms.alicdn.com/legal-agreement/terms/suit_bu1_aliexpress/suit_bu1_aliexpress201909171350_82407.html | UCWeb Singapore Pte. Ltd. | https://terms.alicdn.com/legal-agreement/terms/suit_bu1_uc/suit_bu1_uc202007241608_71682.html | alicdn.com |
| apple | Brave Software | https://brave.com/privacy/browser/ | brave.com | https://brave.com/privacy/browser/ | brave.com |
| android | Metro by T-Mobile | https://www.t-mobile.com/privacy-center/privacy-notices/t-mobile-privacy-notice | T-Mobile | https://www.t-mobile.com/privacy-center/privacy-notices/t-mobile-privacy-notice | t-mobile.com |
| android | Popcore Games | https://www.take2games.com/privacy/en-US/ | Peak Games | https://www.take2games.com/privacy/en-US/ | take2games.com |
| apple | LinkedIn Corporation | https://www.linkedin.com/legal/privacy-policy | linkedin.com | https://www.linkedin.com/legal/privacy-policy/ | linkedin.com |
| apple | BERESNEV s.r.o. | https://beresnev.games/en/privacyPolicy | Beresnev Games | https://beresnev.games/en/privacyPolicy | beresnev.games |
| apple | Ubisoft | https://www.ubisoft.com/legal/documents/privacypolicy/en-US | Ubisoft Entertainment | https://www.ubisoft.com/legal/documents/privacypolicy/en-US | ubisoft.com |
| android | Flo Health Inc. | https://flo.health/privacy-policy | FLO HEALTH UK LIMITED | https://flo.health/privacy-policy | flo.health |
| apple | Versant Media LLC | https://www.versantprivacy.com/privacy | Fandango | https://www.versantprivacy.com/privacy | versantprivacy.com |
| android | Signal Foundation | https://signal.org/legal/#privacy-policy | Signal Messenger, LLC | https://signal.org/legal/ | signal.org |
| android | Shree Ganesha Labs | https://sites.google.com/view/shreeganeshalabsprivacypolicy/home | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| apple | Freeplay LLC | https://freeplay.io/games/ios/privacy-policy/ | Freeplay Inc | https://freeplay.io/games/android/privacy-policy/ | freeplay.io |
| apple | Fox News Network, LLC | https://www.foxnews.com/privacy-policy | foxnews.com | https://www.foxnews.com/privacy-policy | foxnews.com |
| android | Rollic Games | https://www.take2games.com/privacy/en-US/ | Peak Games | https://www.take2games.com/privacy/en-US/ | take2games.com |
| android | UUTEAM Technology Limited-Dragon Inc. | https://sites.google.com/site/bubbleshooterdragonpop/ | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| android | Gamexis | https://gamexis.com/privacy-policy/ | GAMEXIS | https://gamexis.com/privacy-policy/ | gamexis.com |
| android | Audiomack Music Apps | https://audiomack.com/about/privacy-policy | Audiomack, Inc. | https://audiomack.com/about/privacy-policy | audiomack.com |
| android | Sony Entertainment Network | https://www.playstation.com/en-us/legal/privacy-policy/ | playstation.com | https://www.playstation.com/en-us/legal/privacy-policy/ | playstation.com |
| web | microsoft.com | https://www.microsoft.com/en-us/privacy/privacystatement | Microsoft Corporation | https://www.microsoft.com/en-us/privacy/privacystatement | microsoft.com |
| web | office.com | https://www.microsoft.com/en-us/privacy/privacystatement | Microsoft Corporation | https://www.microsoft.com/en-us/privacy/privacystatement | microsoft.com |
| web | office.com | https://www.microsoft.com/en-us/privacy/privacystatement | Microsoft Corporation | https://www.microsoft.com/en-us/privacy/privacystatement | microsoft.com |
| web | azure.com | https://www.microsoft.com/en-us/privacy/privacystatement | Microsoft Corporation | https://www.microsoft.com/en-us/privacy/privacystatement | microsoft.com |
| web | bing.com | https://www.microsoft.com/en-us/privacy/privacystatement | Microsoft Corporation | https://www.microsoft.com/en-us/privacy/privacystatement | microsoft.com |
| web | netflix.com | https://help.netflix.com/legal/privacy | Netflix, Inc. | https://help.netflix.com/legal/privacy | netflix.com |
| web | skype.com | https://www.microsoft.com/en-us/privacy/privacystatement | Microsoft Corporation | https://www.microsoft.com/en-us/privacy/privacystatement | microsoft.com |
| web | nginx.com | https://www.f5.com/company/policies/privacy-notice | f5.com | https://www.f5.com/company/policies/privacy-notice | f5.com |
| web | android.com | https://policies.google.com/privacy | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| web | shopify.com | https://www.shopify.com/legal/privacy | Shopify Inc. | https://www.shopify.com/legal/privacy/consumers | shopify.com |
| web | telegram.org | https://telegram.org/privacy | Telegram FZ-LLC | https://telegram.org/privacy | telegram.org |
| web | googleblog.com | https://policies.google.com/privacy | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| web | mi.com | https://www.mi.com/us/about/privacy/ | Mi Music | https://privacy.mi.com/all/en_US | mi.com |
| web | supercell.com | https://supercell.com/en/privacy-policy/ | Supercell | https://supercell.com/en/privacy-policy/ | supercell.com |
| web | cnbc.com | https://www.versantprivacy.com/privacy | Fandango | https://www.versantprivacy.com/privacy | versantprivacy.com |
| web | google.de | https://policies.google.com/privacy?hl=en&fg=1 | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| web | eventbrite.com | https://www.eventbrite.com/help/en-us/articles/460838/eventbrite-privacy-policy/ | Eventbrite | https://www.eventbrite.com/help/en-us/articles/460838/eventbrite-privacy-policy/ | eventbrite.com |
| web | wps.com | https://www.wps.com/privacy-policy/ | WPS SOFTWARE PTE. LTD. | https://www.wps.com/privacy-policy/ | wps.com |
| web | atlassian.com | https://www.atlassian.com/legal/privacy-policy | atlassian.net | https://www.atlassian.com/legal/privacy-policy | atlassian.com |
| web | stackadapt.com | https://policies.google.com/privacy | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| web | cbsnews.com | https://privacy.paramount.com/en/policy | Pluto.tv | https://privacy.paramount.com/en/policy | paramount.com |
| web | viber.com | https://www.viber.com/en/terms/viber-privacy-policy/ | Viber Media | https://www.viber.com/en/terms/viber-privacy-policy/ | viber.com |
| web | uber.com | https://www.uber.com/global/en/privacy-notice-riders-order-recipients/ | Uber Technologies, Inc. | https://www.uber.com/global/en/privacy-notice-riders-order-recipients/ | uber.com |
| web | google.co.uk | https://policies.google.com/privacy?hl=en&fg=1 | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| web | mlb.com | https://www.mlb.com/official-information/privacy-policy | MLB | https://www.mlb.com/official-information/privacy-policy | mlb.com |
| web | wattpad.com | https://policies.wattpad.com/privacy/ | Wattpad.com | https://policies.wattpad.com/privacy/ | wattpad.com |
| web | discordapp.com | https://discord.com/privacy | discord.com | https://discord.com/privacy | discord.com |
| web | liftoff.io | https://liftoff.ai/privacy-policy/ | vungle.com | https://liftoff.ai/privacy-policy/ | liftoff.ai |
| web | xbox.com | https://www.microsoft.com/en-us/privacy/privacystatement | Microsoft Corporation | https://www.microsoft.com/en-us/privacy/privacystatement | microsoft.com |
| web | nbcnews.com | https://www.nbcuniversalprivacy.com/privacy?intake=NBC_News | Peacock TV LLC | https://www.nbcuniversalprivacy.com/privacy?brandA=Peacock&intake=Peacock | nbcuniversalprivacy.com |
| web | flipkart.com | https://www.flipkart.com/pages/privacypolicy?otracker=footer_navlinks | Flipkart | https://www.flipkart.com/pages/privacypolicy | flipkart.com |
| web | mailchi.mp | https://www.intuit.com/privacy/statement/ | mailchimp.com | https://www.intuit.com/privacy/statement/ | intuit.com |
| web | nationalgeographic.com | https://privacy.thewaltdisneycompany.com/en/current-privacy-policy/ | Disney | https://privacy.thewaltdisneycompany.com/en/current-privacy-policy/ | thewaltdisneycompany.com |
| web | t-mobile.com | https://www.t-mobile.com/privacy-center/privacy-notices/t-mobile-privacy-notice | T-Mobile | https://www.t-mobile.com/privacy-center/privacy-notices/t-mobile-privacy-notice | t-mobile.com |
| web | t-mobile.com | https://www.t-mobile.com/privacy-center/privacy-notices/t-mobile-privacy-notice | T-Mobile | https://www.t-mobile.com/privacy-center/privacy-notices/t-mobile-privacy-notice | t-mobile.com |
| web | auth0.com | https://www.okta.com/legal/privacy-policy/ | okta.com | https://www.okta.com/legal/privacy-policy/ | okta.com |
| web | google.fr | https://policies.google.com/privacy?hl=en&fg=1 | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| web | google.ca | https://policies.google.com/privacy?hl=en&fg=1 | google.com | https://policies.google.com/privacy?hl=en&fg=1 | google.com |
| web | letsencrypt.org | https://letsencrypt.org/privacy/ | lencr.org | https://letsencrypt.org/privacy/ | letsencrypt.org |
| web | cricbuzz.com | https://www.cricbuzz.com/info/privacy-til | Cricbuzz.com | https://www.cricbuzz.com/info/privacy | cricbuzz.com |
| web | cricbuzz.com | https://www.cricbuzz.com/info/privacy | Cricbuzz.com | https://www.cricbuzz.com/info/privacy | cricbuzz.com |

## Policy domain differs from organization domain

`policy_domain_mismatches.tsv`; organization domain is the site, developerWebsite, or sellerUrl when present.

| ID | Organization | Organization domain | Policy domain | Final policy URL |
| --- | --- | --- | --- | --- |
| android-001 | Microsoft Corporation | aka.ms | microsoft.com | https://www.microsoft.com/en-us/privacy/privacystatement |
| web-003 | twitter.com | twitter.com | x.com | https://x.com/en/privacy |
| android-003 | Snap Inc | snapchat.com | snap.com | https://values.snap.com/privacy/privacy-policy?lang=en-US |
| android-008 | Smart Media4U Technology Pte.Ltd. | ushareit.com | wshareit.com | https://web.wshareit.com/cdn/shareit/w/privacy/pr_en.html |
| android-009 | King | candycrush.com | king.com | https://www.king.com/privacyPolicy |
| apple-009 | Apple | shazam.com | apple.com | https://www.apple.com/legal/privacy/en-ww/ |
| web-011 | b-cdn.net | b-cdn.net | bunny.net | https://bunny.net/privacy/ |
| web-015 | lencr.org | lencr.org | letsencrypt.org | https://letsencrypt.org/privacy/ |
| android-016 | Gametion | gametion.com | gametionglobal.com | https://www.gametionglobal.com/privacypolicy.htm |
| apple-017 | Shopify Inc. | shop.app | shopify.com | https://www.shopify.com/legal/privacy/consumers |
| apple-018 | Crumbl, LLC | crumbl.com | crumblcookies.com | https://crumblcookies.com/privacy |
| web-022 | ubuntu.com | ubuntu.com | canonical.com | https://canonical.com/legal/data-privacy |
| android-027 | UCWeb Singapore Pte. Ltd. | ucweb.com | alicdn.com | https://terms.alicdn.com/legal-agreement/terms/suit_bu1_uc/suit_bu1_uc202007241608_71682.html |
| android-029 | Visha Group | vishavideo.com | shalltry.com | https://visha-cdn.shalltry.com/language/en/privacy-policy.html |
| apple-030 | Disney | espn.com | thewaltdisneycompany.com | https://privacy.thewaltdisneycompany.com/en/current-privacy-policy/ |
| android-032 | LINE (LY Corporation) | line.me | lycorp.co.jp | https://www.lycorp.co.jp/en/company/privacypolicy/ |
| apple-032 | Indeed Inc. | indeed.com | hrtechprivacy.com | https://hrtechprivacy.com/brands/indeed#privacypolicy |
| apple-033 | Supercell | supercellsupport.com | supercell.com | https://supercell.com/en/privacy-policy/ |
| web-034 | vungle.com | vungle.com | liftoff.ai | https://liftoff.ai/privacy-policy/ |
| apple-034 | Peacock TV LLC | peacocktv.com | nbcuniversalprivacy.com | https://www.nbcuniversalprivacy.com/privacy?brandA=Peacock&intake=Peacock |
| web-035 | rubiconproject.com | rubiconproject.com | magnite.com | https://www.magnite.com/legal/magnite-website-privacy-policy/ |
| android-035 | InShot Video Editor | inshot.com | inshotapp.com | https://inshotapp.com:443/website/InShotAndroid/privacypolicy.html |
| apple-039 | Episode Interactive | pocketgems.com | episodeinteractive.com | https://home.episodeinteractive.com/privacy |
| apple-040 | Peak Games | peak.com | take2games.com | https://www.take2games.com/privacy/en-US/ |
| apple-042 | Instructure Inc. | canvaslms.com | instructure.com | https://www.instructure.com/policies/product-privacy-policy |
| web-043 | weebly.com | weebly.com | squareup.com | https://squareup.com/us/en/legal/general/privacy |
| android-046 | PLAYIT TECHNOLOGY PTE. LTD. | playit.app | playit2019.com | http://www.playit2019.com/privacy.html |
| apple-047 | The Chamberlain Group, Inc. | chamberlaingroup.com | liftmaster.com | https://www.liftmaster.com/privacy-notice |
| apple-051 | Fandango | fandango.com | versantprivacy.com | https://www.versantprivacy.com/privacy |
| android-056 | Bending Spoons | remini.ai | bendingspoons.com | https://support.bendingspoons.com/privacy?app=1470373330 |
| web-064 | grammarly.com | grammarly.com | superhuman.com | https://superhuman.com/legal/privacy-policy |
| android-065 | QuVideo Inc. Video Editor & Video Maker App | vivavideo.tv | veresource.com | https://rc.veresource.com/web/h5template/53fe22d0-604e-476a-b20e-c4b3bcbcbaf7-language=en/dist/index.html |
| apple-066 | Cardinal Blue | piccollage.com | picc.co | https://picc.co/privacy |
| android-067 | Innovative Connecting | turbovpn.co | turbovpn.com | https://turbovpn.com/policy |
| web-068 | mozilla.com | mozilla.com | mozilla.org | https://www.mozilla.org/en-US/privacy/firefox/ |
| apple-069 | Candywriter, LLC | candywriter.com | candywriter.net | http://www.candywriter.net/ppolicy.pdf |
| web-070 | speedtest.net | speedtest.net | ookla.com | https://www.ookla.com/privacy |
| android-073 | Real Freestyle Soccer | soccer-star-52646070.firebaseapp.com | simface.com | https://www.simface.com/privacy-policy/ |
| web-074 | atlassian.net | atlassian.net | atlassian.com | https://www.atlassian.com/legal/privacy-policy |
| apple-077 | Pluto.tv | pluto.tv | paramount.com | https://privacy.paramount.com/en/policy |
| android-078 | TeaCapps | teacapps.com | qrbot.net | https://app.qrbot.net/privacy.html |
| apple-079 | iconic hearts holdings, inc. | iconichearts.com | getsendit.com | https://www.getsendit.com/privacy |
| android-080 | NEKKI | shadowfight2.com | nekki.com | https://nekki.com/privacy_policy/ |
| apple-080 | Crunchyroll, LLC | crunchyroll.com | sonypictures.com | https://www.sonypictures.com/corp/privacy.html |
| web-086 | wired.com | wired.com | condenast.com | https://www.condenast.com/privacy-policy |
| apple-087 | BPMobile | bpmobile.com | iscanner.com | https://iscanner.com/mobileapp/privacy/en/ |
| apple-090 | The Grizzly Labs | thegrizzlylabs.com | geniusscan.com | https://help.geniusscan.com/security-and-privacy/privacy-policy |
| apple-092 | Parkmobile USA, Inc. | vimeo.com | parkmobile.io | https://parkmobile.io/legal/privacy-policy |
| apple-096 | Albertsons Companies, LLC | safeway.com | albertsonscompanies.com | https://www.albertsonscompanies.com:443/policies-and-disclosures/privacy-policy/default.aspx |
| android-099 | iKame Games - Zego Studio | ikameglobal.com | zegostudio.com | https://zegostudio.com/privacy-policy.html |
| android-103 | JindoBlu | jindoblu.com | iubenda.com | https://www.iubenda.com/privacy-policy/96847333 |
| android-107 | VIDEOSHOW Video Editor & Maker & AI Chat Generator | videoshowapp.com | d10nkoc3mu17gd.cloudfront.net | https://d10nkoc3mu17gd.cloudfront.net/privacy/VideoShow_Privacy_Policy_en.html |
| android-108 | mAst App 2026 | mastinapp.com | vllresource.com | https://mast-rc.vllresource.com/web/h5template/8856fffc-01fe-4b8c-aa82-aca1e8759aaa-language=en/dist/index.html |
| apple-114 | Kaiser Permanente | kp.org | kaiserpermanente.org | https://healthy.kaiserpermanente.org/privacy |
| web-115 | bugsnag.com | bugsnag.com | smartbear.com | https://smartbear.com/privacy/ |
| web-118 | mailchimp.com | mailchimp.com | intuit.com | https://www.intuit.com/privacy/statement/ |
| apple-118 | Monkey Taps | motivation.app | monkeytaps.net | https://monkeytaps.net/privacy |
| android-119 | Elokence SAS | elokence.com | akinator.com | https://en.akinator.com/app/privacy/en |
| apple-123 | Tile, Inc. | tile.com | life360.com | https://legal.corp.life360.com/hc/en-us/articles/16038777217175-Life360-Privacy-Policy |
| apple-124 | General Motors Company | chevrolet.com | onstar.com | https://www.onstar.com/content/dam/onstar/na/us/en/index/legal/legal-privacy-statement-jan012011/02-pdfs/Privacy-Statement-for-Application-Services.pdf |
| android-125 | go live llc | gomo.com | gomocdn.com | http://resource.gomocdn.com/GOMO_Limited/GOLauncher_privacy.html |
| apple-128 | Appchi Media Ltd | quickhitslot.com | sciplay.com | https://www.sciplay.com/terms-of-service#!/privacy |
| android-129 | STORYMATRIX | dramabox.com | dramaboxdb.com | https://support.dramaboxdb.com/privacy.html |
| web-130 | prnewswire.com | prnewswire.com | cision.com | https://privacy.cision.com/dataprivacynotice_customersprospects |
| android-130 | Adaric Music | musicgamestudio.top | adaric.com | https://adaric.com/BeatFirePolicy.html |
| android-131 | Hippo Lab | snakelite.fun | soonistudio.com | https://soonistudio.com/privacy-policy-en.html |
| apple-131 | PlayStudios | brainium.com | playstudios.com | https://www.playstudios.com/privacy-notice/ |
| android-133 | NewLeaf Publishing | reelshort.com | crazymaplestudios.com | https://crazymaplestudios.com/v/privacy-agreement.html |
| web-135 | theverge.com | theverge.com | pmc.com | https://www.pmc.com/privacy-policy |
| android-135 | Hazel Mobile Games | standardgamesstudio.com | gameswing.io | https://gameswing.io/hazelmobile.html |
| android-138 | Unicorn Studio Official | ctctechltd.com | unicornstudio.online | https://unicornstudio.online/policy.html |
| web-142 | stackexchange.com | stackexchange.com | stackoverflow.com | https://stackoverflow.com/legal/privacy-policy |
| android-143 | Play Piknik | playpiknik.com | sagomini.com | https://sagomini.com/privacy-policy/ |
| apple-144 | Kolibri Games GmbH | idleminertycoon.com | kolibrigames.com | https://www.kolibrigames.com/privacy-policy/ |
| android-149 | LBE Tech | app-ads-o54l6ix4xq-uw.a.run.app | parallelspace-app.com | https://www.parallelspace-app.com/static/page/privacy_policy_en.html |
| android-150 | bittorrent.com | utorrent.com | bittorrent.com | https://www.bittorrent.com/legal/privacy-policy/ |
| android-154 | State Bank of India | bank.sbi | sbi.bank.in | https://onlinesbi.sbi.bank.in/sbijava/Privacy_Statement.html |
| apple-158 | FitNow | loseit.com | fitnowinc.com | https://www.fitnowinc.com/privacy/loseit/ |
| apple-159 | Cross Forward Consulting, LLC | widgetsmith.app | david-smith.org | https://david-smith.org/widgetsmith_privacy.html |
| android-160 | Deca Games | decagames.com | zombiecatchers.com | https://zombiecatchers.com/privacy/ |
| apple-163 | Outside Television Inc | mapmyrun.com | outsideinc.com | https://www.outsideinc.com/privacy-policy/ |
| web-164 | bidmachine.io | bidmachine.io | bidmachine.com | https://www.bidmachine.com/privacy-policy |
| apple-168 | DEEP FLOW SOFTWARE SERVICES | codeway.co | cleanup.photos | https://cleanup.photos/privacy |
| web-177 | meethue.com | meethue.com | philips-hue.com | https://www.philips-hue.com/en-us/support/legal/privacy-policy |
| web-181 | economist.com | economist.com | economistgroup.com | https://www.economistgroup.com/privacy-policy |
| apple-182 | Jo-Ann Stores, Inc. | joann.com | michaels.com | https://www.michaels.com/your-privacy-rights?joannweb |
| android-185 | AXLEBOLT LTD | axlebolt.com | standoff2.com | https://standoff2.com/en/privacy-policy.html |
| android-187 | Mediocre | smashhitgame.com | mediocre.se | https://mediocre.se/privacy_policy.html |
| apple-187 | Raketspel AB | voodoo.io | raketspel.se | http://raketspel.se/privacy.html |
| apple-188 | Readdle Technologies Limited | documents.io | readdle.com | https://readdle.com/documents/legal/privacy |
| android-194 | Vuclip Mobile Video | viu.com | pccw.com | https://www.pccw.com/privacy-statement/for-customers/index.page?locale=en |
| android-195 | Yarsa Games | yarsagames.com | yarsalabs.com | https://www.yarsalabs.com/policies/privacy-policy/ |
| apple-200 | Locket Labs, Inc. | locket.com | locket.camera | https://locket.camera/privacy |
