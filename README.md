# release-fixture

Deterministic test-only release source for shared GitHub Release and Homebrew automation.

The repository intentionally owns fixture tags and immutable GitHub Releases so reusable
automation repositories do not mix product tags with test-fixture tag families.

`scripts/build-fixtures.py` creates byte-identical archives for:

- macOS arm64
- macOS x86_64
- Linux arm64
- Linux x86_64

Each archive contains an executable `release-fixture` script. The declarative Homebrew
spec under `.github/homebrew/formula.yml` consumes the same assets for native
integration validation.

The release workflow is operator-triggered and publishes only an existing `vX.Y.Z`
fixture tag.
