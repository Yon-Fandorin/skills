# Serde & Validator Reference

Comprehensive reference for serde serialization/deserialization and validator input
validation patterns in Rust Axum backends.

**Cargo.toml dependencies:**

```toml
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
serde_with = "3.16"
validator = { version = "0.20", features = ["derive"] }
axum = { version = "0.8.8", features = ["json"] }
```

---

## Serde Basics

Serde provides the `Serialize` and `Deserialize` traits via derive macros. These traits
enable automatic conversion between Rust structs/enums and data formats like JSON.

```rust
use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct User {
    pub id: i64,
    pub name: String,
    pub email: String,
    pub age: Option<u32>,
}
```

- `Serialize` generates a `serialize` method that converts the struct into a target format.
- `Deserialize` generates a `deserialize` method that constructs the struct from input data.
- Fields with `Option<T>` accept `null` or missing values during deserialization (they become `None`).
- The derive macros work on structs (named fields, tuple, unit) and enums.

---

## Container Attributes

Container attributes apply to the entire struct or enum via `#[serde(...)]`.

### rename_all

Converts all field names to a different casing convention during serialization and deserialization.

```rust
#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct CreateUserRequest {
    pub first_name: String,   // serializes as "firstName"
    pub last_name: String,    // serializes as "lastName"
    pub email_address: String, // serializes as "emailAddress"
}
```

Common values: `"camelCase"`, `"snake_case"`, `"PascalCase"`, `"SCREAMING_SNAKE_CASE"`, `"kebab-case"`.

### deny_unknown_fields

Rejects any JSON keys not present in the struct. Use this for strict request validation.

```rust
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LoginRequest {
    pub username: String,
    pub password: String,
}
// JSON with extra fields like {"username":"a","password":"b","admin":true} will error.
```

### default (container-level)

Uses `Default::default()` for all missing fields during deserialization.

```rust
#[derive(Deserialize, Default)]
#[serde(default)]
pub struct SearchParams {
    pub query: String,
    pub page: u32,
    pub per_page: u32,
    pub sort_by: String,
}

impl Default for SearchParams {
    fn default() -> Self {
        Self {
            query: String::new(),
            page: 1,
            per_page: 20,
            sort_by: "created_at".to_string(),
        }
    }
}
```

### Enum tagging variants

**Internally tagged** -- the tag lives inside the object:

```rust
#[derive(Serialize, Deserialize)]
#[serde(tag = "type")]
pub enum Event {
    Click { x: i64, y: i64 },
    KeyPress { key: String },
}
// {"type":"Click","x":10,"y":20}
```

**Adjacently tagged** -- tag and content are sibling fields:

```rust
#[derive(Serialize, Deserialize)]
#[serde(tag = "type", content = "data")]
pub enum Message {
    Text(String),
    Image { url: String, width: u32 },
}
// {"type":"Text","data":"hello"}
// {"type":"Image","data":{"url":"...","width":800}}
```

**Untagged** -- no tag at all, serde tries each variant in order:

```rust
#[derive(Serialize, Deserialize)]
#[serde(untagged)]
pub enum StringOrNumber {
    Num(f64),
    Str(String),
}
// 42.0 or "hello" -- serde attempts Num first, then Str
```

---

## Field Attributes

Field attributes apply to individual fields within a struct or enum variant.

### rename

Overrides the serialized name of a single field.

```rust
#[derive(Serialize, Deserialize)]
pub struct ApiToken {
    #[serde(rename = "accessToken")]
    pub access_token: String,

    #[serde(rename = "tokenType")]
    pub token_type: String,
}
```

### skip and skip_serializing_if

`skip` excludes a field from both serialization and deserialization. The field must implement
`Default` so serde can fill it during deserialization.

```rust
#[derive(Serialize, Deserialize)]
pub struct InternalUser {
    pub id: i64,
    pub name: String,

    #[serde(skip)]
    pub password_hash: String, // never serialized or deserialized
}
```

`skip_serializing_if` conditionally omits a field during serialization.

```rust
#[derive(Serialize, Deserialize)]
pub struct UserResponse {
    pub id: i64,
    pub name: String,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub bio: Option<String>, // omitted from JSON when None

    #[serde(skip_serializing_if = "Vec::is_empty")]
    pub tags: Vec<String>,   // omitted from JSON when empty
}
```

### default (field-level)

Provides a default when the field is missing from the input.

