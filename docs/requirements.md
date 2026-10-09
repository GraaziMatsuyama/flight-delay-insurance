# Project Requirements

## Participants
- Customer: purchases insurance and submits a claim.
- Insurer: funds the contract.
- Authorised reporter: records the flight delay.

## Insurance rules
1. A customer must purchase the policy before departure.
2. Each policy belongs to one customer and one flight.
3. The premium is 0.01 test ETH.
4. The compensation is 0.05 test ETH.
5. A delay of 120 minutes or more qualifies for compensation.
6. A shorter delay does not qualify.
7. Only the authorised reporter can record the flight result.
8. The flight result can only be recorded after the scheduled departure.
9. Only the policy owner can submit its claim.
10. Each policy can receive compensation only once.
11. The contract must reserve enough funds for each policy sold.
12. Once recorded, the flight result cannot be changed in this prototype.

## Information stored
- Policy ID
- Customer's wallet address
- Flight identifier and scheduled departure
- Delay in minutes
- Whether the flight result has been reported
- Whether compensation has been paid

## Planned checks
- Purchase before departure succeeds.
- Purchase at or after departure fails.
- A delay of 119 minutes does not qualify.
- Delays of 120 and 121 minutes qualify.
- An unauthorised account cannot report a delay.
- A customer cannot claim another customer's policy.
- A second compensation payment fails.
- A purchase fails if there are insufficient unreserved funds.
- Reporting a flight result before departure fails.
- Changing an already recorded flight result fails.

## Scope
This is an academic prototype using simulated flight data and local test funds. 
The amounts and delay threshold are fictional insurance conditions.
