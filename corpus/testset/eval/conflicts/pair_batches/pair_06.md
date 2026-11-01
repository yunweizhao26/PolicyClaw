=== ITEM p0126
rule 1: {"polarity": "ALLOW", "actor": "We", "action": "disclose (operation: disclosure)", "data": "Your personal data", "recipient": "", "source": "", "purpose": "", "condition": "10. NOTICE TO CALIFORNIA RESIDENCE", "condition_predicate": "user.jurisdiction = California"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "share (operation: disclosure)", "data": "Your personal data", "recipient": "affiliates", "source": "", "purpose": "for their direct marketing purposes", "condition": "10. NOTICE TO CALIFORNIA RESIDENCE", "condition_predicate": "user.jurisdiction = California"}
--- section of rule 1 and rule 2
10. NOTICE TO CALIFORNIA RESIDENCE
Under California Civil Code sections 1798.83, “Shine the Light Act”, California residents are entitled to ask Us for a notice describing what categories of personal data We share with third parties or corporate affiliates for those third parties or corporate affiliates’ direct marketing purposes. Please note that We do not share Your personal data with any third parties or affiliates for their direct marketing purposes.
CCPA provides consumers who are California residents with specific rights regarding their personal data.
Right to Access:
If You are a California resident, You have the right to request, up to two times each year, access to categories and specific pieces of Your personal data that We collect, use and/or disclose.
Right to Delete:
If You are a California resident, You have the right to request that We delete Your personal data that We collect, subject to applicable legal exceptions.
Right to Opt Out of Sale of Personal Information:
As the term is defined by the CCPA, Toca Boca does not sell any personal data.
To make a request regarding Your rights under CCPA as described above, please send an email to
privacy@tocaboca.com
or
DPO@spinmaster.com
or write to us, using the addresses above.
=== END ITEM p0126

=== ITEM p0127
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "use (operation: use)", "data": "such data", "recipient": "", "source": "", "purpose": "only for the legally permitted purposes described above", "condition": "When we process information that is considered “sensitive” under State Privacy Laws (such as when such information is included in your user content); in the same way we process user content generally", "condition_predicate": "([untranslated: When we process information that is considered “sensitive” under State Privacy Laws (such as when such information is included in your user content)] AND [untranslated: in the same way we process user content generally])"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "engage in ... targeted advertising using (operation: use)", "data": "personal information", "recipient": "", "source": "", "purpose": "targeted advertising", "condition": "about anyone we know to be under the age of 18", "condition_predicate": "user.age < 18"}
--- section of rule 1 and rule 2
Use, Disclosure, and Retention of Personal Information for Business Purposes
Category of Personal Information
Uses of Personal Information
Category of Recipients
• Account information (which includes identifiers, such as your email address and account ID)
• Payment information (which includes commercial information, such as records of products purchased)
• Voice data (which includes recordings to create transcriptions of communications captured through our services)
• Communications with us and feedback (which includes survey responses and interactions with our customer support or sales teams)
• Technical information and usage data (which includes internet or other electronic network activity information, such as your activity on our websites and apps and device and browser information, and identifiers, such as your IP address)
• Cookie information (which includes identifiers, such as Cookie IDs)
• Professional information (which includes your job title or industry, which we may license from others)
• Inferences (which includes predictions, such as your approximate location based on your IP address)
• User content
• Provide and tailor our products to you;
• Improve our products and build new ones;
• Develop and improve AI (subject to your settings);
• Secure our products and troubleshoot problems;
• Process payments;
• Communicate with you and provide customer service;
• Market our products to you (excluding user content); and
• Handle compliance issues and protect against harm.
• The Superhuman family of companies;
• Trusted service providers;
• Marketplace participants;
• Government, legal, and similar authorities;
• Recipients in connection with a merger, acquisition, or similar transaction; and
• Others with your consent or at your direction.
When we process information that is considered “sensitive” under State Privacy Laws (such as when such information is included in your user content), we use such data only for the legally permitted purposes described above, in the same way we process user content generally. We similarly limit how we process account log-in information and contents of communications not sent to us, which may be considered “sensitive” under certain State Privacy Laws. We do not use or disclose such information for the purpose of inferring characteristics about you.
Above, we describe that we
collect
personal information from various sources, including directly from you, automatically when you access or use our products, and from other sources, as well as the purposes and time periods for which we
retain
personal information.
Sales, Sharing, and Targeted Advertising
To promote our products on third-party websites and services, we disclose the following categories of personal information to the following categories of recipients. These disclosures may be considered “sales”, “sharing”, or use of personal information for “targeted advertising” under State Privacy Laws.
Category of Personal Information Disclosed
Category of Third-Party Recipient
• Identifiers (such as cookie IDs, IP addresses, or unique IDs generated from your email address or phone number)
• Internet or other electronic network activity information (such as links you click or pages you visit on a Superhuman marketing website)
• Commercial information (such as product purchase information)
• Inferences (such as predictions about your interest in certain products we offer based on your usage data)
• Advertising networks;
• Social networks
We do not engage in sales, sharing, or targeted advertising using personal information about anyone we know to be under the age of 18.
Your Rights under State Privacy Laws
Opt-Out Rights
You may opt out of activities that we engage in that may constitute “targeted advertising”, “sharing”, or “sales” of personal information under the State Privacy Laws.
=== END ITEM p0127

=== ITEM p0128
rule 1: {"polarity": "ALLOW", "actor": "Chipotle Mexican Grill, Inc. and its subsidiaries and affiliates in the United States (“Chipotle”, “we”, “our”, “us”)", "action": "collect (operation: collection)", "data": "personal information", "recipient": "", "source": "", "purpose": "", "condition": "of visitors who access or interact with our mobile application (“App”) or our websites (“Websites”) that link to this Privacy Policy, as well as other personal information about our customers; applicable to all consumers in the United States (US); unless our employees and contractors in the United States and for customers and employees in the European Union, United Kingdom, and Canada; job applicants in the United States, European Union, United Kingdom, and Canada; our former employees and their family members, dependents, and beneficiaries", "condition_predicate": "(((user.category = website visitor AND (service = mobile application OR service = websites)) OR user.category = customer) AND (user.category = consumer AND user.jurisdiction = United States) AND NOT (((user.category = employee OR user.category = contractor) AND user.jurisdiction = United States) OR ((user.category = customer OR user.category = employee) AND (user.jurisdiction = European Union OR user.jurisdiction = United Kingdom OR user.jurisdiction = Canada))) AND NOT (user.category = job applicant AND (user.jurisdiction = United States OR user.jurisdiction = European Union OR user.jurisdiction = United Kingdom OR user.jurisdiction = Canada)) AND NOT (user.category = former employee OR [untranslated: their family members, dependents, and beneficiaries]))"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "seek to collect (operation: collection)", "data": "personal information", "recipient": "", "source": "from any person under 13 years of age through the Services", "purpose": "", "condition": "The online Services are not intended for, and are not intentionally targeted to, children under 13", "condition_predicate": "user.age < 13"}
--- section of rule 1
Chipotle - Privacy Policy
CHIPOTLE’S U.S. PRIVACY POLICY, INCLUDING CALIFORNIA PRIVACY RIGHTS
(LAST UPDATED APRIL 8, 2026)
PARA VER NUESTRA POLÍTICA DE PRIVACIDAD EN ESPAÑOL,
HAGA CLIC AQUÍ
This “Privacy Policy” describes how Chipotle Mexican Grill, Inc. and its subsidiaries and affiliates in the United States (“Chipotle”, “we”, “our”, “us”) may collect, use, and disclose personal information of visitors who access or interact with our mobile application (“App”) or our websites (“Websites”) that link to this Privacy Policy, as well as other personal information about our customers. The App, those Websites, our restaurants, and our related service offerings are referred to in this Privacy Policy as our “Services.” This Privacy Policy is applicable to all consumers in the United States (US). We maintain separate privacy policies and notices for our employees and contractors in the United States and for customers and employees in the European Union, United Kingdom, and Canada. We also maintain a separate Applicant Privacy Notice that is applicable to job applicants in the United States, European Union, United Kingdom, and Canada. This Privacy Policy also does not apply to our former employees and their family members, dependents, and beneficiaries; if you are a California resident who is a current or former Independent Contractor (as that term is defined in the California Consumer Privacy Act (CCPA)) or employee of Chipotle or a family member, dependent, or beneficiary of any of our current or former employees, you may request access to our employee and contractor privacy policies and notices by navigating to the policies link within Chipotle’s intranet or by
sending an email to
privacy@chipotle.com
.
Notice at Collection
We collect personal information as detailed below and in our
Privacy Policy
. To learn more, including how you can opt-out of the sale or sharing of your personal information, please see the “
Your State Privacy Rights and Additional Disclosures
” section below.
--- section of rule 2
6.
PRIVACY FOR THOSE UNDER THE AGE OF 18
The online Services are not intended for, and are not intentionally targeted to, children under 13, and we do not knowingly request or seek to collect personal information from any person under 13 years of age through the Services. If we learn that the online Services have received personal information directly from a child who is under the age of 13, we will delete the information in accordance with applicable law.
The account settings for individuals who indicate they are age 13-17 (“Minors”) will be set to high privacy selections by default. Minors will not receive marketing emails, text messages, push notifications, personalized marketing, personalized experience, or have their precise geolocation utilized/have their personal information sold or shared with non-service provider third parties unless they opt in/consent to these respective options. Once an individual turns 18, their account will automatically be enrolled in personalized experience and marketing.
=== END ITEM p0128

=== ITEM p0129
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "process (operation: processing)", "data": "your personal data", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "process (operation: processing)", "data": "corresponding personal data", "recipient": "", "source": "", "purpose": "", "condition": "When we receive your withdrawal of consent", "condition_predicate": "event.receive_withdrawal_of_consent"}
--- section of rule 1
1. Overview
APUS Launcher (this “Product”) is smart phone user system developed, operated and managed by Beijing Qilin Hesheng Network Technology Co.,ltd. (“APUS” “We” or “us”). We fully respect and protect users’ personal privacy. While providing you with quality services, we will collect, use, disclose, store and protect your personal data in accordance with this Privacy Policy (the “Policy”).
We will explain how we process your personal data in this Policy and how you may access and control your personal data.
Please completely read and fully understand this Policy before using this Product. If you have any questions about this Policy, or have any complaints or suggestions, please contact us via the methods as described in this Policy. This policy will help you understand the followings:
--- section of rule 2
7. How You Access and Control Your Personal Data
7.1. Access and revise your personal data
You may access and edit your personal data online through APUS User Information Center.
7.2. Change of y
our
a
uthorization
s
cope
You may select on the page of APUS User Information Center to change your authorization scope for us to process your personal data. Please be minded that since all functions of the Product need certain basic personal data for normal operation, certain functions of the Product may not operate normally when you withdraw your consent to processing of some personal data.
When we receive your withdrawal of consent, we will no longer process your corresponding personal data.
7.3. Rejection of p
ersonalized
advertising
You may always choose whether to receive promotional emails, messages, calls, and mails from us or third parties. You may also choose to no longer receive personalized advertisements through APUS User Information Center.
We will no longer use your personal data for the above-mentioned commercial promotion purposes when you refuse to receive personalized advertisements.
7.4. Delete your personal data
You may submit a request to us to delete your personal data when:
a) Your personal data is no longer necessary for data collection or processing;
b) You have withdrawn your consent to our processing of your personal data ;
c) Your personal data has been processed illegally;
d) We are obligated to delete your personal data in accordance with the laws of EU members.
We may not be able to delete your personal data immediately due to technical reasons. We will delete it during the next system update. We will not process your personal data in any way during the period between your request of deleting your personal data and the next system update.
7.5. Respond to your requests
We may first verify your identity upon receipt of your request, and may request you to provide the necessary information for authentication.
We will respond to your request on the 30th day after we receive your request and communicate with you in an appropriate way. If necessary, we may extend it (by an additional 30-day at most), and will inform you of the reason for the extension of the deadline on the 30th day after receiving your request. If we have reasonable reasons to believe that no measures are needed to respond your request, we will inform you of our decision 30 days from the date of receipt of your request and provide you with appropriate explanation.
We will use best efforts to help you resolve relevant problems. If you are not satisfied with the response you received, you may refer the complaint to the relevant regulatory authority, or file a lawsuit before a competent judicial authority.
=== END ITEM p0129

