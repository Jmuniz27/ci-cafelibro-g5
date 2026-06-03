# CaféLibro

| Feature | Owner |
|---|---|
| Feature 1: Register a member | Isabella Martin |
| Feature 2: Loan a book | Jose Luis Chong |
| Feature 3: Return a book | Zahid Diaz |
| Feature 4: List member loans | Gabriela Jimenez |
| Feature 5: Overdue loans report | Annabella Sanchez |
| Feature 6: Register a book | Juan Munizaga |

---
## Data Contract — data.json

Exact schema everyone must follow. Do not change it unilaterally.

```json
{
  "books": [
    { "code": "B001", "title": "Clean Code", "available": true }
  ],
  "members": [
    { "id": "M001", "name": "Ana Torres" }
  ],
  "loans": [
    { "book_code": "B001", "member_id": "M001", "loan_date": "2026-06-01", "due_date": "2026-06-15" }
  ]
}
```

Rules derived from the schema:
- `available` is the only field that tracks a book's state. Features 2 and 3 write it; all others only read it.
- An active loan = an entry in loans without a `returned` flag (deletion model: returning a book removes the entry).
- Dates always in YYYY-MM-DD format. Features 2 and 5 depend on this.

## Business Rules

- A book already on loan (available == false) cannot be loaned again → ValueError.
- A member cannot hold more than 3 active loans simultaneously → ValueError.
- You cannot loan to a member_id that does not exist in members → ValueError.
- You cannot loan a book_code that does not exist in books → ValueError.
- Returning a book not present in loans is an error, not silent → ValueError.
- Feature 2 enforces all loan rules. Features 3, 4, 5 trust the state is consistent and do not re-validate.

## Branch Naming Convention

- feature/f1-register-member
- feature/f2-loan-book
- feature/f3-return-book
- feature/f4-list-member-loans
- feature/f5-overdue-loans
- feature/f6-register-book
