# Research: Flight Delay Insurance Using Blockchain

## 1. Proposed business model

This project demonstrates a simplified form of parametric insurance.
Eligibility depends on a predefined event: a reported flight delay
of at least 120 minutes.

The customer purchases a policy before scheduled departure for
0.01 test ETH. The insurer provides funding, and the contract reserves
0.05 test ETH for each policy sold. After an authorised reporter
records a qualifying delay, the policy owner can request compensation.

These amounts and the 120-minute threshold are fictional project rules.
The prototype does not assess whether premiums would cover claims
and operating costs in a real insurance business.

## 2. Why use blockchain?

A smart contract can hold funds and apply predefined payment rules.
Transactions and contract state can be inspected, allowing participants
to check purchases, reported delays and compensation payments.

Ethereum transactions are cryptographically signed instructions.
Signatures authenticate the sending account, while contract code
determines which actions that account may perform
(Ethereum.org, n.d.-c).

The potential change to a conventional insurance process is that
eligibility checks and payment execution move into shared contract
code. However, the insurer and external information provider still
have responsibilities. Blockchain does not remove every intermediary
or source of trust.

A conventional application and database could implement similar
business rules with less technical complexity. Blockchain is more
appropriate when independently verifiable transactions and shared
execution rules justify its additional costs.

The Ganache demonstration verifies local functionality. It does
not demonstrate operation across an independent public network.

## 3. Benefits and challenges

### Potential benefits

- Consistent application of the premium and compensation rules.
- Traceable records of purchases, reports and payments.
- Funds reserved before accepting additional policies.
- Prevention of duplicate purchases and repeated compensation.
- Less manual work in checking eligibility after a delay is reported.

These are design benefits. The project has not measured processing
time, operating costs or improvements over a conventional system.

### Challenges

The main challenge is the reliability of flight information.
Smart contracts cannot directly retrieve external flight data.
An oracle or another reporting mechanism must supply that information
(Ethereum.org, n.d.-b).

The prototype uses one authorised reporter. This account could submit
incorrect information or fail to report a flight. Once accepted,
the recorded result cannot be corrected in this implementation.

Other limitations include transaction fees, public records,
key management and defects in deployed code. There is no claim
expiry or insurer withdrawal function. Funds for qualifying policies
remain reserved until customers claim them.

## 4. Cryptography and authentication

### Transaction signatures

For transactions sent by externally owned accounts, Ethereum uses
digital signatures to authenticate the sender. The contract then
checks msg.sender against the insurer, reporter or policy owner
(Ethereum.org, n.d.-c).

Digital signatures are the main cryptographic mechanism relevant
to authenticating the participants' transactions. The Solidity
contract relies on Ethereum's transaction validation rather than
implementing a separate signature algorithm.

The Python demonstration uses unlocked local Ganache accounts.
It does not implement production wallet or private-key management.

### Flight identification with Keccak-256

The contract generates a bytes32 flight identifier using:

keccak256(abi.encode(flightNumber, scheduledDeparture))

Keccak-256 produces a 256-bit hash. Including both values allows
the contract to distinguish flights with the same number but
different departure timestamps (Solidity, n.d.-a).

The flight number must be entered consistently. Differences in
capitalisation or spaces produce different inputs and identifiers.

Hashing does not encrypt the information or verify the reported
delay. This prototype does not provide confidentiality for flight
and policy records.

### Payment protection

The claim function follows Checks-Effects-Interactions:
it validates the claim, marks the policy as paid and reduces the
reserve before making the external payment call.

This ordering protects against claiming the same policy again
during the transfer. If the transfer fails, the transaction reverts
the state changes (Solidity, n.d.-b).

These protections address specific risks and do not replace
a complete security audit.

## 5. Recent advancements and future development

### Layer 2 transaction costs

Ethereum's Dencun upgrade activated on 13 March 2024 and introduced
EIP-4844 data blobs. Blobs provide a more cost-effective way for
rollups to publish data to Ethereum (Ethereum.org, n.d.-a).

A future insurance application could investigate a layer 2 network
to reduce the cost of purchasing policies and claiming payments.
This is a proposed application of the technology, rather than a
benefit measured by this project.

The current prototype targets Shanghai on Ganache. It does not
implement Dencun blobs or a layer 2 network.

### External flight information

A future version could replace manual reporting with an oracle
service connected to flight information sources.

The design would need to assess source accuracy, availability,
reporting costs and how conflicting results are handled.
Using multiple oracle nodes does not automatically guarantee
independent or truthful underlying data
(Ethereum.org, n.d.-b).

## 6. Findings from the prototype

The complete workflow was executed through Python and Ganache:
deployment, funding, policy purchase, delay reporting and compensation.

With 1 test ETH of initial funding, one policy increased the contract
balance to 1.01 ETH and reserved 0.05 ETH. Following a qualifying
120-minute delay and a successful claim, the balance was 0.96 ETH
and reserved funds were zero.

Remix tests also covered delays of 119 and 121 minutes and protection
scenarios such as unauthorised actions, repeated claims and
insufficient available funds.

These results support the functionality of the tested rules.
They do not establish production security, commercial viability
or real-world flight-data accuracy.

## References

Ethereum.org (n.d.-a) ‘Cancun-Deneb (Dencun)’.
Available at: https://ethereum.org/roadmap/dencun/
(Accessed: 30 October 2026).

Ethereum.org (n.d.-b) ‘Oracles’.
Available at: https://ethereum.org/developers/docs/oracles/
(Accessed: 30 October 2026).

Ethereum.org (n.d.-c) ‘Transactions’.
Available at: https://ethereum.org/developers/docs/transactions/
(Accessed: 30 October 2026).

Solidity (n.d.-a) ‘Units and globally available variables’.
Available at:
https://docs.soliditylang.org/en/v0.8.34/units-and-global-variables.html
(Accessed: 30 October 2026).

Solidity (n.d.-b) ‘Security considerations’.
Available at:
https://docs.soliditylang.org/en/v0.8.34/security-considerations.html
(Accessed: 30 October 2026).