# Axum Examples

10 complete Axum 0.8.x examples. Each is self-contained and compilable.

## Example 1: Basic Router + Handler

**Cargo.toml**
```toml
[package]
name = "axum-basic"
version = "0.1.0"
edition = "2021"

[dependencies]
axum = { version = "0.8.8", features = ["json", "macros"] }
tokio = { version = "1.49", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

**src/main.rs**
```rust
use std::sync::Arc;
use axum::{extract::State, routing::get, Json, Router};
use serde::Serialize;
use tokio::net::TcpListener;

struct AppState { app_name: String }

#[derive(Serialize)]
struct HealthResponse { status: String, app: String }

async fn health_check(State(state): State<Arc<AppState>>) -> Json<HealthResponse> {
    Json(HealthResponse { status: "ok".into(), app: state.app_name.clone() })
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt().with_env_filter("info").init();
    let state = Arc::new(AppState { app_name: "my-api".into() });
    let app = Router::new().route("/health", get(health_check)).with_state(state);
    let listener = TcpListener::bind("0.0.0.0:3000").await.unwrap();
    tracing::info!("listening on {}", listener.local_addr().unwrap());
    axum::serve(listener, app).await.unwrap();
}
```

## Example 2: CRUD Handlers

Body-consuming extractors (`Json`) must always be the **last** parameter.

```rust
use std::sync::Arc;
use axum::{extract::{Path, Query, State}, http::StatusCode, routing::{delete, get, post, put}, Json, Router};
use serde::{Deserialize, Serialize};

struct AppState { db_url: String }
#[derive(Serialize)]
struct User { id: u64, name: String }
#[derive(Deserialize)]
struct ListParams { page: Option<u32>, per_page: Option<u32> }
#[derive(Deserialize)]
struct CreateRequest { name: String, email: String }
#[derive(Deserialize)]
struct UpdateRequest {
    name: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none", with = "::serde_with::rust::double_option")]
    email: Option<Option<String>>,
}

async fn get_user(State(_s): State<Arc<AppState>>, Path(id): Path<u64>) -> Json<User> {
    Json(User { id, name: "Alice".into() })
}
async fn list_users(State(_s): State<Arc<AppState>>, Query(p): Query<ListParams>) -> Json<Vec<User>> {
    let (_page, _per_page) = (p.page.unwrap_or(1), p.per_page.unwrap_or(20));
    Json(vec![User { id: 1, name: "Alice".into() }])
}
async fn create_user(State(_s): State<Arc<AppState>>, Json(payload): Json<CreateRequest>) -> (StatusCode, Json<User>) {
    (StatusCode::CREATED, Json(User { id: 42, name: payload.name }))
}
async fn update_user(State(_s): State<Arc<AppState>>, Path(id): Path<u64>, Json(p): Json<UpdateRequest>) -> Json<User> {
    let mut name = "unchanged".to_string();
    if let Some(n) = p.name { name = n; }
    // p.email: None → omitted, Some(None) → set null, Some(Some(v)) → update
    match p.email {
        None => { /* no change */ }
        Some(None) => { /* clear email */ }
        Some(Some(_v)) => { /* update email */ }
    }
    Json(User { id, name })
}
async fn delete_user(State(_s): State<Arc<AppState>>, Path(id): Path<u64>) -> StatusCode {
    tracing::info!("deleted user {id}");
    StatusCode::NO_CONTENT
}

fn user_router() -> Router<Arc<AppState>> {
    Router::new()
        .route("/", get(list_users).post(create_user))
        .route("/{id}", get(get_user).put(update_user).delete(delete_user))
}
```

## Example 3: Request Validation (ValidatedJson)

Custom extractor that validates the body and returns structured 422 errors.

```rust
use axum::{async_trait, extract::{rejection::JsonRejection, FromRequest, Request}, http::StatusCode, response::{IntoResponse, Response}, Json};
use serde::{de::DeserializeOwned, Deserialize, Serialize};
use validator::Validate;

pub struct ValidatedJson<T>(pub T);

#[derive(Serialize)]
struct ValidationErrorResponse { error: ValidationErrorBody }
#[derive(Serialize)]
struct ValidationErrorBody { code: String, message: String, fields: std::collections::HashMap<String, Vec<String>> }

