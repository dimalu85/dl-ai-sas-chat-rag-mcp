# Business Goals

No relevant information found in the input documents for "Business Goals".

---

# Business Architecture Problems And Gaps

### Business Architecture Problems

> 1:
>
> #: 1
>
> Category: governance
>
> Description: Fundamental architectural disconnect: the delivered, value-producing pipeline bypasses RAG entirely (RAG path is secondary/unused for outputs), creating mismatch between stated architecture and actual implementation.
>
> Impact: High
>
> Status: active
>
> **References**
>
> | Source Location | Source Quote |
> |----|----|
> | Task.docx.txt, Use-Case Analysis: Is This Actually a RAG Application? | The submission has a **fundamental architectural disconnect**: the main value-producing pipeline (batch document analysis → CSV → Plotly charts → HTML report) **does not use RAG at all**. It is a direct LLM processing pipeline. |
> | Task.docx.txt, Use-Case Analysis: Is This Actually a RAG Application? | **You could delete the vector store, embeddings, ChromaDB, and the retriever entirely, and the main output (report + charts) would be identical.** |

> 2:
>
> #: 2
>
> Category: information_and_data
>
> Description: Document-processing approach truncates content (8000 characters), risking incomplete/incorrect extraction for long documents and undermining information completeness.
>
> Impact: High
>
> Status: active
>
> **References**
>
> | Source Location | Source Quote |
> |----|----|
> | Task.docx.txt, Actual architecture (Path A) | PDF Files → Raw Text Concatenation → Truncate to8000 chars → Direct LLM Call → CSV → Charts → HTML |
> | Task.docx.txt, Where RAG Would Actually Add Value in This Use-Case | Instead of truncating to8000 chars (losing ~80% of content for large PDFs like Module9.4 at152 pages), the system could: |

> 3:
>
> #: 3
>
> Category: governance
>
> Description: No structured RAG evaluation/quality measurement (metrics, test sets, retrieval strategy comparison), reducing confidence and limiting ability to tune/improve retrieval and outputs.
>
> Impact: Medium
>
> Status: active
>
> **References**
>
> | Source Location | Source Quote |
> |----|----|
> | Task.docx.txt, Summary (Key Gaps) | - No RAG evaluation or quality metrics at all — this is a major missing section worth1.5 points |
> | Task.docx.txt, Section4. RAG Evaluation & Quality (0–1.5) | **No evaluation framework whatsoever** — no RAGAS, no faithfulness metrics, no precision/recall, no golden dataset, no comparison of retrieval strategies, no quality dashboard, no debug loop. |

> 4:
>
> #: 4
>
> Category: governance
>
> Description: No automated testing (unit/integration/automation) is present, creating reliability and maintainability risk and failing mandatory testing expectations.
>
> Impact: High
>
> Status: active
>
> **References**
>
> | Source Location | Source Quote |
> |----|----|
> | Task.docx.txt, Summary (Key Gaps) | - No tests of any kind |
> | Task.docx.txt, Section8. Testing (0–0.5) | What's missing:- No unit tests, no integration tests, no test files, no automated testing of any kind. |

> 5:
>
> #: 5
>
> Category: governance
>
> Description: Missing delivery/operational artifacts needed to run and maintain the solution (dataset accessibility, README/setup instructions, dependency/env artifacts).
>
> Impact: Medium
>
> Status: active
>
> **References**
>
> | Source Location | Source Quote |
> |----|----|
> | Task.docx.txt, Summary (Key Gaps) | - No dataset link, no README, no setup instructions |
> | Task.docx.txt, Section5. Working Application & Demo (0–1) | What's missing:- **No dataset link** — the PDFs are internal EPAM materials with no public download link.- **No README** with setup instructions (only a brief `comments.md`).- No web UI (notebook-only).- No `.env.example` or `requirements.txt`. |

> 6:
>
> #: 6
>
> Category: governance
>
> Description: Architecture/solution communication is incomplete: there is no diagram-type visualization (flow/relationship/graph), limiting architecture understanding and stakeholder communication.
>
> Impact: Low
>
> Status: active
>
> **References**
>
> | Source Location | Source Quote |
> |----|----|
> | Task.docx.txt, Summary (Key Gaps) | - No diagram-type visualization (graph, flowchart, relationship map) |
> | Task.docx.txt, Section3. Data Extraction & Visualization (0–2) | There is **no diagram type** (graph, flowchart, relationship diagram, entity map, knowledge graph). |

> 7:
>
> #: 7
>
> Category: technology_integration
>
> Description: Codebase maintainability and technical currency issues: deprecated framework APIs are used and implementation is a monolithic notebook with limited modularity/reuse.
>
> Impact: Medium
>
> Status: active
>
> **References**
>
> | Source Location | Source Quote |
> |----|----|
> | Task.docx.txt, Section7. Code Quality & Documentation (0–1) | Deprecated LangChain APIs used (`ConversationalRetrievalChain`, `LLMChain` — deprecated in LangChain0.2.x). |
> | Task.docx.txt, Section7. Code Quality & Documentation (0–1) | - **Monolithic notebook** — no modular Python files, no importable functions. |


### Business Architecture Gaps

> 1:
>
> #: 1
>
> Category: technology_integration
>
> Description: Gap between desired and current architecture: retrieval should be used for extraction (per-query relevant chunk retrieval) instead of direct-LLM over truncated raw text.
>
> Impact: High
>
> Status: planned_to_be_addressed
>
> **References**
>
> | Source Location | Source Quote |
> |----|----|
> | Task.docx.txt, Suggestions for the Student | 1. **Use retrieval for extraction**: For each analysis query, use the retriever to find relevant chunks within that document instead of truncating raw text. |

> 2:
>
> #: 2
>
> Category: business_capabilities
>
> Description: Gap in analytical capability: add cross-document comparative queries/analysis so the system supports corpus-level insights rather than only per-document extraction.
>
> Impact: Medium
>
> Status: planned_to_be_addressed
>
> **References**
>
> | Source Location | Source Quote |
> |----|----|
> | Task.docx.txt, Where RAG Would Actually Add Value in This Use-Case | 1. **Cross-document comparative analysis**: "Which modules cover overlapping topics?" or "How does the treatment of quality attributes differ between Module3.2 and Module8.1?" — these require retrieving relevant chunks from multiple documents. |

> 3:
>
> #: 3
>
> Category: business_processes
>
> Description: Gap in user interaction model: make Q&A/cross-document exploration the primary interface (not a batch pipeline with a tacked-on ask() function).
>
> Impact: Medium
>
> Status: planned_to_be_addressed
>
> **References**
>
> | Source Location | Source Quote |
> |----|----|
> | Task.docx.txt, Where RAG Would Actually Add Value in This Use-Case | 3. **Interactive exploration with context**: The `ask()` function does use RAG, but it's a tacked-on afterthought. A genuine use-case would make cross-document Q&A the primary interaction, with visualization built on RAG-retrieved answers. |

> 4:
>
> #: 4
>
> Category: technology_integration
>
> Description: Gap in handling long documents: implement hierarchical retrieval (small chunks for search, parent-section context) to eliminate truncation-driven information loss.
>
> Impact: High
>
> Status: planned_to_be_addressed
>
> **References**
>
> | Source Location | Source Quote |
> |----|----|
> | Task.docx.txt, Suggestions for the Student | 4. **Use hierarchical retrieval for long documents**: Small chunks for search → retrieve parent sections for context → pass to LLM. This eliminates the8000-char truncation problem entirely. |

> 5:
>
> #: 5
>
> Category: governance
>
> Description: Gap in assurance/quality management: implement structured RAG evaluation and compare RAG vs direct-LLM to measure accuracy/completeness and guide tuning.
>
> Impact: Medium
>
> Status: planned_to_be_addressed
>
> **References**
>
> | Source Location | Source Quote |
> |----|----|
> | Task.docx.txt, Suggestions for the Student | 5. **Compare RAG vs. direct LLM**: Run the same extraction with and without retrieval and measure which produces more accurate/complete results. |
> | Task.docx.txt, Section4. RAG Evaluation & Quality (0–1.5) | **No evaluation framework whatsoever** — no RAGAS, no faithfulness metrics, no precision/recall, no golden dataset, no comparison of retrieval strategies, no quality dashboard, no debug loop. |

> 6:
>
> #: 6
>
> Category: governance
>
> Description: Gap in non-functional requirements: add automated test coverage (unit + integration) to meet mandatory testing expectations.
>
> Impact: High
>
> Status: planned_to_be_addressed
>
> **References**
>
> | Source Location | Source Quote |
> |----|----|
> | Task.docx.txt, special_instructions | Test coverage is mandatory. |
> | Task.docx.txt, Section8. Testing (0–0.5) | What's missing:- No unit tests, no integration tests, no test files, no automated testing of any kind. |

> 7:
>
> #: 7
>
> Category: governance
>
> Description: Gap in operability/onboarding: provide dataset access and standard setup/documentation artifacts (README, requirements, env example).
>
> Impact: Medium
>
> Status: planned_to_be_addressed
>
> **References**
>
> | Source Location | Source Quote |
> |----|----|
> | Task.docx.txt, Section5. Working Application & Demo (0–1) | What's missing:- **No dataset link** — the PDFs are internal EPAM materials with no public download link.- **No README** with setup instructions (only a brief `comments.md`).- No web UI (notebook-only).- No `.env.example` or `requirements.txt`. |

> 8:
>
> #: 8
>
> Category: business_capabilities
>
> Description: Gap against stated target scope: build a combined chatbot (RAG + Agent/MCP) extended with an MCP server that queries a CSV via Pandas to answer natural-disaster questions.
>
> Impact: High
>
> Status: planned_to_be_addressed
>
> **References**
>
> | Source Location | Source Quote |
> |----|----|
> | Task.docx.txt, special_instructions | Create a chatbot, that will be composed from two of your previous tasks: from RAG module and from Agent/MCP module, however, extended with additional functionallity: ability to query infromation on natural disaster. In order to do that, create an MCP server, that will query CSV file with Pandas and return user responses to their question from chat. |


*Notes*

- Only one source artifact (Task.docx.txt) was provided; the identified problems/gaps reflect a learning-project/software-delivery context rather than an enterprise operating model.
- No business goals were provided (business_goals is {}), limiting the ability to assess strategy-to-capability alignment beyond what is explicitly stated in Task.docx.txt.



---

# Quality Attributes

#### Quality Attributes

