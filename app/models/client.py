from datetime import datetime
from app import db
from sqlalchemy.ext.hybrid import hybrid_property


class ClientType:
    """Enum for client type values"""
    INDIVIDUAL = 'individual'
    BUSINESS = 'business'
    NONPROFIT = 'nonprofit'
    GOVERNMENT = 'government'


class Client(db.Model):
    """Client model representing a client in the system"""
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    client_type = db.Column(db.String(20), default=ClientType.INDIVIDUAL)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100), default='United States')

    # Individual-specific fields
    date_of_birth = db.Column(db.Date)
    ssn_last_four = db.Column(db.String(4))

    # Business-specific fields
    company_name = db.Column(db.String(255))
    industry = db.Column(db.String(100))
    tax_id = db.Column(db.String(50))
    website = db.Column(db.String(255))

    # Additional fields
    notes = db.Column(db.Text)
    referral_source = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    cases = db.relationship('Case', backref='client', lazy=True)
    documents = db.relationship('Document', backref='client', lazy=True)
    events = db.relationship('Event', secondary='client_event', back_populates='clients')
    notes = db.relationship('Note', backref='client', lazy=True)

    @hybrid_property
    def full_address(self):
        """Return the full address as a string"""
        address_parts = [self.address]
        if self.city:
            address_parts.append(self.city)
        if self.state:
            if address_parts[-1] != self.city:
                address_parts.append(self.state)
            else:
                address_parts[-1] = f"{self.city}, {self.state}"
        if self.postal_code:
            address_parts[-1] = f"{address_parts[-1]} {self.postal_code}"
        if self.country and self.country != 'United States':
            address_parts.append(self.country)
        return ", ".join(filter(None, address_parts))

    @hybrid_property
    def active_cases_count(self):
        """Return the count of active cases for this client"""
        from app.models.case import Case, CaseStatus
        return Case.query.filter_by(
            client_id=self.id
        ).filter(
            Case.status.in_([CaseStatus.OPEN, CaseStatus.PENDING])
        ).count()

    def __repr__(self):
        return f'<Client {self.name}>'

    def to_dict(self):
        """Convert Client to dictionary for API responses"""
        return {
            'id': self.id,
            'name': self.name,
            'client_type': self.client_type,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'full_address': self.full_address,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'ssn_last_four': self.ssn_last_four,
            'company_name': self.company_name,
            'industry': self.industry,
            'tax_id': self.tax_id,
            'website': self.website,
            'notes': self.notes,
            'referral_source': self.referral_source,
            'is_active': self.is_active,
            'active_cases_count': self.active_cases_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }