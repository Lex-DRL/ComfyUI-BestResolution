## `TODO`

- Add `upscale` versions for `simple` and `ratio` nodes, too.
- Add options for `crop/pad` node - to determine the order of [crop/pad] -> upscale -> [crop/pad].
- Add node for auto-detecting USDU-padding from initial res.

# v1.3.0

- Internal change: All the nodes migrated to Comfy's nodes v3 API schema.
- No new features or changes in behavior.

# v1.1.5

- ... and another one.

# v1.1.4

- ... and an immediate bugfix.

# v1.1.3

- New node: `Upscale Image By (with Model)`

# v1.1.2

- New node: `Scale (Best-Res)`

# v1.1.1

- This `CHANGELOG.md` file.
- Prim-node rename (class and internal name, too): `Upscale Strategy (Best-Res)` -> `Crop-Pad Strategy (Best-Res)`
- Inputs/outputs for upscale-related nodes are renamed to be more intuitive.
- `Best-Res (area+scale)`: change (restore) the value returned by `upscale` output.
- Upscale-related nodes: change some defaults.

# v1.1.0

The minimally-complete version (full workflow coverage for my own use-case).
- Significant internal refactor.
- New group/category name: `Best Resolution`
- New nodes:
  - `Best-Res (area+scale)`
  - `Upscaled Crop/Pad (Best-Res)`
- New primitive nodes:
  - `Priority (Best-Res)`
  - `Upscale Strategy (Best-Res)`

# v1.0.0

The MVP. Contains nodes:
- `Best-Res (simple)`
- `Best-Res (ratio)`
- `Best-Res (area)`