=== ITEM p0130
rule 1: {"polarity": "ALLOW", "actor": "", "action": "selling (operation: sale)", "data": "Personal Data", "recipient": "", "source": "", "purpose": "for collecting or selling the Personal Data", "condition": "if You are a resident of California", "condition_predicate": "user.jurisdiction = California"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "sell (operation: sale)", "data": "personal information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1 and rule 2
We will provide to You, or to a third-party You have chosen, Your Personal Data in a structured, commonly used, machine-readable format. Please note that this right only applies to automated information which You initially provided consent for Us to use or where We used the information to perform a contract with You.
Withdraw Your consent
. You have the right to withdraw Your consent on using your Personal Data. If You withdraw Your consent, We may not be able to provide You with access to certain specific functionalities of the Service.
Exercising of Your GDPR Data Protection Rights
You may exercise Your rights of access, rectification, cancellation and opposition by contacting Us. Please note that we may ask You to verify Your identity before responding to such requests. If You make a request, We will try our best to respond to You as soon as possible.
You have the right to complain to a Data Protection Authority about Our collection and use of Your Personal Data. For more information, if You are in the European Economic Area (EEA), please contact Your local data protection authority in the EEA.
CCPA Privacy
Your Rights under the CCPA
Under this Privacy Policy, and by law if You are a resident of California, You have the following rights:
The right to notice
. You must be properly notified which categories of Personal Data are being collected and the purposes for which the Personal Data is being used.
The right to access / the right to request
. The CCPA permits You to request and obtain from the Company information regarding the disclosure of Your Personal Data that has been collected in the past 12 months by the Company or its subsidiaries to a third-party for the third party's direct marketing purposes.
The right to say no to the sale of Personal Data
. You also have the right to ask the Company not to sell Your Personal Data to third parties. You can submit such a request by visiting our "Do Not Sell My Personal Information" section or web page.
The right to know about Your Personal Data
. You have the right to request and obtain from the Company information regarding the disclosure of the following:
The categories of Personal Data collected
The sources from which the Personal Data was collected
The business or commercial purpose for collecting or selling the Personal Data
Categories of third parties with whom We share Personal Data
The specific pieces of Personal Data we collected about You
The right to delete Personal Data
. You also have the right to request the deletion of Your Personal Data that have been collected in the past 12 months.
The right not to be discriminated against
. You have the right not to be discriminated against for exercising any of Your Consumer's rights, including by:
Denying goods or services to You
Charging different prices or rates for goods or services, including the use of discounts or other benefits or imposing penalties
Providing a different level or quality of goods or services to You
Suggesting that You will receive a different price or rate for goods or services or a different level or quality of goods or services.
Exercising Your CCPA Data Protection Rights
In order to exercise any of Your rights under the CCPA, and if you are a California resident, You can email or call us or visit our "Do Not Sell My Personal Information" section or web page.
The Company will disclose and deliver the required information free of charge within 45 days of receiving Your verifiable request. The time period to provide the required information may be extended once by an additional 45 days when reasonable necessary and with prior notice.
Do Not Sell My Personal Information
We do not sell personal information. However, the Service Providers we partner with (for example, our advertising partners) may use technology on the Service that "sells" personal information as defined by the CCPA law.
=== END ITEM p0130

=== ITEM p0131
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "collect (operation: collection)", "data": "Sensitive Personal Data or Information (as defined below)", "recipient": "", "source": "", "purpose": "for a lawful purpose connected with our functions or activities", "condition": "This Section of the Privacy Policy only applies to those who use our Services and are in a country that is a Member State of the European Economic Area, the United Kingdom, Switzerland or other countries outside of the United States to the extent the laws of such countries require Southwest to provide consumers with rights set forth below; For Indian residents; only for a lawful purpose connected with our functions or activities, where such collection is necessary for the specified purpose, and after obtaining the individual’s prior written consent for such specified purpose, in accordance with applicable laws", "condition_predicate": "((user.jurisdiction = European Economic Area OR user.jurisdiction = United Kingdom OR user.jurisdiction = Switzerland OR [untranslated: other countries outside of the United States to the extent the laws of such countries require Southwest to provide consumers with rights set forth below]) AND user.jurisdiction = India AND ([untranslated: only for a lawful purpose connected with our functions or activities, where such collection is necessary for the specified purpose] AND consent.sensitive_personal_data))"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "collect (operation: collection)", "data": "personal information", "recipient": "", "source": "children under the age of sixteen (16)", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1
19. Individuals from the European Economic Area, Switzerland, the United Kingdom, and Certain Other Countries Outside of the United States
This Section of the Privacy Policy only applies to those who use our Services and are in a country that is a Member State of the European Economic Area, the United Kingdom, Switzerland or other countries outside of the United States to the extent the laws of such countries require Southwest to provide consumers with rights set forth below; to the extent that Southwest is subject to the laws of the European Economic Area, Switzerland, the United Kingdom, or such other countries outside of the United States when processing Personal Information, Southwest shall be a “data controller” or “data fiduciary” under such laws.
The law in Europe and certain other jurisdictions requires us to have legal basis for collecting and using your Personal Information. Where applicable, we rely on one or more of the following legal bases:
Performance of a contract with you: Where we need to perform the contract we are about to enter into or have entered into with you.
Legitimate interests: We may use your Personal Information where it is necessary to conduct our business and pursue our legitimate interests, for example to prevent fraud and enable us to give you the best and most secure customer experience. We consider and balance any potential impact on you and your rights (both positive and negative) before we process your Personal Information for our legitimate interests.
To protect a vital interest of you or another person: We may use your Personal Information to prevent harm, ensure safety, or respond to emergencies where necessary.
Legal obligation: We may use your Personal Information where it is necessary for compliance with a legal obligation that we are subject to.
Consent: We rely on consent only where we have obtained your active agreement to use your Personal Information for a specified purpose in accordance with applicable law, for example if you subscribe to an email newsletter or give your explicit consent by providing us with sensitive health information to manage special assistance requests. For Indian residents, where we collect or process Sensitive Personal Data or Information (as defined below), we will do so only for a lawful purpose connected with our functions or activities, where such collection is necessary for the specified purpose, and after obtaining the individual’s prior written consent for such specified purpose, in accordance with applicable laws.
Whenever we transfer your Personal Information out of your country to countries which have laws that do not provide the same level of data protection as your home country, a similar degree of protection is afforded to it using the following safeguards if applicable:
Standard contractual terms approved for use such as those approved by the Swiss, European Union and UK and other applicable regulators for enabling transfers.
Adequacy decision made by a home state meaning the country to whom the information is transferred to has been determined to afford an equivalent level of protection to the EU/UK or other territory as applicable.
As otherwise permitted under applicable local laws. For Indian residents, if required under applicable law, Southwest will transfer your information to another entity only with your prior consent and only where that entity agrees to provide the same level of data protection as required under applicable law.
We will retain your Personal Information for as long as reasonably necessary to fulfil the purposes we collected it for, including for the purposes of satisfying any legal, regulatory, tax, accounting or reporting requirements. We may retain your Personal Information for a longer period in the event of a complaint or if we reasonably believe there is a prospect of litigation in respect to our relationship with you.
--- section of rule 2
15. Children
Our Services are not intended for and are not targeted to children under the age of sixteen (16). If you are a child under the age of sixteen (16), you are not permitted to use the Services and should not send any information about yourself to us through the Services.
We do not knowingly collect any personal information from children under the age of sixteen (16) and, if we learn that we have received information from a user under the age of 13, we will delete this information in accordance with the Children’s Online Privacy Protection Act (“COPPA”). If you are a parent or guardian and you believe that your child under the age of 13, has provided us with personal information without COPPA-required consent, please contact us by e-mail as detailed
here
.
If you have registered to use the Services, and have posted content or information on the Services, you can request that such information be removed from the Services by contacting us by e-mail as detailed
here
or by sending a letter to Southwest Airlines Co., P.O. Box 36647 TOP-1CR, Dallas, Texas 75235 (Attention: Legal Counsel), stating that you personally posted such content or information and detailing where the content or information is posted. We will make reasonable good faith efforts to endeavor to remove the post from prospective public view or anonymize it so the minor cannot be individually identified. This removal process cannot ensure complete or comprehensive removal. For instance, third parties may have republished the post and archived copies of it may be stored by search engines and others that we do not control.
=== END ITEM p0131

=== ITEM p0132
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "disclosed (operation: disclosure)", "data": "the categories of Personal Information as listed below", "recipient": "", "source": "", "purpose": "", "condition": "In the preceding twelve (12) months; for the business purposes indicated", "condition_predicate": "retention.days <= 360"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "share (operation: disclosure)", "data": "Personal Information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1 and rule 2
If you use the Cloudinary media management platform service as an individual user and not on behalf of a Business, then we will collect and process any Personal Information embedded in the content that you upload to the platform.
Inferences drawn from other Personal Information.
In the preceding twelve (12) months we have processed the personal information for the following business or commercial purposes:
Business development.
Helping to ensure security and integrity of the Service.
Administering the business and professional services relationship with customers and facilitating the provision of support to customers.
Facilitating the provision of the Services and support for the Services.
Responding to, handling, and mitigating suspected violations of law in connection with our business.
Categories of Sensitive Personal Information
Our Services are not intended for Sensitive Personal Information. We do not knowingly collect Sensitive Personal Information, and we require you not to use our Services or provide us with any such information.
We do not collect or process Sensitive Personal Information for the purpose of inferring characteristics about you and we do not sell Sensitive Personal Information or share Sensitive Personal Information for cross-context behavioral advertising.
For the purpose of applicable laws under this section of the policy, Sensitive Personal Information means:
A consumer’s social security, driver’s license, state identification card, or passport number.
A consumer’s account log-in, financial account, debit card, or credit card number in combination with any required security or access code, password, or credentials allowing access to an account.
A consumer’s precise geolocation.
A consumer’s racial or ethnic origin, religious or philosophical beliefs, or union membership.
The contents of a consumer’s mail, email, and text messages unless we are the business that is the intended recipient of the communication.
A consumer’s genetic data.
The processing of biometric information for the purpose of uniquely identifying a consumer.
Personal information collected and analyzed concerning a consumer’s health.
Personal information collected and analyzed concerning a consumer’s sex life or sexual orientation.
Categories of Sources for Personal Information Collection and Disclosure
We obtain the Personal Information directly from you, from your Services activities, from third parties such as event organizers, data providers and publicly available resources.
In the preceding twelve (12) months we have disclosed the categories of Personal Information as listed below for the business purposes indicated:
Categories of personal information
Categories of third parties to whom we disclose your information and the specific business or commercial purpose for the disclosure
Identifiers
Law enforcement, courts and other agencies, authorities and other relevant entities. We will comply with court orders, search warrants, regulatory orders, and subpoenas, and provide information in response to lawful requests by public authorities, including to meet national security or law enforcement requirements. We will also report uploaded content and shared Personal Information, if we have a good-faith belief that the content, or the sharing of the content is illegal, abusive, or violates third-party rights.
Other entities as part of a merger, acquisition, or any other corporate structural change.
Other information that identifies, relates to, describes, or is capable of being associated with, the individual
Commercial information
Internet or other electronic network activity information
Imprecise Geolocation data
Inferences drawn from other Personal Information
Selling and Sharing Personal Information
We do not sell or share Personal Information as these terms are defined under applicable laws.
=== END ITEM p0132

=== ITEM p0133
rule 1: {"polarity": "ALLOW", "actor": "We", "action": "collect (operation: collection)", "data": "personal data", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "collect (operation: collection)", "data": "personal data beyond what is necessary", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1
3. TYPES OF PERSONAL DATA WE COLLECT
In this Section, We describe the types of personal data that We collect or create. In
Section 4
We describe for what purposes and which legal ground that We rely upon when We process Your personal data. For the purposes of this privacy policy, the term personal data shall have the same definition as it has under the GDPR.
Account Inactivity:
An account is considered inactive if there has been no user login or recorded gameplay activity for a consecutive period of 24 months.
User Information:
Information about Your use of Sago Mini™’s apps - such as in-app generated events based on Your interaction with the app, error and crash reports.
Device Information:
Information from Your device - such as device IDs, Android ID, IDFV, App Set ID, operating system, platform, screen resolution and similar information about Your device and device settings/usage, IP address (including Your approximate location).
Unique Identifiers:
Information from Your account - such as account ID, Piknik profile ID, parent’s email address and password (where email login is applicable). This also includes persistent identifiers such as App Set ID and Appsflyer ID which are used to help identify Piknik apps installed on Your device.
Purchasing Data:
Information relating to Your purchase history - such as in-app properties/playset and purchasing tendencies.
Social Media:
Information about You and Your interactions with Sago Mini™ fan pages on social media - such as name and/or user name, posts You like and comment.
Customer Information:
Information from You provided to Us via Our customer support and/or service functions - such as first name, last name, email, age, Your issues and/or ideas.
--- section of rule 2
1. OUR PRIVACY POLICY
Last modified: August 21, 2026
Sago Sago Toys Inc., DUNS #203172499 , having its registered office at 171 John Street, 5th Floor, Toronto, Ontario, M5T 1X3, Canada and doing business under the name Piknik™ and Sago Mini™, (“Sago Sago”, “We”, “Our” and “Us”) is committed to protecting Your privacy as a data subject (“You” or “Your”) and the secure processing of Your personal data and We strive to limit the processing of personal data as far as possible and do not collect personal data beyond what is necessary.
While our apps are designed for young kids and parents, our websites sagomini.com and playpiknik.com (the "Site" or "Site(s)”) are intended for adult use only. We take privacy seriously at Sago Sago and this policy is designed to share the information we collect and how we use it. This Privacy Policy applies to the Sites as well as SAGO MINI WORLD, SAGO MINI SCHOOL, SAGO MINI FIRST WORDS, TOCA BOCA JR, TOCA BOCA JR Hair Salon 4, MathTango, Endless Learning Academy, PAW Patrol Academy™ app (“PAW Academy”), Crayon Club™, Gabby’s Dollhouse, Superfonik™ and PIKNIK digital subscription programs and which are part of the services (“Services”) that Sago Sago offers.
Our Apple Arcade games; SAGO MINI TRIPS+, Toca Boca Jr Classics and JINJA’S GARDEN have their own Privacy Policies and are not indicated here. Please review these specific policies for more details.
SAGO MINI TRIPS+ privacy policy
TOCA BOCA JR CLASSICS privacy policy
JINJA'S GARDEN privacy policy
Needless to say, all processing of personal data, including the collection, registration, storing and general handling is governed by applicable privacy legislation, including the General Data Protection Regulation (“GDPR”). Sago Mini™ strives to make sure that the processing of personal data done by Sago Mini™, is done in accordance with applicable legislation.
For our Privacy Policy for Kids, please see
Section 12
.
We aim to apply the GDPR to everyone but if You reside outside the European Union and use Our services, We may apply additional standards to You as required by local law. To the extent that the California Consumer Privacy Act (“CCPA”) applies to You, the definitions in this privacy policy are to be read as follows: “personal data” includes “personal information”; “data subject” includes “consumer”; “controller” includes “business”; “processor” includes “service provider”, all as defined under the CCPA. For more information about the CCPA, please see
Section 11
.
As a service directed towards children, We also adhere to the Children’s Online Privacy Protection Rule (“COPPA”). To the extent that the COPPA applies to You, the definitions in this privacy policy are to be read as follows: “personal data” includes “personally identifiable information”; “processor” includes “service provider”, all as defined under the COPPA.
Who are We?
Proudly Canadian, Sago Mini™ is a subsidiary of Spin Master Ltd. We cooperate with Spin Master Ltd, and the other gaming studios of the group (each a “Group Company”) to learn from one another, help each other and improve how We all make apps.
Our websites www.sagomini.com , www.playpiknik.com , and superfonik.com are just for grownups, while Our apps are designed for young children with parental supervision. We take privacy seriously at Sago Mini™ and this policy is designed to share what information We collect and how We use it. When You visit Our websites, install one of Our apps or interact with Our social media channels, Sago Mini™ processes Your personal data in accordance with this privacy policy and acts as the controller of Your personal data as defined by the GDPR.
Our contact details are:
You can also call or write to us at:
Sago Sago Toys Inc.
=== END ITEM p0133

=== ITEM p0134
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "disclose (operation: disclosure)", "data": "that data", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "share (operation: disclosure)", "data": "personal information", "recipient": "", "source": "", "purpose": "", "condition": "about individuals we know are under the age of sixteen (16)", "condition_predicate": "user.age < 16"}
--- section of rule 1
Privacy Notice
JetBrains Privacy Notice
Version 3.2, last updated: 12 June 2026
In this Privacy Notice, we describe the types of data, including Personal Data, (collectively, “data”) that we and our associated companies collect from you when you use JetBrains Websites and certain JetBrains products and services as described in this Privacy Notice (collectively, our “services”), how we and our associated companies use and disclose that data, and your options for accessing or updating your data.
For information about your privacy choices, please see Section 10, Your Privacy Choices and Rights, and Section 14, Privacy Notice Specifications for Certain U.S. Jurisdictions.
If you are a resident of California, please also refer to Section 13, Privacy Notice Specifications for California Residents, for information about the categories of personal information we collect and your rights under California privacy laws.
The data controllers are JetBrains s.r.o., Praha 4, Na Hřebenech II 1718/8, PSČ 140 00, Czech Republic, and the
associated companies of JetBrains
(collectively “JetBrains,” “we,” or “us”).
JetBrains and its
associated companies
act as joint data controllers, who are jointly responsible for compliance with data protection legislation. JetBrains s.r.o. is primarily responsible for exercising the rights of data subjects and providing information about data processing.
This Privacy Notice identifies what Personal Data we may process about you. The extent varies depending on whether you are just visiting our Website or using our products or services. We do not process health data or otherwise sensitive data about you. For more information, you can contact us anytime at
privacy@jetbrains.com
. This document applies only to situations where we act as a Personal Data controller. More information about circumstances in which we are in the role of data processor can be found in our
Data Processing Agreement
. The list of our partners who might process your Personal Data, including the location of the data, can be found
here
.
--- section of rule 2
Purposes of Collection, Use, and Disclosure
As described in more detail above in Sections 2 and 6,
Why We Collect Your Data and What We Collect
and
Sharing of Personal Data
, in general, we may collect, use, disclose, and otherwise process personal information for the following business or commercial purposes and as otherwise directed or consented to by you:
To provide our products and services to you;
To protect us from piracy and the unlawful use of our software or services;
To improve our offerings based on usage;
For JetBrains’ internal evidence and to protect the rights and interests of JetBrains and other users;
To advertise and market our products and services to you;
General business and operational support; and,
To comply with applicable laws.
“Sales” and “Sharing” of Personal Information.
The CCPA defines “sale” as disclosing or making available personal information to a third party in exchange for monetary or other valuable consideration, and “sharing” includes disclosing or making available personal information to a third party for purposes of cross-context behavioral advertising. While we do not disclose personal information to third parties in exchange for monetary compensation, we may “sell” or “share” the following categories of personal information: identifiers, internet and network activity information, location data (via your IP address), and inferences. We may disclose these categories to third-party advertising networks, analytics providers, and social networks for purposes of marketing and advertising and to improve and measure our ad campaigns.
We do not sell or share sensitive personal information, nor do we sell or share personal information about individuals we know are under the age of sixteen (16).
Retention of Personal Information.
We store the personal information we collect as described in this Privacy Notice for as long as you use JetBrains Products or as necessary to fulfill the purpose(s) for which it was collected, provide our products and services, resolve disputes, establish legal defenses, conduct audits, pursue legitimate business purposes, enforce our agreements, and comply with applicable laws, or based upon other criteria, including, but not limited to, the sensitivity and volume of such data. Additionally, we endeavor to retain all such personal information in accordance with legal requirements.
De-Identified Information.
If we create or receive de-identified information, we will maintain and use such de-identified information in de-identified form. We will not attempt to reidentify such information, except to comply with applicable law.
Privacy Rights for Residents of California
The CCPA provides California residents with specific rights regarding personal information. Subject to certain conditions and exceptions, California residents have the following rights:
Right to know.
You have the right to request (i) the categories of personal information we collected about you; (ii) the categories of sources from which the personal information is collected; (iii) our business or commercial purposes for collecting, selling, or sharing personal information; (iv) the categories of third parties to whom we have disclosed personal information; and (v) a copy of the specific pieces of personal information we have collected about you.
Right to Delete.
You have the right to request us to delete any personal information we have collected from you.
Right to Correct.
You have the right to request us to correct inaccuracies in your personal information.
Right to Opt Out of Sales and Sharing.
You have the right to opt out of “sales” and “sharing” of your personal information, as those terms are defined under the CCPA.
Right to Limit Use of Sensitive Personal Information.
You have the right to limit the use and disclosure of your sensitive personal information. We do not collect, use, or disclose sensitive personal information; thus, this right is not available to California residents.
=== END ITEM p0134

=== ITEM p0135
rule 1: {"polarity": "ALLOW", "actor": "", "action": "collection (operation: collection)", "data": "your personal information", "recipient": "", "source": "", "purpose": "", "condition": "by using our Site and Mobile Apps; subject to and consistent with applicable laws, regulations and other notices you may have received based on your relationship with us; unless We ask for your consent when required", "condition_predicate": "(event.use_sites_and_mobile_apps AND (law.permitted AND [untranslated: other notices you may have received based on your relationship with us]) AND NOT law.required)"}
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
=== END ITEM p0135

=== ITEM p0136
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "link (operation: alignment or combination)", "data": "personal information you have provided", "recipient": "", "source": "", "purpose": "to personalize the site for you and tailor the content to your needs, for instance to show you other products you may be interested in", "condition": "unless where you manage your account, if you decide later that you want to terminate one or more of these functions", "condition_predicate": "NOT request.terminate_cookie_functions"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "link to (operation: alignment or combination)", "data": "personal information", "recipient": "", "source": "", "purpose": "", "condition": "through persistent cookies; unless your express consent", "condition_predicate": "([untranslated: through persistent cookies] AND NOT consent.persistent_cookies)"}
--- section of rule 1 and rule 2
Postmaster General's Letter on Cookie Usage
Cookies
Cookies may be categorized as session or persistent, which describes the length of time that they stay on your system. Both session and persistent cookies are used on this site. The following are detailed descriptions of how we use these cookies.
Session Cookies
A session cookie is a small piece of textual information that a server places temporarily on your browser during the time your browser is open. The cookies are erased once you close all browsers. We use session cookies in the following manner:
Log-on and log-off administration-If you decide to register with our site, so as, for example, to use one of our online services, session cookies help with the log-on and log-off process. The cookies enable us to recognize your log-on ID when you log on so that we do not establish a duplicate registration record for you.
Transactions and site usability - We use session cookies to improve how you navigate through usps.com and conduct transactions. As examples, session cookies are used to maintain your online session as you browse over several pages; to store and prepopulate information so that you do not have to reenter the same information twice; to enable the postage rate calculator; and to retain your shopping cart information. Session cookies may also be used to collect referral statistics when you click on a link or ad banner to or from usps.com.
Persistent Cookies
A persistent cookie is a small piece of text stored on your computer's hard drive for a defined period of time, after which the cookie is erased. We do not collect or link to personal information through persistent cookies without your express consent. We use persistent cookies as follows:
Site usage measurement-Our site measurement tool uses a persistent cookie to assist us in measuring how and when our Web site and its various components are used. It functions as a "visit cookie," so that we can determine if you are a repeat visitor to our site. This allows us to know if we are attracting new visitors and what aspects of the site seem most useful. The cookie will expire 30 days after your last visit.
Log-off safety function-The USPS uses a persistent cookie to automatically log you off of usps.com if there has been no activity for 15 minutes. This is done for your safety to ensure that, if you have finished using our site, but have forgotten to log off, no one else can use your computer via your log-on and password. The cookie is permanently removed from your computer when you log off, or, if you have closed the browser without logging off, it is removed within 15 minutes from your last activity.
Opt-in cookies-Persistent cookies allow us, at your request, to recognize you when you return to usps.com, or to remember certain information that you have provided us. The recognition feature allows you to log on to usps.com automatically, without having to enter your name and password each visit. The cookie assigns a random number to you, which we link to personal information you have provided and your purchase history. This allows us to personalize the site for you and tailor the content to your needs, for instance to show you other products you may be interested in. Other cookies allow us to remember certain information related to prior transactions, such as package tracking numbers, or mailing or address lists, so that we may prepopulate those fields for you on return visits. These features and cookies are strictly at your option and for your convenience. We will also present you with a convenient way to remove the cookies, via where you manage your account, if you decide later that you want to terminate one or more of these functions. The cookies will expire one year from your last visit.
Ad banner cookies-On behalf of the USPS, persistent cookies and beacons (described below) may be set and managed by third party advertising suppliers to support ad banners.
=== END ITEM p0136

=== ITEM p0137
rule 1: {"polarity": "ALLOW", "actor": "We", "action": "use (operation: use)", "data": "it", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "PLAYit", "action": "use (operation: use)", "data": "personal information", "recipient": "", "source": "", "purpose": "", "condition": "in the event that a user identifies himself or herself as a child under the age of 13 within the Services or in connection with any Content or Software; of such user", "condition_predicate": "((event.user_identifies_as_child AND user.age < 13) AND (event.user_identifies_as_child AND user.age < 13))"}
--- section of rule 1
Privacy Policy
Privacy Policy
PLAYit("Our", "We" or "Us") respects your privacy and is dedicated to protecting the privacy of those persons using ("User(s)" or "You") PLAYit products, services and websites. This Privacy Policy helps You to understand what personal information/data ("Personal Information") and non-personal information We collect, and how We use it.
--- section of rule 2
4. COLLECTION AND USE OF CHILDREN'S PERSONAL INFORMATION
The Services comply with the Children's Online Privacy Protection Act ("COPPA"). PLAYit does not knowingly collect personal information from children under the age of 13 through the Services. In addition, in the event that a user identifies himself or herself as a child under the age of 13 within the Services or in connection with any Content or Software, PLAYit will not collect, store or use any personal information of such user. Further, in the event that PLAYit receives personal information that PLAYit discovers was provided by a child under the age of 13, PLAYit will promptly delete such personal information in a secure manner.
=== END ITEM p0137

=== ITEM p0138
rule 1: {"polarity": "ALLOW", "actor": "", "action": "collected (operation: collection)", "data": "persistent identifiers", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "collect (operation: collection)", "data": "persistent identifiers (such as IDFA or unique device IDs) that track users across different websites or apps", "recipient": "", "source": "", "purpose": "for targeted advertising; profiling", "condition": "", "condition_predicate": "true"}
--- section of rule 1 and rule 2
6. HOW DOES BUDGE STUDIOS HANDLE CHILDREN'S INFORMATION?
Budge Studios has developed its Platforms to be an enjoyable experience for users of all ages. Some parts of the Platforms are primarily intended for children, such as our Apps, while others are intended for parents, such as our Sites. Whenever we refer to children in this Privacy Policy, we mean children under the age of 13 (or, if outside the U.S., under the age of digital majority).
Budge Studios complies with the Children's Online Privacy Protection Act (COPPA), a U.S. law designed to protect the online privacy of children. If you are a data subject in Europe or a California resident and have a child under the age of 16, please see the
What Should I Know as a Data Subject in Europe?
and
What Should I Know as a California Resident?
sections.
Budge Studios is a member of the ESRB Privacy Certified Program. We have designed our Apps to be "Privacy-First," meaning we minimize data collection from children as required by COPPA. Because we do not collect personal information for advertising, marketing or profiling, we do not require or implement Verifiable Parental Consent (VPC) within our Apps.
If you have any questions or comments about how we treat children's information or our compliance with COPPA, please contact us as set out in the
How Do I Contact Budge Studios?
section. If you would like to learn more about COPPA and ESRB Privacy Certified's Kids Privacy Seal, which signals our compliance with COPPA, you can refer to the
Children's Privacy
section of the Federal Trade Commission's website.
A. We Minimize Children's Data Collection and Use
No Accounts: We do not require children to create accounts, provide names, or submit email addresses to play our games.
No Targeted Advertising: Our Apps may display advertisements, but these are strictly contextual. This means ads are selected based on the content of the App you are currently using, not on the individual user's behavior, history, or identity. We do not allow behavioral or targeted advertising to children. Some of our Apps incorporate advertising serving technology offered by our service providers (through SDKs), which enable advertising to be temporarily uploaded into the game and displayed while the user plays. The data collected for this purpose, often through "persistent identifiers," may be used for ad attribution and related internal operations purposes such as allowing our service providers to calculate the number of user views, cap the frequency of ads, and serve ads in a format that fits the device.
No Third Party Sharing or Server Uploads from Device Sensors: Features that use the device's camera or microphone (e.g., to blow out digital candles) are processed entirely on the local device. This data is never uploaded to our servers or shared with any third party. Budge Studios does not store or share any photos, videos, or audio files that contain children's images or voices through our Apps. All photos, videos, and audio files are stored locally on the device only. We do not prompt, encourage, or enable children to make such information publicly available online.
B. We Use Persistent Identifiers and Data Processors Solely to Support Our Internal Operations
No Persistent Identifiers for Targeted Advertising: We do not collect or store persistent identifiers (such as IDFA or unique device IDs) that track users across different websites or apps for targeted advertising or profiling.
We do not collect children's personal information for targeted advertising and profiling. We do use persistent identifiers to deliver the games and support the functioning of our Apps as follows:
Budge ID: We use a randomly generated ID, known as the Budge ID, to collect data reporting analytics (e.g., which Budge applications a user has installed on their device) and to keep track of subscriptions and other game-related purchases.
=== END ITEM p0138

=== ITEM p0139
rule 1: {"polarity": "ALLOW", "actor": "Cision", "action": "transfer (operation: disclosure by transmission)", "data": "personal data", "recipient": "", "source": "Google Gmail", "purpose": "to comply with applicable law", "condition": "If you are a customer user using the email integration feature; as necessary to comply with applicable law", "condition_predicate": "((user.category = customer AND service = email_integration) AND law.required)"}
rule 2: {"polarity": "DENY", "actor": "Cision", "action": "transfers (operation: disclosure by transmission)", "data": "your personal data", "recipient": "", "source": "Google Gmail", "purpose": "", "condition": "If you are a customer user using the email integration feature; unless only transfer your personal data to a third-party, Nylas, as it is necessary to provide or improve user-facing features that are prominent in Cision’s requesting application's user interface; transfer personal data as necessary to comply with applicable law or as part of a merger, acquisition, or sale of assets with notice to users", "condition_predicate": "((user.category = customer AND service = email_integration) AND NOT [untranslated: only transfer your personal data to a third-party, Nylas, as it is necessary to provide or improve user-facing features that are prominent in Cision’s requesting application's user interface] AND NOT (law.required OR event.merger OR event.acquisition OR event.sale_of_assets))"}
--- section of rule 1 and rule 2
Identification and ongoing monitoring of trends and volumes.
Tagging, tracking, storing, and sorting when monitoring public data sets.
Search assistance, query generation.
Content creation – press releases or posts.
When you engage directly with any of our AI product features, they will be labeled as such.
We do not use any Personal Data that we have collected to train either our own AI models or any 3rd party AI models that power our AI features.
Within Our Business Operations
In order to improve your experience as a customer, we may employ AI features like chatbots, call recording analysis, or other tools to help us understand your use of our Services and to give you appropriate answers.
In these instances, you will be made aware that AI is being used and will have the option to avoid the use of AI.
We may also use AI to understand how your organisation views our Services via feedback you have provided.
Product Analytics and AI-Assisted Insights
We use analytics tools, including Mixpanel, to understand how customers and authorised users interact with our products and services. This may include analysis of account information, device information, usage activity, feature interactions and other technical data.
We may use artificial intelligence ("AI") tools in connection with these analytics services to identify trends, detect anomalies, generate reports, provide product usage insights and help improve our products and services.
These tools support our personnel in understanding and improving our services and are not used to make solely automated decisions that produce legal or similarly significant effects on individuals.
We may analyse product usage information to create user segments or behavioural categories for product improvement, customer support and service optimisation purposes.
How we use your personal data via API with Google Gmail
If you are a customer user using the email integration feature, Cision will use your personal data in accordance with the below:
Cision will only use your personal data to provide or improve your use of the email integration functionality within Cision’s platform. We will not use your personal data for any other purpose.
Cision will only transfer your personal data to a third-party, Nylas, as it is necessary to provide or improve user-facing features that are prominent in Cision’s requesting application's user interface. Cision may also transfer personal data as necessary to comply with applicable law or as part of a merger, acquisition, or sale of assets with notice to users. Cision will not engage in any other transfers or sales of your personal data.
Cision will not use or transfer your personal data for serving ads, including retargeting, personalized, or interest-based advertising.
By default Cision is unable to view your integrated email personal data unless:
Cision first obtains your affirmative agreement to access your email and personal data for purposes of providing its service and providing service support;
Cision first obtains your affirmative agreement to access your email and personal data if it is necessary for security purposes (such as investigating a bug or abuse);
It is necessary for Cision to comply with applicable law; or
Cision’s use is limited to internal operations and the data (including derivations) have been aggregated and anonymized.
Cision's use and transfer to any other app of information received from Google APIs will adhere to
Google API Services User Data Policy
including the Limited Use requirements.
Tracking
Cision emails may contain a small, invisible, one pixel image which can be used to let us know when the email is opened or forwarded. If the email recipient has images enabled on their device, when the email is opened, a message (an automatic request) is sent to Cision’s server requesting the image. That request is logged by Cision and tells us that the email has been opened.
=== END ITEM p0139

=== ITEM p0140
rule 1: {"polarity": "ALLOW", "actor": "", "action": "disclosed (operation: disclosure)", "data": "Your personal data", "recipient": "", "source": "", "purpose": "", "condition": "Business Transaction or Reorganization; in the event of insolvency, bankruptcy, or receivership", "condition_predicate": "((event.merger OR event.business_transaction) AND event.bankruptcy)"}
rule 2: {"polarity": "DENY", "actor": "service providers", "action": "disclosing (operation: disclosure)", "data": "personal data", "recipient": "", "source": "", "purpose": "", "condition": "unless performing agreed upon services for us", "condition_predicate": "NOT [untranslated: performing agreed upon services for us]"}
--- section of rule 1 and rule 2
We may also share aggregated demographic information with third parties interested in advertising on our online services to assist them in understanding the audience they would be reaching, but this information is not designed to identify any specific individual.
Service Providers
: We share personal data (all categories set forth in “
Our Collection and Use of Personal Data
” above) with third party vendors and service providers that perform services for or on our behalf, which may include providing mailing or email services, facilitating marketing activities on our behalf, customer service, product fulfillment, payments processing, photo sharing, data processing and enhancement services, fraud prevention, web hosting, analytic services, or other online functionality. We contractually restrict service providers from collecting, using, or disclosing personal data for any purpose other than performing agreed upon services for us.
Support for Business Operations.
We share personal data (all categories set forth in “
Our Collection and Use of Personal Data
” above) with third parties that provide and support critical business operations, such as tax, legal, and accounting services. We contractually restrict these parties from collecting, using, or disclosing personal data for any purpose other than performing agreed upon services for us.
Business Transaction or Reorganization
: We may take part in or be involved with a corporate business transaction, such as a merger, acquisition, joint venture, or financing or sale of company assets. We may disclose your personal data (all categories set forth in “
Our Collection and Use of Personal Data
” above) to a third party during negotiation of, in connection with, or as an asset in such a corporate business transaction. Your personal data may also be disclosed in the event of insolvency, bankruptcy, or receivership.
Legal Obligations and Rights
: We may disclose your personal data (all categories set forth in “
Our Collection and Use of Personal Data
” above) to third parties, such as legal advisors and law enforcement:
-In connection with the establishment, exercise, or defense of legal claims;
-To comply with laws and regulations or to respond to lawful requests and legal process such as a subpoena or search warrant;
-To protect our rights and property and the rights and property of our agents, customers, and others, including to enforce our agreements, notices, and terms of use;
-To detect, suppress, or prevent fraud;
-To reduce credit risk and collect debts owed to us;
-To protect the health and safety of us, our customers, or any person; or
-As otherwise required by applicable law.
-You can find more information about our procedures for these types of disclosures
here
.
Otherwise with Consent or At Your Direction
: We may disclose your personal data to certain other third parties or publicly with your consent or direction. If you post a comment or review our website or a comment on our social media sites, the information you provide may be displayed publicly online for others to view.
Choices about your data
Profile Access and Data Sharing
. You may access and update your profile information, such as your user name, address, or billing information, and may change some of your data sharing preferences on your account page.
Geolocation and Device Permissions
. You are free to decline to provide precise geolocation information through your mobile device settings or any prompt requesting location information. You may also control (opt-in or opt-out) the collection of geolocation data by adjusting your location services options in your mobile device or browser settings. We may still infer your approximate location (for example, based on your IP address), but not your precise geolocation, when you access the services. If you would like to update your device permissions, such as permissions to access your camera, you can do so in your mobile device settings.
=== END ITEM p0140

=== ITEM p0141
rule 1: {"polarity": "ALLOW", "actor": "", "action": "shared (operation: disclosure)", "data": "Personal Data", "recipient": "third parties", "source": "", "purpose": "for the purposes as mentioned in this Privacy Policy", "condition": "If you are a User in India; only with your consent as provided at the time of registration logging in or payment", "condition_predicate": "(user.jurisdiction = India AND (consent.registration OR consent.logging_in OR consent.payment))"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "provide (operation: disclosure)", "data": "the Personal data", "recipient": "third parties", "source": "", "purpose": "", "condition": "in principle", "condition_predicate": "[untranslated: in principle]"}
--- section of rule 1
12. Supplemental terms
(a) India-specific terms
If you are a User in India, the following terms apply to you.
Your Personal Data will be shared or disclosed for the purposes as mentioned in this Privacy Policy and to such third parties only with your consent as provided at the time of registration logging in or payment. To comply with Indian legal requirements, if you are a user in India, we will collect your name, mobile number, email, PAN, address (including state, city, street, and gate number), and zip code when you initiate a payment request. This information will be securely stored upon your first submission to ensure you only need to provide it once. Each time you make a payment, the information will be transmitted to the third-party payment service provider of your choice. Please note that such third parties may further disclose this provided and you hereby consent to such disclosure.
We will not retain any sensitive Personal Data or information for longer than is required for the purpose for which such data or information was collected or may lawfully be used or is otherwise required under any other law for the time being in force. We will retain the Personal Data for a minimum period of 180 days or as required under applicable laws. We may retain anonymized/ de-identified data for as long as is required. However, for the biometric data collected from you (if any), we will not disclose it to any third party and will not use it for any other purpose, and we will delete it within 180 days.
We implement reasonable physical, technical and administrative security standards designed to protect your Personal Data from loss, misuse, alteration, destruction or damage and to ensure a level of security appropriate to the risk and such security standard will be at an equivalent or higher level than the international standard IS/ISO/IEC 27001 on "Information Technology - Security Techniques - Information Security Management System - Requirements".
In respect of cross-border transfer of Personal Data, we will ensure that your Personal Data receives the same or higher level of protection as required under Indian data protection laws.
Our services are not for persons under the age of 18. If you are under 18 years old, you must not use or access the service without the consent of your parent or legal guardian.
In the event of any conflict between the above terms applicable to Users in India and other parts of the Privacy Policy, the India-specific terms shall prevail.
(b) Indonesia-specific terms
If you are a User in Indonesia, the following terms apply to you.
Our services are not for persons under the age of 21. Further, by accessing or using the service, you confirm that you are at least 21 years old. If you are under 21 years old and unmarried, your account must be created under the supervision of your parent or legal guardian and you represent and warrant that you have provided your parent’s or legal guardian’s email address for verification purposes. Your parent or legal guardian will receive a verification email requiring them to approve your account creation. Your account will only be created after your parent or legal guardian clicks on the verification link provided in the email and gives their consent for the creation of an account on your behalf.
You must obtain approval from your parent(s) or legal guardian(s); and your parent(s) or legal guardian(s) are responsible for: (i) all your actions in connection with your access to and use of the Platform; (ii) your compliance with this policy; and (iv) ensuring that any of your participation in the Platform will not, in any event, result in any violation of applicable laws and regulations relating to child protections.
If you do not have consent from your parent(s) or legal guardian(s) and your parent(s) or guardian(s) is not willing to open the account under their name, you must cease accessing the Platform.
--- section of rule 2
We destroy personal data whose purpose of collection as consented to by you have been achieved, or whose periods of and use to which you consented to or which were provided in this privacy policy have expired; provided, however, we will continue to store your personal data for the following statutorily-prescribed periods, where applicable, including, but not limited to:
(i) Act on Consumer Protection in Electronic Commerce Article 6, and Enforcement Degree of the Act on Consumer Protection in Electronic Commerce Article 6
Records on your cancellation of an order, your payment on a purchased item, and our supply of a good/service: 5 years
Records on the handling of consumer complaints or disputes: 3 years
Records on advertisements and labels: 6 months
(ii) Protection of Communications Secrets
Records on your visits to our website: 3 months
Provision of Personal data. We, in principle, does not provide the Personal data to third parties. In order to provide you a smooth and better service, we share information with our business partners service providers entrusted by us. We will enter into strict confidentiality contractual terms with such third parties and require them to process Personal Data within the purpose of process entrusted and in accordance with our requirements (including the retention period which shall be subject to us), this Privacy Policy, and the confidentiality and security measures required by applicable laws and regulations. In addition to the main text of this privacy policy (Section 4 How do we share and entrust the processing of your Personal Data), specifically, we share information with social media including Facebook, Google and Apple if you use them to register FreeReels. We entrust cloud service providers such as Amazon Web Service to transmit through their bandwidth service and store your Personal Data in order to provide you with safe and steady services; We will share, to Google Pay, and Apple Pay your commodity information, anonymous user ID, and other payment information as necessary to complete your top-up and purchase in Service.
Destruction of Personal data. We will destroy your personal data without delay when it becomes unnecessary, such as achievement of the purpose of processing your personal data, or the expiration of the retention period. However, this is not the case when preservation is required in accordance with other laws and regulations, such preservation of personal data will be stored separately and will not be used for any other purpose other than as provided by law. The destruction of personal data shall be subject to the approval of the personal data protection officer. We destroy your personal data in electronic form in a manner that renders it unrestorable by the relevant department. In the case of personal data stored in paper, we will destroy your personal data in manner of crushing or burning.
Data rights. You have the right to access personal data we hold about you, to rectify any personal data held about you that is inaccurate, to request the deletion of personal data held about you, and the right to request the suspension of the processing of your personal data. You can exercise your rights by contacting us at
contact.freereels@gmail.com
, and we will take action without delay. If you are the legal guardian of a user, you may be able to exercise your data rights on behalf of the user by contacting the aforesaid email address.
Data Security. We work hard to protect us and our users from unauthorized access to or unauthorized alteration, disclosure or destruction of information we hold. To this end, we have in place technical, managerial and physical safeguards, including internal policy for data protection, limiting the access to personal data on a need-to-know basis and controlling access to the facilities where personal data is processed.
You declare that you are over the age of 14.
=== END ITEM p0141

=== ITEM p0142
rule 1: {"polarity": "ALLOW", "actor": "We", "action": "collect (operation: collection)", "data": "information", "recipient": "", "source": "", "purpose": "for Children and teens to use our Products and Services", "condition": "only as much information as is reasonably necessary for Children and teens to use our Products and Services", "condition_predicate": "[untranslated: only as much information as is reasonably necessary for Children and teens to use our Products and Services]"}
rule 2: {"polarity": "DENY", "actor": "Life360", "action": "collect (operation: collection)", "data": "additional information", "recipient": "", "source": "your Child", "purpose": "", "condition": "or to withdraw permission for Life360 to collect any additional information from your Child", "condition_predicate": "request.withdraw_consent"}
--- section of rule 1 and rule 2
Life360 does not knowingly collect personal information from children under 13 or under the minimum age requiring parental consent in each jurisdiction where our Services are offered (“Child” or “Children”) without obtaining the consent of a parent or guardian as required under applicable law.
If Life360 learns that we have inadvertently collected personal information of a child without parental consent as required by law, we will take appropriate steps to delete this information. If you are a parent or guardian and discover that your child has a registered account with our Services or is using our Products without your consent, please alert us immediately by emailing
privacy@life360.com
.
A. Setting up a Child Account
If a parent wishes to add a member who is a Child to our Services, we request the parent or guardian provide consent as required by applicable law. The Child will then be able to participate in most aspects of the Life360 Services. In some instances, our Products are intended to be worn and used by Children and pets. By providing the Products to a Child, you represent and warrant to Life360 that you consent to such Child’s use of our Products and Services and further consent as a parent to enable and permit Life360’s collection and use of the information from the Products and Services used by the Child as stated in this Privacy Policy and the
Terms of Service
.
B. Personal Information We Collect about Children and Teens
We take special precautions to collect only as much information as is reasonably necessary for Children and teens to use our Products and Services. We retain personal information of Children and Teens for as long as reasonably necessary to provide our Products and Services as further set forth in Section VII. E of this Privacy Policy.
C. Information Disclosures about Children and Teens
Life360 may disclose the personal information of Children and Teens to our service providers and our business partners that offer integrated services as described in this Privacy Policy. We do not share or sell personal information of members we know to be under 18, nor do we show ads in Child or Teen accounts. Profile and location information of Children and Teens using the Service may be shared with other members of any Circle they join and Children and Teens may exchange messages with those Circle members. You are responsible for monitoring your Child or Teen’s account and location-sharing activity through our Products and Services and for blocking or permitting location-sharing features.
D. Managing your Child’s Account or Information
A parent or legal guardian may have a right to request to review or have deleted their Child’s personal information and may withdraw consent for our Products and Services to collect any further personal information from their Child. Please contact us at
privacy@life360.com
to request to review and/or delete any personal information we may have collected from your Child, or to withdraw permission for Life360 to collect any additional information from your Child. We will require the parent or guardian to provide us with sufficient identification before providing access to such personal information, or acting upon such request.
VII. HOW WE PROTECT YOUR INFORMATION
Life360 cares about the security of your information. The actions we take to protect your personal information are described below.
A. Security
We have implemented appropriate standards to reduce the risk of unauthorized or unlawful access of your personal information. No security system is impenetrable and we cannot absolutely guarantee the security of our systems and your information.
We will never send you unsolicited messages or contact you by phone to request sensitive information, such as your account ID, password, payment, or national ID numbers.
=== END ITEM p0142

=== ITEM p0143
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "need (operation: collection)", "data": "additional information", "recipient": "", "source": "you", "purpose": "to make sure that the request does come from you", "condition": "Since we don’t necessarily collect your email address; sometimes", "condition_predicate": "([untranslated: Since we don’t necessarily collect your email address] AND [untranslated: sometimes])"}
rule 2: {"polarity": "DENY", "actor": "BeReal", "action": "collects (operation: collection)", "data": "personal data", "recipient": "", "source": "", "purpose": "", "condition": "concerning children under 13 years of age", "condition_predicate": "user.age < 13"}
--- section of rule 1
8. What rights do you have over your information
Privacy is a fundamental human right. That means every person that uses our App, irrespective of where they reside, can expect the same things from us. Whether you are in Europe, one of the 50 U.S. States, Latin America, the Middle East, Africa, Japan, Asia Pacific, or anywhere in between, you can:
Right to access and obtain a copy of your data
: you may request access to your personal data. If you request such access, we will provide you with all the information required by law, including the purposes of the processing, the categories of data processed, the categories of recipients, the data retention periods and your rights.
Right of rectification
: You may also ask us to rectify any personal data concerning you that is inaccurate and to complete any incomplete information.
Right to erasure/deletion
: Under certain circumstances, you may request the erasure of your personal data. We may nevertheless need to retain certain limited data in an archived database, in particular if we have a legal obligation to retain such personal data or if it is necessary for the exercise or defense of legal claims.
Right to restrict processing
: In certain circumstances, you may request the limitation of the processing of your personal data, in particular when you request the rectification of your personal data.
Right to withdraw your consent
: Where the processing of your personal data is based on your consent, you may, at any time, withdraw any consent you have previously provided to us. Such withdrawal does not affect the lawfulness of processing based on consent prior to withdrawal.
Right to object
: You may also object at any time to the processing of your Personal Data when it is used for commercial prospecting purposes or for reasons related to your particular situation.
Right to portability
: In certain cases, you may also obtain a copy of your personal data, in a commonly used and machine-readable format, to enable you to exercise your right to data portability.
Right to set instructions for how your data is processed post-mortem
: If you are a French user, you also have the right to set directives concerning the management of your personal data after your death.
If you are in the European Union, EFTA States or the United Kingdom, and wish to raise a concern about our data processing practices, you have the right to do so with your local supervisory authority or BeReal’s lead supervisory authority, the Commission Nationale de l’Informatique et des Libertés (CNIL), using the
contact details listed on their website
.
Some of these rights (rectification, deletion and consent withdrawal) can be exercised directly from the App, in the setting section. You can also exercise these rights and all other rights by addressing your request to our Data Protection Team at
dpo@bere.al
. Since we don’t necessarily collect your email address, we sometimes will need additional information to make sure that the request does come from you.
--- section of rule 2
4. Children’s data
BeReal never knowingly or willingly collects any personal data concerning children under 13 years of age. If you are under 13, please do not use BeReal.
=== END ITEM p0143

