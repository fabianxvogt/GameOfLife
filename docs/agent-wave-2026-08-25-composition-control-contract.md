# Plane composition control contract — 2026-08-25

## Finding

`Plane.append_plane` rotates the destination before delegating to
`append_plane_bottom`. A non-integer `n` or `space_between` reached `range(...)`
only after that rotation, so a failed non-bottom composition could leave the
destination with changed orientation and dimensions.

## Change

Both composition methods now reject boolean or non-integer `n` and
`space_between` values before reading or mutating plane geometry. Existing
non-positive integer behavior is unchanged.

## Evidence and classification

- Regression coverage exercises both invalid controls on all four append sides
  and verifies the destination state is unchanged.
- The bounded audit also checked 108 generalized self-compositions, 8 source
  ownership cases, 6 self-insertion cases, and one multi-component
  `CombinedCreature` coordinate/ownership case; all passed.
- A separate unequal-dimension composition probe still reproduces ragged rows.
  Its padding-versus-rejection contract is unspecified, so it remains outside
  this safe fix.
- Acceptance checks: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q`,
  `git diff --check`, and a clean working tree after verification.
- Classification: **INCREMENTAL / EMPIRICAL**. Evidence is limited to finite
  control validation and the listed bounded probes.

No license metadata or dependency files were changed.
