Scope Boundary Statement (Can be directly included in README or Explainer)

✅ In Scope

This Community Group focuses exclusively on defining the semantic structures that enable verifiable and interoperable interaction between heterogeneous agents.
The scope includes:
1. Interaction Semantics
Formal definitions for Intent, Delegation, Capability advertisement, ExecutionRecord, and related CommunicativeActs.
2. Identity and Verifiability Primitives
Use of Decentralized Identifiers (DIDs), Verifiable Credentials (VCs), signatures, and provenance structures needed to establish trust in agent actions.
3. Narrative Model
The definition of an append-only, context-complete semantic log that provides traceability, accountability, and explainability of agent behavior.
4. Semantic Ledger Model
A logical model for representing immutable, ordered, verifiable records.
This is a semantic abstraction—no blockchain or specific implementation technology is implied.
5. Conformance Definitions
Minimal normative requirements for interpreting CommunicativeActs, Delegations, and other semantic elements in a consistent manner across implementations.
6. Machine-Readable Ontology Artifacts
RDF/OWL vocabularies, JSON-LD contexts, SHACL shapes that express the above concepts in a formally verifiable way.

---

❌ Out of Scope

The following topics are explicitly not within the scope of this Community Group. These topics may be implemented by downstream systems, but will not be defined, standardized, or constrained by this CG:
1. Transport Protocols
No definition or modification of any transport layer (e.g., HTTP, WebSockets, TCP, UDP, QUIC).
Transport is treated as an opaque carrier of serialized semantic payloads.
2. Internal Agent Reasoning Models
The CG does not define:
- LLM behavior
- planning algorithms
- inference engines
- symbolic solvers
- internal cognitive architectures
These are implementation choices left entirely to agent developers.
3. Execution Backends and Compute Targets
The CG does not specify how semantic instructions are executed on:
- CPU
- GPU
- TPU
- WASM
- MLIR
- hardware accelerators
Any compilation or lowering pathway from semantic models to compute IR is outside the CG scope.
4. Economic Models and Payment Systems
The CG does not define:
- settlement systems
- payment rails
- economic incentives
- token models
Although semantic structures (e.g., PaymentIntent) may be modeled, financial mechanisms themselves are not standardized.
5. Blockchain / Distributed Ledger Technology
The CG does not mandate or define consensus protocols, chain structures, or DLT implementations.
A ledger in this CG is purely a logical abstraction.
6. Domain-Specific Knowledge or Vertical Ontologies
No legal, medical, financial, manufacturing, or industry-specific knowledge models are defined.
The ontology remains strictly domain-neutral.
7. Governance, Policy, or Legal Interpretation
The CG does not define regulatory frameworks, compliance interpretations, or legal norms.
It only provides machine-verifiable semantic structures usable by such frameworks.
8. Runtime Implementations or SDKs
The CG does not produce executable software, agents, runtimes, or OS implementations.
Reference code may be published, but not standardized.