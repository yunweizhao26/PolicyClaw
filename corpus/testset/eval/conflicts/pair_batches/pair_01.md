=== ITEM p0001
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "process (operation: processing)", "data": "Personal Data", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "us", "action": "process (operation: processing)", "data": "your Personal Data", "recipient": "", "source": "", "purpose": "", "condition": "Right to Object; Under certain circumstances; on grounds relating to the particular situation; we may be required to no longer process your Personal Data; unless object at any time, on grounds relating to the particular situation, to the processing of your Personal Data by us", "condition_predicate": "(request.object AND [untranslated: Under certain circumstances] AND [untranslated: on grounds relating to the particular situation] AND law.required AND NOT request.object)"}
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
Moreover, as set out in locally applicable Personal Data protection laws, you may have the right to: (i) request access to your Personal Data; (ii) request rectification of your Personal Data; (iii) request the erasure of your Personal Data; (iv) request a restriction on the processing of your Personal Data; (v) request Personal Data portability; or (vi) object to, or opt-out of, the processing of your Personal Data in some cases.
Right of access.
You may have the right to obtain from us a confirmation as to whether or not Personal Data concerning you is being processed, and, where that is the case, to request access to your Personal Data. The information about Personal Data processing includes the purposes of the processing, the categories of Personal Data concerned, the recipients or categories of recipients to whom your Personal Data has been or will be disclosed, etc. However, this is not an absolute right, and the interests of other individuals may restrict your right of access. Further, you may have the right to obtain a copy of your Personal Data undergoing processing. For additional copies requested, we may charge a reasonable fee based on administrative costs.
Right to rectification.
You may have the right to obtain from us the rectification of inaccurate Personal Data. Depending on the purposes of the processing, you may have the right to have incomplete Personal Data made complete, in particular by providing a supplementary statement.
Right to erasure (right to be forgotten).
Under certain circumstances, you may have the right to require us to delete your Personal Data.
Right to a restriction of processing.
Under certain circumstances, you may have the right to require us to restrict the processing of your Personal Data. In this case, the respective Personal Data will be marked and may only be processed by us for certain purposes.
Right to Personal Data portability.
Under certain circumstances, you may have the right to receive the Personal Data that you have provided us concerning you in a structured, commonly used, and machine-readable format, and to transmit this Personal Data to another entity.
Right to Object.
Under certain circumstances, you may have the right to object at any time, on grounds relating to the particular situation, to the processing of your Personal Data by us, and we may be required to no longer process your Personal Data.
These rights can be exercised by submitting a request through our
Data Rights Request Form
.
You may also contact JetBrains to get up-to-date information about the processing of your Personal Data and any Personal Data recipients.
You may lodge a complaint related to the processing of your Personal Data with the competent data protection authority for the country where you are located or with the
Czech data protection authority
, as we are based in that country.
=== END ITEM p0001

=== ITEM p0002
rule 1: {"polarity": "ALLOW", "actor": "We", "action": "collect (operation: collection)", "data": "information", "recipient": "", "source": "", "purpose": "for your convenience", "condition": "every time you communicate directly with us, transfer files, and post content on our Service", "condition_predicate": "(event.communicate_directly_with_us OR event.transfer_files OR event.post_content)"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "collect (operation: collection)", "data": "personal information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1
1.
Information We Collect
We collect information every time you communicate directly with us, transfer files, and post content on our Service for your convenience. We do not collect any information from or about you that does not have to do with our Service. We collect the following types of information:
·
Profile Information (your avatar image, nickname, and Friends List)
·
User Content
·
Unique Device Identifier
·
Chat History (excluding encrypted chat history)
·
File Transfer History (transferred file names and devices you have transferred to)
·
Non-Personal Information (phone IMEI number, phone model, rom, phone operator, location, operation system, etc.)
·
Communications between you and Dewmobile (emails, mail, feedback, etc.)
User Content.
By using the profile page of our Service, you understand and agree that we are providing a platform for you to post content to the Service and to share User Content with the users you have added (“Friends”) on the Service. This means that your Friends may see, collect, or use your User Content that you post on your profile page of our Service. You are fully responsible for the personal information you choose to submit as User Content and we cannot be held liable if someone else collects or uses it. We encourage you to use caution when posting on your profile and refrain from sharing personal information on our Service.
Device Identifiers
. When accessing our Service on a mobile device, we must access, collect, monitor, and/or store on your device "device identifier”. Device identifiers are small data files or similar data structures stored on or associated with your mobile device, which uniquely identify your mobile device.
Chat History.
We store your chat history so that whenever you access the Service you can read previous messages and in case you accidentally delete it and wish to retrieve the messages. However, we will never collect or store encrypted chat history to respect your privacy. Our encrypted chat automatically deletes messages once the receiver has read the message and exited the encrypted chat.
File Transfer History
. We store your file transfer history so that whenever you access the Service you can view and access files that you have sent or received using the Service.
--- section of rule 2
6.
Security
We are very concerned about safeguarding the confidentiality of your information. As stated before, we do not collect personal information. In order to protect the non-personal information we collect, we employ administrative, physical and electronic measures. We are well equipped to handle personal or sensitive user data securely, including transmitting the data to backend server using modern cryptography over HTTPS.
Please be aware that the security measures that we take to protect your information are not absolutely guaranteed to counter unauthorized access or use of your Non-Personal Information. Thus, we must insist that you do not share sensitive information on our Service. We ask that you not send us or disclose any sensitive Personal Information (e.g., information related to racial or ethnic origin, political opinions, religion or other beliefs, health, sexual orientation, criminal background or membership in past organizations, including trade union memberships) on or through our Service.
=== END ITEM p0002

=== ITEM p0003
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "provide access (operation: disclosure)", "data": "personal data we hold about you", "recipient": "", "source": "", "purpose": "", "condition": "If you are a resident of\nAustralia; You have the right to request access to the personal data we hold about you; Upon request; unless subject to any exceptions allowed by law", "condition_predicate": "(user.jurisdiction = Australia AND request.access AND request.access AND NOT law.permitted)"}
rule 2: {"polarity": "DENY", "actor": "Sussex", "action": "share (operation: disclosure)", "data": "personal data", "recipient": "third parties", "source": "", "purpose": "for direct marketing", "condition": "Under California Civil Code Sections 1798.83-1798.84; residents of California", "condition_predicate": "user.jurisdiction = California"}
--- section of rule 1
13. Australian Privacy Rights
If you are a resident of
Australia
, this section explains your privacy rights under the P
rivacy Act 1988 (Cth)
and the
Australian Privacy Principles (APPs)
. These principles regulate how organizations like Sussex collect, store, use, and disclose your personal data.
Your Privacy Rights Under Australian Law:
Right to Access
: You have the right to request access to the personal data we hold about you. Upon request, we will provide access in accordance with the Privacy Act, subject to any exceptions allowed by law.
Right to Correction:
If you believe any of the personal data we hold is inaccurate, incomplete, or outdated, you have the right to request corrections or updates.
Right to Anonymity or Pseudonymity:
You have the option to interact with us anonymously or through a pseudonym, provided it is lawful and practicable. However, in some cases, we may not be able to offer Site without your real identity.
Right to Opt Out of Direct Marketing:
You may request to opt out of receiving direct marketing communications from us. We will process your request promptly and cease sending such communications.
Right to Complain:
You have the right to lodge a complaint about any perceived breach of your privacy rights under the Privacy Act or the Australian Privacy Principles.
Collection, Use, and Disclosure of Personal Data:
We collect your personal data for purposes directly related to providing our Site, including:
For Contributing Bloggers:
Managing your profiles.
For Contributing Bloggers:
Processing payments
and managing services.
Communicating with you
via email, phone, or notifications.
Improving our Site
through usage analytics and feedback.
Cross-border Disclosure of Personal Data:
Your personal data may be disclosed to recipients located outside of Australia, such as our servers or third-party service providers based in the European Union. When disclosing your data to overseas recipients, we take reasonable steps to ensure your personal data is protected by the same privacy standards that apply under Australian law. However, you acknowledge that, in some cases, overseas recipients may not be subject to Australian privacy laws, and you consent to the transfer of your data on this basis.
Legal Basis for Processing Your Information:
We will collect, use, and disclose your personal data only when we have a lawful basis to do so, including:
Consent
: Where you have provided consent for us to process your personal data for a specific purpose (e.g., marketing communications).
Contract
: To fulfill a contract or provide services you have requested.
Legal Obligations:
Where we are required to process your personal data to comply with Australian laws or regulations.
Legitimate Interests:
When processing is necessary for our legitimate business interests, provided these interests do not override your fundamental rights.
Data Protection and Security Measures:
We implement industry-standard security safeguards to protect your personal data from unauthorized access, misuse, or disclosure. These include encryption, firewalls, and secure storage practices. However, no method of transmission over the internet or electronic storage is 100% secure, and we cannot guarantee absolute protection.
Making a Complaint:
If you believe that we have breached the
Privacy Act 1988 (Cth)
or the
Australian Privacy Principles
, you have the right to file a complaint. To do so, please contact us at:
Email
: support@psychologytoday.com
We will acknowledge your complaint and respond promptly, investigating the issue and taking any necessary corrective actions. If you are not satisfied with our response, you may contact the
Office of the Australian Information Commissioner (OAIC)
for further assistance.
--- section of rule 2
To the best of our knowledge, we do not share the personal data of minors under the age of 13 without consent.
No Discrimination for Exercising CCPA Rights
We will not discriminate against you if you exercise any of your rights under the CCPA. This means we will not:
Deny you services.
Provide a different level of service quality.
Additional Rights for California Residents
Under California Civil Code Sections 1798.83-1798.84, residents of California may request to opt out of sharing their personal data with third parties for direct marketing purposes. Although Sussex does not share personal data for direct marketing, you can submit a request by emailing us at support@psychologytoday.com.
=== END ITEM p0003

=== ITEM p0004
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "process (operation: processing)", "data": "your personal information", "recipient": "", "source": "", "purpose": "", "condition": "On the basis of Xiaomi’s legal obligations; In certain circumstances; by law", "condition_predicate": "(basis.legal_obligation AND [untranslated: In certain circumstances] AND law.required)"}
rule 2: {"polarity": "DENY", "actor": "", "action": "further processed (operation: processing)", "data": "your personal information", "recipient": "", "source": "", "purpose": "", "condition": "when required or permitted by applicable law; unless the fulfillment of legal responsibilities and other purposes permitted by applicable law", "condition_predicate": "((law.required OR law.permitted) AND NOT (basis.legal_obligation OR law.permitted))"}
--- section of rule 1
5. What is the legal basis for processing your personal information?
We process your personal information only where we have a valid legal basis under applicable law. Where applicable under the laws in your jurisdiction, the legal bases for processing your personal information under this Privacy Policy are:
To comply with contractual obligations
. When you create a profile, register or access Xiaomi products and its services, the purposes of processing your personal information are primarily determined by that service and we will process your personal information so that we can provide that service to you.
Please note that providing some of your personal information is mandatory (e.g., when marked as such or with an asterisk). If you do not provide such personal information, we may not be able to provide you with our products or services.
As a result of your consent
. With your consent, we may process personal information that you voluntarily provide when you participate in optional activities, such as promotions.
On the basis of Xiaomi’s legal obligations
. In certain circumstances, we may be required by law to retain or otherwise process your personal information. In some cases (e.g., for storing your personal information as a result of a dispute or by request/inquiry of a data protection supervisory authority), the processing of your personal information will be necessary for us in order to fulfill these obligations.
Within the scope of a legitimate interest
. On occasion, considering the minimum privacy impact on you, the processing of your personal information is necessary for the following legitimate interests:
Information system security, network security, and cybersecurity within Xiaomi.
To enhance system security, prevent phishing website fraud, and protect account security.
Corporate operations, due diligence, internal audit (in particular, related to information security and/or privacy).
Product development and enhancement (including analysis and optimization of Xiaomi Account settings or features).
For example, to ensure the security of our services, and to help us further understand the performance of our apps, we may record relevant information, such as the frequency of your usage, crash log information, overall usage, performance data, and app source. To prevent unauthorized vendors from unlocking devices, we may collect the Xiaomi Account ID, serial number, and IP address of the operated computer and the serial number and device info of your mobile device.
--- section of rule 2
7. How long will your personal information be stored?
As a general rule, we retain personal information for the period necessary for the purposes described in our privacy policies, or as required by applicable law. We will cease to retain and delete or anonymize personal information once the purpose of collection is fulfilled, or after we confirm your request for erasure, or after we terminate the operation of the corresponding services, except when required or permitted by applicable law, in which case, your personal information will be isolated and will not be further processed except for the fulfillment of legal responsibilities and other purposes permitted by applicable law. In such circumstances, your personal information could be made available exclusively to the parties permitted by applicable law. Once the corresponding retention periods have elapsed, such personal information will be deleted or anonymized.
=== END ITEM p0004

