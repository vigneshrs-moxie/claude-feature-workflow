# Pages, components and user-facing text

- Reuse existing components before writing new ones.
- Every screen the spec covers has its loading, empty and error states as the spec describes them.
- Text matches the spec exactly. Any wording the spec does not give is proposed in the report, not shipped as final.
- Keyboard and screen-reader basics: labelled controls, focus visible, buttons are buttons.
- Hiding UI is never the permission check; the server enforces it (see api.md).

**Orbit**
- This Next.js version differs from training data: read the relevant guide in `node_modules/next/dist/docs/` before writing route or component code (see `AGENTS.md`).
- Components: `src/components/` (shadcn setup in `components.json`); for example `empty-state.tsx` and `back-link.tsx`.
