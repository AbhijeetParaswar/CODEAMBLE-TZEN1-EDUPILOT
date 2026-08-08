from datetime import date, timedelta
from app.ingestion.base import BaseConnector, RawOpportunity


class NSPConnector(BaseConnector):
    """National Scholarship Portal — seed/sample data for MVP; production uses Playwright scraper."""

    source_id = "nsp"

    def fetch(self) -> list[RawOpportunity]:
        return [
            RawOpportunity(
                external_id="nsp-pm-yasasvi",
                source="nsp",
                title="PM Yasasvi Scholarship for OBC, EBC and DNT Students",
                description=(
                    "Central sector scheme for OBC, EBC and DNT category students studying in Class 9-12. "
                    "Amount: ₹75,000 per annum for Class 9-10 students; ₹1,25,000 per annum for Class 11-12 students. "
                    "Eligibility: students belonging to OBC, EBC or DNT communities with family income not exceeding "
                    "₹2,50,000 per annum, having scored at least 60% marks in previous examination. "
                    "Selection is based on PM YASASVI Entrance Test (PET). "
                    "Documents required: income certificate, caste certificate, Aadhaar card, bank passbook, previous marksheet. "
                    "Apply via the National Scholarship Portal at scholarships.gov.in."
                ),
                amount_min=75000,
                amount_max=125000,
                deadline=date.today() + timedelta(days=45),
                eligibility_rules={
                    "category": ["OBC", "EBC", "DNT"],
                    "max_income": 250000,
                    "min_percentage_12th": 60,
                    "states": ["ALL"],
                },
                documents_required=["income_certificate", "caste_certificate", "aadhaar", "bank_passbook"],
                application_url="https://scholarships.gov.in/",
                state_filter=["ALL"],
                tags=["central", "obc", "ebc", "dnt", "pre-matric", "pm-yasasvi"],
            ),
            RawOpportunity(
                external_id="nsp-post-matric-sc",
                source="nsp",
                title="Post Matric Scholarship for SC Students",
                description=(
                    "Financial assistance to Scheduled Caste (SC) students pursuing post-matriculation or post-secondary "
                    "stage courses in India, offered by the Ministry of Social Justice and Empowerment. "
                    "Amount: maintenance allowance + reimbursement of non-refundable fees; ranges from ₹10,000 to ₹50,000 per annum "
                    "depending on course level and hosteller/day-scholar status. "
                    "Eligibility: students belonging to SC category with family income not exceeding ₹2,50,000 per annum; "
                    "must be studying in Classes 11 and above (post-matriculation) at a recognized institution. "
                    "Documents required: caste certificate, income certificate, fee receipt, Aadhaar card, bank passbook. "
                    "Apply via the National Scholarship Portal at scholarships.gov.in."
                ),
                amount_min=10000,
                amount_max=50000,
                deadline=date.today() + timedelta(days=60),
                eligibility_rules={
                    "category": ["SC"],
                    "max_income": 250000,
                    "min_cgpa": 5.0,
                    "year_of_study": {"min": 1, "max": 4},
                    "states": ["ALL"],
                },
                documents_required=["caste_certificate", "income_certificate", "fee_receipt", "aadhaar"],
                application_url="https://scholarships.gov.in/",
                state_filter=["ALL"],
                tags=["central", "sc", "post-matric", "scheduled-caste"],
            ),
            RawOpportunity(
                external_id="nsp-merit-cum-means",
                source="nsp",
                title="Merit-cum-Means Scholarship for Professional Courses",
                description=(
                    "Scholarship for students from minority communities (Muslim, Christian, Sikh, Buddhist, Jain, Zoroastrian) "
                    "pursuing technical and professional UG or PG courses at a listed institution, "
                    "offered by the Ministry of Minority Affairs. "
                    "Amount: ₹20,000 per annum course fee + ₹10,000 per annum maintenance allowance for day scholars; "
                    "₹20,000 per annum course fee + ₹12,000 per annum for hostellers. "
                    "Eligibility: students from minority communities who have secured at least 50% marks in the previous "
                    "final examination; annual family income from all sources must not exceed ₹2,50,000. "
                    "Documents required: income certificate, marksheet, admission letter, Aadhaar card, bank passbook. "
                    "Apply via the National Scholarship Portal at scholarships.gov.in."
                ),
                amount_min=20000,
                amount_max=30000,
                deadline=date.today() + timedelta(days=30),
                eligibility_rules={
                    "category": ["Minority", "Muslim", "Christian", "Sikh", "Buddhist", "Jain", "Zoroastrian"],
                    "max_income": 250000,
                    "min_cgpa": 6.0,
                    "min_percentage": 50,
                    "streams": ["Engineering", "Medical", "Law", "Management", "Technical", "Professional"],
                    "states": ["ALL"],
                },
                documents_required=["income_certificate", "marksheet", "admission_letter", "aadhaar"],
                application_url="https://scholarships.gov.in/",
                state_filter=["ALL"],
                tags=["central", "minority", "merit", "professional", "muslim", "christian", "sikh"],
            ),
            # -----------------------------------------------------------------------
            # NEW: AICTE Swanath Scholarship
            # -----------------------------------------------------------------------
            RawOpportunity(
                external_id="nsp-aicte-swanath",
                source="nsp",
                title="AICTE Swanath Scholarship Scheme",
                description=(
                    "Scholarship offered by AICTE/Ministry of Education for orphans, wards of parents who died due to "
                    "Covid-19, wards of Armed Forces and Central Paramilitary Forces personnel martyred in action. "
                    "Amount: ₹50,000 per annum (lump sum covering college fee, books, equipment, clothing, etc.). "
                    "Eligibility: students studying in AICTE-approved Degree or Diploma institution; "
                    "family income must not exceed ₹8,00,000 per annum; "
                    "must not be receiving any other Central Government/State Government/AICTE scholarship simultaneously. "
                    "The scholarship is named 'Swanath' to honour the spirit of self-reliance for those who lost guardians. "
                    "Documents required: death certificate of parent, income certificate, admission letter, Aadhaar card, "
                    "bank passbook, self-declaration of no other scholarship. "
                    "Apply via the National Scholarship Portal at scholarships.gov.in."
                ),
                amount_min=50000,
                amount_max=50000,
                deadline=date.today() + timedelta(days=50),
                eligibility_rules={
                    "category": ["Orphan", "Covid-19 ward", "Armed Forces ward", "CAPF ward"],
                    "max_income": 800000,
                    "institution_type": ["AICTE-approved Degree", "AICTE-approved Diploma"],
                    "no_other_scholarship": True,
                    "states": ["ALL"],
                },
                documents_required=[
                    "death_certificate", "income_certificate", "admission_letter",
                    "aadhaar", "bank_passbook", "self_declaration",
                ],
                application_url="https://scholarships.gov.in/",
                state_filter=["ALL"],
                tags=["central", "aicte", "swanath", "orphan", "covid", "armed-forces", "capf", "degree", "diploma"],
            ),
            # -----------------------------------------------------------------------
            # NEW: Central Sector Scheme of Scholarships
            # -----------------------------------------------------------------------
            RawOpportunity(
                external_id="nsp-central-sector-scheme",
                source="nsp",
                title="Central Sector Scheme of Scholarships for College and University Students",
                description=(
                    "Scholarship offered by the Ministry of Education for students who scored above the 80th percentile "
                    "in Class XII board examinations and are pursuing regular degree courses at recognized colleges/universities. "
                    "Amount: ₹10,000 per annum for the first three years of undergraduate studies; "
                    "₹20,000 per annum for postgraduate studies. "
                    "Renewable annually subject to maintaining at least 60% marks or equivalent grade. "
                    "Eligibility: students scoring above 80th percentile in Class XII board exams; "
                    "annual family income not exceeding ₹4,50,000 per annum; "
                    "pursuing regular (not correspondence/distance) degree courses. "
                    "Income limit: family income must not exceed ₹4,50,000 per annum from all sources. "
                    "Documents required: Class XII marksheet, income certificate, Aadhaar card, bank passbook, college fee receipt. "
                    "Apply via the National Scholarship Portal at scholarships.gov.in."
                ),
                amount_min=10000,
                amount_max=20000,
                deadline=date.today() + timedelta(days=60),
                eligibility_rules={
                    "category": ["General", "OBC", "SC", "ST", "EWS"],
                    "max_income": 450000,
                    "min_percentile_12th": 80,
                    "states": ["ALL"],
                },
                documents_required=["marksheet_12th", "income_certificate", "aadhaar", "bank_passbook", "fee_receipt"],
                application_url="https://scholarships.gov.in/",
                state_filter=["ALL"],
                tags=["central", "merit", "ug", "pg", "80th-percentile", "college", "university"],
            ),
            # -----------------------------------------------------------------------
            # NEW: National Fellowship for Scheduled Tribe Students
            # -----------------------------------------------------------------------
            RawOpportunity(
                external_id="nsp-national-fellowship-st",
                source="nsp",
                title="National Fellowship for Scheduled Tribe Students (ST Fellowship)",
                description=(
                    "Fellowship offered by the Ministry of Tribal Affairs for Scheduled Tribe (ST) students pursuing "
                    "M.Phil and Ph.D. at UGC-recognized universities in India. "
                    "Amount: JRF rate ₹31,000 per month for the first two years; "
                    "SRF rate ₹35,000 per month for the remaining tenure; "
                    "contingency grant of ₹10,000 per annum (Humanities/Social Sciences) or ₹20,500 per annum (Sciences). "
                    "Eligibility: students belonging to Scheduled Tribe (ST) category; "
                    "must have cleared UGC-NET/JRF or have passed PG with minimum 55% marks; "
                    "not availing any other fellowship from the Government. "
                    "Documents required: caste certificate (ST), UGC-NET/JRF scorecard or PG marksheet, Aadhaar card, bank passbook. "
                    "Apply via the National Scholarship Portal at scholarships.gov.in."
                ),
                amount_min=31000,
                amount_max=35000,
                deadline=date.today() + timedelta(days=75),
                eligibility_rules={
                    "category": ["ST"],
                    "level": ["M.Phil", "Ph.D"],
                    "states": ["ALL"],
                },
                documents_required=["caste_certificate", "ugc_net_certificate", "marksheet", "aadhaar", "bank_passbook"],
                application_url="https://scholarships.gov.in/",
                state_filter=["ALL"],
                tags=["central", "st", "scheduled-tribe", "mphil", "phd", "fellowship", "research", "jrf", "srf"],
            ),
        ]

    def health_check(self) -> dict:
        return {"source": self.source_id, "status": "ok", "mode": "seed_data"}


