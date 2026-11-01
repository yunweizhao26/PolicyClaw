=== ITEM p0226
rule 1: {"polarity": "ALLOW", "actor": "", "action": "collected (operation: collection)", "data": "some categories of data that may be deemed to be sensitive personal information in certain jurisdictions", "recipient": "", "source": "", "purpose": "", "condition": "as a result of your interaction with Glance AI and its features on Glance", "condition_predicate": "event.interact_with_glance_ai"}
rule 2: {"polarity": "DENY", "actor": "Glance", "action": "collect (operation: collection)", "data": "Sensitive Personal Information", "recipient": "", "source": "", "purpose": "", "condition": "unless some categories of data that may be deemed to be sensitive personal information in certain jurisdictions may be collected as a result of your interaction with Glance AI and its features on Glance", "condition_predicate": "NOT event.interact_with_glance_ai"}
--- section of rule 1 and rule 2
Additional Privacy Rights for Residents of certain countries or states which provide such rights
the right to know what categories of personal information Glance has collected about them, whether Glance disclosed that personal information for a business purpose (e.g., to a service provider), whether Glance “sold” that personal information, and whether Glance “shared” that personal information for “cross-context behavioral advertising” in the preceding 12 months. Such residents can find this information below:
Category of Personal Information Collected by Glance
Category of Third Parties to Whom Personal Information is Disclosed for a Business Purpose
Category of Third Parties to Whom Personal Information is Sold and/or Shared
Login Information.
Information provided on account creation
Group
NA
Identifiers.
Unique personal identifier, online identifier or other similar identifiers.
Group
Advertising networks including the Group
Data analytics providers including the Group.
Internet or other electronic network activity
Information on a consumer's interaction with Glance application and advertisements on Glance.
Group
Advertising networks including the Group
Geolocation data
General area inferred from IP address.
Group
Service providers
N/A
Inferences drawn from other personal information
User’s past interactions
Group
Advertising networks including the Group
According to certain regulation(s) that may be applicable to you, some of the aforementioned activities may be deemed to be “selling” or “sharing” your personal information to provide you with “cross-context behavioral advertising”.
For more information related to categories of information collected, disclosed and shared/sold for the creation of AI Looks via Glance AI, please refer to the
Glance AI App Privacy Policy
.
“Opting Out of “Sales” of Personal Information and/or “Sharing” for Cross-Context Behavioral Advertising under the CCPA.
California residents have the right to opt out of the “sale” of personal information and the “sharing” of personal information for “cross-context behavioural advertising.” California residents may exercise these rights by clicking on “Do not Sell or Share My Personal Information” or contacting us as set forth in “
Contact Information
” below.
Disclosure Regarding Individuals Under the Age of 18.
Glance does not have actual knowledge of any “sale” of personal information of minors under 18 years of age. Glance does not have actual knowledge of any “sharing” of personal information of minors under 16 years of age for “cross-context behavioral advertising.”
Disclosure Regarding Sensitive Personal Information
Glance does not collect or process Sensitive Personal Information.
Please note that some categories of data that may be deemed to be sensitive personal information in certain jurisdictions may be collected as a result of your interaction with Glance AI and its features on Glance. For more information related to such categories of information collected, disclosed and shared/sold for the creation of AI Looks via Glance AI, please refer to the
Glance AI App Privacy Policy
.
Non-Discrimination.
California residents have the right not to receive discriminatory treatment by us for the exercise of their rights conferred by the CCPA.
If you are a California resident and would like to exercise any of your rights under the CCPA, please reach out to us as set forth in “
Contact Information
” section.We will process such requests in accordance with applicable laws.
Refer-a-Friend and Similar Incentive Programs
As described above in “
How We Use Your Information
” (“Share Content with Friends or Colleagues”), we may offer referral programs or other incentivized data collection programs.
=== END ITEM p0226

=== ITEM p0227
rule 1: {"polarity": "ALLOW", "actor": "Headspace", "action": "collect (operation: collection)", "data": "personal information described in Section 1 and as categorized in the table within Section 10(b) above", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "collect (operation: collection)", "data": "personal information", "recipient": "", "source": "individuals under that age", "purpose": "", "condition": "from individuals under that age; unless if you are a parent under a supported employee assistance program (EAP), you may refer your child of at least 6 years old to our Care Providers for in-person care but cannot create an app account for them", "condition_predicate": "((user.age < 13 OR [untranslated: the equivalent age in your jurisdiction]) AND NOT (user.parental_consent AND [untranslated: you are a parent under a supported employee assistance program (EAP)] AND user.age >= 6))"}
--- section of rule 1
OCPA
”). This section is intended to comply with these laws by supplementing the information provided elsewhere in the Privacy Policy.
Collection of personal information.
Headspace may collect the personal information described in Section 1 and as categorized in the table within Section 10(b) above. Please note that some of this personal information will be considered sensitive under your state’s legal definition which can vary across different states. The personal information we may collect depending on how you use our Platform includes mental or physical health information, racial or ethnic origin, and information about sexual orientation or gender identity.
Use of personal information.
Headspace may collect, use, or disclose personal information about US state residents for purposes listed in Section 2 of our Privacy Policy. We use sensitive personal information for the same purposes except for personalizing ads.
Disclosure of personal information.
We may disclose your personal information to the categories of service providers and third parties identified in Section 3 of this Privacy Policy, and in ways that are described in that section.
Your privacy rights.
We generally provide the privacy rights described in Section 5 above to you regardless of your location. Your state may afford you additional privacy rights as noted below. To exercise your right, see the contact information in Section 9 or follow the instructions below for specific state rights. We will respond to your verifiable request within the time limit afforded under applicable law. Exceptions may still apply as described in Section 5.
Residents of Colorado, Connecticut, Delaware, Kentucky, Maryland, Virginia, Utah, Minnesota, Rhode Island, and Oregon have the right to opt out of targeted advertising and sales. If you are a resident of these states, you may opt out by following this link (
Your privacy choices
) and, if you are an Apps user, by going to
the My Data page here
or within your mobile app settings.
For users in Colorado, Connecticut and Virginia, you may opt out of profiling in furtherance of decisions that produce legal or similarly significant effects. While you may still make this request, Headspace does not currently use profiling in this manner.
Nevada provides its residents a limited right to opt out of the sale of personal information. Please know that we do not trigger this requirement because we do not sell your personal information for payment.
Residents in Minnesota and Oregon may obtain a list of the specific third parties to whom we may disclose your personal information. General information about these third parties is available in Section 3. You can make this request using the contact information in Section 9.
The RIDTPA entitles Rhode Island residents to know the third parties to which we sell or may sell their personal information. Headspace does not sell personal information for payment but, like with the CCPA in Section 10b, a “sale” under the RIDTPA can include sharing personal information for targeted advertising. Under that definition, we have shared personal information, which may include yours, to the third parties listed
here
.
--- section of rule 2
6. Children’s privacy
At Headspace, we are committed to protecting and respecting children’s privacy. Our Platform is not intended for individuals below 13 years old or the equivalent age in your jurisdiction. We do not intentionally collect personal information from individuals under that age. There is a limited exception if you are a parent under a supported employee assistance program (EAP), you may refer your child of at least 6 years old to our Care Providers for in-person care but cannot create an app account for them.
If you are a parent or guardian and you are aware that a child under age 13, or equivalent age in your jurisdiction, has provided us with their personal information without parental consent, please contact us at
help@headspace.com
and we will take steps to remove that personal information from our servers.
=== END ITEM p0227

=== ITEM p0228
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "handle (operation: processing)", "data": "your personal data", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "process (operation: processing)", "data": "your personal data", "recipient": "", "source": "", "purpose": "", "condition": "based on this consent in the future; Where we rely on consent you can withdraw your consent to the processing of your personal data by us at any time. As a result", "condition_predicate": "(basis.consent AND basis.consent)"}
--- section of rule 1
User Privacy Notice
At eBay, we take protecting your personal data seriously, and we believe you should know what data we collect and how we use it.
This User Privacy Notice brings together all the essential details about how we handle your personal data and your rights in connection with it. We want you to feel confident using eBay—knowing that your information is handled responsibly, securely, and in line with applicable privacy laws.
We're committed to being open about our practices and giving you meaningful control over your personal data. Understanding how we use your information helps you make informed choices about your relationship with eBay and the Services you use.
This User Privacy Notice is effective from
November 26, 2026
.
--- section of rule 2
6. Your privacy rights and how to use them
Subject to possible restrictions under national law, as a data subject, you have the right to access, rectification, erasure, restriction of processing and data portability with regard to your personal data. In addition, you can withdraw your consent and
object
to our processing of your personal data on the basis of our legitimate interests. You can also lodge a complaint with a supervisory authority.
Your rights in detail:
Where we rely on consent you can
withdraw your consent
to the processing of your personal data by us at any time. As a result, we may no longer process your personal data based on this consent in the future. The withdrawal of consent has no effect on the lawfulness of processing based on consent before its withdrawal.
You have the right to obtain
access
to your personal data that is being processed by us. In particular, you may request information on the purposes of the processing, the categories of personal data concerned, the categories of recipients to whom the personal data have been or will be disclosed, where possible the envisaged period for which the personal data will be stored or the criteria used to determine that period, the existence of the right to request rectification or erasure of personal data or restriction of processing of personal data or to object to such processing, the right to lodge a complaint with a supervisory authority, any available information as to the personal data's source (where they are not collected from you), the existence of automated decision-making, including profiling and, where appropriate, meaningful information on its details. Your right to access shall not adversely affect the rights and freedoms of others. Your right to access may be limited by national law.
You have the right to obtain from us without undue delay the
rectification
of inaccurate personal data concerning you. Taking into account the purposes of the processing, you have the right to have incomplete personal data completed, including by means of providing a supplementary statement.
You have the right to obtain from us the
erasure
of personal data concerning you under certain conditions (e.g. when the personal data are no longer necessary in relation to the purposes for which they were processed or when they are no longer required for overriding legitimate grounds, such as the detection/prevention of fraud), unless processing is necessary for exercising the right of freedom of expression and information, for compliance with a legal obligation, for reasons of public interest or for the establishment, exercise or defense of legal claims. The right to erasure may be limited by national law. Please note that it is not possible to erase data from the blockchain. Please see
section 10
for further information.
You have the right to request that we
restrict the processing of your personal data
to the extent that
the accuracy of the data is disputed by you,
the processing is unlawful, but you oppose the erasure of the personal data,
we no longer need the data, but you need it to assert, exercise or defend legal claims or
you have objected to the processing.
You have the right to receive the personal data concerning you, which you have provided to us, in a structured, commonly used and machine-readable format and have the right to transmit those data to another controller ("
right to data portability
").
You have the right to lodge a complaint with a
supervisory authority
. For example, you can contact the supervisory authority of your usual place of residence, your place of work or the registered office of the
controller
.
If your personal data is processed on the basis of our legitimate interests, you have the
right to object
to the processing of your personal data on grounds relating to your particular situation. This also applies to profiling.
=== END ITEM p0228

=== ITEM p0229
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "processing (operation: use)", "data": "Personal Information", "recipient": "", "source": "", "purpose": "for “targeted advertising” purposes", "condition": "unless opt you out of the “sale” or processing of Personal Information for “targeted advertising” purposes; right to restrict our processing", "condition_predicate": "(NOT (opt_out.sale OR opt_out.targeted_ads) AND NOT request.restrict_processing)"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "use (operation: use)", "data": "sensitive personal information", "recipient": "", "source": "", "purpose": "for any purpose not expressly permitted by applicable law", "condition": "unless expressly permitted by applicable law", "condition_predicate": "NOT law.permitted"}
--- section of rule 1
HERE
. To opt-out of other forms of marketing (such as postal marketing or telemarketing), please contact us using the contact details provided under the "
How to Contact Us
" heading below.
Similarly, if we have collected and process your personal information with your consent, then you can
withdraw your consent
at any time. Withdrawing your consent will not affect the lawfulness of any processing we conducted prior to your withdrawal, nor will it affect processing of your personal information conducted in reliance on lawful processing grounds other than consent.
You have the
right to complain to a data protection authority
about our collection and use of your personal information. For more information, please contact your local data protection authority.
To appeal
our denial of a request you have made under applicable law, you may contact us using the contact details provided under the "How to Contact Us" heading below. Please enclose a copy of, or otherwise specifically reference, our decision on your request, so that we may adequately address your appeal. We will respond to your appeal in accordance with applicable law.
We recognize the law in California enables residents to
limit the use or disclosure of their “sensitive personal information
” (as defined in the CCPA) if it is used for certain purposes. In the limited circumstances that we process sensitive personal information as defined by the CCPA, we do not use or disclose it other than for disclosed and permitted business purposes for which there is not a right to limit under the CCPA.
We do not sell personal information in the traditional sense (i.e., for money). However, some laws define “sale” and “targeted advertising” broadly which may include some types of personalized advertising and analytics. Such laws allow residents to
opt you out of the “sale” or processing of Personal Information for “targeted advertising” purposes
. We enable all US residents to exercise this right, and non-US residents can use the similar right to restrict our processing
--- section of rule 2
Inferences:
This includes information inferred from any of the personal information listed above to create a profile or summary about, for example, an individual’s preferences and characteristics.
Sensitive personal information, as defined in the California Consumer Privacy Act (CCPA):
This includes your NETGEAR account login (such as to the MyNETGEAR, NETGEAR Academy, or Meural platforms), in combination with the associated password or credentials allowing access to such account. We use a variety of measures to help secure Your account login information and we do not use or disclose sensitive personal information for any purpose not expressly permitted by applicable law.
We may also collect other personal information outside of these categories in instances where you contact us or interact with us in-person, online, or by phone or mail, for example in the context of:
Receiving help through our help desks or other customer support channels;
Participation in voluntary customer surveys or contests; and
Facilitation in the delivery of our services and to respond to your inquiries.
In these instances, we collect this information directly from you.
Some of this internet or other network activity information, electronic and usage information and geolocation information may be collected using cookies and similar tracking technology (“
Cookies
”). A Cookie is a piece of text that is placed on your computer that allows us to provide information to improve the Services, recognize new or past customers, store your password (if you are registered on our sites), better understand the interests of our customers and visitors, advertise and market to you (including on other sites), recognize if you have opened an e-mail that we sent, test new website designs, and help our business partners or other websites engage in these activities. Third parties may also collect information using Cookies. You can make certain choices about Cookies as set forth in Your Rights and Choices below. To learn more about the cookies we use, click “Cookie Preferences” in the footer of the Site.
From time to time, we may receive personal information about you from third party sources such as:
Social Media Platforms
for example, if you access our Services using your Facebook account login, we may receive Personal Information about you such as your name, email address, and gender. Any Personal Information that we collect from your Facebook account may depend on your Facebook account’s privacy settings.
Online Stores, Retail Stores, Authorized Resellers, Distribution Partners
if you purchase NETGEAR Products or Services from one of these partners, we may receive information about you and your purchase.
Service partners
with whom we offer co-branded services such as security and parental control software, or engage in joint marketing activities.
Marketing partners
that work with us on social media and online channels to sponsor giveaways and promotions.
Third party personal information
: if you choose to provide us with a third party's Personal Information (such as name, email, and phone number), you must ensure that you have the third party's permission to do so. Examples include providing us with the names and images that you associate with account users, forwarding reference or marketing material to a friend, or sending job referrals.
We may combine the information we collect from or receive about you for the outlined purposes below. We may aggregate or deidentify your information and may process such information for any purpose, and such information is not subject to this Privacy Policy.
=== END ITEM p0229

