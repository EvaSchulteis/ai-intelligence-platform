# Weekly Engineering Log

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