class MahaDBTConnector(BaseConnector):
    source_id = "mahadbt"

    def fetch(self) -> list[RawOpportunity]:
        return [
            RawOpportunity(
                external_id="mahadbt-rajarshi-shahu",
                source="mahadbt",
                title="Rajarshi Shahu Maharaj Scholarship (Maharashtra)",
                description=(
                    "State scholarship offered by the Government of Maharashtra for students belonging to OBC, SEBC, "
                    "and VJNT (Vimukta Jati and Nomadic Tribes) communities pursuing higher education in Maharashtra. "
                    "Amount: ₹5,000 to ₹25,000 per annum depending on course and institution. "
                    "Eligibility: domicile of Maharashtra; caste certificate from OBC/SEBC/VJNT category; "
                    "family income not exceeding ₹8,00,000 per annum; minimum CGPA of 5.5 or equivalent percentage. "
                    "Documents required: domicile certificate, income certificate, caste certificate, Aadhaar card, bank passbook. "
                    "Apply via the MahaDBT portal at mahadbt.maharashtra.gov.in."
                ),
                amount_min=5000,
                amount_max=25000,
                deadline=date.today() + timedelta(days=40),
                eligibility_rules={
                    "category": ["OBC", "SEBC", "VJNT"],
                    "max_income": 800000,
                    "min_cgpa": 5.5,
                    "states": ["Maharashtra"],
                },
                documents_required=["domicile_certificate", "income_certificate", "caste_certificate"],
                application_url="https://mahadbt.maharashtra.gov.in/",
                state_filter=["Maharashtra"],
                tags=["state", "maharashtra", "obc", "sebc", "vjnt", "mahadbt"],
            ),
            RawOpportunity(
                external_id="mahadbt-ebc-scholarship",
                source="mahadbt",
                title="EBC Scholarship for Professional Courses (Maharashtra)",
                description=(
                    "Scholarship for Economically Backward Class (EBC) category students enrolled in professional "
                    "degree programs within Maharashtra, offered by the Government of Maharashtra through MahaDBT portal. "
                    "Amount: ₹15,000 to ₹40,000 per annum depending on course (Engineering, Pharmacy, Architecture). "
                    "Eligibility: students in EBC category with family income not exceeding ₹6,00,000 per annum; "
                    "minimum CGPA of 6.0 or equivalent; must be a Maharashtra domicile. "
                    "Applicable streams: Engineering, Pharmacy, Architecture. "
                    "Documents required: fee receipt, income certificate, Aadhaar card, bank passbook, domicile certificate. "
                    "Apply via the MahaDBT portal at mahadbt.maharashtra.gov.in."
                ),
                amount_min=15000,
                amount_max=40000,
                deadline=date.today() + timedelta(days=55),
                eligibility_rules={
                    "category": ["EBC"],
                    "max_income": 600000,
                    "min_cgpa": 6.0,
                    "streams": ["Engineering", "Pharmacy", "Architecture"],
                    "states": ["Maharashtra"],
                },
                documents_required=["fee_receipt", "income_certificate", "aadhaar", "bank_passbook"],
                application_url="https://mahadbt.maharashtra.gov.in/",
                state_filter=["Maharashtra"],
                tags=["state", "maharashtra", "ebc", "professional", "engineering", "pharmacy", "architecture"],
            ),
        ]

    def health_check(self) -> dict:
        return {"source": self.source_id, "status": "ok", "mode": "seed_data"}


