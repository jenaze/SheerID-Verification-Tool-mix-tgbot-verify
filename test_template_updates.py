"""Quick test for updated document templates"""
import sys
sys.path.insert(0, '.')

from utils.document_templates import (
    get_random_university,
    generate_university_id,
    get_random_term,
    get_random_courses,
    get_tuition_breakdown,
    get_academic_year,
)
from one.name_generator import NameGenerator

print("=" * 60)
print("Testing Updated Document Templates")
print("=" * 60)

# Test University ID generation
print("\n1. Testing University IDs:")
universities_to_test = ['mit', 'columbia', 'nyu', 'berkeley', 'gatech']
for uni_key in universities_to_test:
    from utils.document_templates import UNIVERSITIES
    uni_config = UNIVERSITIES[uni_key]
    sid = generate_university_id(uni_key)
    print(f"   {uni_config['short_name']}: {sid} (format: {uni_config.get('id_format', 'default')})")

# Test Term generation
print("\n2. Testing Semester Dates:")
for _ in range(3):
    term, dates = get_random_term()
    print(f"   {term} ({dates})")

# Test Course generation
print("\n3. Testing Course Generation:")
courses = get_random_courses(4)
for c in courses:
    print(f"   {c['code']} (CRN: {c['crn']}) - {c['title']}")
    print(f"      Time: {c['time']}, Room: {c['room']}, Credits: {c['units']}")

# Test Tuition Breakdown
print("\n4. Testing Tuition Breakdown:")
breakdown = get_tuition_breakdown(25000)
total = 0
for name, amt in breakdown:
    print(f"   {name}: ${amt:,.2f}")
    total += amt
print(f"   ---------------------")
print(f"   TOTAL: ${total:,.2f}")

# Test Academic Year
print(f"\n5. Academic Year: {get_academic_year()}")

# Test Name Generator
print("\n6. Testing Name Generator:")
for _ in range(5):
    name = NameGenerator.generate()
    print(f"   {name['full_name']}")

print("\n" + "=" * 60)
print("All tests completed successfully!")
print("=" * 60)
