# AI Agent Ontology

**A W3C Community Group Draft for a Standardized Agent Communication Language**

---

### **Project Status: W3C Community Group Draft**

This repository contains the draft work of the [Semantic Agent Communication Community Group (SACG)](https://www.w3.org/community/blog/2025/11/09/proposed-group-semantic-agent-communication-community-group/). Our mission is to create a shared, open, and machine-readable language that allows AI agents to communicate, collaborate, and trust each other in a standardized, auditable way.

### **The Vision: A Common Language for Agents**

Today's AI agents often exist as "digital islands," unable to communicate effectively. We are building the common language to solve this, defining core concepts every agent can understand:
*   **Who are you?** (Identity)
*   **What can you do?** (Capability)
*   **Who gave you that authority?** (Delegation)
*   **How can we prove what you did?** (Accountability & Ledger)

This core set of concepts forms a **Minimal Communicable Interface**, enabling basic interoperability and trust, with the flexibility to extend for more complex interactions.

---

### **Live Resources & Interactive Tools**

Explore the ontology and specifications on our live GitHub Pages site.

*   [**Read the Core Ontology Specification (W3C ReSpec Format)**](https://slashlifeai.github.io/agent-ontology/specs/w3c/core-ontology.html)
*   [**Explore the Full Vocabulary Index**](https://slashlifeai.github.io/agent-ontology/specs/vocabulary/)
*   [**Interactive JSON-LD Viewer**](https://slashlifeai.github.io/agent-ontology/tools/jsonld-viewer.html)
*   [**Interactive JSON Schema Viewer**](https://slashlifeai.github.io/agent-ontology/tools/jsonschema-viewer.html)

---

### **Developer Quickstart**

#### **1. Explore the Ontology**
*   The formal definitions of all concepts are in the [`ontologies/`](./ontologies/) directory as `.ttl` files.
*   Rich, real-world usage examples are in the [`ontologies/examples/`](./ontologies/examples/) directory.

#### **2. See the API Mapping**
*   To understand how to implement this ontology in a RESTful API, see our [`specs/openapi-example.yml`](./specs/openapi-example.yml).

#### **3. Generate Vocabulary**
*   You can regenerate the Markdown vocabulary documentation at any time by running:
    ```bash
    pip install rdflib
    python generate_vocabulary.py
    ```

---

### **How to Contribute**

This is an open, community-driven project. We welcome contributions of all kinds.

1.  **Join the Conversation:** The best way to start is by [**joining the W3C Community Group**](https://www.w3.org/community/blog/2025/11/09/proposed-group-semantic-agent-communication-community-group/) and participating in the discussion.
2.  **Read the Contribution Guidelines:** For technical contributions, please see our [**CONTRIBUTING.md**](./CONTRIBUTING.md) file.
3.  **Open an Issue:** Have an idea or a question? [Open a GitHub Issue](https://github.com/slashlifeai/agent-ontology/issues).

### **License**

This work is licensed under the [W3C Software and Document License](https://www.w3.org/Consortium/Legal/2015/doc-license.html).

