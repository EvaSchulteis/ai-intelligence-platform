# Weekly Engineering Log

## Week of 2026-08-03

### What I built 
- Continued building the Crunchbase ingestion module and its retry behavior.
- Added/expanded tests around retry behavior and exception handling.
- Refactored/considered boundaries between application, ingestion, and domain layers.

### Engineering concepts I learned
- A reusable piece of code is not automatically a reusable abstraction. Extract code when the knowledge and reason for change are shared—not merely because the syntax appears more than once.
- A responsibility is defined by its reason to change, not by the number of operations it performs. A function can contain several steps and still have one coherent responsibility if those steps change for the same reason.
- Architecture can be understood by tracing knowledge boundaries: the application orchestrates, the domain represents internal concepts, and ingestion communicates with and translates external systems.
- Reading unfamiliar code is an engineering skill. Understanding the story a module is trying to tell is more useful than merely enumerating its functions and statements.
- Not every algorithm deserves its own abstraction. Fixed delay, exponential backoff, jitter, and retry-after handling can all belong to retry policy because they answer the same question: how should retries behave?
- Refactoring should be driven by evidence of multiple reasons to change, not by the theoretical possibility of future complexity.

### Engineering principles I practiced
- The thing that chooses which implementation to use should usually live at a higher level than the thing that performs the work.
- Single responsibility principle as "single reason to change."
- Separation of concerns — particularly separating external-system communication, domain representation, application orchestration, notifications, and persistence.
- Dependency inversion / dependency injection — callers should be able to supply a dependency rather than forcing lower-level code to choose its own implementation.
- Prefer narrow contracts over "anything goes" interfaces. A function returning whatever happens to be available today can create downstream ambiguity and make future changes harder to manage.
- Don't introduce dependencies merely because two pieces of code currently interact. A lower-level module should not acquire knowledge of higher-level business concepts just because it happens to participate in the workflow.

### Mental model that clicked
- Read code by asking why it exists, not what it does. Instead of describing syntax ("this file has one function"), describe responsibilities ("this module orchestrates the workflow"). Responsibilities reveal architecture much better than implementation details.
- Architecture is about protecting boundaries. A good abstraction doesn't merely make code reusable. It protects a responsibility from unrelated changes.

### Decisions made
- Keep external-source-specific knowledge inside the ingestion layer rather than allowing it to leak into the company domain model.
- Keep application.py responsible for orchestration rather than putting business rules or external-system knowledge there.
- Keep retry behavior together while it represents one coherent retry policy; don't split individual retry algorithms into abstractions prematurely.
- Prefer dependency injection when the caller should control which implementation is used.
- Don't generalize a function into a reusable utility until there is evidence that its knowledge and reason for change are actually shared.
- Continue separating what the system should do from how it performs the work.

### Connections I noticed
- The same architecture principles apply to dbt and Python. A staging model shouldn't know business logic just as an ingestion module shouldn't know domain decisions. Both are examples of putting knowledge at the correct boundary.
- Freshness checking and retry policy are structurally similar. Both separate a policy ("what counts as acceptable?") from a mechanism ("how do we perform the check/retry?").


## Week of 2026-07-27

### What I built
- Designed and then built the next iteration of the retry policy in crunchbase.py before implementing it.
- Planned the structure of and then built tests for retrying HTTP 500 & 400 errors, along with all the other contracts within should_retry() in crunchbase.py

### Engineering concepts I learned
- Different exception classes expose different information. For example, HTTPError carries a response object, while ConnectionError does not.
- Safe exception handling often requires identifying the exception type before accessing exception-specific attributes.
- Tests should use real library objects whenever practical and only fake the minimum behavior needed. 
- Retry decisions can depend on data carried by an exception object (such as an HTTP status code), not just the exception type itself.
- A unit test should fail because our code is wrong, not because the environment is different. 
- Abstraction exists so that change has somewhere to go. 

### Engineering principles I practiced
- Single Responsibility Principle: a test should have one reason to fail.
- Dependency Injection: instead of creating your dependency yourself, someone else gives it to you.
- Boundary isolation: find the boundary of the code I'm testing and replace only that dependency.
- Designing for change: Things that change together belong together. Things that change for different reasons should be separated.
- Separation of concerns: responsibilities exist at different scales: project, package, module, class, and function.

