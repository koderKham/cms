# Full models.py with added case-type specific nullable columns
import enum
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class UserRole(enum.Enum):
    superuser = "superuser"
    manager = "manager"
    attorney = "attorney"
    staff = "staff"
    client = "client"
    pending = "pending"  # default for new signups

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.pending, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def is_superuser(self):
        return self.role == UserRole.superuser

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)


    # -----------------------
    # Personal Injury fields
    # -----------------------
    class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String(200), nullable=False)
    case_number = db.Column(db.String(100), unique=True, nullable=False)
    case_type = db.Column(db.String(100), nullable=True)
    filed_date = db.Column(db.Date, nullable=True)
    judge = db.Column(db.String(100), nullable=True)
    # --- Add new personal injury fields below ---
    incident_address = db.Column(db.String(200), nullable=True)
    incident_city_county = db.Column(db.String(100), nullable=True)
    jurisdiction = db.Column(db.String(100), nullable=True)
    police_report_number = db.Column(db.String(50), nullable=True)
    law_enforcement_agency = db.Column(db.String(100), nullable=True)
    liability_admitted = db.Column(db.String(20), nullable=True)
    # Client
    client_name = db.Column(db.String(120), nullable=True)
    client_dob = db.Column(db.Date, nullable=True)
    client_address = db.Column(db.String(250), nullable=True)
    client_phone = db.Column(db.String(30), nullable=True)
    client_alt_phone = db.Column(db.String(30), nullable=True)
    client_email = db.Column(db.String(120), nullable=True)
    client_dl = db.Column(db.String(30), nullable=True)
    client_insurer = db.Column(db.String(100), nullable=True)
    client_policy = db.Column(db.String(60), nullable=True)
    client_claim = db.Column(db.String(60), nullable=True)
    medpay_coverage = db.Column(db.String(20), nullable=True)
    pip_active = db.Column(db.String(20), nullable=True)
    pip_limits = db.Column(db.String(30), nullable=True)
    # Defendant
    defendant_name = db.Column(db.String(120), nullable=True)
    defendant_address = db.Column(db.String(200), nullable=True)
    defendant_contact = db.Column(db.String(100), nullable=True)
    defendant_dl = db.Column(db.String(30), nullable=True)
    def_vehicle_year = db.Column(db.String(30), nullable=True)
    def_vehicle_make = db.Column(db.String(50), nullable=True)
    def_vehicle_model = db.Column(db.String(50), nullable=True)
    def_insurer = db.Column(db.String(100), nullable=True)
    def_policy = db.Column(db.String(60), nullable=True)
    def_claim = db.Column(db.String(60), nullable=True)
    def_bi_limits = db.Column(db.String(60), nullable=True)
    adjuster_name = db.Column(db.String(100), nullable=True)
    adjuster_phone = db.Column(db.String(30), nullable=True)
    adjuster_email = db.Column(db.String(120), nullable=True)
    defendant_is_commercial = db.Column(db.String(10), nullable=True)
    business_name = db.Column(db.String(100), nullable=True)
    registered_agent = db.Column(db.String(100), nullable=True)
    # Witnesses & Medical
    witnesses = db.Column(db.Text, nullable=True)
    witness_statement_taken = db.Column(db.String(20), nullable=True)
    witness_liability_support = db.Column(db.String(20), nullable=True)
    hospital_er = db.Column(db.String(150), nullable=True)
    ems_transport = db.Column(db.String(10), nullable=True)
    initial_visit_date = db.Column(db.Date, nullable=True)
    chiropractor = db.Column(db.String(100), nullable=True)
    orthopedic = db.Column(db.String(100), nullable=True)
    neurologist = db.Column(db.String(100), nullable=True)
    mri_center = db.Column(db.String(100), nullable=True)
    pain_management = db.Column(db.String(100), nullable=True)
    surgery_center = db.Column(db.String(100), nullable=True)
    total_med_bills = db.Column(db.String(100), nullable=True)
    outstanding_balances = db.Column(db.String(100), nullable=True)
    lops = db.Column(db.Text, nullable=True)
    # Injury areas (multi-checkbox can be comma-separated)
    injury_neck = db.Column(db.Boolean, default=False)
    injury_back = db.Column(db.Boolean, default=False)
    injury_shoulder = db.Column(db.Boolean, default=False)
    injury_knee = db.Column(db.Boolean, default=False)
    injury_concussion = db.Column(db.Boolean, default=False)
    injury_fracture = db.Column(db.Boolean, default=False)
    injury_scars = db.Column(db.Boolean, default=False)
    injury_headaches = db.Column(db.Boolean, default=False)
    injury_radiating = db.Column(db.Boolean, default=False)
    injury_loc = db.Column(db.Boolean, default=False)
    injury_ptd = db.Column(db.Boolean, default=False)
    prior_related_injuries = db.Column(db.String(20), nullable=True)
    prior_accidents = db.Column(db.String(20), nullable=True)
    injury_notes = db.Column(db.Text, nullable=True)
    # Property Damage
    total_loss = db.Column(db.String(10), nullable=True)
    repair_estimate = db.Column(db.String(100), nullable=True)
    photos_uploaded = db.Column(db.String(20), nullable=True)
    rental_car = db.Column(db.String(20), nullable=True)
    tow_storage_location = db.Column(db.String(150), nullable=True)
    diminished_value_claim = db.Column(db.String(10), nullable=True)
    # Insurance Comm
    demand_sent_date = db.Column(db.Date, nullable=True)
    initial_offer = db.Column(db.String(100), nullable=True)
    coverage_disclosure_sent = db.Column(db.String(10), nullable=True)
    bi_disclosure_received = db.Column(db.String(10), nullable=True)
    negotiation_notes = db.Column(db.Text, nullable=True)
    # Document Tracking
    doc_retainer = db.Column(db.Boolean, default=False)
    doc_hipaa = db.Column(db.Boolean, default=False)
    doc_lops = db.Column(db.Boolean, default=False)
    doc_med_records = db.Column(db.Boolean, default=False)
    doc_med_bills = db.Column(db.Boolean, default=False)
    doc_demand_pkg = db.Column(db.Boolean, default=False)
    doc_ins_correspondence = db.Column(db.Boolean, default=False)
    doc_lien_letters = db.Column(db.Boolean, default=False)
    # Litigation
    court_case_number = db.Column(db.String(100), nullable=True)
    division = db.Column(db.String(50), nullable=True)
    opposing_counsel = db.Column(db.String(120), nullable=True)
    opp_counsel_contact = db.Column(db.String(100), nullable=True)
    complaint_filed_date = db.Column(db.Date, nullable=True)
    service_status = db.Column(db.String(30), nullable=True)
    answer_filed_date = db.Column(db.Date, nullable=True)
    mediation_date = db.Column(db.Date, nullable=True)
    trial_date = db.Column(db.Date, nullable=True)
    litigation_notes = db.Column(db.Text, nullable=True)
    # Settlement/Closing
    gross_settlement = db.Column(db.String(100), nullable=True)
    medical_liens = db.Column(db.String(100), nullable=True)
    attorney_fees = db.Column(db.String(100), nullable=True)
    costs = db.Column(db.String(100), nullable=True)
    net_to_client = db.Column(db.String(100), nullable=True)
    disbursement_date = db.Column(db.Date, nullable=True)
    release_signed = db.Column(db.String(10), nullable=True)
    settlement_check_received = db.Column(db.String(15), nullable=True)
    # File Management
    assigned_attorney = db.Column(db.String(120), nullable=True)
    assigned_paralegal = db.Column(db.String(120), nullable=True)
    case_status = db.Column(db.String(30), nullable=True)
    important_notes = db.Column(db.Text, nullable=True)
    followup_reminders = db.Column(db.Text, nullable=True)
    # -----------------------
    # Criminal fields
    # -----------------------
 # Core Case Info
    case_title = db.Column(db.String(200), nullable=True)
    court_case_number = db.Column(db.String(100), nullable=True)
    internal_case_number = db.Column(db.String(100), nullable=True)
    jurisdiction = db.Column(db.String(100), nullable=True)
    case_level = db.Column(db.String(30), nullable=True)
    case_type = db.Column(db.String(50), nullable=True)
    division = db.Column(db.String(50), nullable=True)
    judge = db.Column(db.String(100), nullable=True)
    prosecutor = db.Column(db.String(100), nullable=True)
    arresting_agency = db.Column(db.String(100), nullable=True)
    offense_date = db.Column(db.Date, nullable=True)
    arrest_date = db.Column(db.Date, nullable=True)
    case_status = db.Column(db.String(30), nullable=True)

    # Defendant Info
    def_name = db.Column(db.String(120), nullable=True)
    def_aliases = db.Column(db.String(120), nullable=True)
    def_dob = db.Column(db.Date, nullable=True)
    def_address = db.Column(db.String(200), nullable=True)
    def_phone = db.Column(db.String(50), nullable=True)
    def_email = db.Column(db.String(120), nullable=True)
    def_dl = db.Column(db.String(40), nullable=True)
    def_ssn_last4 = db.Column(db.String(4), nullable=True)
    def_employment = db.Column(db.String(100), nullable=True)
    def_education = db.Column(db.String(100), nullable=True)
    immigration_status = db.Column(db.String(40), nullable=True)
    primary_language = db.Column(db.String(60), nullable=True)
    contact_preference = db.Column(db.String(30), nullable=True)

    # Charges
    primary_charge = db.Column(db.String(200), nullable=True)
    primary_statute = db.Column(db.String(100), nullable=True)
    primary_degree = db.Column(db.String(50), nullable=True)
    primary_max_penalty = db.Column(db.String(120), nullable=True)
    additional_charges = db.Column(db.Text, nullable=True)
    offense_date_range = db.Column(db.String(100), nullable=True)
    enhancements = db.Column(db.String(50), nullable=True)
    score_sheet_needed = db.Column(db.String(10), nullable=True)

    # Arrest/Procedural History
    arrest_type = db.Column(db.String(40), nullable=True)
    booking_number = db.Column(db.String(40), nullable=True)
    first_appearance_date = db.Column(db.Date, nullable=True)
    arraignment_date = db.Column(db.Date, nullable=True)
    procedural_history = db.Column(db.Text, nullable=True)

    # Custody & Bond
    in_custody = db.Column(db.String(10), nullable=True)
    custody_location = db.Column(db.String(100), nullable=True)
    inmate_number = db.Column(db.String(40), nullable=True)
    bond_amount = db.Column(db.String(40), nullable=True)
    bond_type = db.Column(db.String(20), nullable=True)
    bond_status = db.Column(db.String(20), nullable=True)
    bond_hearing_date = db.Column(db.Date, nullable=True)
    release_conditions = db.Column(db.Text, nullable=True)

    # Victim & Co-Defendants
    victim_info = db.Column(db.Text, nullable=True)
    victim_position = db.Column(db.Text, nullable=True)
    no_contact_order = db.Column(db.String(20), nullable=True)
    dv_injunction = db.Column(db.String(20), nullable=True)
    codef_info = db.Column(db.Text, nullable=True)

    # Evidence Summary
    evidence_police_reports = db.Column(db.Boolean, default=False)
    evidence_bodycam = db.Column(db.Boolean, default=False)
    evidence_911 = db.Column(db.Boolean, default=False)
    evidence_witness_statements = db.Column(db.Boolean, default=False)
    evidence_lab_reports = db.Column(db.Boolean, default=False)
    evidence_photos = db.Column(db.Boolean, default=False)
    evidence_search_warrants = db.Column(db.Boolean, default=False)
    evidence_phone_records = db.Column(db.Boolean, default=False)
    evidence_other = db.Column(db.Boolean, default=False)
    evidence_summary = db.Column(db.Text, nullable=True)

    # Prior Criminal History
    prior_felonies = db.Column(db.String(20), nullable=True)
    prior_misdemeanors = db.Column(db.String(20), nullable=True)
    prior_juvenile = db.Column(db.String(20), nullable=True)
    on_probation = db.Column(db.String(10), nullable=True)
    pending_cases = db.Column(db.String(10), nullable=True)
    priors_affecting_sentence = db.Column(db.String(10), nullable=True)
    prior_history_notes = db.Column(db.Text, nullable=True)

    # Motions & Defense Strategy
    motion_suppress = db.Column(db.Boolean, default=False)
    motion_dismiss = db.Column(db.Boolean, default=False)
    motion_compel = db.Column(db.Boolean, default=False)
    motion_bond = db.Column(db.Boolean, default=False)
    motion_other = db.Column(db.Boolean, default=False)
    defense_theory = db.Column(db.Text, nullable=True)

    # Plea Negotiations & Trial
    plea_offer = db.Column(db.String(120), nullable=True)
    offer_date = db.Column(db.Date, nullable=True)
    offer_expiration = db.Column(db.Date, nullable=True)
    plea_discussion_notes = db.Column(db.Text, nullable=True)
    trial_setting = db.Column(db.String(30), nullable=True)
    trial_date = db.Column(db.Date, nullable=True)
    jury_or_bench = db.Column(db.String(20), nullable=True)

    # Sentencing / Post-Judgment
    disposition = db.Column(db.String(20), nullable=True)
    sentencing_date = db.Column(db.Date, nullable=True)
    incarceration_term = db.Column(db.String(120), nullable=True)
    probation_term = db.Column(db.String(120), nullable=True)
    fines = db.Column(db.String(120), nullable=True)
    court_costs = db.Column(db.String(120), nullable=True)
    restitution = db.Column(db.String(120), nullable=True)
    special_conditions = db.Column(db.String(120), nullable=True)
    postconviction_issues = db.Column(db.Text, nullable=True)

    # File Management
    assigned_attorney = db.Column(db.String(100), nullable=True)
    assigned_paralegal = db.Column(db.String(100), nullable=True)
    file_status = db.Column(db.String(30), nullable=True)
    file_notes = db.Column(db.Text, nullable=True)
    followup_tasks = db.Column(db.Text, nullable=True)        # e.g., 'open','plea','dismissed','closed'

    # -----------------------
    # Probate / Estate Planning fields
    # Core probate info
    case_title = db.Column(db.String(200), nullable=True)
    court_case_number = db.Column(db.String(100), nullable=True)
    internal_case_number = db.Column(db.String(100), nullable=True)
    jurisdiction = db.Column(db.String(100), nullable=True)
    case_type = db.Column(db.String(50), nullable=True)
    referral_source = db.Column(db.String(100), nullable=True)
    primary_contact = db.Column(db.String(100), nullable=True)
    primary_contact_phone = db.Column(db.String(50), nullable=True)
    primary_contact_email = db.Column(db.String(120), nullable=True)
    matter_notes = db.Column(db.Text, nullable=True)

    # Decedent Info
    decedent_name = db.Column(db.String(120), nullable=True)
    decedent_dob = db.Column(db.Date, nullable=True)
    decedent_dod = db.Column(db.Date, nullable=True)
    decedent_last_address = db.Column(db.String(200), nullable=True)
    decedent_county = db.Column(db.String(100), nullable=True)
    decedent_ssn_last4 = db.Column(db.String(4), nullable=True)
    marital_status_at_death = db.Column(db.String(20), nullable=True)
    date_of_marriage = db.Column(db.Date, nullable=True)
    spouse_name = db.Column(db.String(120), nullable=True)
    decedent_notes = db.Column(db.Text, nullable=True)

    # Estate type & proceedings
    testate_intestate = db.Column(db.String(20), nullable=True)
    original_will_location = db.Column(db.String(100), nullable=True)
    will_date = db.Column(db.Date, nullable=True)
    prior_probate = db.Column(db.String(30), nullable=True)
    nonprobate_assets = db.Column(db.String(20), nullable=True)
    estimated_estate_value = db.Column(db.String(100), nullable=True)
    proceeding_notes = db.Column(db.Text, nullable=True)

    # Heirs / Beneficiaries
    heirs_beneficiaries_list = db.Column(db.Text, nullable=True)
    minor_beneficiaries = db.Column(db.String(10), nullable=True)
    disabled_beneficiaries = db.Column(db.String(10), nullable=True)
    disputed_heirs = db.Column(db.String(10), nullable=True)
    heir_notes = db.Column(db.Text, nullable=True)

    # Personal Rep/Fiduciary
    pr_name = db.Column(db.String(120), nullable=True)
    pr_relationship = db.Column(db.String(100), nullable=True)
    pr_residency = db.Column(db.String(60), nullable=True)
    pr_address = db.Column(db.String(200), nullable=True)
    pr_phone = db.Column(db.String(50), nullable=True)
    pr_email = db.Column(db.String(120), nullable=True)
    alt_pr_named = db.Column(db.String(20), nullable=True)
    bond_required = db.Column(db.String(20), nullable=True)
    pr_issues = db.Column(db.String(20), nullable=True)
    fiduciary_notes = db.Column(db.Text, nullable=True)

    # Real Property
    real_property_list = db.Column(db.Text, nullable=True)
    primary_residence_homestead = db.Column(db.String(10), nullable=True)
    mortgage_balance = db.Column(db.String(100), nullable=True)
    rental_or_investment = db.Column(db.String(10), nullable=True)
    real_property_notes = db.Column(db.Text, nullable=True)

    # Personal Property & Financial
    financial_accounts = db.Column(db.Text, nullable=True)
    retirement_accounts = db.Column(db.Text, nullable=True)
    life_insurance = db.Column(db.Text, nullable=True)
    personal_property = db.Column(db.Text, nullable=True)

    # Debts / Creditors
    creditors_list = db.Column(db.Text, nullable=True)
    funeral_expenses_paid = db.Column(db.String(20), nullable=True)
    medical_bills_final_illness = db.Column(db.String(20), nullable=True)
    irs_or_tax_debts = db.Column(db.String(10), nullable=True)
    creditor_notes = db.Column(db.Text, nullable=True)

    # Homestead & Exempt Property
    homestead_determination_needed = db.Column(db.String(10), nullable=True)
    exempt_property_items = db.Column(db.String(150), nullable=True)
    family_allowance = db.Column(db.String(20), nullable=True)
    homestead_notes = db.Column(db.Text, nullable=True)

    # Tax & Reporting
    estate_tax_filing_needed = db.Column(db.String(10), nullable=True)
    final_1040_needed = db.Column(db.String(10), nullable=True)
    fiduciary_1041_needed = db.Column(db.String(10), nullable=True)
    tax_preparer = db.Column(db.String(100), nullable=True)
    tax_notes = db.Column(db.Text, nullable=True)

    # Documents & Deadlines
    doc_retainer = db.Column(db.Boolean, default=False)
    doc_original_will = db.Column(db.Boolean, default=False)
    doc_death_certificate = db.Column(db.Boolean, default=False)
    doc_petition_admin = db.Column(db.Boolean, default=False)
    doc_oath_pr = db.Column(db.Boolean, default=False)
    doc_notice_admin = db.Column(db.Boolean, default=False)
    doc_notice_creditors = db.Column(db.Boolean, default=False)
    doc_inventory = db.Column(db.Boolean, default=False)
    doc_final_accounting = db.Column(db.Boolean, default=False)
    date_letters_issued = db.Column(db.Date, nullable=True)
    notice_creditors_pub_date = db.Column(db.Date, nullable=True)
    claims_deadline = db.Column(db.Date, nullable=True)
    doc_deadline_notes = db.Column(db.Text, nullable=True)

    # File Management
    assigned_attorney = db.Column(db.String(120), nullable=True)
    assigned_paralegal = db.Column(db.String(120), nullable=True)
    file_status = db.Column(db.String(30), nullable=True)
    file_notes = db.Column(db.Text, nullable=True)
    followup_tasks = db.Column(db.Text, nullable=True)

    # -----------------------
    # Other / generic matter fields
    # -----------------------
    # Miscellaneous case fields
    case_title = db.Column(db.String(200), nullable=True)
    court_case_number = db.Column(db.String(100), nullable=True)
    internal_case_number = db.Column(db.String(100), nullable=True)
    case_category = db.Column(db.String(50), nullable=True)
    jurisdiction = db.Column(db.String(100), nullable=True)
    division = db.Column(db.String(100), nullable=True)
    judge = db.Column(db.String(100), nullable=True)
    referral_source = db.Column(db.String(100), nullable=True)
    case_description = db.Column(db.Text, nullable=True)
    case_status = db.Column(db.String(30), nullable=True)

    # Client Information
    client_name = db.Column(db.String(120), nullable=True)
    client_type = db.Column(db.String(50), nullable=True)
    client_role = db.Column(db.String(50), nullable=True)
    client_address = db.Column(db.String(200), nullable=True)
    client_phone = db.Column(db.String(50), nullable=True)
    client_email = db.Column(db.String(120), nullable=True)
    primary_contact_person = db.Column(db.String(100), nullable=True)
    primary_contact_phone = db.Column(db.String(50), nullable=True)
    primary_contact_email = db.Column(db.String(120), nullable=True)
    client_notes = db.Column(db.Text, nullable=True)

    # Opposing Party Info
    opposing_name = db.Column(db.String(120), nullable=True)
    opposing_type = db.Column(db.String(50), nullable=True)
    opposing_role = db.Column(db.String(50), nullable=True)
    opposing_address = db.Column(db.String(200), nullable=True)
    opposing_phone = db.Column(db.String(50), nullable=True)
    opposing_email = db.Column(db.String(120), nullable=True)
    opposing_counsel = db.Column(db.String(100), nullable=True)
    opposing_counsel_firm = db.Column(db.String(100), nullable=True)
    opposing_counsel_contact = db.Column(db.String(100), nullable=True)
    opposing_notes = db.Column(db.Text, nullable=True)

    # Court & Procedural
    case_stage = db.Column(db.String(30), nullable=True)
    filing_date = db.Column(db.Date, nullable=True)
    service_status = db.Column(db.String(30), nullable=True)
    answer_due_date = db.Column(db.Date, nullable=True)
    discovery_cutoff = db.Column(db.Date, nullable=True)
    pretrial_date = db.Column(db.Date, nullable=True)
    trial_date = db.Column(db.Date, nullable=True)
    procedural_notes = db.Column(db.Text, nullable=True)

    # Key Facts & Issues
    fact_summary = db.Column(db.Text, nullable=True)
    key_issues = db.Column(db.Text, nullable=True)
    client_objectives = db.Column(db.Text, nullable=True)

    # Claims/Defenses
    claims_list = db.Column(db.Text, nullable=True)
    defenses_list = db.Column(db.Text, nullable=True)
    remedies_sought = db.Column(db.Text, nullable=True)

    # Discovery & Evidence
    discovery_served = db.Column(db.String(30), nullable=True)
    discovery_received = db.Column(db.String(30), nullable=True)
    discovery_deadlines = db.Column(db.String(200), nullable=True)
    evidence_docs = db.Column(db.Boolean, default=False)
    evidence_emails = db.Column(db.Boolean, default=False)
    evidence_witnesses = db.Column(db.Boolean, default=False)
    evidence_experts = db.Column(db.Boolean, default=False)
    evidence_photos = db.Column(db.Boolean, default=False)
    evidence_other = db.Column(db.Boolean, default=False)
    evidence_notes = db.Column(db.Text, nullable=True)

    # Deadlines & Events
    limitations_deadline = db.Column(db.Date, nullable=True)
    contractual_deadline = db.Column(db.Date, nullable=True)
    appeal_deadline = db.Column(db.Date, nullable=True)
    hearing_dates = db.Column(db.Text, nullable=True)
    deadline_notes = db.Column(db.Text, nullable=True)

    # Settlement / ADR
    settlement_posture = db.Column(db.String(30), nullable=True)
    demand_amount = db.Column(db.String(100), nullable=True)
    offer_amount = db.Column(db.String(100), nullable=True)
    adr_type = db.Column(db.String(50), nullable=True)
    adr_date = db.Column(db.Date, nullable=True)
    adr_result = db.Column(db.String(100), nullable=True)
    settlement_notes = db.Column(db.Text, nullable=True)

    # Billing & Trust
    fee_type = db.Column(db.String(30), nullable=True)
    retainer_amount = db.Column(db.String(100), nullable=True)
    billing_rate = db.Column(db.String(100), nullable=True)
    trust_balance = db.Column(db.String(100), nullable=True)
    outstanding_fees = db.Column(db.String(100), nullable=True)
    costs_advanced = db.Column(db.String(100), nullable=True)
    billing_notes = db.Column(db.Text, nullable=True)

    # Document Checklist
    doc_retainer = db.Column(db.Boolean, default=False)
    doc_client_intake = db.Column(db.Boolean, default=False)
    doc_key_pleadings = db.Column(db.Boolean, default=False)
    doc_evidence_uploaded = db.Column(db.Boolean, default=False)
    doc_orders = db.Column(db.Boolean, default=False)
    doc_correspondence = db.Column(db.Boolean, default=False)
    document_notes = db.Column(db.Text, nullable=True)

    # File Management
    assigned_attorney = db.Column(db.String(120), nullable=True)
    assigned_paralegal = db.Column(db.String(120), nullable=True)
    file_status = db.Column(db.String(30), nullable=True)
    file_notes = db.Column(db.Text, nullable=True)
    followup_tasks = db.Column(db.Text, nullable=True)

    # Relationships
    notes = db.relationship('Note', backref='case', lazy=True, cascade="all, delete-orphan")
    documents = db.relationship('Document', backref='case', lazy=True, cascade="all, delete-orphan")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(250), nullable=True)
    # ... other fields ...


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='notes')


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_viewed_at = db.Column(db.DateTime)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=True)
    client = db.relationship('Client', backref='documents')


class CalendarEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    time_length = db.Column(db.String(50), nullable=True)
    deadline = db.Column(db.Boolean, default=False)
    deadline_datetime = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)

    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=True)
    case = db.relationship('Case', backref='calendar_events')

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    client = db.relationship('Client', backref='calendar_events')

    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=True)
    document = db.relationship('Document', backref='calendar_events')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref='calendar_events')

    event_datetime = db.Column(db.DateTime, nullable=False)


class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Add these classes into your models.py (near other SQLAlchemy models)

import json
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

# Custom Field metadata (one per field)
class CustomField(db.Model):
    __tablename__ = 'custom_field'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)      # internal name
    slug = Column(String(120), nullable=False, unique=True)  # stable key used in templates & storage
    label = Column(String(200), nullable=False)     # shown to users
    target = Column(String(50), nullable=False)     # 'case' or 'client' (can extend)
    field_type = Column(String(50), nullable=False) # 'text','textarea','select','radio','checkbox','date','number','boolean'
    options = Column(Text, nullable=True)           # JSON or newline list for choices (for select/radio/checkbox)
    required = Column(Boolean, default=False)
    help_text = Column(Text, nullable=True)
    order = Column(Integer, default=100)
    visible = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_options_list(self):
        """Return options as list of (value,label) tuples."""
        if not self.options:
            return []
        # try JSON first (list or dict)
        try:
            parsed = json.loads(self.options)
            if isinstance(parsed, dict):
                # dict of value:label
                return [(k, v) for k, v in parsed.items()]
            if isinstance(parsed, list):
                # list of strings or [value,label] pairs
                out = []
                for item in parsed:
                    if isinstance(item, list) and len(item) >= 2:
                        out.append((str(item[0]), str(item[1])))
                    else:
                        out.append((str(item), str(item)))
                return out
        except Exception:
            # fallback: newline-separated values
            lines = [l.strip() for l in self.options.splitlines() if l.strip()]
            return [(v, v) for v in lines]
        return []

# CustomFieldValue stores a value for a specific resource (case or client)
class CustomFieldValue(db.Model):
    __tablename__ = 'custom_field_value'
    id = Column(Integer, primary_key=True)
    field_id = Column(Integer, ForeignKey('custom_field.id'), nullable=False)
    # link to case or client (use nullable ints and only one used depending on target)
    case_id = Column(Integer, ForeignKey('case.id'), nullable=True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=True)
    # store as text; for multiple choices store JSON-encoded array
    value = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    field = relationship('CustomField', backref='values')