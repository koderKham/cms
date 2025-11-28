from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, PasswordField, DateTimeField, SubmitField, FileField, TextAreaField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
import datetime
now = datetime.datetime.utcnow()

class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# --- CaseForm (excerpt) ---
# Update your CaseForm in forms.py to include the criminal fields.

class CaseForm(FlaskForm):
    CASE_TYPE_CHOICES = [
        ('', 'Select case type...'),
        ('personal_injury', 'Personal Injury'),
        ('criminal', 'Criminal'),
        ('estate', 'Probate / Estate Planning'),
        ('other', 'Other / General Matter'),
    ]


    # -----------------------
    # Personal Injury
    # -----------------------

        # Core Case Info
    case_title = StringField("Case Title")
    case_number_internal = StringField("Case Number (Internal)")
    case_type = SelectField("Case Type", choices=[
        ("", ""),
        ("Auto Accident", "Auto Accident"),
        ("Slip & Fall", "Slip & Fall"),
        ("Premises Liability", "Premises Liability"),
        ("Negligent Security", "Negligent Security"),
        ("Dog Bite", "Dog Bite"),
        ("Commercial Vehicle", "Commercial Vehicle"),
    ])
    doi = DateField("Date of Incident")
    incident_address = StringField("Incident Address")
    incident_city_county = StringField("City / County")
    jurisdiction = StringField("Jurisdiction (Court/County)")
    police_report_number = StringField("Police Report #")
    law_enforcement_agency = StringField("Law Enforcement Agency")
    liability_admitted = SelectField("Is Liability Admitted?",
                                     choices=[("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")])

    # Client Info
    client_name = StringField("Client Name")
    client_dob = DateField("Client DOB")
    client_address = StringField("Client Address")
    client_phone = StringField("Client Phone")
    client_alt_phone = StringField("Client Alt Phone")
    client_email = EmailField("Client Email")
    client_dl = StringField("Client DL")
    client_insurer = StringField("Client Insurance Company")
    client_policy = StringField("Client Policy #")
    client_claim = StringField("Client Claim #")
    medpay_coverage = SelectField("Med Pay Coverage?",
                                  choices=[("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")])
    pip_active = SelectField("PIP Active?",
                             choices=[("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")])
    pip_limits = StringField("PIP Policy Limits")

    # Defendant Info
    defendant_name = StringField("Defendant Name")
    defendant_address = StringField("Defendant Address")
    defendant_contact = StringField("Defendant Phone/Email")
    defendant_dl = StringField("Defendant DL")
    def_vehicle_year = StringField("Vehicle Year")
    def_vehicle_make = StringField("Vehicle Make")
    def_vehicle_model = StringField("Vehicle Model")
    def_insurer = StringField("Defendant Insurance Company")
    def_policy = StringField("Defendant Policy #")
    def_claim = StringField("Defendant Claim #")
    def_bi_limits = StringField("Bodily Injury Limits")
    adjuster_name = StringField("Adjuster Name")
    adjuster_phone = StringField("Adjuster Phone")
    adjuster_email = EmailField("Adjuster Email")
    defendant_is_commercial = SelectField("Is Defendant Commercial/Corporate?",
                                          choices=[("", ""), ("Yes", "Yes"), ("No", "No")])
    business_name = StringField("Business Name")
    registered_agent = StringField("Registered Agent")

    # Witness Info
    witnesses = TextAreaField("Witnesses")
    witness_statement_taken = SelectField("Statement Taken?", choices=[("", ""), ("Yes", "Yes"), ("No", "No"),
                                                                       ("In Progress", "In Progress")])
    witness_liability_support = SelectField("Liability Support",
                                            choices=[("", ""), ("Strong", "Strong"), ("Moderate", "Moderate"),
                                                     ("Weak", "Weak"), ("Unknown", "Unknown")])

    # Medical Providers
    hospital_er = StringField("Hospital / ER")
    ems_transport = SelectField("EMS / Fire Rescue Transport?", choices=[("", ""), ("Yes", "Yes"), ("No", "No")])
    initial_visit_date = DateField("Initial Visit Date")
    chiropractor = StringField("Chiropractor")
    orthopedic = StringField("Orthopedic")
    neurologist = StringField("Neurologist")
    mri_center = StringField("MRI/Imaging Center")
    pain_management = StringField("Pain Management")
    surgery_center = StringField("Surgery Center")
    total_med_bills = StringField("Total Medical Bills to Date")
    outstanding_balances = StringField("Outstanding Balances")
    lops = TextAreaField("Letters of Protection (LOPs)")

    # Injury Areas
    injury_neck = BooleanField("Neck")
    injury_back = BooleanField("Back")
    injury_shoulder = BooleanField("Shoulder")
    injury_knee = BooleanField("Knee")
    injury_concussion = BooleanField("Concussion")
    injury_fracture = BooleanField("Fractures")
    injury_scars = BooleanField("Scars")
    injury_headaches = BooleanField("Headaches")
    injury_radiating = BooleanField("Radiating Pain")
    injury_loc = BooleanField("Loss of Consciousness")
    injury_ptd = BooleanField("PTD")
    prior_related_injuries = SelectField("Prior Related Injuries?",
                                         choices=[("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")])
    prior_accidents = SelectField("Prior Accidents?",
                                  choices=[("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")])
    injury_notes = TextAreaField("Injury Details / Notes")

    # Property Damage
    total_loss = SelectField("Total Loss?", choices=[("", ""), ("Yes", "Yes"), ("No", "No")])
    repair_estimate = StringField("Repair Estimate")
    photos_uploaded = SelectField("Photos Uploaded?",
                                  choices=[("", ""), ("Yes", "Yes"), ("No", "No"), ("Pending", "Pending")])
    rental_car = SelectField("Rental Car Provided?",
                             choices=[("", ""), ("Yes", "Yes"), ("No", "No"), ("Requested", "Requested")])
    tow_storage_location = StringField("Vehicle Stored/Towed Location")
    diminished_value_claim = SelectField("Diminished Value Claim?",
                                         choices=[("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")])

    # Insurance Communication Log
    demand_sent_date = DateField("Demand Sent Date")
    initial_offer = StringField("Initial Offer")
    coverage_disclosure_sent = SelectField("Coverage Disclosure Request Sent?",
                                           choices=[("", ""), ("Yes", "Yes"), ("No", "No")])
    bi_disclosure_received = SelectField("BI Policy Disclosure Received?",
                                         choices=[("", ""), ("Yes", "Yes"), ("No", "No"), ("Partial", "Partial")])
    negotiation_notes = TextAreaField("Negotiation Notes")

    # Document Tracking
    doc_retainer = BooleanField("Retainer Signed")
    doc_hipaa = BooleanField("HIPAA Authorization")
    doc_lops = BooleanField("LOPs")
    doc_med_records = BooleanField("Medical Records Received")
    doc_med_bills = BooleanField("Medical Bills Received")
    doc_demand_pkg = BooleanField("Demand Package")
    doc_ins_correspondence = BooleanField("Insurance Correspondence")
    doc_lien_letters = BooleanField("Lien Letters (HMO/Medicare/Medicaid)")

    # Litigation
    court_case_number = StringField("Court Case #")
    division = StringField("Division")
    opposing_counsel = StringField("Opposing Counsel")
    opp_counsel_contact = StringField("Opposing Counsel Contact")
    complaint_filed_date = DateField("Complaint Filed Date")
    service_status = SelectField("Service Status",
                                 choices=[("", ""), ("Not Served", "Not Served"), ("Served", "Served"),
                                          ("Substitute Service", "Substitute Service"),
                                          ("Service Waived", "Service Waived")])
    answer_filed_date = DateField("Defendant's Answer Filed Date")
    mediation_date = DateField("Mediation Date")
    trial_date = DateField("Trial Date")
    litigation_notes = TextAreaField("Discovery / Depositions / Motions / Experts")

    # Settlement/Closing
    gross_settlement = StringField("Gross Settlement Amount")
    medical_liens = StringField("Medical Liens")
    attorney_fees = StringField("Attorney Fees")
    costs = StringField("Costs")
    net_to_client = StringField("Net to Client")
    disbursement_date = DateField("Disbursement Date")
    release_signed = SelectField("Release Signed?", choices=[("", ""), ("Yes", "Yes"), ("No", "No")])
    settlement_check_received = SelectField("Settlement Check Received?",
                                            choices=[("", ""), ("Yes", "Yes"), ("No", "No"),
                                                     ("Pending", "Pending")])

    # File Management
    assigned_attorney = StringField("Assigned Attorney")
    assigned_paralegal = StringField("Assigned Paralegal")
    case_status = SelectField("Status", choices=[("", ""), ("Intake", "Intake"), ("Pre-suit", "Pre-suit"),
                                                 ("Treatment Ongoing", "Treatment Ongoing"),
                                                 ("Demand in Progress", "Demand in Progress"),
                                                 ("Negotiations", "Negotiations"), ("Litigation", "Litigation"),
                                                 ("Settled", "Settled"), ("Closed", "Closed")])
    important_notes = TextAreaField("Important Notes")
    followup_reminders = TextAreaField("Follow-up Reminders")
    submit = SubmitField("Save Case")
    # -----------------------
    # Criminal
    # -----------------------
 # Core Case Info
    case_title = StringField("Case Title")
    court_case_number = StringField("Court Case #")
    internal_case_number = StringField("Internal Case #")
    jurisdiction = StringField("Jurisdiction (County / Court)")
    case_level = SelectField("Case Level", choices=[
        ("", ""), ("Felony", "Felony"), ("Misdemeanor", "Misdemeanor"), ("Juvenile", "Juvenile"),
        ("Traffic Criminal", "Traffic Criminal"), ("Violation of Probation", "Violation of Probation")
    ])
    case_type = SelectField("Case Type", choices=[
        ("", ""), ("Drug Offense", "Drug Offense"), ("Violent Crime", "Violent Crime"),
        ("Theft / Property", "Theft / Property"), ("DUI", "DUI"), ("Domestic Violence", "Domestic Violence"),
        ("Sex Offense", "Sex Offense"), ("Weapons / Firearm", "Weapons / Firearm"), ("Other", "Other")
    ])
    division = StringField("Division")
    judge = StringField("Judge")
    prosecutor = StringField("Prosecutor / ASA")
    arresting_agency = StringField("Arresting Agency")
    offense_date = DateField("Offense Date")
    arrest_date = DateField("Arrest Date")
    case_status = SelectField("Current Case Status", choices=[
        ("", ""), ("Pre-Filing / Investigation", "Pre-Filing / Investigation"),
        ("Filed - Pretrial", "Filed - Pretrial"), ("Awaiting Plea", "Awaiting Plea"),
        ("Set for Trial", "Set for Trial"),
        ("Post-Conviction / Appeal", "Post-Conviction / Appeal"), ("Closed", "Closed")
    ])

    # Defendant Info
    def_name = StringField("Defendant Name")
    def_aliases = StringField("Aliases / AKA")
    def_dob = DateField("DOB")
    def_address = StringField("Address")
    def_phone = StringField("Phone")
    def_email = EmailField("Email")
    def_dl = StringField("Driver License #")
    def_ssn_last4 = StringField("SSN (Last 4)")
    def_employment = StringField("Employment")
    def_education = StringField("Education")
    immigration_status = SelectField("Immigration Status", choices=[
        ("", ""), ("U.S. Citizen", "U.S. Citizen"), ("Permanent Resident", "Permanent Resident"),
        ("Non-Immigrant Visa", "Non-Immigrant Visa"), ("Undocumented / Unknown", "Undocumented / Unknown")
    ])
    primary_language = StringField("Primary Language")
    contact_preference = SelectField("Contact Preference", choices=[
        ("", ""), ("Phone", "Phone"), ("Text", "Text"), ("Email", "Email"), ("Mail", "Mail")
    ])

    # Charges
    primary_charge = StringField("Primary Charge")
    primary_statute = StringField("Statute")
    primary_degree = SelectField("Degree", choices=[
        ("", ""), ("Capital Felony", "Capital Felony"), ("Life Felony", "Life Felony"),
        ("1st Degree Felony", "1st Degree Felony"), ("2nd Degree Felony", "2nd Degree Felony"),
        ("3rd Degree Felony", "3rd Degree Felony"), ("1st Degree Misdemeanor", "1st Degree Misdemeanor"),
        ("2nd Degree Misdemeanor", "2nd Degree Misdemeanor"), ("Other", "Other")
    ])
    primary_max_penalty = StringField("Max Penalty (Guideline / Statutory)")
    additional_charges = TextAreaField("Additional Charges (counts, statutes, degrees)")
    offense_date_range = StringField("Offense Date Range (if applicable)")
    enhancements = SelectField("Enhancements", choices=[
        ("", ""), ("HFO / PRR / Career Criminal", "HFO / PRR / Career Criminal"),
        ("Drug Trafficking Minimums", "Drug Trafficking Minimums"),
        ("DV Enhancement", "DV Enhancement"), ("Firearm Minimums (10-20-Life)", "Firearm Minimums (10-20-Life)"),
        ("Sexual Offense Registration", "Sexual Offense Registration"), ("None / Unknown", "None / Unknown")
    ])
    score_sheet_needed = SelectField("Score Sheet Needed?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])

    # Arrest/Procedural History
    arrest_type = SelectField("Arrest Type", choices=[
        ("", ""), ("On-View Arrest", "On-View Arrest"), ("Warrant", "Warrant"), ("Capias", "Capias"),
        ("Notice to Appear", "Notice to Appear")
    ])
    booking_number = StringField("Booking Number")
    first_appearance_date = DateField("First Appearance Date")
    arraignment_date = DateField("Arraignment Date")
    procedural_history = TextAreaField("Procedural History (key events)")

    # Custody & Bond
    in_custody = SelectField("In Custody?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Released", "Released")
    ])
    custody_location = StringField("Custody Location / Jail")
    inmate_number = StringField("Inmate #")
    bond_amount = StringField("Bond Amount")
    bond_type = SelectField("Bond Type", choices=[
        ("", ""), ("Monetary", "Monetary"), ("ROR", "ROR"), ("Pretrial Services", "Pretrial Services"),
        ("No Bond", "No Bond")
    ])
    bond_status = SelectField("Bond Status", choices=[
        ("", ""), ("Not Posted", "Not Posted"), ("Posted", "Posted"), ("Revoked", "Revoked")
    ])
    bond_hearing_date = DateField("Next Bond Hearing")
    release_conditions = TextAreaField("Release Conditions (no contact, GPS, curfew, etc.)")

    # Victim & Co-Defendants
    victim_info = TextAreaField("Victim Name(s) & Contact")
    victim_position = TextAreaField("Victim Position (wants prosecution, neutral, recanting)")
    no_contact_order = SelectField("No Contact Order?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Modified", "Modified")
    ])
    dv_injunction = SelectField("DV Injunction / Other Injunction?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Pending", "Pending")
    ])
    codef_info = TextAreaField("Co-Defendants (names, case #s, attorneys)")

    # Evidence Summary
    evidence_police_reports = BooleanField("Police Reports")
    evidence_bodycam = BooleanField("Bodycam / Dashcam")
    evidence_911 = BooleanField("911 Calls")
    evidence_witness_statements = BooleanField("Witness Statements")
    evidence_lab_reports = BooleanField("Lab / Forensic Reports")
    evidence_photos = BooleanField("Photos / Video")
    evidence_search_warrants = BooleanField("Search Warrants / Affidavits")
    evidence_phone_records = BooleanField("Phone / Cell Site Records")
    evidence_other = BooleanField("Other Significant Evidence")
    evidence_summary = TextAreaField("Evidence Summary / Issues")

    # Prior Criminal History
    prior_felonies = SelectField("Prior Felonies?", choices=[
        ("", ""), ("None", "None"), ("1–2", "1–2"), ("3 or more", "3 or more"), ("Unknown", "Unknown")
    ])
    prior_misdemeanors = SelectField("Prior Misdemeanors?", choices=[
        ("", ""), ("None", "None"), ("1–2", "1–2"), ("3 or more", "3 or more"), ("Unknown", "Unknown")
    ])
    prior_juvenile = SelectField("Juvenile History?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])
    on_probation = SelectField("On Probation / Community Control at Arrest?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])
    pending_cases = SelectField("Other Pending Cases?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])
    priors_affecting_sentence = SelectField("Priors Affecting Minimum/Score?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])
    prior_history_notes = TextAreaField("Criminal History Details")

    # Motions & Defense Strategy
    motion_suppress = BooleanField("Motion to Suppress")
    motion_dismiss = BooleanField("Motion to Dismiss")
    motion_compel = BooleanField("Motion to Compel Discovery")
    motion_bond = BooleanField("Motion to Set/Modify")
    # -----------------------
    # Probate / Estate Planning
    # -----------------------
    # Core Information
    case_title = StringField("Case Title")
    court_case_number = StringField("Court Case #")
    internal_case_number = StringField("Internal Case #")
    jurisdiction = StringField("Jurisdiction (County / Division)")
    case_type = SelectField("Case Type", choices=[
        ("", ""), ("Formal Administration", "Formal Administration"),
        ("Summary Administration", "Summary Administration"),
        ("Ancillary Administration", "Ancillary Administration"),
        ("Trust Administration", "Trust Administration"),
        ("Guardianship", "Guardianship"),
        ("Estate Planning Only", "Estate Planning Only")
    ])
    referral_source = StringField("Referral Source")
    primary_contact = StringField("Primary Client Contact Name")
    primary_contact_phone = StringField("Phone")
    primary_contact_email = EmailField("Email")
    matter_notes = TextAreaField("Brief Description of Matter")

    # Decedent Info
    decedent_name = StringField("Decedent Name")
    decedent_dob = DateField("Date of Birth")
    decedent_dod = DateField("Date of Death")
    decedent_last_address = StringField("Last Residence Address")
    decedent_county = StringField("County of Domicile")
    decedent_ssn_last4 = StringField("SSN (Last 4)")
    marital_status_at_death = SelectField("Marital Status at Death", choices=[
        ("", ""),
        ("Married", "Married"),
        ("Single", "Single"),
        ("Divorced", "Divorced"),
        ("Widowed", "Widowed"),
        ("Separated", "Separated")
    ])
    date_of_marriage = DateField("Date of Marriage (if married)")
    spouse_name = StringField("Surviving Spouse Name (if any)")
    decedent_notes = TextAreaField("Additional Decedent Notes")

    # Estate Type & Proceedings
    testate_intestate = SelectField("Testate or Intestate", choices=[
        ("", ""), ("Testate (Will)", "Testate (Will)"),
        ("Intestate (No Will)", "Intestate (No Will)"),
        ("Unknown", "Unknown")
    ])
    original_will_location = StringField("Original Will Location")
    will_date = DateField("Will / Last Codicil Date")
    prior_probate = SelectField("Any Prior Probate Filed?", choices=[
        ("", ""), ("Yes - In Florida", "Yes - In Florida"),
        ("Yes - Other State", "Yes - Other State"),
        ("No", "No")
    ])
    nonprobate_assets = SelectField("Significant Non-Probate Assets?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])
    estimated_estate_value = StringField("Estimated Probate Estate Value")
    proceeding_notes = TextAreaField("Proceeding / Strategy Notes")

    # Heirs / Beneficiaries
    heirs_beneficiaries_list = TextAreaField("Heirs / Beneficiaries (names, relationships, addresses, DOB)")
    minor_beneficiaries = SelectField("Minor Beneficiaries?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])
    disabled_beneficiaries = SelectField("Disabled / Special Needs Beneficiaries?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])
    disputed_heirs = SelectField("Any Disputed Heirs or Contested Beneficiary Issues?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Possible", "Possible")
    ])
    heir_notes = TextAreaField("Heir / Beneficiary Notes")

    # Personal Rep/Fiduciary
    pr_name = StringField("Name")
    pr_relationship = StringField("Relationship to Decedent")
    pr_residency = StringField("Residency (State)")
    pr_address = StringField("Address")
    pr_phone = StringField("Phone")
    pr_email = EmailField("Email")
    alt_pr_named = SelectField("Alternate PR Named in Will?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Not Applicable", "Not Applicable")
    ])
    bond_required = SelectField("Bond Required?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])
    pr_issues = SelectField("Any Conflicts or Eligibility Issues?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Possible", "Possible")
    ])
    fiduciary_notes = TextAreaField("Fiduciary Notes")

    # Real Property
    real_property_list = TextAreaField("Real Property (addresses, legal descriptions, ownership, estimated values)")
    primary_residence_homestead = SelectField("Primary Residence Homestead?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])
    mortgage_balance = StringField("Approx. Mortgage Balances")
    rental_or_investment = SelectField("Any Rental / Investment Properties?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])
    real_property_notes = TextAreaField("Real Property Notes")

    # Personal Property & Financial
    financial_accounts = TextAreaField(
        "Accounts (bank, brokerage, etc. – institution, ownership, approx. balances, POD/TOD)")
    retirement_accounts = TextAreaField("Retirement (401k, IRA, pensions – beneficiary designations, balances)")
    life_insurance = TextAreaField("Life Insurance Policies (carrier, face amount, named beneficiaries)")
    personal_property = TextAreaField(
        "Significant Personal Property (vehicles, jewelry, collections, business interests, etc.)")

    # Debts / Creditors
    creditors_list = TextAreaField("Known Creditors (names, addresses, amounts, secured/unsecured)")
    funeral_expenses_paid = SelectField("Funeral / Burial Expenses Paid?", choices=[
        ("", ""), ("Yes - Paid", "Yes - Paid"), ("Outstanding", "Outstanding"), ("Unknown", "Unknown")
    ])
    medical_bills_final_illness = SelectField("Medical Bills – Final Illness?", choices=[
        ("", ""), ("Yes - Significant", "Yes - Significant"),
        ("Yes - Minimal", "Yes - Minimal"), ("None", "None"), ("Unknown", "Unknown")
    ])
    irs_or_tax_debts = SelectField("IRS / Tax Debts?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])
    creditor_notes = TextAreaField("Creditor / Debt Notes")

    # Homestead & Exempt Property
    homestead_determination_needed = SelectField("Petition to Determine Homestead Needed?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])
    exempt_property_items = StringField("Exempt Property (household furnishings, vehicles, etc.)")
    family_allowance = SelectField("Family Allowance Requested?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Maybe / Discuss", "Maybe / Discuss")
    ])
    homestead_notes = TextAreaField("Homestead / Exempt Property Notes")

    # Tax & Reporting
    estate_tax_filing_needed = SelectField("Federal Estate Tax Filing Needed?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])
    final_1040_needed = SelectField("Final 1040 (Income Tax) Needed?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])
    fiduciary_1041_needed = SelectField("Fiduciary Return 1041 Needed?", choices=[
        ("", ""), ("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")
    ])
    tax_preparer = StringField("CPA / Tax Preparer Involved?")
    tax_notes = TextAreaField("Tax / Reporting Notes")

    # Documents & Deadlines
    doc_retainer = BooleanField("Retainer / Fee Agreement Signed")
    doc_original_will = BooleanField("Original Will Obtained")
    doc_death_certificate = BooleanField("Death Certificate(s)")
    doc_petition_admin = BooleanField("Petition for Administration")
    doc_oath_pr = BooleanField("Oath of PR / Designation of Resident Agent")
    doc_notice_admin = BooleanField("Notice of Administration")
    doc_notice_creditors = BooleanField("Notice to Creditors")
    doc_inventory = BooleanField("Inventory Filed")
    doc_final_accounting = BooleanField("Final Accounting / Petition for Discharge")
    date_letters_issued = DateField("Date Letters of Administration Issued")
    notice_creditors_pub_date = DateField("Notice to Creditors Publication Date")
    claims_deadline = DateField("Creditor Claims Deadline")
    doc_deadline_notes = TextAreaField("Document / Deadline Notes")

    # File Management
    assigned_attorney = StringField("Assigned Attorney")
    assigned_paralegal = StringField("Assigned Paralegal / Staff")
    file_status = SelectField("File Status", choices=[
        ("", ""), ("Intake", "Intake"),
        ("Active - Opening Probate", "Active - Opening Probate"),
        ("Active - Administration", "Active - Administration"),
        ("Active - Closing", "Active - Closing"),
        ("Closed", "Closed")
    ])
    file_notes = TextAreaField("Important Notes")
    followup_tasks = TextAreaField("Follow-Up Tasks / Reminders")

    submit = SubmitField("Save Case")
    # -----------------------
    # Other / General Matter
    # -----------------------

    # 1. Core Info
    case_title = StringField("Case Title")
    court_case_number = StringField("Court Case #")
    internal_case_number = StringField("Internal Case #")
    case_category = SelectField("Case Category", choices=[
        ("", ""),
        ("Civil (General)", "Civil (General)"),
        ("Family Law", "Family Law"),
        ("Landlord / Tenant", "Landlord / Tenant"),
        ("Real Estate", "Real Estate"),
        ("Contract / Business", "Contract / Business"),
        ("Administrative", "Administrative"),
        ("Other", "Other")
    ])
    jurisdiction = StringField("Jurisdiction / Court")
    division = StringField("Division / Section")
    judge = StringField("Judge")
    referral_source = StringField("Referral Source")
    case_description = TextAreaField("Brief Description of Case")
    case_status = SelectField("Current Case Status", choices=[
        ("", ""),
        ("Intake / Consultation", "Intake / Consultation"),
        ("Pre-Suit", "Pre-Suit"),
        ("Active Litigation", "Active Litigation"),
        ("Post-Judgment", "Post-Judgment"),
        ("Closed", "Closed")
    ])

    # 2. Client Info
    client_name = StringField("Client Name")
    client_type = SelectField("Client Type", choices=[
        ("", ""),
        ("Individual", "Individual"),
        ("Married Couple", "Married Couple"),
        ("Business / Entity", "Business / Entity"),
        ("Trust / Estate", "Trust / Estate"),
        ("Other", "Other")
    ])
    client_role = SelectField("Client Role", choices=[
        ("", ""),
        ("Plaintiff / Petitioner", "Plaintiff / Petitioner"),
        ("Defendant / Respondent", "Defendant / Respondent"),
        ("Applicant", "Applicant"),
        ("Appellant", "Appellant"),
        ("Other", "Other")
    ])
    client_address = StringField("Address")
    client_phone = StringField("Phone")
    client_email = EmailField("Email")
    primary_contact_person = StringField("Primary Contact Person (if entity)")
    primary_contact_phone = StringField("Primary Contact Phone")
    primary_contact_email = EmailField("Primary Contact Email")
    client_notes = TextAreaField("Client Notes")

    # 3. Opposing Party
    opposing_name = StringField("Opposing / Adverse Party Name")
    opposing_type = SelectField("Party Type", choices=[
        ("", ""),
        ("Individual", "Individual"),
        ("Business / Entity", "Business / Entity"),
        ("Government Agency", "Government Agency"),
        ("Association", "Association"),
        ("Other", "Other")
    ])
    opposing_role = SelectField("Role", choices=[
        ("", ""),
        ("Plaintiff / Petitioner", "Plaintiff / Petitioner"),
        ("Defendant / Respondent", "Defendant / Respondent"),
        ("Agency / Board", "Agency / Board"),
        ("Other", "Other")
    ])
    opposing_address = StringField("Address")
    opposing_phone = StringField("Phone")
    opposing_email = EmailField("Email")
    opposing_counsel = StringField("Opposing Counsel Name")
    opposing_counsel_firm = StringField("Firm")
    opposing_counsel_contact = StringField("Opposing Counsel Contact")
    opposing_notes = TextAreaField("Opposing Party Notes")

    # 4. Court & Procedural Posture
    case_stage = SelectField("Case Stage", choices=[
        ("", ""),
        ("Pre-Suit / Demand", "Pre-Suit / Demand"),
        ("Pleading Stage", "Pleading Stage"),
        ("Discovery", "Discovery"),
        ("Pretrial / Mediation", "Pretrial / Mediation"),
        ("Trial", "Trial"),
        ("Post-Judgment", "Post-Judgment"),
        ("Appeal", "Appeal")
    ])
    filing_date = DateField("Filing Date")
    service_status = SelectField("Service Status", choices=[
        ("", ""),
        ("Not Served", "Not Served"),
        ("Served", "Served"),
        ("Substitute Service", "Substitute Service"),
        ("Service Waived", "Service Waived")
    ])
    answer_due_date = DateField("Answer / Response Due Date")
    discovery_cutoff = DateField("Discovery Cutoff")
    pretrial_date = DateField("Pretrial / Case Management Date")
    trial_date = DateField("Trial / Final Hearing Date")
    procedural_notes = TextAreaField("Procedural History / Notes")

    # 5. Key Facts & Issues
    fact_summary = TextAreaField("Fact Summary")
    key_issues = TextAreaField("Key Legal / Factual Issues")
    client_objectives = TextAreaField("Client Objectives")

    # 6. Claims / Defenses
    claims_list = TextAreaField("Claims / Causes of Action")
    defenses_list = TextAreaField("Affirmative Defenses / Counterclaims")
    remedies_sought = TextAreaField("Relief / Remedies Sought")

    # 7. Discovery & Evidence
    discovery_served = SelectField("Discovery Served by Client", choices=[
        ("", ""),
        ("None", "None"),
        ("Interrogatories", "Interrogatories"),
        ("RFP / Production", "RFP / Production"),
        ("RFA", "RFA"),
        ("Multiple", "Multiple")
    ])
    discovery_received = SelectField("Discovery Served on Client", choices=[
        ("", ""),
        ("None", "None"),
        ("Interrogatories", "Interrogatories"),
        ("RFP / Production", "RFP / Production"),
        ("RFA", "RFA"),
        ("Multiple", "Multiple")
    ])
    discovery_deadlines = StringField("Discovery Deadlines / Compliance Dates")
    evidence_docs = BooleanField("Documents / Contracts")
    evidence_emails = BooleanField("Emails / Texts")
    evidence_witnesses = BooleanField("Witness Statements")
    evidence_experts = BooleanField("Experts / Reports")
    evidence_photos = BooleanField("Photos / Video")
    evidence_other = BooleanField("Other Critical Evidence")
    evidence_notes = TextAreaField("Evidence Notes")

    # 8. Deadlines & Events
    limitations_deadline = DateField("Statute of Limitations / Jurisdictional Deadline")
    contractual_deadline = DateField("Contractual / Administrative Deadline")
    appeal_deadline = DateField("Appeal / Rehearing Deadline")
    hearing_dates = TextAreaField("Upcoming Hearings / Events")
    deadline_notes = TextAreaField("Deadline / Calendar Notes")

    # 9. Settlement / ADR
    settlement_posture = SelectField("Settlement Posture", choices=[
        ("", ""),
        ("No Discussions", "No Discussions"),
        ("Demand Sent", "Demand Sent"),
        ("Offer Received", "Offer Received"),
        ("Active Negotiations", "Active Negotiations"),
        ("Settled (Pending Docs)", "Settled (Pending Docs)"),
        ("Settled (Closed)", "Settled (Closed)")
    ])
    demand_amount = StringField("Demand Amount")
    offer_amount = StringField("Offer Amount")
    adr_type = SelectField("ADR Type", choices=[
        ("", ""),
        ("Mediation", "Mediation"),
        ("Arbitration", "Arbitration"),
        ("Non-binding Arbitration", "Non-binding Arbitration"),
        ("Informal Settlement Conference", "Informal Settlement Conference"),
        ("None", "None")
    ])
    adr_date = DateField("ADR Date")
    adr_result = StringField("ADR Result")
    settlement_notes = TextAreaField("Settlement / Negotiation Notes")

    # 10. Billing & Trust
    fee_type = SelectField("Fee Arrangement", choices=[
        ("", ""),
        ("Hourly", "Hourly"),
        ("Flat Fee", "Flat Fee"),
        ("Contingency", "Contingency"),
        ("Hybrid", "Hybrid"),
        ("Pro Bono / Reduced", "Pro Bono / Reduced")
    ])
    retainer_amount = StringField("Retainer / Flat Fee Amount")
    billing_rate = StringField("Hourly Rate (if applicable)")
    trust_balance = StringField("Trust Account Balance")
    outstanding_fees = StringField("Outstanding Fees")
    costs_advanced = StringField("Costs Advanced")
    billing_notes = TextAreaField("Billing / Trust Notes")

    # 11. Document Checklist
    doc_retainer = BooleanField("Retainer / Fee Agreement")
    doc_client_intake = BooleanField("Client Intake Form")
    doc_key_pleadings = BooleanField("Key Pleadings Filed")
    doc_evidence_uploaded = BooleanField("Evidence Uploaded / Organized")
    doc_orders = BooleanField("Orders / Judgments on File")
    doc_correspondence = BooleanField("Important Correspondence Saved")
    document_notes = TextAreaField("Document Notes")

    # 12. File Management
    assigned_attorney = StringField("Assigned Attorney")
    assigned_paralegal = StringField("Assigned Paralegal / Staff")
    file_status = SelectField("File Status", choices=[
        ("", ""),
        ("Intake", "Intake"),
        ("Active", "Active"),
        ("On Hold", "On Hold"),
        ("Closed", "Closed"),
        ("Archived", "Archived")
    ])
    file_notes = TextAreaField("File Notes")
    followup_tasks = TextAreaField("Follow-Up Tasks / Reminders")

    submit = SubmitField('Save Case')

    def populate_obj(self, obj):
        """
        Populate the SQLAlchemy object with form data.
        Handles conversions (e.g., co_defendants radio => boolean) and keeps nullable behavior.
        """
        super().populate_obj(obj)
        # co_defendants radio field to boolean/None
        if hasattr(self, 'co_defendants'):
            val = self.co_defendants.data
            if val == 'yes':
                obj.co_defendants = True
            elif val == 'no':
                obj.co_defendants = False
            else:
                obj.co_defendants = None

    def validate(self, extra_validators=None):
        """
        Perform normal validation, then run any conditional checks.
        Must accept extra_validators to remain compatible with WTForms internal calls.
        """
        # call parent validate and forward extra_validators
        rv = super().validate(extra_validators=extra_validators)
        if not rv:
            return False

        # Example conditional rule area (keep optional by default).
        # Uncomment/modify to require fields for specific case types if desired.
        # if self.case_type.data == 'criminal' and not self.defendant.data:
        #     self.defendant.errors.append('Defendant name is recommended for criminal cases.')
        #     return False

        return True

class ClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    address = StringField('Address', validators=[Length(max=250)])
    submit = SubmitField('Save Client')

class DocumentForm(FlaskForm):
    filename = StringField('Document Name', validators=[DataRequired()])
    client_id = SelectField('Client', coerce=int)
    case_id = SelectField('Case', coerce=int)
    file = FileField('Upload File')
    submit = SubmitField('Save Document')

class NoteForm(FlaskForm):
    note = TextAreaField('Note', validators=[DataRequired()])
    date_made = DateTimeField('Date Made', format='%Y-%m-%d %H:%M', default=now)
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    case_id = SelectField('Case/Matter', coerce=int)
    client_id = SelectField('Client', coerce=int)
    event_id = SelectField('Event', coerce=int)
    document_id = SelectField('Document', coerce=int)
    submit = SubmitField('Save Note')

def get_year_choices():
    this_year = datetime.date.today().year
    return [(str(y), str(y)) for y in range(this_year, this_year + 3)]

def get_month_choices():
    return [(str(m).zfill(2), str(m).zfill(2)) for m in range(1, 13)]

def get_day_choices():
    return [(str(d).zfill(2), str(d).zfill(2)) for d in range(1, 32)]

def get_hour_choices():
    return [(str(h).zfill(2), str(h).zfill(2)) for h in range(0, 24)]

def get_minute_choices():
    return [(str(m).zfill(2), str(m).zfill(2)) for m in range(0, 60)]

class CalendarEventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    time_length = StringField('Time Length')
    deadline = BooleanField('Is there a Deadline?', default=False)
    event_datetime = StringField("Event Date & Time")
    deadline = BooleanField("Is Deadline?")
    deadline_datetime = StringField("Deadline Date & Time")
    case_id = SelectField('Case', coerce=int)
    client_id = SelectField('Client', coerce=int)
    document_id = SelectField('Document', coerce=int)
    user_id = SelectField('User', coerce=int)
    completed = BooleanField('Completed')
    submit = SubmitField('Save Event')

# -----------------------
# DOCUMENT / TEMPLATE FORMS
# -----------------------
class TemplateForm(FlaskForm):
    name = StringField('Template Name', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Template Content (Jinja2)', validators=[DataRequired()])
    submit = SubmitField('Save Template')

class GenerateDocumentForm(FlaskForm):
    template_id = SelectField('Template', coerce=int, validators=[DataRequired()])
    case_id = SelectField('Case', coerce=int, validators=[DataRequired()])
    filename = StringField('Output Filename (no extension)', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Generate Document')

# Multi-checkbox helper and Bulk form (if present in your codebase)
from wtforms import widgets, SelectMultipleField
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class BulkGenerateForm(FlaskForm):
    case_id = SelectField('Case', coerce=int, validators=[DataRequired()])
    doc_types = MultiCheckboxField('Documents to Generate', choices=[])
    submit = SubmitField('Generate Selected Documents')