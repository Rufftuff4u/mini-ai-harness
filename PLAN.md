# ORDER-101 plan

- Add `cancel_order` that looks up an order, allows only `NEW`, and changes it to `CANCELLED`.
- Add tests for successful cancellation, ineligible statuses, and unknown IDs while preserving `get_order` coverage.
- Run the requested unittest discovery suite.