> 1:
>
> Quality Attribute: composability
>
> Business Goals Alignment Reasoning: No Business Goals were provided (business_goals is {}). While multiple confirmed ASRs require composing the chatbot from a RAG module and an Agent/MCP module (CLM-001, CHAT-001, ARCH-001, VC-NLP-001, AIML-001), the business impact of composability cannot be rated against explicit goals.
>
> Business Goals Alignment: Unknown
>
> Business Capabilities Contribution Reasoning: Composability is directly required as the primary QA in multiple confirmed ASRs that define the architecture as a composition of a RAG module and an Agent/MCP module (CLM-001, CHAT-001, ARCH-001, VC-NLP-001, AIML-001). This directly enables Business Capability1 (Conversational Chatbot Delivery) and the composed enabling capabilities2 (RAG) and3 (Agent Tooling & MCP-based Orchestration).
>
> Business Capabilities Contribution: High
>
> *Preliminary Metrics*
>
> 1. Time/effort to swap/replace the RAG module implementation without changing the Agent/MCP module integration (**SUGGESTED**)
> 2. Number of integration points/interfaces required between RAG module and Agent/MCP module (lower is better) (**SUGGESTED**)
> 3. % of chatbot features that continue to work when running with a stubbed RAG module or stubbed Agent/MCP module (composition contract test pass rate) (**SUGGESTED**)
>
> Conflicts and Trade-offs: May trade off with performance: composing multiple modules (RAG + Agent/MCP) can add integration overhead and increase response time., May trade off with maintainability: more composable parts can increase integration complexity and the maintenance surface area.

> 2:
>
> Quality Attribute: interoperability
>
> Business Goals Alignment Reasoning: No Business Goals were provided (business_goals is {}). Although confirmed ASRs require interoperability between the chatbot, MCP server, and Pandas-based CSV querying (CLM-002, DATA-001, ARCH-002, VC-NLP-003, SIR-002), alignment to explicit business outcomes cannot be determined.
>
> Business Goals Alignment: Unknown
>
> Business Capabilities Contribution Reasoning: Interoperability is directly required by confirmed ASRs mandating that an MCP server query a CSV via Pandas and that the chatbot use/expose those query results in answers (CLM-002, DATA-001, ARCH-002, VC-NLP-003, SIR-002). This is a primary enabler of Business Capability5 (Tabular Data Query Service exposed via MCP Server) and supports Capability4 (Natural-Disaster Information Provisioning via Chat) by making CSV-derived query results available to the chatbot (VC-NLP-003).
>
> Business Capabilities Contribution: High
>
> *Preliminary Metrics*
>
> 1. MCP server call success rate (successful responses / total calls) for CSV queries via Pandas (**SUGGESTED**)
> 2. % of user questions requiring CSV data that are answered using MCP query results (end-to-end integration success) (**SUGGESTED**)
> 3. Error rate for CSV query execution/parsing in the MCP server (Pandas read/query failures per N requests) (**SUGGESTED**)
>
> Conflicts and Trade-offs: May trade off with performance: integrating chatbot responses with MCP server query calls can add latency., May trade off with maintainability: more integration contracts between chatbot, MCP server, and CSV querying can increase upkeep effort.

> 3:
>
> Quality Attribute: maintainability
>
> Business Goals Alignment Reasoning: No Business Goals were provided (business_goals is {}). Maintainability appears only as a secondary QA in multiple confirmed ASRs (e.g., CHAT-001, DATA-001, ARCH-001, ARCH-002, VC-NLP-001, VC-NLP-003, AIML-001, SIR-002), but without explicit goals its business alignment is indeterminable.
>
> Business Goals Alignment: Unknown
>
> Business Capabilities Contribution Reasoning: Maintainability is consistently identified as a secondary QA across the confirmed ASRs defining the composed chatbot and MCP CSV-query server (CHAT-001, DATA-001, ARCH-001, ARCH-002, VC-NLP-001, VC-NLP-003, AIML-001, SIR-002). This suggests it is important to sustaining Business Capabilities1–5 over time, but no explicit maintainability constraints/targets are provided, so contribution is rated Medium.
>
> Business Capabilities Contribution: Medium
>
> *Preliminary Metrics*
>
> 1. Unit test coverage percentage for the RAG module, Agent/MCP module integration, and MCP server CSV-query logic (**SUGGESTED**)
> 2. Change lead time for modifying CSV query logic (e.g., implement a new query filter) while keeping all existing tests passing (**SUGGESTED**)
> 3. Cyclomatic complexity (or similar static metric) for MCP server query handlers (**SUGGESTED**)
>
> Conflicts and Trade-offs: May trade off with performance: maintainability-driven abstractions/layers can add overhead in the MCP query/response path., May trade off with interoperability effort: keeping integration code simple and maintainable can constrain how many interoperability scenarios/formats are supported.

> 4:
>
> Quality Attribute: performance
>
> Business Goals Alignment Reasoning: No Business Goals were provided (business_goals is {}). Performance appears only as a secondary QA in DATA-001 and ARCH-002, and no performance targets are stated; therefore business alignment cannot be assessed.
>
> Business Goals Alignment: Unknown
>
> Business Capabilities Contribution Reasoning: Performance is mentioned only as a secondary QA related to the MCP server querying a CSV via Pandas to support chatbot responses (DATA-001, ARCH-002). It likely affects user experience for Capabilities1 and5, but the ASRs provide no explicit performance requirements, so contribution is rated Low.
>
> Business Capabilities Contribution: Low
>
> *Preliminary Metrics*
>
> 1. p95 end-to-end latency for chatbot answers that require an MCP CSV query (chat request -> response) (**SUGGESTED**)
> 2. p95 MCP server query latency for Pandas-based CSV retrieval (**SUGGESTED**)
> 3. Maximum sustained requests per second for MCP CSV queries before error rate increases (**SUGGESTED**)
>
> Conflicts and Trade-offs: May trade off with composability/interoperability: additional module boundaries and MCP calls can increase latency., May trade off with maintainability: performance optimizations can reduce code clarity and increase maintenance cost.

> 5:
>
> Quality Attribute: compatibility
>
> Business Goals Alignment Reasoning: No Business Goals were provided (business_goals is {}). Compatibility appears only as a secondary QA in VC-NLP-003 with no explicit constraints, so business alignment cannot be assessed.
>
> Business Goals Alignment: Unknown
>
> Business Capabilities Contribution Reasoning: Compatibility is cited only as a secondary QA in the confirmed ASR that integrates natural-disaster information queries via MCP CSV querying (VC-NLP-003). With no additional constraints, it provides only indirect support to Business Capability4 (Natural-Disaster Information Provisioning via Chat) and is rated Low.
>
> Business Capabilities Contribution: Low
>
> *Preliminary Metrics*
>
> 1. % of chatbot-MCP interactions that successfully parse and consume MCP query results (schema/format compatibility test pass rate) (**SUGGESTED**)
> 2. % of CSV datasets used that can be read and queried by the MCP server’s Pandas-based pipeline without code changes (dataset compatibility rate) (**SUGGESTED**)
>
> Conflicts and Trade-offs: May trade off with maintainability: adding compatibility handling (adapters/transformations) can increase code complexity., May trade off with performance: compatibility transformations can add processing overhead.

> 6:
>
> Quality Attribute: supportability
>
> Business Goals Alignment Reasoning: No Business Goals were provided (business_goals is {}). Supportability appears only as a secondary QA in AIML-001 and SIR-002, with no explicit operational/support targets; thus business alignment cannot be assessed.
>
> Business Goals Alignment: Unknown
>
> Business Capabilities Contribution Reasoning: Supportability is identified only as a secondary QA in confirmed ASRs that require the chatbot to return responses based on MCP CSV querying (AIML-001, SIR-002). This suggests some need to support/operate the solution, but since no support requirements are stated, contribution to capabilities is rated Low.
>
> Business Capabilities Contribution: Low
>
> *Preliminary Metrics*
>
> 1. Mean time to detect and identify failures in the MCP CSV-query path affecting chatbot answers (**SUGGESTED**)
> 2. % of MCP server query failures that produce actionable error messages for troubleshooting (**SUGGESTED**)
>
> Conflicts and Trade-offs: May trade off with performance: increased diagnostics/support hooks can add overhead in request handling., May trade off with maintainability: support mechanisms can increase the amount of code/configuration to maintain.


**Notes**

- Business Goals were not provided in the input (business_goals is {}), so Business Goal alignment is set to Unknown for all identified QAs.
- No confirmed ASR includes quantified non-functional targets (e.g., latency, throughput, coverage %, availability %); therefore all metrics are SUGGESTED (none are EXPLICIT).
- Several QAs (maintainability, performance, compatibility, supportability) appear only as Secondary Quality Attributes in the confirmed ASRs; ratings and metrics for these are necessarily conservative and should be validated with stakeholders if targets are later defined.

**Quality Attribute Degree Summaries**

> 1:
>
> Quality Attribute Name: compatibility
>
> Goal Alignment: High: 0
>
> Goal Alignment: Medium: 0
>
> Goal Alignment: Low: 0
>
> Goal Alignment: Unknown: 1
>
> Capability Contribution: High: 0
>
> Capability Contribution: Medium: 0
>
> Capability Contribution: Low: 1
>
> Capability Contribution: Unknown: 0

> 2:
>
> Quality Attribute Name: composability
>
> Goal Alignment: High: 0
>
> Goal Alignment: Medium: 0
>
> Goal Alignment: Low: 0
>
> Goal Alignment: Unknown: 1
>
> Capability Contribution: High: 1
>
> Capability Contribution: Medium: 0
>
> Capability Contribution: Low: 0
>
> Capability Contribution: Unknown: 0

> 3:
>
> Quality Attribute Name: interoperability
>
> Goal Alignment: High: 0
>
> Goal Alignment: Medium: 0
>
> Goal Alignment: Low: 0
>
> Goal Alignment: Unknown: 1
>
> Capability Contribution: High: 1
>
> Capability Contribution: Medium: 0
>
> Capability Contribution: Low: 0
>
> Capability Contribution: Unknown: 0

> 4:
>
> Quality Attribute Name: maintainability
>
> Goal Alignment: High: 0
>
> Goal Alignment: Medium: 0
>
> Goal Alignment: Low: 0
>
> Goal Alignment: Unknown: 1
>
> Capability Contribution: High: 0
>
> Capability Contribution: Medium: 1
>
> Capability Contribution: Low: 0
>
> Capability Contribution: Unknown: 0

> 5:
>
> Quality Attribute Name: performance
>
> Goal Alignment: High: 0
>
> Goal Alignment: Medium: 0
>
> Goal Alignment: Low: 0
>
> Goal Alignment: Unknown: 1
>
> Capability Contribution: High: 0
>
> Capability Contribution: Medium: 0
>
> Capability Contribution: Low: 1
>
> Capability Contribution: Unknown: 0

> 6:
>
> Quality Attribute Name: supportability
>
> Goal Alignment: High: 0
>
> Goal Alignment: Medium: 0
>
> Goal Alignment: Low: 0
>
> Goal Alignment: Unknown: 1
>
> Capability Contribution: High: 0
>
> Capability Contribution: Medium: 0
>
> Capability Contribution: Low: 1
>
> Capability Contribution: Unknown: 0




---

# Solution Strategy

**Title**: Solution Strategy: Modular-Monolith Chatbot with RAG + Agent/MCP and Pandas CSV-Query MCP Tool

**Primary Drivers**

Composability: compose chatbot from RAG + Agent/MCP modules and enable stubbing/swapping modules via clear seams
Interoperability & compatibility: reliable chatbot↔MCP integration with stable, versioned request/response parsing contracts
Maintainability: mandatory automated test coverage with fast feedback and low handler complexity in a small learning project
Performance: keep the CSV-query path fast enough and measurable (e.g., via timing fields) despite notebook-first scope
Supportability: actionable, structured errors and minimal observability to diagnose failures quickly