=== ITEM p0005
rule 1: {"polarity": "ALLOW", "actor": "our", "action": "collection (operation: collection)", "data": "your personal information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "", "action": "collected (operation: collection)", "data": "any information", "recipient": "", "source": "Healthkit users", "purpose": "for use by third parties", "condition": "without obtaining user consent; in compliance with this section", "condition_predicate": "(NOT consent.share_healthkit_data AND policy.permits)"}
--- section of rule 1
For this reason, we may transfer your information to other countries that may have different laws and data protection compliance requirements to those that apply in the country in which you are located. We remain liable under the DPF Principles if any third parties that we transfer your personal information to process it in a manner inconsistent with the DPF Principles, unless we prove that we are not responsible for the event giving rise to the damage.
FitNow Inc. and its associated affiliates and subsidiaries complies with the EU-U.S. Data Privacy Framework (EU-U.S. DPF) and the UK Extension to the EU-U.S. DPF, and the Swiss-U.S. Data Privacy Framework (Swiss-U.S. DPF) as set forth by the U.S. Department of Commerce. FitNow Inc. has certified to the U.S. Department of Commerce that it adheres to the EU-U.S. Data Privacy Framework Principles (EU-U.S. DPF Principles) with regard to the processing of personal data received from the European Union and the United Kingdom in reliance on the EU-U.S. DPF and the UK Extension to the EU-U.S. DPF. FitNow Inc. has certified to the U.S. Department of Commerce that it adheres to the Swiss-U.S. Data Privacy Framework Principles (Swiss-U.S. DPF Principles) with regard to the processing of personal data received from Switzerland in reliance on the Swiss-U.S. DPF. If there is any conflict between the terms in this privacy policy and the EU-U.S. DPF Principles and/or the Swiss-U.S. DPF Principles, the Principles shall govern. To learn more about the Data Privacy Framework (DPF) program, and to view our certification, please visit
https://www.dataprivacyframework.gov.
We are committed to staying current with developments related to the Data Privacy Framework and may update our transfer mechanisms and safeguards as necessary to remain compliant. Any updates will be reflected in this Privacy Policy.
If you are a European individual with a privacy related complaint, concern or question about FitNow Inc.'s privacy practices, please contact us through our
privacy portal
. Under certain conditions, more fully described on the Data Privacy Framework website, European individuals may invoke binding arbitration when other dispute resolution procedures have been exhausted.
Where we transfer your personal information from the EEA to recipients located outside the EEA who are not in a jurisdiction that has been formally designated by the European Commission as providing an adequate level of protection for information, we do so on the basis of standard contractual clauses. You may request a copy of the relevant standard contractual clauses using our
privacy portal
. Please note that when you transfer any personal information directly to an entity established outside the EEA, we are not responsible for that transfer of your information. We will nevertheless process your information, from the point at which we receive the data, in accordance with the provisions of this policy.
Enforcement Authority
The Federal Trade Commission has jurisdiction over our compliance with the EU-U.S. Data Privacy Framework (EU-U.S. DPF) and the UK Extension to the EU-U.S. DPF, and the Swiss-U.S. Data Privacy Framework (Swiss-U.S. DPF).
Complaints Mechanism
In compliance with the EU-U.S. DPF and the UK Extension to the EU-U.S. DPF and the Swiss-U.S. DPF, FitNow Inc. commits to resolve DPF Principles-related complaints about our collection and use of your personal information. EU and UK individuals and Swiss individuals with inquiries or complaints regarding our handling of personal data received in reliance on the EU-U.S. DPF and the UK Extension to the EU-U.S. DPF, and the Swiss-U.S. DPF should first contact FitNow Inc. at
privacy@everydayhealth.com
.
In compliance with the EU-U.S. DPF and the UK Extension to the EU-U.S. DPF and the Swiss-U.S. DPF, FitNow Inc. commits to refer unresolved complaints concerning our handling of personal data received in reliance on the EU-U.S. DPF and the UK Extension to the EU-U.S.
--- section of rule 2
If you use a third party connection or log-in (e.g., Facebook Connect, Twitter, or Google+) to access the Services, create a membership or profile on any part of the Services, access our content or forward our content to another person, platform or service, we may also receive your username or email address for those third party services or other information available about you or collected from you on those services.
Please note that Lose It! is not responsible for the information you volunteer about yourself in the discussions in certain public areas of the Services, such as forums, blogs, wikis, chat rooms, private messages, message boards or other publicly accessible interaction, or information that you choose to make public in your member profile or other areas of the Services that allow users to upload or post content. We discourage users from posting such Personal Information in this fashion. You can change your publicly available information at any time via your profile page. To request removal of your Personal Information from these areas, please contact us using our
Privacy Portal
. In some cases, we may not be able to remove your Personal Information, in which case we will let you know we are unable to do so and why.
This Privacy Policy does not cover the practices of third parties, including those that may disclose information to Lose It!.
Creation of User Information. We may also create User Information about you, such as records of your interactions with us and details of your purchase history, for internal administrative purposes and analysis. We may also use User Information you have provided to us with data obtained from third parties to enhance our records or enhance our ability to provide products and services, such as appending additional information to your profile.
Apple HealthKit
Notwithstanding the foregoing, Lose It! will not use or disclose to third parties user data gathered from the Apple, Inc. Healthkit framework or Healthkit API for advertising or other use-based data mining purposes other than improving health, or for the purpose of health research. In no event will any information be collected from Healthkit users for use by third parties in compliance with this section without obtaining user consent.
Sharing Information with Friends and in User Forums
The Lose It! Services allow you to share your diet and exercise goals and information with friends that you select. In addition, if you accept an invitation from a Coach as a part of our Ascend for Lose It! coaching service, you will enable the sharing of your Personal Diet Data information and potentially personally identifiable information with the Coach.
Please bear in mind that Lose It! cannot control what your friends or Coaches do with the information you share with them, so you should only share with friends and Coaches you trust.
The Genetic Information Nondiscrimination Act of 2008
The Genetic Information Nondiscrimination Act of 2008 (GINA) provides, as to users that are residents of the United States, that you do not need to share your genetic Information with your employer or your health insurer. Even so, you may be asked to share your Genetic Information with other insurers. These others could include life, long-term care, and disability insurance firms. You should always take care with whom you choose to share your Genetic Information.
Control of Personal information and Opt-Out Options
Lose It! values the accuracy of the information you provide. All users can
confirm, change, or update personal information you have provided to us
. If you want to opt-out of communications from Lose It!, you can do so
here
. If you change your mind, you can opt-in again here. When you opt-out of promotional communications from us, you may still receive service messages (such as an order confirmation) and legally mandated notices.
=== END ITEM p0005

=== ITEM p0006
rule 1: {"polarity": "ALLOW", "actor": "ClassDojo", "action": "transfer (operation: disclosure by transmission)", "data": "personal information", "recipient": "third parties", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "ClassDojo", "action": "rent (operation: disclosure by transmission)", "data": "your (or your child’s or teen’s)\npersonal information", "recipient": "any third party", "source": "", "purpose": "including for advertising or marketing purposes", "condition": "", "condition_predicate": "true"}
--- section of rule 1
FAQ
. Depending on your country, you may contact us as specified in this Privacy Policy to obtain a copy of the safeguards we use to transfer your
personal information
.
By using the Service, your personal information may be transferred outside your home jurisdiction, including to the United States, and to the storage of your personal information in the United States, for the purpose of hosting, using and processing the personal information in accordance with this Privacy Policy. These countries may not have the same data protection laws as the country from which you provided your personal information, and that ClassDojo may be subject to access requests and be compelled to disclose your personal information to government authorities, courts and law enforcement officials outside of your home country (including the United States). You have the right to withdraw your consent at any time by contacting us as described in the “
How Can I Contact ClassDojo With Questions
” section below.If you have questions regarding our policies and practices with respect to the transfer of your personal information outside of your home country, please contact us as set out
below
.
Basically,
Our servers are located in the U.S., so if you are using the Service from any other country, your data might be transferred to the U.S.
EU-U.S. Data Privacy Framework, Swiss-U.S. Data Privacy Framework, and UK extension to DPF
ClassDojo complies with the EU-U.S. Data Privacy Framework (EU-U.S. DPF), the UK Extension to the EU-U.S. DPF, and the Swiss-U.S. Data Privacy Framework (Swiss-U.S. DPF) as set forth by the U.S. Department of Commerce (collectively the “DPF Programs”). ClassDojo has certified to the U.S. Department of Commerce that it adheres to the EU-U.S. Data Privacy Framework Principles (EU-U.S. DPF Principles) with regard to the processing of
personal information
received from the European Union in reliance on the EU-U.S. DPF and from the United Kingdom (and Gibraltar) in reliance on the UK Extension to the EU-U.S. DPF. ClassDojo has certified to the U.S. Department of Commerce that it adheres to the Swiss-U.S. Data Privacy Framework Principles (Swiss-U.S. DPF Principles) with regard to the processing of personal information received from Switzerland in reliance on the Swiss-U.S. DPF. If there is any conflict between the terms in this Privacy Policy and the EU-U.S. DPF Principles and/or the Swiss-U.S. DPF Principles (collectively, the “DPF Principles”), the DPF Principles shall govern. To learn more about the DPF Programs, and to view our certification, please visit
https://www.dataprivacyframework.gov/
.
ClassDojo may receive from the EU, UK and Switzerland some or all of the
personal information
listed in the above section “
What Information Does ClassDojo Collect?
”. ClassDojo obtains and processes such
personal information
as a Controller or Processor, as explained in the above section “Is ClassDojo a Controller?” For all types of processing, ClassDojo commits to the DPF Principles with respect to all
personal information
received from the EU, UK and Switzerland. We may use the
personal information
received from the EU, UK and Switzerland for the purposes set forth in this Privacy Policy or as you may otherwise be notified. ClassDojo may transfer
personal information
to third parties as described in this privacy policy.
ClassDojo is responsible for the processing of personal data it receives, under the DPF Programs, and subsequently transfers to third parties acting as an agent on its behalf. ClassDojo complies with the DPF Principles for all onward transfers of personal data from the EU, UK and Switzerland, including the onward transfer liability provisions.
With respect to personal data received or transferred pursuant to the DPF Programs, ClassDojo is subject to the jurisdiction and regulatory enforcement powers of the U.S. Federal Trade Commission and other authorized statutory bodies.
--- section of rule 2
Note, however, that the LLM Service Providers may perform automated screening of the inputs and prompts for safety purposes (the “Safety Classifiers”), which shall consist solely of metadata (including classifier types, dates, counts, and confidence scores) and shall not include any inputs, prompts, or outputs themselves (including summarizations of prompts, inputs, or outputs) or any portion thereof. LLM Service Providers may retain data from Safety Classifiers. ClassDojo then receives and retains this AI output in connection with the various AI tools for only as long as your (or your child’s) account is
active
, unless we are required by law to retain it, need it to enforce our policies or to ensure the security of our community.
ClassDojo does not use any children’s
personal information
contained in any inputs, prompts, or output to train any of ClassDojo’s
AI systems
. ClassDojo will only train our
AI systems
with data that has been
de-identified information
in such a way that is not traceable to any ClassDojo user. Additionally, ClassDojo does not allow any
LLM Service Provider
or AI third-party
service provider
it may utilize to use any information (personal information or de-identified) to train, improve or develop their
AI systems
.
This commitment includes the information contained in the chart detailed in the
AI Transparency Note
(in school use) and
Parent and Child AI Transparency Page
(out of school use), such as the teacher, parent, child or teen provided inputs, used to produce the AI outputs. For more information about our retention periods for this information, please see this
chart
for in school use and this
chart
for out of school use.
Basically,
ClassDojo doesn’t
sell
or rent your information to third parties, we don’t permit
third-party advertising
on ClassDojo, and personal information collected from students and Outside School Child Users is never used for
behaviorally-targeted advertising
to students or Outside School Child Users. We use your information to provide and personalize the Service to you, optimize and improve our Service, communicate with you about our Service, and for security and safety reasons. We may also use the information provided by parents, teachers, and school leaders to provide information about events, announcements, offers, promotions, products, including third-party products that we recommend, and services we think will be of interest to you. For information about ClassDojo’s use of AI in connection with the AI Classroom Tools and AI Productivity Tools used in school, please see our
AI Transparency Note
and our
Parent and Child AI Transparency Page
(out of school use). In addition, for more information on our Dojo AI Internal Tools, please see our
Internal AI Productivity Tools FAQ
.
Will ClassDojo Share any information it collects?
ClassDojo
does not
sell
or rent
your (or your child’s or teen’s)
personal information
to any third party for any purpose - including for advertising or marketing purposes.
Third-party advertising
is not permitted on areas where users are required to log in to ClassDojo and personal information collected from students and Outside School Child Users is never used for
behaviorally-targeted advertising
to students or Outside School Child Users (by us or third-parties). Furthermore, we do not disclose personal information with any third parties except in the limited circumstances described in this Privacy Policy and as set forth below:
Other Users You Share and Communicate with on ClassDojo
: No teacher, School Leader, Admin (including District Admins), parent or guardian, student, or Outside School Child User profiles are made available to the general public through our Service. Furthermore, students cannot share their
account information
or
Portfolio
with anyone on ClassDojo, outside of their parents, teachers (including those at other schools), Admins (including District Admins), or School Leaders.
=== END ITEM p0006

=== ITEM p0007
rule 1: {"polarity": "ALLOW", "actor": "", "action": "disclosing (operation: sale)", "data": "PI", "recipient": "", "source": "", "purpose": "for commercial purposes such as for interest-based advertising", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "sell (operation: sale)", "data": "your Personal Information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1
for commercial purposes such as for interest-based advertising and disclosing PI in a manner that is deemed a sale under the CCPA or other applicable U.S. State Privacy Laws.
Identifiers
Personal Records
User Account Details/Commercial Information
Internet Usage Information
Geo-location Data
Professional or Employment Information
Inferences
B. Your Consumer Rights and How to Exercise Them
We provide Consumers the privacy rights described in this section pursuant to the requirements of their applicable U.S. State Privacy Law as of the effective date of each such law, provided any such request meets the requirements for a Verifiable Consumer Request (defined below). For residents of states without applicable U.S. State Privacy Laws, we may consider requests under this section but will apply our discretion in whether and how we process them. We may also apply state law rights in states with U.S. State Privacy Laws prior to the effective date of such laws in our sole and absolute discretion.
To submit a request to exercise your Consumer privacy rights under U.S. State Privacy Laws, or to submit a request as an authorized agent, please mail your request to the following address: AppLock, LLC, One East Erie Street, Suite 525 (#342), Chicago, Illinois 60611, Attention: Privacy, and respond to any follow-up inquiries we make. Please be aware that we do not accept or process requests through other means (via phone, fax, chats, social media, etc.). More details on the request and verification process are provided in Section C below. The Consumer rights we accommodate are as follows:
i. Right to Limit Sensitive PI Processing
With regard to PI that qualifies as Sensitive PI under U.S. State Privacy Laws, if you elect to provide us with that Sensitive PI, you will have consented to our collection and processing of it. You may submit a request to limit certain processing of your Sensitive PI to the following address: AppLock, LLC, One East Erie Street, Suite 525 (#342), Chicago, Illinois 60611 or by email at
[email protected]
. However, under applicable U.S. State Privacy Laws, your request will not affect the following permitted processing purposes, or any other purposes permitted by law:
To perform our Services at your request or at your direction;
To prevent, detect, and investigate security incidents, fraudulent activity, and illegal actions;
For short term transient use, including, but not limited to, non-personalized advertising as part of your interaction with our Services; and
To maintain or service accounts, provide User service, verify User information, or provide similar services.
ii. Right to Know/Access
Consumers have the right under U.S. State Privacy Laws to request access to PI maintained by the Company. This right may be limited in some circumstances by law.
a) Categories
California residents have a right to submit a request for any of the following for the period that is 12-months prior to the request date:
The categories of PI we have collected about you.
The categories of sources from which we collected your PI.
The Business Purposes or Commercial Purposes for our collecting or Selling your PI.
The categories of third parties to whom we have shared your PI.
A list of the categories of your PI disclosed for a Business Purpose and, for each, the categories of recipients, or that no disclosure occurred.
A list of the categories of your PI sold and, for each, the categories of recipients, or that no sale occurred.
Residents of Delaware and Oregon can request additional information regarding certain third party disclosures of your PI (e.g., excluding disclosures to our service providers and processors).
Consumers of other states subject to U.S. State Privacy Laws have the right to confirm if we are processing your PI, which we will treat as a Categories request.
--- section of rule 2
3. How We Share Your Personal Information
We disclose Personal Information that we collect about you in the context of the Services to third parties in the following circumstances:
We may share Personal Information about you with our affiliates and subsidiaries.
We may share Personal Information about you with our third party service providers who perform services on our behalf, such as website hosting, payment processing, data analysis, information technology and related infrastructure provision, customer service, email delivery, online advertising, auditing, and other services. We do not sell your Personal Information and only share it with third party service providers to operate our Services. We may share your Personal Information with our service providers that provide user support and perform other business operations on our behalf, under our instructions and in compliance with appropriate technical and organizational security measures to protect your data. For example, we may partner with other companies to provide you support services, authentication services, perform analytics, maintain the accuracy of our databases.
To a potential or actual acquirer, successor, or assignee as part of any reorganization, merger, sale, joint venture, assignment, transfer or other disposition of all or any portion of our business, assets or stock (including in bankruptcy or similar proceedings). We will use reasonable efforts to direct the new entity to process your information in a way that does not materially differ from that set forth in this Privacy Policy.
If required to do so by law or in the good faith belief that such action is appropriate: (a) under applicable law, including laws outside your country of residence; (b) to comply with legal process; (c) to respond to requests from public and government authorities, including public and government authorities outside your country of residence; (d) to enforce our terms and conditions; (e) to protect our operations or those of any of our affiliates; (f) to protect our rights, privacy, safety or property, and/or that of our affiliates, you or others; and (g) to allow us to pursue available remedies or limit the damages that we may sustain.
We may sell or share information, including personal information that may be in anonymized, aggregated, or de-identified form, to third parties, who may share that information with entities including analytics companies, investment advisors, asset managers, or others.
We may use and disclose aggregate information that does not identify or otherwise relate to an individual for any purpose.
=== END ITEM p0007

=== ITEM p0008
rule 1: {"polarity": "ALLOW", "actor": "", "action": "Duration of Retention (operation: storage)", "data": "Name", "recipient": "", "source": "", "purpose": "To provide our services; to provide advertising for our Apps that support advertising; to comply with legal requests", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "", "action": "retained (operation: storage)", "data": "last name", "recipient": "", "source": "", "purpose": "To conduct privacy scans that you authorize; to update you on those scans", "condition": "", "condition_predicate": "true"}
--- section of rule 1 and rule 2
Category
Examples
General Business Purpose
Duration of Retention
Registration
Information
Email
Name
Phone Number
Password
Mobile Carrier Identifier
IP address for Registration
To provide our services, to provide advertising for our Apps that support advertising, and to comply with legal requests
Indefinitely
Identifiers
Advertising and vendor identifiers
iOS identifiers
Google ID
International mobile equipment identity (IMEI)
Device identifiers
To provide our services, to provide advertising for our Apps that support advertising, and to comply with legal requests
Indefinitely
Location information
Geo location of your device if you have given the app permission to collect your location information
To provide our services, to provide advertising for our Apps that support advertising, and to comply with legal requests
Indefinitely
Network information
IP address for network activity
MCC and MNC information
Local Wi-Fi Identifier
To provide our services and to provide advertising for our TextFree Apps, and to comply with legal requests
2 years account activity
Local Wi-Fi (90 days)
Survey information
Survey answers
Information provided as part of the Survey
To learn more about our customers and contact them, and to improve our Apps and services
Indefinitely, but not maintained in a manner that allows for easily searchable and identifiable personal data
Message Content
Text messages you send and receive
Voicemails
To provide our services and to comply with legal requests and, with your consent, for advertising purposes
Indefinitely for active account and 6 months for inactive accounts, with automated implementation of this process to be completed in Q1 of 2024
Account Attributes
Audience segmentation
Promotional offers to certain audiences
To provide advertising and promotional placements
Indefinitely for active account and 6 months for inactive accounts, with automated implementation of this process to be completed in Q2 of 2024
App Usage Information
App features used and pages viewed (although not identified to an individual)
Purchasing activity, such as if a subscription was purchased, but without any personal financial information retained
App usage information is retained to improve our services
2 years for App feature usage and 45 days for purchasing activity data
Call Detail Records
The time, duration and phone numbers of text messages and calls
To provide our Services and for legal compliance
2 years
Contacts
The contacts associated with your account
To provide our Services
As long as the account is open
Privacy Scan Data
First name, last name, age, city, state
To conduct privacy scans that you authorize and to update you on those scans
Not retained
We disclose your personal information to Back End Providers to enable communications transmissions for our Apps. We disclose your personal information to Services Providers to provide customer support, to analyze the usage of our Apps and the Site, to initiate App alerts, and to provide additional services you request. And we disclose your personal information to Advertising Companies to serve ads to our TextFree Apps.
We will not collect additional categories of personal information from you or use it differently than as described unless we provide you with advance notice and obtain your consent.
What about personal information from users under the age of 16?
Where users of our TextFree Apps have indicated that they are under the age of 16, we don’t sell their personal information and their account is terminated.
What are other uses of personal information?
As noted above, we use personal information to provide our services. In addition, we may use or disclose the personal information we collect for one or more of the following business purposes:
To fulfill or meet the reason for which the information is provided.
=== END ITEM p0008

=== ITEM p0009
rule 1: {"polarity": "ALLOW", "actor": "We", "action": "use (operation: use)", "data": "each category of personal information", "recipient": "", "source": "", "purpose": "to protect our company, our customers, and our business partners", "condition": "as necessary", "condition_predicate": "[untranslated: as necessary]"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "use (operation: use)", "data": "personal information", "recipient": "", "source": "from children under 13 years of age", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1
We use your contact information, and, if you give us access, information from your device’s contacts/phonebook, to enable the messaging functionality of the Services, as well as to match friends and to suggest connections to other users of the Services who you already know, or who you have a connection with outside of the Services.
We use information to respond to your requests or questions.
We use personal information to provide you with customer support anytime you reach out to us with questions about our Privacy Policy or Terms of Service, or issues arising from your account. We may also use personal information to send customers technical alerts, updates, security notifications, and administrative communications.
We use information to improve our products and services.
For example, we may use the information you provide about our products, as well as Internet and Network Activity, Location, and Inferences to make our website, services, and products better and more responsive to your interests.
We use information to administer our site and services and for internal operations.
We use all categories of personal information for our internal operations, such as troubleshooting, insurance claims, data analysis, and testing.
We use information for security purposes.
We may use each category of personal information as necessary to protect our company, our customers, and our business partners. We also may use this personal information to protect our websites or our services, as well as to detect and investigate activities that may be illegal or prohibited (such as cyber attacks or fraudulent activities).
We use information to verify requests made pursuant to this Privacy Policy.
We will use certain pieces of personal information to verify your identity if you make requests pursuant to this Privacy Policy. The verification steps and the pieces of personal information that we request may vary depending on the sensitivity and nature of your request.
We use information as other disclosed or permitted by law, or as we may notify you.
We collect personal information about you from various sources
We collect personal information about you from various sources, directly and indirectly. We collect these categories of personal information from the following categories of sources:
We collect personal information directly from you.
We collect Contact Information if you sign up for our Services or contact us. We also collect any personal information you provide if you make a request, fill out your user profile or other settings, or complete a survey.
We receive personal information from other users and other social media platforms.
We may receive Contact Information about you from other users of the Services who consent to give us access to their device’s contacts/phonebook. We may also receive information from other social media platforms, such as the username, display name and avatar image you use on such other social media platform, if you give your consent to the other social media platform to share that information with us.
We collect personal information from your devices.
We may use tracking tools like browser cookies and web beacons to automatically collect information about you (including Internet and Network Activity, and Location). We may collect this information when you interact with our Site, our ads, and our emails that we or our vendors send to you. We may have third parties collect personal information on our behalf in this way, too.
We get personal information from vendors we hire to work on our behalf.
Vendors that host or maintain our websites and send promotional emails for us may give us Contact Information and Internet and Network Activity Information. Our marketing agencies, advertising technology vendors, and analytics providers may provide us with Contact Information, Internet and Network Activity Information, and Location Information.
--- section of rule 2
You may exercise the above rights by emailing us at
[email protected]
.
Our Site and Services are not intended for children under 13
We do not knowingly collect information from children under 13. We do not knowingly collect, maintain, or use personal information from children under 13 years of age, and no part of the Service is directed to children under the age of 13. If you learn that your child has provided us with personal information without your consent, you may alert us at
[email protected]
.
International data transfers
Iconic Hearts is headquartered in the United States and may have service providers in other countries. Your personal information may be transferred to the United States or other locations outside of your state, province, country, or other governmental jurisdiction where privacy laws may not be as comprehensive as those in your jurisdiction.
We may link to third party sites or services we do not control
If you click on a link to a third party site, you will be taken to a website we do not control. This Policy does not apply to the privacy practices of that website, which may collect information from you. Read the privacy policy of other websites carefully. We are not responsible for these third party websites or their policies.
Security
While we take reasonable steps to protect your personal identifying information, nothing on the internet is 100% secure. For these reasons, we cannot guarantee that all of your personal identifying information will never be disclosed in ways you do not expect or which are not described in this Privacy Policy.
Contact us
If you have any questions about this Privacy Policy, please contact us by sending an email or letter to:
Iconic Hearts Holdings, Inc.
1639 11th Street, #226
Santa Monica, CA 90404
Email:
[email protected]
We may update this Policy
From time to time we may change our privacy policies. We will notify you of any material changes to our Policy as required by law. We will also post an updated copy on our website. Please check our site periodically for updates. Your continued use of our website means that you consent to the collection, use and disclosure of your personal information as set out in the updated Policy.
=== END ITEM p0009

=== ITEM p0010
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "collect (operation: collection)", "data": "personal information", "recipient": "", "source": "", "purpose": "", "condition": "on the Websites (collectively, the \"Sites\") listed here:\nflyfrontier.com\nm.flyfrontier.com\nfacebook.com/flyfrontier\ninstagram.com/flyfrontier/\nlinkedin.com/company/frontier-airlines\npinterest.com/frontierairlines\ntiktok.com/@flyfrontier?\ntwitter.com/flyfrontier\nyoutube.com/channel/UCmvnSoERKhYBDemzliynZ_w", "condition_predicate": "(service = flyfrontier.com OR service = m.flyfrontier.com OR service = facebook.com/flyfrontier OR service = instagram.com/flyfrontier/ OR service = linkedin.com/company/frontier-airlines OR service = pinterest.com/frontierairlines OR service = tiktok.com/@flyfrontier? OR service = twitter.com/flyfrontier OR service = youtube.com/channel/UCmvnSoERKhYBDemzliynZ_w)"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "disclosure (operation: collection)", "data": "more information than is reasonably necessary to complete that specific activity and/or Transaction", "recipient": "", "source": "", "purpose": "", "condition": "your participation in any specific activity on our Website", "condition_predicate": "event.participate_activity_on_website"}
--- section of rule 1
Information That We Collect
This Privacy Notice applies to personal information we collect on the Websites (collectively, the "Sites") listed here:
flyfrontier.com
m.flyfrontier.com
facebook.com/flyfrontier
instagram.com/flyfrontier/
linkedin.com/company/frontier-airlines
pinterest.com/frontierairlines
tiktok.com/@flyfrontier?
twitter.com/flyfrontier
youtube.com/channel/UCmvnSoERKhYBDemzliynZ_w
We collect information that identifies, relates to, describes, references, is capable of being associated with, or could reasonably be linked, directly or indirectly, with a particular consumer or device (“Personal Information”). The chart below shows the following categories of Personal Information about consumers that Frontier Airlines has collected and processed within the last 12 months:
​
Category
Examples
Business or Commercial Purpose
Identification Information
Identification information includes a consumer’s first and last name, home or postal address, Internet Protocol Address (or IP address), email address, passport number, telephone number, and known traveler number and redress number.
Identification information is used to confirm the identity of passengers flying with Frontier Airlines, to provide passengers with their flight information, to assist with any lost baggage claims, and as required by federal, state, local, or international law.
Personal Information Categories Listed in Applicable Law
Personal information includes a consumer’s first and last name, telephone number, passport number, credit and debit card number, home or postal address, driver’s license or state identification number, and signature.
Personal information is used to confirm the identity of passengers flying with Frontier Airlines, to provide passengers with their flight information, and as required by federal, state, local, or international law.
Characteristics of Protected Classifications (under applicable law)
Protected classification characteristics includes date of birth, physical or mental disability, gender identity, veteran or military status.
To confirm identity of passengers, provide certain accommodations or benefits and as required by federal, state, local, or international law.
Commercial Information
Commercial information includes records of products or services purchased, obtained, or considered, or other purchasing or consuming histories or tendencies.
To facilitate future bookings and improve booking and other services for passengers.
Internet or other similar network activity
Internet and network activity information includes browsing history, search history or information on a consumer's interaction with a Website, application or advertisement, and Internet protocol addresses (a.k.a. IP Address).
To provide a better experience on our Network and improve services for our passengers.
Geolocation Data
Geolocation data includes physical location information, such as GPS data.
To provide a better experience on our Network and provide passengers with an expedited booking process.
Sensory Data
Sensory data includes audio information such as phone call recordings.
Telephone calls are recorded for training and other purposes to improve customer service performance.
Professional or Employment related information
Professional or employment related information includes past job history, performance evaluations, background checks, and other information required to be collected by federal, state, local, or international law.
To allow applications for positions at Frontier Airlines online.
Inferences drawn from other personal information
Inferences drawn from personal information includes profiles reflecting a person’s preferences, characteristics, behavior, and attitudes.
To provide a better Network experience and improve services.
Education Information
Education information includes a student’s name, address, government identification numbers, and education records (as defined in 20 U.S.C. Sec. 1232g; 34 C.F.R. Part 99).
--- section of rule 2
FRONTIER
Miles account number; and
Travel agency name, contact information, and IATA / ARC number.
In compliance with applicable laws, it is our policy to require only the Transaction Information necessary for the specific Transaction that you request; we do not condition your participation in any specific activity on our Website, on the disclosure of more information than is reasonably necessary to complete that specific activity and/or Transaction.
FRONTIER Miles & Discount Den (Loyalty and Financial Incentive Programs)
=== END ITEM p0010

=== ITEM p0011
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "transfer (operation: disclosure by transmission)", "data": "your information", "recipient": "a third-party provider of services", "source": "", "purpose": "", "condition": "Your local laws may permit you to request that we; if we need to keep processing your information for our legitimate interests or to comply with a legal obligation; before responding to your request; unless certain information may be exempt from such requests in some circumstances", "condition_predicate": "(law.permitted AND (basis.legitimate_interests OR basis.legal_obligation) AND [untranslated: before responding to your request] AND NOT [untranslated: certain information may be exempt from such requests in some circumstances])"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "transfer (operation: disclosure by transmission)", "data": "personal information", "recipient": "", "source": "", "purpose": "", "condition": "in way of violating this Policy or applicable laws", "condition_predicate": "(NOT policy.permits OR NOT law.permitted)"}
--- section of rule 1
9.Your Rights
Your local laws may permit you to request that we:
•provide access to and/or a copy of certain information we hold about you
•prevent the processing of your information for direct marketing purposes (including any direct marketing processing based on profiling)
•update information that is out of date or incorrect
•delete certain information which we are holding about you
•restrict the way that we process and disclose certain of your information
•transfer your information to a third-party provider of services
•revoke your consent for the processing of your information
We will consider all requests and provide our response within the time period stated by applicable laws. Please note, however, that certain information may be exempt from such requests in some circumstances, which may include if we need to keep processing your information for our legitimate interests or to comply with a legal obligation. We may request you provide us with the information necessary to confirm your identity before responding to your request.
1) How to request data access, correction and query
You can click the personal center to enter your personal information editing page so as to access and correct your nickname information.
You can click“More”or“…”through“My Projects”on the home page to access the audio and video information completed/unfinished by you, and can also copy or rename the projectthrough“…”.
You can access the account, setting and product information of the third party that is boundin "Settings".
For other personal information generated during your use of our products or services, if you would like to access or correct it, you can contact us by adopting the methods specified in the privacy policy. As long as we do not require excessive investment, we will reply to your request within 15 days.
2)How to request data deletion
You can click“More”or“…”through“My Projects”on the home page to access the audio and video information completed/unfinished by you, or conduct the deletion operation through“…”.
You can disable the “Personalised Recommendations” feature and request the deletion of your associated preference profile at any time in the platform’s settings. Upon disabling, we will stop using your interaction data for personalisation and delete your preference profile.
Cancel accountto delete or anonymize your personal information. If you have registered a relevant account, you can choose to cancel your account at any time. You can cancel your account in "Settings" - "Account and Security" - "Cancel Account". Before you cancel your account, we may need to verify your personal identity, security status, device information, etc. You know and understand that the act of canceling your account is irreversible. When you cancel your account, we will delete or anonymize your personal information, except as otherwise provided by laws and regulations.
In addition, under the following circumstances, you can put forward the request of deleting the personal information by sending a deletion request to the email address: support@vivavideo.tv:
a.Our handling of personal information violates the relevant laws and regulations.
b.We collect or use your personal information without your consent.
c.Our handling of personal information violates the agreement with you.
d.You no longer use our products or services, or you cancel your account.
e.We no longer provide you with products or services.
If we decide to respond to your deletion request, we will notify the entities that obtain your personal information from us, and ask them to timely conduct the deletion, unless otherwise specified by laws and regulations, or unless these entities are independently authorized by you.
After you delete the relevant information from our services, we may not immediately delete the corresponding information in the backup system, but we will delete it when the backup is updated.
--- section of rule 2
If your personal information is no longer necessary for the legal or business purposes for which it is processed, we will generally destroy or anonymize that information.
7.How We Share Your Information
We never sell any personal information to third parties, although it may be shared only when necessary to perform a legitimate business function.
We may share your necessary personal information data to third-party service providers to help us deliver and improve Services, marketing, push/deliver notification bar message, and to help you to share content to third-parties media website, and other legitimate business functions. We will confirm on what basis each third-party will use your personal information and we will ensure that there are adequate safeguards and processes in place to protect your personal data.
•Analyze the partners in the service category and the advertising category.To maintain / improve our products / services and provide you with better content, partner SDK s or other applications are embedded in the software and the relevant SDK acquire your unique device ID (AndroidID) to analyze your use of our services, demonstrating advertising, measuring the effectiveness of advertising and services.
•Third-party channel login and sharing partners.To enable you to log in with a third-party account and share information (such as video) on third-party platforms, the partner SDK s or other similar applications are embedded in the software, and the relevant SDK gets your unique device identity (AndroidID).
•Information push partners. In order to provide you with the information push function, the partner's SDK or other similar applications will be embedded in the software, and the relevant SDK retrieves your unique device ID (AndroidID) and a list of running applications.
We will disclose or transfer your Information, only if required to do so by law, or we have acquired consent from you, or in the good faith belief that any such action is necessary to: (a) comply with any legal requirements or comply with the legal process served on us or the Platforms; (b) protect and defend the rights or property of us
, and
(c) act under exigent circumstances to protect the personal safety of our users, or the general public.
We will not share, transfer or disclose your personal information in way of violating this Policy or applicable laws.In the event of a transfer of information that may result from a possible merger, division, acquisition, asset sale, or bankruptcy liquidation by us, we will require the successor to protect your personal information in accordance with laws, regulations
,
and standards not lower than those set forth in this Policy.
8.How We Protect Your Information
We are committed to ensuring that your personal information is secure. In order to prevent unauthorized access, disclosure or other similar risks, we have put in place reasonable physical, electronic and managerial procedures to safeguard and secure the information we collect from your using ofour Services onthe Platforms. We will use all reasonable efforts to safeguard your personal information.
We review our strategies and update as necessary to meet our business needs, changes in technology, and regulatory requirements. These measures include, but are not limited to, technical and organizational security policies and procedures, security controls and employee training.For example,when you send or receive data fromVivaVideo App, we make sure they are encrypted using Secure Sockets Layer ("SSL")or other algorithms.
If we become aware of any breach that affects the security of your personal information, we will provide you with notice as required by applicable laws. By using thePlatforms, you agree to accept notice electronically.
=== END ITEM p0011