=== ITEM p0230
rule 1: {"polarity": "ALLOW", "actor": "We", "action": "disclose (operation: disclosure)", "data": "information", "recipient": "", "source": "", "purpose": "", "condition": "as permitted by law", "condition_predicate": "law.permitted"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "disclose (operation: disclosure)", "data": "sensitive personal information", "recipient": "", "source": "", "purpose": "for inferring characteristics; for purposes other than those permitted by law", "condition": "unless those permitted by law", "condition_predicate": "NOT law.permitted"}
--- section of rule 1
HOW WE DISCLOSE INFORMATION
We disclose information within SciPlay
. We disclose all categories of information with our parent company and subsidiaries. This includes future subsidiaries or affiliates.
We disclose information with service providers who perform services on our behalf
. We may disclose all categories of information with trusted service providers. This includes suppliers that support our products and services. It also includes payment processors and data analytics companies. It also includes advertising agencies and marketing and research companies.
We disclose information for cross-contextual behavioral advertising
. We may share information with third parties in order to provide cross-contextual behavioral advertising. In the Notice at Collection (above) we outlined which categories of information are shared for cross-contextual behavioral advertising. This does not include SMS opt-in consent, which we do not share with third parties for their own marketing purposes.
We may disclose information if we think we have to in order to comply with the law
. We will transfer all categories of information to respond to a court order or subpoena. We will also disclose it if a government agency or investigatory body requests. This includes US and non-US law enforcement or regulatory authorities.
We disclose information for security purposes
. This includes disclosing to protect us and you. It may also include protecting other users of our platforms.
We may transfer information with any successor to all or part of our business
. If all or part of our business is sold, we may transfer all categories of information as part of that transaction. If there is a merger or acquisition, we may disclose your information.
We may disclose information for other reasons we may describe to you or as permitted by law
.
Additional information for California, Nevada, and Virginia residents
. California, Nevada, and Virginia law require that we tell you if we sell personal information with a third-party for monetary or (in California) other valuable consideration. We do not do this. We also do not sell personal information of anyone, including minors under the age of 16 for monetary or other valuable consideration.
--- section of rule 2
We use information to comply with legal or regulatory obligations:
This includes for security purposes and to help avoid fraud or to protect us or our subsidiaries and licensors.
We use information to fulfill our contractual obligations
: This includes facilitating the creation and maintenance of accounts you have with us.
Our legal basis for using information:
If you are in the UK or the EU, we are required to tell you our “legal basis” for processing your information. Typically, we use your information to fulfil our
contract
with you. We will also process certain cookies with your
consent
. We use personal information in some circumstances for
legal compliance.
This includes responding to court orders or law enforcement requests.
How Long We Keep Information
We keep personal information as long as it is necessary or relevant for the practices described in this Privacy Policy. We also keep information as otherwise required by law.
Sensitive Information Collection and Use
We do not use or disclose sensitive personal information for inferring characteristics or for purposes other than those permitted by law.
More Information About Our Privacy Practices
For more information about our privacy practices, please read the rest of our Privacy Policy, below.
=== END ITEM p0230

=== ITEM p0231
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "delete (operation: erasure or destruction)", "data": "your created content", "recipient": "", "source": "", "purpose": "", "condition": "If you need to delete your created content after deleting your account; please contact us via\nsnow_support@snowcorp.com\nwith the content you wish to delete and the reason; after confirming your identity", "condition_predicate": "((request.delete_created_content AND event.delete_account) AND event.contact_us AND event.identity_confirmed)"}
rule 2: {"polarity": "DENY", "actor": "you", "action": "delete (operation: erasure or destruction)", "data": "your uploaded content", "recipient": "", "source": "", "purpose": "", "condition": "after deleting your account", "condition_predicate": "event.delete_account"}
--- section of rule 1 and rule 2
Filters
: Hot > Profile at top right > Select the corresponding menu
Filters: My filters
Likes: Favorite filters
Effects
: Camera > Effects > Select the corresponding menu
MY: Favorite effects
Following and follower information
: Hot > Profile at top right > Select the corresponding menu
In addition, you may delete all of the content (username, profile picture, nickname, Instagram ID, bio (introduction), my filters, favorite filters and effects, followers, following) that you created or provided to the company by selecting Settings > Account Settings > Delete Account.
However, please note that you cannot edit or delete your uploaded content after deleting your account.
Please edit or delete the content before deleting your account.
If you need to delete your created content after deleting your account, please contact us via
snow_support@snowcorp.com
with the content you wish to delete and the reason, and we will help you with the process after confirming your identity.
Deletion requests may be sent by creators themselves or through a legal representative. If the representative sends the request, the company may request the submission of a letter of attorney to confirm the legitimacy of the representative.
Deletion requests may be denied if the requesting person is not the creator themselves (or a legal representative) or if the content must be preserved according to the law (in our sole discretion).
=== END ITEM p0231

=== ITEM p0232
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "use (operation: use)", "data": "personal data", "recipient": "", "source": "", "purpose": "for other purposes not covered by this Privacy Notice", "condition": "When we want to use the personal data for other purposes not covered by this Privacy Notice, we will inform you thereof and ensure that said use of your personal data is lawful", "condition_predicate": "event.use_for_other_purposes_not_covered_by_privacy_notice"}
rule 2: {"polarity": "DENY", "actor": "", "action": "used (operation: use)", "data": "this information", "recipient": "", "source": "", "purpose": "for personal identification or other purposes", "condition": "", "condition_predicate": "true"}
--- section of rule 1
2. When we want to use the personal data for other purposes not covered by this Privacy Notice, we will inform you thereof and ensure that said use of your personal data is lawful.
--- section of rule 2
2. Personal Data We Automatically Collect About Your Use of Our Services
In addition to the personal data you provide yourself, we may also automatically collect information about your use of our Services, particularly when you are using your device. The personal data we may collect includes the following:
• Device information:
This may include the device name, device model, region and language settings, device identification number (IMEI number), device hardware information and status, IP address, MAC address, operating system version and the settings of the device used to access the Service.
• Log information:
This may include when and how long the Service is used, search terms entered through the Service and the device error logs. The Android system on your smartphone and/or wearable is designed in such a way that your error or crash log will contain information collected at the time of the event, which allows us to analyse the reasons for the crash. Such information may sometimes include your personal data, such as phone number, email address, Google account or Facebook account. However, we have implemented security measures to ensure that this information is used only for error log analysis and not for personal identification or other purposes.
• Location information:
This may include the GPS signal of the device or information about Wi-Fi access points and base stations near you, or the device location ID and network service provider ID when you access some location-based services (for example when you use the weather app). We will ask you if you want to enable location-based services for each of the various location-based apps. You can disable the location settings of your device from the device settings. If you disable location information, the functionalities of the apps that use location information to provide Services to you may be impaired.
• Camera:
To ensure the camera app functions properly, we collect operational data (such as how many times you use the app and the number of photos taken), information about the photos taken (such as the photosensitivity and number of faces captured) and information about the available space left on your mobile phone.
• Other information about your use of the Service:
This may include the version of the app or browser type being used, language settings, IP address, device type, IMEI, websites visited and how you interact with content provided through the Service.
Please also see the Section
"How We Use Cookies and Similar Technologies"
below for further information on personal data that we automatically collect via cookies and other tracking technology when you visit our website.
=== END ITEM p0232