**Key Constraints**

- Small learning project implemented in a Python Jupyter notebook context
- Must add functionality to query natural-disaster information from a CSV via an MCP server implemented with Pandas
- Test coverage is mandatory

**Strategic Decisions**

> 1:
>
> Theme: Overall architecture & modularization (Modular Monolith + Ports-and-Adapters)
>
> Justification: To prioritize composability, maintainability, and interoperability without constraints requiring distributed services, the architecture needs explicit module seams that minimize integration points while keeping the MCP boundary clear and testable.
>
> Decision: Adopt a Modular Monolith organized into modules (RAG, Agent/MCP orchestration, CSV-query MCP tool) using explicit ports/interfaces and thin, stub-friendly adapters; keep MCP request/response parsing and Pandas CSV querying behind adapters to reduce coupling and enable contract testing.
>
> - ADR-0002
> - ADR-0003

> 2:
>
> Theme: MCP interoperability contract (versioned response envelope)
>
> Justification: Interoperability/compatibility risks concentrate at the chatbot↔MCP boundary; deterministic parsing and evolvability require a stable, testable schema that cleanly distinguishes success from error outcomes.
>
> Decision: Standardize a versioned MCP CSV-query response envelope (v1) with required fields (schema_version, ok, data/error, meta including request_id and timing_ms) and validate it via contract tests (required fields, mutual exclusivity, representative success/failure cases).
>
> - ADR-0004

> 3:
>
> Theme: CSV-query tool implementation (Pandas + defensive validation)
>
> Justification: The natural-disaster Q&A feature depends on querying CSV data; reliability and supportability require defensive parsing/validation and predictable outputs, while keeping integration points minimal and logic unit-testable.
>
> Decision: Implement the MCP CSV tool in-process using Pandas read_csv and DataFrame filtering/query with a restricted, documented set of supported filters; validate required columns/types/nullability before querying; always return results/errors via the centralized typed response envelope; add unit + contract tests and basic timing instrumentation around the CSV-query path.
>
> - ADR-0005

> 4:
>
> Theme: Testing strategy & quality gates
>
> Justification: Maintainability and composability depend on catching contract breakage and regressions early across module seams (RAG↔Agent/MCP wiring and chatbot↔MCP parsing), with mandatory coverage to enforce discipline in a notebook-driven codebase.
>
> Decision: Use pytest for unit tests (RAG logic, Agent/MCP orchestration, Pandas CSV parsing/validation/query logic) plus contract tests (module composition with stubs; chatbot↔MCP envelope parsing); enforce a CI coverage gate as a mandatory quality gate; include assertions for emitted timing instrumentation and structured, actionable errors.
>
> - ADR-0006

> 5:
>
> Theme: Minimal observability for performance & supportability (timing + actionable errors)
>
> Justification: To support performance and troubleshooting without heavy operational dependencies, the CSV-query path needs lightweight, testable instrumentation and consistent error reporting aligned with the parsing contract.
>
> Decision: Add lightweight lifecycle timing (read/validate/query/serialize) returned via the response envelope’s meta.timing_ms, and standardize stable error codes with user-safe messages plus optional debug details; ensure instrumentation and error schema are covered by automated tests to satisfy the coverage gate.
>
> - ADR-0007


Overall Approach: Implement a notebook-first chatbot as a modular monolith with Ports-and-Adapters: RAG, Agent/MCP orchestration, and an MCP server providing a Pandas-backed CSV-query tool for natural-disaster questions. Interoperability and compatibility are stabilized by a single versioned response envelope used for all MCP outcomes (success/error) and locked down with contract tests. Maintainability is enforced through pytest unit tests per module plus contract tests at composition and the chatbot↔MCP boundary, with a mandatory coverage gate. Performance and supportability are addressed with minimal, testable timing instrumentation and actionable structured errors on the MCP CSV-query path, avoiding distributed-system overhead while keeping adapters thin and swap/stub friendly.

**Trade-Offs**

| Trade-Off | Implication |
|----|----|
| Up-front ports/adapters + response envelope + contract tests vs Fastest possible initial iteration with minimal structure | Accepted to achieve composability, interoperability, and maintainability with mandatory test coverage and reduced boundary regressions. |
| In-process modular monolith vs Independent scaling and stronger fault isolation of separate services | No stated constraints require distributed deployment; simplicity and fewer integration points better match the learning/notebook scope. |
| Pandas in-memory CSV querying with defensive validation vs Better performance/memory behavior for large datasets or advanced query engines | Keeps integration minimal and testable while meeting the explicit Pandas-based MCP server requirement; can be revisited if CSV size grows. |
| Coverage gate as a mandatory quality control vs Lower test-writing effort and potentially faster short-term coding | Improves change confidence and maintainability across modules and seams, which are the highest-risk areas in a composed chatbot. |
| Including timing fields and structured error details in responses vs Absolute minimal response payloads and risk-free exposure of internals | Provides measurable performance and faster diagnosis; mitigated by keeping user-safe messages separate from optional debug details. |

**Notes**

- No explicit business goals were provided; strategy is driven by the listed quality attributes and the notebook learning scope.
- Constraints section was empty; key constraints were inferred from the provided special instructions (notebook-first, Pandas CSV MCP server, mandatory coverage).
- RAG module internals and Agent/MCP orchestration specifics are not defined here (only the seams/ports and testing expectations are).
- Operational details for the “CI coverage gate” in a notebook context (where tests run, how CI is set up) are not specified in the ADRs.
- Data size limits and performance targets beyond basic timing/p95 tracking are not defined; Pandas in-memory trade-offs may require later decisions.



---

# C4 Context Diagram

Title: System Context - RAG MCP Chatbot

Rationale: The system boundary is a notebook-first learning project that delivers a single chatbot experience composed from a RAG module and an Agent/MCP module, plus an in-process MCP server capability for querying natural-disaster data from a CSV via Pandas. The MCP server and CSV access are treated as internal parts of the same solution (modular monolith, ports-and-adapters) because the strategy explicitly avoids distributed deployment and focuses on contract-tested seams. No external deployed services/APIs are explicitly named in the provided artifacts, so the context includes only the end user interacting with the chatbot.

#### Target System

> Alias: ragMcpChatbot
>
> Name: RAG MCP Chatbot
>
> Description: Notebook chatbot combining RAG with Agent/MCP and CSV querying.
>
> Short Description: RAG+MCP chatbot
>
> Group: 
>

#### Actors Identified

| Alias | Name | Description | Short Description | Type |
|-------|-------|-------|-------|-------|
| chatUser | Chat User | Asks questions and receives answers in chat. | User | Person |

#### External Systems Identified


#### Relationships Identified

| Source Alias | Target Alias | Description | Short Description | Protocol | Protocol Technology |
|--------|--------|--------|--------|--------|--------|
| chatUser | ragMcpChatbot | Asks questions and receives answers from the chatbot. | Chats | InProcess |  |

#### Trade-offs

| Trade-Off | Implication |
|----|----|
| Model MCP server and CSV querying as internal capabilities vs Showing separate deployed MCP service boundary | The strategy specifies an in-process modular monolith and no distributed services. |
| Exclude any LLM, vector store, or document sources vs Richer ecosystem context and integrations | No external deployed systems are explicitly named in the provided artifacts. |

#### Structurizr DSL

```structurizr
workspace {
    !identifiers hierarchical
    model {
        properties {
            "structurizr.groupSeparator" "/"
        }

        archetypes {
            https = -> {
                technology "HTTPS"
            }

            hj = --https-> {
                technology "JSON/HTTPS"
            }

            sql = -> {
                technology "SQL/TCP"
            }

            async = -> {
                tag "Async"
            }

            grpc = -> {
                technology "gRPC"
            }

            amqp = --async-> {
                technology "AMQP"
            }
        }

        ragMcpChatbot = softwareSystem "RAG MCP Chatbot" "RAG+MCP chatbot"
        chatUser = person "Chat User" "User"
        chatUser -> ragMcpChatbot "Chats" "In-Process"
    }

    views {
        systemContext ragMcpChatbot "SystemContext_ragMcpChatbot" {
            include *
            autoLayout
        }

        theme default
        styles {
            element Existing {
                background #999999
                color #ffffff
            }

            element Container {
                background #438dd5
                color #ffffff
            }

            element Web {
                shape WebBrowser
            }

            element Mobile {
                shape MobileDeviceLandscape
            }

            element Datastore {
                shape Cylinder
            }

            element Component {
                background #85bbf0
                color #000000
            }

            element Broker {
                shape Pipe
            }

            element Failover {
                opacity 25
            }

            relationship Relationship {
                style dotted
                color #777777
            }

            relationship Async {
                style dashed
            }
        }
    }
}
```

Notes

Pandas, pytest, and Jupyter notebook are treated as internal implementation/tools, not external systems.
Natural-disaster data source is a CSV file accessed via Pandas; files/storage are considered internal per rules.
Mandatory automated test coverage, contract tests at the chatbot↔MCP envelope boundary, and timing/error metadata are non-functional requirements captured as internal concerns rather than external integrations.



---

# C4 Container Diagram

Title: Container Diagram - RAG MCP Chatbot

System Alias: ragMcpChatbot

#### Actors Identified

> Alias: chatUser
>
> Name: Chat User
>
> Description: Asks questions and receives answers in chat.
>
> Short Description: User
>
> Type: Person


#### External Systems Identified


#### Containers Identified

> Alias: notebookChatbot
>
> Name: Notebook Chatbot
>
> Description: Runs chat loop and orchestrates RAG plus MCP tool calls.
>
> Short Description: Chat runtime
>
> Rationale: Primary executable entry point in a Jupyter notebook, hosting modular RAG and Agent/MCP orchestration behind ports to enable stubbing and composition testing.
>
> Technology: Python Jupyter
>
> Archetype: Other
>
> Related ADR IDs
>
> ADR-0002
> ADR-0003
> ADR-0006

> Alias: mcpCsvServer
>
> Name: MCP CSV Server
>
> Description: Handles csv_query tool requests and returns a versioned response envelope.
>
> Short Description: CSV tool
>
> Rationale: Isolates MCP tool handling, response-envelope standardization, timing, and structured errors to stabilize the chatbot↔MCP boundary with contract tests.
>
> Technology: Python Pandas
>
> Archetype: Service
>
> Related ADR IDs
>
> ADR-0003
> ADR-0004
> ADR-0005
> ADR-0007

> Alias: disasterCsvFile
>
> Name: Disaster CSV
>
> Description: Stores natural-disaster data queried by the MCP CSV tool.
>
> Short Description: CSV data
>
> Rationale: Represents the persisted dataset accessed via Pandas read_csv and validated before query execution.
>
> Technology: CSV
>
> Archetype: FileSystem
>
> Related ADR IDs
>
> ADR-0005


#### Relationships Identified

