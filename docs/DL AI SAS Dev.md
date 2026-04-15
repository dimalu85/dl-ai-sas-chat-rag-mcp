# Solution Strategy

**Title**: Notebook-Scale Hexagonal Chatbot: RAG + Agent/MCP Composition with Pandas CSV MCP Tool, Contracts, and CI-Tested Observability

**Primary Drivers**

Composability: explicitly compose the chatbot from the existing RAG module and Agent/MCP module via clear ports/adapters
Interoperability/compatibility: stable, versioned contracts (especially the MCP csv_query tool response envelope) that callers can rely on
Maintainability/supportability: mandatory automated tests with CI gating and clear module boundaries to enable change with confidence
Observability/manageability: required request correlation, timings (including segment timings), and structured errors; plus lightweight aggregation (p95, error rates)
Reliability/security: predictable, tested failure modes and explicit trust boundaries across module integrations

**Key Constraints**

- [CON-001] Must be a small learning project implemented in a Python Jupyter Notebook context
- [CON-002] Chatbot must be composed from two prior modules: a RAG module and an Agent/MCP module
- [CON-003] MCP server must query a CSV file using Pandas and return results to the chat
- [CON-004] Automated test coverage is mandatory
- [CON-005] Deliverable should be kept as short as possible

**Strategic Decisions**

> 1:
>
> Theme: Overall architecture style and modular boundaries (Hexagonal modular monolith)
>
> Justification: To keep a notebook-scale solution small (CON-001, CON-005) while still enabling composition of two existing modules (CON-002) and a new MCP CSV tool (CON-003), the architecture prioritizes composability/interoperability and testability via explicit boundaries. Ports-and-adapters enables stub-based composition tests and isolates integration concerns while remaining a single deployable unit.
>
> Decision: Use a Modular Monolith with Ports-and-Adapters (Hexagonal). Define explicit ports for RAG, Agent/MCP, and the CSV tool (CsvToolPort), with adapters on the outside and stub adapters for composition testing.
>
> - ADR-0002

> 2:
>
> Theme: RAG retrieval strategy (behind the RAG port)
>
> Justification: Answer quality and usability depend on retrieval effectiveness, while maintainability/composability require retrieval details to remain swappable behind the RAGPort so the Agent/MCP orchestration can be tested and evolved independently in a small notebook context.
>
> Decision: Implement retriever-based chunking as baseline, plus cross-document comparison retrieval and hierarchical retrieval for long documents, all encapsulated behind the RAGPort.
>
> - ADR-0007

> 3:
>
> Theme: Natural-disaster CSV querying via MCP server tool (Pandas)
>
> Justification: The solution must support natural-disaster questions by querying a CSV using Pandas through an MCP server (CON-003). Interoperability and reliability require a predictable tool contract and explicit failure handling, while maintainability requires unit/contract/composition tests and coverage gating (CON-004).
>
> Decision: Implement an MCP server exposing a csv_query tool that loads/queries the configured CSV via Pandas. Structure the adapter into read/validate/query/serialize steps and return a standardized response envelope v1; cover success and representative failures (read error, invalid question, empty result) with tests.
>
> - ADR-0005

> 4:
>
> Theme: Tool contract standardization and evolution (envelope v1 + backward-compatible change discipline)
>
> Justification: Interoperability/compatibility across ports/adapters requires a stable, versioned response shape that can evolve without repeatedly breaking the Agent/MCP integration and tests, while still embedding required observability fields for supportability.
>
> Decision: Standardize the csv_query MCP response envelope schema v1 (schema_version='v1', ok, exactly one of data/error, meta.request_id, meta.timing_ms; with segment timings and structured error_code where required). Evolve ports/envelopes backward-compatibly; bump schema_version only for breaking changes and update tests/stubs as part of any contract change.
>
> - ADR-0003
> - ADR-0006
> - ADR-0009

> 5:
>
> Theme: Test strategy and CI gating (unit + contract + composition tests with coverage gate)
>
> Justification: Mandatory automated coverage (CON-004) and the need to prove composition/interoperability across module boundaries drive a test pyramid that explicitly validates contracts and wiring, not just internal logic. CI enforcement preserves maintainability in a learning project where rapid iteration might otherwise erode test discipline.
>
> Decision: Adopt consumer-driven contract tests for the MCP envelope v1 (required fields, success/error exclusivity, failure modes, and versioning behavior) and composition tests that validate RAG + Agent/MCP + CSV tool wiring via ports (using stubs where appropriate). Run unit, contract, and composition tests on every change/before merge, with a configured coverage threshold gate in CI.
>
> - ADR-0004
> - ADR-0008
> - ADR-0002

