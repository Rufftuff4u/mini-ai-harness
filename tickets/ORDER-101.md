# ORDER-101: Cancel an order

## Requirement
Allow cancellation only when an order has status NEW.

## Acceptance criteria
- Cancel a NEW order, changing its status to CANCELLED.
- Reject cancellation of SHIPPED or already CANCELLED orders.
- Reject unknown order IDs.
- Add automated tests for success and failure cases.
- Preserve existing get_order behavior.
