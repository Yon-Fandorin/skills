# Axum 0.8.x Core Reference

API reference for Axum 0.8.x. Covers routing, extractors, responses, middleware, and setup.

**Baseline dependencies:**
```toml
axum = { version = "0.8.8", features = ["json", "macros"] }
tokio = { version = "1.49", features = ["full"] }
tower = "0.5.3"
tower-http = { version = "0.6.8", features = ["cors", "trace", "compression-gzip", "timeout"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

---

## Router

`Router` is generic over state type `S`, defaulting to `()`. `Router<S>` means the router is *missing* state of type `S`. After `.with_state(state)` the type becomes `Router<()>`.

```rust
use axum::{routing::{get, post, put, patch, delete}, Router};

let app = Router::new()
    .route("/", get(index_handler))
    .route("/users", get(list_users).post(create_user))
    .route("/users/{id}", get(get_user).put(update_user).delete(delete_user))
    .route("/users/{id}/profile", patch(patch_profile));
```

### Path Parameter Syntax (0.8.x)

Axum 0.8 uses **brace-delimited** parameters. The old colon syntax (`:param`) from 0.7 panics at startup.

```rust
// Single parameters
.route("/users/{user_id}", get(get_user))
.route("/users/{user_id}/posts/{post_id}", get(get_post))

// Wildcard — captures entire remaining path
.route("/files/{*path}", get(serve_file))

// Literal braces — escape with double braces
.route("/literal/{{braces}}", get(handler))
```

### Fallback

```rust
let app = Router::new()
    .route("/", get(index))
    .fallback(|| async { (StatusCode::NOT_FOUND, "Nothing here") });

// Handle path-matched but wrong HTTP method
let app = Router::new()
    .route("/users", get(list_users))
    .method_not_allowed_fallback(|| async { (StatusCode::METHOD_NOT_ALLOWED, "Not supported") });
```

### Providing State

```rust
use std::sync::Arc;

struct AppState { db: DatabasePool }

let shared_state = Arc::new(AppState { db: pool });
let app = Router::new()
    .route("/users", get(list_users))
    .with_state(shared_state);  // Router<Arc<AppState>> -> Router<()>
```

---

## Route Composition

### merge() — Flat Combination

Combines two routers at the same level. Both must have the same state type.

```rust
let user_routes = Router::new()
    .route("/users", get(list_users))
    .route("/users/{id}", get(get_user));
let post_routes = Router::new()
    .route("/posts", get(list_posts))
    .route("/posts/{id}", get(get_post));

let app = Router::new().merge(user_routes).merge(post_routes).with_state(state);
```

### nest() — Path Prefixing

Mounts a child router under a prefix. The prefix is stripped before the child sees the URI.

```rust
let user_routes = Router::new()
    .route("/", get(list_users).post(create_user))       // /api/users
    .route("/{id}", get(get_user).delete(delete_user));   // /api/users/{id}

let app = Router::new().nest("/api/users", user_routes).with_state(state);
```

### Module-Based Router Pattern

```rust
// src/routes/users.rs
pub fn router() -> Router<Arc<AppState>> {
    Router::new()
        .route("/", get(list_users).post(create_user))
        .route("/{id}", get(get_user).put(update_user).delete(delete_user))
}

// src/main.rs
let app = Router::new()
    .nest("/api/users", routes::users::router())
    .nest("/api/posts", routes::posts::router())
    .with_state(shared_state);
```

---

## Handlers

Async functions taking extractors, returning `impl IntoResponse`.

```rust
async fn index() -> &'static str { "Hello, World!" }

async fn get_user(Path(id): Path<u64>) -> Json<User> { /* ... */ }