=== ITEM p0012
rule 1: {"polarity": "ALLOW", "actor": "We", "action": "stored (operation: storage)", "data": "information", "recipient": "", "source": "", "purpose": "", "condition": "on our systems", "condition_predicate": "[untranslated: on our systems]"}
rule 2: {"polarity": "DENY", "actor": "MPC", "action": "store (operation: storage)", "data": "any of this information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1
Information may also be shared with federal, state, local, tribal, international, or foreign governments, or law enforcement agencies to support security activities such as intelligence, counterintelligence, antiterrorism, law enforcement, and threats to national and international security. However, information collected solely for the purpose of facilitating an MPC transaction is not authorized to be shared with third parties by the application’s owner for any other purpose (e.g., social media, marketing or advertising networks).
Application Security
DHS takes the security of all PII very seriously. We take precautions to maintain the security, confidentiality, and integrity of the information we collect through the MPC-enabled mobile application. Such measures include access controls designed to limit access to the information to the extent necessary to accomplish our mission. We also employ various security technologies to protect the information stored on our systems. We routinely test our security measures to ensure that they remain operational and effective.
The MPC-enabled application transmits your data using secure encryption protocols. Transmission of the information via secure electronic transmission reduces the potential for inadvertent exposure of the information to those without a need to know, such as an unintended or inappropriate disclosure. You have the option of either storing your profile information on your personal device for future travel or deleting the information after a single use.
How to Access or Correct your Information
If you would like to access or correct the information you have provided to this MPC-enabled mobile application, you may contact the DHS Traveler Redress Inquiry Program (TRIP), which is a single point of contact for individuals who wish to correct erroneous data stored in DHS databases. TRIP redress requests may be made online at
https://www.dhs.gov/dhs-trip
or by mail at:
--- section of rule 2
Mobile Passport Control (MPC) Mobile Application Privacy Policy | U.S. Customs and Border Protection
Mobile Passport Control (MPC) Mobile Application Privacy Policy
Thank you for downloading the Mobile Passport Control (MPC)-enabled mobile application, which has been authorized by the U.S. Department of Homeland Security (DHS), Customs and Border Protection (CBP). You may voluntarily elect to provide your personally identifiable information (PII) in order to streamline your entry into the United States.
In order to enter the United States, you are required to provide travel document data, flight information, photos of you and your traveling family members, and responses to CBP inspection-related questions prior to gaining entry into the United States. Your information will be cross-referenced with data maintained in CBP’s other enforcement databases.
This privacy policy explains how CBP collects, uses, and maintains your PII, once the CBP MPC mobile application submission is received. Using MPC to enter the United States is voluntary. It provides international travelers with an alternative approach to traditional methods of submitting the required entry information to CBP during the border inspection process. If you choose not to submit your information, you will be unable to use the MPC-enabled application or be inspected by a CBP Officer in an MPC-dedicated lane. You may instead proceed directly to CBP primary examination to initiate the border inspection process.
Information Collected
CBP collects travel document data, flight information, photos of the traveler and traveling family members, and traveler responses to CBP inspection-related questions from all persons seeking to enter the United States in order to confirm the traveler’s identity and citizenship, establish whether the traveler is admissible into the United States, and facilitate CBP’s enforcement of U.S. laws. MPC allows you as a traveler to voluntarily store you and your co-traveler’s PII (e.g., surname/last name, given name/first name, date of birth, gender/sex, nationality/citizenship, passport number, passport country issuing authority, and passport date of expiration) securely within your MPC profile on your own device for future travel. CBP does not have access to this stored information. This information may be deleted by you at any time.
In addition, MPC collects your device location data to determine your proximity to a Port of Entry. Based on your device location, the device will automatically select the closest Port of Entry for submission to CBP.MPC does not store or transmit any of this information to CBP. CBP only uses this information to determine the correct Port of Entry. Your specific location information is not collected or maintained by CBP.
Uses of Information
CBP uses your information to streamline your entry into the United States. In order to enter the United States, you are required to provide specified biographical and biometric information, which will be cross-referenced with data maintained in CBP’s law enforcement databases.
Information Sharing
CBP will share your information within DHS consistent with its legal authorities and within the terms described in following System of Records Notifications (SORNS): Border Crossing Information (BCI) SORN, and the TECS System SORN. Each SORN is accessible via the following website:
https://www.dhs.gov/system-records-notices-sorns
.
The following DHS components have regular access to border crossing information: U.S. Immigration and Customs Enforcement (ICE), U.S. Citizenship and Immigration Services (USCIS), Transportation Security Administration (TSA), the United States Coast Guard, and the DHS Information & Analysis Directorate (I&A).
=== END ITEM p0012

=== ITEM p0013
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "collect (operation: collection)", "data": "personal data", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "collect (operation: collection)", "data": "personal data", "recipient": "", "source": "", "purpose": "", "condition": "from anyone under 13", "condition_predicate": "user.age < 13"}
--- section of rule 1
12. Storage and international personal data transfers
Flo is based in the UK. The personal data we collect is transferred to and processed in the US, where it is subject to US law and to other countries (where it follows the laws of those countries). These transfers are usually cloud-based and occur when you use our Services. Please note, the laws in these countries may not offer the same protections as those in your country.
Transfers of personal data outside of the EEA and the UK
Personal data in the EEA and the UK is protected by the GDPR and the UK GDPR. When we transfer personal data outside of these areas, we apply appropriate safeguards to ensure your personal data is protected. For example, we use data transfer agreements that include the European Commission’s Standard Contractual Clauses and conduct transfer risk assessments.
For further information, please email us at
support@flo.health.
Data Privacy Framework (“DPF”) Participation
Flo Health, Inc., Flo’s U.S. subsidiary, (“
Flo U.S.
”) is self-certified and complies with the EU–US DPF, the UK Extension to the EU–US DPF and Swiss–US DPF (collectively, the “
DPFs
”). Flo U.S. has certified to the U.S. Department of Commerce that, on reliance of the DPFs, it adheres to the DPF Principles when processing personal data of individuals within the EU, UK and/or Switzerland. For onward transfers, Flo U.S. is responsible for processing personal data it receives under the DPFs, and then transfers to a third party acting on its behalf. Flo U.S. remains liable under the DPFs if those third parties process personal data in a way that is not in compliance with the DPFs, unless it can prove that we are not responsible for the cause of any damage.
If there is any conflict between the terms in this Privacy Policy and the DPF Principles, the DPF Principles will govern, please visit
https://www.dataprivacyframework.gov/
.
You can find Flo US’s certification on the DPF list
here
.
Complaints and dispute resolution:
Flo U.S. is committed to resolving complaints about its collection and use of your personal data. EU, UK and Swiss individuals with inquiries or complaints regarding the DPFs should first contact us by emailing us at
dpo@flo.health
or by mail using the address: Flo Health UK Limited, Fourth Floor, International House, 1 St Katharine’s Way, London, E1W 1UN, United Kingdom.
Arbitration
: You may also be able to invoke binding arbitration for unresolved complaints, but prior to initiating such arbitration, a resident of a European country (including the UK and Switzerland) participating in the DPFs must first (1) contact us and afford us the opportunity to resolve the issue; (2) seek assistance from JAMS; and (3) contact the US Department of Commerce (either directly or through a European data protection authority, the UK’s Information Commissioner’s Office or the Swiss Federal Data Protection) and afford the Department of Commerce time to attempt to resolve the issue. If such a resident invokes binding arbitration, each party shall be responsible for its own attorney’s fees. Please be advised that pursuant to the DPFs, the arbitrator(s) may only impose individual-specific, non-monetary, equitable relief necessary to remedy any violation of the DPF with respect to the resident. The arbitration option may not be invoked if the individual’s same claimed violation of the principles (1) has previously been subject to binding arbitration; (2) was the subject of a final judgment entered in a court action to which the individual was a party; or (3) was previously settled by the parties.
Flo U.S. is subject to the investigatory and enforcement powers of the US Federal Trade Commission concerning personal data transferred under the DPFs, the UK’s Information Commissioner’s Office, the relevant EU Data Protection Authority, and the Swiss Federal Data Protection and Information Commissioner for resolving disputes with Swiss individuals.
Flo U.S.
--- section of rule 2
10. Children’s privacy
General age limitation:
our Services are not for children, and we do not knowingly collect personal data from anyone under 13. If you know of someone under 13 using the Services, please email us at
support@flo.health.
Age limitation for residents of the European Economic Area (EEA), United Kingdom (UK), Canada and India:
For legal reasons, residents of the EEA, the UK, Canada or India must be at least 16. If you know of someone under 16 using the Services, please email us at
support@flo.health.
Some features of the App are only available to members who are 18 or older.
=== END ITEM p0013

