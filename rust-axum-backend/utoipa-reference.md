# utoipa OpenAPI Reference

Reference for generating OpenAPI documentation in Rust Axum backends using utoipa 5.4+.

---

## Setup

```toml
[dependencies]
utoipa = { version = "5.4", features = ["axum_extras"] }
utoipa-axum = "0.2"
utoipa-swagger-ui = { version = "9.0", features = ["axum"] }
```

The `axum_extras` feature enables automatic parameter extraction from axum handler arguments.

```rust
use utoipa::{OpenApi, ToSchema, IntoParams};
use utoipa_axum::{router::OpenApiRouter, routes};
use utoipa_swagger_ui::SwaggerUi;
```

---

## ToSchema Derive

```rust
#[derive(Serialize, Deserialize, ToSchema)]
#[schema(title = "CreateUserRequest")]
pub struct CreateUserRequest {
    /// The user's display name
    #[schema(example = "Alice", min_length = 1, max_length = 100)]
    pub name: String,
    #[schema(example = "alice@example.com", format = "email")]
    pub email: String,
    #[schema(example = 25, minimum = 0, maximum = 150)]
    pub age: Option<u32>,
    #[schema(default = "user")]
    pub role: String,
}
```

Doc comments on structs/fields become descriptions in the OpenAPI output.

### Key `#[schema(...)]` Attributes

| Attribute    | Purpose                                   | Example                 |
|--------------|-------------------------------------------|-------------------------|
| `example`    | Example value for the field               | `example = "Alice"`     |
| `title`      | Display name (container-level)            | `title = "UserRequest"` |
| `min_length` | Minimum string length                     | `min_length = 1`        |
| `max_length` | Maximum string length                     | `max_length = 255`      |
| `minimum`    | Minimum numeric value                     | `minimum = 0`           |
| `maximum`    | Maximum numeric value                     | `maximum = 150`         |
| `format`     | OpenAPI format string                     | `format = "email"`      |
| `value_type` | Override the inferred type                | `value_type = String`   |
| `default`    | Default value                             | `default = "active"`    |
| `inline`     | Inline schema instead of `$ref`           | `inline`                |
| `nullable`   | Mark field as nullable                    | `nullable`              |
| `bound`      | Override generic trait bounds              | `bound = "T: ToSchema"` |
| `as`         | Custom schema path name                   | `as = api::MyType`      |

### value_type for External Types

```rust
#[derive(Serialize, Deserialize, ToSchema)]
pub struct Event {
    #[schema(value_type = String, format = "date-time")]
    pub created_at: chrono::NaiveDateTime,
    #[schema(value_type = String, format = "uuid")]
    pub id: uuid::Uuid,
}
```

### Enum Schemas

```rust
// Plain enum -> string schema with allowed values
#[derive(Serialize, Deserialize, ToSchema)]
#[serde(rename_all = "snake_case")]
pub enum UserRole { Admin, Moderator, User }

// Tagged enum -> polymorphic schema
#[derive(Serialize, Deserialize, ToSchema)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum Notification {
    Email { subject: String, body: String },
    Sms { phone: String, message: String },
}

// Repr enum -> integer schema
#[derive(Serialize, Deserialize, ToSchema)]
#[repr(u8)]
pub enum Priority { Low = 1, Medium = 2, High = 3 }
```

---

## IntoParams Derive

```rust
#[derive(Deserialize, IntoParams)]
#[into_params(parameter_in = Query)]
pub struct ListUsersParams {
    #[param(minimum = 1, example = 1)]
    pub page: Option<u32>,
    #[param(minimum = 1, maximum = 100, example = 20)]
    pub per_page: Option<u32>,
    #[param(min_length = 1, example = "alice")]
    pub search: Option<String>,
}
```

Use in handler annotations with `params(ListUsersParams)`. Key `#[param(...)]` attributes: `example`, `minimum`, `maximum`, `min_length`, `max_length`, `pattern`, `nullable`, `required`, `value_type`, `ignore`.

---

## #[utoipa::path] Macro

### Complete Attribute Reference

