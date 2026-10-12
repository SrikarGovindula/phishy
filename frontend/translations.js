/**
 * ThreatLens Multi-Lingual Localization Engine
 * Supported Languages: English (en), Hindi (hi), Telugu (te)
 */

const THREATLENS_TRANSLATIONS = {
    en: {
        // App / Brand
        brandTitle: "ThreatLens",
        roleAdmin: "Administrator",
        roleUser: "Security User",
        roleGuest: "Guest",
        accessDenied: "Access Restricted: This section is reserved for Administrators.",

        // Sidebar Groups & Items
        chatInterfaceGroup: "CHAT INTERFACE",
        chatNavItem: "Chat with ThreatLens",
        securityAwarenessGroup: "SECURITY AWARENESS",
        awarenessNavItem: "Awareness Modules",
        aiToolsGroup: "AI THREAT TOOLS",
        emailAnalyzerNavItem: "Email Analyzer",
        analyticsInsightsGroup: "ANALYTICS & INSIGHTS",
        overviewDashboardNavItem: "Overview Dashboard",
        emailTrackingNavItem: "Email Tracking",
        activityLogsNavItem: "Activity Logs",
        riskAssessmentNavItem: "Risk Assessment",
        systemManagementGroup: "SYSTEM MANAGEMENT",
        systemHealthNavItem: "System Health",
        flaggedEmailsNavItem: "Flagged Emails",
        userManagementNavItem: "User Directory",
        helplineNumbersGroup: "HELPLINE NUMBERS",
        helplineNavItem: "Official Helpline Reference Sheet",

        // Header
        statusPlatformReady: "Platform Ready",
        loginBtn: "Login",
        logoutBtn: "Logout",
        clearBtn: "Clear View",
        refreshBtn: "Refresh Data",
        apiDocsBtn: "API Docs",

        // Chat Screen
        chatWelcomeTitle: "ThreatLens Intelligence Assistant",
        chatWelcomeGreeting: "Enterprise cybersecurity assistant ready to investigate threat indicators, verify phishing markers, and inspect real simulation telemetry.",
        chatWelcomeCap1: "Evaluate phishing markers and domain spoofing in incoming emails",
        chatWelcomeCap2: "Analyze SPF, DKIM, and DMARC technical authentication",
        chatWelcomeCap3: "Query live simulation clicks and vulnerable user telemetry",
        chatWelcomeCap4: "Provide actionable incident response procedures and password hygiene",
        chatInputPlaceholder: "Ask ThreatLens about phishing detection, security protocols, or live click logs...",
        chatSendBtn: "Send",
        chatQuickPrompt1: "How to identify phishing emails?",
        chatQuickPrompt2: "What are SPF, DKIM, and DMARC?",
        chatQuickPrompt3: "Steps if I clicked a phishing link?",
        chatQuickPrompt4: "Show recent simulation click activity",

        // Dashboard Stats
        statTotalClicks: "Total Clicks",
        statUniqueUsers: "Unique Victims",
        statAvgRisk: "Average Risk Level",
        statTrainingSuccess: "Training Success",
        statTotalOpens: "Total Email Opens",
        statOpenRate: "Open Rate",
        userPortalBadge: "Employee Security Portal",
        userPortalDesc: "Your security awareness overview, training progress, and defense drills.",
        adminPortalBadge: "Enterprise SOC Admin Dashboard",
        adminPortalDesc: "Real-time organization threat metrics, telemetry streams, and administrative controls.",
        chartTitleActivity: "Click Activity Over Time",
        chartTitleUserSummary: "User Click Summary",
        reportGenerationTitle: "Professional Report Generation",
        reportTitleLabel: "Report Title",
        reportPeriodLabel: "Report Period",
        reportFormatLabel: "Report Format",
        generateReportBtn: "Generate Professional Report",
        downloadReportBtn: "Download PDF",

        // Email Analyzer
        analyzerTitle: "Enterprise Email Threat Analyzer",
        analyzerDesc: "Analyze email headers and message body for deceptive links, spoofed senders, and high-risk indicators.",
        analyzerPlaceholder: "Paste full email headers or message content here for deep security analysis...",
        analyzeEmailBtn: "Analyze Email",

        // Modals & Common
        loginTitle: "ThreatLens Account Authentication",
        registerTitle: "Register ThreatLens Account",
        emailPlaceholder: "name@company.com",
        passwordPlaceholder: "Enter password",
        closeModal: "Close",
        privacyPolicyLink: "Privacy Policy",
        termsConditionsLink: "Terms & Conditions"
    },

    hi: {
        // App / Brand
        brandTitle: "ThreatLens",
        roleAdmin: "व्यवस्थापक (Admin)",
        roleUser: "सुरक्षा उपयोगकर्ता (User)",
        roleGuest: "अतिथि (Guest)",
        accessDenied: "पहुंच प्रतिबंधित: यह अनुभाग केवल व्यवस्थापकों (Administrators) के लिए आरक्षित है।",

        // Sidebar Groups & Items
        chatInterfaceGroup: "चैट इंटरफ़ेस",
        chatNavItem: "ThreatLens से चैट करें",
        securityAwarenessGroup: "सुरक्षा जागरूकता",
        awarenessNavItem: "जागरूकता मॉड्यूल",
        aiToolsGroup: "AI सुरक्षा उपकरण",
        emailAnalyzerNavItem: "ईमेल विश्लेषक",
        analyticsInsightsGroup: "विश्लेषण और अंतर्दृष्टि",
        overviewDashboardNavItem: "अवलोकन डैशबोर्ड",
        emailTrackingNavItem: "ईमेल ट्रैकिंग",
        activityLogsNavItem: "गतिविधि लॉग",
        riskAssessmentNavItem: "जोखिम मूल्यांकन",
        systemManagementGroup: "सिस्टम प्रबंधन",
        systemHealthNavItem: "सिस्टम स्थिति",
        flaggedEmailsNavItem: "फ़्लैग किए गए ईमेल",
        userManagementNavItem: "उपयोगकर्ता निर्देशिका",
        helplineNumbersGroup: "हेल्पलाइन नंबर",
        helplineNavItem: "आधिकारिक हेल्पलाइन संदर्भ पत्र",

        // Header
        statusPlatformReady: "प्लेटफ़ॉर्म तैयार है",
        loginBtn: "लॉग इन करें",
        logoutBtn: "लॉग आउट",
        clearBtn: "दृश्य साफ़ करें",
        refreshBtn: "डेटा रीफ़्रेश करें",
        apiDocsBtn: "API दस्तावेज़",

        // Chat Screen
        chatWelcomeTitle: "ThreatLens सुरक्षा बुद्धिमत्ता सहायक",
        chatWelcomeGreeting: "उद्यम साइबर सुरक्षा सहायक खतरे के संकेतों की जांच, फ़िशिंग मार्करों की पहचान और वास्तविक सिमुलेशन टेलीमेट्री की समीक्षा के लिए तैयार है।",
        chatWelcomeCap1: "आने वाले संदेशों में फ़िशिंग मार्कर और डोमेन स्पूफिंग की पहचान करें",
        chatWelcomeCap2: "SPF, DKIM और DMARC तकनीकी प्रमाणीकरण मानकों का विश्लेषण करें",
        chatWelcomeCap3: "वास्तविक सिमुलेशन क्लिक और प्रभावित उपयोगकर्ताओं का डेटा देखें",
        chatWelcomeCap4: "घटना प्रतिक्रिया (Incident Response) और पासवर्ड सुरक्षा के लिए तत्काल मार्गदर्शन प्राप्त करें",
        chatInputPlaceholder: "फ़िशिंग पहचान, सुरक्षा प्रोटोकॉल या क्लिक लॉग के बारे में ThreatLens से पूछें...",
        chatSendBtn: "भेजें",
        chatQuickPrompt1: "फ़िशिंग ईमेल की पहचान कैसे करें?",
        chatQuickPrompt2: "SPF, DKIM और DMARC क्या हैं?",
        chatQuickPrompt3: "फ़िशिंग लिंक पर क्लिक करने पर क्या करें?",
        chatQuickPrompt4: "हाल के सिमुलेशन क्लिक डेटा दिखाएं",

        // Dashboard Stats
        statTotalClicks: "कुल क्लिक",
        statUniqueUsers: "प्रभावित उपयोगकर्ता",
        statAvgRisk: "औसत जोखिम स्तर",
        statTrainingSuccess: "प्रशिक्षण सफलता",
        statTotalOpens: "कुल ईमेल ओपन",
        statOpenRate: "ओपन दर",
        userPortalBadge: "कर्मचारी सुरक्षा पोर्टल",
        userPortalDesc: "आपकी सुरक्षा जागरूकता रिपोर्ट, प्रशिक्षण प्रगति और सुरक्षा अभ्यास।",
        adminPortalBadge: "एंटरप्राइज़ SOC एडमिन डैशबोर्ड",
        adminPortalDesc: "रीयल-टाइम संगठनात्मक खतरे के आँकड़े, टेलीमेट्री स्ट्रीम और प्रशासनिक नियंत्रण।",
        chartTitleActivity: "समय के साथ क्लिक गतिविधि",
        chartTitleUserSummary: "उपयोगकर्ता क्लिक सारांश",
        reportGenerationTitle: "पेशेवर सुरक्षा रिपोर्ट निर्माण",
        reportTitleLabel: "रिपोर्ट शीर्षक",
        reportPeriodLabel: "रिपोर्ट अवधि",
        reportFormatLabel: "रिपोर्ट प्रारूप",
        generateReportBtn: "पेशेवर रिपोर्ट बनाएं",
        downloadReportBtn: "PDF डाउनलोड करें",

        // Email Analyzer
        analyzerTitle: "उद्यम ईमेल खतरा विश्लेषक",
        analyzerDesc: "संदिग्ध लिंक, नकली प्रेषक और उच्च जोखिम वाले संकेतों के लिए ईमेल हेडर और संदेश का विश्लेषण करें।",
        analyzerPlaceholder: "गहन सुरक्षा विश्लेषण के लिए पूरे ईमेल हेडर या संदेश को यहां चिपकाएं...",
        analyzeEmailBtn: "ईमेल का विश्लेषण करें",

        // Modals & Common
        loginTitle: "ThreatLens खाता प्रमाणीकरण",
        registerTitle: "ThreatLens खाता पंजीकरण",
        emailPlaceholder: "name@company.com",
        passwordPlaceholder: "पासवर्ड दर्ज करें",
        closeModal: "बंद करें",
        privacyPolicyLink: "गोपनीयता नीति",
        termsConditionsLink: "नियम और शर्तें"
    },

    te: {
        // App / Brand
        brandTitle: "ThreatLens",
        roleAdmin: "అడ్మినిస్ట్రేటర్ (Admin)",
        roleUser: "భద్రతా వినియోగదారు (User)",
        roleGuest: "అతిథి (Guest)",
        accessDenied: "యాక్సెస్ పరిమితం: ఈ విభాగం కేవలం నిర్వాహకులకు (Administrators) మాత్రమే అందుబాటులో ఉంది.",

        // Sidebar Groups & Items
        chatInterfaceGroup: "చాట్ ఇంటర్‌ఫేస్",
        chatNavItem: "ThreatLens తో చాట్",
        securityAwarenessGroup: "భద్రతా అవగాహన",
        awarenessNavItem: "అవగాహన మాడ్యూల్స్",
        aiToolsGroup: "AI ముప్పు సాధనాలు",
        emailAnalyzerNavItem: "ఈమెయిల్ విశ్లేషకం",
        analyticsInsightsGroup: "విశ్లేషణలు & అంతర్దృష్టులు",
        overviewDashboardNavItem: "డ్యాష్‌బోర్డ్ వివరణ",
        emailTrackingNavItem: "ఈమెయిల్ ట్రాకింగ్",
        activityLogsNavItem: "కార్యాచరణ లాగ్‌లు",
        riskAssessmentNavItem: "రిస్క్ అసెస్‌మెంట్",
        systemManagementGroup: "సిస్టమ్ నిర్వహణ",
        systemHealthNavItem: "సిస్టమ్ ఆరోగ్యం",
        flaggedEmailsNavItem: "ఫ్లాగ్ చేయబడిన ఈమెయిల్‌లు",
        userManagementNavItem: "వినియోగదారుల డైరెక్టరీ",
        helplineNumbersGroup: "హెల్ప్‌లైన్ నంబర్లు",
        helplineNavItem: "అధికారిక హెల్ప్‌లైన్ రెఫరెన్స్ షీట్",

        // Header
        statusPlatformReady: "ప్లాట్‌ఫారమ్ సిద్ధంగా ఉంది",
        loginBtn: "లాగిన్",
        logoutBtn: "లాగ్ అవుట్",
        clearBtn: "స్క్రీన్ క్లియర్",
        refreshBtn: "డేటా రీఫ్రెష్",
        apiDocsBtn: "API డాక్స్",

        // Chat Screen
        chatWelcomeTitle: "ThreatLens సైబర్‌ సెక్యూరిటీ అసిస్టెంట్",
        chatWelcomeGreeting: "ముప్పు సంకేతాలను గుర్తించడం, ఫిషింగ్ మార్కర్లను విశ్లేషించడం మరియు ప్రత్యక్ష సిమ్యులేషన్ టెలిమెట్రీని తనిఖీ చేయడానికి సిద్ధంగా ఉన్న ఎంటర్‌ప్రైజ్ అసిస్టెంట్.",
        chatWelcomeCap1: "ఇన్‌కమింగ్ ఈమెయిల్స్‌లో ఫిషింగ్ గుర్తులు మరియు డొమైన్ స్పూఫింగ్‌ను గుర్తించండి",
        chatWelcomeCap2: "SPF, DKIM మరియు DMARC సాంకేతిక ప్రమాణాలను విశ్లేషించండి",
        chatWelcomeCap3: "ప్రత్యక్ష సిమ్యులేషన్ క్లిక్‌లు మరియు ప్రభావిత వినియోగదారుల డేటాను సమీక్షించండి",
        chatWelcomeCap4: "ఇన్సిడెంట్ రెస్పాన్స్ మరియు పాస్‌వర్డ్ భద్రతపై స్పష్టమైన మార్గదర్శకత్వం పొందండి",
        chatInputPlaceholder: "ఫిషింగ్ గుర్తింపు, సెక్యూరిటీ ప్రోటోకాల్స్ లేదా క్లిక్ లాగ్స్ గురించి ThreatLens ను అడగండి...",
        chatSendBtn: "పంపు",
        chatQuickPrompt1: "ఫిషింగ్ ఈమెయిల్‌ను గుర్తించడం ఎలా?",
        chatQuickPrompt2: "SPF, DKIM మరియు DMARC అంటే ఏమిటి?",
        chatQuickPrompt3: "ఫిషింగ్ లింక్‌పై క్లిక్ చేస్తే ఏమి చేయాలి?",
        chatQuickPrompt4: "ఇటీవలి సిమ్యులేషన్ క్లిక్ డేటాను చూపించు",

        // Dashboard Stats
        statTotalClicks: "మొత్తం క్లిక్‌లు",
        statUniqueUsers: "బాధిత వినియోగదారులు",
        statAvgRisk: "సగటు రిస్క్ స్థాయి",
        statTrainingSuccess: "శిక్షణ విజయం",
        statTotalOpens: "మొత్తం ఈమెయిల్ ఓపెన్‌లు",
        statOpenRate: "ఓపెన్ రేటు",
        userPortalBadge: "ఉద్యోగుల భద్రతా పోర్టల్",
        userPortalDesc: "మీ భద్రతా అవగాహన వివరాలు, శిక్షణ పురోగతి మరియు భద్రతా కసరత్తులు.",
        adminPortalBadge: "ఎంటర్‌ప్రైజ్ SOC అడ్మిన్ డ్యాష్‌బోర్డ్",
        adminPortalDesc: "రియల్-టైమ్ సంస్థాగత ముప్పు కొలమానాలు, టెలిమెట్రీ ప్రవాహం మరియు అడ్మినిస్ట్రేటివ్ నియంత్రణలు.",
        chartTitleActivity: "కాలక్రమేణా క్లిక్ కార్యాచరణ",
        chartTitleUserSummary: "వినియోగదారుల క్లిక్ సారాంశం",
        reportGenerationTitle: "ప్రొఫెషనల్ భద్రతా నివేదిక తయారీ",
        reportTitleLabel: "నివేదిక శీర్షిక",
        reportPeriodLabel: "నివేదిక కాల వ్యవధి",
        reportFormatLabel: "నివేదిక ఫార్మాట్",
        generateReportBtn: "ప్రొఫెషనల్ రిపోర్ట్ రూపొందించండి",
        downloadReportBtn: "PDF డౌన్‌లోడ్ చేయండి",

        // Email Analyzer
        analyzerTitle: "ఎంటర్‌ప్రైజ్ ఈమెయిల్ ముప్పు విశ్లేషకం",
        analyzerDesc: "మోసపూరిత లింక్‌లు, స్పూఫ్ చేయబడిన పంపినవారు మరియు ప్రమాదకర సూచికల కోసం ఈమెయిల్ హెడర్‌లు మరియు సందేశాన్ని విశ్లేషించండి.",
        analyzerPlaceholder: "లోతైన విశ్లేషణ కోసం పూర్తి ఈమెయిల్ హెడర్‌లు లేదా సందేశాన్ని ఇక్కడ అతికించండి...",
        analyzeEmailBtn: "ఈమెయిల్‌ను విశ్లేషించండి",

        // Modals & Common
        loginTitle: "ThreatLens ఖాతా ప్రమాణీకరణ",
        registerTitle: "ThreatLens ఖాతా నమోదు",
        emailPlaceholder: "name@company.com",
        passwordPlaceholder: "పాస్‌వర్డ్ నమోదు చేయండి",
        closeModal: "మూసివేయి",
        privacyPolicyLink: "గోప్యతా విధానం",
        termsConditionsLink: "నిబంధనలు మరియు షరతులు"
    }
};