=== ITEM p0014
rule 1: {"polarity": "ALLOW", "actor": "our", "action": "collected automatically (operation: collection)", "data": "Certain information on our Site", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "collect (operation: collection)", "data": "Personal Data", "recipient": "", "source": "", "purpose": "", "condition": "from children under 13", "condition_predicate": "user.age < 13"}
--- section of rule 1
3. Personal Data Collected.
3.1 Data Controller
Top Games, Inc. is the data controller of your personal information. Top Games, Inc. can be reached at
legal@topgamesinc.com
or at Top Games US, Inc, 1603 Capitol Ave., Ste. 310 A436, Cheyenne, WY 82001.
3.2. Personal Data You Provide To Us On Our Site.
a) Types of Personal Data. We and our service providers collect the Personal Data set forth below in order to provide the Site to you, or because we are legally required to do so. If you do not provide the Personal Data we request, we may not be able to provide you with the Site.
The Personal Data we and our service providers collect includes but is not limited to:
Email address;
Payment information;
Phone number;
Communications you send to us.
b) When Personal Data is Collected.
You may be required to provide us with certain information that may constitute Personal Data in the following ways:
Contact Information.
In various areas of the Site, we provide you the opportunity to submit a form with basic contact information, such as your email and payment information. With your permission, Top Games uses such information to inform you of new products, technical information and services, and upcoming events that may be of interest. If you no longer wish to receive these emails, the opt-out process is described in Section 7.2 of this Privacy Policy.
In addition, if you choose, you may participate in a Top Games e-mail list server by subscribing within the Site or by contacting Top Games staff directly. You may unsubscribe from these e-mail list servers by following the unsubscribe instructions found within the list email.
Member Login Information.
We process your username and password to enable you to securely log into the Site, and we process information regarding your role with Top Games to appropriately control access to restricted content. We process this Personal Data only as necessary to provide you services on the Site under our
Terms of Use
and to further our legitimate interests in protecting the Site and content.
Payment Information.
When you purchase services or products from us, third-party service providers acting on our behalf process payment information, including payment card details and billing addresses, to help us fulfill your orders. Any Personal Data collected by such third party will be subject to the third party’s privacy policy, rather than this Privacy Policy.
Information Collected through Various Forms.
We and our service providers may collect Personal Data in a variety of ways, including: (i) through use of the Site, e.g., when you sign up for a gaming service, forum community, or make a purchase; or (ii) from other sources, such as public databases, joint marketing partners, social media platforms (including from people with whom you are friends or otherwise connected) and from other third parties.
Personal Data You Disclose Relating to Others.
If you disclose any Personal Data relating to other people to us or to our service providers in connection with the Site, you represent that you have the authority to do so and to permit us to use the information in accordance with this Privacy Policy.
3.3. Personal Data You Provide To Third Parties On Our Site.
Please note that we use certain third party service providers on our Site to enhance your experience or deliver certain services. These providers may collect Personal Data about you in performing their services and/or functions on our Site.
3.4. Information Collected Automatically
Certain information on our Site is collected automatically by means of various software tools. We have a legitimate interest in using such information to assist in log-in, systems administration purposes, information security and abuse prevention, to track user trends, and to analyze the effectiveness of our Site. Alone or in combination with other information, such automatically collected information may constitute Personal Data.
--- section of rule 2
10. Children's Privacy.
10.1. Children Under 13.
Children under the age of 13 should not use our websites or games at any time. In the event that we confirm that we have inadvertently gathered personal information from children under the age of 13, we will take reasonable measures to promptly remove such information from our records. We do not knowingly collect or store any Personal Data from children under 13. If parents believe that we have unintentionally collected their children’s’ Personal Data, they may request the deletion of the information by contacting us at:
Top Games, Inc. Attn: Legal - Privacy 585 Glenwood Avenue, Suite 3, Menlo Park, CA 94025 USA
They may also e-mail us at legal@topgamesinc.com.
10.2. Note to Parents.
We recognize a special obligation to protect Personal Data about young children. We urge parents to instruct their children to never give out their real names, addresses, or phone numbers, without permission, when on-line. Teenagers under the age of 17 and over the age of 12 should encourage their parents to review this Privacy Policy and to contact us if they would like to evoke our opt-out policy or to raise any concerns.
=== END ITEM p0014

