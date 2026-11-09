# Unresolved questions

Draft implementation descriptions do not adopt normative profiles. Their
decision, protocol and conformance work follows LIP-0001.

| Question | Location and boundary |
| --- | --- |
| Adoption and coexistence of landlord, locator and action-service profiles | LIP-0004/0005/0006 remain Draft; historical v0.1 requirements and evidence retain their own meaning. |
| Common action vocabulary versus wallet-specific encoding and limits | [LIP-0006 open questions](lips/LIP-0006-grant-gated-actions.md#open-questions); cross-language canonical rules and complete vectors precede normative interoperability claims. |
| Further locator networks and endpoint discovery | [LIP-0005 open questions](lips/LIP-0005-op-return-locator.md#5-open); current closed name schemas do not acquire blob/tracker fields. |
| Name-action continuation, remote transport, broker routing and non-coin budgets | LIP-0006 specifies the implemented wallet v1 choices; extensions need separate action/effect contracts. |
| Deployment qualification, key/UID provisioning and journal migration/recovery | LIP-0006; mainnet configuration support and same-UID fixtures do not establish actual cross-user custody or anti-rollback guarantees. |
| Booking-to-wallet terms and an agent-controlled small-wallet tier | LIP-0006; incompatible byte formats cannot be substituted, and refill/lease policy needs an explicit contract. |

Existing questions for single use and detached grants remain in LIP-0002 and
LIP-0003. This index does not change their status or the preserved evidence.
