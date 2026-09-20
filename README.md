# release-fixture

Deterministic product/source fixture for shared release and Homebrew automation.

This repository behaves like a small product repository. It owns fixture source,
versioned Git tags, immutable GitHub Releases, release assets, and Homebrew specs. Shared
automation is tested from here through its public interfaces rather than by importing
implementation files.

## Release fixture

`scripts/build-fixtures.py` produces byte-identical archives for:

- macOS arm64;
- macOS x86_64;
- Linux arm64;
- Linux x86_64.

Each archive contains an executable `release-fixture` command.

The `release fixture` workflow publishes an existing stable `vX.Y.Z` tag with
`release-actions`. It does not implement GitHub Release lifecycle logic itself.

## Homebrew acceptance

Two specs exercise the public Homebrew workflows:

- `.github/homebrew/source-formula.yml`: source-archive validation;
- `.github/homebrew/formula.yml`: GitHub Release asset validation and publishing.

Run `Homebrew public API acceptance` from the same fixture tag whose immutable GitHub
Release is being validated, and pass that tag as the workflow input. This keeps the
pull-request-style check source and publish source on one immutable commit. The workflow:

1. runs both public `homebrew-actions/check.yml` paths;
2. publishes both source-archive and GitHub Release Formulae with the public
   `homebrew-actions/publish.yml`;
3. writes to the selected allowlisted test tap;
4. verifies reusable-workflow outputs and both resulting Formulae.

Publishing requires an Actions secret named `HOMEBREW_TAP_DEPLOY_KEY` containing a
write deploy key for `releaseway/homebrew-tap-fixture`. No production tap credential
belongs in this repository.

The default destination is `releaseway/homebrew-tap-fixture`. Starter acceptance can
select `releaseway/homebrew-starter-smoke` with the `STARTER_TAP_DEPLOY_KEY` secret.
Only these matching test tap/credential pairs are accepted. The smoke tap is
temporary; its repository and credential are removed after acceptance.

## Local validation

```sh
python3 test/fixtures.py
```

CI also lints all fixture workflows.