```rust
#[utoipa::path(
    get,                              // post, put, patch, delete, head, options, trace
    path = "/users/{id}",
    tag = "users",
    operation_id = "getUserById",     // defaults to function name
    context_path = "/api/v1",         // prepended to path
    summary = "Get a user by ID",     // or use first doc comment line
    description = "Detailed docs.",   // or use remaining doc comment lines
    params(
        ("id" = u64, Path, description = "User ID"),
        ListUsersParams,              // struct-based and inline can be mixed
    ),
    request_body = CreateUserRequest,
    responses(
        (status = 200, description = "User found", body = UserResponse),
        (status = 404, description = "Not found", body = ErrorResponse),
    ),
    security(("bearer" = [])),
)]
async fn get_user(Path(id): Path<u64>) -> Result<UserResponse, ServiceError> { /* ... */ }
```

### Request Body Variants

```rust
request_body = CreateUserRequest
request_body(content = CreateUserRequest, description = "The user to create")
request_body(content = inline(CreateUserRequest))  // inline schema, no $ref
```

### Response Variants

```rust
responses(
    (status = 200, description = "Success", body = UserResponse),
    (status = 200, description = "List", body = [User]),     // array response
    (status = 204, description = "Deleted", body = EmptyResponse),
    (status = 400, description = "Error", body = ErrorResponse),
)
```

### Security Variants

```rust
security(("bearer" = []))                              // require bearer
security(("oauth2" = ["read:users", "write:users"]))   // require scopes
security(("bearer" = []), ("api_key" = []))             // any one suffices
security(())                                            // no security (override global)
```

### Doc Comment Convention

First doc comment line becomes `summary`. Remaining lines become `description`.

---

## OpenApi Derive

```rust
#[derive(OpenApi)]
#[openapi(
    tags(
        (name = "users", description = "User management"),
        (name = "products", description = "Product catalog"),
    ),
    modifiers(&SecurityAddon),
    servers(
        (url = "http://localhost:3000", description = "Local"),
        (url = "https://api.example.com", description = "Production"),
    ),
    // Manual schema registration -- usually NOT needed with OpenApiRouter
    // components(schemas(User, Product)),
    // security(("bearer" = [])),   // global security requirement
)]
struct ApiDoc;
```

### Security Modifier (Modify Trait)

```rust
use utoipa::openapi::security::{HttpAuthScheme, HttpBuilder, SecurityScheme};
use utoipa::Modify;

struct SecurityAddon;

impl Modify for SecurityAddon {
    fn modify(&self, openapi: &mut utoipa::openapi::OpenApi) {
        if let Some(components) = openapi.components.as_mut() {
            components.add_security_scheme(
                "bearer",
                SecurityScheme::Http(
                    HttpBuilder::new()
                        .scheme(HttpAuthScheme::Bearer)
                        .bearer_format("JWT")
                        .build(),
                ),
            );
        }
    }
}
```

When using `OpenApiRouter` with `routes!`, you typically do NOT need to list schemas or paths manually. The router collects them automatically from handler annotations.

---

## OpenApiRouter

### Basic Construction and routes! Grouping

```rust
let (router, api) = OpenApiRouter::with_openapi(ApiDoc::openapi())
    .routes(routes!(list_users, create_user))   // same path, different methods
    .routes(routes!(get_user, update_user))      // same path, different methods
    .split_for_parts();
```

**Critical rule:** handlers in one `routes!()` call must share the **same path** but use different HTTP methods. Different paths require separate `.routes()` calls.

### Router Nesting

Handler `path` values should be relative to the nest prefix (use `"/"` and `"/{id}"`, not full paths):

```rust
fn user_routes() -> OpenApiRouter {
    OpenApiRouter::new()
        .routes(routes!(list_users, create_user))   // path = "/"
        .routes(routes!(get_user, update_user))      // path = "/{id}"
}

let (router, api) = OpenApiRouter::with_openapi(ApiDoc::openapi())
    .nest("/api/v1/users", user_routes())
    .split_for_parts();
```

`.split_for_parts()` returns `(axum::Router, utoipa::openapi::OpenApi)`.

### Multi-Domain Router Aggregation