=== ITEM p0144
rule 1: {"polarity": "ALLOW", "actor": "Firma Superplay", "action": "przekazywać (operation: disclosure by transmission)", "data": "informacje", "recipient": "partnerom biznesowym", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "Superplay", "action": "공유하지 (operation: disclosure by transmission)", "data": "정보", "recipient": "", "source": "", "purpose": "교차 맥락적 행동 광고 목적으로", "condition": "16세 미만 소비자의", "condition_predicate": "user.age < 16"}
--- section of rule 1
Rezygnacja z otrzymywania wiadomości e-mail i powiadomień push
Jeśli użytkownik chce zrezygnować z otrzymywania wiadomości promocyjnych lub marketingowych od firmy Superplay, może to zrobić poprzez:
Kliknięcie „anuluj subskrypcję” w dowolnej promocyjnej wiadomości e-mail z określonej usługi Superplay, aby zmienić i zaktualizować preferencje dotyczące kontaktu w przypadku wiadomości e-mail od nas (uwaga: wciąż możemy kontaktować się z użytkownikiem poprzez pocztę e-mail w związku z jego kontem, na przykład w celu zresetowania hasła lub innego zarządzania kontem).
Jeśli użytkownik chce zrezygnować z powiadomień push od firmy Superplay, może to zrobić poprzez:
Zmianę ustawień na platformach mediów społecznościowych w celu wyłączenia powiadomień od firmy Superplay za pośrednictwem tych platform. Na przykład można tak zrobić wyłączając powiadomienia od firmy Superplay na Facebooku, oraz
Zmianę ustawień urządzenia i/lub przeglądarki w celu wyłączenia powiadomień push z naszej Usługi. W niektórych naszych aplikacjach mamy również opcję wyłączenia powiadomień push w ustawieniach gry.
Rezygnacja z wyświetlania spersonalizowanych reklam
W zależności od miejsca zamieszkania użytkownika i miejsca, z którego uzyskuje on dostęp do naszych usług, użytkownik może mieć prawo do rezygnacji z otrzymywania dostosowanych reklam stron trzecich. Jeśli użytkownik chce zrezygnować z otrzymywania dostosowanych reklam stron trzecich, powinien skontaktować się z nami, korzystając z sekcji Kontakt poniżej.
Użytkownik może zrezygnować ze spersonalizowanych reklam, dostosowując ustawienia śledzenia reklam na swoim urządzeniu (urządzeniach). Można to zrobić poprzez zresetowanie identyfikatora reklamowego na urządzeniu (np. IDFA) lub można pobrać aplikacje, takie jak aplikacja „AppChoices” firmy Digital Advertising Alliance, które mogą pomóc w kontrolowaniu gromadzenia i wykorzystywania informacji między aplikacjami w celu spersonalizowania reklam.
Narzędzia stron trzecich umożliwiające rezygnację, takie jak aplikacja AppChoices, są niezależnie obsługiwane i stanowią ich własność. Firma Superplay nie kontroluje, nie obsługuje ani nie zatwierdza tych narzędzi ani wyborów dokonywanych przez reklamodawców i inne podmioty za pośrednictwem tych narzędzi. Narzędzia te zostały wymienione tutaj wyłącznie jako udogodnienie dla graczy.
Firma Superplay nie reaguje obecnie na sygnały „Nie śledź” na żadnej z platform obsługujących nasze Usługi.
Uwaga: użytkownik może nadal otrzymywać reklamy od firmy Superplay i stron trzecich w grach Superplay, nawet jeśli zrezygnuje ze spersonalizowanych reklam, ale reklamy te nie będą dopasowane do użytkownika.
INFORMACJE OGÓLNE
Sekcja ta zawiera dodatkowe informacje o tym, jak dbamy o dane użytkownika, w tym o tym, jak je zabezpieczamy, jak długo je przechowujemy i w jakich okolicznościach możemy przekazywać je za granicę.
Przesyłanie danych za granicę
Firma Superplay może wysyłać, mieć dostęp, wykorzystywać i/lub przechowywać informacje poza krajem lub regionem zamieszkania użytkownika, w tym na przykład do Stanów Zjednoczonych i Izraela. Firma Superplay może przekazywać informacje jej podmiotom stowarzyszonym, podmiotom zależnym, sprzedawcom, partnerom biznesowym i innym podmiotom w sposób opisany w tej Polityce prywatności.
Obowiązujące przepisy różnią się w zależności od jurysdykcji, dlatego przepisy dotyczące ochrony danych i prywatności obowiązujące w miejscach, do których informacje są przekazywane lub gdzie są przechowywane, wykorzystywane lub przetwarzane, mogą różnić się od przepisów obowiązujących w miejscu zamieszkania użytkownika. Podczas przesyłania informacji poza miejsce, w którym zostały one zebrane, wprowadzamy odpowiednie zabezpieczenia lub w inaczej dokładamy starań, aby takie transfery spełniały obowiązujące lokalne wymogi prawne. Jeśli chcesz uzyskać więcej informacji na temat przesyłania danych za granicę przez firmę Superplay, skorzystaj z sekcji „Kontakt z nami” poniżej.
--- section of rule 2
CCPA
수집
정보
범주
수집된
정보의
예
정보의
출처
정보
수집의
사업
목적
공개된
제
3
자
범주
판매
/
공유된
제
3
자
범주
식별
정보
이름(성과 이름), 별칭, 주소, 전화번호, 이메일 주소, 고유 개인 식별 정보, 온라인 식별 정보, IP 주소.
여러분으로부터 직접;
여러분의 서비스 이용으로부터 간접적으로;소셜 미디어 플랫폼 또는 여러분 친구를 포함한 제3자로부터.
저희의 서비스와 기술 지원을 제공하기 위해;
정보 요청에 대응하기 위해;여러분에게 여러분이 관심이 있을 수 있다고 생각되는 정보와 광고를 제공하기 위해;서비스를 관리하고 개선하기 위해.
저희 서비스 제공을 도울 수 있도록 저희 서비스 제공자에게
공유
:
당사의 분석 및 광고 서비스 제공업체와.
캘리포니아
고객
기록법에
나열된
개인
정보
범주
이름, 서명, 신체적 특징이나 설명, 주소, 전화번호, 신용카드 번호, 직불카드 번호 또는 기타 금융 정보.
여러분으로부터 직접;
여러분의 서비스 이용으로부터 간접적으로;소셜 미디어 사이트나 친구를 포함한 제3자로부터.
저희의 서비스와 기술 지원을 제공하기 위해;
정보 요청에 대응하기 위해;여러분에게 여러분이 관심이 있을 수 있다고 생각되는 정보와 광고를 제공하기 위해;서비스를 관리하고 개선하기 위해.
저희 서비스 제공을 도울 수 있도록 저희 서비스 제공자에게
없음
캘리포니아
또는
연방법에
따른
보호
분류
특성
나이.
여러분으로부터 직접.
서비스를 관리하고 개선하기 위해;
법적 의무를 준수하기 위해.
저희 서비스 제공을 도울 수 있도록 저희 서비스 제공자에게
없음
상업
정보
구매, 취득 또는 고려한 개인 재산, 제품 또는 서비스에 대한 기록이나 기타 구매 또는 소비 내역 또는 경향에 대한 기록
여러분으로부터 직접;
여러분의 서비스 이용으로부터 간접적으로.
저희 서비스를 제공하기 위해;
정보 요청에 대응하기 위해;여러분에게 여러분이 관심이 있을 수 있다고 생각되는 정보와 광고를 제공하기 위해;서비스를 관리하고 개선하기 위해
저희 서비스 제공을 도울 수 있도록 저희 서비스 제공자에게
공유
:
당사의 분석 및 광고 서비스 제공업체와.
생체
정보
홍채, 망막, 지문, 얼굴, 손, 손바닥의 이미지.
수집되지 않음.
해당 사항 없음.
해당 사항 없음.
해당 사항 없음.
인터넷
또는
기타
전자
네트워크
활동
정보
검색 기록, 탐색 기록, 웹사이트, 애플리케이션 또는 광고와 소비자의 상호작용에 대한 정보.
여러분의 기기; 쿠키.
서비스를 개선하고 향상하기 위해; 보안, 법률, 규정 준수 및 규제 의무를 위해.
당사 서비스 제공자 또는 제휴사에게.
공유
:
당사의 분석 및 광고 서비스 제공업체와.
지리적
위치
데이터
물리적 위치.
여러분의 기기(IP 주소).
서비스를 개선하고 향상하기 위해; 보안, 법률, 규정 준수 및 규제 의무를 위해.
당사 서비스 제공자 또는 제휴사에게.
공유
:
당사의 분석 및 광고 서비스 제공업체와.
감각
데이터
오디오, 전자, 시각, 열, 후각 또는 이와 유사한 정보.
수집되지 않음.
서비스를 개선하고 향상하기 위해; 보안, 법률, 규정 준수 및 규제 의무를 위해.
당사 서비스 제공자 또는 제휴사에게.
없음.
직업
또는
업무
관련
정보
고용주 또는 다른 회사 소속, 직함, 회사 연락처 정보. 고용 이력에 대한 정보.
수집되지 않음.
해당 사항 없음.
해당 사항 없음.
해당 사항 없음.
비공립
교육
정보
여러분의 교육적 배경에 대한 특정 정보.
수집되지 않음.
해당 사항 없음.
해당 사항 없음.
해당 사항 없음.
다른
개인
정보에서
도출된
추론
정보
개인의 선호도, 특성, 심리적 경향, 소질, 행동, 태도, 지능, 능력, 적성을 반영하는 프로필.
저희는 여러분의 관심사에 대한 프로필을 만들 수 있습니다.
마케팅 목적으로. 게임 경험을 개인화합니다.
당사 서비스 제공자 또는 제휴사에게.
공유
:
당사의 분석 및 광고 서비스 제공업체와.
민감한
개인
정보
소비자 계정 로그인과 필수 비밀번호, 보안 코드와 함께 제공되는 카드 번호, 정확한 지리적 위치, 채팅이나 포럼 기능을 통한 서비스의 메시지 내용을 공개하는 정보.
여러분으로부터 직접.
여러분의 서비스 이용으로부터 간접적으로.
저희 서비스를 제공하기 위해.
서비스를 개선하고 향상하기 위해; 보안, 법률, 규정 준수 및 규제 의무를 위해.Superplay는 소비자에 대한 특성을 추론하는 목적으로 민감한 개인정보를 사용하지 않습니다.
저희 서비스 제공을 도울 수 있도록 저희 서비스 제공자에게
해당 사항 없음.
Superplay는 16세 미만 소비자의 정보를 교차 맥락적 행동 광고 목적으로 판매하거나 공유하지 않습니다. 분석 및 광고 목적으로 정보를 익명화할 수 있으며, 이 경우 정보를 다시 식별하려고 시도하지 않습니다.
재정적
인센티브
공지
.
저희는 특정 특전 또는 독점 혜택과 같은 인센티브뿐만 아니라 경품 행사 또는 콘테스트와 같은 기타 프로그램을 제공합니다. 이러한 프로그램의 목적을 위해 여러분의 이름과 연락처 정보, 그리고 서비스 사용에 대한 정보를 수집할 수 있습니다. 저희는 위에 설명한 대로 이 정보를 공개, 판매 또는 공유할 수 있습니다. 이러한 인센티브 또는 프로그램은 미국 주 개인정보 보호법에 따라 “재정적 인센티브” 또는 “진정한 로열티 프로그램”으로 간주할 수 있습니다.
이러한 프로그램을 통해 얻은 정보에 가치를 부여하도록 법적으로 요구받는 경우, 저희는 여러분의 관심사에 맞는 미래 혜택을 공유하는 것의 가치에 따라 수집 및 사용된 정보를 평가할 것입니다. 이러한 가치는 수집된 정보의 범주와 제공 또는 홍보되는 제품에 따라 달라질 수 있습니다.
모든 인센티브 프로그램 참여는 자발적이며, 인센티브 프로그램에 가입하면 프로그램과 관련하여 여러분의 정보 수집, 사용 및 공개에 동의하는 것입니다. 나중에 동의를 철회하고 싶으시다면 저희에게 연락하시거나 해당 프로그램의 이용 약관에 명시된 지침을 따르시면 됩니다.
여러분이 여러분의 정보 판매나 공유 또는 타겟 광고에 대한 여러분의 정보 사용을 거부하더라도 저희 프로그램 참여에는 영향을 미치지 않으며, 여러분이 받을 자격이 있는 모든 혜택을 계속 받으실 수 있습니다. 그러나 여러분이 여러분의 모든 정보를 삭제하도록 요청하실 경우, 저희는 여러분이 받을 자격이 있었던 혜택과 여러분을 연계하거나 해당 혜택과 관련하여 여러분에게 연락할 방법이 없으므로 더 이상 여러분에게 어떠한 프로그램 혜택도 제공할 수 없습니다.
쿠키
및
기타
기술
저희는 쿠키 및 기타 기술을 사용하여 여러분이 당사의 서비스와 웹사이트를 어떻게 사용하는지에 대한 정보를 수집하여 서비스 개선 및 광고 타겟팅 등의 작업에 도움을 받을 수 있습니다.
또한, 새로운 기능을 제공하거나 서비스 기능을 지원하는 등 다른 목적으로 인공지능(AI)을 포함한 기술을 배포할 수 있습니다.
쿠키
및
유사
기술
쿠키는 기록 보관 목적으로 귀하의 기기에 전송되는 작은 데이터 파일입니다. 쿠키에 포함된 정보는 귀하의 검색 활동과 같은 정보와 연결될 수 있습니다. 저희는 여러분의 기기에 쿠키를 두어 저희 서비스의 품질을 개선하고, 저희 서비스 사용을 더욱 편리하게 만들고, 타겟 광고를 게재하는 등의 목적으로 사용할 수 있습니다. 제3자 광고주 및 서비스 제공자도 아래 설명된 대로 여러분의 기기에 쿠키나 기타 기술을 사용하거나 두거나 읽을 수 있으며, 이러한 관행은 자체 정책의 적용을 받습니다.
쿠키에는 두 가지 유형이 있습니다. 필수 쿠키와 비필수 쿠키 저희는 필수 쿠키를 사용하여 여러분을 Superplay 웹사이트의 다른 사용자와 구별하고 당사 웹사이트를 원활하게 운영합니다.
웹 브라우저를 설정하거나 타사 플러그인을 활용하여 기기에 쿠키를 배치하려는 시도에 대해 경고하거나 기기에 배치할 수 있는 쿠키 유형을 제한함으로써 필수 쿠키를 포함한 모든 쿠키를 차단할 수 있습니다.
쿠키를 사용하는 Superplay 웹사이트에서는 웹사이트를 처음 방문했을 때 쿠키 배너를 통해 쿠키 설정과 동의를 사용자 지정할 수 있으며, 웹페이지 바닥글이나 쿠키 위젯에 있는 “쿠키 설정” 링크를 클릭하여 언제든지 기본 설정을 변경할 수 있습니다.
=== END ITEM p0144

