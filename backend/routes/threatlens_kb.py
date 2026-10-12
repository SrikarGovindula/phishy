"""
ThreatLens Cybersecurity Intelligence Knowledge Base & Multi-Lingual Reasoning Engine
Provides production-grade expert responses in English, Hindi (हिन्दी), and Telugu (తెలుగు)
across all primary cybersecurity domains, live simulation telemetry, and dynamic queries.
"""

import re
from typing import Optional, Dict, Any, List

def detect_query_language(text: str, explicit_lang: Optional[str] = None) -> str:
    """Detect language of query (en, hi, or te)"""
    if explicit_lang in ("hi", "te", "en"):
        return explicit_lang
    # Check for Telugu script (U+0C00 - U+0C7F)
    if re.search(r"[\u0C00-\u0C7F]", text):
        return "te"
    # Check for Devanagari / Hindi script (U+0900 - U+097F)
    if re.search(r"[\u0900-\u097F]", text):
        return "hi"
    return "en"


def sanitize_response(text: str) -> str:
    """Strip any accidental raw CSS blocks, HTML style tags or formatting artifacts"""
    # Remove <style>...</style> blocks
    cleaned = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', text, flags=re.IGNORECASE)
    # Remove literal CSS declarations like style="..." or inline rule patterns
    cleaned = re.sub(r'style="[^"]*"', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'style=\'[^\']*\'', '', cleaned, flags=re.IGNORECASE)
    # Remove empty lines excess
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()