=== ITEM p0015
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "share (operation: disclosure)", "data": "your personal information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "share (operation: disclosure)", "data": "personal information about you", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1 and rule 2
FACTS
WHAT DOES PROPEL DO WITH YOUR PERSONAL INFORMATION?
Why?
Financial companies choose how they share your personal information. Federal law gives consumers the right to limit some but not all sharing. Federal law also requires us to tell you how we collect, share, and protect your personal information. Please read this notice carefully to understand what we do.
What?
The types of personal information we collect and share depend on the product or service you have with us. This information can include:
Your name, Electronic Benefit Transfer (“EBT”) card number(s).
Your Social Security number and date of birth.
Your physical address, zip code and, if you provide us access to it through your device, your GPS location information.
Your EBT account user ID and password.
Your email address and phone number.
Your EBT balance and EBT transaction data.
Account balances, transactions, and transaction history.
Device information, including your IP address, MAC address, and device ID.
Other information that you may have provided to the EBT processor portal(s) that you have linked with our Services.
Our Services are designed to function without saving sensitive personal information, such as your EBT card number, personal identification number (“PIN”), or full Social Security Number (“SSN”) on our servers.
How?
All financial companies need to share customers’ personal information to run their everyday business. In the section below, we list the reasons financial companies can share their customers’ personal information; the reason Propel chooses to share; and whether you can limit this sharing.
Reasons we can share your personal information
Does Propel share?
Can you limit this sharing?
For our everyday business purposes
–
such as to process your transactions, maintain your account(s), respond to court orders and legal investigations
Yes
No
For our marketing purposes
–
to offer our products and services to you
Yes
No
For joint marketing with other financial companies
No
We don’t share
For our affiliates’ everyday business purposes
–
information about your transactions and experiences
No
We don’t share
For our affiliates’ everyday business purposes
–
information about your creditworthiness
No
We don’t share
For our affiliates to market to you
No
We don’t share
For nonaffiliates to market to you
No
We don’t share
To limit our sharing
While we do not presently share personal information about you that you have the ability to limit, this Privacy Policy may be amended from time to time and our sharing practices may change. If we begin to share personal information about you in ways that you may limit, we will provide you with information on how to exercise your limitation rights.
Questions?
Email us at help@propel.app
Who we are
Who is providing this notice?
Propel, Inc.
What we do
How does Propel protect my personal information?
To protect your personal information from unauthorized access and use, we use reasonable security measures that comply with industry standards. These measures include computer safeguards and secured files and buildings.
How does Propel collect my personal information?
We collect your personal information, for example, when you:
Open a Propel account, or otherwise provide information to open an account with us
Give us your contact information
When you use the Propel Services
We also collect your personal information from others, such as EBT processor portals that you have linked to your account with us.
Why can’t I limit all sharing?
Federal law gives you the right to limit only:
affiliates from using your information to market to you
sharing for nonaffiliates to market to you
for joint marketing with other financial companies
State laws and individual companies may give you additional rights to limit sharing. See below for more on your rights under state law.
What happens when I limit sharing for an account I hold jointly with someone else?
Your choices will apply to everyone on your account.
=== END ITEM p0015

=== ITEM p0016
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "collect (operation: collection)", "data": "your personal information", "recipient": "", "source": "", "purpose": "to comply with laws", "condition": "In certain cases", "condition_predicate": "[untranslated: In certain cases]"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "collect (operation: collection)", "data": "personal information", "recipient": "", "source": "from children under the age of 13", "purpose": "", "condition": "unless the consent of the child's parent or guardian", "condition_predicate": "NOT user.parental_consent"}
--- section of rule 1
Amazon.com Privacy Notice
Last updated: June 30, 2026.
View the
prior version
of this Privacy Notice.
We know that you care how information about you is used and shared, and we appreciate your trust that we will do so carefully and sensibly. This Privacy Notice describes how Amazon.com and its affiliates (collectively "Amazon") collect and process your personal information through Amazon products, services, stores, website and physical locations, devices and applications that reference this Privacy Notice (together "Amazon Services").
By using Amazon Services, you are consenting to the practices described in this Privacy Notice.
Please read our
Additional State-Specific Privacy Disclosures
and
Consumer Health Data Privacy Disclosure
for additional information about the processing of your personal data and your rights under applicable U.S. state data privacy laws.
What Personal Information About Customers Does Amazon Collect?
We collect your personal information in order to provide and continually improve our products and services.
Here are the types of personal information we collect:
Information You Give Us:
We receive and store any information you provide in relation to Amazon Services. You can choose not to provide certain information, but then you might not be able to take advantage of many of our Amazon Services.
Automatic Information:
We automatically collect and store certain types of information about your use of Amazon Services, including information about your interaction with products, content, and services available through Amazon Services. Like many websites, we use "cookies" and other unique identifiers, and we obtain certain types of information when your web browser or device accesses Amazon Services and other content served by or on behalf of Amazon on other websites. Our physical stores may use cameras, computer vision, sensors, and other technology to gather information about your activity in the store, such as the products and services you interact with.
Information from Other Sources:
We might receive information about you from other sources. For example, our carriers may provide us with updated delivery and address information, which we use to keep our records current and make delivery of your future purchases easier.
See
examples of information we collect or receive
.
For What Purposes Does Amazon Use Your Personal Information?
We use your personal information to operate, provide, develop, and improve the products and services that we offer our customers. These purposes include:
Purchase and delivery of products and services.
We use your personal information to take and handle orders, deliver products and services, process payments, and communicate with you about orders, products and services, and promotional offers.
Provide, troubleshoot, and improve Amazon Services.
We use your personal information to provide functionality, analyze performance, fix errors, and improve the usability and effectiveness of the Amazon Services. In so doing, we use machine learning and artificial intelligence to support and enhance the customer experience across our products and services. This includes using data to develop or deploy our generative AI models and services. See our
Generative AI Development Disclosure
for more information.
Recommendations and personalization.
We use your personal information to recommend features, products, and services that might be of interest to you, identify your preferences, and personalize your experience with Amazon Services.
Provide voice, image and camera services.
When you use our voice, image and camera services, we use your voice input, images, videos, and other personal information to respond to your requests, provide the requested service to you, and improve our services. You can read more about
Alexa, Echo Devices, and Your Privacy
.
Comply with legal obligations.
In certain cases, we collect and use your personal information to comply with laws.
--- section of rule 2
When you update information, we usually keep a copy of the prior version for our records.
If you do not want to receive email or other communications from us, please adjust your
Customer Communication Preferences
. If you don't want to receive in-app notifications from us, please adjust your notification settings in the app or device.
You may adjust your personalized advertising preferences by visiting
Your Ads Privacy Choices
.
The Help feature on most browsers and devices will tell you how to prevent your browser or device from accepting new cookies or other identifiers, how to have the browser notify you when you receive a new cookie, or how to block cookies altogether. Because cookies and identifiers allow you to take advantage of some essential features of Amazon Services, we recommend that you leave them turned on. For instance, if you block or otherwise reject our cookies, you will not be able to add items to your Shopping Cart, proceed to Checkout, or use any Services that require you to Sign in. For more information about cookies and other identifiers, see our
Cookies Notice
.
If you want to browse our websites without linking the browsing history to your account, you may do so by
signing out of your account
and blocking cookies on your browser.
You can manage the recommendations you receive in our store at
Improve Your Recommendations
, and you can remove recommendations you don’t want to see by unchecking the “Use this item for recommendations” toggle on the right side of the page for each item. You can edit
Your Browsing History
, as well.
You will also be able to opt out of certain other types of data usage by updating your settings on the applicable Amazon website (for example,
Manage Your Content and Devices
), device, or application. Learn more about certain devices at our
Privacy Settings FAQ page
. Most non-Amazon devices also provide users with the ability to change device permissions (for example, disable/access location services, contacts). For most devices, these controls are located in the device's settings menu. If you have questions about how to change your device permissions on devices manufactured by third parties, we recommend you contact your mobile service carrier or your device manufacturer.
If you are a seller, you can add or update certain information in
Seller Central
, update your account information by accessing your
Seller Account Information
, and adjust your email or other communications you receive from us by updating your
Notification Preferences
.
If you are an author, you can add or update the information you have provided in the
Author Portal
and
Author Central
by accessing your accounts in the Author Portal and Author Central, respectively.
In addition, to the extent required by applicable law, you may have the right to request access to or delete your personal information. If you wish to do any of these things, you may go to
Data Privacy Queries
. Depending on your data choices, certain services may be limited or unavailable.
Are Children Allowed to Use Amazon Services?
Amazon does not sell products for purchase by children. We sell children's products for purchase by adults. If you are under 18, you may use Amazon Services only with the involvement of a parent or guardian. We do not knowingly collect personal information from children under the age of 13 without the consent of the child's parent or guardian. For more information, please see our
Children's Privacy Disclosure
.
EU-US Data Privacy Framework, UK Extension, and Swiss-US Data Privacy Framework
Amazon.com, Inc. participates in the EU-US Data Privacy Framework, the UK Extension to the EU-US Data Privacy Framework, and the Swiss-US Data Privacy Framework. Learn more about the
EU-US Data Privacy Framework, UK Extension, and Swiss-US Data Privacy Framework
.
=== END ITEM p0016

