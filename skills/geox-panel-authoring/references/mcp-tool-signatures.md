# GEOX MCP Tool Signatures

Quick-reference for MCP tools available in geox-gui panels.

## geox_well_ingest

Load well log data (LAS/CSV) and return structured curves.

```typescript
// Args
{ well_id: string; mode: 'auto' | 'manual'; depth_top?: number; depth_base?: number }

// Result
{
  well_id: string;
  curves: {
    depth: number[];
    gr: number[];       // Gamma Ray (API)
    rhob: number[];     // Bulk density (g/cm³)
    nphi: number[];     // Neutron porosity (v/v)
    dt: number[];       // Sonic transit time (μs/ft)
    [key: string]: number[];  // extensible
  };
  tops?: { depth: number; name: string; facies?: string }[];
  facies?: string[];
  depth_range?: [number, number];
  receipt_hash?: string;
}
```

## geox_petrophysics

Compute petrophysical properties from well log curves.

```typescript
// Args
{ well_id: string; mode: 'generate' | 'evaluate'; model?: string }

// Result
{
  vsh?: number[];        // Volume of shale (v/v)
  phie?: number[];       // Effective porosity (v/v)
  sw?: number[];         // Water saturation (v/v)
  dt_synth?: number[];   // Synthetic sonic
  depth?: number[];
  litho_class?: string;  // e.g. 'sandstone', 'shale', 'limestone'
  facies?: string[];
  pay_flags?: boolean[];
  receipt_hash?: string;
}
```

## Standard curve ranges

| Curve | Min  | Max   | Unit    |
|-------|------|-------|---------|
| GR    | 0    | 200   | API     |
| RHOB  | 1.6  | 2.8   | g/cm³   |
| NPHI  | -0.1 | 0.6   | v/v     |
| DT    | 40   | 140   | μs/ft   |
| VSH   | 0    | 1     | v/v     |
| PHIE  | 0    | 0.4   | v/v     |
| SW    | 0    | 1     | v/v     |

## Standard curve colors

| Curve | Color    | Hex       |
|-------|----------|-----------|
| GR    | Green    | `#22c55e` |
| RHOB  | Red      | `#ef4444` |
| NPHI  | Blue     | `#3b82f6` |
| DT    | Orange   | `#f97316` |
| VSH   | Amber    | `#f59e0b` |
| PHIE  | Blue     | `#3b82f6` |
| SW    | Cyan     | `#06b6d4` |

## Correlation / facies colors

| Facies     | Fill color                           |
|------------|--------------------------------------|
| Sand       | `rgba(250, 204, 21, 0.12)`         |
| Shale      | `rgba(148, 163, 184, 0.12)`        |
| Carbonate  | `rgba(59, 130, 246, 0.12)`         |
| Limestone  | `rgba(59, 130, 246, 0.12)`         |
| Dolomite   | `rgba(99, 102, 241, 0.12)`         |