> 6:
>
> Theme: Observability and lightweight operational feedback (correlation IDs, timings, structured errors, metrics aggregation)
>
> Justification: Observability/supportability requirements are met most consistently by making metadata mandatory at the contract boundary, and then extracting actionable signals (p95 latency and error-code rates) with minimal additional code suitable for a notebook and CI artifacts.
>
> Decision: Standardize request correlation (meta.request_id), total and per-segment timings, and structured errors with error_code in every tool response. Add a minimal metrics aggregation utility that consumes captured timings/errors to compute p95 latency and error-code rates over time, with test coverage and notebook/CI-visible outputs.
>
> - ADR-0006
> - ADR-0010

> 7:
>
> Theme: Security boundary clarity (minimal trust boundary documentation)
>
> Justification: With multiple modules and an externalized tool boundary (user/chat ↔ chatbot ↔ MCP tool ↔ CSV file), security and supportability improve when trust assumptions are made explicit at ports/adapters, without adding heavy process overhead that conflicts with the small-scope notebook constraint.
>
> Decision: Maintain a minimal Trust Boundary Map enumerating boundaries (RAG, Agent/MCP, MCP CSV tool/server, CSV file access, and user/chat interface), the direction of data flow, data types exchanged, and the contract surface (e.g., the MCP envelope v1).
>
> - ADR-0011


Overall Approach: Implement the chatbot as a notebook-friendly modular monolith using Hexagonal (ports-and-adapters) boundaries so the existing RAG module and Agent/MCP module can be composed via explicit ports, and extended with a new MCP server tool (csv_query) that queries a CSV via Pandas for natural-disaster questions. Interoperability and compatibility are achieved by standardizing a versioned tool response envelope (v1) with strict success/error shaping and mandatory observability metadata (request_id, timing_ms, segment timings, structured error codes). Maintainability and reliability are enforced through CI that runs unit, consumer-driven contract, and stub-based composition tests with a coverage gate, while observability is enhanced by aggregating captured timings/errors into p95 latency and error-code rate summaries suitable for inspection in the notebook and CI artifacts. Security-relevant assumptions are kept clear with a lightweight trust boundary map across ports/adapters.

**Trade-Offs**

| Trade-Off | Implication |
|----|----|
| Strict, versioned contracts and extensive automated tests (unit + contract + composition) with CI coverage gating vs Fastest possible iteration and minimal test/schema maintenance overhead | Accepted because CON-004 mandates coverage and the architecture’s main risks are broken composition/interoperability between modules and the MCP tool; tests and contracts provide objective, repeatable safeguards in a small project. |
| Rich observability in the tool contract (request_id, timings, segment timings, structured error codes) vs Smaller code surface and keeping internal processing details entirely private | Accepted because supportability/observability are key drivers and the metadata is required at the boundary; the solution limits scope by standardizing a single minimal envelope and using lightweight aggregation rather than a full telemetry stack. |
| Multiple RAG retrieval patterns (chunking, cross-document comparison, hierarchical retrieval) vs Simpler retrieval implementation and potentially lower latency | Accepted because these retrieval behaviors are explicitly selected in ADR-0007 and are isolated behind the RAG port to keep the rest of the system stable; any added latency can be made visible via the standardized timing instrumentation. |
| Explicit Hexagonal ports/adapters for RAG, Agent/MCP, and CSV tool vs A quick, unstructured notebook script with fewer interfaces | Accepted because composability/interoperability and CI-verifiable wiring are primary drivers; ports enable stub-based composition tests and keep the solution evolvable even as a learning project. |
| Metrics aggregation (p95 latency, error-code rates) from captured traces vs Avoiding extra implementation and avoiding potentially noisy statistics with small sample sizes | Accepted because it turns already-required timings/errors into actionable summaries with minimal added complexity, supporting manageability in CI despite limited sample sizes. |

**Notes**