class MySchemeConnector(BaseConnector):
    source_id = "myscheme"

    def fetch(self) -> list[RawOpportunity]:
        return [
            RawOpportunity(
                external_id="myscheme-nsp-bridge",
                source="myscheme",
                title="National Means-cum-Merit Scholarship (NMMS)",
                description=(
                    "Central government scholarship to encourage meritorious students from economically weaker sections "
                    "to continue their studies at the secondary stage without dropping out, offered by Ministry of HRD. "
                    "Amount: ₹12,000 per annum (₹1,000 per month) disbursed through DBT directly to student's bank account. "
                    "Eligibility: students who have passed Class VIII at recognized government or government-aided school "
                    "with at least 55% marks; family income not exceeding ₹3,50,000 per annum; "
                    "selection based on State Level Examination (SLE) conducted by State/UT governments. "
                    "Duration: Classes IX to XII (up to 4 years). "
                    "Documents required: income certificate, Class VIII marksheet, school certificate, Aadhaar card. "
                    "Apply via the National Scholarship Portal at scholarships.gov.in."
                ),
                amount_min=12000,
                amount_max=12000,
                deadline=date.today() + timedelta(days=90),
                eligibility_rules={
                    "category": ["General", "OBC", "SC", "ST", "EWS"],
                    "max_income": 350000,
                    "min_percentage_12th": 55,
                    "year_of_study": {"min": 8, "max": 12},
                    "states": ["ALL"],
                },
                documents_required=["income_certificate", "marksheet", "school_certificate"],
                application_url="https://www.myscheme.gov.in/schemes/nmms",
                state_filter=["ALL"],
                tags=["central", "merit", "school", "nmms", "class9", "class10", "class11", "class12"],
            ),
            RawOpportunity(
                external_id="myscheme-girls-scholarship",
                source="myscheme",
                title="Pragati Scholarship for Girl Students (Technical Degree)",
                description=(
                    "AICTE/Ministry of Education scheme for girl students enrolled in AICTE-approved technical degree programs "
                    "such as Engineering, Technology, Architecture, and Pharmacy. "
                    "Amount: up to ₹50,000 per annum covering tuition fee, incidentals, and book allowance. "
                    "Duration: maximum 4 years for first-year admitted students; maximum 3 years for second-year lateral-entry students. "
                    "Eligibility: girl students admitted in AICTE-approved technical degree programs; "
                    "family income not exceeding ₹8,00,000 per annum; minimum CGPA of 6.5. "
                    "Only two girl children per family can avail this scholarship. "
                    "Must not be receiving any other Government scholarship. "
                    "Documents required: admission letter, income certificate, Aadhaar card, bank passbook, previous marksheet, "
                    "self-declaration of no other scholarship. "
                    "Apply via the National Scholarship Portal at scholarships.gov.in."
                ),
                amount_min=50000,
                amount_max=50000,
                deadline=date.today() + timedelta(days=35),
                eligibility_rules={
                    "gender": ["Female"],
                    "max_income": 800000,
                    "min_cgpa": 6.5,
                    "streams": ["Engineering", "Technology", "Architecture", "Pharmacy"],
                    "states": ["ALL"],
                },
                documents_required=["admission_letter", "income_certificate", "aadhaar", "bank_passbook"],
                application_url="https://www.myscheme.gov.in/",
                state_filter=["ALL"],
                tags=["central", "girls", "women", "female", "technical", "aicte", "pragati", "degree",
                      "engineering", "technology"],
            ),
            # -----------------------------------------------------------------------
            # NEW: Pragati Scholarship (Diploma)
            # -----------------------------------------------------------------------
            RawOpportunity(
                external_id="myscheme-pragati-diploma",
                source="myscheme",
                title="Pragati Scholarship for Girl Students (Technical Diploma)",
                description=(
                    "AICTE/Ministry of Education scheme for girl students enrolled in AICTE-approved technical diploma programs. "
                    "Amount: up to ₹30,000 per annum covering tuition fee, incidentals, and book allowance. "
                    "Duration: maximum 3 years for first-year admitted students; maximum 2 years for second-year lateral-entry students. "
                    "Eligibility: girl students admitted in AICTE-approved technical diploma programs; "
                    "family income not exceeding ₹8,00,000 per annum. "
                    "Only two girl children per family can avail this scholarship. "
                    "Must not be receiving any other Government scholarship simultaneously. "
                    "Documents required: admission letter, income certificate, Aadhaar card, bank passbook, self-declaration. "
                    "Apply via the National Scholarship Portal at scholarships.gov.in."
                ),
                amount_min=30000,
                amount_max=30000,
                deadline=date.today() + timedelta(days=35),
                eligibility_rules={
                    "gender": ["Female"],
                    "max_income": 800000,
                    "institution_type": ["AICTE-approved Diploma"],
                    "states": ["ALL"],
                },
                documents_required=["admission_letter", "income_certificate", "aadhaar", "bank_passbook"],
                application_url="https://www.myscheme.gov.in/",
                state_filter=["ALL"],
                tags=["central", "girls", "women", "female", "technical", "aicte", "pragati", "diploma"],
            ),
            # -----------------------------------------------------------------------
            # NEW: Saksham Scholarship (differently-abled)
            # -----------------------------------------------------------------------
            RawOpportunity(
                external_id="myscheme-saksham-scholarship",
                source="myscheme",
                title="Saksham Scholarship for Specially-Abled Students (AICTE)",
                description=(
                    "AICTE/Ministry of Education scholarship for specially-abled (differently-abled) students "
                    "enrolled in AICTE-approved technical degree or diploma programs in India. "
                    "Amount: ₹50,000 per annum (for degree programs) covering tuition fee, books, equipment, and living expenses. "
                    "Eligibility: students with at least 40% disability (physically challenged, visually impaired, "
                    "hearing impaired, etc.) studying in AICTE-approved technical institutions; "
                    "family income not exceeding ₹8,00,000 per annum; "
                    "not receiving any other Central/State/AICTE scholarship. "
                    "Documents required: disability certificate (40%+ disability), income certificate, admission letter, "
                    "Aadhaar card, bank passbook. "
                    "Apply via the National Scholarship Portal at scholarships.gov.in."
                ),
                amount_min=50000,
                amount_max=50000,
                deadline=date.today() + timedelta(days=45),
                eligibility_rules={
                    "disability_min_percent": 40,
                    "max_income": 800000,
                    "institution_type": ["AICTE-approved Degree", "AICTE-approved Diploma"],
                    "states": ["ALL"],
                },
                documents_required=["disability_certificate", "income_certificate", "admission_letter", "aadhaar", "bank_passbook"],
                application_url="https://www.myscheme.gov.in/",
                state_filter=["ALL"],
                tags=["central", "aicte", "saksham", "disability", "specially-abled", "differently-abled",
                      "physically-challenged", "degree", "diploma"],
            ),
        ]

    def health_check(self) -> dict:
        return {"source": self.source_id, "status": "ok", "mode": "seed_data"}


