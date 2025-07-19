# V1.1.1

- This `CHANGELOG.md` file.
- Prim-node rename (class and internal name, too): `Upscale Strategy (Best-Res)` -> `Crop-Pad Strategy (Best-Res)`

# V1.1.0

The minimally-complete version (full workflow coverage for my own use-case).
- Significant internal refactor.
- New group/category name: `Best Resolution`
- New nodes:
  - `Best-Res (area+scale)`
  - `Upscaled Crop/Pad (Best-Res)`
- New primitive nodes:
  - `Priority (Best-Res)`
  - `Upscale Strategy (Best-Res)`

⚠️ Active `TODO: Add upscale versions for "simple" and "ratio" nodes.`

# v1.0.0

The MVP. Contains nodes:
- `Best-Res (simple)`
- `Best-Res (ratio)`
- `Best-Res (area+scale)`

`TODO: supporting utility nodes (primitives for combo-selectors, calculators for post-upscale res-tweaks with pad/crop).`