=== ITEM p0145
rule 1: {"polarity": "ALLOW", "actor": "We", "action": "use (operation: use)", "data": "PI", "recipient": "", "source": "", "purpose": "for the additional purposes explained at the time of collection (such as in the applicable privacy policy or notice)", "condition": "in a context that is not a Sale or Share under applicable U.S. State Privacy Laws", "condition_predicate": "[untranslated: in a context that is not a Sale or Share under applicable U.S. State Privacy Laws]"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "use (operation: use)", "data": "PI", "recipient": "", "source": "", "purpose": "for Targeted Advertising", "condition": "of Consumers who meet the definition of a “child” (or other similar term) under applicable U.S. State Privacy Laws; unless we receive affirmative opt-in authorization from (i) the Consumer, if that person is at least 13 years of age and Consumer consent is required under the applicable law, or (ii) the parent or guardian of the Consumer, if the Consumer is less than 13 years of age", "condition_predicate": "([untranslated: of Consumers who meet the definition of a “child” (or other similar term) under applicable U.S. State Privacy Laws] AND NOT ((opt_in.sale_sharing_targeted_advertising AND user.age >= 13 AND [untranslated: Consumer consent is required under the applicable law]) OR (user.parental_consent AND user.age < 13)))"}
--- section of rule 1
US STATE PRIVACY NOTICE
Last updated effective March 1, 2025
This U.S. State Privacy Notice (“Notice”) applies to “Consumers” as defined respectively under the California Consumer Privacy Act of 2020, as amended by the California Privacy Rights Act (collectively, the “CCPA”), Colorado Privacy Act (“Colorado Law”), Utah Consumer Privacy Act (“Utah Law”), Connecticut Act Concerning Personal Data Privacy and Online Monitoring (“Connecticut Law”), Virginia Consumer Data Protection Act (“Virginia Law”), Nevada Privacy of Information Collected on the Internet from Consumers Act (“Nevada Law”), Delaware Personal Data Privacy Act (effective January 1, 2025) (“Delaware Law”), Florida Digital Bill of Rights (effective July 1, 2024) (“Florida Law”), Iowa Act Relating to Consumer Data Protection (effective January 1, 2025) (Iowa Law”), Montana Consumer Data Privacy Act (effective October 1, 2024) (“Montana Law”), Nebraska Data Privacy Act (effective January 1, 2025) (“Nebraska Law”), New Hampshire Act Relative to the Expectation of Privacy (effective January 1, 2025) (“New Hampshire Law”), New Jersey Act Concerning Online Services (effective January 15, 2025) (“New Jersey Law”), Oregon Consumer Privacy Act (effective July 1, 2024) (“Oregon Law”), Texas Data Privacy and Security Act (effective July 1, 2024) (“Texas Law”), and all laws implementing, supplementing, or amending the foregoing, including regulations promulgated thereunder, as well as any additional U.S. state privacy laws now or hereafter applicable to the Company (each a “U.S. State
Privacy Law” and collectively, “U.S. State Privacy Laws”). Capitalized terms used but not defined in this Notice shall have the meanings given to them under the relevant U.S. State Privacy Laws or (if applicable) in other sections of our Privacy Policy.
Applicability
Section A of this Notice provides notice of our data practices, including our collection, use, disclosure, and sale of Consumers’ personal information or personal data under relevant U.S. State Privacy Laws (collectively, “PI”).
Sections B-F of this Notice provide information regarding Consumer rights under applicable U.S. State Privacy Laws and how you may exercise them.
Section G of this Notice provides additional information for residents of certain states only.
A. Notice of Data Practices
The description of our data practices in this Notice covers the twelve (12) months prior to the Effective Date and will be updated at least annually. Our data practices may differ between updates to this Notice; however, if materially different from this Notice, we will provide supplemental pre-collection notice of the current practices, which may include references to other privacy policies, notices, or statements. Otherwise, this Notice serves as our notice at collection. We may receive or collect your PI directly from you or from your Devices, from Third Party Services, or from other individuals and businesses, as well as public sources of data.
Generally, we process your PI to provide you our Services and as otherwise related to the operation of our business, including for one or more of the following Business Purposes: Performing Services; Managing Interactions; Security; Debugging; Providing Advertising & Marketing Services; Quality Assurance; Processing Interactions and Transactions; and Research and Development. We may also use PI for other Business Purposes in a context that is not a Sale or Share under applicable U.S. State Privacy Laws, such as disclosing it to our Service Providers, Contractors, or Processors that perform services for us (“Vendors”), to you, or to other parties at your direction or through your action; for the additional purposes explained at the time of collection (such as in the applicable privacy policy or notice); as required or permitted by applicable law; to the government or private parties to comply with law or legal process; and in Business Transactions (collectively, “Additional Business Purposes”).
--- section of rule 2
In addition, the agent is subject to the verification standards applicable to the type of request(s) made.
iii. Our Responses
Some PI that we maintain is insufficiently specific for us to be able to associate it with a Consumer. We do not include that PI in response to those requests. If we deny a request, in whole or in part, we will explain the reasons in our response.
We will make commercially reasonable efforts to identify Consumer PI that we process to respond to your Consumer request(s). In some cases, particularly with voluminous and/or typically irrelevant data, we may suggest you receive the most recent or a summary of your PI and give you the opportunity to elect whether you want the rest. We reserve the right to direct you to where you may access and copy responsive PI yourself. We may also refuse to act upon a request that is excessive, repetitive, unfounded, or overly burdensome.
D. Non-Discrimination/Non-Retaliation
We will not discriminate or retaliate against you in a manner prohibited by applicable U.S. State Privacy Laws for your exercise of your Consumer privacy rights.
E. Our Rights and the Rights of Others
Notwithstanding anything to the contrary, we may collect, use and disclose your PI as required or permitted by applicable law and this may limit or affect your rights under U.S. State Privacy Laws. In addition, we are not required to honor your requests to the extent that doing so would infringe upon our or another person’s rights or conflict with applicable law.
F. Additional Notices for California Residents
This Notice provides additional information on our online practices and the rights of residents of certain states related to the AppLock Services.
i. Shine the Light—California Residents
We also provide California residents with the option to opt-out of the disclosure of “personal information,” as defined by California’s “Shine the Light” law, with third parties (other than with Company affiliates) for such third parties own direct marketing purposes. California residents may exercise this opt-out, request information about our Shine the Light law compliance, and/or obtain a disclosure of third parties we have disclosed information to and the categories of information disclosed. California residents may make such a request, or inquire further about our compliance with this law, by emailing
[email protected]
or mailing us at the address set forth in the Contact Us section above. You must put the statement “Shine the Light Request” in the body of your correspondence. In your request, please attest to the fact that you are a California resident and provide a current California address for your response. This right is different than, and in addition to, CCPA rights, and must be requested separately. We are only required to respond to one request per person each year. We are not required to respond to requests made by means other than through the provided e-mail address or mailing address (requests by phone, fax, chats, social media, etc.). We are not responsible for requests that are incomplete or not labeled and sent properly.
ii. Affirmative Opt-In for Sale or Sharing, or use for Targeted Advertising, of PI of “Child” Residents of Certain States
We do not knowingly Sell or Share, or use for Targeted Advertising, the PI of Consumers who meet the definition of a “child” (or other similar term) under applicable U.S. State Privacy Laws, unless we receive affirmative opt-in authorization from (i) the Consumer, if that person is at least 13 years of age and Consumer consent is required under the applicable law, or (ii) the parent or guardian of the Consumer, if the Consumer is less than 13 years of age. If you think we may have unknowingly Sold or Shared PI, or used PI for Targeted Advertising, of a Consumer under the threshold age (as set by the applicable U.S.
=== END ITEM p0145

=== ITEM p0146
rule 1: {"polarity": "ALLOW", "actor": "Apple", "action": "shares (operation: disclosure)", "data": "your personal data", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "Apple", "action": "“share” (operation: disclosure)", "data": "your personal data", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1
Apple Privacy Policy
Updated July 30, 2025
Apple’s Privacy Policy describes how Apple collects, uses, and shares your personal data.
In addition to this Privacy Policy, we provide data and privacy information embedded in our products and certain features that ask to use your personal data. This product-specific information is accompanied by our Data & Privacy Icon.
You will be given an opportunity to review this product-specific information before using these features. You also can view this information at any time, either in settings related to those features and/or online at
apple.com/legal/privacy/data
.
You can familiarize yourself with our privacy practices, accessible via the headings below, and
contact us
if you have any questions.
What Is Personal Data at Apple?
At Apple, we believe strongly in fundamental privacy rights — and that those fundamental rights should not differ depending on where you live in the world.
That’s why we treat any data that relates to an identified or identifiable individual or that is linked or linkable to them by Apple as “personal data,” no matter where the individual lives.
This means that data that directly identifies you — such as your name — is personal data, and also data that does not directly identify you, but that can reasonably be used to identify you — such as the serial number of your device — is personal data. Aggregated data is considered non‑personal data for the purposes of this Privacy Policy.
This Privacy Policy covers how
Apple or an Apple-affiliated company
(collectively, “Apple”) handles personal data whether you interact with us on our websites, through Apple apps (such as Apple Music or Wallet), or in person (including by phone or when visiting an Apple Store). Apple may also link to third parties on our services or make third-party apps available for download in our App Store. Apple’s Privacy Policy does not apply to how third parties define personal data or how they use it. We encourage you to read their privacy policies and know your privacy rights before interacting with them.
Your Privacy Rights at Apple
At Apple, we respect your ability to know, access, correct, transfer, restrict the processing of, and delete your personal data. We have provided these rights to our global customer base and if you choose to exercise these privacy rights, you have the right not to be treated in a discriminatory way nor to receive a lesser degree of service from Apple. Where you are requested to consent to the processing of your personal data by Apple, you have the right to withdraw your consent at any time.
To exercise your privacy rights and choices, including where a third-party service provider is acting on Apple’s behalf, visit the Apple Data and Privacy page at
privacy.apple.com
for Apple or
shazam.com/privacy
for Shazam.
To help protect the security of your personal data, you must sign in to your account and your identity will be verified. If you want to obtain a copy of personal data that is not currently available from
privacy.apple.com
, you can make a request at
apple.com/legal/privacy/contact
. You also have the right to lodge a complaint with the applicable regulator.
There may be situations where we cannot grant your request — for example, if you ask us to delete your transaction data and Apple is legally obligated to keep a record of that transaction to comply with law. We may also decline to grant a request where doing so would undermine our legitimate use of data for anti-fraud and security purposes, such as when you request deletion of an account that is being investigated for security concerns. Other reasons your privacy request may be denied are if it jeopardizes the privacy of others, is frivolous or vexatious, or would be extremely impractical or unreasonable.
If you live in California and you cannot access Apple’s Data and Privacy page,
you or your authorized agent can make a request at
apple.com/legal/privacy/contact
or by calling 1-800-275-2273.
--- section of rule 2
We may also disclose information about you where there is a lawful basis for doing so, if we determine that disclosure is reasonably necessary to enforce our terms and conditions or to protect our operations or users, or in the event of a reorganization, merger, or sale.
Apple does not sell your personal data including as “sale” is defined in Nevada and California. Apple also does not “share” your personal data as that term is defined in California.
Protection of Personal Data at Apple
At Apple, we believe that great privacy rests on great security. We use
administrative, technical, and physical safeguards
to protect your personal data, taking into account the nature of the personal data and the processing, and the threats posed. We are constantly working to improve on these safeguards to help keep your personal data secure. For more information, visit our
Apple Platform Security
guide.
Children and Personal Data
Apple understands the importance of safeguarding the personal data of children, which we consider to be an
individual under the age of 13 or the equivalent age as specified by law in your jurisdiction
. That is why Apple has implemented additional processes and protections to help keep children’s personal data safe.
To access certain Apple services, a child must have a child Apple Account. A child Apple Account may be created by the
parent
or, in the case of a Managed Apple Account, by the
child’s educational institution
.
Parents.
To create a child account, parents must review the
Family Privacy Disclosure for Children
, which describes how Apple handles children’s personal data. If they agree, the parent must provide Apple with a verifiable parental consent.
Educational Institutions.
Educational institutions that participate in the Apple School Manager Program may also create Apple IDs for students, called “Managed Apple IDs.” These schools are required to agree to the
Managed Apple IDs for Students Disclosure
which is included as Exhibit A to the Apple School Manager Agreement.
If we learn that a child’s personal data was collected without appropriate authorization, it will be deleted as soon as possible.
To exercise privacy rights for your child’s information, visit the Apple Data and Privacy page at
privacy.apple.com
and sign in to their account.
Cookies and Other Technologies
Apple’s websites, online services, interactive applications, and advertisements may use
“cookies” and other technologies
such as web beacons.
These technologies help us to better understand user behavior including for security and fraud prevention purposes, tell us which parts of our websites people have visited, and facilitate and measure the effectiveness of advertisements and web searches.
Communications Cookies.
These cookies are used to enable network traffic to and from Apple’s systems, including by helping us detect any errors.
Strictly Necessary Cookies.
These cookies are set as required to provide a specific feature or service that you have accessed or requested. For example, they allow us to display our websites in the proper format and language, to authenticate and verify your transactions, and to preserve the contents of your Bag when shopping online at
apple.com
.
Other Cookies.
These cookies are used to understand how visitors interact with our websites and online services, including by helping us to assess the effectiveness of advertisements and web searches. Apple also uses these cookies to remember choices you make while browsing, so we can provide you with a customized experience.
If you prefer that Apple not use cookies, we provide you with the means to disable their use. If you want to disable cookies and you’re using the Safari web browser, choose “Block all cookies” in Safari’s privacy settings. If you are using a different browser, check with your provider to find out how to disable cookies. Certain features of the Apple website may not be available if all cookies are disabled.
=== END ITEM p0146

=== ITEM p0147
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "use (operation: use)", "data": "copies of your information", "recipient": "", "source": "", "purpose": "to comply with our legal obligations; resolve disputes; enforce our agreements", "condition": "as necessary to comply with our legal obligations, resolve disputes, and enforce our agreements", "condition_predicate": "(law.required OR [untranslated: resolve disputes, and enforce our agreements])"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "use (operation: use)", "data": "your data", "recipient": "", "source": "", "purpose": "", "condition": "in a materially different manner; without your consent", "condition_predicate": "([untranslated: in a materially different manner] AND NOT consent.material_changes)"}
--- section of rule 1
APEC
”) Cross Border Privacy Rules System. To learn more about this program, please click
here
.
Data Security and Breach Handling
We implement appropriate technical and organizational security measures to protect your personal information against unlawful destruction, loss alteration, misuse, or unauthorized access while in our possession. All parties we contract with must agree to provide reasonable data security measures for the customer information we share with them, in compliance with applicable laws and regulations.
If we learn of a security breach that affects our users, we may send an email or other direct communication to you, or post a blog to notify the public on our Help and Support Security Center. If you have any reason to believe that your data with us has been compromised (for example, there has been unauthorized access to your account), please contact us at
privacy@ookla.com
.
Data Retention
We will retain your personal information for as long as is necessary in connection with the purposes set out in this policy, and in accordance with applicable laws. For more details on how long data is retained see the table in Section 3.
Your Rights With Respect to Your Personal Information
Many privacy regulations afford consumers a number of specific rights. The EEA, Brazil, California, and several other U.S. states grant specific rights to people living under their jurisdiction.
Your rights:
Right to Withdraw Consent:
Where you are requested to consent to the processing of your personal information, you have the right to withdraw your consent at any time.
Right to Know:
You have a right to know what personal information we collect, process, and share or sell. This policy is meant to provide transparency with regard to your data. If you have additional questions, you can email us at
privacy@ookla.com
.
Right of Access:
You can request a copy of the personal information we have collected about you from us.
Right to Delete/Erase:
You can request us to delete all the information we have collected about you. It is important to note that by exercising your right to deletion you may lose access to your account and any purchases, points or features associated with it.
Right to Request Rectification:
If you find that any of your information that we are processing is inaccurate, you can contact us to have your information corrected. In response, we will cancel or remove your information but may retain and use copies of your information as necessary to comply with our legal obligations, resolve disputes, and enforce our agreements. For certain requests, we may require additional information.
Right to Opt-out of the Sale or Sharing for Targeted Ads:
Under some circumstances we may sell or share the personal data you provide to us to provide ads to you that align with your interests. If you would prefer not to have your data sold or shared, you can opt-out of selling or sharing by submitting a request via
Privacy Portal
or by emailing
privacy@ookla.com
. We may ask for additional information to verify your request.
Right to Object to the Processing:
You can object to our processing of your personal information via our privacy portal, under certain circumstances. By objecting to processing, you may not be able to access some or all of our services. This right is limited to personal data processed for commercial purposes.
Right to Object to the Use of Sensitive Personal Information:
You have the right to object to our use of your sensitive personal information. Sensitive personal information is information about your health, race, religion, sexual orientation, gender identity, political opinions or philosophical beliefs. You should always be mindful about the personal information you share online, especially when it is sensitive in nature.
Right to Object to Automated Processing:
You have a right to object to the processing of your data for the purposes of automated decision making about you.
--- section of rule 2
How this Privacy Policy May Change
This policy may be amended or updated from time to time at our discretion. Any updates will be effective at the time of publication, unless specified otherwise. Your continued use of our services after the publication of a policy update constitutes your consent to the changes. We will notify you prior to making policy updates that materially change the way we treat your personal data, and will not use your data in a materially different manner without your consent.
A Simplified Chinese translation of this Privacy Policy is located
here
. Ookla’s China Supplemental Privacy Policy is located
here
.
=== END ITEM p0147

