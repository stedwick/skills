---
name: functional-programming
description: Apply practical functional programming patterns when writing, changing, or reviewing application logic in any language. Use named functions, explicit inputs and outputs, separate side effects, and fast tests to make business rules easy to reuse and verify. Applies to UI behavior, services, APIs, CLI commands, and tools; does not require functional languages or apply to styling-only or static markup changes.
---

# Functional programming

Build application logic from small, named, tested functions. Prefer clear behavior and simple composition over clever abstractions. Use these patterns where they improve the code, while keeping the language's idioms and the project's existing structure.

## Scope

- Apply this guidance to new and changed logic. Refactor nearby code only when needed for the task. Broader refactoring requires a request.
- Keep existing frameworks and public contracts. Do not introduce a functional library, dependency injection framework, or new architecture just to follow this skill.
- Pure CSS and static markup need no function extraction. Their behavior code can still benefit from these patterns.
- Treat these as defaults, not mechanical rules. Keep a simple local expression inline when extraction would only add indirection.

## Functions and ownership

- Give each business rule or operation one clear function and one clear home. Name it for what it does in the domain, such as `calculateShipping` or `approveOrder`.
- A function should have one coherent responsibility. A complex operation can be a named function that calls smaller functions in a clear sequence.
- Pass required data as explicit inputs and return useful results. Prefer pure functions: the same inputs produce the same output without changing external state.
- Avoid hidden inputs such as global state, the current time, random values, or environment settings. Read them at the boundary and pass the values in when the rule needs them.
- Avoid changing caller-owned data. Local mutation is acceptable when it is private, clear, and useful; do not force expensive copies or awkward recursion.
- Keep related functions in a small module organized by business purpose. Use one file per function only when that makes the code easier to find and use. Avoid a shared dumping ground such as a large `utils` file.
- Keep one source of truth for each rule. UI, API, CLI, and MCP adapters should call the same operation rather than copy its logic. Do not build extra adapters unless requested.

## Boundaries and side effects

Keep UI events, HTTP requests, CLI arguments, and tool calls as thin adapters:

1. Read and validate the input for that interface.
2. Call a named operation with ordinary data.
3. Translate its result or error into the interface's response.

Keep domain validation inside the shared logic so each caller gets the same rules. Adapter validation handles interface details such as parsing a request body.

Separate decisions and calculations from database, network, file, and UI operations where practical. A function that changes the DOM is still a UI function even if it has a name. Moving it into another file does not make it pure or independent of the UI.

Use explicit parameters or small injected dependencies when an operation needs external effects. Keep those dependencies narrow. Avoid a general service container or an interface for every function.

For example, the state decision is independent of the browser:

```js
// sidebar.js
export const openSidebar = (state) => ({ ...state, sidebarOpen: true });

// UI adapter; setState belongs to the UI framework.
button.onclick = () => setState(openSidebar);
```

`openSidebar` can be tested with plain state values. The small anonymous handler is acceptable: it connects the UI to the operation and contains no business rule. A different interface can reuse the operation if it needs the same state transition.

## Complex operations

Express complex business logic as an ordinary, readable sequence of small functions. Use local variables, conditionals, loops, and async calls when they make the sequence clear. Functional patterns do not require chains of `map`, `reduce`, or nested callbacks.

Separate pure calculations from effectful steps, but preserve transaction boundaries, error handling, and operation order. Do not move a read outside a transaction merely to make a function appear pure. Make failure behavior part of the operation's contract.

Extract a function when it gives a meaningful name to a rule, makes that rule independently testable, or provides useful reuse. Do not split every line into a function or add pass-through wrappers without a purpose.

## Tests

- Give each business function one focused test group. This means one home for its behavior tests, not exactly one test case or assertion.
- Include normal inputs, meaningful boundary cases, and expected failures. Use table-driven cases when several inputs exercise the same rule.
- Test returned values and observable effects. Do not mirror the implementation or assert internal call order unless that order is part of the required behavior.
- Test small business functions directly. Test the composed operation as well: verify how results are combined and how meaningful failures are handled. Do not repeat every small-function case in the composition tests.
- Keep the default unit suite fast and self-contained. Use ordinary values and small in-memory fakes for external dependencies. Do not require a live database, network, credentials, or real-time sleeps for unit tests.
- Use fixed time and controlled randomness where needed. Prefer real pure helpers over mocks of those helpers.
- Follow the project's test framework and test layout. Do not expose private helpers solely to test them; verify incidental helpers through the business function they support.
- Keep integration and end-to-end tests where they verify wiring, persistence, framework behavior, or complete user flows. Isolate slow or external tests from fast unit tests using the project's conventions.
- Passing tests for individual functions does not prove that the whole app works. Test important connections and workflows too.

## Finish the task

Check that business logic has a clear home, adapters remain thin, and side effects are visible. Run the relevant tests and report what was checked and any limits. For performance work, measure before optimizing and retain tests for observable behavior.
