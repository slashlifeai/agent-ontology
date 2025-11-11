# Legal-Facing Explainer

This document aims to clarify specific terminology within this technical framework for legal professionals and to map them to corresponding legal concepts.

**Disclaimer:** While this document provides interpretations and use cases for legal professionals, it is crucial to note that the Community Group's formal scope is strictly limited to defining machine-verifiable semantic structures. It does not define regulatory frameworks, compliance interpretations, or legal norms. The semantic structures provided are designed to be usable by such frameworks, but the legal interpretations themselves fall outside the CG's standardization efforts.

## Core Ontology Concepts and Legal Mappings

| Ontology Concept | Legal Concept (English)      | Explanation (English)                                  |
| :--------------- | :--------------------------- | :------------------------------------------------------- |
| `Agent`          | Agent (incl. Legal Entity)   | Can have limited liability                             |
| `Intent`         | Declaration of Intent        | Auditable                                              |
| `Delegation`     | Authorization / Mandate      | Validity period, ultra vires, revocation               |
| `ExecutionRecord`| Factual Evidence             | Replayable, immutable                                  |
| `Narrative`      | Case File / Record of Events | State record, tamper-proof                             |
| `Capability`     | Legal Capacity / Authority   | Specific scope of actions                              |

## Delegation (Quasi-Mandate / Agency)

In our system, `Delegation` refers to the process by which one entity (the principal) authorizes another entity (the agent) to perform specific tasks on its behalf. Legally, this can correspond to a "quasi-mandate" or "agency" relationship.

- **Quasi-Mandate:** When the authorized task is not a legal act, such as performing a calculation or data processing, the relationship is analogous to a quasi-mandate in civil law.
- **Agency:** When the authorized task involves a legal act, such as signing a contract or conducting a transaction on behalf of the principal, the relationship constitutes an agency.

Every `Delegation` is recorded, clearly defining the scope of authority, duration, and the rights and obligations of both parties, to serve as a basis in case of future disputes.

## Narrative (Digital Evidence)

A `Narrative` is a chronologically ordered log of all significant events within the system. These events include, but are not limited to, delegations of authority, declarations of intent, execution of actions, and system acknowledgments. This record can be considered "digital evidence" in a legal context.

The design of the `Narrative` ensures its integrity and non-repudiation, allowing it to be admissible as evidence in legal proceedings to prove the occurrence and sequence of specific events.

## Intent (Declaration of Intent)

In this system, an `Intent` refers to the explicit expression by a user or agent of a specific goal they wish to achieve. This is legally equivalent to a "declaration of intent."

- **Intention to Create Legal Relations:** The content of the `Intent` clearly specifies the legal effect or business objective the actor wishes to achieve.
- **Expression of Intent:** Submitting this `Intent` through the system constitutes the act of expressing that intent.

The system precisely records the content, submission time, and originator of the `Intent` to ensure the authenticity and accuracy of the declaration.

## Act / Report / Ack (Procedural Steps)

`Act`, `Report`, and `Ack` are standardized interaction steps defined within the system to ensure the clarity and traceability of all procedures.

- **Act:** The specific operation performed by an agent based on a received `Intent`.
- **Report:** After completing an `Act`, the agent reports the execution results back to the principal.
- **Ack (Acknowledgment):** Upon receiving a `Report`, the principal confirms the result.

Together, these steps form a complete procedural chain, with each step clearly logged, which can be used to clarify the responsibilities of each party in the process.

## Execution Record (Fact / Factum)

An `Execution Record` is a detailed log of the process and outcome of an `Act`. This record legally constitutes a "fact" (factum)—an event that has objectively occurred.

This record includes the execution time, operational details, input and output data, etc., providing strong evidence for the "constituent facts" of a legal case.

## SHACL (Legality Check)

SHACL (Shapes Constraint Language) is used in this system to define the expected structure and rules for data. Its function is analogous to a "legality check" in legal proceedings.

- **A Priori Review:** Before data is processed or stored, the system uses SHACL rules to validate it, ensuring it conforms to predefined formats and legal requirements (e.g., ensuring all necessary fields are completed).
- **Ongoing Compliance:** SHACL rules help ensure the ongoing compliance of system operations, preventing invalid or illegal data from entering the system.

## Conflict (Arbitration / Resolution)

When disputes arise between participants in the system, such as differing interpretations of an `Execution Record`, we have designed a corresponding `Conflict` resolution mechanism.

This mechanism is primarily oriented towards "arbitration." The system will submit all relevant digital evidence (such as `Delegation`, `Intent`, `Execution Record`) to a designated arbitration body or smart contract, which will then adjudicate based on predefined rules or legal clauses to achieve efficient and impartial dispute resolution.

## 12 Use Cases for Semantic Delegation in the Legal Field

Semantic delegation provides a robust framework for managing complex interactions between automated agents and humans. Below are 12 practical use cases in the legal domain.

1.  **Multi-Agent Delegation Chain Traceability:** In complex transactions involving multiple agents (e.g., a buyer's agent, a seller's agent, and a payment agent), the system provides an immutable record of how authority was delegated, creating a clear and traceable chain of command.

2.  **Liability Allocation (Shared vs. Divided):** The delegation record can explicitly define liability terms. For instance, it can state whether two agents acting jointly are jointly and severally liable or if their liability is divided based on their specific roles.

3.  **Attribution of Responsibility for Task Failure:** When a process fails, the detailed `Execution Record` and delegation chain allow for precise attribution of fault. It becomes possible to identify which agent failed to perform its duty as specified in the `Delegation`.

4.  **Checking for Ultra Vires Actions by AI Agents:** The system can use SHACL rules to automatically check if an AI agent's actions (`Act`) exceed the scope of its granted authority (`Delegation`). This prevents unauthorized actions and provides a basis for invalidating such acts.

5.  **Narrative Replay in Arbitration:** During a dispute, the `Narrative` can be replayed chronologically to an arbitrator or judge. This provides an objective, step-by-step reconstruction of events, minimizing factual disputes.

6.  **Defining Auditable Events:** The ontology can be used to semantically tag certain events (e.g., `payment:Transfer`, `identity:VerifyCredential`) as requiring a formal audit trail. This helps organizations meet regulatory and compliance requirements automatically.

7.  **Distinguishing "Declarations of Intent" from "Technical Acts":** The framework provides a clear distinction between a legally significant `Intent` (e.g., "I agree to the terms") and a mere `Act` (e.g., "process data"). This helps determine which actions create legal obligations.

8.  **Automated Compliance Monitoring:** By encoding legal and contractual rules into SHACL shapes, the system can continuously monitor delegations and executions for compliance with regulations like GDPR, HIPAA, or specific contract clauses.

9.  **Dynamic Consent Management:** User consent can be captured as a `Delegation`. If a user revokes consent, the delegation is invalidated, and the system can automatically halt any data processing activities related to that consent, providing a clear audit trail.

10. **Smart Contract Integration:** A `Delegation` chain can be translated into a smart contract. For example, an `Intent` to purchase goods could trigger a smart contract that only releases payment (`Act`) upon receiving a `Report` of successful delivery.

11. **Verifying Evidence Integrity:** The cryptographic signatures on `Execution Records` and `Narratives` ensure they are tamper-proof, making them reliable and verifiable evidence that can be submitted in court.

12. **Managing Cross-Jurisdictional Agreements:** In international transactions, the `Delegation` can include jurisdictional metadata. This helps to automatically determine which country's laws apply to the agreement and where disputes should be resolved.