### Mental model that clicked
- Exception handling follows the same design principles as the rest of the application: first determine what kind of object you're working with, then safely use the information that object provides.
- Good exception handling progressively narrows possibilities rather than making assumptions about every failure.
- Good tests preserve as much real behavior as possible and replace only the boundary being isolated.
- Think of single responsibility principle as single reason to change.
- Architecture is about putting knowledge where it belongs. A good system separates responsibilities based on what can change independently. External APIs, domain concepts, analytics logic, and notifications should not know more about each other than necessary.

### Decisions made
- Retry policy should eventually distinguish between retryable server failures (5xx) and non-retryable client failures (4xx).
- If retry rules continue accumulating, revisit whether the retry policy itself should become a separate abstraction rather than continuing to grow inside a single function.
- Use a real requests.exceptions.HTTPError in tests and attach a fake response rather than creating a fake HTTP error class.
- Continue writing tests that describe new behavior before modifying production code.

### Connections I noticed
- Progressively narrowing the possibilities when handling exceptions is similar to minding the order of a CASE WHEN statement.
- Designing retry logic is similar to business rules in analytics engineering: the challenge is less about syntax and more about deciding where the business knowledge belongs.
- Using real library objects in tests is similar to using real dbt macros while mocking only upstream data—you keep as much production behavior as possible while isolating the dependency under test.
- Software boundaries are similar to dbt model boundaries. A staging model shouldn't contain business logic, and a domain model shouldn't contain API-specific logic. Both are about separating the source of truth from the transformations built on top of it.

## Week of 2026-07-20

### What I built
- Added automated tests with pytest for the Crunchbase ingestion flow.
- Created tests for should_retry() to validate retry policy decisions for different exception types.
- Created a test for fetch_company_from_crunchbase() by replacing the API dependency with a fake response, allowing the domain transformation logic to be tested independently from the external service.
- Created a test for get_crunchbase_response() by replacing requests.get() with a fake implementation and verifying that API responses are transformed into dictionaries correctly.
- Learned how to use monkeypatch to replace dependencies during tests without changing production code.
- Added pytest as a development dependency using uv add --dev pytest.

### Engineering concepts I learned
- Libraries often provide higher-level abstractions over common patterns (e.g. response.json() encapsulates response.text + json.loads()).
- HTTP requests consist of a destination (URL) and metadata (headers); they serve different purposes.
- Query parameters are another way HTTP requests communicate information, similar to headers, but they describe what resource you're requesting rather than how to communicate.
- The requests library can construct query strings from a Python dictionary using params=..., hiding URL formatting details.
- The ingestion layer translates communication in both directions: it translates our application's requests into the external API's language and translates the API's responses back into our domain model.
- Python objects can contain attributes and methods; a Response object is a wrapper around HTTP information.
- Libraries often create specialized types (e.g., CaseInsensitiveDict) to encapsulate domain-specific behavior.
- Exceptions are objects representing failures, not just messages.
- A function contract includes the type/shape of the data it promises to return.
- Breaking a contract causes failures at the boundary where assumptions no longer hold.
- Exceptions are objects, not just error messages.
- Exception propagation through multiple abstraction layers.
- Exception chaining with raise ... from error.
- Translating technical failures into application-level errors.
- Libraries expose abstraction boundaries through their own exception hierarchies.
- Responsibility ownership applies to error handling as well as data modeling.
- Tests should validate behavior and contracts rather than implementation details.
- A mock should replace the boundary dependency that a function interacts with, not simply fake the final data output.
- Dependencies should be mocked where the code looks them up, not where they originally come from (e.g., patching crunchbase.requests.get rather than the global requests.get).
- A fake object only needs to implement the interface that the production code uses; it does not need to recreate the entire real object.
- Python's duck typing allows different objects to be treated interchangeably if they provide the expected methods and behavior.
- A function contract includes the interfaces it expects from its dependencies, not just its inputs and outputs.
- requests.get() returns a Response object with behavior (raise_for_status(), json()), not just raw data.
- API ingestion testing requires controlling external dependencies so tests are deterministic and do not rely on network availability.
- Pytest separates test setup, execution, and validation: setup creates the environment and dependencies, execution runs the production code, and assertions verify the expected behavior.
- Retry logic is a policy decision based on the nature of failures, not just the existence of an exception.
- Connection failures and server-side failures may be transient, while client-side errors often indicate a request that should not be retried.
- HTTP status codes provide information that can guide application behavior (e.g., distinguishing retryable 500-level failures from non-retryable 400-level failures).