=== ITEM p0148
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "use (operation: use)", "data": "your Personal Information", "recipient": "", "source": "", "purpose": "To build up marketing profiles; To aid strategic development, data collection and business analytics; To manage our relationship with advertisers and partners; To enable us to provide the App through the use of appropriate technological services; To moderate content on the App in accordance with the terms of the relevant policies; To audit usage of the App; To enhance user experience in relation to the App", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "use (operation: use)", "data": "Your Personal Information including SPDI", "recipient": "", "source": "", "purpose": "", "condition": "You may request Us in writing that We cease to use Your Personal Information including SPDI and/or delete your existing Personal Information including SPDI by writing to Us at grievances@inshorts.group", "condition_predicate": "(request.cease_use OR request.delete)"}
--- section of rule 1
3. USE AND PURPOSE OF COLLECTING PERSONAL INFORMATION INCLUDING SPDI
3.1 The information collected from you including SPDI is used to ensure services with respect to the App are presented to You in the most effective manner, to carry out our obligations to You, and to communicate with You. The said communication can either be by calls, text or emails and for purposes which include transactional, service, or promotional calls or messages.
3.2 In general, We use Our best efforts to use, disclose or transfer information in aggregate form (so that no individual user is identified). However, we may use your Personal Information including SPDI for the following purposes:
To build up marketing profiles;
To aid strategic development, data collection and business analytics;
To manage our relationship with advertisers and partners;
To enable us to provide the App through the use of appropriate technological services;
To moderate content on the App in accordance with the terms of the relevant policies;
To audit usage of the App; and
To enhance user experience in relation to the App (collectively, “
Permitted Use
”).
--- section of rule 2
7. YOUR RIGHTS
7.1 You have a right to review your Personal Information including SPDI and correct any errors in Your Personal Information including SPDI available with Us by writing to us at
grievances@inshorts.group
.
7.2 You may request Us in writing that We cease to use Your Personal Information including SPDI and/or delete your existing Personal Information including SPDI by writing to Us at
grievances@inshorts.group
. In the event that you refuse to share any information, or withdraw consent to process information that you have previously given to us, we reserve the right to restrict or deny the provision of our services for which we consider such information to be necessary.
If you have questions or grievances, feel free to email Mr. Raghav Gupta, Grievance Officer at
grievances@inshorts.group
and We will attempt to address Your concerns.
Last updated in: May, 2024
=== END ITEM p0148