class AICTEConnector(BaseConnector):
    """AICTE scholarships — seed data for schemes referenced in the golden eval dataset."""

    source_id = "aicte"

    def fetch(self) -> list[RawOpportunity]:
        return [
            # -----------------------------------------------------------------------
            # INSPIRE Scholarship for Higher Education (SHE) — DST
            # -----------------------------------------------------------------------
            RawOpportunity(
                external_id="aicte-inspire-she",
                source="aicte",
                title="INSPIRE Scholarship for Higher Education (SHE) — DST",
                description=(
                    "Scholarship offered by the Department of Science and Technology (DST), Government of India, "
                    "under the INSPIRE programme to attract talented students to study basic and natural sciences. "
                    "Amount: ₹80,000 per annum — comprising ₹60,000 annual scholarship plus ₹20,000 summer attachment grant "
                    "for research exposure at premier research institutes. "
                    "Eligibility: students who scored in the top 1% of Class XII board examinations; "
                    "pursuing B.Sc., B.S., B.Stat., B.Math., Integrated M.Sc., or M.S. in natural and basic sciences "
                    "(Physics, Chemistry, Mathematics, Biology, Statistics, Earth Sciences, etc.) at recognized institutions. "
                    "Not applicable for students pursuing Engineering, Medicine, or Technology programs. "
                    "Duration: up to 5 years (complete UG course). "
                    "Documents required: Class XII marksheet (showing top 1% rank), admission letter, Aadhaar card, bank passbook. "
                    "Apply at online.dst.gov.in/INSPIRE or through the DST INSPIRE portal."
                ),
                amount_min=80000,
                amount_max=80000,
                deadline=date.today() + timedelta(days=90),
                eligibility_rules={
                    "category": ["General", "OBC", "SC", "ST", "EWS"],
                    "min_percentile_12th": 99,  # top 1%
                    "streams": ["B.Sc", "B.S", "B.Stat", "B.Math", "M.Sc", "M.S",
                                "Physics", "Chemistry", "Mathematics", "Biology",
                                "Natural Sciences", "Basic Sciences"],
                    "states": ["ALL"],
                },
                documents_required=["marksheet_12th", "top_1_percent_certificate", "admission_letter", "aadhaar", "bank_passbook"],
                application_url="https://online.dst.gov.in/INSPIRE",
                state_filter=["ALL"],
                tags=["central", "dst", "inspire", "she", "bsc", "science", "natural-sciences",
                      "top-1-percent", "basic-sciences", "research"],
            ),
            # -----------------------------------------------------------------------
            # INSPIRE Fellowship (Ph.D)
            # -----------------------------------------------------------------------
            RawOpportunity(
                external_id="aicte-inspire-fellowship-phd",
                source="aicte",
                title="INSPIRE Fellowship for Ph.D in Science — DST",
                description=(
                    "Fellowship offered by the Department of Science and Technology (DST) under INSPIRE for students "
                    "pursuing Ph.D. in natural and basic sciences at any recognized university in India. "
                    "Amount: ₹20,000 per month fellowship + ₹20,000 per annum contingency grant for research expenses. "
                    "Eligibility: students enrolled in Ph.D. programs in natural sciences (Physics, Chemistry, Mathematics, "
                    "Biology, Earth Sciences, Statistics); must be INSPIRE Scholar (SHE) or cleared competitive exam "
                    "like GATE/CSIR-NET/JEST/JGEEBILS; aged below 32 years. "
                    "Duration: up to 5 years for Ph.D. completion. "
                    "Documents required: Ph.D. enrolment certificate, INSPIRE SHE certificate or NET/GATE scorecard, "
                    "supervisor certificate, Aadhaar card, bank passbook. "
                    "Apply at online.dst.gov.in/INSPIRE."
                ),
                amount_min=20000,
                amount_max=20000,
                deadline=date.today() + timedelta(days=90),
                eligibility_rules={
                    "category": ["General", "OBC", "SC", "ST", "EWS"],
                    "level": ["Ph.D"],
                    "streams": ["Physics", "Chemistry", "Mathematics", "Biology", "Earth Sciences",
                                "Natural Sciences", "Basic Sciences"],
                    "max_age": 32,
                    "states": ["ALL"],
                },
                documents_required=["phd_enrolment_certificate", "inspire_she_certificate", "net_gate_scorecard",
                                    "supervisor_certificate", "aadhaar", "bank_passbook"],
                application_url="https://online.dst.gov.in/INSPIRE",
                state_filter=["ALL"],
                tags=["central", "dst", "inspire", "phd", "fellowship", "research", "science",
                      "physics", "chemistry", "mathematics", "biology"],
            ),
            # -----------------------------------------------------------------------
            # Maulana Azad National Fellowship
            # -----------------------------------------------------------------------
            RawOpportunity(
                external_id="aicte-maulana-azad-fellowship",
                source="aicte",
                title="Maulana Azad National Fellowship for Minority Students",
                description=(
                    "Fellowship offered by the Ministry of Minority Affairs for students from minority communities "
                    "(Muslim, Christian, Sikh, Buddhist, Jain, Zoroastrian/Parsi) pursuing M.Phil and Ph.D. at "
                    "UGC-recognized universities in India. "
                    "Amount: JRF rate ₹31,000 per month for the first two years; "
                    "SRF rate ₹35,000 per month for the remaining tenure. "
                    "Contingency grant: ₹10,000 per annum for Humanities and Social Sciences; "
                    "₹20,500 per annum for Sciences, Engineering, and Technology. "
                    "HRA as per university norms is also provided. "
                    "Eligibility: students from Muslim, Christian, Sikh, Buddhist, Jain, or Zoroastrian minority communities; "
                    "must have passed postgraduate exam with minimum 55% marks (50% for SC/ST); "
                    "aged below 35 years; not availing any other fellowship. "
                    "Documents required: minority community certificate, PG marksheet, NET/JRF certificate (if applicable), "
                    "Aadhaar card, bank passbook, enrolment certificate from university. "
                    "Apply via UGC or the National Scholarship Portal."
                ),
                amount_min=31000,
                amount_max=35000,
                deadline=date.today() + timedelta(days=60),
                eligibility_rules={
                    "category": ["Minority", "Muslim", "Christian", "Sikh", "Buddhist", "Jain", "Zoroastrian", "Parsi"],
                    "level": ["M.Phil", "Ph.D"],
                    "min_percentage_pg": 55,
                    "max_age": 35,
                    "states": ["ALL"],
                },
                documents_required=["minority_certificate", "pg_marksheet", "net_jrf_certificate",
                                    "aadhaar", "bank_passbook", "enrolment_certificate"],
                application_url="https://scholarships.gov.in/",
                state_filter=["ALL"],
                tags=["central", "minority", "muslim", "christian", "sikh", "buddhist", "jain", "zoroastrian",
                      "maulana-azad", "fellowship", "mphil", "phd", "research", "jrf", "srf"],
            ),
            # -----------------------------------------------------------------------
            # ICAR Netaji Subhas International Fellowship
            # -----------------------------------------------------------------------
            RawOpportunity(
                external_id="aicte-icar-netaji-fellowship",
                source="aicte",
                title="Netaji Subhas-ICAR International Fellowship (Agriculture Research)",
                description=(
                    "Fellowship offered by the Indian Council of Agricultural Research (ICAR), Ministry of Agriculture "
                    "and Farmers Welfare, to develop human resources with advanced training in top international "
                    "agricultural research laboratories worldwide. "
                    "Objective: To expose Indian researchers/students to best agricultural research labs internationally, "
                    "and to attract overseas researchers to Indian Agricultural Universities (AUs). "
                    "Amount: fellowship covers international travel, accommodation, and research expenses as per host country rates. "
                    "Eligibility: Indian candidates in agriculture and allied sciences pursuing doctoral or post-doctoral "
                    "research; faculty at ICAR/State Agricultural Universities; merit-based selection. "
                    "The fellowship is named after Netaji Subhas Chandra Bose to honour his vision of self-reliance. "
                    "Fellows work in identified best laboratories worldwide for advanced research in agriculture, "
                    "horticulture, fisheries, animal sciences, and food technology. "
                    "Apply via the ICAR website at icar.gov.in."
                ),
                amount_min=0,
                amount_max=0,
                deadline=date.today() + timedelta(days=120),
                eligibility_rules={
                    "category": ["General", "OBC", "SC", "ST", "EWS"],
                    "level": ["Ph.D", "Post-doctoral", "Faculty"],
                    "streams": ["Agriculture", "Horticulture", "Fisheries", "Animal Sciences", "Food Technology"],
                    "states": ["ALL"],
                },
                documents_required=["research_proposal", "supervisor_recommendation", "marksheets",
                                    "aadhaar", "passport"],
                application_url="https://icar.gov.in/",
                state_filter=["ALL"],
                tags=["central", "icar", "netaji-subhas", "international", "fellowship", "agriculture",
                      "research", "phd", "postdoctoral", "horticulture", "fisheries"],
            ),
            # -----------------------------------------------------------------------
            # Dr. Ambedkar Central Sector Scheme — OBC/EBC Overseas Studies
            # -----------------------------------------------------------------------
            RawOpportunity(
                external_id="aicte-ambedkar-overseas",
                source="aicte",
                title="Dr. Ambedkar Central Sector Scheme for OBC/EBC Students (Overseas Studies)",
                description=(
                    "Central sector scheme by the Ministry of Social Justice and Empowerment for OBC and EBC students "
                    "pursuing Masters or Ph.D. at top-ranked universities abroad (World Ranking Top 500). "
                    "Amount: full financial support including visa fees, air tickets, academic fees, living expenses, "
                    "and contingency grant; total support up to ₹10-15 lakh per annum. "
                    "Eligibility: students belonging to OBC or Economically Backward Class (EBC) categories; "
                    "family income not exceeding ₹2,50,000 per annum for EBC, ₹8,00,000 for OBC; "
                    "admission secured in top-ranked (top 500) foreign university; "
                    "pursuing Masters or Ph.D. programme. "
                    "Documents required: admission letter from foreign university, university world ranking proof, "
                    "caste/EBC certificate, income certificate, Aadhaar card, passport. "
                    "Apply via Ministry of Social Justice and Empowerment portal."
                ),
                amount_min=1000000,
                amount_max=1500000,
                deadline=date.today() + timedelta(days=90),
                eligibility_rules={
                    "category": ["OBC", "EBC"],
                    "max_income_obc": 800000,
                    "max_income_ebc": 250000,
                    "level": ["Masters", "Ph.D"],
                    "institution_type": ["Top 500 World Ranking"],
                    "states": ["ALL"],
                },
                documents_required=["foreign_admission_letter", "university_ranking_proof",
                                    "caste_certificate", "income_certificate", "aadhaar", "passport"],
                application_url="https://socialjustice.gov.in/",
                state_filter=["ALL"],
                tags=["central", "obc", "ebc", "overseas", "abroad", "masters", "phd",
                      "ambedkar", "international-studies", "foreign-university"],
            ),
        ]

    def health_check(self) -> dict:
        return {"source": self.source_id, "status": "ok", "mode": "seed_data"}


