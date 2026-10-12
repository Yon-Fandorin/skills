# Goal

State which user or system flow should become faster and what behavior must remain unchanged.

# Baseline

State the causal bottleneck and measured baseline with its environment, workload or operation shape, and measurement scope.

# Constraints

Explain constraints that materially shaped the optimization.

# Decision

Explain the chosen optimization, why it addresses the bottleneck, and the semantic invariant that makes the rewrite safe.

# Result

Give before/after results one canonical home and compare them only when conditions and measurement scope match. Under generic repository headings, default the comparison beside the baseline and causal bottleneck; move it to validation only when it serves solely as post-change verification. Label estimates, isolated component measurements, synthetic benchmarks, and end-to-end latency explicitly. If the change affects several runtime paths, use a compact mapping or comparison table instead of repeating the paths in prose.

# Deployment Behavior

When rollout behavior depends on pre-existing state, show the meaningful states and the outcome in each one. Include recovery triggers and actions when persistent effects make them relevant. Omit this section when deployment behavior is ordinary.

# Trade-offs

Explain meaningful costs or behavior changes. Omit when none exist.

# Validation

Present how the result and behavior were established, including correctness and compatibility evidence. Do not repeat the result table; reference its evidence source and add only distinct validation facts.

# Reviewer Guide

Direct reviewers to the preserved behavior, measurement validity, deployment branches, and residual bottlenecks. Keep unrelated follow-up ideas out unless they define an explicit non-goal or remaining risk.