#[async_trait]
impl<S, T> FromRequest<S> for ValidatedJson<T>
where S: Send + Sync, T: DeserializeOwned + Validate, Json<T>: FromRequest<S, Rejection = JsonRejection>,
{
    type Rejection = Response;
    async fn from_request(req: Request, state: &S) -> Result<Self, Self::Rejection> {
        let Json(value) = Json::<T>::from_request(req, state).await.map_err(|rej| {
            let body = serde_json::json!({"error": {"code": "INVALID_JSON", "message": rej.body_text()}});
            (StatusCode::UNPROCESSABLE_ENTITY, Json(body)).into_response()
        })?;
        value.validate().map_err(|errors| {
            let mut fields = std::collections::HashMap::new();
            for (field, errs) in errors.field_errors() {
                fields.insert(field.to_string(), errs.iter().filter_map(|e| e.message.as_ref().map(|m| m.to_string())).collect());
            }
            (StatusCode::UNPROCESSABLE_ENTITY, Json(ValidationErrorResponse {
                error: ValidationErrorBody { code: "VALIDATION_ERROR".into(), message: "Validation failed".into(), fields }
            })).into_response()
        })?;
        Ok(ValidatedJson(value))
    }
}

// Usage
#[derive(Deserialize, Validate)]
struct CreateUserRequest {
    #[validate(length(min = 1, max = 100, message = "Name must be 1-100 chars"))]
    name: String,
    #[validate(email(message = "Invalid email"))]
    email: String,
    #[validate(range(min = 0, max = 150, message = "Age must be 0-150"))]
    age: u8,
}

async fn create_user(ValidatedJson(p): ValidatedJson<CreateUserRequest>) -> StatusCode {
    tracing::info!("creating user: {} <{}>", p.name, p.email);
    StatusCode::CREATED
}
```

## Example 4: Unified Error Handling (ServiceError + Error Macros)

`ServiceError` wraps `ErrorCode` + `anyhow::Error`. Convenience macros handle logging
and construction. `IntoResponse` converts `ServiceError` to `ErrorResponse` JSON.

```rust
use axum::{extract::Path, http::StatusCode, response::{IntoResponse, Response}, Json};
use chrono::{DateTime, Utc};
use serde::Serialize;
use utoipa::ToSchema;

// ── Meta (shared by success + error responses) ──────────────────────

#[derive(Debug, Serialize, ToSchema)]
pub struct Meta {
    pub timestamp: DateTime<Utc>,
    pub version: &'static str,
}
impl Meta {
    pub fn new() -> Self {
        Self { timestamp: Utc::now(), version: env!("CARGO_PKG_VERSION") }
    }
}

// ── ErrorCode ───────────────────────────────────────────────────────

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
    pub fn from_status(status: StatusCode) -> Self {
        match status.as_u16() {
            400 => BAD_REQUEST, 401 => UNAUTHORIZED, 403 => FORBIDDEN,
            404 => NOT_FOUND, 409 => CONFLICT, _ => INTERNAL_ERROR,
        }
    }
}
impl Serialize for ErrorCode {
    fn serialize<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        serializer.serialize_str(self.code)
    }
}

// ── define_error_codes! ─────────────────────────────────────────────