> Source Alias: chatUser
>
> Target Alias: notebookChatbot
>
> Description: Chats to ask questions and receive answers.
>
> Short Description: Chats
>
> Protocol: InProcess
>
> Protocol Technology:

> Source Alias: notebookChatbot
>
> Target Alias: mcpCsvServer
>
> Description: Invokes csv_query tool to answer natural-disaster questions.
>
> Short Description: Invokes tool
>
> Protocol: InProcess
>
> Protocol Technology:

> Source Alias: mcpCsvServer
>
> Target Alias: disasterCsvFile
>
> Description: Reads and validates CSV data for query execution.
>
> Short Description: Reads data
>
> Protocol: FileIo
>
> Protocol Technology:


#### Trade Offs

> Trade-Off: In-process modular monolith with explicit ports/adapters vs Independent scaling and strong fault isolation
>
> Implication: No requirement for distributed deployment; fewer integration points fit notebook learning scope.

> Trade-Off: Versioned MCP response envelope with contract tests vs Fastest minimal-structure iteration
>
> Implication: Stabilizes the chatbot↔MCP seam and prevents parsing regressions with mandatory tests.

> Trade-Off: Pandas in-memory CSV querying with defensive validation vs Better performance/memory behavior for large datasets
>
> Implication: Meets the explicit Pandas MCP CSV requirement while staying simple and testable.

> Trade-Off: Coverage gate with pytest unit + contract tests vs Lower short-term test-writing effort
>
> Implication: Enforces maintainability and protects module seams in a notebook-driven codebase.

> Trade-Off: Timing fields and structured errors in MCP responses vs Minimal response payload and zero diagnostic exposure
>
> Implication: Improves supportability and performance tracking with lightweight, testable instrumentation.


#### Structurizr DSL

```structurizr
workspace {
    !identifiers hierarchical
    model {
        properties {
            "structurizr.groupSeparator" "/"
        }

        archetypes {
            https = -> {
                technology "HTTPS"
            }

            hj = --https-> {
                technology "JSON/HTTPS"
            }

            sql = -> {
                technology "SQL/TCP"
            }

            async = -> {
                tag "Async"
            }

            grpc = -> {
                technology "gRPC"
            }

            amqp = --async-> {
                technology "AMQP"
            }
        }

        ragMcpChatbot = softwareSystem "Rag Mcp Chatbot" "" {
            notebookChatbot = container "Notebook Chatbot" "Chat runtime" "Python Jupyter"
            mcpCsvServer = container "MCP CSV Server" "CSV tool" "Python Pandas" "Application"
            disasterCsvFile = container "Disaster CSV" "CSV data" "CSV" "Datastore"
        }
        chatUser = person "Chat User" "User"
        chatUser -> ragMcpChatbot.notebookChatbot "Chats" "In-Process"
        ragMcpChatbot.notebookChatbot -> ragMcpChatbot.mcpCsvServer "Invokes tool" "In-Process"
        ragMcpChatbot.mcpCsvServer -> ragMcpChatbot.disasterCsvFile "Reads data" "File I/O"
    }

    views {
        container ragMcpChatbot "Container_ragMcpChatbot" {
            include *
            autoLayout
        }

        theme default
        styles {
            element Existing {
                background #999999
                color #ffffff
            }

            element Container {
                background #438dd5
                color #ffffff
            }

            element Web {
                shape WebBrowser
            }

            element Mobile {
                shape MobileDeviceLandscape
            }

            element Datastore {
                shape Cylinder
            }

            element Component {
                background #85bbf0
                color #000000
            }

            element Broker {
                shape Pipe
            }

            element Failover {
                opacity 25
            }

            relationship Relationship {
                style dotted
                color #777777
            }

            relationship Async {
                style dashed
            }
        }
    }
}
```

Notes

RAG and Agent/MCP orchestration are treated as modules within the Notebook Chatbot container; their boundaries are enforced via ports and tested via stubs and contract tests.
All MCP CSV-query outcomes use the standardized response envelope v1 (schema_version, ok, data/error, meta with request_id and timing_ms) validated by contract tests.
CI and test runners are not modeled as containers; mandatory coverage gating is a quality requirement enforced by the test strategy.



---

# Technology Asset Names

**Categories**

| Name | Entities | Entities Count |
|-----|-----|-----|
| application_programming_interfaces | System.String[] | 2 |
| software_frameworks | System.String[] | 6 |
| communication_protocols | System.String[] | 1 |
| data_storage_solutions | System.String[] | 3 |
| software_development_kits | System.String[] | 0 |
| software_applications | System.String[] | 1 |
| software_platforms | System.String[] | 0 |
| desktop_applications | System.String[] | 0 |
| mobile_applications | System.String[] | 0 |
| web_applications | System.String[] | 0 |
| version_control_systems | System.String[] | 0 |
| security_tools | System.String[] | 0 |
| collaboration_tools | System.String[] | 1 |
| monitoring_tools | System.String[] | 0 |
| enterprise_software_systems | System.String[] | 0 |
| integration_middleware | System.String[] | 1 |
| messaging_systems | System.String[] | 0 |
| business_intelligence_tools | System.String[] | 0 |
| content_management_systems | System.String[] | 0 |
| analytics_platforms | System.String[] | 0 |
| customer_relationship_management_systems | System.String[] | 0 |
| operating_systems | System.String[] | 0 |
| database_management_systems | System.String[] | 1 |
| distributed_computing_frameworks | System.String[] | 0 |
| container_platforms | System.String[] | 0 |
| virtualization_platforms | System.String[] | 0 |
| enterprise_resource_planning_systems | System.String[] | 0 |
| cloud_software_services_saas | System.String[] | 2 |
| cloud_platform_services_paas | System.String[] | 3 |
| cloud_infrastructure_services_iaas | System.String[] | 1 |
| cloud_function_services_faas_serverless | System.String[] | 0 |
| other_entities | System.String[] | 29 |



---

# Tech Asset Properties

## langchain-cohere

Message: No relevant information found in the input documents for "langchain-cohere".

Expected documents




---

## RAGAS

Message: No relevant information found in the input documents for "RAGAS".

Expected documents




---

## GitHub

Message: No relevant information found in the input documents for "GitHub".

Expected documents




---

## Vertex AI Vector Search

Message: No relevant information found in the input documents for "Vertex AI Vector Search".

Expected documents




---

## PyPDFLoader

**Source References**


**Key Properties**


**Key Relationships**


**Insights**


**Additional General Insights and Hints for Further Analysis**


**Key Findings and Implications**

- Implication for diagram/view suitability: N/A for PyPDFLoader-specific C4/4+1/UML views, because the element cannot be placed with evidence into any container/component/class/interaction view from the provided materials.



---

## Document Processing with Gemini

Message: No relevant information found in the input documents for "Document Processing with Gemini".

Expected documents




---

## Document AI

Message: No relevant information found in the input documents for "Document AI".

Expected documents




---

## Gemini API

Message: No relevant information found in the input documents for "Gemini API".

Expected documents




---

## Cohere reranker

Message: No relevant information found in the input documents for "Cohere reranker".

Expected documents




---

## Hybrid Search

Message: No relevant information found in the input documents for "Hybrid Search".

Expected documents




---

## ChromaDB

Message: No relevant information found in the input documents for "ChromaDB".

Expected documents




---

## Gemini

Message: No relevant information found in the input documents for "Gemini".

Expected documents




---

## Vertex AI

Message: No relevant information found in the input documents for "Vertex AI".

Expected documents




---

## Chatbot

Message: No relevant information found in the input documents for "Chatbot".

Expected documents




---

## LangChain

Message: No relevant information found in the input documents for "LangChain".

Expected documents




---

## Google GenAI

Message: No relevant information found in the input documents for "Google GenAI".

Expected documents




---

## Plotly

Message: No relevant information found in the input documents for "Plotly".

Expected documents




---

## ConversationalRetrievalChain

Message: No relevant information found in the input documents for "ConversationalRetrievalChain".

Expected documents




---

## Python

Message: No relevant information found in the input documents for "Python".

Expected documents




---

## RAG

Message: No relevant information found in the input documents for "RAG".

Expected documents




---

## Jupyter Notebook

Message: No relevant information found in the input documents for "Jupyter Notebook".

Expected documents




---

## Agents

Message: No relevant information found in the input documents for "Agents".

Expected documents




---

## HTML

Message: No relevant information found in the input documents for "HTML".

Expected documents




---

## Semantic Search

Message: No relevant information found in the input documents for "Semantic Search".

Expected documents




---

## Keyword Search

Message: No relevant information found in the input documents for "Keyword Search".

Expected documents




---

## BM25

Message: No relevant information found in the input documents for "BM25".

Expected documents




---

## LLMChain

Message: No relevant information found in the input documents for "LLMChain".

Expected documents




---

## Multimodal RAG

Message: No relevant information found in the input documents for "Multimodal RAG".

Expected documents




---

## Google Colab

Message: No relevant information found in the input documents for "Google Colab".

Expected documents




---

## PromptTemplate

Message: No relevant information found in the input documents for "PromptTemplate".

Expected documents




---

## LLM

Message: No relevant information found in the input documents for "LLM".

Expected documents




---

## CSV

Message: No relevant information found in the input documents for "CSV".

Expected documents




---

## PDF

Message: No relevant information found in the input documents for "PDF".

Expected documents




---

## MCP

Message: No relevant information found in the input documents for "MCP".

Expected documents




---

## Azure

Message: No relevant information found in the input documents for "Azure".

Expected documents




---

## cosine similarity

Message: No relevant information found in the input documents for "cosine similarity".

Expected documents




---

## Vector Search

Message: No relevant information found in the input documents for "Vector Search".

Expected documents




---

## HyDE

Message: No relevant information found in the input documents for "HyDE".

Expected documents




---

## MCP server

Message: No relevant information found in the input documents for "MCP server".

Expected documents




---

## Pandas

Message: No relevant information found in the input documents for "Pandas".

Expected documents




---

## Kaggle

Message: No relevant information found in the input documents for "Kaggle".

Expected documents




---

## ReAct

Message: No relevant information found in the input documents for "ReAct".

Expected documents




---

## RecursiveCharacterTextSplitter

Message: No relevant information found in the input documents for "RecursiveCharacterTextSplitter".

Expected documents




---

## cross-encoder

Message: No relevant information found in the input documents for "cross-encoder".

Expected documents




---

## TOGAF

Message: No relevant information found in the input documents for "TOGAF".

Expected documents




---

## Gemini2.0

Message: No relevant information found in the input documents for "Gemini2.0".

Expected documents




---

## python-dotenv

Message: No relevant information found in the input documents for "python-dotenv".

Expected documents




---

## Healthcare NL API

Message: No relevant information found in the input documents for "Healthcare NL API".

Expected documents




---

## HuggingFaceEmbeddings

Message: No relevant information found in the input documents for "HuggingFaceEmbeddings".

Expected documents




---

## Chat with your data solution accelerator

Message: No relevant information found in the input documents for "Chat with your data solution accelerator".

Expected documents




---

## MMR

Message: No relevant information found in the input documents for "MMR".

Expected documents




---

# Developer Recommendations

#### Process Recommendations