In production, each domain module returns its own `(Router, Vec<OpenApi>)`. Only API-key
(v1) endpoints use `OpenApiRouter` — user-facing endpoints use plain `Router` without OpenAPI.

```rust
// api/user/v1.rs — returns path + router + OpenApi spec
pub fn router(app_state: Arc<AppState>) -> (&'static str, Router, utoipa::openapi::OpenApi) {
    let (router, api) = OpenApiRouter::with_openapi(V1Api::openapi())
        .routes(routes!(v1_list_users))
        .routes(routes!(v1_get_user))
        .split_for_parts();

    (
        "/api/v1/users",
        router
            .layer(middleware::from_fn_with_state(app_state.clone(), api_key::required))
            .with_state(app_state),
        api,
    )
}

// api/user/mod.rs — aggregates sub-routers, collects OpenApi specs
pub fn router(app_state: Arc<AppState>) -> (Router, Vec<utoipa::openapi::OpenApi>) {
    let (v1_path, v1_router, v1_api) = v1::router(app_state.clone());
    (
        Router::new()
            .nest("/api/users", user::router(app_state))   // plain Router (no OpenAPI)
            .nest(v1_path, v1_router),                      // v1 with OpenAPI
        vec![v1_api],
    )
}

// api/mod.rs — merges all domains + Swagger UI via serve()

/// Ergonomic macro: calls domain router, merges OpenApi specs into accumulator
macro_rules! router_with_openapi {
    ($router:ident, $state:expr, $openapi:expr) => {{
        let (router, apis) = $router::router(Arc::clone($state));
        apis.into_iter().for_each(|api| $openapi.merge(api));
        router
    }};
}

pub async fn serve(state: Arc<AppState>) {
    let mut openapi = openapi::Doc::openapi();   // base spec from openapi.rs

    let app = Router::new()
        .route("/health", get(health_handler))
        // domains WITH OpenAPI (v1 endpoints) — use macro
        .merge(router_with_openapi!(user, &state, openapi))
        // domains WITHOUT OpenAPI — plain merge
        .merge(genre::router(Arc::clone(&state)))
        .merge(SwaggerUi::new("/api/docs").url("/api/docs/openapi.json", openapi))
        .layer(middleware::from_fn_with_state(Arc::clone(&state), auth_middleware::base));

    let listener = TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
}
```

Key points:
- **`v1.rs`** owns its path constant and returns `(&str, Router, OpenApi)` — self-contained
- **Domain `mod.rs`** collects specs into `Vec<OpenApi>` — each domain may have 0+ specs
- **`router_with_openapi!` macro** — calls domain router, merges specs, returns just `Router`
- **`serve()` function** — owns full server lifecycle (state, middleware, Swagger UI, graceful shutdown)
- Mixed domains: some use the macro (have OpenAPI), others use plain `.merge()` (no OpenAPI)
- Only v1 endpoints appear in Swagger UI — user-facing endpoints stay undocumented

See **examples.md Example 8** for the full implementation.

---

## Swagger UI Integration

```rust
let app = Router::new()
    .merge(router)
    .merge(SwaggerUi::new("/swagger-ui").url("/api-docs/openapi.json", api));
```

`SwaggerUi::new(path)` sets the UI base path. `.url(json_path, spec)` registers the OpenAPI JSON endpoint. `SwaggerUi` implements `Into<Router>` for direct merging.

---

## Response & Error Type System

The types below form shared infrastructure used across all handlers. In a real project,
they live in `common/response.rs` (Meta, EmptyResponse, define_response!) and `errors.rs`
(ErrorCode, ServiceError, ErrorResponse, define_error_codes!, error macros).

### Meta

Response metadata — included in both success and error responses.

```rust
use chrono::{DateTime, Utc};
use serde::Serialize;
use utoipa::ToSchema;

#[derive(Debug, Serialize, ToSchema)]
pub struct Meta {
    pub timestamp: DateTime<Utc>,
    #[schema(examples(json!(env!("CARGO_PKG_VERSION"))))]
    pub version: &'static str,
}

impl Meta {
    pub fn new() -> Self {
        Self { timestamp: Utc::now(), version: env!("CARGO_PKG_VERSION") }
    }
}
```