class DevnarayanConnector(BaseConnector):
    """Rajasthan state scholarship connector — seed data."""

    source_id = "devnarayan"

    def fetch(self) -> list[RawOpportunity]:
        return [
            RawOpportunity(
                external_id="devnarayan-post-matric",
                source="devnarayan",
                title="Devnarayan Post Matric Scholarship (Rajasthan)",
                description=(
                    "Scholarship offered by the Government of Rajasthan for students belonging to the Banjara, Bairwa, "
                    "Balai, Bhatia and other specified backward class communities pursuing post-matriculation courses. "
                    "Benefits include reimbursement of maintenance allowance and tuition/non-refundable fees. "
                    "Amount: maintenance allowance ₹15,000–₹25,000 per annum + fee reimbursement depending on course level. "
                    "Eligibility: students belonging to Banjara/Bairwa/Balai/Bhatia (backward class) communities; "
                    "family income not exceeding ₹2,50,000 per annum; Rajasthan domicile; pursuing post-matric courses. "
                    "Documents required: caste certificate, income certificate, Aadhaar card, domicile certificate, "
                    "fee receipts, previous marksheet. "
                    "Apply through the Rajasthan state scholarship portal at sje.rajasthan.gov.in."
                ),
                amount_min=15000,
                amount_max=25000,
                deadline=date.today() + timedelta(days=50),
                eligibility_rules={
                    "category": ["Banjara", "Bairwa", "Balai", "Bhatia", "Backward Class"],
                    "max_income": 250000,
                    "states": ["Rajasthan"],
                },
                documents_required=["caste_certificate", "income_certificate", "aadhaar", "domicile_certificate",
                                    "fee_receipt", "marksheet"],
                application_url="https://sje.rajasthan.gov.in/",
                state_filter=["Rajasthan"],
                tags=["state", "rajasthan", "devnarayan", "banjara", "bairwa", "balai", "bhatia",
                      "backward-class", "post-matric"],
            ),
        ]

    def health_check(self) -> dict:
        return {"source": self.source_id, "status": "ok", "mode": "seed_data"}