> 1:
>
> Id: PROC-001
>
> Category: Definition of Done Gate
>
> Reference
>
>> Source Location: input_data.slot_context.candidate_tactics
>>
>> Source Quote: Mandatory automated tests with coverage gating for RAG module, Agent/MCP integration, and Pandas CSV-query logic; keep handler complexity low
>>
>
> Rationale: A mandatory quality gate enforces maintainability and reduces integration regressions across the composed modules.
>
> Recommendation: Make merge/acceptance conditional on (a) automated unit tests for each module and (b) a CI-enforced coverage gate for the RAG module, Agent/MCP orchestration, and CSV-query MCP logic; fail the change if the gate does not pass.
>
> Priority: High
>
> Related QAs
>
> maintainability
> composability
> interoperability

> 2:
>
> Id: PROC-002
>
> Category: Contract Testing Process
>
> Reference
>
>> Source Location: input_data.slot_context.candidate_tactics
>>
>> Source Quote: Contract tests for (a) module composition with stubs and (b) chatbot↔MCP result parsing (schema/format compatibility)
>>
>
> Rationale: Contract tests stabilize ports/adapters, improving composability and compatibility at the chatbot↔MCP boundary.
>
> Recommendation: Add contract tests as a required pipeline stage that verify (1) module composition works with stubbed RAG and/or stubbed Agent/MCP modules, and (2) chatbot↔MCP result parsing stays schema/format compatible for representative success and failure cases.
>
> Priority: High
>
> Related QAs
>
> composability
> compatibility
> interoperability

> 3:
>
> Id: PROC-003
>
> Category: Operational Readiness Checks
>
> Reference
>
>> Source Location: input_data.slot_context.candidate_tactics
>>
>> Source Quote: Basic timing instrumentation around MCP CSV-query path to track p95 latency; structured error messages for troubleshooting
>>
>
> Rationale: Testable instrumentation and structured errors provide performance baselines and faster diagnosis, supporting supportability without adding heavy ops overhead.
>
> Recommendation: Require tests that assert the CSV-query MCP path emits timing fields and returns structured, actionable errors; treat missing timing/error structure as a failing check.
>
> Priority: Medium
>
> Related QAs
>
> performance
> supportability
> maintainability


#### Tooling Recommendations

> 1:
>
> Id: TOOL-001
>
> Category: Unit Testing Framework
>
> Reference
>
>> Source Location: slot_context.slot_notes
>>
>> Source Quote: Testing strategy and coverage gate for RAG module, Agent/MCP integration, and MCP CSV-query logic (unit + contract tests)
>>
>
> Rationale: Automated unit and contract tests are the primary mechanism to achieve mandatory coverage and protect module seams in a modular monolith.
>
> Recommendation: Use a unit-testing toolchain that supports both unit tests and contract tests, and run it in CI for every change affecting RAG, Agent/MCP orchestration, or the CSV-query MCP server.
>
> Priority: High
>
> Related QAs
>
> maintainability
> composability
> interoperability

> 2:
>
> Id: TOOL-002
>
> Category: Code Coverage Measurement Tool
>
> Reference
>
>> Source Location: slot_context.candidate_tactics
>>
>> Source Quote: Mandatory automated tests with coverage gating for RAG module, Agent/MCP integration, and Pandas CSV-query logic; keep handler complexity low
>>
>
> Rationale: A coverage gate provides an objective maintainability control aligned with the mandatory coverage requirement.
>
> Recommendation: Integrate a coverage measurement tool into CI to enforce a minimum coverage threshold for core modules and to report coverage deltas per change.
>
> Priority: High
>
> Related QAs
>
> maintainability

> 3:
>
> Id: TOOL-003
>
> Category: Contract Test Harness
>
> Reference
>
>> Source Location: slot_context.candidate_tactics
>>
>> Source Quote: Contract tests for (a) module composition with stubs and (b) chatbot↔MCP result parsing (schema/format compatibility)
>>
>
> Rationale: A dedicated contract-test harness reduces regressions at integration points and improves interoperability/compatibility metrics.
>
> Recommendation: Adopt tooling support for contract tests that can execute stubbed module compositions and validate chatbot↔MCP response schema/format across success and error scenarios.
>
> Priority: High
>
> Related QAs
>
> compatibility
> interoperability
> composability

> 4:
>
> Id: TOOL-004
>
> Category: Tabular Data Processing Library
>
> Reference
>
>> Source Location: input_data.slot_context
>>
>> Source Quote: Pandas CSV read/query validation and defensive parsing to reduce CSV query execution/parsing failures
>>
>
> Rationale: A dataframe-style CSV tool supports fast iteration while enabling defensive parsing/validation and testability for the MCP CSV-query path.
>
> Recommendation: Use the selected tabular data processing library’s CSV read + dataframe filtering APIs behind the CSV-query port, with explicit column selection and validation as part of the implementation.
>
> Priority: High
>
> Related QAs
>
> interoperability
> maintainability
> performance


#### Coding Best Practices

> 1:
>
> Id: CODE-001
>
> Category: Response Schema Standard
>
> Reference
>
>> Source Location: slot_context.candidate_tactics[2]
>>
>> Source Quote: Centralized, typed response envelope for MCP CSV-query results and errors to reduce parse failures and improve interoperability
>>
>
> Rationale: A stable, typed success/error envelope minimizes parsing ambiguity and improves interoperability/compatibility with contract-test coverage.
>
> Recommendation: Implement a centralized, versioned response envelope for the CSV-query MCP tool that cleanly separates success vs error and is the only allowed payload shape across the chatbot↔MCP boundary.
>
> Priority: High
>
> Related QAs
>
> interoperability
> compatibility
> supportability
> maintainability

> 2:
>
> Id: CODE-002
>
> Category: Defensive Input Parsing and Validation
>
> Reference
>
>> Source Location: input_data.slot_context
>>
>> Source Quote: Pandas CSV read/query validation and defensive parsing to reduce CSV query execution/parsing failures
>>
>
> Rationale: Defensive parsing/validation reduces CSV query failures, improves dataset compatibility, and supports maintainability via predictable behavior under bad inputs.
>
> Recommendation: Before executing any CSV filters, validate required columns and basic types/nullable constraints; if validation fails, return a structured error in the standard envelope (do not raise raw exceptions across the port).
>
> Priority: High
>
> Related QAs
>
> interoperability
> compatibility
> supportability
> maintainability

> 3:
>
> Id: CODE-003
>
> Category: Safe Query Construction
>
> Reference
>
>> Source Location: slot_context.slot_notes
>>
>> Source Quote: Implement the MCP server’s CSV tool using Pandas as follows: (1) load CSV via pandas.read_csv with explicit column selection and defensive parsing; ... (3) execute queries via DataFrame boolean indexing (and/or DataFrame.query when safe) with a restricted, documented set of supported filters;
>>
>
> Rationale: Restricting supported filters and preferring safe boolean indexing reduces query parsing errors and keeps handlers simpler and more testable.
>
> Recommendation: Limit CSV-query capabilities to a documented, restricted set of filters and implement filtering via safe dataframe boolean indexing; treat unsupported filters as a structured parse/validation error in the standard envelope.
>
> Priority: High
>
> Related QAs
>
> maintainability
> interoperability
> supportability

> 4:
>
> Id: CODE-004
>
> Category: Instrumentation and Structured Errors
>
> Reference
>
>> Source Location: input_data.slot_context.candidate_tactics
>>
>> Source Quote: Basic timing instrumentation around MCP CSV-query path to track p95 latency; structured error messages for troubleshooting
>>
>
> Rationale: Lightweight timing plus stable error codes enables performance baselining and faster troubleshooting while staying suitable for a small monolith/notebook context.
>
> Recommendation: Emit lightweight timing for the CSV-query MCP request lifecycle and return structured, actionable error objects (stable error codes + user-safe message + optional debug details) within the standard response envelope.
>
> Priority: Medium
>
> Related QAs
>
> performance
> supportability
> interoperability

> 5:
>
> Id: CODE-005
>
> Category: Thin Adapter Implementation
>
> Reference
>
>> Source Location: input_data/slot_context
>>
>> Source Quote: Define explicit ports (interfaces) for RAG, Agent/MCP orchestration, and CSV-query tool; keep adapters thin to minimize integration points
>>
>
> Rationale: Thin adapters reduce integration complexity and make swapping/stubbing modules easier, improving composability and maintainability.
>
> Recommendation: Keep adapters (MCP request/response parsing, CSV read/query integration) as thin translation layers; place business logic behind ports so stubs can replace implementations in contract tests.
>
> Priority: Medium
>
> Related QAs
>
> composability
> maintainability
> compatibility




---

# DevOps Recommendations

#### Cicd Recommendations

> 1:
>
> Id: CICD-001
>
> Category: CI/CD Platform
>
> Reference
>
>> Source Location: slot_context.candidate_tactics
>>
>> Source Quote: Mandatory automated tests with coverage gating for RAG module, Agent/MCP integration, and Pandas CSV-query logic; keep handler complexity low
>>
>
> Rationale: The architecture relies on stable composition across RAG, Agent/MCP orchestration, and the CSV-query MCP tool, and it has a mandatory coverage requirement; enforcing automated tests and coverage gating in CI directly supports maintainability and reduces integration regressions at module seams.
>
> Recommendation: Implement pipeline-as-code with a required CI workflow on every change and before merge: run automated unit tests for each module, run contract tests for stubbed-module composition and chatbot↔MCP parsing, and enforce a minimum test-coverage threshold gate (fail the pipeline if unmet).
>
> Priority: High
>
> Related QAs
>
> maintainability
> composability
> interoperability
> compatibility


#### Iac Recommendations


#### Quality Gate Recommendations

> 1:
>
> Id: QG-001
>
> Category: Code Quality Tool
>
> Reference
>
>> Source Location: slot_context.candidate_tactics
>>
>> Source Quote: Mandatory automated tests with coverage gating for RAG module, Agent/MCP integration, and Pandas CSV-query logic; keep handler complexity low
>>
>
> Rationale: A coverage gate is explicitly required, and low handler complexity is a stated maintainability driver; making these non-optional gates prevents fragile changes to the MCP handler and core logic from merging undetected.
>
> Recommendation: Add mandatory quality gates that block merge/release when (1) automated test coverage is below the enforced threshold and (2) handler complexity exceeds the agreed static threshold for MCP query handlers; publish gate results as CI artifacts for review.
>
> Priority: High
>
> Related QAs
>
> maintainability
> supportability

> 2:
>
> Id: QG-002
>
> Category: Testing Framework
>
> Reference
>
>> Source Location: slot_context.candidate_tactics
>>
>> Source Quote: Contract tests for (a) module composition with stubs and (b) chatbot↔MCP result parsing (schema/format compatibility)
>>
>
> Rationale: Interoperability and compatibility depend on stable module composition and a parseable chatbot↔MCP boundary; contract tests are the explicit mechanism to lock the contract and prevent schema/format regressions.
>
> Recommendation: Embed contract-test gates that must pass before merge: (a) composition tests with stubbed ports for RAG and Agent/MCP, and (b) schema/format compatibility tests for chatbot↔MCP results (including representative success and failure cases) using the standardized response envelope.
>
> Priority: High
>
> Related QAs
>
> composability
> interoperability
> compatibility
> maintainability