### EmptyResponse

For 204 No Content — includes `meta` but no `data` field.

```rust
#[derive(Serialize, ToSchema)]
pub struct EmptyResponse {
    #[serde(skip)]
    #[schema(ignore)]
    pub http_status: axum::http::StatusCode,
    pub meta: Meta,
}

impl axum::response::IntoResponse for EmptyResponse {
    fn into_response(self) -> axum::response::Response {
        (self.http_status, axum::Json(self)).into_response()
    }
}
```

### define_response! Macro

Generates concrete response types with clean schema names, embedded HTTP status, `Meta`,
and `IntoResponse` implementation. Handlers return the type directly — no `Json` wrapper needed.

```rust
#[macro_export]
macro_rules! define_response {
    ($name:ident, $data_type:ty) => {
        #[derive(serde::Serialize, utoipa::ToSchema)]
        pub struct $name {
            #[serde(skip)]
            #[schema(ignore)]
            pub http_status: axum::http::StatusCode,
            pub data: $data_type,
            pub meta: $crate::api::dto::Meta,
        }

        impl $name {
            pub fn new(http_status: axum::http::StatusCode, data: $data_type) -> Self {
                Self { http_status, data, meta: $crate::api::dto::Meta::new() }
            }
            #[allow(unused)]
            pub fn ok(data: $data_type) -> Self {
                Self::new(axum::http::StatusCode::OK, data)
            }
            #[allow(unused)]
            pub fn created(data: $data_type) -> Self {
                Self::new(axum::http::StatusCode::CREATED, data)
            }
            #[allow(unused)]
            pub fn no_content() -> $crate::api::dto::EmptyResponse {
                $crate::api::dto::EmptyResponse {
                    http_status: axum::http::StatusCode::NO_CONTENT,
                    meta: $crate::api::dto::Meta::new(),
                }
            }
        }

        impl axum::response::IntoResponse for $name {
            fn into_response(self) -> axum::response::Response {
                (self.http_status, axum::Json(self)).into_response()
            }
        }
    };
}
```

Key design points:
- **`http_status`**: `#[serde(skip)]` + `#[schema(ignore)]` — stored for `IntoResponse`, invisible in JSON/OpenAPI
- **`Meta`**: timestamp + version in every response (success and error alike)
- **`IntoResponse`**: handlers return `UserResponse` directly, no `(StatusCode, Json(...))` tuple
- **`no_content()`**: returns `EmptyResponse` (no `data` field) — available on every response type

Per-domain usage:

```rust
define_response!(UserResponse, User);                      // schema: "UserResponse"
define_response!(UserListResponse, PaginatedData<User>);   // schema: "UserListResponse"
define_response!(ProductResponse, Product);                 // schema: "ProductResponse"
```

### Schema Name Comparison

| Approach | body = | Swagger Schema Name |
|----------|--------|---------------------|
| Generic (native) | `ApiResponse<User>` | `ApiResponse_User` |
| **Macro (recommended)** | `UserResponse` | `UserResponse` |
| **Macro (recommended)** | `UserListResponse` | `UserListResponse` |
| Error | `ErrorResponse` | `ErrorResponse` |
| Empty | `EmptyResponse` | `EmptyResponse` |

Schemas used in `#[utoipa::path]` responses are collected recursively when using `OpenApiRouter`
with `routes!`. You do NOT need to manually register response types in
`#[openapi(components(schemas(...)))]`.

### Alternative: Native Generics

If you prefer less boilerplate over clean names, generic `ToSchema` still works:

```rust
#[derive(Serialize, ToSchema)]
pub struct ApiResponse<T: ToSchema> {
    pub success: bool,
    pub data: T,
}
// body = ApiResponse<User> → schema name "ApiResponse_User"
```

Limitations of native generics:
- Schema names use underscore convention (`ApiResponse_PaginatedData_User`)
- Inner types are inlined (not `$ref`)
- Tuples, arrays, slices cannot be generic arguments

### ErrorCode + define_error_codes!

