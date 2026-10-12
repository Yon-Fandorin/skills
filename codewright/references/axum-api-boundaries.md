# Axum API Boundaries

Read when changing Axum handlers, extractors, middleware, request DTOs, or API
schemas. Apply alongside the Rust reference. Repository authorities and the
existing API contract override the choices below.

## Ground The Version And Contract

Inspect `Cargo.toml`, the resolved lockfile, neighboring routes, error conversion,
and request tests before choosing an API. Use docs for the installed version;
route syntax and extractor traits vary across Axum releases. A handler change
does not authorize a dependency upgrade.

Keep established status codes, error bodies, module owners, and validation
libraries. A project's custom error macro or a preference for HTTP 422 is a local
policy, not an Axum requirement.

## Extraction And Effects

The request body can be consumed once. Put its extractor last; preceding
extractors operate on request parts. For a custom extractor, choose
`FromRequestParts` or `FromRequest` from what it consumes and check the resolved
version's trait signature.

Inspect rejection handling as well as the handler body: malformed JSON or a
failed extractor can return before the handler runs. Preserve the API's intended
error mapping. Keep authentication, authorization, and required validation ahead
of the protected mutation or publication. Check the actual router and layer
composition when changing middleware order or scope.

## Nullable Updates

Before implementing a PATCH DTO, establish whether omission and explicit `null`
have different meanings. When the API supports clearing a nullable value, keep
all three states through deserialization and mutation:

| Input | Contract | Representation with a configured double option |
|-------|----------|------------------------------------------------|
| Field omitted | Leave the stored value unchanged | `None` |
| Explicit `null` | Clear the stored value | `Some(None)` |
| Supplied value | Validate and set the value | `Some(Some(value))` |

A plain `Option<T>` commonly collapses omission and null. A bare
`Option<Option<T>>` does not supply the distinction by itself. Use the repository's
existing update representation or an explicit deserializer. If a compatible
`serde_with` dependency is already in use, its `rust::double_option` adapter with
`#[serde(default, with = "serde_with::rust::double_option")]` preserves these
states. Add `skip_serializing_if = "Option::is_none"` when serializing a missing
field must omit it. Do not add a dependency solely to impose this representation
on an API that treats null differently.

Verify omitted, null, valid, and invalid inputs through the real request path and
assert the resulting stored state. For rejected input, assert that the protected
effect did not occur.

## Runtime And Schema

When the project generates OpenAPI, keep field presence, nullability, status
codes, and response shapes consistent with runtime behavior. Inspect the actual
schema output where a Serde adapter or custom extractor could change the contract;
a derive annotation alone is not evidence that it matches.

Use the repository's existing request-test seam for affected routes and
middleware. Include denial or rejection cases when the changed boundary controls
an effect, and retain successful-path coverage.

## Primary Sources

Consult only the section needed for the resolved dependency version:

- [Axum extractors](https://docs.rs/axum/latest/axum/extract/index.html) — body consumption, order, traits, and rejection handling; select the installed version.
- [Axum middleware](https://docs.rs/axum/latest/axum/middleware/index.html) — layer composition and route scope; select the installed version.
- [Serde double-option adapter](https://docs.rs/serde_with/latest/serde_with/rust/double_option/index.html) — missing/null/value behavior and adapter attributes; select the installed version.