#### Monitoring Recommendations

> 1:
>
> Id: MON-001
>
> Category: Observability Platform
>
> Reference
>
>> Source Location: input_data.slot_context.candidate_tactics
>>
>> Source Quote: Basic timing instrumentation around MCP CSV-query path to track p95 latency; structured error messages for troubleshooting
>>
>
> Rationale: Performance and supportability are driven by the MCP CSV-query path; timing instrumentation and structured errors provide measurable latency/error baselines and faster diagnosis without adding heavy operational overhead.
>
> Recommendation: Implement lightweight, testable observability for the MCP CSV-query lifecycle: emit end-to-end and query-segment timing metrics plus structured error codes/messages (correlated by a request_id), and add automated tests that assert timing and error fields are produced for both success and failure responses.
>
> Priority: High
>
> Related QAs
>
> performance
> supportability
> maintainability
> interoperability




---

# Quality Assurance Recommendations

#### Process Recommendations

> 1:
>
> Id: PROC-001
>
> Category: Test Strategy
>
> Reference
>
>> Source Location: adr_per_slot_decisions.ADR-0006.references[0] (slot_context.slot_notes)
>>
>> Source Quote: Testing strategy and coverage gate for RAG module, Agent/MCP integration, and MCP CSV-query logic (unit + contract tests)
>>
>
> Rationale: The modular-monolith with explicit ports needs fast feedback that verifies module seams (composition + chatbot↔MCP) and enforces the mandatory coverage requirement across the three core modules.
>
> Recommendation: Adopt a single automated test strategy covering (1) unit tests per module (RAG, orchestration, CSV-query tool) and (2) contract tests at ports (module-stub composition + chatbot↔MCP parsing), reviewed each iteration with traceability to the listed QA metrics.
>
> Priority: High
>
> Related QAs
>
> Maintainability
> Composability
> Interoperability
> Compatibility


#### Tooling Recommendations

> 1:
>
> Id: TOOL-001
>
> Category: Coverage Measurement Tool
>
> Reference
>
>> Source Location: adr_per_slot_decisions.ADR-0006.decision_description
>>
>> Source Quote: Use an automated testing methodology based on pytest with: (1) unit tests for RAG logic, Agent/MCP orchestration logic, and Pandas CSV-query logic (including defensive parsing/validation); (2) contract tests covering (a) module composition with stubs and (b) chatbot↔MCP result parsing using a centralized typed response envelope; (3) a CI coverage gate (minimum coverage threshold enforced) as a mandatory quality gate; (4) basic tests that assert timing instrumentation is emitted around the MCP CSV-query path and that error responses are structured/actionable.
>>
>
> Rationale: A CI-enforced coverage gate and automated execution are explicitly required to keep the notebook-scale codebase maintainable while evolving the CSV-query tool and integration contracts.
>
> Recommendation: Use a coverage measurement tool integrated into CI to enforce the mandatory coverage gate for unit + contract tests across core modules (RAG, orchestration, CSV-query) and to publish coverage reports per change.
>
> Priority: High
>
> Related QAs
>
> Maintainability

> 2:
>
> Id: TOOL-002
>
> Category: Contract Testing Tool
>
> Reference
>
>> Source Location: adr_per_slot_decisions.ADR-0003.references[3] (slot_context.candidate_tactics)
>>
>> Source Quote: Contract tests for (a) module composition with stubs and (b) chatbot↔MCP result parsing (schema/format compatibility)
>>
>
> Rationale: Contract testing at ports is the primary mechanism called out to reduce integration fragility and ensure the chatbot can reliably consume MCP results over time.
>
> Recommendation: Adopt a contract testing tool to validate (1) module composition with stubs and (2) schema/format compatibility for chatbot↔MCP result parsing, executed in CI on every change affecting ports or adapters.
>
> Priority: High
>
> Related QAs
>
> Composability
> Interoperability
> Compatibility


#### Testing Best Practices

> 1:
>
> Id: TEST-001
>
> Category: Contract Testing Practice
>
> Reference
>
>> Source Location: adr_per_slot_decisions.ADR-0004.decision_description (Testing standardization)
>>
>> Source Quote: Add contract tests validating: (1) ok/data/error mutual exclusivity, (2) required fields, (3) schema_version, (4) representative success and failure cases (CSV read error, invalid question, empty result).
>>
>
> Rationale: A versioned response envelope and explicit contract tests minimize parse ambiguity at the chatbot↔MCP boundary, improving interoperability/compatibility and keeping failures diagnosable.
>
> Recommendation: Implement contract tests for the versioned response envelope covering required fields, success/error mutual exclusivity, schema versioning, and representative failure modes (read error, invalid question, empty result).
>
> Priority: High
>
> Related QAs
>
> Interoperability
> Compatibility
> Supportability

> 2:
>
> Id: TEST-002
>
> Category: Data Validation Testing Practice
>
> Reference
>
>> Source Location: adr_per_slot_decisions.ADR-0005.references[2] (slot_context.candidate_tactics)
>>
>> Source Quote: Pandas CSV read/query validation and defensive parsing to reduce CSV query execution/parsing failures
>>
>
> Rationale: Defensive parsing/validation is explicitly chosen to reduce CSV query failures and protect interoperability and dataset compatibility as the CSV content varies.
>
> Recommendation: Create focused unit tests for CSV parsing/validation (required columns, basic types/nullability) and for supported query filters, including negative cases that must return structured errors rather than exceptions.
>
> Priority: High
>
> Related QAs
>
> Interoperability
> Compatibility
> Maintainability

> 3:
>
> Id: TEST-003
>
> Category: Observability Testing Practice
>
> Reference
>
>> Source Location: adr_per_slot_decisions.ADR-0007.references[1] (slot_context.candidate_tactics)
>>
>> Source Quote: Basic timing instrumentation around MCP CSV-query path to track p95 latency; structured error messages for troubleshooting
>>
>
> Rationale: Performance and supportability goals depend on emitting timing and structured errors in a way that is stable and testable, so regressions are detected early in a small learning project.
>
> Recommendation: Add automated tests that assert timing fields are emitted for CSV-query calls and that error responses include stable error codes and user-safe messages (with optional debug details) to support troubleshooting.
>
> Priority: Medium
>
> Related QAs
>
> Performance
> Supportability
> Maintainability


#### Quality Gate Recommendations

> 1:
>
> Id: QG-001
>
> Category: Coverage Threshold
>
> Reference
>
>> Source Location: adr_per_slot_decisions.ADR-0006.traceability[0].qa_metrics
>>
>> Source Quote: - [SUGGESTED] Line coverage >=85% on core modules (RAG, Agent/MCP orchestration, CSV-query)
>>
>
> Rationale: Mandatory test coverage is a stated requirement; setting an explicit coverage threshold makes the requirement enforceable and supports maintainability as modules evolve.
>
> Recommendation: Quality gate: block merge/release unless automated test execution passes and line coverage is >=85% on the core modules (RAG, orchestration, CSV-query).
>
> Priority: High
>
> Related QAs
>
> Maintainability

> 2:
>
> Id: QG-002
>
> Category: Release Readiness Gate
>
> Reference
>
>> Source Location: adr_per_slot_decisions.ADR-0003.references[3] (slot_context.candidate_tactics)
>>
>> Source Quote: Contract tests for (a) module composition with stubs and (b) chatbot↔MCP result parsing (schema/format compatibility)
>>
>
> Rationale: The architecture’s main risk is contract drift between composed modules and the MCP boundary; a hard gate prevents shipping incompatible adapters/envelopes.
>
> Recommendation: Quality gate: require100% pass of (1) module-stub composition contract tests and (2) chatbot↔MCP schema/format compatibility tests (including success and failure envelope cases) before release.
>
> Priority: High
>
> Related QAs
>
> Composability
> Interoperability
> Compatibility

> 3:
>
> Id: QG-003
>
> Category: Quality Gate
>
> Reference
>
>> Source Location: adr_per_slot_decisions.ADR-0006.traceability[1].qa_metrics
>>
>> Source Quote: - [SUGGESTED] Actionable error-message rate >=95% for CSV-query failures
>>
>
> Rationale: Supportability is explicitly targeted via structured, actionable errors; gating on error-schema completeness keeps failures diagnosable as the CSV-query tool evolves.
>
> Recommendation: Quality gate: in automated tests, verify CSV-query failure scenarios emit structured errors with stable error codes and user-safe messages, and meet the suggested actionable-error rate of >=95% across the covered failure cases.
>
> Priority: Medium
>
> Related QAs
>
> Supportability
> Interoperability
> Maintainability




---

# Maintenance Recommendations

#### Process Recommendations

> 1:
>
> Id: PROC-001
>
> Category: Maintenance Testing Governance Process
>
> Reference
>
>> Source Location: adr_per_slot_decisions: ADR-0006 decision_description
>>
>> Source Quote: Use an automated testing methodology based on pytest with: (1) unit tests for RAG logic, Agent/MCP orchestration logic, and Pandas CSV-query logic (including defensive parsing/validation); (2) contract tests covering (a) module composition with stubs and (b) chatbot↔MCP result parsing using a centralized typed response envelope; (3) a CI coverage gate (minimum coverage threshold enforced) as a mandatory quality gate;
>>
>
> Rationale: Mandatory automated tests plus a coverage gate keep the modular monolith’s modules maintainable and prevent regressions at the key integration seams.
>
> Recommendation: Define a maintenance workflow where every change must add/adjust unit tests for each module and contract tests for module composition and chatbot↔tool parsing, and must pass the automated coverage gate before merge.
>
> Priority: High
>
> Related QAs
>
> maintainability
> composability
> interoperability
> compatibility

> 2:
>
> Id: PROC-002
>
> Category: Interface Contract Change Management Process
>
> Reference
>
>> Source Location: input_data.slot_context.candidate_tactics
>>
>> Source Quote: Contract tests for (a) module composition with stubs and (b) chatbot↔MCP result parsing (schema/format compatibility)
>>
>
> Rationale: Treating tool schemas and port interfaces as contracts reduces breakage when evolving the CSV-query tool or swapping/stubbing modules.
>
> Recommendation: Require an explicit contract-change step for any port/schema update: update the typed response envelope/schema version as needed, update contract tests for success+error cases, and verify stub-based composition tests still pass.
>
> Priority: High
>
> Related QAs
>
> compatibility
> interoperability
> composability

> 3:
>
> Id: PROC-003
>
> Category: Complexity Management Process
>
> Reference
>
>> Source Location: input_data.slot_context.candidate_tactics
>>
>> Source Quote: Mandatory automated tests with coverage gating for RAG module, Agent/MCP integration, and Pandas CSV-query logic; keep handler complexity low
>>
>
> Rationale: Keeping handler complexity low reduces maintenance cost and helps sustain required test coverage as features (filters/queries) grow.
>
> Recommendation: Add a lightweight complexity review to maintenance changes for query handlers/adapters; if complexity rises, schedule refactoring within the same iteration and require tests to remain green before accepting the change.
>
> Priority: Medium
>
> Related QAs
>
> maintainability
> supportability