```rust
#[derive(Deserialize)]
pub struct Pagination {
    #[serde(default = "default_page")]
    pub page: u32,

    #[serde(default = "default_per_page")]
    pub per_page: u32,
}

fn default_page() -> u32 { 1 }
fn default_per_page() -> u32 { 20 }
```

Using `#[serde(default)]` without a function path calls `Default::default()` for that field's type.

### flatten

Inlines the fields of a nested struct into the parent.

```rust
#[derive(Serialize, Deserialize)]
pub struct Timestamps {
    pub created_at: String,
    pub updated_at: String,
}

#[derive(Serialize, Deserialize)]
pub struct Post {
    pub id: i64,
    pub title: String,

    #[serde(flatten)]
    pub timestamps: Timestamps,
}
// Serializes as {"id":1,"title":"...","created_at":"...","updated_at":"..."}
```

### with and deserialize_with

`with` specifies a module with custom `serialize` and `deserialize` functions.
`deserialize_with` specifies only a custom deserialization function.

```rust
use serde::{Deserialize, Deserializer};

#[derive(Deserialize)]
pub struct Config {
    #[serde(deserialize_with = "deserialize_non_empty_string")]
    pub name: String,
}

fn deserialize_non_empty_string<'de, D>(deserializer: D) -> Result<String, D::Error>
where
    D: Deserializer<'de>,
{
    let s = String::deserialize(deserializer)?;
    if s.trim().is_empty() {
        Err(serde::de::Error::custom("string must not be empty"))
    } else {
        Ok(s)
    }
}
```

---

## serde_with

The `serde_with` crate extends serde with additional (de)serialization helpers. The most
useful pattern for Update APIs is `double_option`, which distinguishes three states for
nullable optional fields.

### double_option -- Three-state update fields

With plain `Option<T>`, a missing field and an explicit `null` both deserialize to `None`.
`serde_with::rust::double_option` uses `Option<Option<T>>` to distinguish all three cases:

| JSON | Rust value | Meaning |
|------|-----------|---------|
| field omitted | `None` | Do not change |
| `"email": null` | `Some(None)` | Set to NULL |
| `"email": "a@b.com"` | `Some(Some("a@b.com"))` | Update value |

Apply on each nullable updatable field:

```rust
use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct UpdateUserRequest {
    pub name: Option<String>,

    #[serde(
        default,                                    // missing field → None
        skip_serializing_if = "Option::is_none",    // None → omit from output
        with = "::serde_with::rust::double_option", // enable three-state
    )]
    pub email: Option<Option<String>>,

    #[serde(
        default,
        skip_serializing_if = "Option::is_none",
        with = "::serde_with::rust::double_option",
    )]
    pub bio: Option<Option<String>>,
}
```

Key attribute combination:
- `default` — when the field is absent from JSON, serde fills `None` instead of erroring.
- `skip_serializing_if = "Option::is_none"` — omits the field when serializing `None`.
- `with = "::serde_with::rust::double_option"` — maps JSON `null` → `Some(None)` and a
  present value → `Some(Some(value))`.

### Handler matching pattern

```rust
// In the update handler:
if let Some(email) = payload.email {
    // Some(None) → set to NULL, Some(Some(v)) → set to v
    user.email = email;
}
// None → field was omitted, do nothing

// Or use explicit match for clarity:
match payload.email {
    None => { /* field omitted — no change */ }
    Some(None) => { /* explicit null — set DB column to NULL */ }
    Some(Some(value)) => { /* new value — update DB column */ }
}
```

---

## Enum Representations

Serde supports four enum representation strategies. Each produces different JSON shapes.

### Externally tagged (default)

The variant name wraps the content as a key.

```rust
#[derive(Serialize, Deserialize)]
pub enum Shape {
    Circle { radius: f64 },
    Rectangle { width: f64, height: f64 },
}
```

```json
{ "Circle": { "radius": 5.0 } }
{ "Rectangle": { "width": 10.0, "height": 20.0 } }
```

### Internally tagged

A `type` field sits inside the object alongside other fields.

```rust
#[derive(Serialize, Deserialize)]
#[serde(tag = "shape_type")]
pub enum Shape {
    Circle { radius: f64 },
    Rectangle { width: f64, height: f64 },
}
```

```json
{ "shape_type": "Circle", "radius": 5.0 }
{ "shape_type": "Rectangle", "width": 10.0, "height": 20.0 }
```

