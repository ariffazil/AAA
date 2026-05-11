---
name: lasio-api-notes
description: "lasio 0.32 API quirks for writing LAS files programmatically — well headers, curve data, and params sections. Use when generating synthetic LAS files for GEOX fixtures or testing."
category: data-science
tags: [lasio, petrophysics, las-format, geoscience]
---

# lasio 0.32 API Notes

## Well Header Fields (LAS 2.0)

Use `.append()` not item assignment for header fields:
```python
import lasio
las = lasio.LASFile()

# WRONG (raises AttributeError or silent failure):
las.well['WELL'] = 'BOKOR-1'

# CORRECT:
las.well.append(lasio.HeaderItem('WELL', unit='', value='BOKOR-1'))
```

Built-in well fields (STRT, STOP, STEP, NULL, UNIT) can use item assignment:
```python
las.well['STRT'].value = 1200.0
las.well['STOP'].value = 2500.0
las.well['STEP'].value = 0.152
las.well['NULL'].value = -999.25
las.well['UNIT'].value = 'M'
```

## Params Section

Custom parameters in ~Params section use `.append()`:
```python
las.params.append(lasio.HeaderItem('COMP', unit='', value='Synthetic Demo'))
las.params.append(lasio.HeaderItem('WELL', unit='', value='BOKOR-1'))
las.params.append(lasio.HeaderItem('FLD', unit='', value='BOKOR'))
las.params.append(lasio.HeaderItem('LOC', unit='', value='Synthetic BOKOR-style demonstration'))
las.params.append(lasio.HeaderItem('SRVC', unit='', value='Synthetic'))
las.params.append(lasio.HeaderItem('DATE', unit='', value='2026-01-01'))
las.params.append(lasio.HeaderItem('UWI', unit='', value='BOKOR-1-DEMO'))
las.params.append(lasio.HeaderItem('API', unit='', value='00DEMO000100'))
las.params.append(lasio.HeaderItem('EKB', unit='M', value=20.0))
las.params.append(lasio.HeaderItem('EGL', unit='M', value=18.0))
las.params.append(lasio.HeaderItem('TDD', unit='M', value=2500.0))
```

## Curves

Curves use `.append()`:
```python
las.append_curve('DEPT', depth_data, unit='M')
las.append_curve('GR', gr_data, unit='GAPI')
las.append_curve('RT', rt_data, unit='OHMM')
```

## Read

```python
las = lasio.read('file.las', encoding='latin-1')
# Or:
las = lasio.read('file.las')  # auto-detect encoding

# Access curves:
for curve in las.curves:
    print(f'{curve.mnemonic}: {len(curve.data)} samples')

# Well header:
las.well['WELL'].value
las.well.STRT.value  # only for built-in fields
```

## Write

```python
las.write('output.las', version=2.0)
```

## Common Issues

- **las.df()** requires pandas — don't call in minimal environments. Use `las.curves` directly.
- **encoding='latin-1'** needed for some older LAS files with special characters.
- **null values**: lasio uses -999.25 as default NULL. Set with `las.well['NULL'].value = -999.25`.
