# Project Design

## Purpose
This project demonstrates flight delay insurance using a Solidity
smart contract. A customer buys a policy before departure and can
claim compensation if an authorised reporter records a delay of
120 minutes or more.

All flight information is simulated and all funds are test ETH.
The insurance conditions are fictional rules for this project.

## Participants
- Insurer: deploys and funds the contract.
- Customer: purchases a policy and requests compensation.
- Reporter: records the flight delay after scheduled departure.
- Smart contract: checks the rules, stores records and transfers funds.

## Main Rules
- Each policy costs 0.01 test ETH.
- Compensation is 0.05 test ETH.
- A delay of at least 120 minutes qualifies.
- Policies must be purchased before scheduled departure.
- Each customer can buy only one policy per flight.
- The contract must have enough unreserved funds to cover a new policy.
- Only the reporter can record a delay.
- A recorded delay cannot be changed.
- Only the policy owner can claim compensation.
- Each policy can receive compensation only once.

## Process
1. The insurer deploys and funds the contract.
2. A customer purchases a policy for a future flight.
3. The contract records the policy and reserves 0.05 test ETH.
4. After scheduled departure, the reporter records the delay.
5. If the delay is below 120 minutes, the flight's reserves are released.
6. If the delay is 120 minutes or more, the customer can claim.
7. The contract marks the policy as paid, reduces the reserve
   and transfers compensation.

Releasing a reserve changes the amount committed to potential claims.
It does not transfer ETH out of the contract.

## Stored Information
Each flight stores its scheduled departure, delay in minutes
and whether a result has been reported.

Each policy stores the customer address, flight identifier
and whether compensation has been paid.

The contract also tracks the total policy count, reserved funds,
policy count per flight and duplicate purchases.

## Flight Identification
The contract uses keccak256 with abi.encode to create a flight
identifier from the flight number and scheduled departure timestamp.

This distinguishes flights with the same number on different dates.
The same flight number and timestamp must be used consistently.

Hashing provides an identifier; it does not encrypt flight information
or prove that the reported delay is true.

## Security
The contract checks the sender's address to restrict funding,
delay reporting and compensation claims.

It marks a policy as paid and reduces reserved funds before
transferring compensation. This prevents the same policy from being
claimed again during the transfer.

If the transfer fails, the transaction reverts, including the changes
to the paid status and reserved funds.

Events record funding, policy purchases, delay reports
and compensation payments.

## Tools and Current Status
- Solidity: implements the insurance rules.
- Remix VM: used for development and manual testing.
- Ganache: planned for local blockchain deployment.
- Python: planned for interacting with the deployed contract.

## Benefits and Limitations
The contract applies consistent rules and provides a shared record
of purchases, reports and payments.

However, it depends on the reporter providing accurate information.
The prototype does not connect to an airline API or a decentralised
oracle, verify passenger bookings or assess real insurance risk.

Flight and policy records are publicly readable on the blockchain.
A wallet address does not verify a customer's real-world identity.

Funds remain reserved for qualifying policies until they are claimed.
There is currently no claim expiry or insurer withdrawal function.