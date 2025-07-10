# Correlation

This extension defines attributes for tracking occurrence relationships and
causality in distributed systems, enabling comprehensive traceability through
correlation and causation identifiers.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

## Attributes

### correlationid

- Type: `String`
- Description: An identifier that groups related events within the same logical
  flow or business transaction. All events sharing the same correlation ID are
  part of the same workflow.
- Constraints
  - OPTIONAL
  - If present, MUST be a non-empty string

### causationid

- Type: `String`
- Description: The unique identifier of the event that directly caused this
  event to be generated. This SHOULD be the `id` value of the causing event.
- Constraints
  - OPTIONAL
  - If present, MUST be a non-empty string

## Usage

The Correlation extension provides two complementary mechanisms for tracking
event relationships:

1. **Correlation ID**: Groups all events that are part of the same logical flow,
   regardless of their causal relationships
2. **Causation ID**: Tracks the direct parent-child relationships between events
   in a causal chain

These attributes can be used independently or together, depending on the correlation
requirements of your system.

### Correlation vs Causation

Understanding the distinction between these two concepts is crucial:

- **Correlation ID** answers: "Which events are part of the same business
  transaction?"
- **Causation ID** answers: "Which specific event directly triggered this
  event?"

### Example Scenario

Consider an e-commerce order processing flow:

1. User initiates checkout (correlation ID: "txn-abc-123" is created)
2. Order is placed (Event A)
3. Payment is processed (Event B, caused by A)
4. Inventory is checked (Event C, caused by A)
5. Shipping is scheduled (Event D, caused by C)
6. Notification is sent (Event E, caused by D)

In this scenario:

- All events share the same `correlationid`: "txn-abc-123"
- Each event has a `causationid` pointing to its direct trigger:
  - Event B and C have `causationid`: "order-123" (Event A's ID)
  - Event D has `causationid`: "inventory-456" (Event C's ID)
  - Event E has `causationid`: "shipping-789" (Event D's ID)

## Examples

### Example 1: Complete Correlation Chain

Initial Order Event:

```json
{
  "specversion": "1.0",
  "type": "com.example.order.placed",
  "source": "https://example.com/orders",
  "id": "order-123",
  "correlationid": "txn-abc-123",
  "data": {
    "orderId": "123",
    "customerId": "456"
  }
}
```

Payment Processing (triggered by order):

```json
{
  "specversion": "1.0",
  "type": "com.example.payment.processed",
  "source": "https://example.com/payments",
  "id": "payment-789",
  "correlationid": "txn-abc-123",
  "causationid": "order-123",
  "data": {
    "amount": 150.0,
    "currency": "USD"
  }
}
```

Inventory Check (also triggered by order):

```json
{
  "specversion": "1.0",
  "type": "com.example.inventory.checked",
  "source": "https://example.com/inventory",
  "id": "inventory-456",
  "correlationid": "txn-abc-123",
  "causationid": "order-123",
  "data": {
    "items": ["sku-001", "sku-002"],
    "available": true
  }
}
```

Shipping Scheduled (triggered by inventory check):

```json
{
  "specversion": "1.0",
  "type": "com.example.shipping.scheduled",
  "source": "https://example.com/shipping",
  "id": "shipping-012",
  "correlationid": "txn-abc-123",
  "causationid": "inventory-456",
  "data": {
    "carrier": "FastShip",
    "estimatedDelivery": "2024-01-15"
  }
}
```

### Example 2: Error Handling with Correlation

When an error occurs, the correlation attributes help identify both the affected
transaction and the specific trigger:

```json
{
  "specversion": "1.0",
  "type": "com.example.payment.failed",
  "source": "https://example.com/payments",
  "id": "error-345",
  "correlationid": "txn-abc-123",
  "causationid": "payment-789",
  "data": {
    "error": "Insufficient funds",
    "retryable": true
  }
}
```

### Example 3: Fan-out Pattern

A single event can cause multiple downstream events:

```json
{
  "specversion": "1.0",
  "type": "com.example.order.fulfilled",
  "source": "https://example.com/fulfillment",
  "id": "fulfillment-567",
  "correlationid": "txn-abc-123",
  "causationid": "shipping-012",
  "data": {
    "completedAt": "2024-01-14T10:30:00Z"
  }
}
```

This might trigger multiple notification events, all with the same causationid:

```json
{
  "specversion": "1.0",
  "type": "com.example.notification.email",
  "source": "https://example.com/notifications",
  "id": "notify-email-890",
  "correlationid": "txn-abc-123",
  "causationid": "fulfillment-567",
  "data": {
    "recipient": "customer@example.com",
    "template": "order-fulfilled"
  }
}
```

```json
{
  "specversion": "1.0",
  "type": "com.example.notification.sms",
  "source": "https://example.com/notifications",
  "id": "notify-sms-891",
  "correlationid": "txn-abc-123",
  "causationid": "fulfillment-567",
  "data": {
    "recipient": "+1234567890",
    "message": "Your order has been fulfilled!"
  }
}
```

## Best Practices

1. **Correlation ID Generation**: Generate correlation IDs at the entry point of
   your system (e.g., API gateway, UI interaction)
2. **Causation ID Propagation**: Always set the causation ID to the `id` of the
   event that directly triggered the current event
3. **Consistent Usage**: If you start using these attributes in a flow, use them
   consistently throughout
4. **ID Format**: Use globally unique identifiers (e.g., UUIDs) to avoid
   collisions across distributed systems
5. **Retention**: Consider the retention implications when designing queries
   based on these attributes