macro_rules! define_error_codes {
    ($( $(#[$meta:meta])* $name:ident($status:ident, $message:literal); )*) => {
        $( $(#[$meta])* pub const $name: ErrorCode = ErrorCode::new(
            stringify!($name), $message, StatusCode::$status,
        ); )*
    };
}

// Global error codes
define_error_codes! {
    BAD_REQUEST(BAD_REQUEST, "Bad request");
    UNAUTHORIZED(UNAUTHORIZED, "Unauthorized");
    FORBIDDEN(FORBIDDEN, "Forbidden");
    NOT_FOUND(NOT_FOUND, "Not found");
    CONFLICT(CONFLICT, "Conflict");
    INTERNAL_ERROR(INTERNAL_SERVER_ERROR, "Internal server error");
}

// Domain error codes
define_error_codes! {
    USER_NOT_FOUND(NOT_FOUND, "User not found");
    INVALID_USER_ID(BAD_REQUEST, "Invalid user ID");
}

// ── ErrorResponse (JSON shape) ──────────────────────────────────────

#[derive(Serialize, ToSchema)]
pub struct ErrorResponse {
    #[schema(value_type = String)]
    pub error_code: ErrorCode,
    pub error_message: String,
    pub meta: Meta,
}

// ── ServiceError (runtime error type) ───────────────────────────────

pub struct ServiceError(pub ErrorCode, pub anyhow::Error);

impl IntoResponse for ServiceError {
    fn into_response(self) -> Response {
        let body = ErrorResponse {
            error_code: self.0,
            error_message: self.1.to_string(),
            meta: Meta::new(),
        };
        (self.0.status(), Json(body)).into_response()
    }
}

// ── Error macros ────────────────────────────────────────────────────
//
// Design rationale:
// - service_error!/service_bail!: Takes ErrorCode directly. No HTTP status mapping
//   (from_status) in macros — error codes are pre-defined per domain and passed
//   explicitly, making intent clear and code-reviewable.
// - log: variant: Separates client message from server log. When log: is used,
//   client message is restricted to literals only — prevents internal data (DB errors,
//   queries, etc.) from accidentally leaking to clients at the type system level.
// - internal_error!/internal_bail!: For unexpected failures with no domain error code.
//   Always INTERNAL_ERROR — exposes minimal information to clients.

/// service_error! — Takes ErrorCode directly. 5 variants.
macro_rules! service_error {
    // ① ErrorCode + custom literal + separate log
    ($code:expr, $expose:literal, log: $($log_arg:tt)+) => {{
        tracing::error!($($log_arg)+);
        ServiceError($code, anyhow::anyhow!($expose))
    }};
    // ② ErrorCode + default message + separate log
    ($code:expr, log: $($log_arg:tt)+) => {{
        tracing::error!($($log_arg)+);
        ServiceError($code, anyhow::anyhow!($code.message()))
    }};
    // ③ ErrorCode only (default message)
    ($code:expr $(,)?) => {{
        tracing::error!("{}", $code.message());
        ServiceError($code, anyhow::anyhow!($code.message()))
    }};
    // ④ ErrorCode + custom literal
    ($code:expr, $msg:literal $(,)?) => {{
        tracing::error!("{}", $msg);
        ServiceError($code, anyhow::anyhow!($msg))
    }};
    // ⑤ ErrorCode + format string (dynamic message)
    ($code:expr, $fmt:expr, $($arg:tt)*) => {{
        tracing::error!($fmt, $($arg)*);
        ServiceError($code, anyhow::anyhow!($fmt, $($arg)*))
    }};
}

/// service_bail! — same 5 variants as service_error!, but wraps in `return Err(...)`.
/// internal_error! — same pattern but hardcodes INTERNAL_ERROR instead of $code.
/// internal_bail! — INTERNAL_ERROR + return Err(...).
/// (See utoipa-reference.md § Error Macros for full source.)

// ── Handler usage ───────────────────────────────────────────────────

async fn get_user(Path(id): Path<u64>) -> Result<Json<serde_json::Value>, ServiceError> {
    // ③ Default message, early return
    if id == 0 {
        service_bail!(INVALID_USER_ID);
    }

    // ⑤ Dynamic message with ? operator
    let user = find_user(id)
        .ok_or_else(|| service_error!(USER_NOT_FOUND, "User {} not found", id))?;

    Ok(Json(user))
}

async fn create_user(Json(body): Json<serde_json::Value>) -> Result<Json<serde_json::Value>, ServiceError> {
    // ② Default message + separate log
    let name = body["name"].as_str()
        .ok_or_else(|| service_error!(BAD_REQUEST, log: "Missing 'name': {:?}", body))?;

    // ① Custom literal + separate log
    let _validated = validate_name(name)
        .map_err(|e| service_error!(BAD_REQUEST, "Invalid name format", log: "validation: {}", e))?;

    // internal_error! with log: — separate internal details
    let result = save_to_db(name).map_err(|e| {
        internal_error!("Processing failed", log: "DB insert failed: {}", e)
    })?;

    Ok(Json(result))
}

fn find_user(_id: u64) -> Option<serde_json::Value> { None }
fn validate_name(_name: &str) -> Result<(), String> { Ok(()) }
fn save_to_db(_name: &str) -> Result<serde_json::Value, String> { Ok(serde_json::json!({})) }
```

Error response shape:
```json
{ "error_code": "USER_NOT_FOUND", "error_message": "User 99 not found",
  "meta": { "timestamp": "2026-02-12T...", "version": "0.1.0" } }
```

## Example 5: Middleware -- Logging + Timing

```rust
use std::time::Instant;
use axum::{extract::Request, http::HeaderValue, middleware::{self, Next}, response::Response, routing::get, Router};
use tower::ServiceBuilder;
use tower_http::trace::TraceLayer;

async fn request_id_middleware(mut req: Request, next: Next) -> Response {
    let id = uuid::Uuid::new_v4().to_string();
    req.headers_mut().insert("x-request-id", HeaderValue::from_str(&id).unwrap());
    let mut res = next.run(req).await;
    res.headers_mut().insert("x-request-id", HeaderValue::from_str(&id).unwrap());
    res
}

async fn timing_middleware(req: Request, next: Next) -> Response {
    let start = Instant::now();
    let mut res = next.run(req).await;
    let ms = format!("{}ms", start.elapsed().as_millis());
    res.headers_mut().insert("x-response-time", HeaderValue::from_str(&ms).unwrap());
    res
}

fn build_router() -> Router {
    Router::new().route("/hello", get(|| async { "Hello!" })).layer(
        ServiceBuilder::new()
            .layer(TraceLayer::new_for_http())
            .layer(middleware::from_fn(request_id_middleware))
            .layer(middleware::from_fn(timing_middleware)),
    )
}
```

> Add `uuid = { version = "1", features = ["v4"] }` to Cargo.toml.

## Example 6: Serde Patterns -- Response Envelope with define_response!

Demonstrates `rename_all`, `skip_serializing_if`, `PaginatedData<T>`, and the `define_response!` macro pattern for clean response types.

```rust
use axum::{extract::Query, http::StatusCode};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

// ── Meta ────────────────────────────────────────────────────────────

#[derive(Debug, Serialize, ToSchema)]
pub struct Meta {
    pub timestamp: DateTime<Utc>,
    pub version: &'static str,
}
impl Meta {
    pub fn new() -> Self { Self { timestamp: Utc::now(), version: env!("CARGO_PKG_VERSION") } }
}

// ── define_response! macro ──────────────────────────────────────────

macro_rules! define_response {
    ($name:ident, $data_type:ty) => {
        #[derive(Serialize, ToSchema)]
        pub struct $name {
            #[serde(skip)]
            #[schema(ignore)]
            pub http_status: StatusCode,
            pub data: $data_type,
            pub meta: Meta,
        }
        impl $name {
            pub fn ok(data: $data_type) -> Self {
                Self { http_status: StatusCode::OK, data, meta: Meta::new() }
            }
        }
        impl axum::response::IntoResponse for $name {
            fn into_response(self) -> axum::response::Response {
                (self.http_status, axum::Json(self)).into_response()
            }
        }
    };
}

// ── Domain types (camelCase for JSON API) ───────────────────────────

#[derive(Serialize, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct PaginatedData<T: ToSchema> {
    pub items: Vec<T>,
    pub total: u64,
    pub page: u32,
    pub per_page: u32,  // serializes as "perPage"
}

#[derive(Serialize, ToSchema)]
#[serde(rename_all = "camelCase")]
struct User {
    id: u64,
    full_name: String,  // serializes as "fullName"
    email: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    bio: Option<String>, // omitted when None
}

#[derive(Deserialize)]
struct ListParams { page: Option<u32>, per_page: Option<u32> }

// ── Response types ──────────────────────────────────────────────────

define_response!(UserListResponse, PaginatedData<User>);

// ── Handler ─────────────────────────────────────────────────────────

async fn list_users(Query(p): Query<ListParams>) -> UserListResponse {
    let (page, per_page) = (p.page.unwrap_or(1), p.per_page.unwrap_or(20));
    let users = vec![User { id: 1, full_name: "Alice Smith".into(), email: "alice@example.com".into(), bio: None }];
    UserListResponse::ok(PaginatedData { total: 1, items: users, page, per_page })
}
// Response (http_status is skipped, bio omitted):
// { "data": { "items": [{"id":1,"fullName":"Alice Smith","email":"alice@example.com"}],
//   "total":1, "page":1, "perPage":20 }, "meta": { "timestamp":"...", "version":"0.1.0" } }
```

## Example 7: utoipa -- Full OpenAPI with define_response! + ErrorResponse

Uses `define_response!` macro for clean Swagger schema names, `Meta` in every response,
`EmptyResponse` for 204, and `ErrorResponse` for error cases.

```rust
use std::sync::Arc;
use axum::{extract::{Path, State}, http::StatusCode};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use tokio::net::TcpListener;
use utoipa::{OpenApi, ToSchema};
use utoipa_axum::{router::OpenApiRouter, routes};

// ── Shared infrastructure ────────────────────────────────────────────
// Meta, EmptyResponse, define_response!, ErrorCode, ServiceError,
// ErrorResponse, service_error! — see Example 4 for full implementations.
// Below are minimal definitions needed for this example to compile.

#[derive(Debug, Serialize, ToSchema)]
pub struct Meta { pub timestamp: DateTime<Utc>, pub version: &'static str }
impl Meta { pub fn new() -> Self { Self { timestamp: Utc::now(), version: env!("CARGO_PKG_VERSION") } } }

#[derive(Serialize, ToSchema)]
pub struct EmptyResponse {
    #[serde(skip)] #[schema(ignore)] pub http_status: StatusCode,
    pub meta: Meta,
}
impl axum::response::IntoResponse for EmptyResponse {
    fn into_response(self) -> axum::response::Response { (self.http_status, axum::Json(self)).into_response() }
}

macro_rules! define_response {
    ($name:ident, $data_type:ty) => {
        #[derive(Serialize, ToSchema)]
        pub struct $name {
            #[serde(skip)] #[schema(ignore)] pub http_status: StatusCode,
            pub data: $data_type, pub meta: Meta,
        }
        impl $name {
            pub fn ok(data: $data_type) -> Self { Self { http_status: StatusCode::OK, data, meta: Meta::new() } }
            pub fn created(data: $data_type) -> Self { Self { http_status: StatusCode::CREATED, data, meta: Meta::new() } }
            pub fn no_content() -> EmptyResponse { EmptyResponse { http_status: StatusCode::NO_CONTENT, meta: Meta::new() } }
        }
        impl axum::response::IntoResponse for $name {
            fn into_response(self) -> axum::response::Response { (self.http_status, axum::Json(self)).into_response() }
        }
    };
}

#[derive(Debug, Clone, Copy)]
pub struct ErrorCode { code: &'static str, message: &'static str, status: StatusCode }
impl ErrorCode {
    pub const fn new(code: &'static str, message: &'static str, status: StatusCode) -> Self { Self { code, message, status } }
    pub fn message(&self) -> &'static str { self.message }
    pub fn status(&self) -> StatusCode { self.status }
}
impl Serialize for ErrorCode {
    fn serialize<S: serde::Serializer>(&self, s: S) -> Result<S::Ok, S::Error> { s.serialize_str(self.code) }
}

#[derive(Serialize, ToSchema)]
pub struct ErrorResponse {
    #[schema(value_type = String)] pub error_code: ErrorCode,
    pub error_message: String, pub meta: Meta,
}

pub struct ServiceError(pub ErrorCode, pub anyhow::Error);
impl axum::response::IntoResponse for ServiceError {
    fn into_response(self) -> axum::response::Response {
        let body = ErrorResponse { error_code: self.0, error_message: self.1.to_string(), meta: Meta::new() };
        (self.0.status(), axum::Json(body)).into_response()
    }
}

const USER_NOT_FOUND: ErrorCode = ErrorCode::new("USER_NOT_FOUND", "User not found", StatusCode::NOT_FOUND);

macro_rules! service_error {
    ($code:expr, log: $($log_arg:tt)+) => {{ tracing::error!($($log_arg)+); ServiceError($code, anyhow::anyhow!($code.message())) }};
    ($code:expr $(,)?) => {{ tracing::error!("{}", $code.message()); ServiceError($code, anyhow::anyhow!($code.message())) }};
}

// ── Domain types ────────────────────────────────────────────────────

#[derive(Serialize, Deserialize, ToSchema)]
pub struct User {
    #[schema(example = 1)] pub id: u64,
    #[schema(example = "Alice")] pub name: String,
    #[schema(example = "alice@example.com")] pub email: String,
}

#[derive(Deserialize, ToSchema)]
pub struct CreateUserRequest {
    #[schema(example = "Alice")] pub name: String,
    #[schema(example = "alice@example.com")] pub email: String,
}

// ── Response types (clean schema names) ─────────────────────────────

define_response!(UserResponse, User);

struct AppState { db_url: String }

// ── Handlers ────────────────────────────────────────────────────────

/// Get user by ID
#[utoipa::path(get, path = "/users/{id}", tag = "users",
    params(("id" = u64, Path, description = "User ID")),
    responses((status = 200, body = UserResponse), (status = 404, body = ErrorResponse)),
    security(("bearer" = []))
)]
async fn get_user(
    State(_s): State<Arc<AppState>>, Path(id): Path<u64>,
) -> Result<UserResponse, ServiceError> {
    if id == 0 {
        return Err(service_error!(USER_NOT_FOUND, log: "Invalid lookup for id={}", id));
    }
    Ok(UserResponse::ok(User { id, name: "Alice".into(), email: "alice@example.com".into() }))
}

