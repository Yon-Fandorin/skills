#[test]
fn child_test_accesses_the_owning_module_private_item() {
    assert_eq!(super::super::secret(21), 42);
}