=== ITEM p0017
rule 1: {"polarity": "ALLOW", "actor": "nous", "action": "avons conservées (operation: storage)", "data": "données à caractère personnel", "recipient": "", "source": "", "purpose": "", "condition": "Pour les résidents du Colorado, du Connecticut, du Delaware, de l’Indiana, de l’Iowa, du Kentucky, du Maryland, du Minnesota, du Montana, du Nebraska, du New Hampshire, du New Jersey, de l’Oregon, du Rhode Island, du Tennessee, du Texas, de l’Utah et de la Virginie; conformément à la législation de l'État concerné", "condition_predicate": "((user.jurisdiction = Colorado OR user.jurisdiction = Connecticut OR user.jurisdiction = Delaware OR user.jurisdiction = Indiana OR user.jurisdiction = Iowa OR user.jurisdiction = Kentucky OR user.jurisdiction = Maryland OR user.jurisdiction = Minnesota OR user.jurisdiction = Montana OR user.jurisdiction = Nebraska OR user.jurisdiction = New Hampshire OR user.jurisdiction = New Jersey OR user.jurisdiction = Oregon OR user.jurisdiction = Rhode Island OR user.jurisdiction = Tennessee OR user.jurisdiction = Texas OR user.jurisdiction = Utah OR user.jurisdiction = Virginia) AND law.permitted)"}
rule 2: {"polarity": "DENY", "actor": "Nous", "action": "conserverons (operation: storage)", "data": "vos données à caractère personnel", "recipient": "", "source": "", "purpose": "", "condition": "plus longtemps que nécessaire pour atteindre les objectifs pour lesquels les informations ont été initialement recueillies, sauf si une période de conservation plus longue est requise ou autorisée par la loi, pour des raisons juridiques, fiscales ou réglementaires, ou à d’autres fins commerciales légitimes et légales", "condition_predicate": "([untranslated: plus longtemps que nécessaire pour atteindre les objectifs pour lesquels les informations ont été initialement recueillies] OR law.required OR law.permitted OR basis.legitimate_interests)"}
--- section of rule 1
Veuillez noter que si vous souhaitez refuser les ventes ou la publicité ciblée par le biais de certains suivis basés sur des témoins à des fins publicitaires, vous devrez en faire la demande séparément en cliquant sur le lien Vos choix en matière de confidentialité dans le pied de page du site que vous visitez pour définir vos préférences ou en diffusant un signal de préférence de refus reconnu par CG, comme un signal de contrôle global de la confidentialité, sur les navigateurs ou les extensions de navigateurs qui prennent en charge un tel signal. Vous pouvez également régler les paramètres de votre appareil ou navigateur pour limiter la façon dont vos données d’utilisation d’Internet et celles de votre appareil sont partagées avec des tiers. Veuillez vous reporter à la section « Collecte de renseignements », sous-section « Témoins utilisés sur les Services », pour obtenir des références supplémentaires aux outils permettant de régler vos préférences.
Loi Shine the Light de la Californie
Si vous résidez en Californie, vous avez le droit de nous demander une fois par an si nous avons communiqué des informations personnelles à des tiers à des fins de marketing direct. Pour faire une demande, veuillez nous envoyer un e-mail ou nous écrire à l'adresse indiquée dans la section « Coordonnées » ci-dessous. Veuillez préciser dans votre courrier que vous êtes un résident californien effectuant une demande au titre de la loi Shine the Light.
Pour les résidents du Colorado, du Connecticut, du Delaware, de l’Indiana, de l’Iowa, du Kentucky, du Maryland, du Minnesota, du Montana, du Nebraska, du New Hampshire, du New Jersey, de l’Oregon, du Rhode Island, du Tennessee, du Texas, de l’Utah et de la Virginie
Les résidents du Colorado, du Connecticut, du Delaware, de l’Indiana, de l'Iowa, du Kentucky, du Maryland, du Minnesota, du Montana, du Nebraska, du New Hampshire, du New Jersey, de l'Oregon, du Rhode Island, du Tennessee, du Texas, de l’Utah et de la Virginie peuvent présenter des demandes conformément à la législation de l'État concerné, y compris :
demandes d’accès et de confirmation :
sous réserve de certaines exceptions prévues par la loi, vous pouvez nous demander de confirmer si nous traitons vos données à caractère personnel et vous pouvez également demander l’accès à vos données à caractère personnel. Les résidents du Delaware, du Minnesota et de l’Oregon peuvent également demander une liste des tiers (tels que définis dans la loi applicable) auxquels nous avons divulgué des données à caractère personnel.
demandes d’effacement
: vous pouvez nous demander de supprimer les données à caractère personnel que nous détenons à votre sujet et que nous avons conservées, sous réserve de certaines exceptions.
demandes de correction
: vous pouvez nous demander de corriger les données à caractère personnel que nous conservons à votre sujet, sous réserve de certaines exceptions.
demande d’opposition à la vente
: vous pouvez refuser la « vente » de vos données à caractère personnel, conformément à la définition de ce terme prévue par la loi de l’état en vigueur.
demande d’opposition à la publicité ciblée
: Nous pouvons utiliser des données à caractère personnel obtenues à partir de ou en rapport avec vos activités sur des sites non affiliés pour vous envoyer des publicités plus pertinentes. Vous pouvez nous demander de cesser d’utiliser vos données à caractère personnel à des fins de publicité ciblée.
Les résidents du Colorado, du Connecticut, du Delaware, de l’Indiana, de l’Iowa, du Kentucky, du Maryland, du Minnesota, du Montana, du Nebraska, du New Hampshire, du New Jersey, de l’Oregon, du Rhode Island, du Tennessee, du Texas, de l’Utah et de la Virginie peuvent consulter notre formulaire web de Demandes de droits du consommateur ou soumettre une demande en utilisant les méthodes indiquées dans la section « Coordonnées » ci-dessous.
--- section of rule 2
TRANSFERTS TRANSFRONTALIERS DE DONNÉES À CARACTÈRE PERSONNEL
Les données à caractère personnel que nous recueillons auprès de vous peuvent être transférées vers, et stockées dans, une destination en dehors du pays dans lequel elles sont recueillies, y compris, en ce qui concerne les résidents de l’EEE et du Royaume-Uni, en dehors de l’EEE et du Royaume-Uni, dans des pays dont les lois ne prévoient pas une protection des données équivalente à celle de votre pays de résidence. Elles peuvent également être traitées par du personnel opérant en dehors de l’EEE et du Royaume-Uni qui travaille pour nous ou d’autres entités agissant en tant que sous-traitants des données traitant des données à caractère personnel pour notre compte. Cela comprend le personnel engagé, entre autres, dans l’exécution de votre demande ou commande et la fourniture de Services d’assistance. Si tel est le cas, CG prendra des mesures pour protéger vos données à caractère personnel, notamment en mettant en œuvre les Clauses contractuelles types de l’UE et du Royaume-Uni afin de fournir des garanties appropriées et appropriées pour les données à caractère personnel transférées vers des pays en dehors de l’EEE et du Royaume-Uni où un niveau adéquat de protection n’est pas déjà garanti. Vous pouvez en obtenir un exemplaire en contactant
privacy@chamberlain.com
.
Nous prendrons toutes les mesures raisonnablement nécessaires pour nous assurer que vos données à caractère personnel sont traitées en toute sécurité et sous réserve des garanties appropriées conformément au présent Avis de confidentialité et aux lois applicables.
CONSERVATION DES DONNÉES
Nous ne conserverons pas vos données à caractère personnel plus longtemps que nécessaire pour atteindre les objectifs pour lesquels les informations ont été initialement recueillies, sauf si une période de conservation plus longue est requise ou autorisée par la loi, pour des raisons juridiques, fiscales ou réglementaires, ou à d’autres fins commerciales légitimes et légales.
Les critères utilisés pour déterminer nos périodes de conservation comprennent :
la nécessité de remplir notre objectif commercial légitime ;
prescription par les lois applicables, énoncées dans le contrat et autres obligations légales ; et
obligation légale ou réglementaire ou enquête.
Lorsque nous n’avons pas de besoin professionnel légitime continu de traiter vos données à caractère personnel, nous les supprimerons ou les rendrons anonymes.
VOS OPTIONS ET L’ACCÈS À VOS DONNÉES PERSONNELLES
Pour « refuser » de recevoir de futurs messages marketing par e-mail de CG, vous pouvez cliquer sur le lien « se désabonner » au bas d’un message marketing par e- mail. Pour y accéder à vos informations stockées par CG, les examiner ou les mettre à jour, vous pouvez consulter la page Profil de compte sur les Sites et Applications, où vous pouvez afficher, mettre à jour ou modifier vos données à caractère personnel et mettre à jour votre profil de membre, votre mot de passe et les informations associées. Vous pouvez gérer vos préférences concernant notre utilisation des cookies via notre
Centre de préférences en matière de cookies
sur nos Sites et Applications. Pour les utilisateurs de l’application myQ, des options de contrôle des données peuvent également être disponibles dans le tableau de bord de confidentialité de l’application.
Si vous avez d’autres questions concernant l’accès à vos données à caractère personnel ou leur mise à jour, veuillez nous contacter via les coordonnées fournies dans la section « Coordonnées » ci-dessous.
VOS DROITS EN MATIÈRE DE VIE PRIVÉE
En vertu de la loi et de la réglementation en vigueur, vous pouvez exercer certains droits à tout moment, comme décrit ci-dessous.
=== END ITEM p0017

