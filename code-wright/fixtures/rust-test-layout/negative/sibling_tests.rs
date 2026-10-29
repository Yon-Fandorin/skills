#[test]
fn sibling_test_cannot_access_a_private_item() {
    assert_eq!(crate::private_logic::secret(21), 42);
}