class InternshalaSeeder(BaseConnector):
    """Seed internship data for MVP; production uses the Playwright-based InternshalaConnector."""

    source_id = "internshala"

    def fetch(self) -> list[RawOpportunity]:
        return [
            RawOpportunity(
                external_id="internshala-sde-intern-blr",
                source="internshala",
                title="Software Development Intern (Full-Stack)",
                description="Work with a fast-growing fintech startup building React + Node.js features. Own end-to-end feature delivery and code reviews. Ideal for 2nd/3rd-year CS/IT students.",
                amount_min=10000, amount_max=15000,
                deadline=date.today() + timedelta(days=20),
                eligibility_rules={"streams": ["Engineering", "Computer Science", "IT"], "year_of_study": {"min": 2, "max": 4}, "skills": ["HTML", "CSS", "JavaScript"], "states": ["ALL"]},
                documents_required=["resume", "college_id"],
                application_url="https://internshala.com/internship/detail/software-development-intern",
                state_filter=["ALL"], tags=["web", "react", "node", "full-stack"],
                raw_data={"company": "FinPay Technologies", "location": "Bengaluru (Remote)", "duration": "3 months"},
            ),
            RawOpportunity(
                external_id="internshala-ml-intern-pune",
                source="internshala",
                title="Machine Learning Intern",
                description="Join our AI lab to build NLP models for document classification using Python and HuggingFace transformers. Open to 3rd/4th-year B.Tech students with CGPA ≥ 7.0.",
                amount_min=12000, amount_max=20000,
                deadline=date.today() + timedelta(days=30),
                eligibility_rules={"streams": ["Engineering", "Computer Science", "Data Science"], "min_cgpa": 7.0, "year_of_study": {"min": 3, "max": 4}, "skills": ["Python", "Machine Learning"], "states": ["ALL"]},
                documents_required=["resume", "college_id"],
                application_url="https://internshala.com/internship/detail/machine-learning-intern",
                state_filter=["ALL"], tags=["ml", "ai", "python", "nlp"],
                raw_data={"company": "DocuAI Labs", "location": "Pune / Remote", "duration": "6 months"},
            ),
            RawOpportunity(
                external_id="internshala-ux-intern-remote",
                source="internshala",
                title="UI/UX Design Intern",
                description="Design mobile-first interfaces for our EdTech platform. Proficiency in Figma required. Portfolio submission mandatory.",
                amount_min=6000, amount_max=10000,
                deadline=date.today() + timedelta(days=35),
                eligibility_rules={"streams": ["Design", "Engineering", "Arts"], "year_of_study": {"min": 1, "max": 4}, "skills": ["Figma", "UI Design"], "states": ["ALL"]},
                documents_required=["resume", "portfolio_link"],
                application_url="https://internshala.com/internship/detail/ui-ux-design-intern",
                state_filter=["ALL"], tags=["design", "figma", "ux", "edtech", "remote"],
                raw_data={"company": "LearnSpark", "location": "Remote", "duration": "3 months"},
            ),
            RawOpportunity(
                external_id="internshala-android-intern-hyd",
                source="internshala",
                title="Android Development Intern",
                description="Build features for a consumer app (2M+ downloads) using Kotlin and Jetpack Compose. CS/IT students in 3rd or final year preferred.",
                amount_min=15000, amount_max=25000,
                deadline=date.today() + timedelta(days=22),
                eligibility_rules={"streams": ["Engineering", "Computer Science", "IT"], "min_cgpa": 6.5, "year_of_study": {"min": 3, "max": 4}, "skills": ["Kotlin", "Android", "Java"], "states": ["ALL"]},
                documents_required=["resume", "college_id"],
                application_url="https://internshala.com/internship/detail/android-development-intern",
                state_filter=["ALL"], tags=["android", "kotlin", "mobile"],
                raw_data={"company": "ShopNow App", "location": "Hyderabad", "duration": "4 months"},
            ),
            RawOpportunity(
                external_id="internshala-hr-intern-chennai",
                source="internshala",
                title="HR & Talent Acquisition Intern",
                description="Support campus hiring drives, screen CVs, schedule interviews, and onboard new hires. MBA/BBA or any stream with strong communication skills welcome.",
                amount_min=7000, amount_max=10000,
                deadline=date.today() + timedelta(days=18),
                eligibility_rules={"streams": ["Management", "Commerce", "Arts", "Engineering"], "year_of_study": {"min": 2, "max": 4}, "states": ["ALL"]},
                documents_required=["resume"],
                application_url="https://internshala.com/internship/detail/hr-talent-acquisition-intern",
                state_filter=["ALL"], tags=["hr", "recruitment", "management"],
                raw_data={"company": "HireHub Solutions", "location": "Chennai / Remote", "duration": "3 months"},
            ),
        ]

    def health_check(self) -> dict:
        return {"source": self.source_id, "status": "ok", "mode": "seed_data"}