=== ITEM p0018
rule 1: {"polarity": "ALLOW", "actor": "", "action": "deleted (operation: erasure or destruction)", "data": "personal data", "recipient": "", "source": "", "purpose": "", "condition": "After an objection or cancellation declared by you; within 7 days; unless if we are authorised or obliged to continue storing it on the basis of a legal basis other than your consent (e.g. in the case of chargeable events on the basis of the AO or the HGB", "condition_predicate": "((request.object OR request.cancel) AND retention.days <= 7 AND NOT (law.permitted OR law.required OR basis.legal_obligation OR basis.contract OR basis.vital_interests OR basis.public_task OR basis.legitimate_interests))"}
rule 2: {"polarity": "DENY", "actor": "", "action": "deleted (operation: erasure or destruction)", "data": "data", "recipient": "", "source": "", "purpose": "", "condition": "if we are authorised or obliged to continue storing it on the basis of a legal ground other than your consent (e.g. in connection with the processing of customer enquiries or complaints and in order to be able to prove previous consent)", "condition_predicate": "(law.permitted OR law.required)"}
--- section of rule 1
(3) Purpose of data processing
The data will be used exclusively for the realisation of the respective event.
(4) Duration of storage
The data will be deleted as soon as it is no longer required to fulfil the purpose for which it was collected.
After an objection or cancellation declared by you [see below under (5)], your personal data will be deleted within 7 days. However, this data will not be deleted if we are authorised or obliged to continue storing it on the basis of a legal basis other than your consent (e.g. in the case of chargeable events on the basis of the AO or the HGB.
(5) Possibility of objection and removal
You have the option to withdraw your consent to the processing of personal data at any time [see XXI.(8) Right of withdrawal below].
You can also object to the processing of your personal data at any time if and insofar as this processing is carried out on the basis of Art. 6 para. 1 sentence 1 lit. f) GDPR [see XXI.(1) Right to object below].
You can send both the withdrawal and the objection, e.g. by clicking
here
. In such a case, however, the conversation cannot be continued.
Third Party Tools
A. Matomo
(1) Description and scope of processing
Our website uses the web analysis service Matomo, which uses the the cookies specified in “Cookies preferences” accessible via the footer of our website. Collection and analysis only occurs if you have authorised this by setting the cookie banner accordingly and thereby declaring your consent. You can revoke this consent at any time by changing the setting of the cookie banner under “Cookies preferences” in the footer of our website.
We store the information collected in this way in the Matomo cloud. We have concluded an order processing agreement for this purpose.
Our website uses Matomo with the “AnonymiseIP” extension. This ensures that IP addresses are processed in abbreviated form, i.e. anonymised, maintaining user anonymity during web analysis. The IP address transmitted by your browser via Matomo is not merged with other data
collected by us and is not transmitted to third parties.
The following information is stored in Matomo:
Anonymised IP address
Browser used (type, version)
Operating system used
Type of device used (desktop, mobile device, tablet)
Screen resolution
Duration of the visit
Visited entry and exit pages
Clicks on external or internal links
File downloads
Search engine used
Interaction with forms
The Matomo programme is an open source project. Information from the third-party provider on data protection can be found at
https://Matomo.org/privacy-policy/
and at
https://matomo.org/gdpr-analytics/
.
(2) Legal basis
The legal basis for the use of Matomo is your consent in accordance with Section 25 (1) TDDDG, Art. 6 (1) (a) GDPR, provided that you have given your consent via our cookie banner. You can revoke your consent at any time. Please make the appropriate settings via our cookie banner. You can access this via the “Cookies preferences” in the footer of our website.
(3) Purpose of data processing
The processing of users’ personal data in anonymised form allows us to analyse their surfing behaviour. By analysing this data, we can compile information about how individual components of our website are used. This helps us to continually improve our website and improve its user-friendliness.
(4) Duration of storage
The data is deleted as soon as it is no longer required for our recording purposes. In our case, this is the case after 365 days. Cookies are deleted after a maximum of 30 days.
(5) Objection and removal options
As a user, you also have full control over the use of Matomo. You can deactivate its use by changing the settings in the cookie banner on this website. You can access this cookie banner via “Cookies preferences” in the footer of our website.
B.
--- section of rule 2
(2) Legal basis for data processing
The legal basis for the processing of the data is, if and insofar as your consent has been obtained, Art. 6 para. 1 lit. a) GDPR.
The legal basis for the processing of the data transmitted to us during registration, before the apps are made available or commented on, is also Article 6(1)(c) and (f) GDPR. We have an interest in contacting you in the event of technical problems with the uploaded apps or their updates as well as illegal content in your comments. We need your email address to contact you if a third party objects to your comment as unlawful. We will then carry out a so-called notice-amend-take-down procedure and give your the opportunity to respond.
(3) Purpose of data processing
The processing of personal data serves the purpose of offering a functional app store with open source apps for the Nextcloud software. For security reasons, we cannot allow the anonymous uploading and distribution of apps.
(4) Duration of storage
The data will be deleted as soon as it is no longer required to fulfill the purpose for which it was collected. If you declare an objection or cancellation: [see below under (5)], your personal data will be deleted within 7 days.
However, this data will not be deleted if we are authorised or obliged to continue storing it on the basis of a legal ground other than your consent (e.g. in connection with the processing of customer enquiries or complaints and in order to be able to prove previous consent).
Once your data has been deleted, your comments and ratings will only be displayed as “Anonymous” and no longer with your user name.
(5) Possibility of objection and removal
You have the option to revoke your consent to the processing of personal data at any time [see below . (8) Right of revocation].
You can also object to the processing of your personal data at any time if and insofar as this processing is carried out on the basis of Art. 6 para. 1 sentence 1 lit. f) GDPR [see below XIX. (1) Right to object].
You can send both the cancellation and the objection, e.g. by clicking
here
. In such a case, however, the conversation cannot be continued.
For security reasons, we must also remove the apps you have uploaded when deleting your personal data.
Events – offline and online (e.g. webinars)
(1) Description and scope of data processing
From time to time we organise online or offline events for which you can register via our homepage. For this purpose, we collect data necessary for the organisation of the event:
Name,
Email address,
Time of participation in longer events that take place offline
We also ask you to provide additional voluntary information to make it easier for us to organise the event. Your telephone number will only be used to contact you if we have any questions about your registration; it will not be shared with third parties or used it for any other purpose.
We ask about your dietary preferences so that we have enough suitable catering available
. The capacity in which you are associated with Nextcloud helps us to assess the composition of the specific audience and plan our event agenda. Both pieces of information are stored separately from your personal data for statistical purposes only.
When organising such events, we also issue calls for speakers in order to give you the opportunity to be selected by us for a presentation at one of our events if you wish. To this end, we ask for information that will enable us to assess whether your presentation is suitable for our event.
(2) Legal basis for data processing
The legal basis for the processing of the data is, if and insofar as your consent has been given, Art. 6 para. 1 lit. a) GDPR.
The legal basis for this is
Art. 6 para. 1 lit. f GDPR
. Our legitimate interest lies in the smooth organisation of the event.
The legal basis for paid and free events is also Art. 6 para. 1 lit. b) GDPR, as participation is also based on a contract.
=== END ITEM p0018

=== ITEM p0019
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "store (operation: storage)", "data": "your information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "retain (operation: storage)", "data": "Personal Information", "recipient": "", "source": "", "purpose": "", "condition": "for longer than is necessary for our business or for legal requirements", "condition_predicate": "([untranslated: longer than is necessary for our business] OR law.required)"}
--- section of rule 1
Privacy Policy - ZeptoLab
Privacy Policy
LAST UPDATED: 27 AUGUST 2025
This document is available in the following languages: German, French, Spanish, Polish, Italian, Portuguese, Dutch, Turkish, Arabic, Russian, Korean, Simplified Chinese and Japanese. Only the English language version shall have legal force and effect. Any non-English translations are provided solely for convenience and shall not be relied upon for interpretation.
This Privacy Policy explains how ZeptoLab UK Limited ("
ZeptoLab
" or "
we
") collects, uses, shares and otherwise processes your personal information when you play any of our games including, without limitation, Bullet Echo, Cut the Rope, Overcrowded: Tycoon, Robotics!, Downhill Smash, Evo Pop (“
Games
”), or use our websites (“
Websites
”) and related services (collectively, “
Services
”).
This Privacy Policy explains your rights over your personal information, like your name and contact details. It tells you how we collect, store, use, and share your information. Depending on where you live, you might have different options for controlling how your information is handled, and this Privacy Policy will explain those choices.
Our Services contain links to other apps and websites that may also collect and use information about you in accordance with their own separate rules. Please read the notices and information on their apps or websites to find out more about how and why they do this.
We may update this Privacy Policy from time to time. If we make material changes, we will provide a prominent notice in the Games or on the Websites before the changes take effect. Where required by law, we will seek your consent for such changes. This Privacy Policy states its effective date at the top.
--- section of rule 2
8. HOW LONG IS YOUR PERSONAL INFORMATION STORED
It will depend on the purpose for which we originally collected it. We will not retain Personal Information for longer than is necessary for our business or for legal requirements. In some circumstances, you can ask us to delete your data: see Section 11 of this Privacy Policy for further information.
Once we no longer have a legal right to hold your personal data, we will delete it or, in some circumstances, we will anonymise your Personal Information (so that it can no longer be associated with you) for research or statistical purposes, in which case we may use this information indefinitely without further notice to you. If you do not use the Services for a period of 90 days, then we may delete your personal data.
=== END ITEM p0019

=== ITEM p0020
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "collect (operation: collection)", "data": "information", "recipient": "", "source": "", "purpose": "", "condition": "It applies to all interactions you make with our games", "condition_predicate": "service = games"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "collect (operation: collection)", "data": "information such as your name", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1
OVERVIEW
We've done our best to cut through the legal jargon and explain in simple terms what information we collect, what we use it for, and the few situations in which we may share it with others. Please read this privacy policy carefully. It applies to all interactions you make with our games.
--- section of rule 2
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
=== END ITEM p0020

=== ITEM p0021
rule 1: {"polarity": "ALLOW", "actor": "BeReal", "action": "access (operation: use)", "data": "your address book", "recipient": "", "source": "", "purpose": "to identify the friends in your Address Book who may already be on BeReal or to recommend you new friends", "condition": "You can decide to allow BeReal to access your address book", "condition_predicate": "consent.access_address_book"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "access (operation: use)", "data": "your Address Book", "recipient": "", "source": "", "purpose": "", "condition": "unless your permission", "condition_predicate": "NOT consent.access_address_book"}
--- section of rule 1 and rule 2
Mobile advertising IDs and device identifiers
We collect technical identifiers developed by mobile operating systems for advertising purposes which remain under your control and can be reset or erased at any time through your device settings:
Mobile advertising IDs (e.g., Apple IDFA if you use iOS or Google AAID if you use Android).
Device identifiers (e.g., IDFV for iOS devices and Android ID for Android devices).
Interaction Data
Friend (number of friends, friend invitations, the friends with whom you interact the most).
Inferred Information
We will analyse Account Creation Data and the Content Data to infer information about you:
Your time zone.
Your likely interests derived from the visual elements of your photos, used exclusively as internal targeting criteria.
Your likely gender, inferred via AI from your username, first name and biography, used exclusively as internal targeting criteria.
Usage Data
Actions performed on the App or our website, time of posting Content, how many times you retook a photo before posting, number of BeReal posts, Content viewed, Content interactions, the fact that you deleted Content, or that you blocked users, when you take a screenshot in our App, App crashes, pages visited and event logs.
Geolocation Data
When you use our App, we infer your country, city, region based on your IP address.
Address Book Data
You can decide to allow BeReal to access your address book to identify the friends in your Address Book who may already be on BeReal or to recommend you new friends. We do not access your Address Book without your permission. Bear in mind that even if you don’t agree to share your Address Book with us, we can still make personalized friends’ suggestions to you based on your contact details that we received from your friends who use our App (see below). You can revoke your permission to access your Address Book Data at any time through your device settings. Once access is revoked, we will no longer collect or update contact information from your address book, and previously uploaded contact data will be deleted within a reasonable time.
UX Interaction Recordings
For a randomized sample of users (0.001%), we record technical interactions with the App interface, such as touching and swiping. This is conducted through our analytic partner to help us visualize how users navigate the App and improve the overall user interface. This processing is not deployed in all geographic regions and may not apply depending on your location. This data is kept for a maximum of 90 days from the time of collection and is then automatically deleted.
1.3. Information about you provided by third parties
The table below details the categories of personal data that we receive about you from third parties, and the context in which we receive them.
Source
Description & Context of Collection
Other users of the App
We may receive information about you from other users of our App. For instance, if other users know you and choose to use contact importing, they may share your contact details, such as your phone number, with us, just as you may share theirs. Where friends of yours use contact importing, we may suggest you as a friend to them, and them as a friend to you, or they can find you via our search tool.
Integrations with Partners
When you decide to connect a partner application (for example Spotify) to use a specific integration on BeReal, we receive information that allows us to bring that feature to you. This will include all necessary device data, and other optional data that you may choose to share as part of the integration.
Our partners
We receive information about where you came from to download the App (for example, if you clicked on an ad on another social media).
Advertisers
When an advertiser runs a campaign with us, it may provide us with a hashed (pseudonymized) list of phone numbers of its own customers.
=== END ITEM p0021

