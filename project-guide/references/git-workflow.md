# Git workflow

Apply when the target project actually uses Git. Respect its hosting service
and existing contribution conventions; Git does not imply GitHub or hosted CI.

## Pull requests

Create PRs only when the task authorizes creation, and always create them as
drafts. For GitHub CLI, use `gh pr create --draft`; see the
[creation command](https://cli.github.com/manual/gh_pr_create). Verify the
created PR's draft state with its base, head, and change scope. If the host
cannot create a draft, report the limitation rather than create a ready PR.

Keep the PR in draft until the user explicitly requests promotion. Passing
checks or a clean review does not authorize marking it ready or merging it.
For title and body work, use `pr-writer` when available and preserve the existing
template and evidence requirements.

## CI/CD opt-in

Add, enable, or expand CI/CD only within explicit user authorization. This
includes setup instructions, workflow/configuration files, provider integration,
scheduled automation, and deployment automation. An uncommitted workflow file
is still a setup change. A general request to improve the project, implement a
feature, or create a PR is not CI/CD authorization.

Treat suggestions from implementation or independent review as proposals, not
permission to configure CI/CD. Before an unapproved setup or expansion, explain
the proposed scope, triggers, and possible hosted-run or quota impact and obtain
the user's decision. Reuse approval already given for that scope; do not ask
again for the same authorization.

Preserve existing automation and follow the task's authorization for its use.
Reading configuration or logs and running permitted local checks do not require
new CI/CD setup approval. Starting extra hosted runs or changing existing CI/CD
configuration requires explicit authorization for those operations; do not
disable or replace existing workflows to avoid this boundary.

Without CI/CD authorization, finish the independently authorized work using
available checks and report any verification gaps. If a required check cannot
be completed, retain it as incomplete rather than inventing a passing result or
silently adding automation.