async fn create_user(
    State(state): State<Arc<AppState>>,
    Json(payload): Json<CreateUser>,
) -> (StatusCode, Json<User>) { /* ... */ }
```

### Extractor Ordering Rules

`FromRequestParts` extractors (non-body) go in any order. The **one** `FromRequest` extractor (body-consuming) **must be last**.

```rust
// CORRECT: body-consuming Json is last
async fn handler(
    State(state): State<Arc<AppState>>,  // FromRequestParts
    Path(id): Path<u64>,                  // FromRequestParts
    Query(params): Query<ListParams>,     // FromRequestParts
    Json(body): Json<UpdateUser>,         // FromRequest — MUST be last
) -> impl IntoResponse { /* ... */ }
```

### Closure Handlers

```rust
let app = Router::new()
    .route("/", get(|| async { "Hello" }))
    .route("/config", get({
        let val = config.name.clone();
        move || async move { val }
    }));
```

---

## Extractors (FromRequestParts)

Read request metadata without consuming the body. Multiple allowed in any order.

### Path\<T\>

```rust
use axum::extract::Path;

async fn get_user(Path(user_id): Path<u64>) -> impl IntoResponse {
    format!("User {user_id}")
}

// Tuple for multiple params
async fn get_post(Path((uid, pid)): Path<(u64, u64)>) -> impl IntoResponse {
    format!("User {uid}, Post {pid}")
}
// Route: .route("/users/{uid}/posts/{pid}", get(get_post))

// Struct for named params
#[derive(Deserialize)]
struct PostPath { user_id: u64, post_id: u64 }
async fn get_post_v2(Path(p): Path<PostPath>) -> impl IntoResponse {
    format!("User {}, Post {}", p.user_id, p.post_id)
}
```

### Query\<T\>

```rust
use axum::extract::Query;

#[derive(Deserialize)]
struct Pagination { page: Option<u32>, per_page: Option<u32> }

// GET /users?page=2&per_page=10
async fn list_users(Query(p): Query<Pagination>) -> impl IntoResponse {
    let page = p.page.unwrap_or(1);
    format!("Page {page}")
}
```

### State\<T\>

State is cloned per extraction — wrap in `Arc` for non-trivial state.

```rust
use axum::extract::State;
use std::sync::Arc;

struct AppState { db: DatabasePool, config: AppConfig }

async fn list_users(State(state): State<Arc<AppState>>) -> impl IntoResponse {
    let users = state.db.fetch_users().await;
    Json(users)
}
```

### HeaderMap

```rust
use axum::http::HeaderMap;

async fn read_headers(headers: HeaderMap) -> impl IntoResponse {
    let ua = headers.get("user-agent").and_then(|v| v.to_str().ok()).unwrap_or("unknown");
    format!("User-Agent: {ua}")
}
```

### Extension\<T\>

Extracts from request extensions (typically set by middleware).

```rust
use axum::Extension;

#[derive(Clone)]
struct CurrentUser { id: u64, name: String }

async fn profile(Extension(user): Extension<CurrentUser>) -> impl IntoResponse {
    format!("Hello, {}", user.name)
}
```

### ConnectInfo\<T\>

Requires `into_make_service_with_connect_info` at serve time.

```rust
use axum::extract::ConnectInfo;
use std::net::SocketAddr;

async fn handler(ConnectInfo(addr): ConnectInfo<SocketAddr>) -> impl IntoResponse {
    format!("Client IP: {}", addr.ip())
}
```

### MatchedPath

The inner field is `pub(crate)` — use `.as_str()` instead of destructuring.

```rust
use axum::extract::MatchedPath;

async fn handler(path: MatchedPath) -> impl IntoResponse {
    format!("Matched route: {}", path.as_str())  // e.g. "/users/{id}"
}
```

---

## Extractors (FromRequest)

Consume the request body. Only **one** per handler, **must be last**.

### Json\<T\>

Requires `Content-Type: application/json`. `T: Deserialize`.

```rust
use axum::Json;

#[derive(Deserialize)]
struct CreateUser { name: String, email: String }

async fn create_user(Json(payload): Json<CreateUser>) -> (StatusCode, Json<User>) {
    let user = User { id: 1, name: payload.name, email: payload.email };
    (StatusCode::CREATED, Json(user))
}
```

### Form\<T\>

Expects `Content-Type: application/x-www-form-urlencoded`. `T: Deserialize`.

```rust
use axum::Form;

