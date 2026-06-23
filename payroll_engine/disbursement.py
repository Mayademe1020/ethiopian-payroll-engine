# Stub for Telebirr disbursement (two-phase intent -> paid)
# In a real implementation, this would call the Telebirr API.

import uuid
from datetime import datetime

# In-memory store for disbursement records (for demo/stub)
_disbursement_records = []

def record_disbursement_intent(employee_id, amount, currency='ETB'):
    """
    Record intent to disburse salary.
    Returns a dict with intent ID and status PENDING.
    """
    intent_id = str(uuid.uuid4())
    record = {
        'intent_id': intent_id,
        'employee_id': employee_id,
        'amount': amount,
        'currency': currency,
        'status': 'PENDING',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'confirmed': None
    }
    _disbursement_records.append(record)
    return record

def confirm_disbursement(intent_id):
    """
    Confirm that the disbursement was successful.
    In stub, we always succeed.
    """
    for record in _disbursement_records:
        if record['intent_id'] == intent_id:
            record['status'] = 'PAID'
            record['confirmed'] = datetime.utcnow().isoformat() + 'Z'
            return record
    raise ValueError(f"Intent ID {intent_id} not found")

def get_disbursement_record(intent_id):
    for record in _disbursement_records:
        if record['intent_id'] == intent_id:
            return record
    return None

def list_disbursements():
    return list(_disbursement_records)
