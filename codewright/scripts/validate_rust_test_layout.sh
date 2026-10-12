#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "$0")/.." && pwd)"
fixture_dir="$skill_dir/fixtures/rust-test-layout"
temp_dir="$(mktemp -d "${TMPDIR:-/tmp}/codewright-rust-test-layout.XXXXXX")"
target_dir="$temp_dir/target"

cleanup() {
    rm -rf "$temp_dir"
}
trap cleanup EXIT

required_files=(
    "$fixture_dir/Cargo.toml"
    "$fixture_dir/src/lib.rs"
    "$fixture_dir/src/private_logic.rs"
    "$fixture_dir/src/private_logic/tests/mod.rs"
    "$fixture_dir/src/private_logic/tests/calculation.rs"
    "$fixture_dir/src/private_logic/tests/validation.rs"
    "$fixture_dir/tests/public_contract.rs"
    "$fixture_dir/negative/lib.rs"
    "$fixture_dir/negative/sibling_tests.rs"
)

for required_file in "${required_files[@]}"; do
    if [[ ! -f $required_file ]]; then
        printf 'missing fixture file: %s\n' "$required_file" >&2
        exit 1
    fi
done

if ! awk 'NF { previous = current; current = $0 } END { exit !(previous == "#[cfg(test)]" && current == "mod tests;") }' "$fixture_dir/src/private_logic.rs" \
    || ! grep -Fqx 'mod calculation;' "$fixture_dir/src/private_logic/tests/mod.rs" \
    || ! grep -Fqx 'mod validation;' "$fixture_dir/src/private_logic/tests/mod.rs"; then
    printf '%s\n' 'fixture does not match the documented private test-module layout' >&2
    exit 1
fi

if grep -Fq 'private_logic' "$fixture_dir/tests/public_contract.rs"; then
    printf '%s\n' 'integration fixture reaches into private implementation details' >&2
    exit 1
fi

cp -R "$fixture_dir/." "$temp_dir"

(cd "$temp_dir" && CARGO_TARGET_DIR="$target_dir" cargo test)

cp "$fixture_dir/negative/lib.rs" "$temp_dir/src/lib.rs"
cp "$fixture_dir/negative/sibling_tests.rs" "$temp_dir/src/sibling_tests.rs"

set +e
negative_output="$(cd "$temp_dir" && CARGO_TARGET_DIR="$target_dir" cargo test 2>&1)"
negative_status=$?
set -e

if [[ $negative_status -eq 0 ]] \
    || [[ $negative_output != *"E0603"* ]] \
    || [[ $negative_output != *"sibling_tests.rs"* ]] \
    || [[ $negative_output != *"private_logic::secret"* ]]; then
    printf '%s\n' "expected sibling_tests.rs to reject private_logic::secret with E0603" >&2
    printf '%s\n' "$negative_output" >&2
    exit 1
fi

printf '%s\n' "Rust test-layout fixture validated"