=== ITEM p0022
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "store (operation: storage)", "data": "such information", "recipient": "", "source": "", "purpose": "for photo processing", "condition": "When you use some face recognition functions (including but not limited to theme templates)", "condition_predicate": "event.use_face_recognition_functions"}
rule 2: {"polarity": "DENY", "actor": "We", "action": "store (operation: storage)", "data": "facial feature information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
--- section of rule 1 and rule 2
2.Which permissions we might ask you to authorize
In order to provide you with more high-quality, efficient products and services and improve your service experience, we may ask you to authorize the corresponding terminal device permissions in the following additional services we provide to you.We collect the following permissions and corresponding information following the criterion of minimal data collection with your consent:
•Read and write external memory card:
for reading and writing files on external memory card for video editing or upload and download personal videos, photos, audios and subtitle data through the Cloud Disk Service Technology（when you use our cloud disk, you will be deemed to have agreed to abide by our
Cloud Disk Service Agreement
）；
•Camera permissions：
For taking photos and video shooting.
•Microphone permissions:
for video shooting and editing.
•Web access:
a variety of network services for accessing and downloading materials.
• Receive notification messages:
used to receive messages;
• Gets the current network status:
to alert users whether they are currently using the mobile network or determine whether a user's wifi network is available；
• TrueDepth API:
to get face data and track faces in our template functions.
• Face recognition:
For specific theme template editing and short video production services, VivaVideo collects the avatar photos you’ve uploaded or shot. To use some functions of the theme templates that need face matting, you can voluntarily permitVivaVideo to access the camera or photo album to obtain photos from your mobile device. Only after you confirm your permission, canVivaVideo access your camera and photo album. When you use some face recognition functions (including but not limited to theme templates), we automatically capture the positions and shapes of your five sense organs, analyze the facial feature information, store such information on our server for photo processing, and return the renderings to you. We will not store such processed photos, facial feature information, or renderings, or share them with any third party. Such information is processed only to run the face recognition function and provide you with better renderings.
You can check the status of the above permissions in the system settings of your terminal device, and you can turn on or off any or all above permissions at your own discretion at any time. Please note that when you open any permission,it means that you authorize us to collect and use the personal information corresponding to the permission to provide you with the above corresponding services. Once you turn off any permission,it means that you cancel or revoke the authorization of the permission, and we will no longer continue to collect and use the corresponding personal information based on this permission, nor will we be able to provide you with the services corresponding to this permission. However, your decision to turn off the permissions will not affect the previous collection and use of information based on your previous authorization.
3.How We Collect Your Information
We collect information in different ways.
We collect information directly from you.
We collect information directly from you when you use the customer services on the Platforms.
We collect information from you passively.
We use tracking tools like Google Analytics, browser cookies and web beacons(see below for details)for collecting information about your usage of ourPlatforms.
4.How We Use Your Personal Information
We may use the information you have provided pursuant to this Policy to provide our Services, or to communicate with you. Specifically, we may use your information for the following purposes:
•We use information to improve our Services.
We use your information to help us create, develop, operate, deliver, and improve our Services. For example, we might look at usage trends to make sure the Platforms is easy to use.
=== END ITEM p0022

=== ITEM p0023
rule 1: {"polarity": "ALLOW", "actor": "", "action": "provided with a copy of (operation: disclosure by transmission)", "data": "Personal Data", "recipient": "", "source": "", "purpose": "", "condition": "In certain circumstances; in a structured, machine-readable and commonly used format", "condition_predicate": "([untranslated: In certain circumstances] AND [untranslated: in a structured, machine-readable and commonly used format])"}
rule 2: {"polarity": "DENY", "actor": "Retrica, Inc.", "action": "transfer (operation: disclosure by transmission)", "data": "Personal Data", "recipient": "an organisation or a country", "source": "", "purpose": "", "condition": "unless there are adequate controls in place including the security of your data and other personal information", "condition_predicate": "NOT [untranslated: there are adequate controls in place including the security of your data and other personal information]"}
--- section of rule 1
10. Your Data Protection Rights Under General Data Protection Regulation (GDPR)
If you are a resident of the European Union (EU) and European Economic Area (EEA), you have certain data protection rights covered by GDPR.
We aim to take reasonable steps to allow you to correct, amend, delete, or limit the use of your Personal Data.
If you wish to be informed what Personal Data we hold about you and if you want it to be removed from our systems, please email us at contact@retrica.co.
In certain circumstances, you have the following data protection rights:
the right to access, update or to delete the information we have on you;
the right of rectification. You have the right to have your information rectified if that information is inaccurate or incomplete;
the right to object. You have the right to object to our processing of your Personal Data;
the right of restriction. You have the right to request that we restrict the processing of your personal information;
the right to data portability. You have the right to be provided with a copy of your Personal Data in a structured, machine-readable and commonly used format;
the right to withdraw consent. You also have the right to withdraw your consent at any time where we rely on your consent to process your personal information;
Please note that we may ask you to verify your identity before responding to such requests. Please also note that we may not be able to provide the Service without some necessary data.
You have the right to complain to a Data Protection Authority about our collection and use of your Personal Data.
--- section of rule 2
7. Transfer of Data
Your information, including Personal Data, may be transferred to — and maintained on — computers located outside of your state, province, country or other governmental jurisdiction where the data protection laws may differ from those of your jurisdiction.
If you are located outside the United States and choose to provide information to us, please note that we transfer the data, including Personal Data, to the United States and process it there.
If you are located inside the European Union, European Economic Area, or the United Kingdom and choose to provide information to us, please note that we transfer the data, including Personal Data, to locations outside the European Union, European Economic Area, and/or the United Kingdom and process it there.
Your consent to this Privacy Policy followed by your submission of such information represents your agreement to that transfer.
Retrica, Inc. will take all steps reasonably necessary to ensure that your data is treated securely and in accordance with this Privacy Policy and that no transfer of your Personal Data will take place to an organisation or a country unless there are adequate controls in place including the security of your data and other personal information.
Uploaded photos and other personal data processed through the Service may be stored and processed through cloud infrastructure and service providers used to operate the Service, subject to the safeguards described in this Privacy Policy.
=== END ITEM p0023

=== ITEM p0024
rule 1: {"polarity": "ALLOW", "actor": "our", "action": "processing (operation: processing)", "data": "data", "recipient": "", "source": "", "purpose": "", "condition": "The most recent version of this Notice will govern our processing of your data", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "process (operation: processing)", "data": "data", "recipient": "", "source": "children under thirteen 13 years old", "purpose": "", "condition": "from children under thirteen 13 years old", "condition_predicate": "user.age < 13"}
--- section of rule 1
UPDATES TO THIS PRIVACY NOTICE
This Privacy Notice might change from time to time.
The most recent version of this Notice will govern our processing of your data and can be found on the Philips Hue website. Our Privacy Notice archive will keep prior versions of this Privacy Notice for your reference.
--- section of rule 2
YES
YES, to affiliates, service providers, and other vendors mentioned in this Notice
A. Identifiers.
B. Personal information categories listed in the California Customer Records statute (Cal. Civ. Code § 1798.80(e)).
C. Protected classification characteristics under California or federal law.
D. Commercial information.
E. Biometric information.
F. Internet or other similar network activity.
G. Geolocation data.G. Geolocation data.
H. Sensory data.
I. Professional or employment-related information.
J. Non-public education information (per the Family Educational Rights and Privacy Act (20 U.S.C. Section 1232g, 34 C.F.R. Part 99)).
K. Inferences drawn from other personal information.
We disclose your data for a business purpose to the following categories of third parties:
Signify group companies.
Service providers.
Third parties to whom we disclose your personal data in connection with products or services we provide to you, and to accomplish our business purposes and objectives as outlined in the notice.
Data from children?
We do not intentionally collect information from children under the age of sixteen (16) years as we do not offer services to them. Parents who set up a profile holding information about children under the age of sixteen (16) years can only do so by granting parental consent which consent choices can be changed by the adults in the family. We do not direct services to children under the age of thirteen (13) years old. As a result, we do not knowingly process data or information from children under thirteen 13 years old.
Do not sell or share personal data?
We do not respond to “Do Not Sell” requests as we do not sell your personal data to third parties. In the twelve months before the effective date of this Privacy Notice, we have not sold any personal data of Customers, as per the definition of the CCPA/CPRA.
After receiving your opt-in consent, we sometimes disclose personal data collected via cookies for cross-contextual behavioral advertising purposes, which may qualify as sharing your personal data under the CCPA/CPRA. To opt out, you can adjust your cookie preferences on our website to block our advertising cookies, or you can change your device settings to block cookies or install a third-party plugin to control how cookies interact with your device. For more information on how we use cookies and other tracking technologies, read our
Cookie Notice
.
Your rights?
"Right to Know":
You may have the right to request that we disclose to you what personal data of yours we collect, use, and/or disclose.
"Right to Delete":
You may have the right to request the deletion of your personal data collected or maintained by us. Depending on your Choices, certain offerings may be limited or unavailable. Upon verifying the validity of a deletion request, we will delete your personal data from our records and instruct any service providers or third parties to delete your information, when applicable.
"Right to Control Use”
: You may have the right to control or limit the use of your personal data, including:
Right to Opt-Out of Sales/Sharing/cross-context behavioral advertising.
Right to Object to or Opt Out of automated decision-making/profiling.
Right to Opt-Out of processing/Limit Use of Sensitive personal data.
“
Right of Access
”: You may have the right to access your personal data, and to transmit it to another entity.
“
Right of Correction
”: You may have the right to request amendments to your personal data if it is inaccurate or outdated in any way. Upon verifying the validity of a verifiable correction request, we will use commercially reasonable efforts to correct your personal data as directed, considering the nature of the personal data and the purposes of maintaining your personal data.
You may also make a verifiable request to exercise your rights by
contacting us via this link
or the toll-free telephone 1-800-555-0050.
=== END ITEM p0024

=== ITEM p0025
rule 1: {"polarity": "ALLOW", "actor": "we", "action": "collect (operation: collection)", "data": "information that we collect about you or that you provide to us, including any Personal Information", "recipient": "", "source": "", "purpose": "", "condition": "", "condition_predicate": "true"}
rule 2: {"polarity": "DENY", "actor": "we", "action": "collect (operation: collection)", "data": "personal information", "recipient": "", "source": "children under 13", "purpose": "", "condition": "The Service is not intended for children under 13 years of age; from children under 13", "condition_predicate": "(user.age < 13 AND user.age < 13)"}
--- section of rule 1
Disconnecting deletes the stored tokens and connected-account profile data for that account from our systems.
The platforms you may connect and the data we collect from each:
Twitch.
Display name, profile URL, follower count, and broadcaster type. See the
Twitch Privacy Policy
.
TikTok.
Account identifier, display name, username, avatar, bio or profile description, follower count, verification status, and profile link. Uses TikTok Login Kit. See the
TikTok Privacy Policy
.
YouTube/Google.
Channel identifier, channel name, custom channel URL, subscriber count, and authorized channel metadata and statistics returned by YouTube API Services. Our use of information received from Google APIs will adhere to the
Google API Services User Data Policy
, including the Limited Use requirements. You can revoke itch.io’s access to your YouTube data at any time by disconnecting your YouTube account in your itch.io
account settings
or through Google’s security settings page at
https://security.google.com/settings/security/permissions
. If you revoke access, we will delete stored YouTube API data and tokens associated with that connection in accordance with applicable Google API requirements. See the
Google Privacy Policy
.
GitHub.
Username, profile URL, and email address.
Steam.
Steam ID and profile name.
How We Use Your Information
We use information that we collect about you or that you provide to us, including any Personal Information, to:
Provide you with the Service and its contents, and any other information, products or services that you request from us.
Fulfill any other purpose for which you provide it.
Give you notices about your account.
Carry out our obligations and enforce our rights arising from any contracts entered into between you and us, including for billing and collection.
Notify you when Service updates are available, and of changes to any products or services we offer or provide though it.
Improve our Service experience and efficiency.
The usage information we collect helps us to improve our Service and to deliver a better and more personalized experience by enabling us to:
Estimate our audience size and usage patterns.
Store information about your preferences, allowing us to customize our Service according to your individual interests.
Speed up your searches.
Suggest other content which may be of interest to you.
Recognize you when you use the Service.
Disclosure of Your Information
We do not intend to sell or market your Personal Information, however, through providing the Service we may disclose aggregated information about our users in order to deliver the Service, including for the following:
To contractors, service providers, and other third parties we use to support our business, and who are bound by contractual obligations to keep Personal Information confidential and use it only for the purposes for which we disclose it to them.
To a buyer or other successor in the event of a merger, divestiture, restructuring, reorganization, dissolution, or other sale or transfer of some or all of Itch.io’s assets, whether as a going concern or as part of bankruptcy, liquidation, or similar proceeding, in which Personal Information held by Itch.io about our Service users is among the assets transferred.
To fulfill the purpose for which you provide it (For example, if you give us a social media account handle to use social sharing features of our Service, we will transmit the contents of that request to the recipients.).
For any other purpose disclosed by us when you provide the information.
With your consent.
To comply with any court order, law, or legal process, including to respond to any government or regulatory request;
To enforce our rights arising from any contracts entered into between you and us, including the Itch.io Terms of Service, and for billing and collection.
If we believe disclosure is necessary or appropriate to protect the rights, property, or safety of Itch.io, our customers or others.
--- section of rule 2
itch.io Privacy Policy
This Privacy Policy was last modified on March 26, 2026.
Introduction
We at Itch Corp. (“
Company
”, “
We
”, or “
Itch.io
”) respect your privacy and are committed to protecting it through our compliance with this policy. This policy describes the types of information we may collect or that you may provide when you purchase, download, install, register with, access, or use the Itch.io application (the “App”) or website (the “Website” and collectively with the App, the “
Service
”). The policy also describes our practices for collecting, using, maintaining, protecting, and disclosing that information.
We utilize payment processors who have their own privacy policies, which we encourage you to read their privacy policies before providing information on or through them.
Please read this policy carefully to understand our policies and practices regarding your information and how we will treat your information. If you do not agree with our policies and practices, please do not download, register with, or use this Service. By downloading, registering with, or using this Service, you agree to this privacy policy. This policy may change from time to time, with updates appearing on the Website and on the App. Your continued use of this Service after we make changes is deemed to be acceptance of those changes, so please check the policy periodically for updates.
Children Under the Age of 13
The Service is not intended for children under 13 years of age, and we do not knowingly collect personal information from children under 13. If we learn we have collected or received personal information from a child under 13 without verification of parental consent, we will delete that information. If you believe we might have any information from or about a child under 13, please contact us at
support@itch.io
.
Information We Collect and How We Collect It
We collect information from and about users of our Service:
Directly from you when you provide it to us.
Automatically when you use certain parts of the Service.
Information You Provide to Us
When you download, register with, or use this Service, we may ask you provide information:
By which you may be personally identified, such as your name, postal address, email address, telephone number, payment service provider account information, and any other identifier by which you may be contacted online or offline (“
Personal Information
”).
Information that you provide by filling in forms in the Service. This includes information provided at the time of registering to use the Service, posting material, comments or content, and if you request further services from Itch.io. We may also ask you for information when you enter a contest or promotion sponsored by us, and when you report a problem with the Service.
Records and copies of your correspondence (including email addresses and/or phone numbers), if you contact us.
Your responses to surveys that we might ask you to complete for research purposes.
Details of transactions you carry out through the Service and of the fulfillment of your orders. You may be required to provide financial information with a payment service provider before placing an order through the Service. We only hold onto a portion of your payment information for fraud detection purposes.
You may provide information to be published or displayed (“
Posted
”) on public areas of our Service (collectively, “
User Contributions
”). Your User Contributions are Posted and transmitted to others at your own risk. Although you may set certain privacy settings for such information by logging into your account profile, please be aware that no security measures are perfect or impenetrable. Additionally, we cannot control the actions of third parties with whom you may choose to share your User Contributions or view on the Service.
=== END ITEM p0025

