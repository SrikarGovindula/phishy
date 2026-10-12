import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=1, # Center
        textColor=colors.HexColor('#0f172a')
    )
    
    sub_title_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=1, # Center
        textColor=colors.HexColor('#64748b')
    )
    
    urgent_style = ParagraphStyle(
        'UrgentText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#991b1b')
    )
    
    sec_heading_style = ParagraphStyle(
        'SecHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.white
    )
    
    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1e3a8a')
    )
    
    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0f172a')
    )
    
    cell_text = ParagraphStyle(
        'CellText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor('#334155')
    )
    
    cell_contact = ParagraphStyle(
        'CellContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor('#1d4ed8')
    )

    notice_style = ParagraphStyle(
        'NoticeStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor('#475569')
    )
    
    story = []
    
    # Title
    story.append(Paragraph("<b>Cybersecurity • Enterprise Security • Financial Security</b>", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("India — Official Portals & Helpline Numbers | Quick Reference Sheet", sub_title_style))
    story.append(Spacer(1, 8))
    
    # Urgent banner
    urgent_html = "<b>URGENT CYBER / FINANCIAL FRAUD:</b> If money has been lost or an online financial fraud has just occurred, call <b>1930</b> immediately and file the complaint on the <b>National Cyber Crime Reporting Portal</b>."
    urgent_table = Table([[Paragraph(urgent_html, urgent_style)]], colWidths=[523])
    urgent_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fef2f2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#fca5a5')),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(urgent_table)
    story.append(Spacer(1, 9))
    
    def make_section_header(title):
        t = Table([[Paragraph(f"<b>{title}</b>", sec_heading_style)]], colWidths=[523])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1e40af')),
            ('PADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        return t

    # SECTION 1
    story.append(make_section_header("1. CYBERSECURITY — Individuals & General Cyber Crime"))
    data1 = [
        [Paragraph("<b>Portal / Service</b>", th_style), Paragraph("<b>Use for</b>", th_style), Paragraph("<b>Official link / contact</b>", th_style)],
        [
            Paragraph("<b>National Cyber Crime Reporting Portal (I4C / MHA)</b>", cell_bold),
            Paragraph("Report cybercrime, phishing, online fraud, suspicious URLs/numbers and track complaints.", cell_text),
            Paragraph("<b>cybercrime.gov.in</b><br/>Helpline: <b>1930</b> (24×7)", cell_contact)
        ],
        [
            Paragraph("<b>Report Suspect — I4C</b>", cell_bold),
            Paragraph("Report suspicious website URLs, phone numbers, email IDs, SMS headers/numbers, WhatsApp/Telegram handles and social-media URLs.", cell_text),
            Paragraph("<b>Report Suspect portal</b><br/><b>1930</b> if you are a victim.", cell_contact)
        ],
        [
            Paragraph("<b>Sanchar Saathi — Chakshu</b>", cell_bold),
            Paragraph("Report suspected fraudulent communications received through calls, SMS or WhatsApp.", cell_text),
            Paragraph("<b>Sanchar Saathi / Chakshu</b><br/>Actual financial cyber fraud: <b>1930</b>", cell_contact)
        ],
        [
            Paragraph("<b>National Emergency / Police</b>", cell_bold),
            Paragraph("Emergency or crimes other than cybercrime.", cell_text),
            Paragraph("<b>112</b> — National Police / Emergency Helpline", cell_contact)
        ],
    ]
    t1 = Table(data1, colWidths=[140, 233, 150])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e0e7ff')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t1)
    story.append(Spacer(1, 9))

    # SECTION 2
    story.append(make_section_header("2. ENTERPRISE SECURITY — Organizations & Security Teams"))
    data2 = [
        [Paragraph("<b>Organization</b>", th_style), Paragraph("<b>Use for</b>", th_style), Paragraph("<b>Official link / contact</b>", th_style)],
        [
            Paragraph("<b>CERT-In — Indian Computer Emergency Response Team</b>", cell_bold),
            Paragraph("Cybersecurity incident reporting, security alerts, vulnerability reporting and technical cybersecurity queries.", cell_text),
            Paragraph("<b>cert-in.org.in</b><br/>Incident Helpdesk: +91-1800-11-4949<br/>incident@cert-in.org.in<br/>info@cert-in.org.in", cell_contact)
        ],
        [
            Paragraph("<b>CERT-In Incident Reporting</b>", cell_bold),
            Paragraph("Use when an organization needs to report a cyber security incident to CERT-In.", cell_text),
            Paragraph("+91-1800-11-4949<br/>incident@cert-in.org.in<br/>+91-11-22902657", cell_contact)
        ],
        [
            Paragraph("<b>CERT-In Vulnerability Disclosure</b>", cell_bold),
            Paragraph("Report vulnerabilities and collaborate with CERT-In on cybersecurity matters.", cell_text),
            Paragraph("vdisclose@cert-in.org.in<br/><b>cert-in.org.in</b>", cell_contact)
        ],
    ]
    t2 = Table(data2, colWidths=[140, 233, 150])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e0e7ff')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t2)
    story.append(Spacer(1, 9))

    # SECTION 3
    story.append(make_section_header("3. FINANCIAL SECURITY — Banking, Securities & Insurance"))
    data3 = [
        [Paragraph("<b>Regulator / Portal</b>", th_style), Paragraph("<b>Use for</b>", th_style), Paragraph("<b>Official link / helpline</b>", th_style)],
        [
            Paragraph("<b>RBI — Complaint Management System (CMS)</b>", cell_bold),
            Paragraph("Complaints against RBI-regulated entities and Ombudsman-related grievance redressal.", cell_text),
            Paragraph("<b>cms.rbi.org.in</b><br/>RBI Contact Centre: <b>14448</b>", cell_contact)
        ],
        [
            Paragraph("<b>SEBI — SCORES</b>", cell_bold),
            Paragraph("Investor grievances involving SEBI-regulated entities such as listed companies, registered intermediaries and market infrastructure institutions.", cell_text),
            Paragraph("<b>scores.sebi.gov.in</b><br/>1800 266 7575 / 1800 22 7575<br/>(9:00 AM–6:00 PM, ex. holidays)", cell_contact)
        ],
        [
            Paragraph("<b>IRDAI — Bima Bharosa</b>", cell_bold),
            Paragraph("Insurance policyholder complaints and grievance redressal.", cell_text),
            Paragraph("<b>bimabharosa.irdai.gov.in</b><br/>155255 / 1800 4254 732<br/>complaints@irdai.gov.in", cell_contact)
        ],
        [
            Paragraph("<b>National Cyber Crime Portal — Financial Cyber Fraud</b>", cell_bold),
            Paragraph("Immediate reporting of online financial fraud / cyber financial fraud.", cell_text),
            Paragraph("<b>cybercrime.gov.in</b><br/><b>1930</b> — 24×7", cell_contact)
        ],
    ]
    t3 = Table(data3, colWidths=[140, 233, 150])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e0e7ff')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t3)
    story.append(Spacer(1, 9))

    # SECTION 4: Quick decision guide
    story.append(make_section_header("Quick decision guide"))
    data4 = [
        [Paragraph("<b>Situation</b>", th_style), Paragraph("<b>Contact first</b>", th_style)],
        [
            Paragraph("<b>Money lost / UPI, card, bank or online financial fraud</b>", cell_bold),
            Paragraph("<b>1930 immediately + cybercrime.gov.in</b>; then contact your bank/payment provider.", cell_text)
        ],
        [
            Paragraph("<b>Phishing link, suspicious phone/SMS/WhatsApp/email or cybercrime</b>", cell_bold),
            Paragraph("<b>cybercrime.gov.in / 1930</b>; use <b>Chakshu</b> for suspected fraud communications.", cell_text)
        ],
        [
            Paragraph("<b>Company / enterprise cyber incident</b>", cell_bold),
            Paragraph("<b>CERT-In: 1800-11-4949</b> and <b>incident@cert-in.org.in</b>; follow your internal incident-response process.", cell_text)
        ],
        [
            Paragraph("<b>Banking complaint not resolved by the regulated entity</b>", cell_bold),
            Paragraph("<b>RBI CMS — cms.rbi.org.in / 14448</b>.", cell_text)
        ],
        [
            Paragraph("<b>Securities / investment grievance</b>", cell_bold),
            Paragraph("<b>SEBI SCORES / 1800 266 7575</b> or <b>1800 22 7575</b>.", cell_text)
        ],
        [
            Paragraph("<b>Insurance grievance</b>", cell_bold),
            Paragraph("<b>Bima Bharosa / 155255</b> or <b>1800 4254 732</b>.", cell_text)
        ],
    ]
    t4 = Table(data4, colWidths=[200, 323])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e0e7ff')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t4)
    story.append(Spacer(1, 8))

    # Notes
    safety_text = "<b>Safety reminder:</b> Use only official government/regulator portals shown here. Never share OTPs, PINs, passwords, CVV, UPI PINs or remote-access credentials with a caller claiming to be from a bank, regulator or cyber cell."
    story.append(Paragraph(safety_text, notice_style))
    story.append(Spacer(1, 4))
    
    src_text = "<b>Sources verified from official Government of India / regulator websites:</b> I4C National Cyber Crime Reporting Portal, CERT-In, RBI, SEBI and IRDAI. Contact details can change; verify the official portal before relying on a number."
    story.append(Paragraph(src_text, notice_style))

    doc.build(story)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    out_dir = r"c:\Users\srika\Desktop\Phishy\Phishy-master\frontend"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "helpline-quick-reference-sheet.pdf")
    build_pdf(out_path)