- Business goals are not provided in the input; strategy is derived from quality attributes, constraints, architecture style, and ADRs only.
- ADR-0008 leaves the CI coverage threshold value unspecified (TBD); this needs an explicit configuration decision to avoid arbitrary gating.
- The definition of “breaking change” for schema_version bumps (ADR-0009) is noted as requiring clarity to prevent inconsistent versioning.
- Where and how aggregated metrics outputs are persisted (print vs file) is left flexible in ADR-0010; choose a minimal approach consistent with the notebook/CI setup.
- The exact CSV schema, allowed query/question format, and validation rules for “invalid question” are not specified; they must be defined to make failure-mode tests unambiguous.
- Agent/MCP integration details are only described at the port level; any additional tool invocation patterns beyond csv_query would require extending the same envelope/contract approach.



---

# C4 Context Diagram

Title: System Context - Notebook Chatbot (RAG + Agent/MCP + CSV MCP Tool)

Rationale: The system boundary is a notebook-scale modular-monolith chatbot that composes two internal modules (RAG and Agent/MCP) and includes an in-process MCP server tool (csv_query) to answer natural-disaster questions by reading/querying a local CSV via Pandas. Contract-tested, versioned response envelopes and lightweight observability metadata (request_id, timing_ms, segment timings, structured errors) are treated as core behaviors of the system. No explicitly named external deployed services/APIs (e.g., LLM providers, hosted monitoring, CI platform) are present in the provided artifacts, so none are modeled as external systems; the CSV dataset is treated as internal file I/O within the system boundary per the rules.

#### Target System

> Alias: notebookChatbot
>
> Name: Notebook Chatbot
>
> Description: Notebook chatbot combining RAG and Agent/MCP with an in-process CSV-query MCP tool and tests.
>
> Short Description: RAG + MCP Chatbot
>
> Group: 
>

#### Actors Identified

| Alias | Name | Description | Short Description | Type |
|-------|-------|-------|-------|-------|
| chatUser | Chat User | Asks questions and receives answers via the chatbot chat interface. | Chat user | Person |
| developer | Developer | Changes the notebook code and runs CI-tested unit, contract, and composition tests. | Developer | Person |

#### External Systems Identified


#### Relationships Identified

| Source Alias | Target Alias | Description | Short Description | Protocol | Protocol Technology |
|--------|--------|--------|--------|--------|--------|
| chatUser | notebookChatbot | Asks questions and receives chatbot answers. | Chats | Other | Jupyter |
| developer | notebookChatbot | Runs tests and reviews quality signals. | Tests | Other | CI |

#### Trade-offs