```rust
/// Error codes as const values — zero-cost, &'static str.
#[derive(Debug, Clone, Copy)]
pub struct ErrorCode {
    code: &'static str,
    message: &'static str,
    status: StatusCode,
}

impl ErrorCode {
    pub const fn new(code: &'static str, message: &'static str, status: StatusCode) -> Self {
        Self { code, message, status }
    }
    pub fn code(&self) -> &'static str { self.code }
    pub fn message(&self) -> &'static str { self.message }
    pub fn status(&self) -> StatusCode { self.status }

    /// Fallback: HTTP status → default error code
    pub fn from_status(status: StatusCode) -> Self {
        match status.as_u16() {
            400 => BAD_REQUEST, 401 => UNAUTHORIZED, 403 => FORBIDDEN,
            404 => NOT_FOUND, 409 => CONFLICT, _ => INTERNAL_ERROR,
        }
    }
}

/// Domain modules define error codes via macro.
#[macro_export]
macro_rules! define_error_codes {
    ($( $(#[$meta:meta])* $name:ident($status:ident, $message:literal); )*) => {
        $(
            $(#[$meta])*
            pub const $name: $crate::error::ErrorCode = $crate::error::ErrorCode::new(
                stringify!($name), $message, axum::http::StatusCode::$status,
            );
        )*
    };
}
```

Usage per module:

```rust
// src/api/user/mod.rs
crate::define_error_codes! {
    USER_NOT_FOUND(NOT_FOUND, "User not found");
    USER_ALREADY_EXISTS(CONFLICT, "User already exists");
    INVALID_EMAIL(BAD_REQUEST, "Invalid email format");
}
```

### ErrorResponse + ServiceError

```rust
/// Uniform error response — same Meta as success responses.
#[derive(Serialize, ToSchema)]
pub struct ErrorResponse {
    #[schema(value_type = String)]
    pub error_code: ErrorCode,
    pub error_message: String,
    pub meta: Meta,
}

/// Runtime error type — used in service layer and handlers.
pub struct ServiceError(pub ErrorCode, pub anyhow::Error);

impl axum::response::IntoResponse for ServiceError {
    fn into_response(self) -> axum::response::Response {
        let body = ErrorResponse {
            error_code: self.0,
            error_message: self.1.to_string(),
            meta: Meta::new(),
        };
        (self.0.status(), axum::Json(body)).into_response()
    }
}
```

`ErrorCode` serializes as its `code` string (e.g. `"USER_NOT_FOUND"`). Implement `Serialize`
manually:

```rust
impl Serialize for ErrorCode {
    fn serialize<S: serde::Serializer>(&self, s: S) -> Result<S::Ok, S::Error> {
        s.serialize_str(self.code)
    }
}
```

### Error Macros

Four macros for ergonomic error construction with automatic `tracing::error!` logging.

**Design rationale:**
- **Explicit ErrorCode**: Macros take an `ErrorCode` directly instead of mapping from HTTP
  status via `from_status()`. Error codes are pre-defined per domain with `define_error_codes!`
  and passed explicitly at the call site — this makes intent clear and enables instant
  identification of which error is returned during code review.
- **`log:` literal constraint**: When using the `log:` variant, the client-facing message is
  restricted to string literals (`"..."`). Combining format arguments (`"User {} failed", id`)
  with `log:` is not possible due to macro_rules parsing limitations, but this is leveraged as
  a **security guardrail** — using `log:` signals the intent to hide internal details, so the
  type system prevents dynamic data from accidentally leaking into client-facing messages.
- **service vs internal**: `service_error!` is for business logic errors (explicit domain
  ErrorCode), `internal_error!` is for unexpected system failures (always `INTERNAL_ERROR`).
  This separation makes error origin tracing straightforward.

**`service_error!`** — Takes an `ErrorCode` directly. 5 variants:

