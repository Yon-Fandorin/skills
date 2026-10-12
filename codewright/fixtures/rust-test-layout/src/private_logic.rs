fn secret(value: i32) -> i32 {
    value * 2
}

pub fn public_contract(value: i32) -> i32 {
    secret(value)
}

#[cfg(test)]
mod tests;
