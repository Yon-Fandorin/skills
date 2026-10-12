#[test]
fn public_contract_delegates_to_private_logic() {
    assert_eq!(super::super::public_contract(21), 42);
}