#### Tooling Recommendations

> 1:
>
> Id: TOOL-001
>
> Category: Continuous Integration System
>
> Reference
>
>> Source Location: adr_per_slot_decisions: ADR-0006 decision_description
>>
>> Source Quote: a CI coverage gate (minimum coverage threshold enforced) as a mandatory quality gate;
>>
>
> Rationale: An automated pipeline is needed to enforce the required coverage gate and keep maintenance changes consistently validated.
>
> Recommendation: Use a continuous integration system that runs all unit+contract tests on each change and fails the build when the coverage gate is not met.
>
> Priority: High
>
> Related QAs
>
> maintainability
> composability
> interoperability

> 2:
>
> Id: TOOL-002
>
> Category: Coverage Reporting Tool
>
> Reference
>
>> Source Location: slot_context.drivers
>>
>> Source Quote: Mandatory test coverage requirement
>>
>
> Rationale: Coverage reporting makes the mandatory coverage requirement measurable and enforceable during maintenance.
>
> Recommendation: Adopt a coverage reporting tool integrated into the test run to produce per-module coverage reports for the core modules and to support an enforceable minimum threshold.
>
> Priority: High
>
> Related QAs
>
> maintainability

> 3:
>
> Id: TOOL-003
>
> Category: Monitoring Tool
>
> Reference
>
>> Source Location: input_data.slot_context.candidate_tactics
>>
>> Source Quote: Basic timing instrumentation around MCP CSV-query path to track p95 latency; structured error messages for troubleshooting
>>
>
> Rationale: Latency and failure visibility are required to maintain responsiveness and quickly diagnose CSV-query path issues.
>
> Recommendation: Use a monitoring tool (or lightweight metrics capture) to aggregate timing emitted by the MCP CSV-query path (e.g., compute p95 from captured timings) and to track error-code rates over time.
>
> Priority: Medium
>
> Related QAs
>
> performance
> supportability


#### Maintenance Best Practices

> 1:
>
> Id: MAINT-001
>
> Category: Response Schema Standardization Practice
>
> Reference
>
>> Source Location: adr_per_slot_decisions: ADR-0004 decision_description
>>
>> Source Quote: Adopt a standard, versioned MCP CSV-query response envelope used for every tool call outcome.
>>
>
> Rationale: A single, versioned success/error envelope prevents parsing ambiguity and reduces maintenance risk when the tool evolves.
>
> Recommendation: Implement and maintain a versioned response envelope for all CSV-query tool outcomes, and evolve it only via backward-compatible changes (or explicit version bumps) validated by contract tests.
>
> Priority: High
>
> Related QAs
>
> compatibility
> interoperability
> supportability
> maintainability

> 2:
>
> Id: MAINT-002
>
> Category: Input Validation Practice
>
> Reference
>
>> Source Location: adr_per_slot_decisions: ADR-0005 decision_description
>>
>> Source Quote: validate required columns and basic types/nullable constraints before executing filters;
>>
>
> Rationale: Defensive validation reduces runtime query/parsing failures and improves long-term robustness as datasets and filters change.
>
> Recommendation: Before running any CSV filter, validate required columns and basic types/nullability, and restrict execution to a documented set of supported filters validated by unit tests.
>
> Priority: High
>
> Related QAs
>
> interoperability
> compatibility
> maintainability
> supportability

> 3:
>
> Id: MAINT-003
>
> Category: Instrumentation and Error Hygiene Practice
>
> Reference
>
>> Source Location: adr_per_slot_decisions: ADR-0006 decision_description
>>
>> Source Quote: basic tests that assert timing instrumentation is emitted around the MCP CSV-query path and that error responses are structured/actionable.
>>
>
> Rationale: Consistent timing fields and actionable error shapes reduce mean time to diagnose issues and enable performance regression detection.
>
> Recommendation: Keep timing and structured error codes/messages as part of the maintained contract; whenever modifying the CSV-query path, update tests to ensure timings are still emitted and errors remain structured and user-safe.
>
> Priority: Medium
>
> Related QAs
>
> supportability
> performance
> interoperability

> 4:
>
> Id: MAINT-004
>
> Category: Refactoring Practice
>
> Reference
>
>> Source Location: adr_per_slot_decisions: ADR-0003 decision_description
>>
>> Source Quote: keep adapters thin and stub-friendly;
>>
>
> Rationale: Thin adapters and stable ports make module swapping/stubbing easier and keep maintenance changes localized.
>
> Recommendation: Refactor new functionality to stay behind existing ports where possible; keep adapters focused on translation/IO and push business logic into testable core modules behind ports.
>
> Priority: Medium
>
> Related QAs
>
> composability
> maintainability


#### Quality Gate Recommendations

> 1:
>
> Id: QG-001
>
> Category: Regression Threshold
>
> Reference
>
>> Source Location: adr_per_slot_decisions: ADR-0006 decision_description
>>
>> Source Quote: a CI coverage gate (minimum coverage threshold enforced) as a mandatory quality gate;
>>
>
> Rationale: A clear automated exit criterion prevents low-test changes from accumulating and degrading maintainability.
>
> Recommendation: Exit criterion for maintenance changes: the automated pipeline passes and the configured minimum coverage threshold is met for the core modules; otherwise the change is not releasable.
>
> Priority: High
>
> Related QAs
>
> maintainability

> 2:
>
> Id: QG-002
>
> Category: Schema Compatibility Gate
>
> Reference
>
>> Source Location: adr_per_slot_decisions: ADR-0004 decision_description
>>
>> Source Quote: Add contract tests validating: (1) ok/data/error mutual exclusivity, (2) required fields, (3) schema_version, (4) representative success and failure cases (CSV read error, invalid question, empty result).
>>
>
> Rationale: Schema compatibility tests prevent chatbot↔tool parsing regressions during maintenance changes.
>
> Recommendation: Exit criterion for any tool/schema change: contract tests must prove required envelope fields, ok/data/error exclusivity, and representative success+failure responses remain valid for the current schema_version.
>
> Priority: High
>
> Related QAs
>
> compatibility
> interoperability
> supportability

> 3:
>
> Id: QG-003
>
> Category: Composition Contract Gate
>
> Reference
>
>> Source Location: input_data.slot_context.candidate_tactics
>>
>> Source Quote: Contract tests for (a) module composition with stubs and (b) chatbot↔MCP result parsing (schema/format compatibility)
>>
>
> Rationale: Stub-based composition tests ensure modules remain swappable and integration seams remain stable.
>
> Recommendation: Exit criterion for changes affecting ports/adapters: composition contract tests using stubs must pass for both (a) module composition and (b) chatbot parsing of tool results.
>
> Priority: High
>
> Related QAs
>
> composability
> interoperability

> 4:
>
> Id: QG-004
>
> Category: Operational Readiness Gate
>
> Reference
>
>> Source Location: input_data.slot_context.candidate_tactics
>>
>> Source Quote: Basic timing instrumentation around MCP CSV-query path to track p95 latency; structured error messages for troubleshooting
>>
>
> Rationale: Maintained instrumentation and structured errors are the minimum operational readiness baseline for diagnosing and tracking performance regressions.
>
> Recommendation: Exit criterion for releases that touch the CSV-query path: automated tests confirm timing fields are emitted for requests and that failures return structured error codes/messages suitable for troubleshooting.
>
> Priority: Medium
>
> Related QAs
>
> performance
> supportability




---

# Security Recommendations

Note: 

#### Security Processes By Phase

> 1:
>
> Id: PROC-001
>
> Phase: Design
>
> Reference
>
>> Source Location: input_data/slot_context
>>
>> Source Quote: Define explicit ports (interfaces) for RAG, Agent/MCP orchestration, and CSV-query tool; keep adapters thin to minimize integration points
>>
>
> Rationale: Explicit module boundaries and stable interfaces reduce integration risk and make it easier to govern security-relevant changes (input/output contracts, error handling) in a small, fast-moving learning project.
>
> Processes
>
> Define and version the interfaces for each module boundary (ports) and document expected request/response shapes
> Define the response envelope contract (success vs error) and required metadata fields to support diagnosability and contract testing
> Identify and document which module boundaries are considered external trust boundaries for review and testing focus
>
> Roles
>
> Solution Architect
> Developer
> Security Champion
>
> Priority: High

> 2:
>
> Id: PROC-002
>
> Phase: Implement
>
> Reference
>
>> Source Location: input_data.slot_context
>>
>> Source Quote: Pandas CSV read/query validation and defensive parsing to reduce CSV query execution/parsing failures
>>
>
> Rationale: Defensive input handling at the CSV-query boundary reduces avoidable failures and creates predictable behavior that can be validated via tests and enforced as a governance expectation.
>
> Processes
>
> Implement defensive parsing and validation for CSV inputs and supported filters before executing queries
> Implement structured error responses with stable error codes and user-safe messages
> Keep boundary adapters thin and isolate parsing/validation logic so it is unit-testable and reviewable
>
> Roles
>
> Developer
> Code Reviewer
>
> Priority: High

> 3:
>
> Id: PROC-003
>
> Phase: Test
>
> Reference
>
>> Source Location: input_data.slot_context
>>
>> Source Quote: Mandatory automated tests with coverage gating for RAG module, Agent/MCP integration, and Pandas CSV-query logic; keep handler complexity low
>>
>
> Rationale: Mandatory automated tests and coverage gating provide a measurable, enforceable mechanism to prevent regressions in critical integration paths and data-handling logic.
>
> Processes
>
> Maintain unit tests for core logic and edge cases (parsing/validation/query handling)
> Maintain contract tests for module composition with stubs and for response parsing compatibility at the chatbot↔tool boundary
> Enforce a coverage gate in CI and require triage/remediation of failing tests before merge
>
> Roles
>
> Developer
> Test Owner
> CI Maintainer
>
> Priority: High

> 4:
>
> Id: PROC-004
>
> Phase: Deploy
>
> Reference
>
>> Source Location: input_data.slot_context.candidate_tactics
>>
>> Source Quote: Basic timing instrumentation around MCP CSV-query path to track p95 latency; structured error messages for troubleshooting
>>
>
> Rationale: Deploy-time governance ensures that releases include the minimum observability and structured failure behavior needed to detect and resolve issues without expanding operational scope.
>
> Processes
>
> Verify instrumentation fields and structured errors are present in responses as part of release checks
> Confirm contract tests cover representative success and failure cases for the tool boundary
> Record baseline latency and error-rate metrics for the CSV-query path for later comparison
>
> Roles
>
> Release Owner
> Developer
> Test Owner
>
> Priority: Medium