/// Create user
#[utoipa::path(post, path = "/users", tag = "users",
    request_body = CreateUserRequest,
    responses((status = 201, body = UserResponse), (status = 422, body = ErrorResponse)),
    security(("bearer" = []))
)]
async fn create_user(
    State(_s): State<Arc<AppState>>, axum::Json(p): axum::Json<CreateUserRequest>,
) -> UserResponse {
    UserResponse::created(User { id: 1, name: p.name, email: p.email })
}

/// Delete user (204 No Content)
#[utoipa::path(delete, path = "/users/{id}", tag = "users",
    params(("id" = u64, Path, description = "User ID")),
    responses((status = 204, body = EmptyResponse), (status = 404, body = ErrorResponse)),
    security(("bearer" = []))
)]
async fn delete_user(
    State(_s): State<Arc<AppState>>, Path(_id): Path<u64>,
) -> EmptyResponse {
    UserResponse::no_content()
}

// ── Security + Bootstrap ────────────────────────────────────────────

struct SecurityAddon;
impl utoipa::Modify for SecurityAddon {
    fn modify(&self, openapi: &mut utoipa::openapi::OpenApi) {
        let components = openapi.components.get_or_insert_with(Default::default);
        components.add_security_scheme("bearer",
            utoipa::openapi::security::SecurityScheme::Http(
                utoipa::openapi::security::Http::new(utoipa::openapi::security::HttpAuthScheme::Bearer)));
    }
}