#[derive(Deserialize)]
struct LoginForm { username: String, password: String }

async fn login(Form(input): Form<LoginForm>) -> impl IntoResponse {
    format!("Logging in as {}", input.username)
}
```

### Multipart

For `multipart/form-data` (file uploads).

```rust
use axum::extract::Multipart;

async fn upload(mut multipart: Multipart) -> impl IntoResponse {
    while let Some(field) = multipart.next_field().await.unwrap() {
        let name = field.name().unwrap_or("unknown").to_string();
        let data = field.bytes().await.unwrap();
        tracing::info!("Field '{}': {} bytes", name, data.len());
    }
    StatusCode::OK
}
```

### Bytes / String

```rust
use axum::body::Bytes;

async fn raw_body(body: Bytes) -> impl IntoResponse { format!("{} bytes", body.len()) }
async fn text_body(body: String) -> impl IntoResponse { format!("Body: {body}") }
```

---

## Optional Extraction

Wrap in `Option<T>`. Returns `None` when data is absent, but **rejects if present and malformed** (Axum 0.8 `OptionalFromRequestParts` / `OptionalFromRequest` traits).

```rust
// None if no query string; error if malformed
async fn search(params: Option<Query<SearchParams>>) -> impl IntoResponse {
    match params {
        Some(Query(s)) => format!("Searching: {}", s.q),
        None => "No search query".to_string(),
    }
}

// Optional JSON body
async fn maybe_json(body: Option<Json<CreateUser>>) -> impl IntoResponse {
    match body {
        Some(Json(user)) => format!("Got user: {}", user.name),
        None => "No body".to_string(),
    }
}
```

---

## Response Types

Any type implementing `IntoResponse` can be returned from a handler.

### Common Types

```rust
use axum::{http::StatusCode, response::{Html, IntoResponse, Json, Redirect}};

async fn plain() -> &'static str { "Hello" }                           // text/plain
async fn no_content() -> StatusCode { StatusCode::NO_CONTENT }          // empty body
async fn json() -> Json<serde_json::Value> { Json(serde_json::json!({"ok": true})) }
async fn html() -> Html<&'static str> { Html("<h1>Hello</h1>") }       // text/html
async fn redirect() -> Redirect { Redirect::to("/login") }             // 303
// Also: Redirect::permanent(), Redirect::temporary()
```

### Tuple Responses

Form: `(StatusCode, T1, ..., Tn, Body)` where `T`s implement `IntoResponseParts`.

```rust
async fn created() -> (StatusCode, Json<User>) {
    (StatusCode::CREATED, Json(user))
}
async fn not_found() -> (StatusCode, &'static str) {
    (StatusCode::NOT_FOUND, "Resource not found")
}
async fn with_headers() -> (StatusCode, [(header::HeaderName, &'static str); 1], Json<Data>) {
    (StatusCode::OK, [(header::CACHE_CONTROL, "max-age=3600")], Json(data))
}
async fn custom_header() -> ([(&'static str, &'static str); 1], &'static str) {
    ([("x-request-id", "abc-123")], "Hello")
}
```

### Result\<T, E\> and Custom IntoResponse

Both `T` and `E` must implement `IntoResponse`.

```rust
async fn get_user(Path(id): Path<u64>) -> Result<Json<User>, StatusCode> {
    find_user(id).ok_or(StatusCode::NOT_FOUND).map(Json)
}

// Custom error type
enum ApiError { NotFound(String), Internal(String), BadRequest(String) }

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let (status, msg) = match self {
            ApiError::NotFound(m) => (StatusCode::NOT_FOUND, m),
            ApiError::Internal(m) => (StatusCode::INTERNAL_SERVER_ERROR, m),
            ApiError::BadRequest(m) => (StatusCode::BAD_REQUEST, m),
        };
        (status, Json(serde_json::json!({ "error": msg }))).into_response()
    }
}