/**
 * Global active language helper
 */
let currentLanguage = localStorage.getItem('threatlens_lang') || 'en';

function getI18nText(key) {
    const langDict = THREATLENS_TRANSLATIONS[currentLanguage] || THREATLENS_TRANSLATIONS.en;
    return langDict[key] || THREATLENS_TRANSLATIONS.en[key] || key;
}

function applyThreatLensLanguage(lang) {
    if (!['en', 'hi', 'te'].includes(lang)) lang = 'en';
    currentLanguage = lang;
    localStorage.setItem('threatlens_lang', lang);

    const t = THREATLENS_TRANSLATIONS[lang] || THREATLENS_TRANSLATIONS.en;

    // Update Language Dropdown
    const langSelect = document.getElementById('threatlensLanguageSelect');
    if (langSelect && langSelect.value !== lang) {
        langSelect.value = lang;
    }

    // Update Navigation Group Titles
    const elChatGroup = document.getElementById('chatInterfaceGroupTitle');
    if (elChatGroup) elChatGroup.textContent = t.chatInterfaceGroup;

    const elAwareGroup = document.getElementById('securityAwarenessGroupTitle');
    if (elAwareGroup) elAwareGroup.textContent = t.securityAwarenessGroup;

    const elAiGroup = document.getElementById('aiToolsGroupTitle');
    if (elAiGroup) elAiGroup.textContent = t.aiToolsGroup;

    const elAnalyticsGroup = document.getElementById('analyticsInsightsGroupTitle');
    if (elAnalyticsGroup) elAnalyticsGroup.textContent = t.analyticsInsightsGroup;

    const elSysGroup = document.getElementById('systemManagementGroupTitle');
    if (elSysGroup) elSysGroup.textContent = t.systemManagementGroup;

    // Update Nav Items
    const elChatNav = document.getElementById('chatNavItemText');
    if (elChatNav) elChatNav.textContent = t.chatNavItem;

    const elAwareNav = document.getElementById('awarenessNavItemText');
    if (elAwareNav) elAwareNav.textContent = t.awarenessNavItem;

    const elAnalyzerNav = document.getElementById('emailAnalyzerNavItemText');
    if (elAnalyzerNav) elAnalyzerNav.textContent = t.emailAnalyzerNavItem;

    const elOverviewNav = document.getElementById('overviewDashboardNavItemText');
    if (elOverviewNav) elOverviewNav.textContent = t.overviewDashboardNavItem;

    const elTrackingNav = document.getElementById('emailTrackingNavItemText');
    if (elTrackingNav) elTrackingNav.textContent = t.emailTrackingNavItem;

    const elLogsNav = document.getElementById('activityLogsNavItemText');
    if (elLogsNav) elLogsNav.textContent = t.activityLogsNavItem;

    const elRiskNav = document.getElementById('riskAssessmentNavItemText');
    if (elRiskNav) elRiskNav.textContent = t.riskAssessmentNavItem;

    const elHealthNav = document.getElementById('systemHealthNavItemText');
    if (elHealthNav) elHealthNav.textContent = t.systemHealthNavItem;

    const elFlaggedNav = document.getElementById('flaggedEmailsNavItemText');
    if (elFlaggedNav) elFlaggedNav.textContent = t.flaggedEmailsNavItem;

    const elUserNav = document.getElementById('userManagementNavItemText');
    if (elUserNav) elUserNav.textContent = t.userManagementNavItem;

    const elHelplineGroupTitle = document.getElementById('helplineNumbersGroupTitle');
    if (elHelplineGroupTitle) elHelplineGroupTitle.textContent = t.helplineNumbersGroup;

    const elHelplineNav = document.getElementById('helplineNavItemText');
    if (elHelplineNav) elHelplineNav.textContent = t.helplineNavItem;

    // Update Header Buttons
    const elLoginBtn = document.getElementById('loginBtn');
    if (elLoginBtn) elLoginBtn.textContent = t.loginBtn;

    const elLogoutBtn = document.getElementById('logoutBtn');
    if (elLogoutBtn) elLogoutBtn.textContent = t.logoutBtn;

    const elClearBtn = document.getElementById('clearHeaderBtn');
    if (elClearBtn) elClearBtn.textContent = t.clearBtn;

    const elRefreshBtn = document.getElementById('refreshHeaderBtn');
    if (elRefreshBtn) elRefreshBtn.textContent = t.refreshBtn;

    const elApiDocsBtn = document.getElementById('apiDocsHeaderBtn');
    if (elApiDocsBtn) elApiDocsBtn.textContent = t.apiDocsBtn;

    // Update Chat Screen
    const chatInput = document.getElementById('chatInput');
    if (chatInput) chatInput.placeholder = t.chatInputPlaceholder;

    const chatSendBtn = document.getElementById('chatSendBtn');
    if (chatSendBtn) chatSendBtn.title = t.chatSendBtn;

    const qp1 = document.getElementById('quickPrompt1');
    if (qp1) qp1.textContent = t.chatQuickPrompt1;

    const qp2 = document.getElementById('quickPrompt2');
    if (qp2) qp2.textContent = t.chatQuickPrompt2;

    const qp3 = document.getElementById('quickPrompt3');
    if (qp3) qp3.textContent = t.chatQuickPrompt3;

    const qp4 = document.getElementById('quickPrompt4');
    if (qp4) qp4.textContent = t.chatQuickPrompt4;

    // Update Overview Dashboard Stat Labels
    const l1 = document.getElementById('labelTotalClicks');
    if (l1) l1.textContent = t.statTotalClicks;

    const l2 = document.getElementById('labelUniqueUsers');
    if (l2) l2.textContent = t.statUniqueUsers;

    const l3 = document.getElementById('labelRiskScore');
    if (l3) l3.textContent = t.statAvgRisk;

    const l4 = document.getElementById('labelSuccessRate');
    if (l4) l4.textContent = t.statTrainingSuccess;

    const l5 = document.getElementById('labelTotalOpens');
    if (l5) l5.textContent = t.statTotalOpens;

    const l6 = document.getElementById('labelOpenRate');
    if (l6) l6.textContent = t.statOpenRate;

    // Portal Banners
    const ubTitle = document.getElementById('userBannerTitle');
    if (ubTitle) ubTitle.textContent = t.userPortalBadge;

    const ubDesc = document.getElementById('userBannerDesc');
    if (ubDesc) ubDesc.textContent = t.userPortalDesc;

    const abTitle = document.getElementById('adminBannerTitle');
    if (abTitle) abTitle.textContent = t.adminPortalBadge;

    const abDesc = document.getElementById('adminBannerDesc');
    if (abDesc) abDesc.textContent = t.adminPortalDesc;

    // Chart Titles & Reports
    const ct1 = document.getElementById('chartTitleActivity');
    if (ct1) ct1.textContent = t.chartTitleActivity;

    const ct2 = document.getElementById('chartTitleUserSummary');
    if (ct2) ct2.textContent = t.chartTitleUserSummary;

    const rt = document.getElementById('reportGenTitle');
    if (rt) rt.textContent = t.reportGenerationTitle;

    const genBtn = document.getElementById('generateReportBtn');
    if (genBtn) genBtn.textContent = t.generateReportBtn;

    // Email Analyzer Screen
    const eaTitle = document.getElementById('analyzerTitle');
    if (eaTitle) eaTitle.textContent = t.analyzerTitle;

    const eaDesc = document.getElementById('analyzerDesc');
    if (eaDesc) eaDesc.textContent = t.analyzerDesc;

    const eaInput = document.getElementById('emailContentInput');
    if (eaInput) eaInput.placeholder = t.analyzerPlaceholder;

    const eaBtn = document.getElementById('analyzeEmailBtn');
    if (eaBtn) eaBtn.textContent = t.analyzeEmailBtn;

    // Footer Links
    const privLink = document.getElementById('privacyPolicyLink');
    if (privLink) privLink.textContent = t.privacyPolicyLink;

    const termLink = document.getElementById('termsConditionsLink');
    if (termLink) termLink.textContent = t.termsConditionsLink;

    // Refresh dynamic user badge if auth loaded
    if (typeof updateAuthUI === 'function') {
        updateAuthUI();
    }
}