### Mental model that clicked
- Good libraries apply the same design principles that I should apply in my own code: hide repetitive implementation details while preserving a simple public contract.
- I had been thinking of the ingestion layer as translating external data into internal models. Today I realized it is really an interpreter between two systems, responsible for translating both outbound requests and inbound responses while shielding the rest of the application from external API details.
- External representations flow through layers: HTTP response → parsed dictionary → domain model.
- Each layer should hide implementation details from the layer above.
- The question remains: "Who owns this knowledge?"
- The happy path and failure path both flow through the architecture.
- Each layer should understand failures in its own language.
- Errors are another form of data transformation.
- A test is not checking whether code works in isolation; it is checking whether a component honors its contract with the systems around it.
- Mocking is less about "fake data" and more about "fake collaborators."
- The important question when creating a mock is: "What does my code expect this dependency to be able to do?"
- External systems should be treated as unreliable collaborators. Production code needs to define what happens when those systems fail.
- The architecture now has clear testing boundaries:requests.get() → get_crunchbase_response() tests communication handling. get_crunchbase_response() → fetch_company_from_crunchbase() tests transformation into domain objects.
-The same separation principles apply to testing as to application design: each layer should be responsible for its own concerns.
- Reliability is part of ingestion design, not an afterthought added after the happy path works.

### Decisions made
- Keep communication-specific knowledge (URL construction, headers, authentication) inside the ingestion layer rather than exposing it to callers.
- Retry logic currently belongs inside get_crunchbase_response() because it owns communication with the external system.
- A shared retry abstraction should only be introduced when multiple consumers justify it.
- Keep tests focused on behavior rather than internal implementation details.
- Mock get_crunchbase_response() when testing domain transformation logic.
- Mock requests.get() when testing API communication logic.
- Keep retry logic inside the ingestion layer for now because that layer owns communication with the external API.
- Continue separating retry policy (should_retry) from retry execution (the loop that performs retries).
- Expand retry logic to consider HTTP status codes rather than only exception types.

### Connections I noticed
- response.json() is similar to using a well-designed dbt macro: instead of repeating multiple implementation steps everywhere, you expose a simpler operation that communicates intent.
- URLs and headers are configuration for communicating with an external system, similar to connection profiles or source configurations in analytics engineering—they describe how to communicate, not what the business logic is.
- Mocking dependencies is similar to isolating upstream systems in analytics engineering: when testing a dbt model, you often want to control the inputs rather than rely on live upstream data.
- The fake response object is similar to creating a test fixture for a warehouse table: it provides the shape and behavior needed for downstream logic without depending on the real source.
- API ingestion reliability has parallels with data pipeline reliability: external API availability ≈ upstream source availability, retries ≈ pipeline recovery strategies, contracts ≈ source schema expectations.
- The same principle applies across Python, SQL, and dbt: define clear boundaries, hide implementation details, and make assumptions explicit.
- Testing has reinforced the same architectural question from earlier: "Who owns this knowledge?", The ingestion layer owns API communication knowledge; the domain layer owns business object knowledge.

## Week of 2026-07-13

### What I built
- Built the first application orchestrator.
- Replaced the mocked Crunchbase response flow with a real HTTP request pattern using requests, exposing the difference between external API responses and internal domain models.

### Engineering concepts I learned
- When to use a dataclass vs a regular class
- The difference between functions (return values) and applications (produce effects)
- Orchestration
- Good abstractions let implementations evolve without changing their public contract.
- Variable names can document architecture.
- Encapsulation: When external requirements change, the change should be localized behind the appropriate boundary.
- Distinguish between domain models and external representations.
- YAGNI - "Don't build tomorrow's solution until today's problem actually requires it."
- External representations vs internal models
- Error ownership follows responsibility
- Mocking and external dependencies
- Naming should describe concepts, not temporary implementation details
- `import json` and `import requests` are both modules. The module is really a namespace—a container that groups related functionality together.
- There are often two files: One that expresses intent. One that records implementation.
- Contracts exist through the function signature, the function name, the code that consumes it, and the assumptions between the two modules.
- HTTPS lifecycle: A request returns a Response object, which contains status codes, headers, and body content. response.text and response.json() represent different transformations of the response body.
- JSON serialization/deserialization: json.loads() converts JSON strings into Python objects. json.dumps() converts Python objects into JSON strings.