async fn get_user(Path(id): Path<u64>) -> Result<Json<User>, ApiError> {
    let user = find_user(id)
        .map_err(|e| ApiError::Internal(e.to_string()))?
        .ok_or_else(|| ApiError::NotFound(format!("User {id} not found")))?;
    Ok(Json(user))
}
```

---

## Middleware

### from_fn

Signature: zero+ `FromRequestParts` extractors, then `Request`, then `Next`. Returns `impl IntoResponse`. Must call `next.run(request).await`.

```rust
use axum::{extract::Request, middleware::{self, Next}, response::Response};

async fn logging_middleware(request: Request, next: Next) -> Response {
    let method = request.method().clone();
    let uri = request.uri().clone();
    tracing::info!("{method} {uri}");
    let response = next.run(request).await;
    tracing::info!("{method} {uri} -> {}", response.status());
    response
}

let app = Router::new()
    .route("/", get(handler))
    .layer(middleware::from_fn(logging_middleware));
```

### from_fn with Extractors

```rust
async fn auth_middleware(
    headers: HeaderMap,
    request: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let token = headers.get("authorization")
        .and_then(|v| v.to_str().ok())
        .ok_or(StatusCode::UNAUTHORIZED)?;
    if !is_valid_token(token) { return Err(StatusCode::UNAUTHORIZED); }
    Ok(next.run(request).await)
}
```

### from_fn_with_state

`from_fn` does **not** support `State` extraction. Use `from_fn_with_state` instead.

```rust
async fn state_middleware(
    State(state): State<Arc<AppState>>,
    request: Request,
    next: Next,
) -> Response {
    tracing::info!("DB pool size: {}", state.db.pool_size());
    next.run(request).await
}

let app = Router::new()
    .route("/", get(handler))
    .layer(middleware::from_fn_with_state(shared_state.clone(), state_middleware))
    .with_state(shared_state);
```

### map_request / map_response

Simpler middleware — transforms request or response without `Next`.

```rust
use axum::middleware::{map_request, map_response};

async fn add_request_id(mut req: Request) -> Request {
    req.headers_mut().insert("x-request-id", uuid::Uuid::new_v4().to_string().parse().unwrap());
    req
}
async fn add_server_header(mut res: Response) -> Response {
    res.headers_mut().insert("x-server", "axum".parse().unwrap());
    res
}

let app = Router::new()
    .route("/", get(handler))
    .layer(map_request(add_request_id))
    .layer(map_response(add_server_header));
```

`map_request` can return `Result<Request, impl IntoResponse>` to short-circuit.

---

## .layer() vs .route_layer()

### .layer()

Applies to **all routes and fallback**. Every request passes through, even unmatched.

```rust
let app = Router::new()
    .route("/", get(handler))
    .fallback(fallback_handler)
    .layer(TraceLayer::new_for_http());  // traces ALL requests including 404s
```

### .route_layer()

Applies **only to matched routes**. Fallback and unmatched requests skip it.

```rust
let app = Router::new()
    .route("/api/users", get(list_users))
    .route("/api/admin", get(admin_panel))
    .route_layer(middleware::from_fn(require_auth))   // only matched routes
    .layer(TraceLayer::new_for_http())                 // everything
    .fallback(|| async { StatusCode::NOT_FOUND });     // NOT auth-wrapped
```

**Ordering:** Later layers wrap earlier ones. `TraceLayer` (added last) is outermost, runs first.

---

## Tower Common Layers

### CorsLayer

```rust
use tower_http::cors::{Any, CorsLayer};
use axum::http::{header, Method};

let cors = CorsLayer::permissive();  // development

let cors = CorsLayer::new()          // production
    .allow_origin(["https://example.com".parse().unwrap()])
    .allow_methods([Method::GET, Method::POST, Method::PUT, Method::DELETE])
    .allow_headers([header::CONTENT_TYPE, header::AUTHORIZATION])
    .allow_credentials(true)
    .max_age(std::time::Duration::from_secs(3600));
