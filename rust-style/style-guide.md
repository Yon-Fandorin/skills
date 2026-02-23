# Rust Style Guide

Reference rules by section number (e.g., "Section 1.1").

---

## 1. `use` Declarations

**Ordering and grouping are handled by `cargo fmt` — do not manually sort or group.** This section covers only merging, which rustfmt stable cannot do.

### 1.1 Merging

Same root path → merge into one `use` with `{}`:

- `std::` → `use std::{...};`
- `crate::` → `use crate::{...};`
- `super::` → `use super::{...};`
- Same external crate → `use tokio::{sync::RwLock, time::Duration};`
- A single item may stay flat: `use anyhow::Result;`
- Use `self` for module + children: `use std::io::{self, Read, Write};`
- No glob imports except `use super::*;` in tests and `pub use crate::prelude::*;`

### 1.2 Re-exports

`pub use` goes **after** all `use`, separated by a blank line. Do not merge `use` and `pub use` into one block.

---

## 2. Module Structure

### 2.1 File-Based Modules (Rust 2018+)

Use `mod.rs` only for directories with sub-modules. Leaf modules are flat files.

```
src/
  lib.rs
  config.rs
  error.rs
  domain/
    mod.rs        // pub mod user; pub mod post;
    user.rs
    post/
      mod.rs      // sub-modules here
      service.rs
```

### 2.2 Declaration Order in `lib.rs` / `mod.rs`

```rust
pub mod config;     // 1. pub mod
pub mod error;
mod internal;       // 2. mod

pub use config::AppConfig;  // 3. pub use re-exports
pub use error::{AppError, Result};
```

### 2.3 Facade with `pub use`

Re-export to hide internal structure:

```rust
// error/mod.rs
mod kinds;
mod response;
pub use kinds::AppError;
pub use response::ErrorResponse;
// Consumers: use my_crate::error::AppError;
```

---

## 3. Naming

Based on [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/naming.html).

### 3.1 Method Prefixes

| Prefix | Meaning | Signature |
|--------|---------|-----------|
| `as_` | Cheap ref-to-ref | `&self → &T` |
| `to_` | Expensive, may allocate | `&self → T` |
| `into_` | Consumes self | `self → T` |
| `is_` / `has_` | Boolean query | `&self → bool` |
| `with_` | Builder setter | `self → Self` |
| `try_` | Fallible | `→ Result<T, E>` |
| `set_` | Imperative setter | `&mut self` |

### 3.2 Getters

No `get_` prefix — use the field name directly: `fn name(&self) -> &str`.
Exception: `get(key)` for collection-like types.

### 3.3 Enum Variants

`UpperCamelCase`. Don't repeat the enum name: `Color::Red`, not `Color::ColorRed`.

---

## 4. Documentation

### 4.1 Requirements

All `pub` items (fn, struct, enum, trait) must have `///`. Module-level `//!` is recommended.

### 4.2 Style

- Imperative mood summary ending with period: `/// Creates a new user.`
- Sections in order: `# Examples`, `# Errors`, `# Panics`, `# Safety`
- `# Safety` is **mandatory** for `unsafe fn`
- Use intra-doc links: `[`AppError`]`

```rust
/// Finds a user by ID.
///
/// # Errors
///
/// Returns [`AppError::NotFound`] if no user exists.
pub async fn find_by_id(&self, id: i64) -> Result<User> { ... }
```

---

## 5. Idiomatic Patterns

### 5.1 `let-else`

```rust
let Some(user) = repo.find(id).await? else {
    return Err(AppError::not_found("user"));
};
```

### 5.2 `matches!`

```rust
if matches!(status, Status::Active | Status::Pending) { ... }
```

### 5.3 Iterators vs Loops

Iterators for pure transformations. `for` loops when there are side effects, `await`, or `break`/`continue`.

### 5.4 `From` / `TryFrom`

Use for type conversions — enables `?` operator.

### 5.5 Error Design

```rust
#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("not found: {0}")]
    NotFound(String),
    #[error(transparent)]
    Internal(#[from] anyhow::Error),
}
```

Rules: lowercase messages, no trailing period, `#[from]` for conversions, `#[error(transparent)]` for wrapped errors.

### 5.6 `Result` Alias

```rust
pub type Result<T> = std::result::Result<T, AppError>;
```

### 5.7 Derive Order

`Debug, Clone, PartialEq, Eq, Hash, Default, Serialize, Deserialize`

---

## 6. Tooling

### 6.1 Clippy Lints

```toml
[lints.clippy]
enum_glob_use = "deny"
unwrap_used = "warn"
expect_used = "warn"
needless_pass_by_value = "warn"
redundant_closure_for_method_calls = "warn"
cloned_instead_of_copied = "warn"
flat_map_option = "warn"
manual_let_else = "warn"
too_many_arguments = "warn"

[lints.rust]
unsafe_code = "forbid"
```

### 6.2 rustfmt

See `rustfmt.toml` template in this directory. Key: `edition = "2021"`, `max_width = 100`.