### Mental model that clicked
- The application coordinates modules rather than doing the work itself.
- Why requests exists, what a Response object represents, where HTTP belongs architecturally, where failures belong, why external dependencies complicate testing, and why we mock at boundaries.
- A function’s contract allows the implementation behind it to change without affecting callers. External systems should be isolated behind contracts. The rest of the application should depend on the shape of the data it receives, not the mechanism used to retrieve it. Debugging starts by identifying which contract was violated rather than immediately changing code. 

### Decisions made
- Chose a single `application.py` rather than an `application/` package because only one application exists today.
- `fetch_company_response()` should remain the public operation to `application.py`. The latter doesn’t need to know the order things are executed, it just wants to receive a Company dataclass.

### Connections I noticed
- The ingestion layer should be responsible for mapping because, in dbt, you perform casts and field manipulation in staging rather than downstream. We’re mapping external representations to our domain model.
- Encapsulation is like changing the staging layers of a mart that is connected to Tableau. So long as the output into the mart stays the same, Tableau doesn’t care about any changes that were made.
- It’s preferred in a python module to list the public function first and then the helpers, similar to how it’s preferred to start with the engineering principle and outcome before jumping into the details in an interview story (going chronologically is great for debugging though).
- "The decision to avoid premature abstractions mirrors analytics engineering: don't create intermediate models unless they simplify downstream logic or remove duplication."
- Error boundaries and deciding where we convert a technical failure into something meaningful is similar to where we deal with a column name changing from a source in dbt (we do that at the staging layer and not the mart layer).
- Splitting functions so they have discrete functions makes it easier to identify where a contract was violated. This is the same as modularity in dbt models.


## Week of 2026-07-06

### What I built
- Created the first `Company` domain model.
- Added the first ingestion module (`crunchbase.py`).
- Organized the project into `domain` and `ingestion` packages.
- Implemented the first end-to-end ingestion function (`fetch_company_from_crunchbase()`).
- Built the first application orchestrator (`application.py`) that coordinates the workflow.

### Engineering concepts I learned
- Packages vs. modules
- `__init__.py`
- Dataclasses
- Type hints
- Imports
- Local variable scope
- Application vs. library
- Orchestration
- Separation of responsibilities

### Mental model that clicked
- Every function call gets its own local workspace.
- The application orchestrates modules rather than performing their work itself.
- Functions should expose useful operations while hiding implementation details.

### Decisions we made
- Kept `Company` as a dataclass because its primary responsibility is representing data.
- Organized the project by responsibility (`domain`, `ingestion`) rather than by file type.
- Implemented the smallest possible version of each architectural contract before introducing external systems.

### Connections I noticed
- Organizing Python packages by responsibility feels similar to organizing dbt projects into staging, intermediate, and marts.
- Introducing abstractions only after duplication appears mirrors the HCP model refactor I completed at work.
- The application layer plays a role similar to `dbt build`: it orchestrates components rather than performing the transformations itself.


## Week of 2026-06-29

### What I built
- Created the skeleton for the AI Intelligence Platform packaged application.
- Initialized the project with `uv`.
- Created the virtual environment and `pyproject.toml`.
- Configured the project to use the `src/` layout.
- Connected the project to GitHub using SSH.

### Engineering concepts I learned
- Packaged applications vs. libraries vs. standalone applications.
- `src` layout
- Editable installs
- `sys.path`
- Virtual environments
- Build systems
- Git branches and SSH authentication

### Mental model that clicked
- Python is only one layer of a larger development ecosystem that includes virtual environments, package managers, build systems, and the import system.

### Decisions made
- Used `uv` instead of `pip` as the primary project manager.
- Chose the `src/` project layout because it better reflects production Python projects.
- Decided to build one evolving portfolio project rather than many small tutorial projects.
- Adopted an engineering-first learning approach focused on architecture before implementation.

### Connections I noticed
- A .pth file pointing to the src directory is similar to a a sticky header with a hyperlink at the top of a website. The hyperlink references another page. That other page could get updated, but the hyperlink in the header doesn't need to change.
- A packaged Python project feels similar to a dbt project: both rely on conventions, project configuration, and clear organization rather than a collection of independent files.