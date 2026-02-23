# Rust Style Examples

Bad → Good comparisons. References `style-guide.md` sections.

---

## 1. Import Merging (Section 1.1)

### Bad

```rust
use std::collections::HashMap;
use std::sync::Arc;
use crate::domain::user::UserService;
use crate::error::AppError;
```

### Good

```rust
use std::{collections::HashMap, sync::Arc};
use crate::{domain::user::UserService, error::AppError};
```

Same root path merged with `{}`. Ordering/grouping is left to `cargo fmt`.

---

## 2. Module Structure (Section 2.1–2.2)

### Bad

```
src/domain/user/mod.rs      // unnecessary mod.rs
src/domain/user/service.rs
```

### Good

```
src/domain/mod.rs            // pub mod user;
src/domain/user.rs           // flat file for leaf module
```

---

## 3. `pub use` Re-exports (Section 2.3)

### Bad

```rust
use my_crate::error::kinds::AppError;  // exposes internal structure
```

### Good

```rust
// error/mod.rs
mod kinds;
pub use kinds::AppError;
// Consumer: use my_crate::error::AppError;
```

---

## 4. Naming (Section 3.1–3.2)

### Bad

```rust
pub fn get_name(&self) -> &str { &self.name }
pub fn to_dto(self) -> UserDto { ... }  // consumes self but uses to_
pub fn active(&self) -> bool { ... }     // bool without is_ prefix
```

### Good

```rust
pub fn name(&self) -> &str { &self.name }       // no get_ prefix
pub fn into_dto(self) -> UserDto { ... }         // into_ for consuming
pub fn is_active(&self) -> bool { ... }          // is_ for bool
pub fn to_summary(&self) -> String { ... }       // to_ for expensive conversion
```

---

## 5. Documentation (Section 4)

### Bad

```rust
pub fn delete(&self, id: i64) -> Result<()> { ... }  // no docs
```

### Good

```rust
/// Deletes a user by ID (soft delete).
///
/// # Errors
///
/// Returns [`AppError::NotFound`] if no user exists.
pub fn delete(&self, id: i64) -> Result<()> { ... }
```

---

## 6. `let-else` (Section 5.1)

### Bad

```rust
let user = match repo.find(id).await? {
    Some(u) => u,
    None => return Err(AppError::not_found("user")),
};
```

### Good

```rust
let Some(user) = repo.find(id).await? else {
    return Err(AppError::not_found("user"));
};
```

---

## 7. Iterators vs Loops (Section 5.3)

### Bad

```rust
let mut names = Vec::new();
for u in &users {
    if u.is_active() { names.push(u.name().to_string()); }
}
```

### Good

```rust
let names: Vec<String> = users.iter()
    .filter(|u| u.is_active())
    .map(|u| u.name().to_string())
    .collect();
```

---

## 8. Error Design (Section 5.5)

### Bad

```rust
#[derive(Debug)]
pub enum Error {
    VALIDATION_ERROR(String),  // wrong naming, no thiserror
}
```

### Good

```rust
#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("validation failed: {0}")]
    Validation(String),
    #[error(transparent)]
    Internal(#[from] anyhow::Error),
}
```

Lowercase messages, no trailing period, `#[from]` for conversions.