### Adjacently tagged

Tag and content live in separate sibling fields.

```rust
#[derive(Serialize, Deserialize)]
#[serde(tag = "t", content = "c")]
pub enum Shape {
    Circle { radius: f64 },
    Rectangle { width: f64, height: f64 },
}
```

```json
{ "t": "Circle", "c": { "radius": 5.0 } }
{ "t": "Rectangle", "c": { "width": 10.0, "height": 20.0 } }
```

### Untagged

No discriminator. Serde tries each variant in declaration order until one succeeds.

```rust
#[derive(Serialize, Deserialize)]
#[serde(untagged)]
pub enum Value {
    Integer(i64),
    Float(f64),
    Text(String),
    Bool(bool),
}
```

```json
42
3.14
"hello"
true
```

Warning: untagged enums produce poor error messages on failure because serde cannot
identify which variant was intended. Prefer tagged representations when possible.

---

## serde_json

The `serde_json` crate provides JSON-specific serialization and deserialization.

### Serialization and deserialization

```rust
use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct User {
    pub id: i64,
    pub name: String,
}

// Serialize to string
let user = User { id: 1, name: "Alice".to_string() };
let json_string: String = serde_json::to_string(&user).unwrap();
// => {"id":1,"name":"Alice"}

let pretty: String = serde_json::to_string_pretty(&user).unwrap();

// Deserialize from string
let parsed: User = serde_json::from_str(&json_string).unwrap();

// Serialize to bytes (Vec<u8>)
let bytes: Vec<u8> = serde_json::to_vec(&user).unwrap();

// Deserialize from byte slice
let from_bytes: User = serde_json::from_slice(&bytes).unwrap();
```

### json! macro

Builds `serde_json::Value` instances with JSON-like syntax. Useful for ad-hoc responses
and tests.

```rust
use serde_json::json;

let payload = json!({
    "status": "success",
    "data": {
        "id": 42,
        "tags": ["rust", "axum"]
    }
});

// Access fields
let id = payload["data"]["id"].as_i64().unwrap(); // 42
```

### serde_json::Value for dynamic JSON

When the schema is unknown or variable, use `serde_json::Value`.

```rust
use serde_json::Value;

fn handle_dynamic(body: String) -> Result<(), serde_json::Error> {
    let v: Value = serde_json::from_str(&body)?;

    match &v {
        Value::Object(map) => {
            for (key, val) in map {
                println!("{key}: {val}");
            }
        }
        _ => println!("Expected an object"),
    }

    Ok(())
}
```

`Value` variants: `Null`, `Bool(bool)`, `Number(Number)`, `String(String)`,
`Array(Vec<Value>)`, `Object(Map<String, Value>)`.

---

## Request/Response DTO Patterns

### Naming conventions

Use suffixed names to distinguish request and response types clearly:

- `CreateUserRequest` -- input DTO for creating a resource
- `UpdateUserRequest` -- input DTO for updating a resource (fields often optional)
- `UserResponse` -- output DTO returned to clients
- `UserListResponse` -- output DTO for list endpoints

Never reuse the same struct for both input and output. Input types derive `Deserialize`,
output types derive `Serialize`. Only derive both when genuinely needed.

### Separate input and output types

```rust
use serde::{Serialize, Deserialize};

// Input: only what the client sends
#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CreateUserRequest {
    pub name: String,
    pub email: String,
    pub password: String,
}

// Input: partial updates — Option<T> for required fields, Option<Option<T>> for nullable fields
#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct UpdateUserRequest {
    pub name: Option<String>,

    #[serde(
        default,
        skip_serializing_if = "Option::is_none",
        with = "::serde_with::rust::double_option",
    )]
    pub email: Option<Option<String>>,
}

// Handler matching:
// match payload.email {
//     None => { /* field omitted — no change */ }
//     Some(None) => { /* explicit null — set to NULL */ }
//     Some(Some(value)) => { /* update value */ }
// }

// Output: what the client receives (no password)
#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct UserResponse {
    pub id: i64,
    pub name: String,
    pub email: String,
    pub created_at: String,
}
```

### Response Envelope

For response types (`define_response!` macro, `Meta`, `EmptyResponse`, `ErrorResponse`),
see **utoipa-reference.md § Response & Error Type System**.

DTO naming conventions above still apply — the macro-generated types use those names:

```rust
define_response!(UserResponse, User);
define_response!(UserListResponse, PaginatedData<User>);
```

JSON output:

```json
{ "data": { "id": 1, "name": "Alice" }, "meta": { "timestamp": "2026-02-12T10:00:00Z", "version": "0.1.0" } }
```

### PaginatedData\<T\>

```rust
#[derive(Debug, Serialize, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct PaginatedData<T: ToSchema> {
    pub items: Vec<T>,
    pub total: u64,
    pub page: u32,
    pub per_page: u32,
}

// Usage: define_response!(UserListResponse, PaginatedData<User>);
```

---

## Validator Setup

The `validator` crate provides derive-based validation. Apply `#[derive(Validate)]` and
annotate fields with `#[validate(...)]` rules.

```rust
use validator::Validate;
use serde::Deserialize;

#[derive(Debug, Deserialize, Validate)]
pub struct CreateUserRequest {
    #[validate(length(min = 1, max = 100))]
    pub name: String,

    #[validate(email)]
    pub email: String,

    #[validate(url)]
    pub website: Option<String>,

    #[validate(length(min = 8, max = 128))]
    pub password: String,

    #[validate(must_match(other = "password"))]
    pub password_confirm: String,

    #[validate(range(min = 0, max = 150))]
    pub age: Option<u32>,
}
```

### Built-in validators

| Attribute | Description |
|---|---|
| `#[validate(email)]` | Validates email format |
| `#[validate(url)]` | Validates URL format |
| `#[validate(length(min = 1, max = 255))]` | String or collection length bounds |
| `#[validate(range(min = 0, max = 1000))]` | Numeric range bounds |
| `#[validate(must_match(other = "field_name"))]` | Two fields must be equal |
| `#[validate(regex(path = *RE))]` | Match a regex pattern |
| `#[validate(contains(pattern = "needle"))]` | String contains a substring |
| `#[validate(does_not_contain(pattern = "bad"))]` | String must not contain substring |
| `#[validate(non_control_character)]` | No control characters |
| `#[validate(nested)]` | Recursively validate a nested struct |

### Regex validation

```rust
use std::sync::LazyLock;
use regex::Regex;
use validator::Validate;
use serde::Deserialize;

static USERNAME_RE: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"^[a-zA-Z0-9_-]{3,30}$").unwrap());

#[derive(Debug, Deserialize, Validate)]
pub struct RegisterRequest {
    #[validate(regex(path = *USERNAME_RE, message = "Invalid username format"))]
    pub username: String,
}
```

### Nested validation

Use `#[validate(nested)]` to validate structs within structs.

```rust
#[derive(Debug, Deserialize, Validate)]
pub struct Address {
    #[validate(length(min = 1))]
    pub street: String,

    #[validate(length(min = 1))]
    pub city: String,
}

#[derive(Debug, Deserialize, Validate)]
pub struct CreateOrderRequest {
    #[validate(nested)]
    pub shipping_address: Address,

    #[validate(nested)]
    pub billing_address: Address,
}
```

---

## Custom Validators

Write custom validation functions when built-in validators are insufficient.

### Basic custom validator

A custom validator function takes a reference to the field value and returns
`Result<(), validator::ValidationError>`.

```rust
use validator::ValidationError;

fn validate_password_strength(password: &str) -> Result<(), ValidationError> {
    let has_uppercase = password.chars().any(|c| c.is_uppercase());
    let has_lowercase = password.chars().any(|c| c.is_lowercase());
    let has_digit = password.chars().any(|c| c.is_ascii_digit());

    if has_uppercase && has_lowercase && has_digit {
        Ok(())
    } else {
        let mut err = ValidationError::new("password_strength");
        err.message = Some(
            "Password must contain uppercase, lowercase, and a digit".into()
        );
        Err(err)
    }
}

#[derive(Debug, Deserialize, Validate)]
pub struct SetPasswordRequest {
    #[validate(length(min = 8), custom(function = "validate_password_strength"))]
    pub password: String,
}
```

### Custom validator with parameters

Add parameters to the error for richer client-side feedback.

```rust
use validator::ValidationError;

fn validate_not_reserved(username: &str) -> Result<(), ValidationError> {
    let reserved = ["admin", "root", "system", "superuser"];
    if reserved.contains(&username.to_lowercase().as_str()) {
        let mut err = ValidationError::new("reserved_username");
        err.message = Some("This username is reserved".into());
        err.add_param(std::borrow::Cow::from("value"), &username);
        Err(err)
    } else {
        Ok(())
    }
}
```

