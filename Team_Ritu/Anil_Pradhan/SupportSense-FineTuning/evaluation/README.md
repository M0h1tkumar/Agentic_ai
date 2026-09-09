# Evaluation

The fine-tuned model was evaluated on 300 unseen test examples.

## Result

**Accuracy: 91.67%**

- Correct: 275
- Incorrect: 25

Error analysis was performed on all 25 incorrect predictions.

The most common confusion was between:

- `card_arrival`
- `card_delivery_estimate`

Other semantic overlaps included:

- `exchange_rate`
- `card_payment_wrong_exchange_rate`
- `fiat_currency_support`
