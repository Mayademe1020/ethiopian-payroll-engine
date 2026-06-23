import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from payroll_engine.disbursement import record_disbursement_intent, confirm_disbursement, get_disbursement_record, list_disbursements

def test_record_and_confirm():
    # Clear any existing records (not ideal but for demo)
    # We'll just rely on the fact that the module-level list is fresh each import? 
    # Since we import the module, the list is already there; we can't easily clear.
    # Instead, we'll just test that recording adds a record and confirming changes status.
    intent_record = record_disbursement_intent('E001', 5000.0)
    assert 'intent_id' in intent_record
    assert intent_record['employee_id'] == 'E001'
    assert intent_record['amount'] == 5000.0
    assert intent_record['status'] == 'PENDING'
    intent_id = intent_record['intent_id']
    # Confirm
    confirmed = confirm_disbursement(intent_id)
    assert confirmed['status'] == 'PAID'
    assert confirmed['confirmed'] is not None
    # Retrieve record
    record = get_disbursement_record(intent_id)
    assert record['status'] == 'PAID'
    # List
    all_records = list_disbursements()
    assert len(all_records) >= 1
    # Ensure our record is in the list
    found = any(r['intent_id'] == intent_id for r in all_records)
    assert found

def test_intent_not_found():
    try:
        confirm_disbursement('non-existent-id')
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "not found" in str(e)

if __name__ == '__main__':
    test_record_and_confirm()
    test_intent_not_found()
    print("All disbursement tests passed")