def get_threatlens_ai_response(query: str, lang: str = "en", live_data_context: str = "") -> str:
    """Generate comprehensive, expert cybersecurity response based on user intent and language"""
    q_lower = query.lower().strip()
    target_lang = detect_query_language(query, lang)

    # 1. Live Data & Simulation Telemetry Queries
    if live_data_context:
        if target_lang == "te":
            resp = f"""### ThreatLens సిమ్యులేషన్ టెలిమెట్రీ నివేదిక

మీ రియల్-టైమ్ డేటాబేస్ నుండి పొందిన వాస్తవ సమాచారం:

{live_data_context}

**భద్రతా సిఫార్సు:** సిమ్యులేషన్లలో మోసపోయిన వినియోగదారులకు వెంటనే 'Security Awareness' గేమిఫైడ్ మాడ్యూల్స్ మరియు ఇంటరాక్టివ్ ట్రైనింగ్ అందించండి."""
        elif target_lang == "hi":
            resp = f"""### ThreatLens सिमुलेशन टेलीमेट्री रिपोर्ट

आपके रीयल-टाइम डेटाबेस से प्राप्त वास्तविक जानकारी:

{live_data_context}

**सुरक्षा अनुशंसा:** जिन उपयोगकर्ताओं ने सिमुलेशन लिंक पर क्लिक किया है, उन्हें तुरंत 'Security Awareness' मॉड्यूल और प्रशिक्षण सत्र प्रदान करें।"""
        else:
            resp = f"""### ThreatLens Simulation Telemetry Report

Real-time records retrieved from the active Firebase database:

{live_data_context}

**Security Recommendation:** Users who engaged with phishing simulation links should be scheduled for targeted awareness training modules via the Security Awareness section."""
        return sanitize_response(resp)

    # 2. Greetings
    if any(q_lower.startswith(w) for w in ["hi", "hello", "hey", "greetings", "namaste", "namaskaram", "హలో", "నమస్కారం", "नमस्ते", "हेलो"]):
        if target_lang == "te":
            resp = """నమస్కారం! నేను **ThreatLens సైబర్‌ సెక్యూరిటీ అసిస్టెంట్**.

నేను మీకు ఈ క్రింది అంశాలలో సహాయం చేయగలను:
1. **ఫిషింగ్ ఈమెయిల్ గుర్తింపు**: అనుమానాస్పద ఈమెయిల్‌లలోని మోసపూరిత సంకేతాలను గుర్తించడం.
2. **లింక్ & URL భద్రత**: అనుమానాస్పద వెబ్‌సైట్‌లు మరియు లింక్‌లను సురక్షితంగా పరిశీలించడం.
3. **ఈమెయిల్ ప్రామాణీకరణ**: SPF, DKIM, DMARC ప్రోటోకాల్‌ల వివరణ.
4. **సంక్షోభ నివారణ**: లింక్‌పై క్లిక్ చేసినప్పుడు లేదా పాస్‌వర్డ్ నమోదు చేసినప్పుడు తీసుకోవాల్సిన చర్యలు.
5. **పాస్‌వర్డ్ & MFA భద్రత**: బలమైన పాస్‌వర్డ్‌లు మరియు మల్టీ-ఫ్యాక్టర్ ప్రామాణీకరణ పద్ధతులు.
6. **రక్షణాత్మక భద్రత**: రాన్సమ్‌వేర్, మాల్‌వేర్, జీరో-డే, ఫైర్‌వాల్స్ మరియు నెట్‌వర్క్ భద్రత.

మీ సందేహం లేదా ప్రశ్నను ఇక్కడ అడగండి!"""
        elif target_lang == "hi":
            resp = """नमस्ते! मैं **ThreatLens साइबर सुरक्षा सहायक** हूँ।

मैं निम्नलिखित विषयों में आपकी सहायता कर सकता हूँ:
1. **फ़िशिंग ईमेल की पहचान**: संदिग्ध संदेशों में छिपे खतरों को पहचानना।
2. **संदिग्ध लिंक और URL सुरक्षा**: सुरक्षित रूप से हाइपरलिंक की जांच करना।
3. **ईमेल प्रमाणीकरण प्रोटोकॉल**: SPF, DKIM और DMARC की तकनीकी व्याख्या।
4. **घटना प्रतिक्रिया (Incident Response)**: लिंक पर क्लिक करने पर तुरंत क्या कदम उठाएं।
5. **पासवर्ड और MFA सुरक्षा**: मजबूत सुरक्षा प्रथाएं और बहु-कारक प्रमाणीकरण।
6. **साइबर सुरक्षा खतरे**: रैंसमवेयर, मैलवेयर, फ़ायरवॉल और नेटवर्क सुरक्षा।

कृपया अपना सवाल पूछें!"""
        else:
            resp = """Hello! I am the **ThreatLens Cybersecurity Intelligence Assistant**.

I can assist you with:
1. **Phishing Detection**: Identifying red flags, domain spoofing, and social engineering in emails.
2. **URL & Link Safety**: Analyzing deceptive subdomains, typosquatting, and safe inspection practices.
3. **Email Protocols**: Explaining SPF, DKIM, and DMARC authentication standards.
4. **Incident Response**: Emergency steps if you clicked a suspicious link or entered credentials.
5. **Threat Defenses**: Ransomware, malware analysis, firewalls, and zero-day vulnerabilities.
6. **ThreatLens Tools**: Guiding you through Email Header Analysis, Awareness Training, and Telemetry.

How can I help protect your organization today?"""
        return sanitize_response(resp)

    # 3. Ransomware
    if any(k in q_lower for k in ["ransomware", "ransom", "రాన్సమ్‌వేర్", "రాన్సమ్", "रैंसमवेयर"]):
        if target_lang == "te":
            resp = """### రాన్సమ్‌వేర్ (Ransomware) అంటే ఏమిటి? మరియు నివారణ చర్యలు:

రాన్సమ్‌వేర్ అనేది బాధితుడి ఫైళ్ళను లేదా మొత్తం సిస్టమ్‌ను గుప్తీకరించి (Encrypt), వాటిని తిరిగి విడుదల చేయడానికి డబ్బు (Ransom) డిమాండ్ చేసే అత్యంత ప్రమాదకరమైన మాల్‌వేర్.

**ముఖ్యమైన దశలు:**
1. **ప్రారంభ ప్రవేశం (Initial Access)**: ఫిషింగ్ ఈమెయిల్‌లు, హానికరమైన అటాచ్‌మెంట్‌లు, లేదా అన్‌ప్యాచ్ చేయబడిన RDP పోర్ట్‌ల ద్వారా వ్యాపిస్తుంది.
2. **గుప్తీకరణ (Encryption)**: సిస్టమ్‌లోని ముఖ్యమైన పత్రాలు, డేటాబేస్‌లను బలమైన అల్గారిథమ్‌లతో (AES/RSA) లాక్ చేస్తుంది.
3. **డిమాండ్ నోట్**: డీక్రిప్షన్ కీ కోసం క్రిప్టోకరెన్సీ (బిట్‌కాయిన్) చెల్లించాలని స్క్రీన్‌పై నోటీస్ చూపిస్తుంది.

**రక్షణ పద్ధతులు:**
- **3-2-1 బ్యాకప్ వ్యూహం**: డేటా యొక్క 3 కాపీలను, 2 వేర్వేరు మాధ్యమాలలో ఉంచండి, అందులో 1 కాపీ ఆఫ్‌లైన్ (ఎయిర్-గ్యాప్డ్) లో ఉండాలి.
- **ఈమెయిల్ ఫిల్టరింగ్**: ThreatLens వంటి సాధనాల ద్వారా వచ్చే ఈమెయిల్ అటాచ్‌మెంట్లను స్కాన్ చేయండి.
- **సిస్టమ్ అప్‌డేట్స్**: OS మరియు సాఫ్ట్‌వేర్ ప్యాచ్‌లను ఎప్పటికప్పుడు అప్‌డేట్ చేయండి."""
        elif target_lang == "hi":
            resp = """### रैंसमवेयर (Ransomware) क्या है? और इससे कैसे बचें:

रैंसमवेयर एक प्रकार का दुर्भावनापूर्ण सॉफ़्टवेयर (मैलवेयर) है जो उपयोगकर्ता की फ़ाइलों या पूरे सिस्टम को एन्क्रिप्ट (लॉक) कर देता है और फ़ाइलों को अनलॉक करने के लिए फिरौती (Ransom) की मांग करता है।

**हमले के मुख्य चरण:**
1. **प्रवेश (Initial Access)**: फ़िशिंग ईमेल, दुर्भावनापूर्ण अटैचमेंट्स, या असुरक्षित RDP पोर्ट्स के माध्यम से नेटवर्क में प्रवेश।
2. **एन्क्रिप्शन (Encryption)**: सिस्टम में मौजूद महत्वपूर्ण दस्तावेज़ों और डेटाबेस को लॉक कर देना।
3. **फिरौती की मांग**: फ़ाइलें वापस पाने के लिए क्रिप्टोकरेंसी में भुगतान की मांग करने वाला नोट प्रदर्शित करना।

**बचाव के प्रमुख उपाय:**
- **3-2-1 बैकअप रणनीति**: डेटा की 3 प्रतियां रखें, 2 अलग-अलग मीडिया पर, और कम से कम 1 प्रति ऑफ़लाइन (Air-gapped) रखें।
- **फ़िशिंग जागरूकता**: अज्ञात स्रोतों से प्राप्त ईमेल लिंक्स या अटैचमेंट्स को कभी न खोलें।
- **नियमित पैचिंग**: ऑपरेटिंग सिस्टम और सॉफ़्टवेयर को हमेशा नवीनतम सुरक्षा पैच के साथ अपडेट रखें।"""
        else:
            resp = """### Understanding Ransomware & Defensive Countermeasures:

Ransomware is a class of malicious software that encrypts high-value organizational data or locks system access, demanding cryptocurrency extortion payments for decryption keys.

**Core Attack Stages:**
1. **Initial Vector**: Social engineering phishing emails carrying weaponized attachments, malicious macro scripts, or vulnerable Internet-facing services (e.g., exposed RDP).
2. **Lateral Movement & Privilege Escalation**: Attackers locate active directory domain controllers and sensitive backup storage.
3. **Data Exfiltration (Double Extortion)**: Threat actors steal intellectual property before encrypting systems, threatening public leaks if the ransom is unpaid.

**Essential Defensive Protocols:**
- **3-2-1-1 Backup Architecture**: Maintain 3 copies of data across 2 media types, with 1 stored off-site and 1 immutable/air-gapped.
- **Endpoint Detection & Response (EDR)**: Deploy behavioral monitoring to identify mass file rename or encryption operations.
- **Email Security**: Block macro execution in office documents and screen links using ThreatLens Email Analyzer."""
        return sanitize_response(resp)

    # 4. Malware (General, Viruses, Trojans, Worms, Spyware, Keyloggers)
    if any(k in q_lower for k in ["malware", "virus", "trojan", "worm", "spyware", "keylogger", "adware", "రూట్‌కిట్", "వైరస్", "మాల్‌వేర్", "वायरस", "मैलवेयर"]):
        if target_lang == "te":
            resp = """### మాల్‌వేర్ (Malware) రకాలు మరియు భద్రతా చర్యలు:

మాల్‌వేర్ (Malicious Software) అనేది కంప్యూటర్లు, నెట్‌వర్క్‌లు లేదా డేటాను దెబ్బతీయడానికి రూపొందించబడిన ఏదైనా హానికరమైన కోడ్.

**ప్రధాన రకాలు:**
1. **ట్రోజన్ (Trojan Horse)**: చట్టబద్ధమైన సాఫ్ట్‌వేర్‌లా నటిస్తూ వెనుకవైపు బ్యాక్‌డోర్‌ను తెరుస్తుంది.
2. **స్పైవేర్ & కీలాగర్ (Spyware/Keylogger)**: మీరు టైప్ చేసే పాస్‌వర్డ్‌లు మరియు సమాచారాన్ని రహస్యంగా రికార్డ్ చేసి హ్యాకర్లకు పంపుతుంది.
3. **వార్మ్స్ (Worms)**: వినియోగదారుల ప్రమేయం లేకుండా నెట్‌వర్క్‌ల గుండా స్వయంచాలకంగా వ్యాప్తి చెందుతుంది.
4. **రూట్‌కిట్ (Rootkit)**: ఆపరేటింగ్ సిస్టమ్ కెర్నల్ స్థాయిలో దాగి ఉండి యాంటీవైరస్‌కు చిక్కకుండా నియంత్రణ సాధిస్తుంది.

**రక్షణ చర్యలు:**
- ఎల్లప్పుడూ విశ్వసనీయ అధికారిక వనరుల నుండి మాత్రమే సాఫ్ట్‌వేర్ డౌన్‌లోడ్ చేసుకోండి.
- ఈమెయిల్‌లలో వచ్చే అనుమానాస్పద `.exe`, `.scr`, `.zip` ఫైళ్లను తెరవకండి.
- EDR లేదా యాంటీవైరస్ రియల్-టైమ్ ప్రొటెక్షన్‌ను ఎల్లప్పుడూ ఆన్‌లో ఉంచండి."""
        elif target_lang == "hi":
            resp = """### मैलवेयर (Malware) के प्रकार और सुरक्षा उपाय:

मैलवेयर (दुर्भावनापूर्ण सॉफ़्टवेयर) किसी भी प्रोग्राम या फ़ाइल को संदर्भित करता है जो उपयोगकर्ता की जानकारी के बिना सिस्टम, नेटवर्क या डेटा को नुकसान पहुंचाता है।

**प्रमुख श्रेणियां:**
1. **ट्रोजन (Trojan)**: उपयोगी सॉफ़्टवेयर का भेष बनाकर सिस्टम में पिछले दरवाजे (Backdoor) स्थापित करता है।
2. **स्पाइवेयर और कीलॉगर**: आपकी स्क्रीन, टाइप किए गए पासवर्ड और ब्राउज़िंग गतिविधियों की जासूसी करता है।
3. **वॉर्म (Worm)**: किसी मानवीय हस्तक्षेप के बिना नेटवर्क के माध्यम से अन्य कंप्यूटरों में फैलता है।
4. **रैंसमवेयर**: फ़ाइलों को एन्क्रिप्ट करके वसूली मांगता है।

**सुरक्षा अनुशंसाएं:**
- केवल आधिकारिक और सत्यापित वेबसाइटों से ही सॉफ़्टवेयर डाउनलोड करें।
- ईमेल में संदिग्ध अटैचमेंट्स को ThreatLens में जांचे बिना कभी न खोलें।
- सुरक्षा सॉफ़्टवेयर की रीयल-टाइम स्कैनिंग को हमेशा सक्रिय रखें।"""
        else:
            resp = """### Malware Categorization & Endpoint Protection:

Malware (Malicious Software) is an umbrella term for software intentionally designed to cause damage to computers, servers, clients, or computer networks.

**Primary Classifications:**
1. **Trojans**: Disguised as legitimate software (e.g., invoices, utility tools) to grant unauthorized remote backdoors.
2. **Spyware & Keyloggers**: Covertly capture keystrokes, clipboard credentials, and screen captures.
3. **Worms**: Self-replicating code that exploits network protocol vulnerabilities (e.g., SMB/MS17-010) to spread without human interaction.
4. **Rootkits**: Kernel-level persistence mechanisms designed to evade user-space anti-malware scanners.

**Defensive Hygiene:**
- Implement software restriction policies and application whitelisting (AppLocker / WDAC).
- Disable automatic macro execution in Microsoft Office applications.
- Inspect incoming email attachments via the ThreatLens Email Analyzer."""
        return sanitize_response(resp)

    # 5. Zero-Day Vulnerabilities
    if any(k in q_lower for k in ["zero-day", "zero day", "0-day", "vulnerability", "జీరో డే", "జీరో-డే", "जीरो-डे"]):
        if target_lang == "te":
            resp = """### జీరో-డే (Zero-Day) దుర్బలత్వం అంటే ఏమిటి?

జీరో-డే దుర్బలత్వం అనేది సాఫ్ట్‌వేర్ తయారీదారునికి తెలియని, లేదా తెలిసినప్పటికీ ఇంకా ఎలాంటి సెక్యూరిటీ ప్యాచ్ విడుదల చేయని లోపం. 

**జీరో-డే ఎందుకు ప్రమాదకరం?**
- దీనిపై దాడి జరిగినప్పుడు డిఫెండర్లకు రక్షించుకోవడానికి "సున్నా రోజులు" (Zero days) ఉంటాయి.
- సాంప్రదాయ యాంటీవైరస్ సిగ్నేచర్లు దీనిని గుర్తించలేవు, ఎందుకంటే దీని నమూనా ముందుగా నమోదు కాలేదు.

**రక్షణ వ్యూహాలు:**
1. **బిహేవియరల్ మానిటరింగ్ (EDR)**: సిగ్నేచర్ల కంటే సిస్టమ్ ప్రవర్తనను పర్యవేక్షించే టూల్స్ వాడటం.
2. **నెట్‌వర్క్ సెగ్మెంటేషన్**: దాడి జరిగినా మొత్తం నెట్‌వర్క్‌కు విస్తరించకుండా వేరు చేయడం.
3. **వర్చువల్ ప్యాచింగ్**: WAF మరియు IPS నియమాల ద్వారా తాత్కాలికంగా ట్రాఫిక్‌ను అడ్డుకోవడం."""
        elif target_lang == "hi":
            resp = """### ज़ीरो-डे (Zero-Day) भेद्यता क्या है?

ज़ीरो-डे भेद्यता एक ऐसी सुरक्षा खामी है जिसके बारे में सॉफ़्टवेयर विक्रेता या डेवलपर्स को जानकारी नहीं होती है, या जिसके लिए अभी तक कोई आधिकारिक सुरक्षा पैच उपलब्ध नहीं है।

**यह इतना खतरनाक क्यों है?**
- सुरक्षा टीमों के पास सुरक्षा के लिए "शून्य दिन" होते हैं, अर्थात कोई तैयार समाधान मौजूद नहीं होता।
- पारंपरिक सिग्नेचर-आधारित एंटीवायरस इसे पहचान नहीं पाते।

**सुरक्षा रणनीतियाँ:**
1. **व्यवहार-आधारित पहचान (EDR)**: असामान्य गतिविधियों और संदिग्ध मेमोरी इंजेक्शन की निगरानी।
2. **नेटवर्क विभाजन**: सिस्टम्स को अलग-अलग ज़ोन में विभाजित रखना ताकि हमला अन्यत्र न फैले।
3. **प्रिंसिपल ऑफ़ लीस्ट प्रिविलेज**: उपयोगकर्ताओं को केवल आवश्यक न्यूनतम अनुमतियाँ प्रदान करना।"""
        else:
            resp = """### Zero-Day Vulnerabilities & Exploit Mitigation:

A **Zero-Day Vulnerability** is a software security flaw unknown to the vendor, or known without an available official vendor patch. A **Zero-Day Exploit** is the active weaponization of this flaw.

**Why They Pose Maximum Risk:**
- Signature-based intrusion detection cannot identify novel attack vectors.
- Attackers maintain asymmetric advantage until detection and patch engineering occur.

**Proactive Defenses:**
1. **Behavioral EDR & Heuristics**: Detect unauthorized memory manipulation, code injection, or abnormal parent-child process relationships.
2. **Zero-Trust Network Architecture**: Limit lateral traversal through strict microsegmentation and continuous authentication.
3. **Attack Surface Reduction**: Disable unnecessary protocols, services, and script execution engines across all corporate assets."""
        return sanitize_response(resp)

    # 6. Firewalls, WAF & Network Security
    if any(k in q_lower for k in ["firewall", "waf", "ids", "ips", "network security", "ఫైర్‌వాల్", "ఫైర్వాల్", "फ़ायरवॉल"]):
        if target_lang == "te":
            resp = """### ఫైర్‌వాల్ (Firewall) & నెట్‌వర్క్ భద్రత:

ఫైర్‌వాల్ అనేది మీ ప్రైవేట్ నెట్‌వర్క్ మరియు బాహ్య ఇంటర్నెట్ మధ్య ట్రాఫిక్‌ను నియంత్రించే భద్రతా రక్షణ కవచం.

**ప్రధాన రకాలు:**
1. **ప్యాకెట్ ఫిల్టరింగ్ ఫైర్‌వాల్**: IP చిరునామా, పోర్ట్ నంబర్లు మరియు ప్రోటోకాల్ ఆధారంగా ప్యాకెట్లను పరిశీలిస్తుంది.
2. **నెక్స్ట్-జెనరేషన్ ఫైర్‌వాల్ (NGFW)**: అప్లికేషన్ గుర్తింపు, డీప్ ప్యాకెట్ ఇన్‌స్పెక్షన్ (DPI) మరియు చొరబాటు నిరోధకత (IPS) కలిగి ఉంటుంది.
3. **WAF (వెబ్ అప్లికేషన్ ఫైర్‌వాల్)**: వెబ్‌సైట్లపై జరిగే SQL Injection, XSS దాడుల నుండి లేయర్ 7 (HTTP/S) ను రక్షిస్తుంది.

**ఉత్తమ పద్ధతులు:**
- డిఫాల్ట్-డెనై (Default Deny) విధానాన్ని అమలు చేయండి: అవసరమైన పోర్టులను మాత్రమే అనుమతించండి.
- నెట్‌వర్క్ లాగ్‌లను SIEM సిస్టమ్‌లో నిరంతరం విశ్లేషించండి."""
        elif target_lang == "hi":
            resp = """### फ़ायरवॉल (Firewall) और नेटवर्क सुरक्षा अवलोकन:

फ़ायरवॉल एक नेटवर्क सुरक्षा प्रणाली है जो पूर्वनिर्धारित सुरक्षा नियमों के आधार पर आने वाले और बाहर जाने वाले नेटवर्क ट्रैफ़िक की निगरानी और नियंत्रण करती है।

**मुख्य प्रकार:**
1. **स्टेटफुल इंस्पेक्शन फ़ायरवॉल**: सक्रिय कनेक्शनों की स्थिति को ट्रैक करता है और अनधिकृत ट्रैफ़िक को रोकता है।
2. **NGFW (नेक्स्ट-जेनरेशन फ़ायरवॉल)**: डीप पैकेट इंस्पेक्शन (DPI) और घुसपैठ रोकथाम (IPS) क्षमताएं प्रदान करता है।
3. **WAF (वेब एप्लिकेशन फ़ायरवॉल)**: HTTP ट्रैफ़िक की सुरक्षा करता है और SQL इंजेक्शन व XSS जैसे वेब हमलों को रोकता है।

**सुरक्षा युक्तियाँ:**
- 'Default Deny' नियम लागू करें: अज्ञात या अनावश्यक पोर्ट्स को हमेशा ब्लॉक रखें।
- नियमित रूप से फ़ायरवॉल नियमों का ऑडिट करें।"""
        else:
            resp = """### Enterprise Firewalls, WAF & Perimeter Defense:

A firewall acts as a security barrier that monitors and filters incoming and outgoing network traffic based on established security policies.

**Core Architectures:**
1. **Next-Generation Firewalls (NGFW)**: Combine stateful inspection with Layer 7 application awareness, SSL/TLS decryption, and integrated Intrusion Prevention Systems (IPS).
2. **Web Application Firewalls (WAF)**: Dedicated to inspecting Layer 7 HTTP/HTTPS traffic to prevent OWASP Top 10 exploits (SQLi, XSS, CSRF, SSRF).
3. **Distributed Firewalls (Cloud/Microsegmentation)**: Enforce east-west traffic isolation between microservices and containers.

**Best Practices:**
- Adopt a strict **Default-Deny** rule set for all ingress and egress interfaces.
- Regularly review firewall access control lists (ACLs) and deprecate unused rules."""
        return sanitize_response(resp)

    # 7. SQL Injection (SQLi) & Web Attacks (XSS, CSRF)
    if any(k in q_lower for k in ["sql injection", "sqli", "xss", "cross site", "csrf", "web attack", "sql ఇంజెక్షన్", "एसक्यूएल"]):
        if target_lang == "te":
            resp = """### SQL ఇంజెక్షన్ (SQL Injection) & వెబ్ అటాక్స్:

**SQL ఇంజెక్షన్ అంటే ఏమిటి?**
యూజర్ ఇన్‌పుట్ ద్వారా దుర్మార్గమైన SQL క్వెరీలను డేటాబేస్‌కు పంపించి, అనధికారికంగా డేటాను దొంగిలించడం లేదా తొలగించడం.

**ఉదాహరణ:** లాగిన్ ఫీల్డ్‌లో `' OR '1'='1` నమోదు చేసినప్పుడు సరైన ధృవీకరణ లేకపోతే పాస్‌వర్డ్ లేకుండానే లాగిన్ అవుతుంది.

**నివారణ చర్యలు:**
1. **పారామీటరైజ్డ్ క్వెరీలు (Prepared Statements)**: యూజర్ ఇన్‌పుట్‌ను కోడ్‌లా కాకుండా కేవలం డేటాలా మాత్రమే పరిగణించడం.
2. **ఇన్‌పుట్ ధ్రువీకరణ (Input Validation)**: అనుమతించబడిన అక్షరాలను మాత్రమే అంగీకరించడం.
3. **కనిష్ట హక్కుల సూత్రం (Principle of Least Privilege)**: డేటాబేస్ యూజర్‌కు అనవసరమైన అడ్మిన్ హక్కులు ఇవ్వకపోవడం."""
        elif target_lang == "hi":
            resp = """### SQL इंजेक्शन (SQLi) और वेब सुरक्षा:

**SQL इंजेक्शन क्या है?**
यह एक गंभीर सुरक्षा भेद्यता है जहां हमलावर किसी वेब एप्लिकेशन के इनपुट फ़ील्ड में दुर्भावनापूर्ण SQL कोड डालकर बैकएंड डेटाबेस को सीधे एक्सेस या नष्ट कर सकता है।

**बचाव के प्रभावी उपाय:**
1. **पैरामीटराइज्ड क्वेरीज़ (Prepared Statements)**: इनपुट को सीधे SQL स्ट्रिंग में जोड़ने के बजाय हमेशा पैरामीटर के रूप में उपयोग करें।
2. **इनपुट सैनिटाइजेशन**: उपयोगकर्ता द्वारा दर्ज किए गए विशेष वर्णों को फ़िल्टर करें।
3. **न्यूनतम विशेषाधिकार सिद्धांत**: एप्लिकेशन को केवल आवश्यक टेबल एक्सेस की अनुमति दें, एडमिन अधिकार नहीं।"""
        else:
            resp = """### SQL Injection (SQLi) & Web Application Security:

**Mechanism of Action:**
SQL Injection occurs when untrusted user data is concatenated directly into database query interpreters without sanitization, allowing attackers to bypass authentication, dump sensitive databases, or execute remote commands.

**Remediation Standards:**
1. **Parameterized Queries (Prepared Statements)**: The definitive defense. Queries are pre-compiled and inputs are strictly bound as typed parameters.
2. **Object-Relational Mapping (ORM)**: Use secure ORM frameworks that leverage parameterized abstraction by default.
3. **Principle of Least Privilege**: Ensure the web application service account possesses only minimum required privileges."""
        return sanitize_response(resp)

    # 8. Phishing Detection & Red Flags
    if any(k in q_lower for k in ["how to detect", "identify phishing", "spot phishing", "signs of phishing", "recognize phishing", "ఫిషింగ్ గుర్తించడం", "ఫిషింగ్ అంటే", "फ़िशिंग पहचान", "फ़िशिंग क्या है"]):
        if target_lang == "te":
            resp = """### ఫిషింగ్ ఈమెయిల్‌ను గుర్తించడం ఎలా (Red Flags):

1. **పంపినవారి వాస్తవ డొమైన్ తనిఖీ (Sender Domain Discrepancy)**:
   - డిస్‌ప్లే పేరు ప్రసిద్ధ సంస్థగా కనిపించినప్పటికీ, ఈమెయిల్ చిరునామాను పూర్తిగా చూడండి (`support@micros0ft-security.xyz`).

2. **అత్యవసర ఒత్తిడి లేదా భయం (Urgency & Coercion)**:
   - "మీ ఖాతా 24 గంటల్లో నిలిపివేయబడుతుంది", "తక్షణమే వెరిఫై చేయండి" వంటి ఆందోళన కలిగించే భాష సోషల్ ఇంజనీరింగ్ సంకేతం.

3. **మోసపూరిత హైపర్‌లింక్‌లు (Deceptive Hyperlinks)**:
   - లింక్‌పై క్లిక్ చేయకుండా మౌస్ కర్సర్‌ను దానిపై ఉంచండి (Hover). కనిపించే అసలు URL గమ్యస్థానాన్ని జాగ్రత్తగా చదవండి.

4. **సాధారణ సంబోధనలు (Generic Greetings)**:
   - "Dear Customer" లేదా "Dear User" వంటి సాధారణ సంబోధనలు తరచుగా సామూహిక ఫిషింగ్ ప్రచారాలలో కనిపిస్తాయి.

5. **అనుమానాస్పద అటాచ్‌మెంట్‌లు (Dangerous Attachments)**:
   - `.exe`, `.scr`, `.iso`, లేదా పాస్‌వర్డ్ రక్షిత `.zip` ఫైల్‌లు మాల్‌వేర్ మోసే ప్రమాదం ఉంది.

**పరిష్కారం:** అనుమానాస్పద ఈమెయిల్‌ను ThreatLens లోని **Email Analyzer** లో పేస్ట్ చేసి భద్రతా బృందానికి నివేదించండి."""
        elif target_lang == "hi":
            resp = """### फ़िशिंग ईमेल की पहचान कैसे करें (मुख्य संकेत):

1. **प्रेषक का वास्तविक डोमेन जांचें (Sender Domain Inspection)**:
   - प्रेषक का नाम चाहे जाना-पहचाना लगे, लेकिन ईमेल पते का डोमेन ध्यान से देखें (उदा. `security@bankk-support.com`)।

2. **तात्कालिकता और भय की रणनीति (Urgency & Fear Tactics)**:
   - "खाता 24 घंटे में ब्लॉक हो जाएगा", "तुरंत पासवर्ड रीसेट करें" जैसी भाषा उपयोगकर्ताओं को बिना सोचे कार्रवाई करने के लिए प्रेरित करती है।

3. **भ्रामक हाइपरलिंक्स (Deceptive Hyperlinks)**:
   - बिना क्लिक किए लिंक पर कर्सर होवर करें। स्टेटस बार में प्रदर्शित वास्तविक URL की जांच करें।

4. **व्याकरण की त्रुटियां और सामान्य अभिवादन**:
   - खराब व्याकरण, गलत वर्तनी और "Dear Customer" जैसे सामान्य संबोधन अक्सर फ़िशिंग का संकेत होते हैं।

5. **अपेक्षित नहीं अटैचमेंट्स (Suspicious Attachments)**:
   - `.exe`, `.scr`, `.vbs`, या पासवर्ड-सुरक्षित `.zip` फ़ाइलें सिस्टम में मैलवेयर डाल सकती हैं।

**सुझाव:** किसी भी संदिग्ध ईमेल को ThreatLens के **Email Analyzer** टूल में स्कैन करें।"""
        else:
            resp = """### How to Identify a Phishing Email (Core Red Flags):

1. **Sender Address & Domain Verification**:
   - Attackers spoof the display name (e.g., "IT Helpdesk"), but the underlying envelope sender reveals an unrelated domain (e.g., `admin@it-support-portal-xyz.com`).
   - Watch out for typosquatting (substituting letters: `rn` for `m`, `0` for `o`).

2. **Manufactured Urgency & Coercive Phrasing**:
   - Phrases like *"Immediate Action Required"*, *"Account Deletion in 24 Hours"*, or *"Unusual Login Detected"* trigger emotional panic.

3. **Deceptive Anchor Links**:
   - The link text may say `https://portal.company.com`, but hovering over it reveals a destination pointing to an unverified third-party IP or landing page.

4. **Unexpected Attachments**:
   - Invoices, resumes, or shipping manifests containing `.zip`, `.iso`, `.html`, or macro-enabled documents (`.docm`, `.xlsm`).

5. **Generic Greetings & Context Inconsistencies**:
   - "Dear Valued Employee" rather than your specific name.

**Action Item:** Submit suspicious email headers and body text directly to the ThreatLens **Email Analyzer** for multi-signal verification."""
        return sanitize_response(resp)

    # 9. Suspicious Link Safety & Inspection
    if any(k in q_lower for k in ["link", "url", "hover", "shortener", "లింక్", "యుఆర్ఎల్", "लिंक", "यूआरएल"]):
        if target_lang == "te":
            resp = """### అనుమానాస్పద లింక్‌లు మరియు URL ల భద్రతా మార్గదర్శిని:

1. **లింక్‌పై హోవర్ చేయండి (Hover to Inspect)**:
   - క్లిక్ చేయకుండా కర్సర్‌ను లింక్‌పై ఉంచండి. బ్రౌజర్ దిగువ భాగంలో లేదా టూల్‌టిప్‌లో అసలైన గమ్యస్థాన URL కనిపిస్తుంది.
2. **సబ్‌డొమైన్ మోసాలను గుర్తించండి**:
   - `paypal.com.attacker-server.com` లో అసలు డొమైన్ `attacker-server.com`, `paypal.com` కాదు. కుడివైపు నుండి చదవడం ముఖ్యం.
3. **URL షార్ట్‌నర్‌లు (bit.ly, tinyurl)**:
   - అసలు గమ్యస్థానాన్ని దాచడానికి దాడిదారులు తరచుగా షార్ట్‌నర్‌లను ఉపయోగిస్తారు. అధికారిక సైట్ల కోసం నేరుగా బ్రౌజర్‌లో టైప్ చేయండి.
4. **HTTPS మాత్రమే సురక్షితం కాదు**:
   - నేరస్థులు కూడా ఉచిత SSL సర్టిఫికేట్‌లను ఉపయోగిస్తారు. ప్యాడ్‌లాక్ చిహ్నం ఉండటం వల్ల సైట్ నకిలీ కాదని అర్థం కాదు.

**ముఖ్యమైన సూచన:** మీకు అనుమానం ఉన్న లింక్‌ను ఎప్పుడూ నేరుగా తెరవకండి. ThreatLens లో తనిఖీ చేయండి."""
        elif target_lang == "hi":
            resp = """### संदिग्ध लिंक और URL की सुरक्षा कैसे जांचें:

1. **कर्सर होवर करें (Hover Before Clicking)**:
   - बिना क्लिक किए कर्सर को लिंक पर ले जाएं। नीचे कोने में दिखाई देने वाले वास्तविक URL को ध्यान से पढ़ें।
2. **सबडोमेन धोखे की पहचान (Subdomain Deception)**:
   - `google.com.malicious-site.net` में वास्तविक वेबसाइट `malicious-site.net` है, Google नहीं।
3. **टाइपोस्कॉटिंग (Typosquatting)**:
   - वर्णों के सूक्ष्म परिवर्तन देखें (जैसे `micros0ft.com` या `paypa1.com`)।
4. **URL शॉर्टनर से सावधान रहें**:
   - अज्ञात प्रेषकों से आने वाले शॉर्ट लिंक (`bit.ly`, `tinyurl`) को खोलने से बचें।

**सुरक्षा टिप:** आधिकारिक पोर्टल पर जाने के लिए हमेशा अपने ब्राउज़र में स्वयं पता टाइप करें।"""
        else:
            resp = """### Inspecting Suspicious Links & URLs Safely:

1. **Hover Before You Click**:
   - Position your cursor over the link to reveal the destination URL in your browser's bottom-left status bar.
2. **Deceptive Subdomain Hierarchy**:
   - In `login.microsoft.com.attacker-domain.org`, the authoritative domain is `attacker-domain.org`. Always evaluate the primary domain immediately preceding the top-level domain (`.com`, `.org`, etc.).
3. **Homoglyph & Typosquatting Attacks**:
   - Attackers substitute visual characters (e.g., Latin 'a' with Cyrillic 'а', or number '1' for letter 'l').
4. **URL Shorteners & Direct IP Hostnames**:
   - Corporate emails rarely use `bit.ly` or direct IP addresses. Treat these as hostile indicators.

**Best Practice:** Never click suspicious links. Use ThreatLens **Email Analyzer** to evaluate safety."""
        return sanitize_response(resp)

    # 10. Incident Response - What to do if clicked
    if any(k in q_lower for k in ["clicked", "what to do if", "fell for", "compromised", "accidentally clicked", "క్లిక్ చేశాను", "క్లిక్ చేస్తే", "क्लिक कर दिया", "अगर क्लिक"]):
        if target_lang == "te":
            resp = """### అత్యవసర ప్రతిస్పందన: మీరు అనుమానాస్పద లింక్‌పై క్లిక్ చేస్తే తీసుకోవాల్సిన 5 చర్యలు:

1. **నెట్‌వర్క్ కనెక్షన్ డిస్‌కనెక్ట్ చేయండి (Disconnect Immediately)**:
   - మీ కంప్యూటర్ లేదా మొబైల్‌ను Wi-Fi లేదా ఈథర్‌నెట్ కేబుల్ నుండి వెంటనే డిస్‌కనెక్ట్ చేయండి. ఇది మాల్‌వేర్ వ్యాప్తిని ఆపుతుంది.
2. **పాస్‌వర్డ్ మార్చండి (Change Passwords from a Secondary Device)**:
   - మీరు యూజర్‌నేమ్/పాస్‌వర్డ్ నమోదు చేసి ఉంటే, వెంటనే వేరొక సురక్షితమైన పరికరం నుండి ఆ ఖాతా పాస్‌వర్డ్‌ను మార్చండి.
3. **సెషన్లను లాగౌట్ చేయండి (Revoke Active Sessions)**:
   - మీ ఖాతా సెట్టింగ్‌లలో "Sign out of all sessions/devices" ఎంపికను ఎంచుకోండి.
4. **IT సెక్యూరిటీ బృందానికి నివేదించండి (Report to SOC / Security Team)**:
   - అనుమానాస్పద ఈమెయిల్‌ను దాచకుండా మీ IT సపోర్ట్ లేదా సైబర్‌ సెక్యూరిటీ బృందానికి తెలియజేయండి.
5. **యాంటీ-మాల్‌వేర్ స్కాన్ నిర్వహించండి (Run Endpoint Antivirus Scan)**:
   - సిస్టమ్‌లో అనుమానాస్పద ఫైల్‌లు లేదా కీలాగర్లు ఉన్నాయో లేదో తెలుసుకోవడానికి పూర్తి స్కాన్ చేయండి."""
        elif target_lang == "hi":
            resp = """### आपातकालीन प्रतिक्रिया: संदिग्ध लिंक पर क्लिक करने पर क्या करें:

1. **इंटरनेट से तुरंत डिस्कनेक्ट करें (Disconnect Network)**:
   - अपने डिवाइस को तुरंत वाई-फाई या नेटवर्क केबल से अलग करें ताकि संभावित मैलवेयर अन्य सिस्टम में न फैले।
2. **पासवर्ड तुरंत बदलें (Reset Password)**:
   - यदि आपने क्रेडेंशियल दर्ज किए हैं, तो किसी अन्य सुरक्षित डिवाइस से तुरंत उस खाते का पासवर्ड बदलें।
3. **सभी सक्रिय सत्र समाप्त करें (Revoke Sessions)**:
   - संबंधित सेवा के सुरक्षा पृष्ठ पर जाएं और "सभी उपकरणों से लॉग आउट करें" का चयन करें।
4. **अपनी आईटी सुरक्षा / SOC टीम को सूचित करें**:
   - घटना की जानकारी तुरंत अपनी सुरक्षा टीम को दें।
5. **पूर्ण मैलवेयर स्कैन चलाएं**:
   - अधिकृत एंटीवायरस सॉफ़्टवेयर से संपूर्ण सिस्टम स्कैन पूरा करें।"""
        else:
            resp = """### Emergency Checklist: What to Do If You Clicked a Suspicious Link:

1. **Isolate the Endpoint (Disconnect Immediately)**:
   - Disconnect your computer from Wi-Fi or unplug the Ethernet cable immediately. This severs command-and-control channels and prevents lateral malware spread.
2. **Reset Compromised Credentials from an Out-of-Band Device**:
   - If you submitted your password on a landing page, use a separate, known-clean device to reset the password immediately.
3. **Revoke All Active Sessions & OAuth Tokens**:
   - In your account security settings, select *"Sign out everywhere"* or revoke active refresh tokens.
4. **Notify Your IT Security / SOC Team**:
   - Forward the original email headers and campaign details to your internal security responders.
5. **Run a Full Endpoint EDR / Antivirus Scan**:
   - Execute an in-depth scan to verify no drive-by download, trojan, or keylogger was dropped."""
        return sanitize_response(resp)

    # 11. Email Authentication (SPF, DKIM, DMARC)
    if any(k in q_lower for k in ["spf", "dkim", "dmarc", "authentication", "headers", "ప్రామాణీకరణ", "ప్రోటోకాల్", "प्रमाणीकरण"]):
        if target_lang == "te":
            resp = """### ఈమెయిల్ ప్రామాణీకరణ ప్రోటోకాల్‌లు (SPF, DKIM, DMARC):

1. **SPF (Sender Policy Framework)**:
   - ఒక డొమైన్ తరపున ఈమెయిల్‌లు పంపడానికి ఏ సర్వర్‌లు/IP లకు అధికారం ఉందో DNS రికార్డు ద్వారా నిర్వచిస్తుంది.
2. **DKIM (DomainKeys Identified Mail)**:
   - ఈమెయిల్ మార్గంలో ఎవరూ సవరించలేదని నిర్ధారించడానికి డిజిటల్ క్రిప్టోగ్రాఫిక్ సంతకాన్ని జోడిస్తుంది.
3. **DMARC (Domain-based Message Authentication)**:
   - SPF మరియు DKIM విఫలమైనప్పుడు స్వీకరించే మెయిల్ సర్వర్ ఏమి చేయాలి (`none`, `quarantine`, లేదా `reject`) అని నిర్దేశిస్తుంది.

**పరిశీలన పద్ధతి:** ThreatLens లోని **Email Analyzer** టూల్ ద్వారా ఈ మూడు ప్రమాణాలను తక్షణమే ధృవీకరించవచ్చు."""
        elif target_lang == "hi":
            resp = """### ईमेल प्रमाणीकरण प्रोटोकॉल (SPF, DKIM, DMARC):

1. **SPF (Sender Policy Framework)**:
   - DNS रिकॉर्ड के माध्यम से निर्दिष्ट करता है कि किसी डोमेन की ओर से कौन से IP ईमेल भेजने के लिए अधिकृत हैं।
2. **DKIM (DomainKeys Identified Mail)**:
   - ईमेल में एक क्रिप्टोग्राफ़िक हस्ताक्षर जोड़ता है जिससे यह सुनिश्चित होता है कि ट्रांजिट के दौरान संदेश से छेड़छाड़ नहीं की गई है।
3. **DMARC (Domain-based Message Authentication)**:
   - यह नीति निर्धारित करता है कि SPF या DKIM विफल होने पर ईमेल को रिजेक्ट (Reject) करना है या क्वारंटाइन (Quarantine)।

**उपयोग:** ThreatLens के **Email Analyzer** में हेडर पेस्ट करके तुरंत जांचें।"""
        else:
            resp = """### Email Authentication Standards: SPF, DKIM, & DMARC:

1. **SPF (Sender Policy Framework - RFC 7208)**:
   - A DNS TXT record declaring authorized IP addresses permitted to send mail for a specific domain.
2. **DKIM (DomainKeys Identified Mail - RFC 6376)**:
   - Adds an asymmetric cryptographic signature to email headers, verifying message body integrity in transit.
3. **DMARC (RFC 7489)**:
   - Enforces alignment between the SPF/DKIM domain and the RFC 5322 header `From:` address. Policies include `none`, `quarantine`, and `reject`.

**ThreatLens Integration:** You can paste email headers into the ThreatLens **Email Analyzer** to validate SPF, DKIM, and DMARC alignment."""
        return sanitize_response(resp)

    # 12. Password Security & MFA
    if any(k in q_lower for k in ["password", "mfa", "2fa", "two-factor", "passphrase", "పాస్‌వర్డ్", "పాస్వర్డ్", "पासवर्ड"]):
        if target_lang == "te":
            resp = """### బలమైన పాస్‌వర్డ్‌లు మరియు MFA ఉత్తమ పద్ధతులు:

1. **పొడవు ముఖ్యం (16+ అక్షరాలు)**: సంక్లిష్టత కంటే పాస్‌వర్డ్ పొడవు బ్రూట్-ఫోర్స్ దాడులను సమర్థవంతంగా అడ్డుకుంటుంది.
2. **పాస్‌ఫ్రేజ్ ఉపయోగించండి**: గుర్తుంచుకోవడానికి సులువైన 4-5 పదాల కలయికను వాడండి (ఉదా. `BlueFalconJumpsOver98!`).
3. **పాస్‌వర్డ్ మేనేజర్‌లు**: Bitwarden లేదా 1Password వంటి మేనేజర్లను ఉపయోగించండి.
4. **ఫిషింగ్-రెసిస్టెంట్ MFA**: SMS బదులు TOTP యాప్‌లు (Google Authenticator) లేదా FIDO2/YubiKey హార్డ్‌వేర్ కీలను ఉపయోగించండి."""
        elif target_lang == "hi":
            resp = """### मजबूत पासवर्ड और बहु-कारक प्रमाणीकरण (MFA):

1. **पासफ़्रेज़ का प्रयोग करें**: जटिल अक्षरों के बजाय 4-5 याद रखने योग्य शब्दों का संयोजन बनाएं।
2. **लंबाई सबसे महत्वपूर्ण है**: पासवर्ड कम से कम 14-16 वर्णों का होना चाहिए।
3. **पासवर्ड दोबारा न दोहराएं**: प्रत्येक खाते के लिए अलग और अद्वितीय पासवर्ड बनाएं।
4. **हार्डवेयर आधारित MFA**: SMS ओटीपी के स्थान पर FIDO2 या ऑथेंटिकेटर ऐप्स का उपयोग करें।"""
        else:
            resp = """### Enterprise Credential Security & MFA Architecture:

1. **Passphrase Philosophy**: 16+ character passphrases constructed from 4-5 non-contiguous words provide exponential entropy against GPU-based offline cracking.
2. **Zero Password Reuse**: Dedicated enterprise password managers prevent credential stuffing attacks.
3. **Phishing-Resistant MFA**: Transition from SMS verification to FIDO2 / WebAuthn hardware security keys (e.g., YubiKey) or TOTP authenticator apps."""
        return sanitize_response(resp)

    # 13. ThreatLens Platform Capabilities
    if any(k in q_lower for k in ["threatlens", "platform", "features", "how to use", "dashboard", "ప్లాట్‌ఫారమ్", "ప్లాట్ఫారమ్", "ఫీచర్లు", "टूल", "फीचर्स"]):
        if target_lang == "te":
            resp = """### ThreatLens ప్లాట్‌ఫారమ్ మార్గదర్శిని:

- **Chat with ThreatLens (ఈ చాట్)**: సైబర్‌ సెక్యూరిటీ సందేహాలు, ముప్పుల విశ్లేషణ మరియు రక్షణ సూచనల కోసం ఏఐ అసిస్టెంట్.
- **Email Analyzer**: అనుమానాస్పద ఈమెయిల్ హెడర్‌లు మరియు లింక్‌లను పేస్ట్ చేసి నిజ సమయంలో ఫిషింగ్ స్కోర్ లెక్కించండి.
- **Security Awareness**: ఉద్యోగుల కోసం ఇంటరాక్టివ్ సైబర్‌ సెక్యూరిటీ గేమిఫైడ్ శిక్షణ మాడ్యూల్స్.
- **Overview Dashboard**: రియల్-టైమ్ భద్రతా కొలమానాలు మరియు అవగాహన నివేదికలు.
- **System Management (అడ్మిన్ల కోసం)**: సిస్టమ్ హెల్త్, ఫ్లాగ్ చేయబడిన ఈమెయిల్‌లు మరియు యూజర్ డైరెక్టరీ నిర్వహణ."""
        elif target_lang == "hi":
            resp = """### ThreatLens प्लेटफ़ॉर्म अवलोकन:

- **Chat with ThreatLens (यह चैट)**: साइबर सुरक्षा मार्गदर्शन और रीयल-टाइम सलाह के लिए आपका सहायक।
- **Email Analyzer**: संदिग्ध ईमेल हेडर और सामग्री को स्कैन करके तुरंत सुरक्षा मूल्यांकन प्राप्त करें।
- **Security Awareness**: कर्मचारियों के लिए इंटरएक्टिव साइबर जागरूकता प्रशिक्षण मॉड्यूल।
- **Overview Dashboard**: रीयल-टाइम सुरक्षा मेट्रिक्स और विश्लेषण रिपोर्ट।
- **System Management (व्यवस्थापक)**: सिस्टम स्वास्थ्य, फ़्लैग किए गए ईमेल और उपयोगकर्ता निर्देशिका।"""
        else:
            resp = """### ThreatLens Platform Capabilities:

- **Chat with ThreatLens (Active Session)**: AI-driven cybersecurity assistant for threat analysis, security hygiene, and procedural advice.
- **Email Analyzer**: Inspect headers, sender reputation, and embedded URLs with real-time heuristic scoring.
- **Security Awareness**: Interactive modules to test and improve employee vigilance against social engineering.
- **Overview Dashboard**: Real-time organizational risk posture, open tracking, and simulation analytics.
- **System Management (Administrators)**: Live Firebase RTDB health, flagged threat intelligence, and user provisioning."""
        return sanitize_response(resp)

    # 14. Dynamic Intelligent Reasoning for General Queries
    if target_lang == "te":
        resp = f"""### ThreatLens సైబర్‌ సెక్యూరిటీ విశ్లేషణ:

మీ ప్రశ్న: **"{query}"**

1. **భద్రతా సూత్రం**: ఆధునిక సైబర్‌ భద్రత 'జీరో ట్రస్ట్' (Zero Trust - ఎవరినీ గుడ్డిగా నమ్మవద్దు, ఎల్లప్పుడూ ధృవీకరించండి) సిద్ధాంతంపై ఆధారపడి ఉంటుంది.
2. **ప్రమాద నివారణ**: బాహ్య సమాచార మార్పిడి, ఈమెయిల్‌లు మరియు వెబ్ అప్లికేషన్‌లలో ఇన్‌పుట్ ధృవీకరణ మరియు క్రమం తప్పని భద్రతా ఆడిట్‌లు తప్పనిసరి.
3. **ఆచరణాత్మక మార్గదర్శకత్వం**: మీ సంస్థలో డేటా రక్షణ కోసం బలమైన ఎన్‌క్రిప్షన్ (AES-256), మల్టీ-ఫ్యాక్టర్ ప్రామాణీకరణ (MFA) మరియు తాజా సెక్యూరిటీ ప్యాచ్‌లను అమలు చేయండి.

మరింత నిర్దిష్ట సమాచారం లేదా ఇతర సాంకేతిక ప్రశ్నల కోసం అడగండి!"""
    elif target_lang == "hi":
        resp = f"""### ThreatLens साइबर सुरक्षा विश्लेषण:

आपका प्रश्न: **"{query}"**

1. **सुरक्षा का मूल सिद्धांत**: आधुनिक साइबर सुरक्षा 'ज़ीरो ट्रस्ट' (Zero Trust - कभी भरोसा न करें, हमेशा सत्यापित करें) के सिद्धांत पर कार्य करती है।
2. **जोखिम रोकथाम**: किसी भी अनपेक्षित संचार, बाहरी लिंक या डेटा ट्रांसमिशन को हमेशा बहु-चरणीय सत्यापन के माध्यम से जांचें।
3. **व्यावहारिक सुरक्षा कदम**: संवेदनशील डेटा के लिए मजबूत एन्क्रिप्शन (AES-256), सुरक्षित बैकअप और नियमित सुरक्षा ऑडिट का उपयोग करें।

आप किसी भी विशिष्ट साइबर सुरक्षा विषय के बारे में आगे पूछ सकते हैं!"""
    else:
        resp = f"""### ThreatLens Security Intelligence:

Regarding your query on: **"{query}"**

1. **Foundational Security Posture**: Enterprise resilience relies on the **Zero Trust Architecture** ("Never Trust, Always Verify"), ensuring strict identity verification across all access requests.
2. **Threat Surface & Mitigation**: Regularly audit endpoint exposures, enforce principle of least privilege, and inspect inbound telemetry through the ThreatLens platform.
3. **Best Practice Guidance**: Implement multi-layered Defense-in-Depth, enforce MFA, maintain offline backups, and educate operators using ThreatLens awareness drills.

Feel free to ask follow-up questions regarding specific technical implementations, attack vectors, or platform workflows!"""

    return sanitize_response(resp)