> 5:
>
> Id: PROC-005
>
> Phase: Maintain
>
> Reference
>
>> Source Location: architecture_style_decision.qa_impacts.metrics
>>
>> Source Quote: Mean time to detect and identify failures in the MCP CSV-query path affecting chatbot answers (**SUGGESTED**)
>>
>
> Rationale: Ongoing measurement and triage workflows are needed to keep the integration path reliable and to make failures diagnosable over time.
>
> Processes
>
> Monitor and periodically review failure detection/diagnosis measures for the CSV-query path and track recurring causes
> Review and update the response envelope versioning/compatibility tests when schema changes are needed
> Maintain a lightweight incident/bug triage process for parsing errors, query failures, and compatibility regressions
>
> Roles
>
> Maintainer
> Developer
> Test Owner
>
> Priority: Medium


#### Security Tooling


#### Best Practices

> 1:
>
> Id: BEST-001
>
> Reference Framework: Custom
>
> Reference
>
>> Source Location: slot_context.candidate_tactics[2]
>>
>> Source Quote: Centralized, typed response envelope for MCP CSV-query results and errors to reduce parse failures and improve interoperability
>>
>
> Rationale: A single, typed envelope for success and error outcomes reduces ambiguity at integration boundaries and supports repeatable verification through contract tests.
>
> Practice: Standardize on a versioned response envelope for tool results that clearly separates success vs error and includes stable fields for parsing and diagnostics.
>
> Applicability: Applies to every chatbot↔tool call and to all contract tests that validate schema/format compatibility.
>
> Priority: High

> 2:
>
> Id: BEST-002
>
> Reference Framework: DefenseInDepth
>
> Reference
>
>> Source Location: input_data.slot_context.candidate_tactics
>>
>> Source Quote: Basic timing instrumentation around MCP CSV-query path to track p95 latency; structured error messages for troubleshooting
>>
>
> Rationale: Basic instrumentation and actionable error reporting provide layered assurance: issues are both detectable (timing) and diagnosable (structured errors), improving operational resilience.
>
> Practice: Emit lightweight timing metadata and structured, actionable error responses for all tool calls; ensure these outputs are testable and stable.
>
> Applicability: Applies to the CSV-query request lifecycle and to tests that validate observability fields and error schema determinism.
>
> Priority: Medium


#### Quality Gates

> 1:
>
> Id: QG-001
>
> Stage: CI
>
> Reference
>
>> Source Location: input_data.slot_context.candidate_tactics
>>
>> Source Quote: Mandatory automated tests with coverage gating for RAG module, Agent/MCP integration, and Pandas CSV-query logic; keep handler complexity low
>>
>
> Rationale: CI gating makes test coverage and stability an enforceable release criterion for core modules and integration seams.
>
> Checks
>
> Run unit tests for core modules and boundary parsing/validation logic
> Measure code coverage and enforce a minimum threshold per core module
> Fail the build on failing tests or unmet coverage requirements
>
> Pass Criteria: Blocking: pipeline passes only when all tests pass and the coverage gate is met.
>
> Priority: High

> 2:
>
> Id: QG-002
>
> Stage: PreDeployment
>
> Reference
>
>> Source Location: input_data.slot_context.candidate_tactics
>>
>> Source Quote: Contract tests for (a) module composition with stubs and (b) chatbot↔MCP result parsing (schema/format compatibility)
>>
>
> Rationale: Pre-deployment contract validation reduces the risk of schema/format incompatibilities and parsing regressions reaching users.
>
> Checks
>
> Execute contract tests that validate response envelope requirements for both success and error cases
> Execute composition tests with stubbed modules to validate interface compatibility across ports
> Verify representative failure modes return structured errors with stable codes/messages
>
> Pass Criteria: Blocking: deployment proceeds only if all contract/composition tests pass.
>
> Priority: High


#### Compliance Alignment




---

# Architectural Decisions

Title: Architecture Decision Log - Extracted from Task.docx.txt

Description: Extract architecturally significant decisions evidenced in the provided source document (Task.docx.txt), focusing on choices that materially affect system structure and quality attributes.

#### Decisions

> 1:
>
> Id: ADR-001
>
> Title: Use direct LLM processing (raw text concatenation +8000-char truncation) for the main batch analysis/report pipeline instead of retrieval-augmented generation
>
> Status: Accepted
>
> Date: N/A
>
> Author: N/A
>
> Context: The submission’s primary value-producing pipeline (CSV export, Plotly charts, HTML report) is generated via a direct LLM call over concatenated PDF text that is truncated, rather than using the implemented vector store/retriever path.
>
> Drivers
>
> N/A
>
> Rationale: N/A
>
> Alternatives Considered
>
> Use per-question retrieval over chunked documents (RAG) to supply relevant context instead of truncation (rejected: N/A (no explicit alternative evaluation or rejection is documented; this alternative is presented as a suggestion after the fact).)
> N/A ✓ selected
>
> Consequences
>
> Positive: Produces an end-to-end pipeline that generates a “polished HTML report with multiple Plotly visualizations” (as described in the source).
> Negative: Vector store/retriever becomes non-essential for the primary outputs (“You could delete the vector store… and the main output… would be identical”), undermining the claimed RAG architecture.
> Negative: Truncation risks incomplete/incorrect extraction (“Character-based truncation (`[:8000]`) may cut mid-sentence” and may lose large portions of long PDFs).
>
> Quality Attributes Impacted
>
> Accuracy/Completeness (risk of missing content due to truncation)
> Maintainability (architecture/docs mismatch; duplicated paths)
> Traceability (weak linkage between retrieved evidence and extracted outputs)
>
> Status Evidence: “Actual architecture: Path A (main pipeline — produces all outputs): PDF Files → Raw Text Concatenation → Truncate to8000 chars → Direct LLM Call → CSV → Charts → HTML”
>
> Decision Description: The main batch analysis path sends concatenated raw text (truncated to8000 characters) directly to the LLM to produce structured extraction outputs and downstream artifacts (CSV, charts, HTML report).
>
> Notes
>
> Classified as a significant tech choice because it determines the primary system pipeline and materially impacts output quality and the role of retrieval.
> Drivers/rationale are not documented in the source; only the implemented behavior and its critique are evidenced.
> Completeness score:45/100 (context and consequences evidenced; drivers, rationale, and explicit alternatives analysis missing).

> 2:
>
> Id: ADR-002
>
> Title: Implement a secondary RAG Q&A path using chunking + ChromaDB + MMR retriever + ConversationalRetrievalChain, but keep it separate from the batch/report pipeline
>
> Status: Accepted
>
> Date: N/A
>
> Author: N/A
>
> Context: The system includes a RAG-based Q&A capability, but it is exercised only by a small set of interactive queries and does not feed the core batch outputs (CSV/charts/HTML). This creates a two-path architecture where RAG is effectively peripheral.
>
> Drivers
>
> N/A
>
> Rationale: N/A
>
> Alternatives Considered
>
> Integrate the retriever into the batch extraction pipeline (use retrieval for each of the11 analysis queries) (rejected: N/A (no explicit rejection/decision outcome documented; presented as a recommendation).)
> N/A ✓ selected
>
> Consequences
>
> Positive: Provides an interactive Q&A capability using retrieval components (chunking, vector store, MMR retriever, conversational chain).
> Negative: Creates architectural disconnect/duplication (“The RAG pipeline exists but is not the pipeline that drives the application's core functionality”).
> Negative: Reduces the practical value of chunking/vector store for the primary use-case (“Chunking is done but the chunks are only used by the secondary Q&A path”).
>
> Quality Attributes Impacted
>
> Maintainability (two divergent paths; docs/implementation mismatch)
> Operability (harder to reason about what path produces what outputs)
> Effectiveness/Quality of responses (RAG not applied where it could reduce truncation loss)
>
> Status Evidence: “Path B (secondary — produces only stdout output): PDF Files → Chunking → ChromaDB → MMR Retriever → ConversationalRetrievalChain → Print answer”
>
> Decision Description: A separate path (Path B) uses a vector store and retriever for conversational Q&A, while the main analysis/reporting path (Path A) bypasses retrieval.
>
> Notes
>
> Classified as a significant tech choice because it defines a split topology (batch vs interactive) and influences maintainability and alignment with claimed architecture.
> Drivers/rationale are not documented; only the existence of separate paths and critique are evidenced.
> Completeness score:50/100 (context and consequences evidenced; drivers, rationale, and explicit alternatives analysis missing).

> 3:
>
> Id: ADR-003
>
> Title: Use environment-based secret management via python-dotenv instead of hardcoding API keys
>
> Status: Accepted
>
> Date: N/A
>
> Author: N/A
>
> Context: The source notes that API keys are managed via dotenv and that no real secrets are hardcoded in committed code.
>
> Drivers
>
> N/A
>
> Rationale: N/A
>
> Alternatives Considered
>
> Hardcode API keys/secrets in source code (rejected: Security risk; flagged as a potential red flag in the rubric (not chosen).)
> N/A ✓ selected
>
> Consequences
>
> Positive: Reduces likelihood of committing real secrets to source control (explicitly noted as not present).
> Negative: N/A (the source does not document downsides such as secret rotation, deployment secret injection, or key vault integration).
>
> Quality Attributes Impacted
>
> Security (secret handling)
> Compliance/Operational hygiene (reduces accidental secret exposure)
>
> Status Evidence: “`python-dotenv` used for API keys (no hardcoded real secrets).”
>
> Decision Description: Secrets (API keys) are managed using python-dotenv rather than being embedded directly in code.
>
> Notes
>
> Classified as a governance/standard decision because it is a cross-cutting security practice.
> Rationale and broader secret-management alternatives (vault/KMS, CI secret injection) are not discussed in the source.
> Completeness score:55/100 (decision and basic consequence evidenced; drivers and rationale missing; alternatives only implicitly addressed).


Notes: Decisions found:3 (all Accepted, based on the source describing the implemented architecture/practices). Status distribution: Accepted=3. Quality attributes covered by decisions: maintainability, operability, accuracy/completeness risk (via truncation), and security (dotenv). Canonical section sweep gaps (no architecturally significant decisions evidenced in the source for these areas): Executive Summary (no binding architecture commitments; only an evaluation summary), Requirements (no system requirements/SLAs captured), Quality Attributes (discussed as critique, but not as binding QA-driven design choices), Transition / Migration Plan (not present). Governance / Operations had one qualifying standard (dotenv); other governance topics (CI/CD, observability, formal testing strategy) are mostly described as missing rather than decided.



---



---

## Document Analytics and Effort Estimates

### Time Efficiency Summary

| Activity | Manual Process | AI-Assisted Process |
|------------------------|----------------|---------------------|
| *Input Processing* | **1h** | **39s** |
| *Document Creation* | **38h 58m** | **1h 9m** |
| *Coordination & Oversight* | **-** | **7h 30m** |
| **Total Effort** | **39h 59m** | **8h 40m** |
| **Time Saved** | **-** | **31h 19m** |

### Copilot Processing Statistics

- **Total Input Files: 1**
- **Input Files Total Tokens: ~4,173**
- **Output Tokens (Markdown): ~20,466**

### Estimates Used for Calculations

- **1.4** tokens per word (technical density)
- **60** words per minute baseline reading speed
- **+18%** overhead for deep comprehension (document-specific)
- **10** words per minute technical writing/composition speed
- **+60%** overhead for quality review and refinement

---