```

### TraceLayer

```rust
use tower_http::trace::TraceLayer;
let app = Router::new().route("/", get(handler)).layer(TraceLayer::new_for_http());
```

Requires tracing-subscriber initialization (see Application Setup).

### CompressionLayer

```rust
use tower_http::compression::CompressionLayer;
let app = Router::new().route("/", get(handler)).layer(CompressionLayer::new());
```

### TimeoutLayer

```rust
use tower_http::timeout::TimeoutLayer;
use std::time::Duration;
let app = Router::new().route("/", get(handler)).layer(TimeoutLayer::new(Duration::from_secs(30)));
```

### ServiceBuilder Composition

First layer = outermost middleware (runs first).

```rust
use tower::ServiceBuilder;

let app = Router::new()
    .route("/api/data", get(handler))
    .layer(
        ServiceBuilder::new()
            .layer(TraceLayer::new_for_http())
            .layer(TimeoutLayer::new(Duration::from_secs(30)))
            .layer(CompressionLayer::new())
            .layer(CorsLayer::permissive())
    );

// Or as a tuple (equivalent)
let app = Router::new()
    .route("/", get(handler))
    .layer((
        TraceLayer::new_for_http(),
        TimeoutLayer::new(Duration::from_secs(30)),
        CompressionLayer::new(),
        CorsLayer::permissive(),
    ));
```

---

## Application Setup

### Minimal Server

```rust
use axum::{routing::get, Router};
use tokio::net::TcpListener;

#[tokio::main]
async fn main() {
    let app = Router::new().route("/", get(|| async { "Hello, World!" }));
    let listener = TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

### Full Setup with Tracing and Graceful Shutdown

```rust
use axum::{routing::get, Router};
use std::sync::Arc;
use tokio::net::TcpListener;
use tokio::signal;
use tower_http::{compression::CompressionLayer, cors::CorsLayer, timeout::TimeoutLayer, trace::TraceLayer};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};
use std::time::Duration;

struct AppState { db: DatabasePool }

#[tokio::main]
async fn main() {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "app=debug,tower_http=debug,axum=trace".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    let state = Arc::new(AppState { db: create_pool().await });

    let app = Router::new()
        .nest("/api/users", routes::users::router())
        .nest("/api/posts", routes::posts::router())
        .fallback(|| async { (axum::http::StatusCode::NOT_FOUND, "Not found") })
        .layer((
            TraceLayer::new_for_http(),
            TimeoutLayer::new(Duration::from_secs(30)),
            CompressionLayer::new(),
            CorsLayer::permissive(),
        ))
        .with_state(state);

    let listener = TcpListener::bind("0.0.0.0:3000").await.unwrap();
    tracing::info!("Listening on {}", listener.local_addr().unwrap());
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
}

async fn shutdown_signal() {
    let ctrl_c = async {
        signal::ctrl_c().await.expect("failed to install Ctrl+C handler");
    };
    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("failed to install signal handler")
            .recv()
            .await;
    };
    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }
    tracing::info!("Shutdown signal received, starting graceful shutdown");
}
```

### ConnectInfo Setup

```rust
use std::net::SocketAddr;

let listener = TcpListener::bind("0.0.0.0:3000").await.unwrap();
axum::serve(listener, app.into_make_service_with_connect_info::<SocketAddr>()).await.unwrap();
```

---

## Quick Reference

| What | How |
|------|-----|
| Path param | `/{name}` in route, `Path(name): Path<String>` in handler |
| Wildcard | `/{*rest}` in route, `Path(rest): Path<String>` in handler |
| Query string | `Query(p): Query<T>` where `T: Deserialize` |
| JSON body | `Json(b): Json<T>` where `T: Deserialize` (must be last param) |
| App state | `State(s): State<Arc<AppState>>` -- provide via `.with_state()` |
| Return JSON | `Json(val)` or `(StatusCode, Json(val))` |
| Return error | `impl IntoResponse` for error type, return `Result<T, E>` |
| Add middleware | `.layer(middleware::from_fn(my_fn))` |
| State in mw | `.layer(middleware::from_fn_with_state(state, my_fn))` |
| Nest routes | `.nest("/prefix", child_router)` |
| Merge routes | `.merge(other_router)` |
| Graceful shutdown | `.with_graceful_shutdown(shutdown_signal())` |
