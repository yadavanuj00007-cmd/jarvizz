#!/usr/bin/env python3
"""India AI Value Chain Comprehensive Stock Report — 2026 Edition"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime

W, H = A4

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY    = HexColor('#0A1628')
BLUE    = HexColor('#1B4F8C')
LBLUE   = HexColor('#EAF2FF')
DGRAY   = HexColor('#2C3E50')
MGRAY   = HexColor('#AEB6BF')
LGRAY   = HexColor('#F4F6F7')
GOLD    = HexColor('#D4A017')
SGOLD   = HexColor('#FFF8E7')
GREEN   = HexColor('#1A7A4A')
LGREEN  = HexColor('#EAFAF1')
RED     = HexColor('#C0392B')
LRED    = HexColor('#FDEDEC')
ORANGE  = HexColor('#C87000')
LORANGE = HexColor('#FEF5E7')
TEAL    = HexColor('#0E7F6E')
LTEAL   = HexColor('#E8F8F5')
PURPLE  = HexColor('#5B2D8E')
LPURP   = HexColor('#F5EEF8')
WHITE   = HexColor('#FFFFFF')
CREAM   = HexColor('#FAFAFA')


def score_clr(s):
    if s >= 4.5: return GREEN
    if s >= 3.5: return TEAL
    if s >= 2.5: return ORANGE
    return RED

def verdict_clr(v):
    v = v.upper()
    if 'STRONG BUY' in v: return GREEN
    if 'BUY' in v:        return TEAL
    if 'WATCHLIST' in v:  return ORANGE
    if 'SPECULATIVE' in v: return PURPLE
    return RED

def bars(s, total=5):
    return '●' * int(s) + '○' * (total - int(s))


# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    b = getSampleStyleSheet()
    def S(name, parent='Normal', **kw):
        return ParagraphStyle(name, parent=b[parent], **kw)

    return {
        'cover_h1': S('cover_h1', fontSize=30, textColor=WHITE,
                       alignment=TA_CENTER, fontName='Helvetica-Bold', leading=36),
        'cover_h2': S('cover_h2', fontSize=17, textColor=GOLD,
                       alignment=TA_CENTER, fontName='Helvetica-Bold', leading=22),
        'cover_body': S('cover_body', fontSize=11, textColor=WHITE,
                         alignment=TA_CENTER, fontName='Helvetica', leading=16),
        'sec_hdr': S('sec_hdr', 'Heading1', fontSize=14, textColor=WHITE,
                      fontName='Helvetica-Bold', spaceBefore=4, spaceAfter=6, leading=18),
        'seg_hdr': S('seg_hdr', fontSize=12, textColor=NAVY,
                      fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=4, leading=15),
        'co_name': S('co_name', fontSize=11, textColor=BLUE,
                      fontName='Helvetica-Bold', spaceBefore=4, spaceAfter=2),
        'body': S('body', fontSize=8.5, textColor=DGRAY,
                   alignment=TA_JUSTIFY, fontName='Helvetica', leading=13, spaceAfter=3),
        'bullet': S('bullet', fontSize=8.5, textColor=DGRAY,
                     fontName='Helvetica', leading=12, spaceAfter=2, leftIndent=8),
        'small': S('small', fontSize=7.5, textColor=MGRAY,
                    fontName='Helvetica', leading=11),
        'toc': S('toc', fontSize=9.5, textColor=NAVY,
                  fontName='Helvetica', leading=14, spaceAfter=3),
        'disc': S('disc', fontSize=7.5, textColor=MGRAY,
                   fontName='Helvetica-Oblique', leading=11, alignment=TA_JUSTIFY),
        'tag': S('tag', fontSize=8, textColor=WHITE,
                  fontName='Helvetica-Bold', alignment=TA_CENTER),
        'intro': S('intro', fontSize=9, textColor=DGRAY,
                    fontName='Helvetica', leading=14, alignment=TA_JUSTIFY, spaceAfter=4),
        'h3': S('h3', fontSize=10, textColor=NAVY,
                 fontName='Helvetica-Bold', spaceBefore=6, spaceAfter=3),
    }


# ── Company Dataset ───────────────────────────────────────────────────────────
COMPANIES = [
    # ── 1. AI Infrastructure & Data Centers ──────────────────────────────────
    dict(
        seg="AI Infrastructure & Data Centers",
        name="Adani Enterprises", ticker="ADANIENT", cap="Large Cap",
        mcap="~₹2,00,000 Cr",
        desc="India's largest new-business incubator. Building hyperscale AI data centers via Adani Connex (JV with EdgeConneX). Plans 1 GW+ of AI data center capacity.",
        thesis="Positioned as the physical backbone of India's AI infrastructure. Adani Connex targets hyperscaler demand from Google, Microsoft & Indian cloud companies. PLI data center scheme beneficiary.",
        rules=dict(uptrend=3,volume=5,not_extended=3,theme=5,structure=3,rel_strength=3,liquidity=5,entry=3),
        pros=["India's largest planned AI data center buildout (1GW+)", "Strategic land bank near power grids", "Govt digital infra alignment"],
        cons=["High group-level debt remains a concern", "Governance risk premium in market", "Diversified conglomerate – not pure-play AI"],
        verdict="WATCHLIST",
    ),
    dict(
        seg="AI Infrastructure & Data Centers",
        name="Tata Communications", ticker="TATACOMM", cap="Large Cap",
        mcap="~₹35,000 Cr",
        desc="Global digital infrastructure company connecting 7,000+ enterprises in 190+ countries. AI-powered cloud, network, IoT, and cybersecurity services.",
        thesis="Network intelligence + edge AI delivery infrastructure. Provides the underlying secure fabric for GenAI applications. MOVE AI platform serves enterprise AI orchestration needs.",
        rules=dict(uptrend=4,volume=4,not_extended=3,theme=4,structure=4,rel_strength=4,liquidity=4,entry=4),
        pros=["AI-powered global network = unique moat", "Recurring enterprise revenue base", "Tata Group governance premium"],
        cons=["Ongoing high capex requirements", "Hyperscaler direct-connect competition"],
        verdict="BUY ON PULLBACK",
    ),
    dict(
        seg="AI Infrastructure & Data Centers",
        name="Tejas Networks", ticker="TEJASNET", cap="Mid Cap",
        mcap="~₹8,000 Cr",
        desc="Indian optical & data networking product company. Supplies 5G and broadband equipment for BharatNet and commercial telecom. Tata Sons subsidiary.",
        thesis="AI data centers require massive optical bandwidth. Tejas provides India-made networking equipment reducing import dependency. 5G + AI infrastructure convergence play.",
        rules=dict(uptrend=4,volume=3,not_extended=3,theme=4,structure=4,rel_strength=4,liquidity=3,entry=3),
        pros=["Tata backing + Atmanirbhar Bharat theme", "5G BharatNet order momentum", "Import substitution tailwind in networking"],
        cons=["Order book concentration risk", "Scale gap vs Nokia / Ericsson"],
        verdict="WATCHLIST",
    ),
    dict(
        seg="AI Infrastructure & Data Centers",
        name="Sterlite Technologies", ticker="STRTECH", cap="Small Cap",
        mcap="~₹4,500 Cr",
        desc="End-to-end optical fiber cable manufacturer and digital network solutions provider. Exports fiber to 100+ countries.",
        thesis="Every AI data center and 5G deployment requires vast optical fiber infrastructure. STL is India's only integrated fiber + network company serving AI infra demand globally.",
        rules=dict(uptrend=2,volume=3,not_extended=4,theme=3,structure=2,rel_strength=2,liquidity=3,entry=3),
        pros=["Secular global fiber demand from AI buildout", "End-to-end digital network capability"],
        cons=["High debt, undergoing balance sheet repair", "Margin pressure from competition", "Weak near-term chart trend"],
        verdict="WATCHLIST",
    ),

    # ── 2. Semiconductor & Electronics Manufacturing ──────────────────────────
    dict(
        seg="Semiconductor & Electronics Manufacturing",
        name="Dixon Technologies", ticker="DIXON", cap="Large Cap",
        mcap="~₹70,000 Cr",
        desc="India's largest electronics manufacturing services (EMS) company. Manufactures smartphones, LED TVs, washing machines, and increasingly AI-enabled edge devices.",
        thesis="As AI moves to edge devices – AI phones, AI PCs, AI TVs, IoT – Dixon benefits directly from every unit shipped. Apple ecosystem entry and Samsung JV make it India's premier AI device manufacturer.",
        rules=dict(uptrend=5,volume=4,not_extended=3,theme=4,structure=4,rel_strength=5,liquidity=4,entry=3),
        pros=["India's AI device manufacturing leader", "PLI tailwinds attracting large anchor OEM orders", "Apple ecosystem entry underway"],
        cons=["Thin EMS margins (2–4% PAT)", "Customer concentration risk", "Input commodity price sensitivity"],
        verdict="BUY ON PULLBACK",
    ),
    dict(
        seg="Semiconductor & Electronics Manufacturing",
        name="Kaynes Technology", ticker="KAYNES", cap="Mid Cap",
        mcap="~₹16,000 Cr",
        desc="IoT-enabled electronics manufacturing services company building India's first OSAT (semiconductor packaging) facility with government support.",
        thesis="India's semiconductor ambitions converge at Kaynes. OSAT facility will domestically serve AI chip packaging demand. IoT + industrial AI hardware leader.",
        rules=dict(uptrend=5,volume=3,not_extended=3,theme=5,structure=4,rel_strength=5,liquidity=3,entry=3),
        pros=["First Indian OSAT chip-packaging facility", "Strong aerospace + defence order book", "AI + Semiconductor + India PLI trifecta"],
        cons=["OSAT execution is capital-intensive and new", "Premium valuation prices in high growth", "Moderate daily liquidity"],
        verdict="BUY ON PULLBACK",
    ),
    dict(
        seg="Semiconductor & Electronics Manufacturing",
        name="Tata Elxsi", ticker="TATAELXSI", cap="Mid Cap",
        mcap="~₹40,000 Cr",
        desc="Design and technology services for automotive, healthcare, and broadcast. Embedded software + AI/ML product engineering for global OEMs.",
        thesis="AI-embedded product design leader. Autonomous vehicle AI (SDV), medical AI imaging, connected home AI. GenAI product engineering growing. Premium design firm with software-like margins.",
        rules=dict(uptrend=3,volume=4,not_extended=4,theme=5,structure=3,rel_strength=3,liquidity=4,entry=4),
        pros=["Premium AI product design moat", "SDV / Automotive AI dominant position", "~27% EBITDA margins – software-like"],
        cons=["Auto sector cyclicality dampens growth", "Revenue concentration in top 3 clients", "Near-term growth headwinds persist"],
        verdict="WATCHLIST",
    ),
    dict(
        seg="Semiconductor & Electronics Manufacturing",
        name="Moschip Technologies", ticker="MOSCHIP", cap="Small Cap",
        mcap="~₹1,200 Cr",
        desc="Semiconductor IP and custom VLSI/ASIC design services company – one of India's very few listed chip design companies.",
        thesis="Rare Indian semiconductor IP play. Custom AI chip design, RISC-V implementations, VLSI services for AI edge processors. Nascent but high potential – potential acquisition target for global fabless firms.",
        rules=dict(uptrend=3,volume=2,not_extended=3,theme=5,structure=3,rel_strength=3,liquidity=2,entry=2),
        pros=["Rare listed Indian chip design company", "AI chip design secular long-term opportunity", "Potential strategic M&A target"],
        cons=["Very low daily liquidity (<₹3–5 Cr/day)", "Tiny scale vs global opportunity", "Execution track record still building"],
        verdict="SPECULATIVE",
    ),
    dict(
        seg="Semiconductor & Electronics Manufacturing",
        name="Cyient DLM", ticker="CYIENTDLM", cap="Small Cap",
        mcap="~₹5,000 Cr",
        desc="Design-led electronics manufacturing (DLM) for aerospace, defence, and medical. End-to-end PCB assembly and electronics for mission-critical AI-enabled systems.",
        thesis="Manufactures electronics for defence AI systems, medical imaging AI, aerospace AI. Triple tailwind: Defence + AI + Electronics Manufacturing with Cyient parent customer relationships.",
        rules=dict(uptrend=4,volume=3,not_extended=3,theme=4,structure=4,rel_strength=4,liquidity=3,entry=3),
        pros=["Defence AI hardware manufacturing play", "Design-to-manufacture capability moat", "Cyient parent brings blue-chip client access"],
        cons=["Low daily trading volumes", "Niche market limits near-term scale", "Strategic dependency on parent"],
        verdict="WATCHLIST",
    ),

    # ── 3. IT Services & Cloud AI – Large Cap ────────────────────────────────
    dict(
        seg="IT Services & Cloud AI (Large Cap)",
        name="Persistent Systems", ticker="PERSISTENT", cap="Large Cap",
        mcap="~₹75,000 Cr",
        desc="Mid-large IT company with industry-best revenue growth in Indian IT. GenAI practice contributes 15%+ to revenue. Ranked among top GenAI services providers globally.",
        thesis="GenAI product engineering leader. SASVA AI platform accelerates software development. Consistently outgrowing IT peers 25%+ CAGR. The closest India has to a pure-play AI services company at scale.",
        rules=dict(uptrend=5,volume=4,not_extended=3,theme=5,structure=5,rel_strength=5,liquidity=4,entry=3),
        pros=["India IT sector's top revenue growth (25%+ CAGR)", "SASVA GenAI platform creates productivity moat", "Premium valuation justified by consistent execution"],
        cons=["Expensive at 60–70x PE – limited margin of safety", "BFSI + Hi-tech client concentration", "Sustaining growth at larger base is harder"],
        verdict="BUY ON DIP",
    ),
    dict(
        seg="IT Services & Cloud AI (Large Cap)",
        name="Coforge", ticker="COFORGE", cap="Large Cap",
        mcap="~₹45,000 Cr",
        desc="Mid-large IT services company with aggressive AI/digital transformation focus. Strong in BFSI, travel, and insurance. CIGNITI acquisition strengthened AI testing capabilities.",
        thesis="Quicreate AI platform + CIGNITI AI testing create differentiated mid-market AI services offering. Strong deal wins momentum; improving margins; management credibility high.",
        rules=dict(uptrend=4,volume=4,not_extended=3,theme=4,structure=4,rel_strength=4,liquidity=4,entry=4),
        pros=["Aggressive AI capability buildout via focused M&A", "Improving deal momentum and order book", "Management credibility and execution track record"],
        cons=["Integration risk from multiple acquisitions", "BFSI sector dependency", "Margin management at growing scale"],
        verdict="BUY",
    ),
    dict(
        seg="IT Services & Cloud AI (Large Cap)",
        name="Tech Mahindra", ticker="TECHM", cap="Large Cap",
        mcap="~₹1,20,000 Cr",
        desc="Large-cap IT services undergoing TechM 2.0 transformation with AI at center. Unique 5G + AI convergence positioning. Strong telecom domain heritage.",
        thesis="TechM 2.0 strategy rebuilds company around AI. Unique intersection of 5G network AI and enterprise AI services. Significant margin expansion runway post-restructuring = multi-year upside.",
        rules=dict(uptrend=4,volume=5,not_extended=3,theme=4,structure=4,rel_strength=4,liquidity=5,entry=3),
        pros=["Turnaround + AI-first strategy = strong re-rating potential", "5G + AI unique vs all IT peers", "Significant margin improvement runway"],
        cons=["Execution risk in ongoing transformation", "Telecom client weakness persists", "Catching up vs Persistent/Coforge"],
        verdict="BUY ON PULLBACK",
    ),
    dict(
        seg="IT Services & Cloud AI (Large Cap)",
        name="LTIMindtree", ticker="LTIM", cap="Large Cap",
        mcap="~₹1,50,000 Cr",
        desc="Large-cap IT formed from LTI + Mindtree merger. Canvas AI platform for enterprise AI. Strong manufacturing sector AI expertise and deep client relationships.",
        thesis="Canvas AI integrated platform for enterprise AI. Post-merger integration completing; growth acceleration expected. Attractive relative valuation vs Persistent. Manufacturing + BFSI AI depth.",
        rules=dict(uptrend=3,volume=5,not_extended=4,theme=4,structure=3,rel_strength=3,liquidity=5,entry=4),
        pros=["Canvas AI enterprise platform at scale", "Attractive valuation vs growth peers", "L&T group governance and client access"],
        cons=["Integration challenges slowing growth recovery", "Sub-par relative strength vs IT peers", "Margin recovery taking longer than guided"],
        verdict="WATCHLIST",
    ),
    dict(
        seg="IT Services & Cloud AI (Large Cap)",
        name="Mphasis", ticker="MPHASIS", cap="Large Cap",
        mcap="~₹35,000 Cr",
        desc="AI-first IT company focused on cloud and AI for BFSI. Backed by Blackstone. DeepInsights AI platform for financial services digital transformation.",
        thesis="DeepInsights + X2C2T AI frameworks create deep BFSI AI moat. Hyper-specialization differentiates from generalist IT peers. Blackstone exit creates M&A optionality catalyst.",
        rules=dict(uptrend=3,volume=4,not_extended=4,theme=4,structure=3,rel_strength=3,liquidity=4,entry=4),
        pros=["Strong BFSI AI platform (DeepInsights)", "Relatively attractive valuation vs peers", "Potential M&A catalyst – Blackstone ownership"],
        cons=["DXC revenue concentration remains significant", "Slower growth vs peers over 2023–25", "Needs to prove sustained revenue recovery"],
        verdict="WATCHLIST",
    ),

    # ── 4. IT Services – Mid / Small Cap ─────────────────────────────────────
    dict(
        seg="IT Services & Cloud AI (Mid/Small Cap)",
        name="Happiest Minds Technologies", ticker="HAPPSTMNDS", cap="Small Cap",
        mcap="~₹8,000 Cr",
        desc="Born Digital, Born Agile IT services company. 100% digital-native revenue model. Founded by Ashok Soota; strong AI/ML and GenAI service capabilities.",
        thesis="Purpose-built AI-native IT company with no legacy drag. GenAI product engineering, AI-embedded cloud services, edge AI. High EBITDA margins (~22%) for size. Founder credibility = quality culture.",
        rules=dict(uptrend=3,volume=3,not_extended=4,theme=5,structure=3,rel_strength=3,liquidity=3,entry=4),
        pros=["100% digital/AI revenue – zero legacy overhead", "High margins (~22% EBITDA) for its size", "Founder credibility (Ashok Soota, ex-Wipro CEO)"],
        cons=["Revenue growth deceleration since FY24", "Small scale limits large-deal access", "Founder succession planning uncertainty"],
        verdict="WATCHLIST",
    ),
    dict(
        seg="IT Services & Cloud AI (Mid/Small Cap)",
        name="Zensar Technologies", ticker="ZENSARTECH", cap="Mid Cap",
        mcap="~₹11,000 Cr",
        desc="Mid-tier IT services under RPG Group. Focused on experience services and AI-driven digital transformation for manufacturing, retail, and hi-tech verticals.",
        thesis="Recovery story with RPG Group governance improvement. AI-powered customer experience transformation. Improving financials and relative strength make it a value play in AI services.",
        rules=dict(uptrend=4,volume=3,not_extended=3,theme=3,structure=4,rel_strength=4,liquidity=3,entry=3),
        pros=["Recovery story with improving financials", "RPG Group governance premium improving", "Attractive valuation vs mid-tier IT peers"],
        cons=["Less differentiated AI story vs pure-plays", "Client concentration risk in top accounts", "Mid-tier scale disadvantage in large deals"],
        verdict="WATCHLIST",
    ),
    dict(
        seg="IT Services & Cloud AI (Mid/Small Cap)",
        name="Latent View Analytics", ticker="LATENTVIEW", cap="Small Cap",
        mcap="~₹5,000 Cr",
        desc="India's only listed pure-play data analytics and AI services company. Works with Fortune 500 companies on advanced analytics, ML models, and GenAI adoption.",
        thesis="Pure analytics/AI play with Fortune 500 client quality that larger peers can't match for deep data work. Cash-rich (zero debt), enabling future AI M&A. GenAI advisory is fast-growing.",
        rules=dict(uptrend=3,volume=3,not_extended=4,theme=5,structure=3,rel_strength=3,liquidity=3,entry=4),
        pros=["Only listed pure-play analytics/AI in India", "Excellent Fortune 500 client quality", "Cash-rich, zero debt balance sheet"],
        cons=["Revenue growth slowdown in recent quarters", "High client concentration (top 5 ~60% revenue)", "Small scale limits enterprise deal size"],
        verdict="WATCHLIST",
    ),
    dict(
        seg="IT Services & Cloud AI (Mid/Small Cap)",
        name="Mastech Digital", ticker="MASTECH", cap="Small Cap",
        mcap="~₹1,500 Cr",
        desc="AI and digital talent solutions company. iMocha AI skills assessment SaaS platform plus digital staffing for AI/cloud roles.",
        thesis="Unique play on AI talent shortage: iMocha skills platform + digital staffing. Enterprises need AI talent assessment and sourcing – Mastech addresses both ends. Growing iMocha SaaS ARR.",
        rules=dict(uptrend=3,volume=2,not_extended=3,theme=4,structure=3,rel_strength=3,liquidity=2,entry=3),
        pros=["iMocha AI skills assessment platform is unique listed asset", "AI talent shortage is multi-year secular tailwind", "Growing SaaS revenue through iMocha"],
        cons=["Very low market liquidity (<₹3 Cr/day)", "Staffing business cyclicality", "Small scale, limited institutional coverage"],
        verdict="SPECULATIVE",
    ),

    # ── 5. AI Applications & Platforms ───────────────────────────────────────
    dict(
        seg="AI Applications & Platforms",
        name="Info Edge (Naukri)", ticker="NAUKRI", cap="Large Cap",
        mcap="~₹72,000 Cr",
        desc="India's monopoly online recruitment platform (Naukri.com) plus real estate classifieds. Holds strategic stakes in Zomato, PolicyBazaar, and other AI-driven startups.",
        thesis="AI-powered recruitment monopoly + venture portfolio of AI companies within a listed stock. Naukri's AI matching algorithms grow in value as India's tech hiring booms. Startup portfolio = AI sector exposure.",
        rules=dict(uptrend=5,volume=4,not_extended=3,theme=4,structure=5,rel_strength=5,liquidity=4,entry=3),
        pros=["AI-powered monopoly in Indian job recruitment", "Portfolio: Zomato, PolicyBazaar AI company exposure", "Strong cash generation + compounding moat"],
        cons=["Premium valuation (40–50x PE)", "Job market cyclicality impacts core revenue", "Core Naukri growth somewhat maturing"],
        verdict="BUY ON DIP",
    ),
    dict(
        seg="AI Applications & Platforms",
        name="Zomato", ticker="ZOMATO", cap="Large Cap",
        mcap="~₹2,20,000 Cr",
        desc="India's leading food delivery and quick commerce (Blinkit) company. AI drives delivery optimization, demand forecasting, personalization, and fraud detection at scale.",
        thesis="AI is the competitive moat: route optimization AI, demand forecasting AI, restaurant recommendation AI, fraud AI. Every transaction is AI-powered. Blinkit creates an AI-powered last-mile data flywheel.",
        rules=dict(uptrend=5,volume=5,not_extended=3,theme=5,structure=5,rel_strength=5,liquidity=5,entry=3),
        pros=["AI as fundamental competitive moat across all operations", "Market leadership + profitability milestone achieved", "Blinkit quick commerce driving secular growth"],
        cons=["Very high valuation (100x+ PE, expensive)", "Swiggy / Instamart competition", "Unit economics of new verticals still evolving"],
        verdict="BUY ON DIP",
    ),
    dict(
        seg="AI Applications & Platforms",
        name="Affle India", ticker="AFFLE", cap="Mid Cap",
        mcap="~₹18,000 Cr",
        desc="AI-powered mobile marketing and consumer intelligence platform. Proprietary CPCU (Cost Per Converted User) model. Serves 2B+ user devices across 30+ markets globally.",
        thesis="Pure AI platform: every consumer conversion decision is ML-driven. As mobile AI advertising grows in emerging markets, Affle's platform advantages compound with scale. Global expansion via acquisitions.",
        rules=dict(uptrend=4,volume=3,not_extended=3,theme=5,structure=4,rel_strength=4,liquidity=3,entry=4),
        pros=["Proprietary AI platform with strong technology moat", "CPCU model aligns perfectly with advertiser ROI", "Growing global emerging market footprint"],
        cons=["High valuation (50–60x PE)", "Digital advertising spend cyclicality risk", "Execution risk in international acquisitions"],
        verdict="BUY",
    ),
    dict(
        seg="AI Applications & Platforms",
        name="Newgen Software", ticker="NEWGEN", cap="Mid Cap",
        mcap="~₹14,000 Cr",
        desc="Low-code AI-powered business process automation and content management platform. Products used by 500+ banks, insurance companies, and governments globally.",
        thesis="AI embedded in low-code BPM enables enterprise GenAI adoption without custom coding. AI document processing, intelligent banking automation. SaaS transition accelerates recurring revenue.",
        rules=dict(uptrend=5,volume=3,not_extended=3,theme=4,structure=5,rel_strength=5,liquidity=3,entry=3),
        pros=["Consistent 25%+ revenue growth trajectory", "AI embedded in sticky enterprise BPM products", "SaaS transition driving valuation re-rating"],
        cons=["Low daily liquidity (~₹5–8 Cr/day)", "Premium valuation (60–70x PE)", "Enterprise sales cycles are inherently long"],
        verdict="BUY ON PULLBACK",
    ),
    dict(
        seg="AI Applications & Platforms",
        name="Intellect Design Arena", ticker="INTELLECT", cap="Mid Cap",
        mcap="~₹10,000 Cr",
        desc="AI-powered financial technology company. Cloud-native banking, insurance, treasury, and risk platforms for 270+ clients across 57 countries.",
        thesis="AI embedded in every BFSI module: risk AI, treasury AI, lending AI. Composable AI banking is the future of financial services. Growing product licenses = strong operating leverage ahead.",
        rules=dict(uptrend=4,volume=3,not_extended=3,theme=4,structure=4,rel_strength=4,liquidity=3,entry=3),
        pros=["Deep BFSI AI moat across 57 countries", "Composable AI banking architecture advantage", "Growing SaaS / subscription revenue transition"],
        cons=["Lumpy revenue recognition from large deals", "Long enterprise financial services sales cycles", "Moderate daily trading liquidity"],
        verdict="BUY ON PULLBACK",
    ),
    dict(
        seg="AI Applications & Platforms",
        name="RateGain Travel Technologies", ticker="RATEGAIN", cap="Small Cap",
        mcap="~₹5,500 Cr",
        desc="AI-powered travel technology SaaS. Revenue management, distribution, and marketing AI for hotels, airlines, OTAs, and car rental companies globally.",
        thesis="AI-powered revenue management is mission-critical for hotels/airlines. Dynamic pricing AI + demand forecasting AI create high switching costs. GenAI marketing copilot is new growth vector.",
        rules=dict(uptrend=4,volume=3,not_extended=3,theme=4,structure=4,rel_strength=4,liquidity=3,entry=3),
        pros=["Niche AI SaaS in travel with global scale", "Recurring revenue from sticky hotel/airline clients", "GenAI marketing copilot is emerging growth driver"],
        cons=["Travel sector cyclicality exposure", "Integration risks from multiple acquisitions", "Small scale in global context vs Amadeus/Sabre"],
        verdict="WATCHLIST",
    ),

    # ── 6. Telecom AI Enablers ────────────────────────────────────────────────
    dict(
        seg="Telecom AI Enablers",
        name="Bharti Airtel", ticker="BHARTIARTL", cap="Large Cap",
        mcap="~₹8,50,000 Cr",
        desc="India's largest telecom by revenue. Heavy AI investments for network optimization, customer AI, and enterprise AI solutions. Aggressive 5G rollout across India.",
        thesis="5G network becomes AI delivery infrastructure. Airtel AI platform for enterprises. Network AI enables self-optimizing 5G. The pipe AND the AI become inseparable – Airtel owns both.",
        rules=dict(uptrend=5,volume=5,not_extended=3,theme=4,structure=5,rel_strength=5,liquidity=5,entry=3),
        pros=["5G + AI convergence – unique strategic position", "Enterprise AI monetization already underway", "Consistent long-term compounding story"],
        cons=["Capital intensive – 5G + AI capex is heavy", "Not a pure AI play – telecom is the core", "Jio competition constrains pricing power"],
        verdict="BUY",
    ),
    dict(
        seg="Telecom AI Enablers",
        name="Reliance Industries", ticker="RELIANCE", cap="Large Cap",
        mcap="~₹16,00,000 Cr",
        desc="India's largest conglomerate with major AI initiatives via Jio Brain platform, massive data center investments ($20B+), and Meta partnership for Indian language AI.",
        thesis="Jio Brain AI platform + India's largest AI data center commitment. Meta Llama partnership creates Indian language AI moat. 500M+ Jio users = India's largest AI data flywheel.",
        rules=dict(uptrend=3,volume=5,not_extended=4,theme=4,structure=3,rel_strength=3,liquidity=5,entry=4),
        pros=["Massive AI investment capacity at conglomerate scale", "Jio AI + Meta Llama partnership moat", "500M+ user base = AI data flywheel"],
        cons=["Not pure-play – diverse conglomerate structure", "AI value not yet clearly monetized in financials", "Complex holding structure – hard to value AI piece"],
        verdict="WATCHLIST",
    ),

    # ── 7. Defence AI ─────────────────────────────────────────────────────────
    dict(
        seg="Defence AI",
        name="Bharat Electronics (BEL)", ticker="BEL", cap="Large Cap",
        mcap="~₹2,00,000 Cr",
        desc="Navratna defence PSU. India's largest electronics company. Manufactures AI-powered radar, surveillance, communication, and battlefield management systems.",
        thesis="AI-powered defence electronics monopoly. AI radar systems, AI surveillance, drone swarm AI, battlefield AI. As India's defence AI budget grows, BEL is the primary and overwhelmingly dominant beneficiary.",
        rules=dict(uptrend=4,volume=5,not_extended=3,theme=5,structure=4,rel_strength=4,liquidity=5,entry=3),
        pros=["Defence AI monopoly position in India", "₹70,000+ Cr order book – 4+ years visibility", "Government defence budget expansion secular tailwind"],
        cons=["PSU execution pace constraints vs private sector", "Stretched valuation already prices in strong growth", "Private sector defence competition increasing"],
        verdict="BUY ON PULLBACK",
    ),
    dict(
        seg="Defence AI",
        name="Zen Technologies", ticker="ZENTEC", cap="Small Cap",
        mcap="~₹5,000 Cr",
        desc="Defence simulation and training solutions. AI-powered military simulation systems, counter-drone AI systems (PELICAN), and combat training simulators.",
        thesis="Counter-drone AI market is growing exponentially post-Ukraine conflict. Zen's AI-powered anti-drone systems are export-grade. Military simulation AI creates recurring training contracts. Rare pure-play AI + Defence company.",
        rules=dict(uptrend=5,volume=3,not_extended=3,theme=5,structure=5,rel_strength=5,liquidity=3,entry=3),
        pros=["Counter-drone AI leader in India + export markets", "AI military simulation = recurring MoD contracts", "Strong order book with Ministry of Defence"],
        cons=["Low daily liquidity (~₹10–15 Cr/day)", "Government procurement cycle unpredictability", "Small company concentration and execution risk"],
        verdict="WATCHLIST",
    ),
    dict(
        seg="Defence AI",
        name="Data Patterns India", ticker="DATAPATTNS", cap="Small Cap",
        mcap="~₹8,000 Cr",
        desc="Defence and aerospace electronics company. Products include avionics, radar electronics, and space electronics for DRDO, ISRO, and Indian defence agencies.",
        thesis="AI-embedded defence electronics: radar AI, missile guidance AI, satellite AI. Space + Defence + AI triple play. ISRO's growing program provides strong order pipeline. Rare listed Space economy + AI play.",
        rules=dict(uptrend=4,volume=3,not_extended=3,theme=5,structure=4,rel_strength=4,liquidity=3,entry=3),
        pros=["Space + Defence + AI unique intersection listing", "High EBITDA margins (>30%) for defence electronics", "Import substitution in mission-critical electronics"],
        cons=["Lumpy order execution creates revenue volatility", "Low daily trading liquidity", "Dependent on government defence/space budget cycles"],
        verdict="WATCHLIST",
    ),
    dict(
        seg="Defence AI",
        name="MTAR Technologies", ticker="MTARTECH", cap="Small Cap",
        mcap="~₹3,500 Cr",
        desc="Precision engineering for space, defence, nuclear, and clean energy. Manufactures precision components for rockets, missiles, and nuclear power systems.",
        thesis="Precision manufacturing for AI-enabled defence + space systems. Bloom Energy partnership for fuel cells – a critical power source for AI data centers (backup + primary). Space economy beneficiary.",
        rules=dict(uptrend=3,volume=2,not_extended=3,theme=3,structure=3,rel_strength=3,liquidity=2,entry=3),
        pros=["Space launch + Defence precision play", "Bloom Energy fuel cell = AI data center power angle", "High technical moat in precision engineering"],
        cons=["Indirect AI connection – not core AI company", "Low liquidity, high stock volatility", "Revenue concentration in few key customers"],
        verdict="WATCHLIST",
    ),
]

# Pre-compute avg scores
for c in COMPANIES:
    c['avg'] = round(sum(c['rules'].values()) / len(c['rules']), 1)


# ── Header / Footer ───────────────────────────────────────────────────────────
def draw_header_footer(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 32, W, 32, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.setFont('Helvetica-Bold', 9.5)
    canvas.drawString(30, H - 20, '  INDIA AI VALUE CHAIN REPORT — 2026 EDITION')
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica', 8.5)
    canvas.drawRightString(W - 30, H - 20, f'Generated: {datetime.now().strftime("%d %b %Y")}')
    # Footer bar
    canvas.setFillColor(LGRAY)
    canvas.rect(0, 0, W, 22, fill=1, stroke=0)
    canvas.setFillColor(MGRAY)
    canvas.setFont('Helvetica-Oblique', 7)
    canvas.drawString(30, 7, 'FOR EDUCATIONAL PURPOSES ONLY | NOT INVESTMENT ADVICE | Verify all data with current charts before investing')
    canvas.setFillColor(NAVY)
    canvas.setFont('Helvetica-Bold', 8.5)
    canvas.drawRightString(W - 30, 7, f'Page {doc.page}')
    canvas.restoreState()


# ── Cover Page ────────────────────────────────────────────────────────────────
def build_cover(story):
    # Full-page navy background via a table
    def cover_cell():
        inner = [
            Spacer(1, 1.6*cm),
            Paragraph('INDIA AI VALUE CHAIN', ParagraphStyle('cx1', fontSize=32, textColor=WHITE, alignment=TA_CENTER, fontName='Helvetica-Bold', leading=38)),
            Paragraph('COMPREHENSIVE STOCK REPORT', ParagraphStyle('cx2', fontSize=22, textColor=GOLD, alignment=TA_CENTER, fontName='Helvetica-Bold', leading=28)),
            Spacer(1, 0.4*cm),
            Paragraph('2026 EDITION', ParagraphStyle('cx3', fontSize=16, textColor=WHITE, alignment=TA_CENTER, fontName='Helvetica', leading=20)),
            Spacer(1, 1.0*cm),
            HRFlowable(width='70%', thickness=1.5, color=GOLD, hAlign='CENTER'),
            Spacer(1, 0.8*cm),
            Paragraph('Track India\'s AI Revolution Across the Entire Value Chain', ParagraphStyle('cx4', fontSize=13, textColor=WHITE, alignment=TA_CENTER, fontName='Helvetica-Oblique', leading=18)),
            Spacer(1, 0.5*cm),
            Paragraph('~30 Companies  |  All Cap Sizes  |  8-Rule Evaluation Framework', ParagraphStyle('cx5', fontSize=11, textColor=GOLD, alignment=TA_CENTER, fontName='Helvetica-Bold', leading=16)),
            Spacer(1, 1.2*cm),
            HRFlowable(width='60%', thickness=0.8, color=HexColor('#3A5F8C'), hAlign='CENTER'),
            Spacer(1, 0.6*cm),
        ]

        # Segment pills
        segs = ['AI Infrastructure', 'Semiconductors', 'IT/Cloud AI', 'AI Applications', 'Telecom AI', 'Defence AI']
        pill_data = [[Paragraph(s, ParagraphStyle('pill', fontSize=8.5, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)) for s in segs]]
        pill_tbl = Table(pill_data, colWidths=[(W-100)/6]*6)
        pill_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), BLUE),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [BLUE]),
            ('ROUNDEDCORNERS', [4]),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#3A5F8C')),
        ]))
        inner.append(pill_tbl)
        inner.append(Spacer(1, 1.4*cm))
        inner.append(HRFlowable(width='60%', thickness=0.8, color=HexColor('#3A5F8C'), hAlign='CENTER'))
        inner.append(Spacer(1, 0.6*cm))

        # Formula
        formula_data = [[
            Paragraph('TREND', ParagraphStyle('f1', fontSize=11, textColor=GOLD, fontName='Helvetica-Bold', alignment=TA_CENTER)),
            Paragraph('+', ParagraphStyle('fp', fontSize=13, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
            Paragraph('VOLUME', ParagraphStyle('f2', fontSize=11, textColor=GOLD, fontName='Helvetica-Bold', alignment=TA_CENTER)),
            Paragraph('+', ParagraphStyle('fp2', fontSize=13, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
            Paragraph('STRUCTURE', ParagraphStyle('f3', fontSize=11, textColor=GOLD, fontName='Helvetica-Bold', alignment=TA_CENTER)),
            Paragraph('=', ParagraphStyle('feq', fontSize=13, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
            Paragraph('HIGH PROBABILITY SETUP', ParagraphStyle('f4', fontSize=9.5, textColor=HexColor('#90EE90'), fontName='Helvetica-Bold', alignment=TA_CENTER)),
        ]]
        ftbl = Table(formula_data, colWidths=[70, 20, 70, 20, 80, 20, 120])
        ftbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(-1,-1), HexColor('#0D2240')),
            ('TOPPADDING', (0,0),(-1,-1), 8),
            ('BOTTOMPADDING', (0,0),(-1,-1), 8),
            ('LEFTPADDING', (0,0),(-1,-1), 4),
            ('RIGHTPADDING', (0,0),(-1,-1), 4),
            ('BOX', (0,0),(-1,-1), 1, GOLD),
        ]))
        inner.append(ftbl)
        inner.append(Spacer(1, 1.2*cm))
        inner.append(Paragraph(f'Report Date: {datetime.now().strftime("%B %d, %Y")}',
                                ParagraphStyle('dt', fontSize=10, textColor=MGRAY, alignment=TA_CENTER, fontName='Helvetica')))
        return inner

    cover = Table([[cover_cell()]], colWidths=[W - 60], rowHeights=[H - 110])
    cover.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 30),
        ('RIGHTPADDING', (0, 0), (-1, -1), 30),
    ]))
    story.append(cover)
    story.append(PageBreak())


# ── Framework Section ─────────────────────────────────────────────────────────
RULES_META = [
    ('1', 'Only Buy in Uptrends',     'EMA 8 > EMA 21 | Price above moving averages | No trend = no trade'),
    ('2', 'Volume Must Confirm',      'Breakout with strong volume | Higher-than-average participation | Weak volume = weak conviction'),
    ('3', 'Never Chase Extended',     'Avoid stocks far from support | Wait for proper entries | Focus on low-risk setups'),
    ('4', 'Strong Themes Only',       'AI | Defence | EV | Energy | Capital inflow sectors'),
    ('5', 'Clean Chart Structure',    'Flags | VCP | Cup & Handle | Flat Bases | Avoid messy charts'),
    ('6', 'High Relative Strength',   'Stock outperforming Nifty 50 | Strong momentum only | Avoid weak performers'),
    ('7', 'Good Liquidity',           'High daily volume | Easy entry & exit | Avoid illiquid traps'),
    ('8', 'Enter Only on Strength',   'Breakout entry | Gap-up continuation | Confirmation before buying | Never buy randomly'),
]

def build_framework(story, styles):
    story.append(Paragraph('EVALUATION FRAMEWORK: 8 RULES BEFORE HITTING BUY', styles['sec_hdr']))
    story.append(Spacer(1, 0.2*cm))

    intro = (
        'Every company in this report is scored 1–5 on each of the 8 rules. '
        'The scores are qualitative assessments based on fundamental AI positioning, '
        'historical chart behavior, and sector dynamics. <b>Technical scores (Uptrend, Volume, '
        'Structure, Entry) must be verified with real-time charts before acting.</b> '
        'The framework follows the principle: <i>Trend + Volume + Structure = High Probability Setup.</i>'
    )
    story.append(Paragraph(intro, styles['intro']))
    story.append(Spacer(1, 0.3*cm))

    rule_rows = [
        [Paragraph('<b>#</b>', styles['small']),
         Paragraph('<b>Rule</b>', styles['small']),
         Paragraph('<b>Criteria</b>', styles['small']),
         Paragraph('<b>Score Key</b>', styles['small'])]
    ]
    score_key = '5=Excellent  4=Good  3=Neutral  2=Weak  1=Poor'
    for num, name, criteria in RULES_META:
        rule_rows.append([
            Paragraph(num, ParagraphStyle('rc', fontSize=10, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
            Paragraph(f'<b>{name}</b>', styles['body']),
            Paragraph(criteria, styles['small']),
            Paragraph(score_key if num == '1' else '', styles['small']),
        ])

    rt = Table(rule_rows, colWidths=[22, 130, 230, 130])
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('BACKGROUND', (0, 1), (0, -1), BLUE),
        ('ROWBACKGROUNDS', (1, 1), (-1, -1), [WHITE, LGRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.4, MGRAY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ]))
    story.append(rt)
    story.append(Spacer(1, 0.4*cm))

    # Scoring scale legend
    scale_data = [[
        Paragraph('● ● ● ● ●  5 – EXCELLENT', ParagraphStyle('sl5', fontSize=8, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        Paragraph('● ● ● ●  4 – GOOD',       ParagraphStyle('sl4', fontSize=8, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        Paragraph('● ● ●  3 – NEUTRAL',       ParagraphStyle('sl3', fontSize=8, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        Paragraph('● ●  2 – WEAK',            ParagraphStyle('sl2', fontSize=8, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        Paragraph('●  1 – POOR',              ParagraphStyle('sl1', fontSize=8, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
    ]]
    st = Table(scale_data, colWidths=[(W-60)/5]*5)
    st.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), GREEN),
        ('BACKGROUND', (1, 0), (1, 0), TEAL),
        ('BACKGROUND', (2, 0), (2, 0), ORANGE),
        ('BACKGROUND', (3, 0), (3, 0), RED),
        ('BACKGROUND', (4, 0), (4, 0), RED),
        ('TOPPADDING', (0,0),(-1,-1), 6),
        ('BOTTOMPADDING', (0,0),(-1,-1), 6),
    ]))
    story.append(st)
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>Disclaimer:</b> Scores are qualitative research guidance, not buy/sell signals. '
        'Always verify with up-to-date charts, financials, and your risk management rules before investing.',
        styles['disc']
    ))
    story.append(PageBreak())


# ── India AI Value Chain Map ───────────────────────────────────────────────────
def build_chain_map(story, styles):
    story.append(Paragraph('INDIA AI VALUE CHAIN — SECTOR MAP', styles['sec_hdr']))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        'The AI value chain spans from raw hardware and semiconductors all the way to consumer-facing applications. '
        'India is positioned across multiple layers, making it one of the most diverse AI investment landscapes in Asia.',
        styles['intro']
    ))
    story.append(Spacer(1, 0.3*cm))

    chain = [
        ('LAYER 1\nHardware & Infrastructure', 'AI Data Centers, Optical Fiber, Networking, Power Infrastructure',
         'Adani Enterprises, Tata Comms, Tejas Networks, Sterlite Tech', NAVY),
        ('LAYER 2\nSemiconductors & EMS', 'Chip Design, Electronics Manufacturing, OSAT, PCB Assembly',
         'Dixon Technologies, Kaynes Technology, Tata Elxsi, Moschip, Cyient DLM', BLUE),
        ('LAYER 3\nCloud & IT AI Services', 'GenAI Services, Cloud AI, AI Product Engineering, AI Testing',
         'Persistent, Coforge, Tech Mahindra, LTIM, Mphasis, Happiest Minds, Latent View', HexColor('#1F618D')),
        ('LAYER 4\nAI Applications', 'FinTech AI, HR AI, Food/Commerce AI, BPM AI, AdTech AI, TravelTech AI',
         'Zomato, Naukri, Affle, Newgen, Intellect Design, RateGain', TEAL),
        ('LAYER 5\nTelecom AI Enablers', '5G AI Delivery Networks, Enterprise AI Pipes, Edge AI',
         'Bharti Airtel, Reliance Industries', HexColor('#0E5F4B')),
        ('LAYER 6\nDefence AI', 'AI Radar, Counter-Drone AI, Military Simulation AI, Space AI',
         'BEL, Zen Technologies, Data Patterns, MTAR Technologies', HexColor('#4A235A')),
    ]

    rows = [[
        Paragraph('<b>Value Chain Layer</b>', ParagraphStyle('ch', fontSize=9, textColor=WHITE, fontName='Helvetica-Bold')),
        Paragraph('<b>AI Activities</b>', ParagraphStyle('ch2', fontSize=9, textColor=WHITE, fontName='Helvetica-Bold')),
        Paragraph('<b>Key Companies Covered</b>', ParagraphStyle('ch3', fontSize=9, textColor=WHITE, fontName='Helvetica-Bold')),
    ]]
    for layer, activities, companies, color in chain:
        rows.append([
            Paragraph(layer.replace('\n', '<br/>'), ParagraphStyle('cl', fontSize=8.5, textColor=WHITE, fontName='Helvetica-Bold', leading=12)),
            Paragraph(activities, ParagraphStyle('ca', fontSize=8, textColor=DGRAY, fontName='Helvetica', leading=12)),
            Paragraph(companies,  ParagraphStyle('cc', fontSize=8, textColor=DGRAY, fontName='Helvetica-Oblique', leading=12)),
        ])

    ct = Table(rows, colWidths=[115, 185, 212])
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TOPPADDING', (0,0),(-1,-1), 7),
        ('BOTTOMPADDING', (0,0),(-1,-1), 7),
        ('LEFTPADDING', (0,0),(-1,-1), 8),
        ('RIGHTPADDING', (0,0),(-1,-1), 8),
        ('GRID', (0,0),(-1,-1), 0.4, MGRAY),
        ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
    ]
    for i, (_, _, _, color) in enumerate(chain):
        style_cmds.append(('BACKGROUND', (0, i+1), (0, i+1), color))
        style_cmds.append(('TEXTCOLOR', (0, i+1), (0, i+1), WHITE))
        bg = LGRAY if i % 2 == 0 else WHITE
        style_cmds.append(('BACKGROUND', (1, i+1), (2, i+1), bg))
    ct.setStyle(TableStyle(style_cmds))
    story.append(ct)
    story.append(PageBreak())


# ── Company Profile Block ──────────────────────────────────────────────────────
RULE_LABELS = {
    'uptrend':      'Uptrend',
    'volume':       'Volume',
    'not_extended': 'Not Extended',
    'theme':        'Strong Theme',
    'structure':    'Chart Structure',
    'rel_strength': 'Relative Strength',
    'liquidity':    'Liquidity',
    'entry':        'Entry Signal',
}

def company_block(c, styles):
    elements = []
    avg = c['avg']
    verdict = c['verdict']
    vcl = verdict_clr(verdict)
    acl = score_clr(avg)

    # Company header bar
    hdr_data = [[
        Paragraph(f'<b>{c["name"]}</b>  <font size="9" color="#AEB6BF">({c["ticker"]} | NSE)</font>',
                  ParagraphStyle('cn', fontSize=11, textColor=WHITE, fontName='Helvetica-Bold')),
        Paragraph(f'{c["cap"]}<br/><font size="8">{c["mcap"]}</font>',
                  ParagraphStyle('cap', fontSize=8.5, textColor=GOLD, fontName='Helvetica-Bold', alignment=TA_CENTER, leading=12)),
        Paragraph(verdict,
                  ParagraphStyle('vd', fontSize=9, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        Paragraph(f'AVG: {avg}/5',
                  ParagraphStyle('avg', fontSize=10, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
    ]]
    ht = Table(hdr_data, colWidths=[230, 80, 110, 72])
    ht.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('BACKGROUND', (2, 0), (2, 0), vcl),
        ('BACKGROUND', (3, 0), (3, 0), acl),
        ('TOPPADDING', (0,0),(-1,-1), 6),
        ('BOTTOMPADDING', (0,0),(-1,-1), 6),
        ('LEFTPADDING', (0,0),(-1,-1), 8),
        ('RIGHTPADDING', (0,0),(-1,-1), 8),
        ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
    ]))
    elements.append(ht)

    # Description + Scores side-by-side
    desc_content = [
        Paragraph('<b>Business + AI Thesis</b>', styles['h3']),
        Paragraph(c['desc'], styles['body']),
        Spacer(1, 3),
        Paragraph(c['thesis'], ParagraphStyle('th', fontSize=8.5, textColor=TEAL, fontName='Helvetica-Oblique', leading=13)),
        Spacer(1, 5),
        Paragraph('<b>Key Strengths</b>', styles['h3']),
    ]
    for p in c['pros']:
        desc_content.append(Paragraph(f'✔  {p}', styles['bullet']))
    desc_content.append(Spacer(1, 4))
    desc_content.append(Paragraph('<b>Key Risks</b>', styles['h3']))
    for k in c['cons']:
        desc_content.append(Paragraph(f'⚠  {k}', styles['bullet']))

    # Scores column
    score_rows = [[
        Paragraph('<b>Rule</b>', ParagraphStyle('sr0', fontSize=7.5, textColor=WHITE, fontName='Helvetica-Bold')),
        Paragraph('<b>Score</b>', ParagraphStyle('sr1', fontSize=7.5, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        Paragraph('<b>Rating</b>', ParagraphStyle('sr2', fontSize=7.5, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
    ]]
    for key, label in RULE_LABELS.items():
        s = c['rules'][key]
        sc = score_clr(s)
        score_rows.append([
            Paragraph(label, ParagraphStyle('rl', fontSize=7.5, textColor=DGRAY, fontName='Helvetica', leading=10)),
            Paragraph(str(s), ParagraphStyle('sv', fontSize=8, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
            Paragraph(bars(s), ParagraphStyle('br', fontSize=7, textColor=sc, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        ])
    # Total row
    score_rows.append([
        Paragraph('<b>OVERALL</b>', ParagraphStyle('tot', fontSize=8, textColor=NAVY, fontName='Helvetica-Bold')),
        Paragraph(f'<b>{avg}</b>', ParagraphStyle('totv', fontSize=9, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        Paragraph(bars(round(avg)), ParagraphStyle('totb', fontSize=7, textColor=acl, fontName='Helvetica-Bold', alignment=TA_CENTER)),
    ])

    st = Table(score_rows, colWidths=[82, 28, 52])
    st_style = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('BACKGROUND', (0, -1), (-1, -1), LGRAY),
        ('TOPPADDING', (0,0),(-1,-1), 3),
        ('BOTTOMPADDING', (0,0),(-1,-1), 3),
        ('LEFTPADDING', (0,0),(-1,-1), 4),
        ('RIGHTPADDING', (0,0),(-1,-1), 4),
        ('GRID', (0,0),(-1,-1), 0.3, MGRAY),
        ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,-1),(-1,-1), 'Helvetica-Bold'),
    ]
    for i in range(1, len(score_rows)-1):
        s = list(c['rules'].values())[i-1]
        sc = score_clr(s)
        st_style.append(('BACKGROUND', (1, i), (1, i), sc))
        bg = WHITE if i % 2 == 0 else LGRAY
        st_style.append(('BACKGROUND', (0, i), (0, i), bg))
        st_style.append(('BACKGROUND', (2, i), (2, i), bg))
    st_style.append(('BACKGROUND', (1, -1), (1, -1), acl))
    st.setStyle(TableStyle(st_style))

    side_by_side = Table([[desc_content, st]], colWidths=[305, 162+45])  # adjusted
    side_by_side.setStyle(TableStyle([
        ('VALIGN', (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING', (0,0),(-1,-1), 6),
        ('LEFTPADDING', (0,0),(-1,-1), 6),
        ('RIGHTPADDING', (0,0),(-1,-1), 6),
        ('BACKGROUND', (0,0),(0,0), CREAM),
        ('BACKGROUND', (1,0),(1,0), WHITE),
        ('BOX', (0,0),(-1,-1), 0.5, MGRAY),
    ]))
    elements.append(side_by_side)
    elements.append(Spacer(1, 0.4*cm))
    return elements


# ── Segment Section ────────────────────────────────────────────────────────────
SEG_DESC = {
    'AI Infrastructure & Data Centers':
        'The physical foundation of AI — data centers, networking, fiber optic cables, and power infrastructure. '
        'India is investing massively in building sovereign AI infrastructure to serve both domestic and global hyperscaler demand.',
    'Semiconductor & Electronics Manufacturing':
        'India\'s semiconductor and electronics manufacturing ambitions are accelerating via PLI schemes and OSAT investments. '
        'These companies sit at the hardware layer of the AI stack — from chip design to device manufacturing.',
    'IT Services & Cloud AI (Large Cap)':
        'India\'s large IT services sector is pivoting aggressively to GenAI. These companies are building proprietary AI platforms, '
        'acquiring AI capabilities, and repositioning as AI-first digital transformation partners.',
    'IT Services & Cloud AI (Mid/Small Cap)':
        'Mid and small-cap IT companies often have more concentrated, specialized AI capabilities vs larger peers. '
        'Higher growth potential but also higher execution risk. Pure-play AI exposure with smaller scale.',
    'AI Applications & Platforms':
        'Consumer and enterprise AI applications represent the highest visible AI impact. These companies use AI as a core '
        'competitive moat — from food delivery optimization to financial process automation.',
    'Telecom AI Enablers':
        '5G networks are the delivery pipes for AI applications. Telecom companies are evolving from connectivity providers '
        'to AI platform providers. India\'s 5G rollout creates a unique AI + telecom convergence opportunity.',
    'Defence AI':
        'India\'s defence AI spending is growing rapidly with increasing indigenization mandate. Counter-drone AI, '
        'radar AI, military simulation AI, and space AI are priority areas. Strong government order visibility.',
}

def build_segments(story, styles):
    segs = {}
    for c in COMPANIES:
        segs.setdefault(c['seg'], []).append(c)

    for seg, companies in segs.items():
        # Segment header
        hdr = Table([[Paragraph(seg.upper(), ParagraphStyle('sh', fontSize=13, textColor=WHITE, fontName='Helvetica-Bold'))]],
                    colWidths=[W - 60])
        hdr.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(-1,-1), BLUE),
            ('TOPPADDING', (0,0),(-1,-1), 8),
            ('BOTTOMPADDING', (0,0),(-1,-1), 8),
            ('LEFTPADDING', (0,0),(-1,-1), 12),
        ]))
        story.append(KeepTogether([hdr]))
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(SEG_DESC.get(seg, ''), styles['intro']))
        story.append(Spacer(1, 0.3*cm))

        for c in companies:
            story.append(KeepTogether(company_block(c, styles)))

        story.append(PageBreak())


# ── Master Comparison Table ────────────────────────────────────────────────────
def build_comparison_table(story, styles):
    story.append(Paragraph('MASTER COMPARISON TABLE — ALL COMPANIES', styles['sec_hdr']))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        'Quick reference for all 30 companies. Sort by Overall Score to find highest conviction setups. '
        'Green = Excellent (4.5+), Teal = Good (3.5–4.4), Orange = Neutral (2.5–3.4), Red = Weak (<2.5).',
        styles['intro']
    ))
    story.append(Spacer(1, 0.3*cm))

    hdr = ['Company', 'Ticker', 'Cap', 'Uptrend', 'Volume', 'Not Ext', 'Theme', 'Structure', 'Rel.Str', 'Liquid', 'Entry', 'AVG', 'Verdict']
    rows = [hdr]
    for c in sorted(COMPANIES, key=lambda x: x['avg'], reverse=True):
        r = c['rules']
        rows.append([
            c['name'],
            c['ticker'],
            c['cap'].replace(' Cap', ''),
            r['uptrend'], r['volume'], r['not_extended'], r['theme'],
            r['structure'], r['rel_strength'], r['liquidity'], r['entry'],
            c['avg'],
            c['verdict'],
        ])

    col_w = [105, 65, 38, 32, 32, 32, 32, 38, 32, 32, 32, 28, 72]
    tbl = Table(rows, colWidths=col_w, repeatRows=1)

    ts = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7.5),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('TOPPADDING', (0,0),(-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 3.5),
        ('LEFTPADDING', (0,0),(-1,-1), 4),
        ('RIGHTPADDING', (0,0),(-1,-1), 4),
        ('GRID', (0, 0), (-1, -1), 0.3, MGRAY),
        ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
        ('ALIGN', (3,0),(11,-1), 'CENTER'),
        ('ALIGN', (12,0),(12,-1), 'CENTER'),
    ])

    for i, c in enumerate(sorted(COMPANIES, key=lambda x: x['avg'], reverse=True)):
        row_i = i + 1
        bg = WHITE if i % 2 == 0 else LGRAY
        ts.add('BACKGROUND', (0, row_i), (2, row_i), bg)
        ts.add('BACKGROUND', (12, row_i), (12, row_i), bg)

        # Color score cells
        rule_keys = ['uptrend', 'volume', 'not_extended', 'theme', 'structure', 'rel_strength', 'liquidity', 'entry']
        for j, key in enumerate(rule_keys):
            s = c['rules'][key]
            sc = score_clr(s)
            ts.add('BACKGROUND', (3+j, row_i), (3+j, row_i), sc)
            ts.add('TEXTCOLOR', (3+j, row_i), (3+j, row_i), WHITE)
            ts.add('FONTNAME', (3+j, row_i), (3+j, row_i), 'Helvetica-Bold')

        # Avg color
        ts.add('BACKGROUND', (11, row_i), (11, row_i), score_clr(c['avg']))
        ts.add('TEXTCOLOR', (11, row_i), (11, row_i), WHITE)
        ts.add('FONTNAME', (11, row_i), (11, row_i), 'Helvetica-Bold')

        # Verdict color
        vcl = verdict_clr(c['verdict'])
        ts.add('BACKGROUND', (12, row_i), (12, row_i), vcl)
        ts.add('TEXTCOLOR', (12, row_i), (12, row_i), WHITE)
        ts.add('FONTNAME', (12, row_i), (12, row_i), 'Helvetica-Bold')

    tbl.setStyle(ts)
    story.append(tbl)
    story.append(PageBreak())


# ── Top Picks Summary ─────────────────────────────────────────────────────────
TOP_PICKS = [
    dict(
        rank=1, name='Persistent Systems', ticker='PERSISTENT', cap='Large Cap',
        avg=4.5, verdict='BUY ON DIP', theme='AI-First IT Services',
        why='India IT sector\'s fastest growing company. SASVA GenAI platform creates productivity moat. '
            'Every GenAI services deal flows to Persistent. Buy any meaningful 10–15% dip from highs.',
        entry='Look for VCP or flag base formation. Ideal entry near 21-week EMA. '
              'Avoid buying at all-time highs without consolidation.',
        target='5-year conviction hold. Next re-rating when AI services reach 30%+ revenue.',
    ),
    dict(
        rank=2, name='Bharti Airtel', ticker='BHARTIARTL', cap='Large Cap',
        avg=4.5, verdict='BUY', theme='5G + AI Convergence',
        why='5G network becomes the AI delivery infrastructure of India. Airtel owns both the pipe and '
            'the enterprise AI platform. Consistent compounder with improving ARPU and AI monetization.',
        entry='Breakout from multi-month consolidation on volume confirmation. Flag patterns are common. '
              'EMA 8 > EMA 21 maintained in strong uptrend.',
        target='2–3 year hold. Monetization of enterprise AI = re-rating catalyst.',
    ),
    dict(
        rank=3, name='Coforge', ticker='COFORGE', cap='Large Cap',
        avg=3.9, verdict='BUY', theme='AI-Led Digital Transformation',
        why='Aggressive AI capability buildout via CIGNITI acquisition. Strong deal momentum in BFSI. '
            'Management credibility high. Improving margins + AI service differentiation = quality compounder.',
        entry='After consolidation from breakout. Cup & Handle formation typical. '
              'Volume confirmation on breakout from base critical.',
        target='2–3 year hold. Margin expansion from AI services premium pricing.',
    ),
    dict(
        rank=4, name='Dixon Technologies', ticker='DIXON', cap='Large Cap',
        avg=4.1, verdict='BUY ON PULLBACK', theme='AI Device Manufacturing',
        why='Every AI phone, AI PC, and AI TV manufactured in India passes through Dixon. PLI supercharges '
            'growth. Apple ecosystem entry is transformational. Structural multi-year volume story.',
        entry='Pull back to 21-week EMA or flat base. Avoid buying after strong gap-ups without base.',
        target='3–5 year hold as India becomes global AI device manufacturing hub.',
    ),
    dict(
        rank=5, name='Affle India', ticker='AFFLE', cap='Mid Cap',
        avg=3.9, verdict='BUY', theme='AI Mobile Marketing Platform',
        why='Proprietary CPCU AI model is a genuine technology moat. As mobile commerce in emerging '
            'markets accelerates, Affle\'s AI-powered platform compounds. Global expansion adding revenue.',
        entry='VCP or flag breakout with volume. Entry near 21-week EMA in uptrend context is ideal.',
        target='3–4 year hold. 30%+ revenue growth CAGR with margin expansion.',
    ),
    dict(
        rank=6, name='Zomato', ticker='ZOMATO', cap='Large Cap',
        avg=4.4, verdict='BUY ON DIP', theme='AI-Powered Quick Commerce',
        why='AI is the moat, not just a feature. Route optimization AI, demand forecasting AI, '
            'and personalization AI compound over time. Blinkit quick commerce is the next major growth '
            'vector. Profitability achieved = re-rating from growth to quality compounder.',
        entry='Buy meaningful dips (10–20% corrections). Flat base or Cup & Handle structures. '
              'Never chase 20%+ gap-ups.',
        target='5-year conviction hold for India\'s AI-powered consumer commerce leader.',
    ),
    dict(
        rank=7, name='Kaynes Technology', ticker='KAYNES', cap='Mid Cap',
        avg=4.1, verdict='BUY ON PULLBACK', theme='Semiconductor + Electronics Manufacturing',
        why='First Indian OSAT facility + IoT/AI hardware manufacturing. Intersection of India\'s '
            'semiconductor ambitions and AI hardware demand. High growth visibility from order book.',
        entry='Pull back to 50-day MA or flat base. OSAT news can create sharp gap-ups — wait for base.',
        target='3–5 year hold as OSAT facility ramps up operations.',
    ),
    dict(
        rank=8, name='Newgen Software', ticker='NEWGEN', cap='Mid Cap',
        avg=4.1, verdict='BUY ON PULLBACK', theme='AI Process Automation',
        why='Consistent 25%+ revenue growth with AI embedded in sticky BPM products. '
            'SaaS transition drives valuation re-rating. 500+ global BFSI clients = deep moat.',
        entry='Breakout from long consolidation with volume. Low daily liquidity requires patience — '
              'use limit orders. Not suitable for large position sizes.',
        target='3–4 year hold as SaaS revenue crosses 50% of total.',
    ),
]

def build_top_picks(story, styles):
    story.append(Paragraph('TOP 8 PICKS — HIGHEST CONVICTION AI VALUE CHAIN STOCKS', styles['sec_hdr']))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        'Based on the 8-rule evaluation framework, these companies score highest on the combination of '
        'AI theme strength, chart quality, liquidity, and relative performance. All technical signals '
        'must be confirmed with real-time charts before entering any position.',
        styles['intro']
    ))
    story.append(Spacer(1, 0.3*cm))

    for p in TOP_PICKS:
        acl = score_clr(p['avg'])
        vcl = verdict_clr(p['verdict'])

        hdr_data = [[
            Paragraph(f'<b>#{p["rank"]}  {p["name"]}</b>',
                      ParagraphStyle('ph', fontSize=11, textColor=WHITE, fontName='Helvetica-Bold')),
            Paragraph(p['ticker'], ParagraphStyle('pt', fontSize=9, textColor=GOLD, fontName='Helvetica-Bold', alignment=TA_CENTER)),
            Paragraph(p['cap'], ParagraphStyle('pc', fontSize=8.5, textColor=WHITE, fontName='Helvetica', alignment=TA_CENTER)),
            Paragraph(p['theme'], ParagraphStyle('pth', fontSize=8.5, textColor=GOLD, fontName='Helvetica-Oblique', alignment=TA_CENTER)),
            Paragraph(p['verdict'], ParagraphStyle('pv', fontSize=9, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
            Paragraph(f'Score: {p["avg"]}/5', ParagraphStyle('ps', fontSize=9, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        ]]
        ht = Table(hdr_data, colWidths=[155, 55, 65, 140, 90, 57])
        ht.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(-1,-1), NAVY),
            ('BACKGROUND', (4,0),(4,0), vcl),
            ('BACKGROUND', (5,0),(5,0), acl),
            ('TOPPADDING', (0,0),(-1,-1), 6),
            ('BOTTOMPADDING', (0,0),(-1,-1), 6),
            ('LEFTPADDING', (0,0),(-1,-1), 8),
            ('RIGHTPADDING', (0,0),(-1,-1), 6),
            ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
        ]))
        story.append(ht)

        body_data = [[
            [
                Paragraph('<b>Why This Stock?</b>', styles['h3']),
                Paragraph(p['why'], styles['body']),
                Spacer(1, 4),
                Paragraph('<b>Entry Strategy (verify with real-time chart)</b>', styles['h3']),
                Paragraph(p['entry'], styles['body']),
            ],
            [
                Paragraph('<b>Investment Horizon & Target</b>', styles['h3']),
                Paragraph(p['target'], styles['body']),
                Spacer(1, 8),
                Paragraph('<b>Score Visual</b>', styles['h3']),
                Paragraph(f'{bars(round(p["avg"]))}  {p["avg"]}/5',
                          ParagraphStyle('sc_vis', fontSize=14, textColor=acl, fontName='Helvetica-Bold')),
            ]
        ]]
        bt = Table(body_data, colWidths=[350, 212])
        bt.setStyle(TableStyle([
            ('VALIGN', (0,0),(-1,-1), 'TOP'),
            ('TOPPADDING', (0,0),(-1,-1), 8),
            ('LEFTPADDING', (0,0),(-1,-1), 10),
            ('RIGHTPADDING', (0,0),(-1,-1), 10),
            ('BACKGROUND', (0,0),(0,0), CREAM),
            ('BACKGROUND', (1,0),(1,0), LGREEN),
            ('BOX', (0,0),(-1,-1), 0.5, MGRAY),
            ('LINEAFTER', (0,0),(0,0), 0.5, MGRAY),
        ]))
        story.append(bt)
        story.append(Spacer(1, 0.5*cm))

    story.append(PageBreak())


# ── Segment Score Summary ─────────────────────────────────────────────────────
def build_segment_summary(story, styles):
    story.append(Paragraph('SEGMENT AVERAGE SCORES', styles['sec_hdr']))
    story.append(Spacer(1, 0.25*cm))

    segs = {}
    for c in COMPANIES:
        segs.setdefault(c['seg'], []).append(c['avg'])

    rows = [[
        Paragraph('<b>Segment</b>', ParagraphStyle('ssh', fontSize=9, textColor=WHITE, fontName='Helvetica-Bold')),
        Paragraph('<b>Companies</b>', ParagraphStyle('ssh2', fontSize=9, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        Paragraph('<b>Avg Score</b>', ParagraphStyle('ssh3', fontSize=9, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        Paragraph('<b>Assessment</b>', ParagraphStyle('ssh4', fontSize=9, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
    ]]

    seg_assessments = {
        'AI Infrastructure & Data Centers': 'Structural long-term play; needs patience for execution',
        'Semiconductor & Electronics Manufacturing': 'Multi-year winner; volatile short-term',
        'IT Services & Cloud AI (Large Cap)': 'Safe AI exposure; growth differentiation matters',
        'IT Services & Cloud AI (Mid/Small Cap)': 'Higher growth but verify liquidity & momentum',
        'AI Applications & Platforms': 'Strongest AI moats; wait for correct entries',
        'Telecom AI Enablers': 'Steady compounder; AI monetization is the re-rating trigger',
        'Defence AI': 'Strong government visibility; illiquidity of small caps is key risk',
    }

    for seg, scores in segs.items():
        avg = round(sum(scores) / len(scores), 1)
        acl = score_clr(avg)
        rows.append([
            Paragraph(seg, ParagraphStyle('sr', fontSize=8.5, textColor=DGRAY, fontName='Helvetica')),
            Paragraph(str(len(scores)), ParagraphStyle('sn', fontSize=8.5, textColor=DGRAY, fontName='Helvetica-Bold', alignment=TA_CENTER)),
            Paragraph(f'{avg}', ParagraphStyle('sa', fontSize=10, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
            Paragraph(seg_assessments.get(seg, ''), ParagraphStyle('sm', fontSize=8, textColor=DGRAY, fontName='Helvetica-Oblique')),
        ])

    t = Table(rows, colWidths=[185, 55, 65, 207])
    ts = TableStyle([
        ('BACKGROUND', (0,0),(-1,0), NAVY),
        ('TOPPADDING', (0,0),(-1,-1), 6),
        ('BOTTOMPADDING', (0,0),(-1,-1), 6),
        ('LEFTPADDING', (0,0),(-1,-1), 8),
        ('RIGHTPADDING', (0,0),(-1,-1), 8),
        ('GRID', (0,0),(-1,-1), 0.4, MGRAY),
        ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
    ])
    for i, (seg, scores) in enumerate(segs.items()):
        avg = round(sum(scores) / len(scores), 1)
        bg = WHITE if i % 2 == 0 else LGRAY
        ts.add('BACKGROUND', (0, i+1), (1, i+1), bg)
        ts.add('BACKGROUND', (3, i+1), (3, i+1), bg)
        ts.add('BACKGROUND', (2, i+1), (2, i+1), score_clr(avg))
        ts.add('TEXTCOLOR', (2, i+1), (2, i+1), WHITE)
    t.setStyle(ts)
    story.append(t)
    story.append(Spacer(1, 0.4*cm))

    # Mini notes
    notes = [
        '✔  Risk management matters most — position size based on conviction and liquidity',
        '✔  Avoid emotional entries — wait for proper base formations (VCP, Cup & Handle, Flat Base)',
        '✔  Great setups are usually obvious — if the chart looks messy, it probably is',
        '✔  Combine this report with real-time technical analysis before any trade execution',
        '✔  Diversify across segments — infrastructure, applications, and services to balance risk',
    ]
    box = Table(
        [[Paragraph(n, ParagraphStyle('note', fontSize=9, textColor=DGRAY, fontName='Helvetica', leading=14))] for n in notes],
        colWidths=[W - 60]
    )
    box.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), SGOLD),
        ('TOPPADDING', (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING', (0,0),(-1,-1), 14),
        ('BOX', (0,0),(-1,-1), 1.5, GOLD),
    ]))
    story.append(Paragraph('<b>MINI NOTES</b>', ParagraphStyle('mn_hdr', fontSize=10, textColor=NAVY, fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=4)))
    story.append(box)
    story.append(PageBreak())


# ── Disclaimer Page ───────────────────────────────────────────────────────────
def build_disclaimer(story, styles):
    story.append(Paragraph('IMPORTANT DISCLAIMER & METHODOLOGY NOTES', styles['sec_hdr']))
    story.append(Spacer(1, 0.5*cm))

    disclaimers = [
        ('NOT INVESTMENT ADVICE',
         'This report is prepared purely for educational and research purposes. Nothing in this document '
         'constitutes investment advice, a recommendation to buy or sell any security, or a solicitation '
         'to invest in any financial instrument. Always consult a SEBI-registered investment advisor '
         'before making investment decisions.'),
        ('DATA & ACCURACY',
         'Company descriptions, AI positioning, and qualitative scores are based on publicly available '
         'information and research analysis. Market cap figures are approximate. Financial data may have '
         'changed since the time of writing. Always verify with the latest annual reports, quarterly results, '
         'and stock exchange filings before any investment decision.'),
        ('TECHNICAL ANALYSIS CAVEAT',
         'Scores for Uptrend, Volume, Chart Structure, and Entry Signal are framework guidelines only. '
         'These require real-time chart verification using live market data, current EMAs, volume profiles, '
         'and actual price patterns. A score of 4–5 does not mean the stock is in a valid technical setup today.'),
        ('PAST PERFORMANCE',
         'Past stock performance does not guarantee future returns. AI sector stocks can be highly volatile '
         'and subject to rapid valuation changes based on technology shifts, competitive dynamics, and '
         'macroeconomic factors including interest rates, currency movements, and global tech sentiment.'),
        ('RISK MANAGEMENT',
         'Never invest more than you can afford to lose. Use stop-losses. Diversify across sectors and '
         'market caps. Small-cap and mid-cap stocks in this report may have significantly lower liquidity '
         'than large-caps — position sizing must account for this. Illiquid stocks can cause significant '
         'slippage on entry and exit.'),
        ('METHODOLOGY',
         'The 8-rule evaluation framework used in this report is adapted from a visual checklist for '
         'stock selection based on trend, volume, and chart structure principles. Scores are assigned '
         'qualitatively (1–5 scale) based on the author\'s assessment of each criterion for each company. '
         'Different analysts may reach different conclusions using the same framework.'),
    ]

    for title, text in disclaimers:
        box = Table([[
            Paragraph(f'<b>{title}</b>', ParagraphStyle('dt', fontSize=9, textColor=NAVY, fontName='Helvetica-Bold')),
            Paragraph(text, styles['disc']),
        ]], colWidths=[105, W - 60 - 105])
        box.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(0,0), LGRAY),
            ('BACKGROUND', (1,0),(1,0), WHITE),
            ('TOPPADDING', (0,0),(-1,-1), 8),
            ('BOTTOMPADDING', (0,0),(-1,-1), 8),
            ('LEFTPADDING', (0,0),(-1,-1), 10),
            ('RIGHTPADDING', (0,0),(-1,-1), 10),
            ('BOX', (0,0),(-1,-1), 0.5, MGRAY),
            ('LINEAFTER', (0,0),(0,0), 0.5, MGRAY),
            ('VALIGN', (0,0),(-1,-1), 'TOP'),
        ]))
        story.append(box)
        story.append(Spacer(1, 0.2*cm))

    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width='100%', thickness=1, color=NAVY))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        f'India AI Value Chain Report — 2026 Edition  |  Generated on {datetime.now().strftime("%B %d, %Y")}  |  '
        'For research use only. All trademarks and company names are property of their respective owners.',
        ParagraphStyle('footer_txt', fontSize=8, textColor=MGRAY, alignment=TA_CENTER, fontName='Helvetica-Oblique')
    ))


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    output_path = '/home/user/jarvizz/India_AI_Value_Chain_Report_2026.pdf'

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=30, rightMargin=30,
        topMargin=45, bottomMargin=35,
        title='India AI Value Chain Report 2026',
        author='AI Research Framework',
        subject='India AI Sector Stock Analysis',
    )

    styles = make_styles()
    story = []

    build_cover(story)
    build_framework(story, styles)
    build_chain_map(story, styles)
    build_segments(story, styles)
    build_comparison_table(story, styles)
    build_top_picks(story, styles)
    build_segment_summary(story, styles)
    build_disclaimer(story, styles)

    doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=draw_header_footer)
    print(f'✅ Report generated: {output_path}')
    return output_path


if __name__ == '__main__':
    main()