=== ITEM p0233
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "receive (operation: collection)", "data": "data", "recipient": "", "source": "third-party platforms or APIs (including Google services)", "purpose": "", "condition": "Where we receive data through third-party platforms or APIs (including Google services)", "condition_predicate": "event.receive_data_through_third_party_platforms_or_apis"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "collect (operation: collection)", "data": "any special categories of personal data about you (this includes details about your race or ethnicity, religious or philosophical beliefs, sex life, sexual orientation, political opinions, trade union membership, information about your health, and genetic and biometric data)", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1
Ad Management Service Provider
Israel
https://www.anzu.io/privacy-policy
AppLovin Corporation
Ad Management Service Provider
U.S.A.
https://www.applovin.com/privacy/
AppsFlyer Inc.
Analytics Service Provider
U.S.A.
https://www.appsflyer.com/privacy-policy/
Audiomob Ltd
Ad Management Service Provider
United Kingdom
https://audiomob.com/privacy-policy
Bigo Technology Pte. Ltd
Ad Management Service Provider
Singapore
https://www.bigossp.com/agreement/privacyPolicy
Bytedance Pte. Ltd.
Ad Management Service Provider
Singapore
https://www.pangleglobal.com/privacy
Chartboost, Inc.
Ad Management Service Provider
U.S.A.
https://docs.chartboost.com/en/legal/privacy-policy/
Digital Turbine, Inc.
Ad Management Service Provider
U.S.A.
https://www.digitalturbine.com/privacy-policy/
Facebook (Meta Platforms, Inc.)
Analytics / ad management service provider
U.S.A.
https://www.facebook.com/privacy/explanation
Gadsme Managed Ad Network Services
Ad Management Service Provider
France
https://www.gadsme.com/privacy-policy
GameAnalytics Ltd
Analytics Service Provider
UK
https://gameanalytics.com/privacy/
Google LLC
Analytics / Ad Management / Authentication Service Provider
U.S.A.
https://policies.google.com/privacy
InMobi Pte Ltd
Ad Management Service Provider
India
https://www.inmobi.com/privacy-policy/
ironSource Mobile Ltd.
Ad Management Service Provider
Israel
https://developers.ironsrc.com/...
Liftoff Mobile, Inc.
Ad Management Service Provider
U.S.A.
https://liftoff.io/privacy-policy/
Mintegral North America Inc.
Ad Management Service Provider
U.S.A.
https://www.mintegral.com/en/privacy
MOBILEFUSE, LLC
Ad Management Service Provider
U.S.A.
https://mobilefuse.com/privacy-policy
Ogury Ltd
Ad Management Service Provider
United Kingdom
https://ogury.com/ogury-advertising-privacy-policy/
PubMatic, Inc.
Ad Management Service Provider
U.S.A.
https://pubmatic.com/legal/privacy-policy/
Rollbar, Inc.
Analytics Service Provider
U.S.A.
https://docs.rollbar.com/docs/privacy-policy
Smaato, Inc.
Ad Management Service Provider
U.S.A.
https://www.smaato.com/privacy/
Sonic Odeeo Ltd
Ad Management Service Provider
Israel
https://odeeo.io/privacy-policy
Tapjoy, Inc.
Ad Management Service Provider
U.S.A.
https://www.tapjoy.com/legal/general/privacy-policy/
Unity Technologies, Inc.
Analytics / Ad Management Service Provider
U.S.A.
https://unity3d.com/legal/privacy-policy
Vungle, Inc.
Ad Management Service Provider
U.S.A.
https://vungle.com/privacy/
Where we receive data through third-party platforms or APIs (including Google services), such data is used only to provide and improve user-facing features of the App and is processed in accordance with applicable requirements. We do not use such data for advertising, marketing, or profiling purposes, nor do we sell such data to third parties.
The above-said legal entities provide us with automatic data processing technologies for the App and deliver data processing, payment processing, and other services to us concerning the App, and may be involved in the other types of services and activities otherwise discussed in this Privacy Policy. That is why the App may contain tracking and data collection and analytics tools and other automatic data processing technologies for the App provided to us by such legal entities, and that is why third-party companies may have access to and collect data and information about you (within the categories of personal information mentioned above), such as your device identifier, Advertising ID or Android ID, Designated Market Area (DMA), geo-location information, IP address, application usage, access and session times, and your viewing of and interactions with advertising, provided and delivered as described in further detail below.
Please note that all third-party service providers, as well as advertising partners that are engaged in processing user data, are service providers that use such information based on agreement and according to business purposes.
--- section of rule 2
PRIVACY POLICY
Last Updated: April 07, 2026, with Effective Date April 07, 2026
Freeplay Inc
("
we
", "
us
" or "
our
") respects your privacy and understands that you care about your personal information and how it is used. This Privacy Policy ("
Privacy Policy
") clarifies our privacy practices and describes how we collect, use, disclose, and otherwise process your personal information when you install and/or use ("
use
") one or more of our Mobile Apps (hereinafter, "the
App(s)
" or "
our App(s)
"), and explains the rights and choices available to you concerning your personal information.
When we refer to personal information (or personal data), we mean any information of any kind relating to you as an identified or identifiable natural person. It is a natural person who can be identified directly or indirectly, in particular by reference to an identification number or one or more factors specific to your physical, physiological, mental, economic, cultural, or social status. And, namely, personal information identifies, relates to, describes, references, is capable of being associated with, or could reasonably be linked, directly or indirectly, with you.
Our Privacy Policy applies to all users and others who access our Apps ("
Users
").
PLEASE READ THE FOLLOWING PRIVACY POLICY FOR INFORMATION REGARDING THE WAYS YOUR PERSONAL INFORMATION MAY BE PROCESSED AND YOUR CHOICES REGARDING YOUR PERSONAL DATA CAREFULLY. WHEN YOU USE THE APP(S), YOU ACKNOWLEDGE THAT YOU HAVE READ, UNDERSTOOD, AND AGREE TO BE BOUND BY THESE TERMS.
Following the EU General Data Protection Policy (EU GDPR) and the UK General Data Protection Regulation (UK GDPR), we are the data controller unless otherwise stated.
I. INFORMATION WE PROCESS AND HOW WE DO THE PROCESSING
Depending on the circumstances mentioned below, the following general categories of personal information may be collected and otherwise processed:
Category
General Examples
A.
Identifiers
A real name, postal code, unique personal identifier, online identifier (including identifiers provided by third-party services), Internet Protocol address, email address, or other similar identifiers.
B.
Geolocation Data
Physical location or movements.
C.
Internet or other similar network activity
Information on your interaction with an application, or advertisement.
D.
Commercial Information
Records of personal property, products or services purchased, obtained, or considered, or other purchasing or consuming histories or tendencies.
PLEASE, NOTE THAT:
We do not collect any special categories of personal data about you (this includes details about your race or ethnicity, religious or philosophical beliefs, sex life, sexual orientation, political opinions, trade union membership, information about your health, and genetic and biometric data). Nor do we collect any information about criminal convictions and offenses.
Moreover, we cannot access or use your credit card or debit card information.
When the App includes in-app purchases our e-commerce provider (Google) is responsible for billing, processing, and charging for the in-app purchases, handles your personal information, and keeps it absolutely safe and secure. You may access the applicable “in-app” purchase rules and policies directly from the Google Play store.
We obtain the categories of personal information listed above from the following categories of sources:
1.1. Directly from you (Information that you submit):
Guided by the principle of data minimization, we designed our Apps in a way that doesn't require you to sign up for an account to use the App. It means that you do not need to provide us with any information that can be used to access the App (like full name, username, the public username used on social media accounts, phone number(s), e-mail address, or other similar information).
However, in certain cases, you may choose to provide us with limited information by using optional features of the App.
=== END ITEM p0233

=== ITEM p0234
rule 1: {"polarity": "ALLOW", "actor": "IRS", "action": "amendment (operation: adaptation or alteration)", "data": "records", "recipient": "", "source": "", "purpose": "", "condition": "You must submit your Privacy Act request for an amendment of records in writing to the IRS; You must clearly describe the records you are seeking to have amended to include identifying the specific record or note title, date of the record or note, and the specific information within the record or note requested to be amended; You may submit an amendment request via mail, fax or the\nFOIA and Privacy Act Public Access Portal\n.*; unless If the IRS denies your request for amendment", "condition_predicate": "([untranslated: You must submit your Privacy Act request for an amendment of records in writing to the IRS] AND [untranslated: You must clearly describe the records you are seeking to have amended to include identifying the specific record or note title, date of the record or note, and the specific information within the record or note requested to be amended] AND NOT event.irs_denies_request_for_amendment)"}
rule 2: {"polarity": "DENY", "actor": "", "action": "amendment (operation: adaptation or alteration)", "data": "Federal tax records", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1
PDF
Act and submit it on the
FOIA and Privacy Act Public Access Portal
.
If you use these forms, they include all the required elements from
How to write a Privacy Act request (U.S. Department of Treasury)
.
Requests for Amendment:
You must submit your Privacy Act request for an amendment of records in writing to the IRS. You must clearly describe the records you are seeking to have amended to include identifying the specific record or note title, date of the record or note, and the specific information within the record or note requested to be amended.
You may submit an amendment request via mail, fax or the
FOIA and Privacy Act Public Access Portal
.*
If the IRS denies your request for amendment, you will be notified of this decision in writing, which will contain information about your right to appeal the decision.
Requests for Accounting of Disclosures:
You may request an accounting of disclosures made under the Privacy Act if you are the individual named in the disclosed records. Your request must be written, signed, and include a description of the records that is specific enough to the specific record or system of records and its location to allow a search of
Form 5482
files.
Or, you may mail or fax your request(s) above, or a signed written request with the required elements, to:
Internal Revenue Service
FOIA Public Liaison Line:
312-292-2929
IRS FOIA/Privacy Act Request
--- section of rule 2
PDF
is to explain how the IRS preserves privacy and enhances public trust through proper authentication, access, disclosure, retention and protection, of all data and records.
The plan provides an overview of the:
IRS’s privacy protection responsibilities
A description of the structure of the privacy program
Resources dedicated to the privacy program
Role of the Senior Agency Official for Privacy (SAOP) and other privacy officials and staff
Strategic goals and objectives of the privacy program
Management controls in place or planned for meeting applicable privacy requirements and managing privacy risks
Information necessary by the agency’s privacy requirements
Privacy Act requests
Overview
The Privacy Act grants individuals increased rights of access to records maintained about them by government agencies, as well as the right to seek amendment of those records if warranted. The primary types of Privacy Act Requests include:
Requests for Access
Requests for Amendment
Requests for Accounting of disclosures
Note:
Federal tax records are exempt from access or amendment. To amend a federal tax record, taxpayers must file
Form 1040-X
or follow IRS procedures for other changes, such as
change of address
.
The Privacy Act of 1974, as amended, provides safeguards against unwarranted invasions of privacy by establishing a code of "fair information practices." The principles, commonly referenced as the fair information practice principles (FIPPs), require agencies to comply with statutory norms for collection, maintenance, access, use, and dissemination of records.
To increase transparency and assure notice to individuals, the Privacy Act requires agencies to publish in the Federal Register notice of modifications to or the creation of systems of records. The term "system of records" means a group of any records under the control of any agency from which information is retrieved by the name of the individual or by some identifying number, symbol, or other identifying particular assigned to the individual.
A current listing of the Department's System of Records, along with updated routine uses and claimed exemptions, can be found the on the
Treasury Department's System of Records Notices
page.
To further protect the individual, the Privacy Act requires all records which are used by the agency in making any determination about any individual to be maintained with such accuracy, relevance, timeliness, and completeness as is reasonably necessary to assure fairness to the individual in the determination.
The Privacy Act grants individuals increased rights of access to records maintained about them, as well as the right to seek amendment of records maintained about them.
IRS offers routine access to other records through
procedures designed to make access quick and easy
. If you are working directly with an IRS employee on an open tax case, you can request information from the file directly from them.
How to make a Privacy Act request
Requests for Access:
To request to access your Privacy Act records electronically, complete
Form 15603, IRS Request for Individual Access to Non-Tax Records Protected under the Privacy Act
=== END ITEM p0234

=== ITEM p0235
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "collect (operation: collection)", "data": "Personal Information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "collect (operation: collection)", "data": "personal information", "recipient": "", "source": "users under the age of 18", "purpose": "", "condition": "from users under the age of 18", "condition_predicate": "user.age < 18"}
--- section of rule 1
Personal information that we collect, use, and share
The chart accessible
here
provides additional information pursuant to the CCPA about the Personal Information we collect, use, and share.
Information for all other users in the United States (non-California residents)
If you reside in Colorado, Connecticut, Delaware, Iowa, Montana, Nebraska, New Hampshire, New Jersey, Oregon, Texas, Utah or Virginia, or are otherwise protected by privacy and data protection laws you may submit a request to
privacy@turo.com
to exercise any data subject right that you may have under applicable law.
Please note that you may need to verify your identity and request before we are able to process your request. As part of this process, you may be required to provide personal information, such as your name, state of residence, and email address associated with your account and/or government identification.
Information for users in the United Kingdom and Europe
The information in this section applies only to individuals in the European Economic Area (“
Europe
”) and the United Kingdom.
Personal information.
Except as otherwise specified, references to “personal information” in this Privacy Policy are equivalent to “personal data” governed by European data protection legislation.
Controller.
Turo Inc. is the controller of your personal information covered by this Privacy Policy for purposes of data protection legislation in the United Kingdom and Europe. You may contact us at
privacy@turo.com
.
Legal bases for processing.
The legal bases of our processing of your personal information as described in this Privacy Policy will depend on the type of personal information and the specific context in which we process it. If you have questions about the legal basis of how we process your personal information, contact us at
privacy@turo.com
.
Use for new purposes.
We may use your personal information for reasons not described in this Privacy Policy where permitted by law and the reason is compatible with the purpose for which we collected it. If we need to use your personal information for an unrelated purpose, we will notify you and explain the applicable legal basis.
Retention.
We retain personal information where we have an ongoing legitimate business need to do so (for example, to provide you with a service you have requested; to comply with applicable legal, tax, or accounting requirements; to establish or defend legal claims; or for fraud prevention). When we have no ongoing legitimate business need to process your personal information, we will either delete or anonymize it, or if this is not possible (for example, because your personal information has been stored in backup archives), then we will securely store your personal information and isolate it from any further processing until deletion is possible.
Your rights
The data protection laws of the United Kingdom and Europe give you certain rights regarding your personal information. If you are located in the United Kingdom or Europe, you may ask us to take the following actions in relation to your personal information that we hold:
Access
. Provide you with information about our processing of your personal information and give you access to your personal information.
Correct
. Update or correct inaccuracies in your personal information.
Delete
. Delete your personal information.
Transfer
. Transfer a machine‐readable copy of your personal information to you or a third party of your choice.
Restrict
. Restrict the processing of your personal information.
Object
. Object to our reliance on our legitimate interests as the basis of our processing of your personal information that impacts your rights.
You may submit these requests by email to
privacy@turo.com
or our
postal address
or by accessing certain features in the Services.
We may request specific information from you to help us confirm your identity and process your request. Applicable law may require or permit us to decline your request.
--- section of rule 2
As a result, this information may be subject to access requests from governments, courts, regulatory agencies, security authorities, or law enforcement in those jurisdictions according to the laws in those jurisdictions.
Sensitive information
We ask that you not send us, and you not disclose, any sensitive information (e.g., Social Security numbers, social insurance numbers, passports, information related to racial or ethnic origin, or health) on or through the Services or otherwise to us unless specifically requested.
Minors
The Services are not intended for anyone under the age of 18 and we do not knowingly collect personal information from users under the age of 18. If a minor under the age of 18 has already provided us with personal information, his or her parent or guardian may contact us to request that we delete it.
Complaints
If you would like to submit a complaint about our use of your personal information, this privacy policy, or our response to your requests regarding your personal information, you may contact us at
privacy@turo.com
.
Third-party privacy practices
This Privacy Policy addresses only the use and disclosure of information collected by Turo. This Privacy Policy does not address, and we are not responsible for, the privacy, information, or other practices of any third parties, including any third party operating any site or service to which the Services link. The inclusion of a link on the Services does not imply endorsement of the linked site or service by us or by our affiliates. If you disclose your information to others, or if you are directed to a third-party website, their privacy notices and practices will apply. Some areas of the Services implement Google Maps/Places mapping services, including the Google Places API. In addition, to fight spam and abuse of the Services, Turo has implemented reCAPTCHA Enterprise, a Google service. Your use of the Services is subject to
Google’s Privacy Policy
and you can learn more about how Google processes personal data in
Google’s Business Data Responsibility Site
.
Translations
Where Turo has provided you with a version of this Privacy Policy in a language other than English, in case of any wording discrepancies between such version and the English version, the English wording takes precedence. In France and if you are a consumer, the French language version will prevail.
Changes to this privacy policy
We may change this Privacy Policy. Please take a look at the “Last revised” legend at the top of this page to see when this Privacy Policy was last revised. Any changes to this Privacy Policy will become effective when we post the revised Privacy Policy on the Services or as otherwise indicated. Your use of the Services following these changes means that you accept the revised Privacy Policy. If you don’t agree to these changes, you can contact us to close your account.
Contact
Turo welcomes your questions and comments about privacy. Please feel free to contact us at Turo Inc., 111 Sutter Street, San Francisco, CA 94104 USA. You may also
email
us.
Information for California residents
Scope.
This section applies only to California residents entitled to receive the information in this section under the California Consumer Privacy Act of 2018, including as amended under the California Privacy Rights Act of 2020 ("
=== END ITEM p0235

=== ITEM p0236
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "disclose (operation: disclosure)", "data": "Personal Information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "share (operation: disclosure)", "data": "Personal Information", "recipient": "", "source": "", "purpose": "", "condition": "of individuals under 16 years of age", "condition_predicate": "user.age < 16"}
--- section of rule 1
For purposes of this section, the term “Personal Information” has the meaning given to “personal data”, “personal information” or other similar terms, and “Sensitive Personal Information” has the meaning given to “sensitive personal information,” “sensitive data”, or other similar terms in the Applicable State Privacy Laws but does not include information or entities exempted from the scope of the Applicable State Privacy Laws, such as those subject to GLBA. Please note that we may claim legal exemptions for certain types of Personal Information and certain Intuit companies from all or certain parts of the Applicable State Privacy Laws.
Personal Information that we collect, use, and disclose
. The chart
here
summarizes the Personal Information we collect and describes our practices currently and during the 12 months preceding the effective date of this Privacy Statement. Information you voluntarily provide to us, such as in free-form webforms, may contain other categories of Personal Information not described in this chart.
Your privacy rights.
As a resident whose Personal Information is protected by Applicable State Privacy Laws, you may have the rights listed below. However, these rights are not absolute, and in certain cases we may decline your request as permitted by law.
Access
. You may request a copy of the Personal Information in
your Intuit account
or visit our
Intuit Privacy Center
or call us toll-free at 1 (877) 261-6470. If your inquiry is specific to Credit Karma, visit the
Credit Karma Help Center
or email us at
CCPArequests@creditkarma.com
.
If your inquiry is specific to Mailchimp,visit the
Mailchimp Privacy Rights Request Page
.
Correction
. You can edit and correct your Personal Information at any time by changing it directly in our products and services.
Deletion
. You may have the right, under certain circumstances, to request that we delete the Personal Information you have provided to us. You may delete your Personal Information in the Privacy section of
your Intuit account
or visit our
Intuit Privacy Center
or call us toll-free at 1 (877) 261-6470. If your inquiry is specific to Credit Karma, visit the
Credit Karma Help Center
or email us at
CCPArequests@creditkarma.com
.
If your inquiry is specific to Mailchimp,visit the
Mailchimp Privacy Rights Request Page
.
Opt-out of tracking for targeted advertising purposes
. You may opt-out of tracking for targeted advertising by visiting the “Manage Cookies” or “Privacy Settings” link located at the footer of the Intuit website. Our
Mailchimp website
will track for targeted advertising purposes, if you choose. You can control that function by visiting the “Cookie Preferences” link in the footer of the
Mailchimp website
. Intuit, Mailchimp and Credit Karma do not otherwise “sell” your Personal Information to third parties for monetary consideration.
In addition, if you have enabled a recognized opt-out mechanism on your browser, device, or platform, you will be automatically opted out of tracking for targeted advertising purposes when you interact with our Services. Please go here to learn more about enabling one such preference signal, the Global Privacy Control:
https://globalprivacycontrol.org/#download
.
Opt-out of profiling
. You can opt-out of the automated processing of your Personal Information to evaluate, analyze, or predict personal aspects related to your economic situation, health, personal preferences, interests, reliability, behavior, location, or movements, to the extent this results in decisions that produce legal or similarly significant effects.
Sensitive Personal Information
. Some of the Personal Information that we may collect may be considered Sensitive Personal Information under certain Applicable State Privacy Laws. We will not process your Sensitive Personal Information without your consent.
Non-discrimination
. You have the right to be free from discrimination related to your exercise of any of your privacy rights.
Appeal
.
--- section of rule 2
Credit Karma does not sell or share Personal Information subject to the CCPA, and therefore does not offer a “Your California Privacy Rights” link on its website. We do not knowingly sell or share the Personal Information of individuals under 16 years of age.
Limit processing of Sensitive Personal Information.
Some of the Personal Information that we may collect is considered Sensitive Personal Information under the CCPA. We collect Sensitive Personal Information for the purposes allowed by law or with your consent. We only use Sensitive Personal Information as necessary for our (1) Service delivery and operations, (2) compliance and protection, (3) research and development, or (4) Service improvement and analytics purposes in accordance with CCPA. If we use Sensitive Personal Information outside the permitted purposes of the CCPA, we will provide you with the right to limit processing of Sensitive Personal Information.
California Shine the Light.
Customers who are California residents may request certain information concerning the categories of personal information (if any) we disclose to third parties or affiliates for their direct marketing purposes. If you would like more information, please submit a written request to us using the contact information provided below.
Non-discrimination
. You have the right to be free from discrimination or retaliation related to your exercise of any of your California privacy rights.
Verification.
In order to protect your Personal Information from unauthorized access or deletion, we may require you to verify your credentials before you can submit a rights request. If you do not have an account with us, or if we suspect your account has been accessed without your authorization, we may ask you to provide additional Personal Information for verification. For Credit Karma members, we may require that you confirm certain pieces of Personal Information that we have on file and/or log into your Credit Karma account. If we are subsequently unable to confirm your identity, we may refuse your rights request.
Authorized agents.
You may use an authorized agent to submit a rights request. If you do so, the authorized agent must present signed written authorization to act on your behalf, and you will also be required to independently verify your own identity directly with us and confirm with us that you provided the authorized agent permission to submit the rights request. This verification process is not necessary if your authorized agent provides documentation showing that the authorized agent has power of attorney to act on your behalf under Cal. Prob. Code §§ 4121 to 4130.
Learn more about instructions for authorized agents
.
We may deny a request from an agent that does not submit adequate proof that they have been authorized by you to act on your behalf.
Transparency matters.
Learn more about the requests we process by viewing our
Privacy Rights Transparency Report
.
Other U.S. State Residents
Scope.
This section applies only to the residents of U.S. states that have privacy laws that grant their residents the rights described below, including Colorado, Connecticut, Delaware, Iowa, Maryland, Minnesota, Montana, New Hampshire, Nebraska, New Jersey, Oregon, Tennessee, Texas, Utah, Virginia, Indiana, Kentucky, and Rhode Island (collectively, “
Applicable State Privacy Laws
”). It describes how we collect, use, and share Personal Information of state residents described in this subsection in our capacity as a business or controller under Applicable State Privacy Laws, and your rights with respect to that Personal Information.
=== END ITEM p0236

=== ITEM p0237
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "collect (operation: collection)", "data": "Personal Information", "recipient": "", "source": "such persons in your Organization", "purpose": "", "condition": "If you are using WeChat on behalf of a company, partnership, association, government or other organization (your \" Organization \")", "condition_predicate": "user.category = organization_representative"}
rule 2: {"polarity": "DENY", "actor": "WeChat", "action": "provide (operation: collection)", "data": "sensitive Personal Information", "recipient": "", "source": "", "purpose": "to use the service", "condition": "", "condition_predicate": "true"}
--- section of rule 1
2. SCOPE AND APPLICATION
This Privacy Policy only applies to you if you are a
WeChat user
.
This Privacy Policy does not apply to you if you are a
Weixin user
. You are a Weixin user if you had either:
registered by linking a Chinese Mainland mobile number; or
contracted with 深圳市腾讯计算机系统有限公司 (Shenzhen Tencent Computer Systems Company Limited) for Weixin.
If you are a Weixin user, you are subject to the
Weixin Agreement on Software License and Service of Tencent Weixin
and
Weixin Privacy Protection Guidelines
and not this Privacy Policy.
You can check whether you are a WeChat or Weixin user by clicking "Me" > "Settings" > "About" and then clicking the link to the "Terms of Service". If you see the WeChat – Terms of Service then you are a WeChat user. If you see the Agreement on Software License and Service of Tencent Weixin then you are a Weixin user. Alternatively, if you are using the latest version of WeChat, you can also check whether you are a WeChat or Weixin user by verifying the service name listed in the header at the top of the "Chats" screen. If you see "WeChat" in the header then you are a WeChat user, whereas a Weixin user will see "Weixin" (or "微信" for users viewing in a Chinese language interface).
If you subsequently change your phone number (either from a Chinese Mainland mobile number to a non-Chinese Mainland mobile number, or vice versa) you will be required to convert your account (to either a WeChat or Weixin account, depending on your new phone number). If you convert your Weixin account to a WeChat account, this Privacy Policy applies to you from the date our system records such conversion. If you convert your WeChat account to a Weixin account, this Privacy Policy ceases to apply to you from the date our system records such conversion.
This Privacy Policy does not apply to Personal Information collected by third party services that you may access through the WeChat platform (e.g., features operated by Weixin such as Advanced Search, Channels, Top Stories, and WeBeans; Weixin Open Platform services including Official Accounts, Mini Programs, and Weixin Login; Weixin Pay or WeChat Pay; or a third-party web site viewed via the internal browser), and Personal Information that you choose to share with a Weixin user. Please refer to the privacy policy of the relevant third party service. For more information, please see the section entitled
"Who do we share your data with?"
below.
If you are using WeChat on behalf of a company, partnership, association, government or other organization (your "
Organization
"), you agree to notify such persons in your Organization whose Personal Information (defined below) we collect or you provide to us ("
Connected Persons
"), and you agree to obtain such Connected Persons' consent to the processing of their Personal Information in accordance with this Privacy Policy as required by applicable laws and regulations. When this Privacy Policy refers to "you"or "your", this includes you and any Connected Persons. If you or any Connected Persons would like to request for your Personal Information to be removed from our database, please contact us via our form
here
.
--- section of rule 2
SENSITIVE PERSONAL INFORMATION
In some jurisdictions, certain types of Personal Information, such as information about your race, religious, political or philosophical views, sexual orientation, and health, are characterized as sensitive and are subject to stricter regulation than other types of Personal Information.
WeChat does not require you to provide sensitive Personal Information to use the service. By posting or communicating any sensitive Personal Information within WeChat, you consent to such information being available within the privacy controls you have selected.
=== END ITEM p0237

=== ITEM p0238
rule 1: {"polarity": "ALLOW", "actor": "", "action": "cached (operation: storage)", "data": "chats", "recipient": "", "source": "", "purpose": "", "condition": "What information does Brave Talk process?; If you use the chat function; temporarily; for the duration of the meeting", "condition_predicate": "(event.use_chat_function AND [untranslated: temporarily] AND [untranslated: for the duration of the meeting])"}
rule 2: {"polarity": "DENY", "actor": "", "action": "retained (operation: storage)", "data": "they", "recipient": "", "source": "", "purpose": "", "condition": "What information does Brave Talk process?; If you use the chat function; after a call ends", "condition_predicate": "(event.use_chat_function AND event.call_ends)"}
--- section of rule 1 and rule 2
No data that identifies you or that can be linked to you leaves your device.
Brave Wallet
Brave Wallet relies on third party service providers to help us read and write transactional data from various blockchains including Bitcoin, Ethereum, Solana, and others on a user’s behalf. To do this we typically need to pass wallet address(s) or transactional data to these service providers in order to help users interact with the blockchain. In certain circumstances, such as when a service is used by default, Brave proxies requests to prevent data from being connected to your IP address. By enabling Brave Wallet, you consent to relying on these services to interact with the Blockchain when necessary.
When you make a transaction using a third-party that redirects you to their services, such as an on-ramp partner, they will capture your IP address, wallet address, transaction and event data. With on-ramp services, you’ll be linked to a third-party site which may conduct identity verification checks in order to meet obligations they have under sanctions and anti-money laundering laws. You should review the privacy notices and terms of service of those third parties.
We use Decentralised Exchange Aggregators (DEX) such as
0x
for swaps made on EVM compatible blockchains and
Jupiter
for swaps completed on the Solana blockchain. They will also process your wallet address, related transaction data and your IP address but will ONLY use this data to fulfill the transaction (including getting a quote).
Sanctions compliance
Cryptocurrency addresses that are listed on the OFAC’s
Specially Designated Nationals List
(SDN list) are ineligible to participate in Brave services, including Brave Wallet. To meet our legal obligations, Brave compares cryptographic addresses to a copy of the SDN list built-in to the browser. Brave Wallet will not allow for transfers to any sanctioned addresses. We may also need to perform periodic lookbacks of past transactions to meet compliance obligations. We use a third-party provider (
Inca.Digital
) to perform this service on our behalf.
Brave Wallet privacy protections
Brave does not track actions that you make in your wallet.
Brave proxies and strips the IP address associated with access to the Brave Wallet.
Brave does not log transaction data.
We use anonymized and aggregated statistics collected from on-ramp partners which include regional volumes of transactions, the daily number of transactions by token/chain, daily currency volumes of transactions by token/chain, and monthly unique transactions by token/chain. We use this statistical data to understand at a high level which cryptocurrency assets are being used and on which platforms.
Brave premium services
Brave Talk
Brave Talk is a private video and/or audio conference tool. What you say or type in the service is not logged or saved. Who you talk to, when, and how, is private to you.
Please note that Brave uses the
8x8
communications platform, and software (API) capabilities of 8x8 (based on the
Jitsi
Open Source video conferencing software) to help deliver Brave Talk. 8x8 provides a service on behalf of Brave, and we remain responsible for Brave Talk.
Brave Talk is Internet-only; it does not support participation via telephony.
What information does Brave Talk process?
We process the minimum information necessary to provide the Brave Talk service. This includes:
Your IP address and the URL of the meeting that will be processed in order to enable calls. This data is not retained after a call ends.
If you use the chat function, chats will be temporarily cached for the duration of the meeting; they are not retained after a call ends.
If you record a meeting that you host, the recording will be temporarily stored on the server for 24 hours to allow you to download it. Your profile name that you choose to display will be processed and available during the meeting.
=== END ITEM p0238

=== ITEM p0239
rule 1: {"polarity": "ALLOW", "actor": "", "action": "Collected (operation: collection)", "data": "Work Email", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "collect (operation: collection)", "data": "email addresses", "recipient": "", "source": "", "purpose": "to provide our services", "condition": "", "condition_predicate": "true"}
--- section of rule 1
Type of Information Collected
Purpose
IP Address
Standard web HTTP request; may be used for limited security login controls
Cookie (ours)
Standard web cookie used for dashboard session management
Cookie (other-party)
Other-party web tracking tools used for business intelligence
First, Last Name
Used for team user identification
Work Email
Used as the primary login identifier
Password
Account registration, secure our Services and prevent fraud
Account Holder Primary Role
Account registration, tell Clients about products and services offered by Branch and Branch’s selected partners
User Agent
Standard web browser user agent metadata; may be used for limited security login controls
Referer
Standard web browser HTTP referer; may be used for general internal business analytics
Request
Standard web HTTP request; may be used for general internal business analytics
Github ID
(optional) Can be used as a login method
Billing Information
Payment account registration
Log Data
Provide the Services, tell Clients about products and services offered by Branch and Branch’s selected partners, personalize our experience, secure our Services and prevent fraud, and defend our legal rights and comply with the law
Account holder feedback
Help us improve your experience on the account dashboard
Dashboard Information:
Information we collect from visitors who register for an account on our dashboard includes the following, some of which is considered Personal Data under applicable law:When a Client creates an account and uses the Services, Branch may collect certain log data, such as IP address from which a Client is connecting to the Services, information related to the device being used to connect to the Services (e.g., browser type and version, device type, OS version) and the features and functions of the Services used by the Client (“Log Data”).
We also require Clients to set up a user ID and unique password for account security purposes. Clients must not disclose their passwords to anyone. Clients also have the option of adding other team members to their account. This account information enables us to set up an account for Clients, to provide the Services, and to otherwise manage Client accounts. We may also use this information to notify Clients about updates to our Services and provide them with promotional emails. We offer a mechanism to opt out from promotional emails as described in the “Opt-Out from Promotional Emails” section below.
Account and Billing Information:
To the extent that we charge a fee for the Services, we may also collect limited billing, payment, and contract information from Clients through our payment and contract vendors.
Connection Information with Other Parties:
Some features of the dashboard Services allow you to disclose your information through your accounts to other companies such as Facebook and Google. If you choose to connect Branch to such services provided by other parties, we may collect information related to your use of those services provided by other parties, such as authentication tokens that allow us to connect to your accounts with those other parties. We will ask you for permission before you authorize our collection of this information. We may also collect information about how you are using the Services to interact with those connected services.
Information from Other Sources:
In addition to the information collected through our Website, we or our vendors may obtain and disclose additional information, such as job title or contact information, from other public and non-public sources such as business websites, social networking platforms, or databases maintained by other parties. We use this information to better enable Branch to identify and contact businesses that might be interested in engaging our Services, and to gain a better understanding of a potential Client’s business needs.
--- section of rule 2
Privacy Policy
Last updated September 15, 2025
The Branch Guiding Privacy Principles
Branch is a deep linking and attribution analytics platform for app and website developers. We are proud of our commitment to providing our services in a privacy-first way. So we thought it would be helpful to lay out, in plain English, the Branch Guiding Privacy Principles that drive how we’ve chosen to design our services with privacy as a top priority. We further describe our privacy practices in the official
Privacy Policy
below this section, but we hope you’ll find this summary of our principles helpful.
We limit the data we collect. We practice data minimization, which means that we take steps to avoid collecting or storing information that we don’t need to provide our services. The personal data that we collect to provide our services is limited to data like advertising identifiers, IP address, and information derived from resettable cookies (the full list is below in our privacy policy). We do not collect or store information such as names, email addresses, physical addresses, or SSNs to provide our services. Nor do we want to. In fact, our
Terms & Conditions
prohibit our customers from providing Branch with any kind of sensitive end-user information.
We will only provide you with data about actual end-user activity on your apps or websites. Customers who subscribe to our linking and analytics platform can only access “earned” cookies or identifiers. This means that an end user must visit a customer’s site before our customer can see the cookie; and an end user must download a customer’s app in order for Branch to collect the end user’s advertising identifier for that customer. In short, the Branch services benefit customers who already have seen an end user across their platforms and want to understand the relationship between those web visits and app sessions.
We do not rent or sell customer end user data. No Branch customer can access another Branch customer’s end-user data. And we are not in the business of renting or selling any customer’s end-user data to anyone else. To enable customers to control their end-user personal data, they can request deletion
here
of that data at any time, whether in bulk or for a specific end user. These controls are available to customers worldwide, although we designed them to comply with the CCPA and GDPR requirements.
Beyond these principles stated above, Branch will continue to find ways to design our services to respect end user privacy. We’re committed to making sure our customers understand how we use data they entrust to us and how they can control it so that they can, in turn, be transparent with their end users.
Introduction
Branch Metrics, Inc. ( “Branch”, “us”, “our” or “we”) offers a linking and analytics platform enabling developers of applications (our “Clients”)–whether those applications are websites or “apps,” and across different types of devices (“Digital Properties”)–to improve their end users’ (“Users”) cross-application experiences, and to derive additional insights into how their Users download and utilize those applications. Branch recognizes and believes that data privacy is important to all Internet users, and therefore we design and operate our services in a privacy-first manner.
This Privacy Policy is divided into three parts:
Collection and Use of Information from Our Services: This section explains how Branch collects and uses information about Users in connection with our linking and analytics products and services (the “Branch Services” or the “Services”).
Collection and Use of Information from Our Website and for Marketing Purposes: This section explains how we collect and use information about our website visitors through our website located at branch.io (the “Website”), which includes the dashboard we provide to our Clients located at dashboard.branch.io. So, if you are a Client using our Branch dashboard, this section applies to the data we collect from you.
=== END ITEM p0239

=== ITEM p0240
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "disclose (operation: disclosure by transmission)", "data": "children’s Personal Information", "recipient": "vendors we use to support the internal operations of our App, or data processors", "source": "", "purpose": "to support the internal operations of our App", "condition": "who are bound by contractual or other obligations to use the information only for such purpose and to keep the information confidential", "condition_predicate": "[untranslated: who are bound by contractual or other obligations to use the information only for such purpose and to keep the information confidential]"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "share (operation: disclosure by transmission)", "data": "children’s personal information", "recipient": "", "source": "", "purpose": "", "condition": "unless as described in this section", "condition_predicate": "NOT policy.permits"}
--- section of rule 1 and rule 2
4. Children’s Privacy
We know that children deserve special, enhanced privacy protections. That’s why we develop our App and Services to ensure that parents, caregivers, and guardians are in control. We require an adult to register their child and provide the child’s information to establish an account; in particular, we collect the child’s first name (optional) so that you can easily distinguish between different profiles and the child’s age (optional) so that we can customize App content for the child.
Once the parent has created the child’s account, then we strive to collect only as much information about a child player as is reasonably necessary for the child to participate in the educational activities in our Services. We do not condition a child’s use of our Services on their disclosure of more information than is reasonably necessary.
How We Use Your Child’s Information.
We use the information we collect to improve our App and to deliver a better and more personalized experience. For example, we may use your child’s information to:
Estimate our customer size and usage patterns.
Store information about the child’s preferences regarding the activities played in our App and context (such as language), allowing us to customize the content according to individual interests.
Generate regular reports on your child’s progress, using artificial intelligence, so that you can be part of your child’s learning journey, see your child’s strengths and areas for improvement and explore other resources inside and outside the app to support your child’s learning progress. You can object to this processing of your child’s data at any time through the channels provided.
Our Practices for Disclosing Children’s Information.
We do not share, sell, rent, or transfer children’s personal information other than as described in this section:
If a Parent opts to share content from the app (e.g., achievements) we will provide the content via shareable links with secure tokens.
We may disclose aggregated information about many of our users, and information that does not identify any individual.
In addition, we may disclose children’s Personal Information:
To vendors we use to support the internal operations of our App, or data processors, and who are bound by contractual or other obligations to use the information only for such purpose and to keep the information confidential.
If we are required to do so by law or legal processes, such as to comply with any valid court order or subpoena or to respond to any valid request from a governmental, regulatory, or law enforcement entity.
Accessing and Correcting Your Child’s Personal Information.
At any time, you may review the child’s Personal Information maintained by us, require us to correct or delete the Personal Information, and/or refuse to permit us to further collect or use the child’s Personal Information. You can review, change, or delete your child’s personal information by sending us a request here:
https://help.lingokids.com/hc/en-us/requests/new
or emailing us at
dpo@lingokids.com
. To protect your privacy and security, we may require you to take certain steps or provide additional information to verify your identity before we provide any information or make corrections.
If we learn that we mistakenly collected any personal information from a child (as defined based on the minimum age for data collection in their jurisdiction), we will delete it immediately, unless we have a legal obligation to retain it, and then disable the child’s account.
Lingokids is audited and certified by the kidSAFE Seal Program (
https://www.kidsafeseal.com/aboutourprogram.html
), and complies with its standards and requirements for online security and privacy. You can see Lingokids’ certification by visiting its page (www.kidsafeseal.com/certifiedproducts/lingokidsenglish_app.html).
Persistent Identifiers We Automatically Collect from Children.
=== END ITEM p0240

=== ITEM p0241
rule 1: {"polarity": "ALLOW", "actor": "our", "action": "store (operation: storage)", "data": "such information", "recipient": "", "source": "", "purpose": "for photo processing", "condition": "When you use some face recognition functions (including but not limited to theme templates)", "condition_predicate": "event.use_face_recognition_functions"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "store (operation: storage)", "data": "facial feature information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1 and rule 2
We will not store the materials, tags and any related information for more than the necessary time, or use them for any other purpose besides this, or Provide to third parties.<br/><strong>2.</strong> <strong>Which permissions we might ask you to authorize</strong><br/>In order to provide you with more high-quality, efficient products and services and improve your service experience, we may ask you to authorize the corresponding terminal device permissions in the following additional services we provide to you. We collect the following permissions and corresponding information following the criterion of minimal data collection with your consent:<br/>• Camera permissions: for video shooting；<br/>• Microphone permissions: for video shooting and editing；<br/>• REQUEST_INSTALL_PACKAGES：for receiving app packages, AND Enabling user-initiated installation of app packages;<br/>• Album: used to access photos for video editing or upload and download personal videos, photos, audios, and subtitle data；<br/>• Receive notification messages: used to receive messages;<br/>• Gets the current network status: to alert users whether they are currently using the mobile network or determine whether a user&#x27;s wifi network is available；<br/>• IDFA permission: for ad tracking.<br/>If you access our Service through a device made by Apple, Inc. (“<strong>Apple</strong>”), this term will apply: Identifier for advertisers (“<strong>IDFA”</strong>) is analogous to an advertising cookie on Apple
mobile devices (“<strong>iPhones</strong>”). Apple created the IDFA for ad tracking. It enables an advertiser to get notified when you have taken an action like clicking on their ad or installing their app. Starting with iOS14.5, You can choose whether to grant ad tracking. when you clicked the “Ask App Not to Track” button on your iPhone, we would not be able to access the device’s IDFA, so we could not use the IDFA to track you across apps and services. You also can turn off the ad tracking permission at your own discretion at any time in the system Settings of your terminal device. If you turn off the ad tracking permission, we will not track. <br/>• TrueDepth API: to get face data and track faces in our template functions.<br/>Face recognition: For specific theme template editing and short video production services, mAst collects the avatar photos you’ve uploaded or shot. To use some functions of the theme templates that need face matting, you can voluntarily permit mAst to access the camera or photo album to obtain photos from your mobile device. Only after you confirm your permission, can mAst access your camera and photo album. When you use some face recognition functions (including but not limited to theme templates), we automatically capture the positions and shapes of your five sense organs, analyze the facial feature information, store such information on our server for photo processing, and return the renderings to you. We will not store such processed photos,
facial feature information, or renderings, or share them with any third party. Such information is processed only to run the face recognition function and provide you with better renderings.<br/>You can check the status of the above permissions in the system settings of your terminal device, and you can turn on or off any or all above permissions at your own discretion at any time. Please note that when you open any permission. It means that you authorize us to collect and use the personal information corresponding to the permission to provide you with the above corresponding services. Once you turn off any permission, it means that you cancel or revoke the authorization of the permission, And we will no longer continue to collect and use the corresponding personal information based on this permission, nor will we be able to provide you with the services corresponding to this permission.
=== END ITEM p0241

=== ITEM p0242
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "collect (operation: collection)", "data": "personal data", "recipient": "", "source": "", "purpose": "for the purposes stated in this Statement", "condition": "In the HONOR Email services", "condition_predicate": "service = HONOR Email"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "collect (operation: collection)", "data": "any of the preceding information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1 and rule 2
1. What Data Do We Collect About You?
In the HONOR Email services, we shall collect and use your personal data only for the purposes stated in this Statement. Personal data refers to any data that enables us to identify you as a user.
When you use HONOR Email, the corresponding third-party email service provider will directly collect your email address, username, and password/token. If you log in to your email account via Exchange ActiveSync, your mobile device ID will also be collected, in addition to the preceding information.
We will not collect or store any of the preceding information. Instead, your password(s)/token(s) are encrypted and stored locally on your device.
To provide you with the service, HONOR Email requires Internet access and the permissions to access Storage, Contacts, Calendar.
Storage: The Storage permission is required for you to preview, add, and download email attachments.
Contacts: The Contacts permission is required to sync data between your email contacts and device contacts.
Calendar: The Calendar permission is required to sync your email calendar events to the Calendar app on your device.
You can manage the permissions for HONOR Email from system settings.
=== END ITEM p0242

=== ITEM p0243
rule 1: {"polarity": "ALLOW", "actor": "", "action": "transmission (operation: disclosure by transmission)", "data": "personal data", "recipient": "", "source": "", "purpose": "", "condition": "applicable exclusively to users and visiting users residing in the Federative Republic of Brazil or to any other situation in which Brazilian laws are applicable; By visiting the Platforms and using the Services, you as an individual aged 18 or over", "condition_predicate": "((user.jurisdiction = Brazil OR [untranslated: any other situation in which Brazilian laws are applicable]) AND (event.visit_platforms AND event.use_services AND user.age >= 18))"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "share (operation: disclosure by transmission)", "data": "your personal data", "recipient": "third parties", "source": "", "purpose": "", "condition": "unless as indicated below", "condition_predicate": "NOT policy.permits"}
--- section of rule 1
APPENDIX FOR BRAZIL
The provisions set forth in this appendix are applicable exclusively to users and visiting users residing in the Federative Republic of Brazil or to any other situation in which Brazilian laws are applicable. In the event of a conflict between the main text of the Privacy Policies and this appendix, the provisions of this appendix will apply for users and visiting users residing in the Federative Republic of Brazil.
The collection of your Personal Data is based not only on your express consent, but also: (i) on compliance with the legal or regulatory obligations of Mercado Libre; (ii) on the regular exercise of rights in procedures of judicial, administrative or arbitration proceedings nature; (iii) on the protection of life and health; (iv) on the execution of the commercial and contractual relationship between Mercado Libre and the users; (v) on the legitimate interest of Mercado Libre or third parties; and (vi) on the protection of the credit.
Learn more about the
legal bases we use
in the processing of your personal data.
By visiting the Platforms and using the Services, you as an individual aged 18 or over, accept the collection, use, transmission, production, receipt, classification, access, reproduction, distribution, management, filing, storage, exclusion, evaluation and/or information control, modification, communication, transfer, dissemination, extraction or any processing activity ("Processing") of your personal data, as described in this Privacy Statement.
Who is responsible for the processing of Personal Data?
In the Federative Republic of Brazil, the Services of Mercado Libre are provided by (i)
EBAZAR.COM.BR LTDA
, registered with CNPJ/MF under No. 03.007.331/0001-41, and (ii)
MercadoPago.com Representações Ltda.
, registered with CNPJ/MF under No. 10.573.521/0001-91;
MERCADOLIVRE.COM ATIVIDADES DE INTERNET LTDA.
, registered with CNPJ/MF under No. 03.361.252/0001-34;
IBAZAR.COM ATIVIDADES DE LTDA.
, registered with CNPJ/MF under No. 03.499.243/0001-04 CNPJ/MF under No. 03.499.243/0001-04; and
MERCADO ENVIOS SERVIÇOS DE LOGÍSTICA LTDA.
, registered with CNPJ/MF under No. 20.121.850/0001-55, all headquartered at Av. das Nações Unidas, No. 3.003, Bonfim, Osasco/SP, Brazil, who is responsible for the processing of your personal data.
Such Services are provided through the
www.mercadolibre.com.br
, api.mercadolibre.com,
www.mercadopago.com.br
, api.mercadopago.com Platforms and their mobile versions: mobile.mercadolibre.com.ar, mobile.mercadolibre.com, login-mobile.mercadolibre.com, frontend.mercadolibre.com, and mobile.mercadopago.com.
Automated decisions and profiling
Subject to clause 13 of the Privacy Statement, you may also exercise your right of access at any time to know what Personal Information has been used as part of the relevant decision-making and, if applicable, the right of rectification where you consider that any Personal Data used is inaccurate or incomplete.
How can you exercise your rights to control your Personal Information?
Applicable regulations grant you certain rights over your Personal Information: (i) confirmation of the existence of the processing of your Personal Information; (ii) access; (iii) correction of incomplete, inaccurate or outdated Personal Information; (iv) anonymization, blocking or exclusion of Personal Information that is unnecessary, excessive or processed in violation of applicable law; (v) portability of Personal Information; (vi) exclusion of Personal Information when it is no longer necessary for the purposes for which it was collected, except in the case of retention necessary for: (a) the fulfillment of a legal or regulatory obligation; (b) the transfer to third parties for any other reason authorized by law or any regulation other than the law or regulation governing the protection of personal data in Brazil, including the Brazilian Law on Personal Data Protection - LGPD (Law no. 13.
--- section of rule 2
The use of your data for any other purpose that is not compatible with those detailed above, will be communicated to you before we proceed to its processing.
Mercado Libre will keep your Personal Data for as long as necessary to fulfill the purposes for which it was collected.
"How do we share personal data?"
Protecting your privacy is very important for Mercado Libre. For this reason, we do not sell or commercialize data that may identify our users. We neither share nor transfer your personal data to third parties in any other way, except as indicated below:
Mercado Libre may assign, transmit and/or transfer your personal data to:
(i) "Service Providers": Service providers or companies are third parties that we contract to act on behalf of Mercado Libre to provide a service following our instructions and in accordance with the provisions of this Privacy Notice, to contribute to improve or facilitate operations through our platform, such as: (a) transport, logistics, parcel and courier companies, to deliver the products you purchased, (b) means of payment, intermediaries in the payment or insurance management, to obtain payment for the services or products contracted, as well as to provide you with protection with respect to the products purchased, (c) computer systems providers, cloud service providers, database providers, IT service providers in general, and providers of artificial intelligence, machine learning, or large language model services, such as OpenAI, Anthropic, or Google, which may process limited personal data on Mercado Libre’s behalf to enable, support, and improve certain features or services, (d) call centers or customer service centers, (e) companies that manage fidelity or loyalty programs, to grant you benefits, (f) advertising or marketing companies, (g) data analysis, (h) collection agencies, (i) government entities or companies specialized in risk management, in order to verify your information. These Service Providers only access the data that is strictly necessary to provide with the agreed upon services and cannot use them for purposes other than those entrusted to them by
Mercado Libre.
(ii) "Commercial allies": Companies with financial or commercial activities with which Mercado Libre has a collaborative or an alliance relationship, in order to offer you promotions, products and services of said companies or co-branding. In these cases, Mercado Libre always ensures that confidentiality and security standards are met, by signing agreements or conventions whose purpose is the privacy of our users' personal data and compliance with the applicable legislation.
(iii) "Mercado Libre Group": Companies that belong to our corporate group, which operate under the same internal processes and policies, whether they are companies that are controlled, controlling or affiliated with Mercado Libre, to comply with our internal regulations, prevent fraud, manage risk and facilitate the management of the products and services of Mercado Libre.
(iv) "Counterparty to the transaction": Other users of Mercado Libre platforms, under the conditions provided, with the purpose to put you in contact with the seller or buyer for the sake of the transaction you wish to carry out.
=== END ITEM p0243

=== ITEM p0244
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "collect (operation: collection)", "data": "the personal information that you voluntarily provide to us (e.g. email addresses you give us when you submit a request to a support via our web or email)", "recipient": "", "source": "", "purpose": "", "condition": "Occasionally", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "collect (operation: collection)", "data": "personal Information", "recipient": "", "source": "", "purpose": "", "condition": "CHILDREN'S PRIVACY; from children; with our mobile applications", "condition_predicate": "(user.age < 13 AND user.age < 13 AND service = mobile_apps)"}
--- section of rule 1 and rule 2
THE INFORMATION WE COLLECT
We receive some information automatically when you use our Apps. This includes data about your device, software, operating system, the language you've set for your Device, advertising IDs for advertisement tracking ("Advertising IDs") and your IP address.
In order to try to improve your experience with our games, occasionally we can collect information about how you interact with content and advertisements throughout the application.
We do not collect personally identifiable information about you or your children through our apps. In other words, we do not collect information such as your name, address, phone number or email address.
Occasionally we collect the personal information that you voluntarily provide to us (e.g. email addresses you give us when you submit a request to a support via our web or email).
Cookies
When you visit our website, occasionally we may send cookies to your computer that uniquely identify your browser. We use cookies to improve the quality of our service by storing user preferences and tracking usage information. Most browsers allow you to disable cookies or set your browser to alert you when cookies are being sent to your computer.
Does ORANGE STUDIOS GAMES Collect My Financial Information When I Make In-App Purchases?
When you make in-app purchases in the our Games, we do not collect or have any access to your name and billing information. This information is collected and stored by your platform (Android's Google Play) or your platform's payment processor.
Social media features and tools.
Our Games may include integrated social media features and tools, such as button "Share". Social media features and tools are hosted by a third-party, and your interactions with these integrated social media features and tools are governed by the privacy policy of the company providing it.
CHILDREN'S PRIVACY
Our products respect the privacy of children. We don't collect personal Information from children with our mobile applications.
Our apps for children's do not show Interest-based Advertising.
We comply with the Children's Online Privacy Protection Act (COPPA).
Our website and mobile applications comply with the Children's Online Privacy Protection Act ("COPPA").
In the event that a user identifies himself/herself as a child under the age of 13 through a support request or feedback, we will not collect, store or use and will delete in a secure manner any personal information of such a user.
We take care of filtering categories of sensitive and unsuitable ads for children. But rarely can an advertiser misclassify your ads, and this situation is beyond our reach.
=== END ITEM p0244

=== ITEM p0245
rule 1: {"polarity": "ALLOW", "actor": "GblobalSign", "action": "collected (operation: collection)", "data": "personal data", "recipient": "", "source": "", "purpose": "", "condition": "within Japan", "condition_predicate": "user.jurisdiction = Japan"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "collect (operation: collection)", "data": "personal information", "recipient": "", "source": "minors", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1
The data controller for personal data collected by GblobalSign within Japan is GlobalSign K.K., having it’s registered offices at 
Shibuya Fukuras 9-16F, 1-2-3, Dogenzaka, Shibuya-ku, Tokyo 150-0043, Japan.
--- section of rule 2
The services are not designed for, not marketed to, minors.   We do not knowingly collect or solicit personal information from 
minors, and we do not knowingly allow such persons to use the services.   If you are a minor, please do not attempt to use the 
services or send any information about yourself to us.   In the event that we learn that we have collected personal information 
from a minor without verified parental consent, we will delete that information as quickly as possible.   If you believe we have 
any information from or about a minor, please contact us using the contact information below  
15 Relevant laws
=== END ITEM p0245

=== ITEM p0246
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "provide (operation: disclosure by transmission)", "data": "Personal Information", "recipient": "third parties", "source": "", "purpose": "", "condition": "Cases where we provide Personal Information to third parties as specified in the items of Article 27(5) of the APPI; Cases where we have obtained the prior consent of the Customer etc., to provide the information to third parties; Cases where required by laws and regulations; Cases where it is necessary for the protection of the life, body, or property of an individual and it is difficult to obtain the consent of the individual; Cases where there is a specific need for improving public health or to promote the sound development of children and it is difficult to obtain the consent of the individual; Cases where it is necessary to cooperate with a national agency, a local government, or an individual or entity entrusted by either a national agency or local government to execute affairs prescribed by laws and regulations, and in which obtaining the consent of the individual is likely to impede the execution of such affairs; Cases where we receive an inquiry from a police officer, public prosecutor, public prosecutor’s assistant, national tax official, drug enforcement official, bar association, court, or other party with legal authority to make an inquiry, or when we determine that an emergency evacuation or self-defense is required.", "condition_predicate": "([untranslated: specified in the items of Article 27(5) of the APPI] AND consent.share_third_parties AND law.required AND ([untranslated: it is necessary for the protection of the life, body, or property of an individual] AND [untranslated: it is difficult to obtain the consent of the individual]) AND ([untranslated: there is a specific need for improving public health or to promote the sound development of children] AND [untranslated: it is difficult to obtain the consent of the individual]) AND ([untranslated: it is necessary to cooperate with a national agency, a local government, or an individual or entity entrusted by either a national agency or local government to execute affairs prescribed by laws and regulations] AND [untranslated: obtaining the consent of the individual is likely to impede the execution of such affairs]) AND (event.receive_legal_inquiry OR [untranslated: we determine that an emergency evacuation or self-defense is required]))"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "provide (operation: disclosure by transmission)", "data": "Personal Data", "recipient": "third parties", "source": "", "purpose": "", "condition": "In principle; unless the cases set forth in the paragraphs of this Article and the cases set forth in the following items", "condition_predicate": "([untranslated: In principle] AND NOT policy.permits)"}
--- section of rule 1
Cases where we provide Personal Information to third parties as specified in the items of Article 27(5) of the APPI
Cases where we have obtained the prior consent of the Customer etc., to provide the information to third parties
Cases where required by laws and regulations
Cases where it is necessary for the protection of the life, body, or property of an individual and it is difficult to obtain the consent of the individual
Cases where there is a specific need for improving public health or to promote the sound development of children and it is difficult to obtain the consent of the individual
Cases where it is necessary to cooperate with a national agency, a local government, or an individual or entity entrusted by either a national agency or local government to execute affairs prescribed by laws and regulations, and in which obtaining the consent of the individual is likely to impede the execution of such affairs
Cases where we receive an inquiry from a police officer, public prosecutor, public prosecutor’s assistant, national tax official, drug enforcement official, bar association, court, or other party with legal authority to make an inquiry, or when we determine that an emergency evacuation or self-defense is required.
Provision to payment companies etc. and transfer outside Japan
In order to detect or prevent payment execution and payment abuse, we may provide payment-related User Data to payment-related companies and companies that actually perform payments through payment-related companies (“Payment Companies”; payment-related companies and payment companies are collectively referred to as “Payment Companies etc.”). If a Payment Company etc. used by a Customer etc. is located outside of Japan, this information may be transferred to a third party outside of Japan. In such cases, please check
here
for information on the transfer destination.
Security Control Systems
When handling Personal Information, we take the following strict security measures in accordance with internal rules to prevent loss, falsification, and leakage of Personal Data.
Establishment of basic policy
In order to ensure the proper handling of User Data that falls under the category of Personal Information, we will establish and review as necessary matters such as compliance with related laws, regulations, guidelines etc., matters concerning security control measures, and the contact point for handling complaints, in this Privacy Policy.
Establishment of handling rules for security control of Personal Data
For each stage of obtainment, use, storage, provision, deletion, etc., we will establish rules regarding handling methods, responsible persons, persons in charge, and their duties, etc., and review them as necessary.
Organizational security control measures
In addition to appointing a person responsible for the handling of Personal Data, we will clarify the employees who handle Personal Data and the scope of Personal Data handled by such employees, and establish a system for reporting to the person responsible in the event that we become aware of facts or signs of any violation of laws or handling rules.
Personnel security control measures
We educate our employees on the matters to keep in mind regarding the handling of Personal Data.
Physical security control measures
We take the following measures for physical security control:
Management of Personal Data handling areas, etc.
Measures to be taken in the event of theft of equipment or electronic media, etc.
Prevention of leakage etc. when carrying electronic media, etc.
Establishment and implementation of rules for deletion of Personal Data and disposal of equipment, electronic media, etc.
--- section of rule 2
(2) Purpose of use of User Data that falls under “Specific Personal Information”
(i) “Specific Personal Information” in this item refers to Personal Information of our officers and employees (collectively, “Employees etc.”) and their dependents, etc. that relates to the personal numbers and Specific Personal Information of Employees etc. and their dependents.
(ii) We use such Specific Personal Information to perform the following operations.
Administrative work relating withholding tax
Administrative work relating to preparation of application forms for exemption for dependents, deduction for insurance premiums, and special exemption for spouse of employment income earner
Administrative work relating preparation of tax returns relating to retirement income
Administrative work relating individual inhabitant tax
Administrative work relating to employment insurance
Administrative work relating to health insurance and employees’ pension insurance
Notification of National Pension Plan No. 3 insured persons
Administrative work relating to preparation of payment records for remuneration, fees, etc.
(iii) We do not provide Specific Personal Information to any third party, except in cases permitted under the Act on the Use of Numbers to Identify a Specific Individual in Administrative Procedures.
Entrustment of Operations Involving Personal Information
We may entrust all or part of the operations handling Personal Data to third parties to the extent necessary to achieve the “Purposes of Use.” Such entrustment may include companies outside of Japan.
The companies
to which we currently entrust operations outside of Japan are listed .
We select service providers that are found to handle Personal Data appropriately and ensure that Personal Data is properly managed when contracting with such service providers.
Sharing of Personal Data
We share your Personal Data as follows. Please note that for the purpose of sharing, your Personal Data will be shared only with our group companies to the extent necessary, and not necessarily with all of our group companies.
In the event that laws, regulations, guidelines, etc. apply to the provision of Personal Data, we will comply with such laws and regulations etc. and take appropriate measures, and will not share Personal Data except as permitted by laws and regulations.
(1) Items of Personal Data to be shared
Items registered with us by Users or transaction counterparties
Identification information of Users and transaction counterparties
Any and all items registered by the Users on the Services
information about our employees
(2) Scope of joint Users
Pixiv Inc.
Incolore Corporation
Pixiv Marketing, Inc.
Pixiv Technologies, Inc.
Pixiv Qualia Inc.
(3) Purpose of use in case of sharing
Please refer to the
“Purposes of Use”
section of this Privacy Policy for the purposes for which Personal Data may be shared.
(4) Person responsible for sharing
4-23-5 Sendagaya, Shibuya-ku, Tokyo
Pixiv Inc.
Yasuhiro Niwa
Provision of Personal Data to Third Parties
Cases of provision of Personal Data to third parties
In principle, we do not provide Personal Data to third parties (provision of Personal Data to a third party is hereinafter referred to as “Provision of Personal Data to Third Parties”); provided, however, that this excludes the cases set forth in the paragraphs of this Article and the cases set forth in the following items.
=== END ITEM p0246

=== ITEM p0247
rule 1: {"polarity": "ALLOW", "actor": "Our", "action": "collecting (operation: collection)", "data": "that information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "collect (operation: collection)", "data": "personal information", "recipient": "", "source": "children under 13 years of age", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1 and rule 2
Privacy Policy Multi Product
Privacy Policy - Multi-Product
Effective Date: March 6, 2022
Last
Updated: September 14, 2026
Introduction
Triumph Labs, Inc., and its affiliates (including, without limitation, "Triumph Arcade, LLC", "Triumph TCG, LLC", and the European subsidiaries referenced in our Arcade Terms of Use (SIA Triumph Arcade Europe (EU) and Triumph Arcade UK LTD (UK)), (collectively, "The Company") take your privacy seriously. The Company is committed to protecting it through our compliance with this policy.
The Company develops and publishes software that allows for the purchase of products, the entry into various tournaments to the players of such games (each a “Player” and together “Players”), this policy covers all information collected using Triumph’s software, including:
(i) leaderboards that publish Player scores in a given game category or multi-game category (”Leaderboards”);
(ii) match-making between real players which may or may not include leaderboard functionality (”Match-Making”);
(iii) real-cash prize tournaments and other real-cash prize games, including, in certain cases offering of leaderboards, match-making, and the creation and development of real-cash entry prize structures for each tournament or game with a prize (”Real Cash Tournaments”);
(iv) the purchasing and selling of collectible goods (the "Collectible Transaction").
In each case an application that integrates the Company software is referred to as an “App” in this Privacy Policy and the Company software that is integrated into each App the “Triumph SDK” - in most cases the App and the Company Software are indistinguishable and are operated together by the Company.
This policy describes:
The types of information we may collect or that you may provide when you register with, access, use, or transact with an App, the Company website, or the Triumph SDK.
Our practices for collecting, using, maintaining, protecting, and disclosing that information.
This policy applies to information we collect in the Triumph SDK, the App, from our website, and in electronic communications sent through or in connection with any of the foregoing. This policy DOES NOT apply to information that you provide to or is collected by any third party.
Third parties have their own privacy policies, which we encourage you to read before providing information on or through them.
Please read this policy carefully to understand our policies and practices regarding your information and how we will treat it. If you do not agree with our policies and practices, do not download, register with, or use a Company App or the Triumph website. By downloading, registering with, or using the Website or the App, you agree to this Privacy Policy. This policy may change from time to time (see Changes to Our Privacy Policy). Your continued use of the Company App or Website after we revise this policy means you accept those changes, so please check the policy periodically for updates.
Age Limits.
Certain features of the App are not intended for all age groups. For the Leaderboard and Match-Making products the Company uses an age-gate to determine the age of a user. If a person is under the age of 13 certain features will not be available, for example, the uploading of avatars, the changing of default username, and reuse of a username in multiple sessions (together the features available after such restriction being referred to as “Anonymous Mode”) in order to ensure that no data is collected from such users.
If a user is under 18 years of age Leaderboard and Match-Making will be available but the Real Cash Tournaments feature and the Collectible Transaction feature will not be available.
We do not knowingly collect personal information from children under 13 years of age. If we learn we have collected or received personal information from a child under 13, we will delete that information.
=== END ITEM p0247

=== ITEM p0248
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "collect (operation: collection)", "data": "email address", "recipient": "", "source": "", "purpose": "", "condition": "When you create an account", "condition_predicate": "event.create_account"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "ask for (operation: collection)", "data": "email address", "recipient": "", "source": "", "purpose": "", "condition": "12. Residents of the European Union; 12.3. Meet Legitimate Interest; unless you want to create an account with us", "condition_predicate": "(user.jurisdiction = European Union AND basis.legitimate_interests AND NOT [untranslated: you want to create an account with us])"}
--- section of rule 1
1. How we collect your information
We collect information only when we need to collect certain information to provide the service you are using. The type of information and its use depends on the service you are using and how you use it. We collect the information you voluntarily provide us to use our services and the information we obtain from other sources.
1.1. The information you provide us
When you send us a message using an online form or contact us by email or phone, or subscribe to our mailing list, we may collect your email address, phone number, name, and other personal information that you provide us. We also collect any information that you voluntarily provide to help us resolve any issues within our service.
Account Information
When you create an account, we collect the personal information you provide, like your full name, email address, phone number, birthday, and photo.
Information you upload
We collect information about other people, like photos, videos, phone numbers, email addresses, that you may upload to our services. For example, you may upload your contacts to see which of your friends are already playing a game, or invite them to try a new app. Or, you may upload a photo to our service for editing or sharing with other users.
The content you create & share
When you use our service, we collect the content that you create, upload, share, and the content that others have shared with you. Content means all kinds of text, files, and digital information that you upload, documents you create, the messages you send, posts you write, comments you make, and opinions you share using our service.
1.2. The information we automatically collect
When you use our services, we collect information about the browser or apps you used to access our services, information about your device, network, operating system, and crash reports. We may also collect unique identifiers about your device or browser using cookies or other technologies.
Usage Information
We also collect information about how your browser or apps communicated with our servers, including your public IP address, date and time of interaction, the referrer URL in our server logs. We use server logs, device logs, event logs, cookies, local storage, device cache, and databases to collect, transmit, and store information.
Information from installed apps
When you install our desktop app or mobile app, the app may occasionally send information about your device and network status, and how you are using it. The apps may upload information stored on your device to keep the previously uploaded content up to date with your consent.
Information about your device
We may collect information about your device's wireless and mobile network connections, such as available Wi-Fi access points, network service provider, IP address, signal strength, and mobile phone number. We may also collect information from your device's sensors, such as accelerometers and gyroscopes.
Information stored on your device
Some of our services may ask for additional information stored on your device to function fully. We may collect information stored on your device's storage, such as your contacts and photos, with your permission.
Information about your location
Our services may occasionally collect information about your approximate location. Some of our services may also use GPS, wireless networks, cell towers, and Wi-Fi access points to determine your precise location with your permission.
1.3. Information from other sources
We may also collect information about you from public sources, and when service providers, marketing partners, security researchers, or other users of our services provide us with that information. For example, another user of our service may upload their contact list, which includes your information.
We collect such information to prevent abuse of our services, improve our services, identify business opportunities, and provide services to our users.
--- section of rule 2
12. Residents of the European Union
The residents of the European Union (EU) can exercise their rights of access, deletion, correction, and portability as described in the
"Your control over your information
" section above. Please note that Yarsa Labs Private Limited is the controller of your personal information.
Your country requires us to only collect and use your information if we have a "legal basis" to do so. Here are the conditions in which we collect and use your information.
12.1. Performance of Contract with you
By using our services you enter into an agreement with us that governs your use of our services. For example, when you create an account with us and accept our Terms of Service, we need to collect your personal information to maintain your account and authenticate you in the future according to the agreement.
12.2 Upon your Consent
Some of our services ask your permission to collect your information to improve your experience. For example, our services may ask for your permission to read your contacts to find people in your contact list who already use our service. When you give your explicit consent, we collect and use that information according to this privacy policy.
12.3. Meet Legitimate Interest
When we have a legitimate interest to collect information from you, we try to collect as little information as possible to meet that interest. For example, unless you want to create an account with us, we do not ask for your name and email address; you can use our services without providing your personal information. When you use our services, our service providers may collect the information they need from you to meet their legitimate business interests. For example, our advertising partners may collect analytics data to display relevant ads based on your interests.
12.4. Compliance with Law
We may use your information to comply with the local laws that govern us, and your local laws that govern your use of our service. We may also use your information to protect other users, and comply with legal obligations.
12.5. Exercise Legal Rights
We may use your information to exercise our legal rights to protect our services and users.
=== END ITEM p0248

=== ITEM p0249
rule 1: {"polarity": "ALLOW", "actor": "Company", "action": "transfer (operation: disclosure by transmission)", "data": "Your Personal Data", "recipient": "", "source": "", "purpose": "", "condition": "Your Rights under the GDPR; by law if You are within the EU; Request the transfer of Your Personal Data", "condition_predicate": "(user.jurisdiction = European Economic Area AND (law.required AND user.jurisdiction = European Union) AND request.portability)"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "transfer (operation: disclosure by transmission)", "data": "any of your personal data", "recipient": "third parties", "source": "", "purpose": "", "condition": "unless as provided in this privacy policy", "condition_predicate": "NOT policy.permits"}
--- section of rule 1
That information is provided directly to Our third-party payment processors whose use of Your personal information is governed by their Privacy Policy. These payment processors adhere to the standards set by PCI-DSS as managed by the PCI Security Standards Council, which is a joint effort of brands like Visa, Mastercard, American Express and Discover. PCI-DSS requirements help ensure the secure handling of payment information.
• Apple Store In-App Payments
Their Privacy Policy can be viewed at
https://www.apple.com/legal/privacy/en-ww/
• Google Play In-App Payments
Their Privacy Policy can be viewed at
https://www.google.com/policies/privacy/
• PayPal
Their Privacy Policy can be viewed at
https://www.paypal.com/webapps/mpp/ua/privacy-full
• PayPal
Their Privacy Policy can be viewed at
https://www.braintreepayments.com/legal/braintree-privacy-policy
• WeChat
Their Privacy Policy can be viewed at
https://www.wechat.com/en/privacy_policy.html
• Alipay
Their Privacy Policy can be viewed at
https://render.alipay.com/p/f/agreementpages/alipayglobalprivacypolicy.html
When You use Our Service to pay a product and/or service via bank transfer, We may ask You to provide information to facilitate this transaction and to verify Your identity.
GDPR Privacy
Legal Basis for Processing Personal Data under GDPR
We may process Personal Data under the following conditions:
Consent
: You have given Your consent for processing Personal Data for one or more specific purposes.
Performance of a contract
: Provision of Personal Data is necessary for the performance of an agreement with You and/or for any pre-contractual obligations thereof.
Legal obligations
: Processing Personal Data is necessary for compliance with a legal obligation to which the Company is subject.
Vital interests
: Processing Personal Data is necessary in order to protect Your vital interests or of another natural person.
Public interests
: Processing Personal Data is related to a task that is carried out in the public interest or in the exercise of official authority vested in the Company.
Legitimate interests
: Processing Personal Data is necessary for the purposes of the legitimate interests pursued by the Company.
In any case, the Company will gladly help to clarify the specific legal basis that applies to the processing, and in particular whether the provision of Personal Data is a statutory or contractual requirement, or a requirement necessary to enter into a contract.
Your Rights under the GDPR
The Company undertakes to respect the confidentiality of Your Personal Data and to guarantee You can exercise Your rights.
You have the right under this Privacy Policy, and by law if You are within the EU, to:
Request access to Your Personal Data
. The right to access, update or delete the information We have on You. Whenever made possible, you can access, update or request deletion of Your Personal Data directly within Your account settings section. If you are unable to perform these actions yourself, please contact Us to assist You. This also enables You to receive a copy of the Personal Data We hold about You.
Request correction of the Personal Data that We hold about You
. You have the right to to have any incomplete or inaccurate information We hold about You corrected.
Object to processing of Your Personal Data
. This right exists where We are relying on a legitimate interest as the legal basis for Our processing and there is something about Your particular situation, which makes You want to object to our processing of Your Personal Data on this ground. You also have the right to object where We are processing Your Personal Data for direct marketing purposes.
Request erasure of Your Personal Data
. You have the right to ask Us to delete or remove Personal Data when there is no good reason for Us to continue processing it.
Request the transfer of Your Personal Data
.
--- section of rule 2
IDFA);
Time zone;
Device mute status (related to reminder function)
In order to provide a better user experience, we have integrated data statistics tools in the App, they won't collect users’ health data or privacy data and are only used for CRASH targeting and AB-testing for new features and design,The details are as follows:
Device information
Screen Size
OEM Name
Model
Device system information
OS Name
OS Version
OS Build
Time Zone
System Language
Carrier Country
Carrier Name
Location information
Locale
Country Area
Application information
App Name
App Build
APP Version Number
SDK Name
SDK Version
Information from Third-Party Social Media Services
The Company allows You to create an account and log in to use the Service through the following Third-party Social Media Services:
Google
Facebook
If You decide to register through or otherwise grant us access to a Third-Party Social Media Service, We may collect Personal data that is already associated with Your Third-Party Social Media Service's account, such as Your name, Your email address, Your activities or Your contact list associated with that account.
You may also have the option of sharing additional information with the Company through Your Third-Party Social Media Service's account. If You choose to provide such information and Personal Data, during registration or otherwise, You are giving the Company permission to use, share, and store it in a manner consistent with this Privacy Policy.
App Permission Involved
Physical activity Permission
When you are using the pedometer feature, this permission enables us to access your Physical Activity, track and record your step data.
Storage Permission
When you are using the pedometer feature, this permission enables us to access your local media to store your step data. Please note that we will never modify or delete the content in your local media storage.
Location Permission
When you are using the pedometer feature, this permission enables us to get your location for tracking and counting your steps accurately. We will ask if you allow us to get this permission, and you could disable this permission at any time.
Google Fit
You may allow us to synchronize your data from Google Fit. This permission enables you to have a better App experience. You could disable this connection and stop the automatic updating of your personal information to your Google Fit account at any time. Besides, we will never upload your data from Google Fit.
Your Consent and Our Use of Your Personal Data
By creating a profile or registering to use our apps, you expressly agree to:
We may process the health data you provide by using the app to import or export the data with third-party services, such as Apple HealthKit and Google Fit.
We may process the account data you provide by using the app and create it through your account only for the purposes of login or registration, third-party services, such as Apple ID, Google account and Facebook account.
Except as provided in this privacy policy, we will not transfer any of your personal data to third parties.
The Company may use Personal Data for the following purposes:
To provide and maintain our Service
, including to monitor the usage of our Service.
To manage Your Account
: to manage Your registration as a user of the Service. The Personal Data You provide can give You access to different functionalities of the Service that are available to You as a registered user.
For the performance of a contract
: the development, compliance and undertaking of the purchase contract for the products, items or services You have purchased or of any other contract with Us through the Service.
=== END ITEM p0249

=== ITEM p0250
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "collect (operation: collection)", "data": "personal information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "collect (operation: collection)", "data": "personal information", "recipient": "", "source": "children under 13", "purpose": "", "condition": "from children under 13; unless prior parental consent", "condition_predicate": "(user.age < 13 AND NOT user.parental_consent)"}
--- section of rule 1
Bank of America U.S. Online Privacy Notice
(Last updated June, 2025)
Your privacy is important to us. We conduct regular assessment reviews and abide by rigorous privacy standards to ensure personal information we collect, use and share is protected. This U.S. Online Privacy Notice ("Notice") describes how Bank of America and our affiliates manage personal information about you when you interact with us online through our websites, event registration sites, mobile applications and social sites ("Sites and Mobile Apps") through your computer, smartphone, tablet or other mobile devices ("computer or mobile devices").
This Notice explains
How we collect personal information when you visit, use or interact with us online, and through our ads displayed through online services operated by us or non-affiliated third parties.
How we may use or share personal information collected to deliver products and services to you and for advertising or event management purposes.
The term "Bank of America" or "we", "us" or "our" in this Notice refers to banking and non-banking U.S. affiliates or subsidiaries of Bank of America Corporation that link to or reference this Notice.
By using our Sites and Mobile Apps, you agree to the terms and conditions of this Notice. Our U.S. online services covered by this Notice are intended for a U.S. audience. If you visit or use one of our online services, your information may be transferred or processed in the U.S. For Non-U.S. online services, please review the privacy policy applicable to that service to understand how your information is collected, used and shared.
Bank of America works with third-party providers who are contractually obligated to comply with our policies to protect information. However, if you visit or access one of these third-party provider sites or mobile apps, please review the online privacy practices of that site or mobile app to understand the specifics of how your online personal information may be collected, used and shared.
Updates to this Notice
This Notice is subject to change. We update this Notice periodically to comply with the most recent federal and local laws. Please review it whenever you have questions. If we make changes to this Notice, we will revise the
Last updated
date on this page.
Download our U.S. Online Privacy Notice in English (PDF)
Download our U.S. Online Privacy Notice in Spanish (PDF)
Our Online Privacy Practices
We are committed to transparency about your personal information. We ask for your consent when required, otherwise by using our Site and Mobile Apps, you consent to the collection, use and sharing of your personal information subject to and consistent with applicable laws, regulations and other notices you may have received based on your relationship with us.
Linking to other sites
We may provide links to non-affiliated third-party sites, such as credit bureaus, service providers or merchants. If you follow links to sites not affiliated with, or controlled by Bank of America, you should review their privacy and security policies and other terms and conditions, as they may be different from those of our Sites and Mobile Apps. Bank of America does not guarantee and is not responsible for the privacy or security of these sites, including the accuracy, completeness or reliability of their information.
Protecting your personal information
To protect personal information from unauthorized access and use, we use security measures that comply with applicable federal and state laws. These measures may include device safeguards and secured files and buildings as well as oversight of our third-party providers to ensure personal information remains confidential and secure. In the event of a data breach, we provide timely notification, in accordance with applicable laws and regulations.
We recognize the importance of protecting privacy where children are involved. Our Sites and Mobile Apps are not marketed to individuals under the age of 13.
--- section of rule 2
Accounts that include online access for children under the age of 13 are owned by a parent or guardian and require specific consent for online access. We do not knowingly collect personal information from children under 13 without prior parental consent. Read our
Children's Privacy Policy
for more information.
Making sure personal information is accurate
Keeping your personal information accurate and up to date is very important. If your personal information is incomplete, inaccurate or not current, please use the
Contact Us
option on our Sites and Mobile Apps, or call or write to us at the telephone numbers or appropriate address for changes listed on your account statements, records, online or other account materials. You can also speak to a customer representative at a financial center, your Financial Advisor or account representative.
Personal Information We Collect Online
How do we collect personal information online?
We collect personal information about you through your computer or mobile devices by the use of cookies and similar tracking technologies (see our
Cookie Policy (PDF)
for details) as well as personal information you provide when you visit or use our Sites and Mobile Apps, for example when you:
Apply for or open a new account
Register for a new product or service, or request information about a product or service
Register as a participant in one of our events
Complete a survey, contest or sweepstakes or other promotion
Use aggregation services such as My Portfolio® and My Financial Picture® in order to consolidate your financial account or information at one online location
We may use third-party providers to process personal information for business purposes on our behalf. Third-party providers are contractually obligated to comply with our policies to protect information we share with them or they collect on our behalf.
We also may obtain personal information from a sponsor for individuals onboarded via a Commercial Prepaid card program with us. If we combine such personal information with information collected through the Mobile Services, we will treat the combined information as personal information in accordance with this Notice.
The personal information we collect is limited to what is required to provide our products or services and to support legal and risk requirements. For additional information, please review the
How We Use and Share Personal Information
section of this Notice.
Types of personal information we collect online
The type of personal information we collect from and about you online will depend on how you interact with us and may include:
Contact Information
such as name, mailing address, email address, telephone and mobile number(s).
Account Application information
such as credit and income information.
Identifiers
such as Social Security number, account number(s), driver's license number (or comparable) or other information that identifies you for ordinary business purposes.
Access Authorization
such as user ID, alias, PIN and password and security questions and answers.
Documents or images
submitted via our Site or Mobile Apps to support account opening, such as statements and voided checks.
Debit/Credit Card Information
such as card number, expiration date, CVV2, billing address.
=== END ITEM p0250

