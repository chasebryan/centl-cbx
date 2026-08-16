# CENTL-CBX migration provenance

This repository is the focused successor proving ground for the CBX
and exact Erdős–Straus research machine previously developed inside
`chasebryan/centl`.

Initial source:

- repository: `chasebryan/centl`
- branch: `agent/cbx-kernel`
- source area: `research/erdos-straus/`

Migration policy:

- the complete `cbx.kernel/` executable surface is copied to `kernel/`;
- active K27/K31/K35/h169/Type-II/route-local theorem and verifier
  modules are copied to `research/`;
- broad historical CENTL application code is intentionally not copied;
- future CBX-focused research belongs here.

The Bryan Entanglement Cross / BREC layer remains observational and
scheduling metadata. Exact arithmetic state is the sole proof-bearing
authority.