```rust
#[macro_export]
macro_rules! service_error {
    // ① ErrorCode + custom literal + separate log
    ($code:expr, $expose:literal, log: $($log_arg:tt)+) => {{
        tracing::error!($($log_arg)+);
        $crate::error::ServiceError($code, anyhow::anyhow!($expose))
    }};
    // ② ErrorCode + default message + separate log
    ($code:expr, log: $($log_arg:tt)+) => {{
        tracing::error!($($log_arg)+);
        $crate::error::ServiceError($code, anyhow::anyhow!($code.message()))
    }};
    // ③ ErrorCode only (default message)
    ($code:expr $(,)?) => {{
        tracing::error!("{}", $code.message());
        $crate::error::ServiceError($code, anyhow::anyhow!($code.message()))
    }};
    // ④ ErrorCode + custom literal
    ($code:expr, $msg:literal $(,)?) => {{
        tracing::error!("{}", $msg);
        $crate::error::ServiceError($code, anyhow::anyhow!($msg))
    }};
    // ⑤ ErrorCode + format string (dynamic message)
    ($code:expr, $fmt:expr, $($arg:tt)*) => {{
        tracing::error!($fmt, $($arg)*);
        $crate::error::ServiceError($code, anyhow::anyhow!($fmt, $($arg)*))
    }};
}
```

**`service_bail!`** — Identical to `service_error!` but wraps the result in `return Err(...)` for early return. Same 5 variants.

**`internal_error!`** — Always `INTERNAL_ERROR` code. No `$code` parameter. Same `log:` rule applies:

```rust
#[macro_export]
macro_rules! internal_error {
    // Custom literal + separate log
    ($expose:literal, log: $($log_arg:tt)+) => {{
        tracing::error!($($log_arg)+);
        $crate::error::ServiceError($crate::error::INTERNAL_ERROR, anyhow::anyhow!($expose))
    }};
    // Literal message
    ($msg:literal $(,)?) => {{
        tracing::error!("{}", $msg);
        $crate::error::ServiceError($crate::error::INTERNAL_ERROR, anyhow::anyhow!($msg))
    }};
    // Expression (anyhow::Error, etc.)
    ($err:expr $(,)?) => {{
        tracing::error!("{}", $err);
        $crate::error::ServiceError($crate::error::INTERNAL_ERROR, anyhow::anyhow!($err))
    }};
    // Format string
    ($fmt:expr, $($arg:tt)*) => {{
        tracing::error!($fmt, $($arg)*);
        $crate::error::ServiceError($crate::error::INTERNAL_ERROR, anyhow::anyhow!($fmt, $($arg)*))
    }};
}
```

**`internal_bail!`** — Identical to `internal_error!` but wraps the result in `return Err(...)`.

Usage:

```rust
// ── service_error! / service_bail! ──────────────────────────────────

service_error!(USER_NOT_FOUND, "No such user", log: "DB miss id={}", id) // ① custom literal + separate log
service_error!(USER_NOT_FOUND, log: "DB miss for id={}", id)            // ② default msg + separate log
service_error!(USER_NOT_FOUND)                                          // ③ default message
service_error!(USER_NOT_FOUND, "Custom static message")                 // ④ custom literal
service_error!(USER_NOT_FOUND, "User {} not found", id)                 // ⑤ dynamic message

service_bail!(INVALID_EMAIL)                                            // early return
service_bail!(USER_ALREADY_EXISTS, "Already registered", log: "dup key: {}", db_err)

// ── internal_error! / internal_bail! ────────────────────────────────

internal_error!("Something went wrong")                                 // simple message
internal_error!("Processing failed", log: "Panic in worker: {}", e)     // separate log
internal_bail!("Internal server error", log: "DB pool exhausted")       // early return
```

### Variant Summary

| # | Call form | error_message | Server log |
|---|-----------|--------------|-----------|
| ① | `service_error!(CODE, "lit", log: ...)` | custom literal | separate |
| ② | `service_error!(CODE, log: ...)` | default message | separate |
| ③ | `service_error!(CODE)` | default message | default message |
| ④ | `service_error!(CODE, "lit")` | custom literal | custom literal |
| ⑤ | `service_error!(CODE, fmt, args)` | dynamic format | dynamic format |

**When using `log:`, client message is literal-only** — prevents internal data from leaking via format arguments.

### Using Error Responses in utoipa::path

```rust
responses(
    (status = 200, body = UserResponse),
    (status = 404, body = ErrorResponse),
)
```

---

For a complete integration example combining OpenApiRouter + handlers + Swagger UI with
all the patterns above, see **examples.md Example 7**.