#[derive(OpenApi)]
#[openapi(modifiers(&SecurityAddon))]
struct ApiDoc;

#[tokio::main]
async fn main() {
    let state = Arc::new(AppState { db_url: "postgres://localhost/db".into() });
    let (router, api) = OpenApiRouter::with_openapi(ApiDoc::openapi())
        .routes(routes!(get_user))
        .routes(routes!(create_user))
        .routes(routes!(delete_user))
        .split_for_parts();
    let app = axum::Router::new()
        .merge(router)
        .merge(utoipa_swagger_ui::SwaggerUi::new("/swagger-ui").url("/api-docs/openapi.json", api))
        .with_state(state);
    let listener = TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

## Example 8: api/domain Module Structure

Shows the full production router pattern: each domain module aggregates user-facing
handlers (plain `Router`) and v1 API-key handlers (`OpenApiRouter`), returning
`(Router, Vec<OpenApi>)`. The top-level `api/mod.rs` merges all domains and sets up Swagger UI.

```
src/
├── main.rs                  ├── common/response.rs
├── state.rs                 ├── common/extractor.rs
├── errors.rs                ├── api/mod.rs
├── api/user/mod.rs          ├── api/user/dto.rs
├── api/user/user.rs         ├── api/user/v1.rs
```

**src/main.rs**
```rust
use std::sync::Arc;
mod api; mod common; mod errors; mod state;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt().with_env_filter("info").init();
    let state = Arc::new(state::AppState::new().await);
    api::serve(state).await;
}
```

**src/state.rs**
```rust
pub struct AppState { pub db_url: String }
impl AppState {
    pub async fn new() -> Self { Self { db_url: "postgres://localhost/db".into() } }
}
```

**src/errors.rs** — ErrorCode + ServiceError + define_error_codes! + error macros (see Example 4).

**src/common/response.rs** — Meta + EmptyResponse + define_response! with `$crate` paths (see utoipa-reference.md § define_response!).

**src/api/user/dto.rs**
```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct CreateUserRequest { pub name: String, pub email: String }

#[derive(Serialize, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct UserDto { pub id: u64, pub name: String, pub email: String }

crate::define_response!(SingleUserResponse, UserDto);
crate::define_response!(UserListResponse, Vec<UserDto>);
```

**src/api/user/user.rs** — User-facing handlers (plain Router, no OpenAPI).
```rust
use std::sync::Arc;
use axum::{extract::{Path, State}, routing::get, Router};
use crate::errors::ServiceError;
use crate::state::AppState;
use super::dto::*;

crate::define_error_codes! {
    USER_NOT_FOUND(NOT_FOUND, "User not found");
}

pub fn router(app_state: Arc<AppState>) -> Router {
    Router::new()
        .route("/", get(list_users).post(create_user))
        .route("/{id}", get(get_user))
        .with_state(app_state)
}

async fn get_user(
    State(_s): State<Arc<AppState>>, Path(id): Path<u64>,
) -> Result<SingleUserResponse, ServiceError> {
    let user = find_user(id)
        .ok_or_else(|| crate::service_error!(USER_NOT_FOUND, "User {} not found", id))?;
    Ok(SingleUserResponse::ok(user))
}

async fn list_users(State(_s): State<Arc<AppState>>) -> UserListResponse {
    UserListResponse::ok(vec![])
}

async fn create_user(
    State(_s): State<Arc<AppState>>, axum::Json(p): axum::Json<CreateUserRequest>,
) -> SingleUserResponse {
    SingleUserResponse::created(UserDto { id: 1, name: p.name, email: p.email })
}

pub(super) fn find_user(id: u64) -> Option<UserDto> {
    (id == 42).then(|| UserDto { id, name: "Alice".into(), email: "alice@example.com".into() })
}
```

**src/api/user/v1.rs** — API-key endpoints with `OpenApiRouter`. Returns `(path, Router, OpenApi)`.
```rust
use std::sync::Arc;
use axum::{extract::{Path, State}, middleware, Router};
use utoipa::OpenApi;
use utoipa_axum::{router::OpenApiRouter, routes};
use crate::errors::ServiceError;
use crate::state::AppState;
use super::dto::*;

const USER_V1_PATH: &str = "/api/v1/users";
const USER_V1_TAG: &str = "users-v1";

#[derive(OpenApi)]
#[openapi(tags((name = USER_V1_TAG, description = "User V1 API")))]
struct V1Api;

/// List users
#[utoipa::path(get, path = "/", tag = USER_V1_TAG,
    responses((status = 200, body = UserListResponse)),
    security(("api_key" = []))
)]
async fn v1_list_users(State(_s): State<Arc<AppState>>) -> UserListResponse {
    UserListResponse::ok(vec![])
}

/// Get user by ID
#[utoipa::path(get, path = "/{id}", tag = USER_V1_TAG,
    params(("id" = u64, Path, description = "User ID")),
    responses((status = 200, body = SingleUserResponse), (status = 404, body = crate::errors::ErrorResponse)),
    security(("api_key" = []))
)]
async fn v1_get_user(
    State(_s): State<Arc<AppState>>, Path(id): Path<u64>,
) -> Result<SingleUserResponse, ServiceError> {
    let user = super::user::find_user(id)
        .ok_or_else(|| crate::service_error!(super::user::USER_NOT_FOUND))?;
    Ok(SingleUserResponse::ok(user))
}

pub fn router(app_state: Arc<AppState>) -> (&'static str, Router, utoipa::openapi::OpenApi) {
    let (router, api) = OpenApiRouter::with_openapi(V1Api::openapi())
        .routes(routes!(v1_list_users))
        .routes(routes!(v1_get_user))
        .split_for_parts();

    (
        USER_V1_PATH,
        router
            .layer(middleware::from_fn_with_state(
                app_state.clone(),
                crate::middleware::api_key::required,
            ))
            .with_state(app_state),
        api,
    )
}
```

**src/api/user/mod.rs** — Aggregates sub-routers, collects OpenAPI specs from v1.
```rust
pub mod dto;
mod user;
mod v1;

use std::sync::Arc;
use axum::Router;
use crate::state::AppState;

pub fn router(app_state: Arc<AppState>) -> (Router, Vec<utoipa::openapi::OpenApi>) {
    let (v1_path, v1_router, v1_api) = v1::router(app_state.clone());

    (
        Router::new()
            .nest("/api/users", user::router(app_state))
            .nest(v1_path, v1_router),
        vec![v1_api],
    )
}
```

**src/api/mod.rs** — Entry point. `router_with_openapi!` macro merges OpenAPI specs from
domains that return `(Router, Vec<OpenApi>)`. Domains without OpenAPI use plain `.merge()`.
```rust
mod auth_middleware;
mod openapi;
mod user;
mod genre;
mod notice;
// ... other domain modules

use std::sync::Arc;
use axum::{Extension, Router, middleware, routing::get};
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;
use crate::state::AppState;

/// Calls $router::router(state), merges collected OpenApi specs into $openapi,
/// and returns just the Router for .merge().
macro_rules! router_with_openapi {
    ($router:ident, $state:expr, $openapi:expr) => {{
        let (router, apis) = $router::router(Arc::clone($state));
        apis.into_iter().for_each(|api| $openapi.merge(api));
        router
    }};
}

pub async fn serve(state: Arc<AppState>) {
    let mut openapi = openapi::Doc::openapi();

    let app = Router::new()
        .route("/health", get(health_handler))
        // Domains WITH OpenAPI (v1 endpoints) — use macro
        .merge(router_with_openapi!(user, &state, openapi))
        // Domains WITHOUT OpenAPI — plain merge
        .merge(genre::router(Arc::clone(&state)))
        .merge(notice::router(Arc::clone(&state)))
        // Swagger UI — must come after all router_with_openapi! calls
        .merge(SwaggerUi::new("/api/docs").url("/api/docs/openapi.json", openapi))
        // Middleware stack (outermost = added last)
        .layer(middleware::from_fn_with_state(Arc::clone(&state), auth_middleware::base))
        .layer(Extension(Arc::clone(&state)));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
}

async fn health_handler() -> &'static str { "ok" }
async fn shutdown_signal() { tokio::signal::ctrl_c().await.ok(); }
```

**src/api/openapi.rs** — Base OpenAPI spec with security scheme and global config.
```rust
use utoipa::OpenApi;
use utoipa::openapi::security::{HttpAuthScheme, HttpBuilder, SecurityScheme};

struct SecurityAddon;
impl utoipa::Modify for SecurityAddon {
    fn modify(&self, openapi: &mut utoipa::openapi::OpenApi) {
        if let Some(c) = openapi.components.as_mut() {
            c.add_security_scheme("api_key",
                SecurityScheme::Http(HttpBuilder::new().scheme(HttpAuthScheme::Bearer).build()));
        }
    }
}

#[derive(OpenApi)]
#[openapi(modifiers(&SecurityAddon))]
pub struct Doc;
```

Key patterns:
- **`router_with_openapi!` macro**: Eliminates per-domain boilerplate — calls `router()`, destructures `(Router, Vec<OpenApi>)`, merges specs, returns router
- **Mixed domains**: Some domains have v1 endpoints (use macro), others don't (plain `.merge()`)
- **`serve()` function**: `api/mod.rs` owns the full server lifecycle — state, middleware, Swagger UI, graceful shutdown. `main.rs` just calls `api::serve(state).await`
- **`openapi.rs`**: Separate file for base OpenAPI spec — keeps `mod.rs` clean
- **Middleware order**: Auth → Extension → (rate limit) → CORS — outermost layer added last

Routes produced:
- `GET /health` — health check
- `GET/POST /api/users` + `GET /api/users/{id}` — user-facing (no Swagger)
- `GET /api/v1/users` + `GET /api/v1/users/{id}` — API-key (in Swagger)
- `/api/docs` — Swagger UI

## Example 9: from_fn_with_state Middleware

API key validation applied selectively with `.route_layer()`.

```rust
use std::sync::Arc;
use axum::{extract::{Request, State}, http::{HeaderMap, StatusCode}, middleware::{self, Next}, response::{IntoResponse, Response}, routing::get, Json, Router};
use serde_json::json;

struct AppState { valid_api_keys: Vec<String> }

async fn api_key_middleware(State(state): State<Arc<AppState>>, headers: HeaderMap, request: Request, next: Next) -> Response {
    let key = headers.get("x-api-key").and_then(|v| v.to_str().ok());
    match key {
        Some(k) if state.valid_api_keys.contains(&k.to_string()) => next.run(request).await,
        _ => (StatusCode::UNAUTHORIZED, Json(json!({"error": {"code": "UNAUTHORIZED", "message": "Invalid API key"}}))).into_response(),
    }
}

async fn public_health() -> &'static str { "ok" }
async fn protected_data() -> Json<serde_json::Value> { Json(json!({"secret": "treasure"})) }

fn build_router(state: Arc<AppState>) -> Router {
    let protected = Router::new()
        .route("/data", get(protected_data))
        .route_layer(middleware::from_fn_with_state(state.clone(), api_key_middleware));
    Router::new()
        .route("/health", get(public_health))
        .nest("/api", protected)
        .with_state(state)
}
// curl -H "x-api-key: valid-key" http://localhost:3000/api/data
```

## Example 10: Nested Routers with Versioned API

```rust
use std::sync::Arc;
use axum::{http::StatusCode, response::IntoResponse, routing::get, Json, Router};
use serde_json::json;
use tokio::net::TcpListener;

struct AppState { version: String }

mod users {
    use std::sync::Arc;
    use axum::{extract::{Path, State}, routing::get, Json, Router};
    use super::AppState;
    async fn list(State(_s): State<Arc<AppState>>) -> Json<serde_json::Value> {
        Json(serde_json::json!([{"id": 1, "name": "Alice"}]))
    }
    async fn show(State(_s): State<Arc<AppState>>, Path(id): Path<u64>) -> Json<serde_json::Value> {
        Json(serde_json::json!({"id": id, "name": "Alice"}))
    }
    pub fn router() -> Router<Arc<AppState>> {
        Router::new().route("/", get(list)).route("/{id}", get(show))
    }
}

mod posts {
    use std::sync::Arc;
    use axum::{routing::get, Json, Router};
    use super::AppState;
    async fn list() -> Json<serde_json::Value> {
        Json(serde_json::json!([{"id": 1, "title": "Hello World"}]))
    }
    pub fn router() -> Router<Arc<AppState>> {
        Router::new().route("/", get(list))
    }
}

async fn fallback_handler() -> impl IntoResponse {
    (StatusCode::NOT_FOUND, Json(json!({"error": {"code": "NOT_FOUND", "message": "Route not found"}})))
}

#[tokio::main]
async fn main() {
    let state = Arc::new(AppState { version: "1.0.0".into() });
    let v1 = Router::new().nest("/users", users::router()).nest("/posts", posts::router());
    let app = Router::new().nest("/api/v1", v1).fallback(fallback_handler).with_state(state);
    let listener = TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
// Routes: GET /api/v1/users, GET /api/v1/users/{id}, GET /api/v1/posts
```