| Trade-Off | Implication |
|----|----|
| Model MCP CSV server and dataset access inside the target system boundary. vs Depicting the CSV dataset as an external system. | Artifacts specify in-process execution and CSV file access; file storage is internal per rules. |
| Omit any LLM provider, monitoring platform, or CI service as external systems. vs Visibility of third-party runtime dependencies. | No named deployed external services/endpoints are provided in the artifacts. |

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

        notebookChatbot = softwareSystem "Notebook Chatbot" "RAG + MCP Chatbot"
        chatUser = person "Chat User" "Chat user"
        developer = person "Developer" "Developer"
        chatUser -> notebookChatbot "Chats" "Jupyter"
        developer -> notebookChatbot "Tests" "CI"
    }

    views {
        systemContext notebookChatbot "SystemContext_notebookChatbot" {
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

Pandas is a library used internally for CSV read/query; it is not modeled as an external system.
MCP server capability is described as running in-process as part of the notebook-scale modular monolith.
The standardized csv_query response envelope (v1) and its contract tests are key cross-module contracts inside the system boundary.
Observability requirements are met via response metadata (request_id, timing_ms, segment timings) and structured error codes/messages returned by the MCP csv_query tool.
Ownership/enterprise boundaries cannot be inferred beyond the single learning-project system because no other owned systems are named.



---

# C4 Container Diagram

Title: Container Diagram - Notebook Chatbot

System Alias: notebookChatbot

#### Actors Identified

> Alias: chatUser
>
> Name: Chat User
>
> Description: Asks questions and receives answers via the chatbot chat interface.
>
> Short Description: Chat user
>
> Type: Person

> Alias: developer
>
> Name: Developer
>
> Description: Changes notebook code and runs CI-tested unit, contract, and composition tests.
>
> Short Description: Developer
>
> Type: Person


#### External Systems Identified


#### Containers Identified

> Alias: chatNotebook
>
> Name: Chat Notebook
>
> Description: Provides chat UI and orchestrates RAG and Agent/MCP flows.
>
> Short Description: Chat UI
>
> Rationale: Acts as the primary user-facing entry point in the Jupyter notebook context and coordinates calls to the modular capabilities via ports.
>
> Technology: Python Jupyter
>
> Archetype: Other
>
> Related ADR IDs
>
> ADR-0002

> Alias: agentMcpModule
>
> Name: Agent/MCP Module
>
> Description: Orchestrates agent reasoning and invokes MCP tools via ports.
>
> Short Description: Agent orchestration
>
> Rationale: Encapsulates Agent/MCP behaviors behind a port so the chatbot can compose it with RAG and tools while enabling stub-based composition tests.
>
> Technology: Python
>
> Archetype: Service
>
> Related ADR IDs
>
> ADR-0002

> Alias: ragModule
>
> Name: RAG Module
>
> Description: Retrieves relevant content using chunking, cross-doc, and hierarchical strategies.
>
> Short Description: Retrieval
>
> Rationale: Keeps retrieval strategies swappable behind a RAGPort to preserve composability and testability within the modular monolith.
>
> Technology: Python
>
> Archetype: Service
>
> Related ADR IDs
>
> ADR-0002
> ADR-0007

> Alias: csvMcpServer
>
> Name: CSV MCP Server
>
> Description: Exposes csv_query tool and returns envelope v1 responses.
>
> Short Description: CSV tool
>
> Rationale: Implements the required MCP server tool that queries a CSV via Pandas and emits a strict, observable envelope v1 for interoperability.
>
> Technology: Python Pandas
>
> Archetype: Service
>
> Related ADR IDs
>
> ADR-0002
> ADR-0003
> ADR-0005
> ADR-0006

> Alias: disasterCsv
>
> Name: Disaster CSV
>
> Description: Stores natural-disaster dataset queried by the MCP csv_query tool.
>
> Short Description: CSV data
>
> Rationale: Represents the file-based dataset accessed via File I/O by the Pandas-backed MCP tool.
>
> Technology: CSV
>
> Archetype: FileSystem
>
> Related ADR IDs
>
> ADR-0005

> Alias: metricsAggregator
>
> Name: Metrics Aggregator
>
> Description: Computes p95 latency and error-code rates from captured tool metadata.
>
> Short Description: Metrics
>
> Rationale: Turns mandatory request timings and structured errors into lightweight operational summaries suitable for notebook and CI artifacts.
>
> Technology: Python
>
> Archetype: Service
>
> Related ADR IDs
>
> ADR-0010
> ADR-0006

> Alias: testSuite
>
> Name: Test Suite
>
> Description: Runs unit, contract, and composition tests with coverage gating.
>
> Short Description: Tests
>
> Rationale: Enforces contract stability (envelope v1), validates module wiring via stubs, and applies the mandatory coverage gate in CI.
>
> Technology: pytest pytest-cov
>
> Archetype: ConsoleApp
>
> Related ADR IDs
>
> ADR-0008
> ADR-0004


#### Relationships Identified

> Source Alias: chatUser
>
> Target Alias: chatNotebook
>
> Description: Asks questions and reads chatbot answers.
>
> Short Description: Chats
>
> Protocol: Other
>
> Protocol Technology: Jupyter

> Source Alias: developer
>
> Target Alias: chatNotebook
>
> Description: Edits and runs the notebook chatbot during development.
>
> Short Description: Develops
>
> Protocol: Other
>
> Protocol Technology: Jupyter

> Source Alias: developer
>
> Target Alias: testSuite
>
> Description: Runs the automated tests and reviews quality signals.
>
> Short Description: Tests
>
> Protocol: Other
>
> Protocol Technology: CI

> Source Alias: chatNotebook
>
> Target Alias: agentMcpModule
>
> Description: Submits prompts for agent orchestration and tool use.
>
> Short Description: Orchestrates
>
> Protocol: InProcess
>
> Protocol Technology:

> Source Alias: agentMcpModule
>
> Target Alias: ragModule
>
> Description: Requests retrieval results to ground generated answers.
>
> Short Description: Retrieves
>
> Protocol: InProcess
>
> Protocol Technology:

> Source Alias: agentMcpModule
>
> Target Alias: csvMcpServer
>
> Description: Invokes csv_query tool for natural-disaster questions.
>
> Short Description: Queries CSV
>
> Protocol: InProcess
>
> Protocol Technology:

> Source Alias: csvMcpServer
>
> Target Alias: disasterCsv
>
> Description: Reads CSV data to answer tool queries.
>
> Short Description: Reads data
>
> Protocol: FileIo
>
> Protocol Technology:

> Source Alias: chatNotebook
>
> Target Alias: metricsAggregator
>
> Description: Aggregates timings and error codes into summary metrics.
>
> Short Description: Aggregates
>
> Protocol: InProcess
>
> Protocol Technology:

> Source Alias: testSuite
>
> Target Alias: chatNotebook
>
> Description: Executes composition tests for module wiring through ports.
>
> Short Description: Composes
>
> Protocol: InProcess
>
> Protocol Technology:

> Source Alias: testSuite
>
> Target Alias: csvMcpServer
>
> Description: Validates envelope v1 success and failure responses.
>
> Short Description: Contracts
>
> Protocol: InProcess
>
> Protocol Technology:

> Source Alias: testSuite
>
> Target Alias: metricsAggregator
>
> Description: Verifies p95 latency and error-rate computations.
>
> Short Description: Verifies
>
> Protocol: InProcess
>
> Protocol Technology:


#### Trade Offs

> Trade-Off: Modular monolith with explicit ports/adapters vs Simplest single-script notebook structure
>
> Implication: Enables composability of RAG and Agent/MCP plus stub-based composition tests in a small scope.

> Trade-Off: Strict envelope v1 contract with mandatory observability vs Smaller tool response surface and hidden internal timings
>
> Implication: Improves interoperability and supportability and is enforceable via contract tests.

> Trade-Off: CI-gated unit, contract, and composition tests with coverage threshold vs Fastest iteration with minimal test maintenance
>
> Implication: Meets mandatory coverage requirements and reduces integration breakage risk across module boundaries.


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

        notebookChatbot = softwareSystem "Notebook Chatbot" "" {
            chatNotebook = container "Chat Notebook" "Chat UI" "Python Jupyter"
            agentMcpModule = container "Agent/MCP Module" "Agent orchestration" "Python" "Application"
            ragModule = container "RAG Module" "Retrieval" "Python" "Application"
            csvMcpServer = container "CSV MCP Server" "CSV tool" "Python Pandas" "Application"
            disasterCsv = container "Disaster CSV" "CSV data" "CSV" "Datastore"
            metricsAggregator = container "Metrics Aggregator" "Metrics" "Python" "Application"
            testSuite = container "Test Suite" "Tests" "pytest pytest-cov" "Application"
        }
        chatUser = person "Chat User" "Chat user"
        developer = person "Developer" "Developer"
        chatUser -> notebookChatbot.chatNotebook "Chats" "Jupyter"
        developer -> notebookChatbot.chatNotebook "Develops" "Jupyter"
        developer -> notebookChatbot.testSuite "Tests" "CI"
        notebookChatbot.chatNotebook -> notebookChatbot.agentMcpModule "Orchestrates" "In-Process"
        notebookChatbot.agentMcpModule -> notebookChatbot.ragModule "Retrieves" "In-Process"
        notebookChatbot.agentMcpModule -> notebookChatbot.csvMcpServer "Queries CSV" "In-Process"
        notebookChatbot.csvMcpServer -> notebookChatbot.disasterCsv "Reads data" "File I/O"
        notebookChatbot.chatNotebook -> notebookChatbot.metricsAggregator "Aggregates" "In-Process"
        notebookChatbot.testSuite -> notebookChatbot.chatNotebook "Composes" "In-Process"
        notebookChatbot.testSuite -> notebookChatbot.csvMcpServer "Contracts" "In-Process"
        notebookChatbot.testSuite -> notebookChatbot.metricsAggregator "Verifies" "In-Process"
    }

    views {
        container notebookChatbot "Container_notebookChatbot" {
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

No external systems are identified in the provided context; all capabilities are modeled as in-process containers within the notebook-scale system.
The RAG module’s underlying document stores/indexes are not specified in the provided artifacts and are therefore not modeled as separate containers.



---

# Developer Recommendations

#### Process Recommendations

> 1:
>
> Id: PROC-001
>
> Category: Continuous Integration Quality Gate
>
> Reference
>
>> Source Location: input_data/slot_context
>>
>> Source Quote: CI must run on every change/before merge and fail if coverage threshold not met (threshold value currently unspecified) (CRD-002; CON-004).
>>
>
> Rationale: A CI gate with an explicit coverage threshold and required test suites provides objective, repeatable proof of maintainability and reliability while keeping the notebook-scale project disciplined.
>
> Recommendation: Make “merge-ready” contingent on CI running on every change/before merge, executing unit + contract + composition tests, and failing the pipeline if overall coverage is below a configured threshold (value TBD but enforced).
>
> Priority: High
>
> Related QAs
>
> Maintainability
> Reliability
> Composability
> Interoperability

> 2:
>
> Id: PROC-002
>
> Category: Contract Testing Process
>
> Reference
>
>> Source Location: slot_context (ADR-0004)
>>
>> Source Quote: Must cover required fields, success/error exclusivity, schema versioning behavior, and failure modes: read error, invalid question, empty result (RELIABILITY-004; CRD-004).
>>
>
> Rationale: Contract tests are the enforceable mechanism ensuring stable interoperability and reliable failure behavior across ports/adapters.
>
> Recommendation: Adopt consumer-driven contract tests for the tool/port response envelope that assert: required fields, schema_version behavior, success/error mutual exclusivity, and explicit failure modes (read error, invalid question, empty result).
>
> Priority: High
>
> Related QAs
>
> Interoperability
> Reliability
> Standards_compliance
> Compatibility
> Observability

> 3:
>
> Id: PROC-003
>
> Category: Contract Change Control
>
> Reference
>
>> Source Location: input_data/slot_context
>>
>> Source Quote: Contract-change step required for any port/schema update: update schema/version as needed, update contract tests, ensure stub composition tests pass (MAINTAINABILITY-006; COLLAB-006).
>>
>
> Rationale: A lightweight change-control workflow prevents silent breaking changes and keeps module composition verifiable in CI.
>
> Recommendation: For any port/envelope change, require a contract-change checklist: (1) decide backward-compatible vs breaking, (2) bump schema_version only for breaking changes, (3) update contract tests, and (4) ensure stub-based composition tests pass before merge.
>
> Priority: High
>
> Related QAs
>
> Compatibility
> Maintainability
> Composability
> Interoperability

> 4:
>
> Id: PROC-004
>
> Category: Security Documentation Standard
>
> Reference
>
>> Source Location: slot_context.ADR-0011.slot_notes
>>
>> Source Quote: Explicit requirement to identify and document trust boundaries (SECURITY-001); test cases/review depth is suggested but not mandated.
>>
>
> Rationale: Documenting trust boundaries at ports/adapters supports secure composition and makes external input handling explicit without adding heavy process.
>
> Recommendation: Maintain a minimal Trust Boundary Map for each port/adapter boundary (including user input and CSV access) and require updating it in the same change whenever a port/tool surface is added or modified.
>
> Priority: Medium
>
> Related QAs
>
> Security
> Composability
> Maintainability


#### Tooling Recommendations

> 1:
>
> Id: TOOL-001
>
> Category: Unit Test Runner and Coverage Measurement Tool
>
> Reference
>
>> Source Location: adr_per_slot_decisions → ADR-0008 recommendations
>>
>> Source Quote: pytest + coverage.py (pytest-cov)
>>
>
> Rationale: Automated testing with measurable coverage enables a hard coverage gate and supports fast regression detection in a small project.
>
> Recommendation: Use a unit-test runner plus a coverage measurement tool integrated into CI so the build can fail when the configured coverage threshold is unmet.
>
> Priority: High
>
> Related QAs
>
> Maintainability
> Reliability

> 2:
>
> Id: TOOL-002
>
> Category: CSV Query Library (Dataframe-Based)
>
> Reference
>
>> Source Location: DL AI SAS SAD.docx.txt, special_instructions
>>
>> Source Quote: create an MCP server, that will query CSV file with Pandas and return user responses to their question from chat.
>>
>
> Rationale: A dataframe-style CSV querying capability is required for the natural-disaster feature and should remain behind a port/adapter for testability.
>
> Recommendation: Implement the CSV-query adapter using a dataframe-based CSV processing library (kept behind the CSV tool port) to support natural-disaster Q&A from a local CSV dataset.
>
> Priority: High
>
> Related QAs
>
> Interoperability
> Maintainability
> Reliability

> 3:
>
> Id: TOOL-003
>
> Category: Metrics Aggregation Utility
>
> Reference
>
>> Source Location: slot_context.ADR-0010.candidate_tactics
>>
>> Source Quote: Instrument per-segment timings (read/validate/query/serialize) and compute p95 and error-code rates from captured timings (AIML-MONOPS-002; AIML-MONOPS-005).
>>
>
> Rationale: A minimal aggregation utility makes observability/manageability requirements actionable (p95 and error rates) without adding service-level infrastructure.
>
> Recommendation: Add a lightweight metrics aggregation utility that consumes emitted meta timing data and structured error codes to compute p95 latency and error-code rates, producing notebook/CI-inspectable summaries.
>
> Priority: Medium
>
> Related QAs
>
> Observability
> Manageability
> Reliability
> Maintainability


#### Coding Best Practices

> 1:
>
> Id: CODE-001
>
> Category: Versioned Response Envelope Implementation
>
> Reference
>
>> Source Location: slot_context (ADR-0003)
>>
>> Source Quote: Envelope must include schema_version='v1', ok, exactly one of data/error, meta.request_id and meta.timing_ms; validated by contract tests (VCNLP-006; MRTE-001).
>>
>
> Rationale: A strict envelope makes cross-module/tool integration predictable and contract-testable.
>
> Recommendation: Implement the tool response envelope v1 exactly: schema_version='v1', ok, exactly one of data/error, and meta containing request_id and timing_ms; keep envelope construction centralized to avoid drift.
>
> Priority: High
>
> Related QAs
>
> Interoperability
> Observability
> Standards_compliance
> Compatibility

> 2:
>
> Id: CODE-002
>
> Category: Observability Fields and Structured Errors
>
> Reference
>
>> Source Location: input_data.slot_context
>>
>> Source Quote: Every response (success/failure) must include meta.request_id and meta.timing_ms; include segment timing breakdown and error_code in structured error (MON-001; AIML-MONOPS-002).
>>
>
> Rationale: Correlation IDs, timings, and structured error codes make failures diagnosable and enable metric computation (latency/error-rate) from emitted data.
>
> Recommendation: Generate a unique request_id per tool invocation, capture total timing_ms plus per-segment timings (read/validate/query/serialize), and return structured errors with an error_code on every failure path.
>
> Priority: High
>
> Related QAs
>
> Observability
> Reliability
> Manageability

> 3:
>
> Id: CODE-003
>
> Category: Adapter Step Decomposition and Failure-Mode Handling
>
> Reference
>
>> Source Location: slot_context (ADR-0005)
>>
>> Source Quote: define adapter responsibilities (read/validate/query/serialize) to support required segment timings.
>>
>
> Rationale: Explicit read/validate/query/serialize steps make behavior testable, timing instrumentation consistent, and failure modes deterministic.
>
> Recommendation: Structure the CSV tool adapter into explicit steps (read, validate, query, serialize); ensure each step can surface a controlled failure that maps to an envelope error response (including read error, invalid question, and empty result) and is covered by tests.
>
> Priority: High
>
> Related QAs
>
> Reliability
> Maintainability
> Observability

> 4:
>
> Id: CODE-004
>
> Category: Retriever-Based RAG Patterns
>
> Reference
>
>> Source Location: slot_context
>>
>> Source Quote: Must implement retriever-based chunking (SIR-001), cross-document retrieval (SIR-002), and hierarchical retrieval for long docs (SIR-004).
>>
>
> Rationale: Retriever-based and hierarchical patterns improve answer usefulness while keeping retrieval behavior modular and testable behind a port.
>
> Recommendation: Implement the RAG module behind its port using: (1) retriever-based chunk retrieval, (2) cross-document comparative retrieval, and (3) hierarchical retrieval for long documents (coarse-to-fine).
>
> Priority: Medium
>
> Related QAs
>
> Usability
> Maintainability
> Composability




---



---

## Document Analytics and Effort Estimates

### Time Efficiency Summary

| Activity | Manual Process | AI-Assisted Process |
|------------------------|----------------|---------------------|
| *Input Processing* | **5h 22m** | **1m** |
| *Document Creation* | **13h 54m** | **37m** |
| *Coordination & Oversight* | **-** | **2h 12m** |
| **Total Effort** | **19h 17m** | **2h 51m** |
| **Time Saved** | **-** | **16h 26m** |

### Copilot Processing Statistics

- **Total Input Files: 1**
- **Input Files Total Tokens: ~23,177**
- **Output Tokens (Markdown): ~7,304**

### Estimates Used for Calculations

- **1.4** tokens per word (technical density)
- **60** words per minute baseline reading speed
- **+17%** overhead for deep comprehension (document-specific)
- **10** words per minute technical writing/composition speed
- **+60%** overhead for quality review and refinement

---