### Struct-level custom validation (schema validation)

Use `#[validate(schema(function = "..."))]` at the container level for cross-field rules.

```rust
use validator::{Validate, ValidationError, ValidationErrors};
use serde::Deserialize;

fn validate_date_range(req: &DateRangeRequest) -> Result<(), ValidationErrors> {
    if req.start_date >= req.end_date {
        let mut errors = ValidationErrors::new();
        let mut err = ValidationError::new("invalid_date_range");
        err.message = Some("start_date must be before end_date".into());
        errors.add("end_date", err);
        return Err(errors);
    }
    Ok(())
}

#[derive(Debug, Deserialize, Validate)]
#[validate(schema(function = "validate_date_range"))]
pub struct DateRangeRequest {
    pub start_date: String,
    pub end_date: String,
}
```

---

## ValidatedJson Extractor

A custom Axum extractor that deserializes JSON and runs validator checks in one step.
On failure it returns a structured 422 Unprocessable Entity response with per-field error
details.

### Full implementation

```rust
use axum::{
    async_trait,
    extract::{FromRequest, Request, rejection::JsonRejection},
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde::de::DeserializeOwned;
use serde_json::json;
use validator::Validate;

/// Extractor that deserializes JSON and validates it.
/// Produces a 422 response with field-level errors on failure.
pub struct ValidatedJson<T>(pub T);

#[derive(Debug)]
pub enum ValidatedJsonRejection {
    JsonError(JsonRejection),
    ValidationError(validator::ValidationErrors),
}

impl IntoResponse for ValidatedJsonRejection {
    fn into_response(self) -> Response {
        match self {
            ValidatedJsonRejection::JsonError(rejection) => {
                let body = json!({
                    "success": false,
                    "error": {
                        "code": "INVALID_JSON",
                        "message": rejection.body_text(),
                    }
                });
                (StatusCode::UNPROCESSABLE_ENTITY, Json(body)).into_response()
            }
            ValidatedJsonRejection::ValidationError(errors) => {
                let field_errors: serde_json::Map<String, serde_json::Value> = errors
                    .field_errors()
                    .into_iter()
                    .map(|(field, errs)| {
                        let messages: Vec<String> = errs
                            .iter()
                            .map(|e| {
                                e.message
                                    .as_ref()
                                    .map(|m| m.to_string())
                                    .unwrap_or_else(|| e.code.to_string())
                            })
                            .collect();
                        (field.to_string(), json!(messages))
                    })
                    .collect();

                let body = json!({
                    "success": false,
                    "error": {
                        "code": "VALIDATION_FAILED",
                        "message": "One or more fields failed validation",
                        "fields": field_errors,
                    }
                });
                (StatusCode::UNPROCESSABLE_ENTITY, Json(body)).into_response()
            }
        }
    }
}

#[async_trait]
impl<S, T> FromRequest<S> for ValidatedJson<T>
where
    T: DeserializeOwned + Validate,
    S: Send + Sync,
{
    type Rejection = ValidatedJsonRejection;

    async fn from_request(req: Request, state: &S) -> Result<Self, Self::Rejection> {
        let Json(value) = Json::<T>::from_request(req, state)
            .await
            .map_err(ValidatedJsonRejection::JsonError)?;

        value.validate().map_err(ValidatedJsonRejection::ValidationError)?;

        Ok(ValidatedJson(value))
    }
}
```

### Usage in handlers

```rust
use axum::{routing::post, Router};

async fn create_user(
    ValidatedJson(payload): ValidatedJson<CreateUserRequest>,
) -> impl IntoResponse {
    // payload is already deserialized AND validated here
    let response = UserResponse {
        id: 1,
        name: payload.name,
        email: payload.email,
        created_at: "2025-01-01T00:00:00Z".to_string(),
    };
    (StatusCode::CREATED, Json(response))
}

fn app() -> Router {
    Router::new()
        .route("/users", post(create_user))
}
```

### Example error response (422)

When validation fails, the response body looks like:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "One or more fields failed validation",
    "fields": {
      "email": ["email"],
      "name": ["length"],
      "password": ["length", "password_strength"]
    }
  }
}
```

Each key in `fields` is the struct field name. Each value is an array of validator codes
(or custom messages when `message` is set on the `ValidationError`).