=== ITEM p0149
rule 1: {"polarity": "ALLOW", "actor": "We", "action": "share (operation: disclosure)", "data": "this data", "recipient": "third-party vendors supporting our technology", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "share (operation: disclosure)", "data": "this data", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1
Type of Data
How We Use This Data
Legal Basis for Processing
Whether We Share This Data
Public images, audio-video, and survey data (e.g., lidar / radar data) surrounding our NVIDIA- or partner-identified vehicles.
Public images and audio-video in clearly disclosed locations.
Publicly available or appropriately licensed datasets containing images, audio-video, or text relating to people, voices, or other personal data or scenes.
We use this data to train our AV and AI models to perform safely and reliably, including to accurately classify or generate images, audio, video, or text, or to navigate public roads or other spaces.
This data is used exclusively for the purposes of AV and AI projects and is not used or connected to personal data for our other products and services. This data is never used to uniquely identify or profile individuals.
We process this data based on our legitimate interest in developing safe and reliable AV and AI models.
We sometimes share this data with third-party vendors supporting our technology or with business partners that are also developing AV and AI technology.
We require all recipients to agree to contractual restrictions on how personal data is used, stored, and shared.
NVIDIA does not use, sell, or share “sensitive personal information” as defined by California law. However, our sharing of non-sensitive data with advertising providers may qualify as the sale of personal data or the sharing of personal data for purposes of targeted advertising.
From time to time, we may launch certain products or features (e.g., demos or beta technologies) that involve collection of personal data that falls outside the scope of this privacy policy. In those instances, we will provide you with additional privacy-related information and disclosures at the time of collection. The additional privacy disclosures will supplement this Privacy Policy and govern how we may process the personal data collected at that time.
Sharing Hashed Data for Interest-based Advertising on Third-party Platforms
If you’ve consented to receive marketing communications or recommendations, we share hashed details about your identity with third-party ad providers such as Google to serve interest-based ads to you and others. These hashed details may include your name, email, phone number, job title, organizational business affiliations, zip code, country, and social media handles.
Your information is shared in hashed form only, which means that your details are irreversibly converted to a fixed-size string of characters such as “0890f456684a70f1a9f1dbcee40c1fe847b76f338581a9a1d9202c76b1c175f4” (which is the SHA-256 hash of “NVIDIA”). Sharing information in hashed form means that third-party ad providers can only identify you if they already have the information we have shared and have hashed it themselves to match the hashed version we are sharing. Sharing information in hashed form is a way of identifying information that both parties have without sharing the information itself.
You can opt out of data sharing for interest-based advertising at any time by visiting our
Privacy Center
or by enabling an opt-out preference signal.
How to Set Up and Use an Opt-Out Preference Signal
NVIDIA websites detect and respond to Global Privacy Control signals by disabling all Performance, Personalization, and Advertising cookies. We also automatically adjust your preferences in our
Privacy Center
when we are able to connect the Global Privacy Control signal to your account or email. To enable this signal, download and use a browser or browser extension that supports the Global Privacy Control.
Data on NVIDIA Websites
If you visit any of our NVIDIA websites, we or our third-party partners collect information using cookies, web beacons, or log file information. Please see our
Cookie Policy
for more details.
--- section of rule 2
Effective date September 22, 2025 (
Archived versions
)
NVIDIA Privacy Policy
We promise to protect your privacy.
We’re committed to supporting your privacy rights.
Control your personal data
You have the right to see the data we have collected, take it with you, make corrections, withdraw consent for future uses, opt out of sales and sharing, or erase your data all together at any time.
Expect non-discrimination
You have the right to non-discriminatory treatment, regardless of whether you allow us to process your data.
Protect your privacy—and your choices
If you feel we’ve failed in any way, you have the right to lodge a complaint with a data protection authority in your region.
When we use the term “NVIDIA” we’re referring collectively to NVIDIA Corp. in the United States and to our subsidiaries and affiliates globally.
If you have an NVIDIA account or have signed up for our content with your email address, you may visit the
NVIDIA Privacy Center
to exercise your privacy rights. Otherwise, you can contact us directly at
privacy@nvidia.com
. We use your NVIDIA account or your registered email address to verify your identity.
Visiting Our Website and Interacting With Our Online Content
We collect your information when you search for information, order products, request to download content, register for events or demos, or give us feedback. This helps us deliver what you ask for, communicate with you, and better understand what your interests are. It also enables us to improve our web experiences, products and services, and find others who may be interested in them.
Type of Data
How We Use This Data
Legal Basis for Processing
Whether We Share This Data
When you visit our websites or online services, we collect your IP address, web response times, and any error message that results from your visit.
We use this data to ensure reliable responses from our websites.
We process this data as part of a contract with you to provide a service (e.g., delivering web content), and based on our legitimate interest in making and improving our products and services.
We never share this data.
When you visit our websites or online services, we collect information about your visit such as IP address, how long you have been on the website or app, or your mouse movements.
Our service provider hCaptcha uses this data to verify whether user actions meet our security requirements.
We process your data based on our legitimate interest in protecting the service from abusive automated crawling, spam, and other forms of abuse that can harm our service or other users of our service.
We never share this data.
When you visit our websites or online services, we collect a history of the content you have viewed.
We use content viewing history to understand your experience, improve our content, and customize content for you.
If you consent, we may also use content viewing history to send customized communications to you (e.g., emailed recommendations).
We process content viewing history based on our legitimate interest in making and improving our content.
We rely solely on your consent if we use content viewing history to send customized communications to you.
We never share this data.
When you register for our events or when you request content (e.g., newsletters or white papers), we collect your contact information, including your name, email address, phone number, address, and organization affiliations.
We use your request history and contact information to communicate with you about your requests, and to find other individuals and organizations that may be interested in our products and services.
If you consent, we may also use your request history and contact information to send customized communications to you (e.g., emailed recommendations).
We process your contact information with your consent or based on our legitimate interest in finding potential customers for our products and services.
=== END ITEM p0149

=== ITEM p0150
rule 1: {"polarity": "ALLOW", "actor": "We", "action": "collect (operation: collection)", "data": "data relating to you", "recipient": "", "source": "directly from you and/or your device by automatic means", "purpose": "", "condition": "when you use our Services or interact with our ads outside of our Services (for example, on third-party websites or applications); unless disable some or all cookies from your browser settings", "condition_predicate": "((event.use_services OR event.interact_ads_outside_services) AND NOT setting.disable_cookies)"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "collect (operation: collection)", "data": "any special categories of data relating to you", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1
To find out more, please press the plus sign.
We may collect data relating to you from the following sources:
directly from you when you submit it to us (for example, when registering an account with us, subscribing to our communications, sending support enquiries to us, or responding to our surveys),
directly from you and/or your device by automatic means when you use our Services or interact with our ads outside of our Services (for example, on third-party websites or applications), including through cookies or similar technologies or software development kits (SDKs),
companies that distribute or publish our Games, which may include both companies in the Rovio group and third parties (for example, platform operators),
if you interact with ads in our Games or our ads outside of our Services (for example, on third-party websites or applications), from our advertising partners involved in the delivery and measurement of those ads,
if you choose to connect a third-party account (for example, a social media account) with our Services, from the third-party account provider,
if you participate in official community groups for our Games on third-party platforms, from those community groups or the platform provider,
if you make purchases in our Games or other Services, from the third-party payment service provider involved in those transactions, or
with your consent, from other sources explained to you when asking for your consent.
Providing data to us is not mandatory. However, we are unable to provide the Services, or some parts or features of the Services, without processing your data. If you use our Services, we will collect data relating to you for some or all of the purposes described in this notice, depending on the Services you decide to use and your choices when using them. You have a number of options to limit or control the extent to which your data is processed. For example, you can choose to not connect your third-party accounts with our Games (or to utilize the privacy settings of those third-party services to control the extent to which your data is shared to us), to use options provided to you in our Games to manage your preferences regarding the use of your data for advertising purposes, to use your device settings to reset or control the use of your Advertising ID or to toggle features such as push notifications or location tracking, or disable some or all cookies from your browser settings. At the same time, please be aware that our Websites may not respond to “Do Not Track” signals in HTTP headers.
6 Who do we share your data with?
As we operate the Services globally, your data is likely to be transferred to and/or processed in countries other than your home country when you access or use our Services. Where allowed by applicable laws and regulations, you consent to the transfer of your data outside of your home country by using the Services. We routinely share data within the Rovio group and to our service providers and partners who we work with to provide the Services. By design, some information (such as your in-game alias or chat messages) may also be visible to other users of our Services. More rarely, we may need to share data when making changes to our corporate structure, when required by applicable law or regulation, or when necessary for our legal rights or someone’s vital interests. To find out more, please press the plus sign.
We may share your data with third parties to achieve the purposes described in this notice.
--- section of rule 2
We may process the following data relating to you:
your name, email address, or other contact information if you have provided them to us (for example, when creating an account with us or subscribing to our communications),
your age or information about when you were born,
online identifiers such as your in-game alias, IP address, identifiers we assign to your account, or hardware or operating system based identifiers including your Advertising ID,
technical information about the device you use to play our Games or use our other Services (for example, information about its type, model, manufacturer, operating system, language, display, processor, or memory),
your coarse location (for example, country, state, or city), inferred from your IP address,
information about your use of the Services (for example, information about your progress or purchases in our Games or other Services, your use of an account you have with us, your visits to our Websites, or your interactions with ads in our Games),
information about your interactions with our ads outside of the Services (for example, on third-party websites or applications), including information on how you were referred to our Games or other Services,
crash logs or other information related to bugs, errors, or other issues you encounter in our Services,
inferences we make based on your activity in our Services (for example, about the content you might enjoy),
messages or other communications you send to us or through the Services or related communities managed by us on third-party platforms (for example, your chat messages in our Games, emails you send to our support team, or messages you post to official community groups for the Games),
if you choose to connect a third-party account (for example, a social media account) with our Services, information we receive from the third-party account provider (for example, an account name, identifier, or email address to enable cross-device gameplay or a profile name, picture, or friends information to provide social features),
if you make purchases in our Games or other Services, information we receive from third-party payment service providers to validate those purchases (note that we do not receive your credit card or other payment method information when you make purchases in our Services),
if you have subscribed to our communications, your content preferences or other information you submit to us when subscribing to our communications,
if you participate in our surveys or other research, any comments, feedback, responses, or other information you provide to us when doing so (for example, information about your background or experience with our Games),
information about your choices regarding your data (for example, any consents you may have given or withdrawn),
any other information you choose to submit to us through our Services or otherwise, and
with your consent, other information explained to you when asking for your consent (for example, your GPS location for location-based experiences).
We do not expect or intend to collect or otherwise process any special categories of data relating to you. By special categories of data, we mean genetic, biometric or health information, information revealing racial or ethnic origin, sex life or sexual orientation, political opinions, religious or philosophical beliefs or trade union membership, or information about your criminal offences or convictions. Please do not provide this kind of information to us or use the Services to make it available to others.
5 Where do we collect your data from?
Primarily, we collect data directly from you or your device when you use our Services. However, we may also receive data about you from other companies, for example third-party login providers if you choose to use them, companies that facilitate the purchases you make in our Games, or advertising partners involved in delivering our ads to you outside of the Services.
=== END ITEM p0150

