use codewright_rust_test_layout::public_contract;

#[test]
fn integration_test_uses_the_public_api() {
    assert_eq!(public_contract(21), 42);
}
