# TSRA D2 Style Guide

Conventions for authoring and maintaining Trust Security Reference Architecture diagrams in D2.

---

## 1. File Naming

| Pattern | Example | Purpose |
|---|---|---|
| `NN-descriptive-name.d2` | `09-privileged-trust-architecture.d2` | Current diagram; `NN` is zero-padded sequence |
| `NN-descriptive-name-v2.d2` | `15-implementation-roadmap-v2.d2` | Revised replacement (both kept for traceability) |
| `NN-descriptive-name-old.d2` | `04-staff-authentication-flow-old.d2` | Superseded version retained for audit trail |

- Use lowercase, hyphen-separated words.
- Sequence numbers align to SRA document order where possible, **not** to SRA section numbers (the title block carries the section reference).

---

## 2. Title Block

Every diagram **must** begin with a title block containing:
1. A Markdown `#` heading with the diagram name.
2. A bold **SRA §N** line mapping to the parent document section.

```d2
title: |md
  # Diagram Title
  **SRA §N** — Section Name
| {near: top-center}
```

For appendices or cross-cutting diagrams:

```d2
title: |md
  # Legend: TSRA Diagram Conventions
  **TSRA** — Cross-Cutting Diagram Reference
| {near: top-center}
```

---

## 3. Configuration Block

Immediately after the title (or before it, if the file uses `dagre`):

```d2
vars: {
  d2-config: {
    layout-engine: elk
  }
}
```

- **ELK** is the default layout engine for all diagrams.
- **Dagre** is permitted when ELK produces suboptimal results (document the reason in a comment).

---

## 4. Canvas Defaults

```d2
direction: right          # default; use 'down' only for vertical taxonomies
style: {
  fill: "#FFFFFF"
  stroke: "#CFD8DC"
  stroke-width: 1
}
```

---

## 5. Edge Defaults

Apply globally at file scope to ensure consistent connection styling:

```d2
(*** -> ***)[*]: {
  style.border-radius: 0
  style.stroke: "#455A64"
  style.stroke-width: 1
}
```

---

## 6. Leaf-Node Defaults

```d2
**: {
  &leaf: true
  !&shape: image          # exclude image-shaped nodes
  width: 250              # adjust per diagram (range: 200–340)
  height: 88              # adjust per diagram (range: 50–124)
  style.border-radius: 6
}
```

For image nodes (cloud-provider icons, etc.):

```d2
**: {
  &shape: image
  width: 72
  height: 72
}
```

### Sizing Guidance

| Diagram Type | Recommended width × height |
|---|---|
| Flow / architecture (default) | 250 × 88 |
| Matrix / comparison | 200 × 50 |
| Metric / KPI | 320 × 120 |
| Roadmap phases | 200 × 100 |

---

## 7. Color Palette

### Primary Semantic Colors (from legend)

These five are the core domain colors used across the diagram set:

| Domain | Fill | Stroke | Hex Pair |
|---|---|---|---|
| Identity / Access | `#E3F2FD` | `#1565C0` | Blue 50 / Blue 800 |
| Trust Decision / Policy | `#E8F5E9` | `#2E7D32` | Green 50 / Green 800 |
| Exposure / Posture / Device | `#FFF8E1` | `#F57F17` | Amber 50 / Amber 900 |
| Cloud Context / Platform | `#F3E5F5` | `#6A1B9A` | Purple 50 / Purple 800 |
| Risk / Compliance / Control | `#FFEBEE` | `#C62828` | Red 50 / Red 800 |

### Extended Colors (supplementary)

Used for sub-domains or specialized diagrams:

| Purpose | Fill | Stroke | Used In |
|---|---|---|---|
| Outcome / Impact | `#FCE4EC` | `#AD1457` | Overview, Outcomes |
| Governance / Workflow | `#FFF3E0` | `#EF6C00` | Doc Control, KPI |
| Metadata / Document | `#E8EAF6` | `#303F9F` | Doc Control |
| Versioning / Lifecycle | `#E0F2F1` | `#00695C` | Doc Control |
| KPI / Measurement | `#E1F5FE` | `#0277BD` | KPI Framework |
| Conditions (matrix) | `#FFF3E0` | `#E65100` | CA Policy Matrix |
| Medium Risk Tier | `#FFFDE7` | `#F9A825` | CA Policy Matrix |

### Application Rules

- All colors are Material Design palette values (50-weight fill, 800/900-weight stroke).
- Group containers use `stroke-width: 2`.
- Leaf nodes inherit the group fill or use white when ungrouped.
- **Do not introduce new fill/stroke pairs** without adding them to this table and updating `00-legend-conventions.d2`.

---

## 8. Group (Container) Structure

```d2
group_id: {
  label: "Human-Readable Domain Name"
  style: {
    fill: "<palette fill>"
    stroke: "<palette stroke>"
    stroke-width: 2
  }
  node1: "Short label"
  node2: "Short label with\nline break"
}
```

- Group IDs are `snake_case`.
- Node IDs within groups are short (`c1`, `m2`, `admin`, etc.) — the label carries meaning.
- Use `\n` for multi-line labels; avoid nodes wider than 340 px.

---

## 9. Icons and Images

Cloud provider icons use jsDelivr-hosted Simple Icons:

```d2
aws: {
  label: "AWS"
  shape: image
  icon: "https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/amazonaws.svg"
}
azure: {
  label: "Azure"
  shape: image
  icon: "https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/microsoftazure.svg"
}
gcp: {
  label: "GCP"
  shape: image
  icon: "https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/googlecloud.svg"
}
```

- Icon URL pattern: `https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/{slug}.svg`
- Pin to a major version (`@v11`) to avoid breakage.

---

## 10. Rendering

### CLI

```bash
# Single file
d2 --layout elk diagrams/security-reference-architecture/01-trust-security-architecture-overview.d2

# All current files (skip -old variants)
for f in diagrams/security-reference-architecture/[0-2][0-9]-*.d2; do
  [[ "$f" == *-old.d2 ]] && continue
  d2 --layout elk "$f"
done
```

### Output Conventions

| Format | Folder | Purpose |
|---|---|---|
| SVG | `rendering/` | Word/Confluence embedding |
| PNG | `rendering_png_v2/` | Slide decks, exports |

### Page Orientation

Landscape (8.5 × 11 in) is the intended output layout. Diagrams use `direction: right` to flow left-to-right across the wide axis.

---

## 11. Section-to-File Mapping

See [README.md](README.md) for the authoritative file-to-SRA-section mapping table.

---

## 12. Versioning and Lifecycle

| Action | Convention |
|---|---|
| Minor content update | Edit in place; commit with descriptive message |
| Structural redesign | Copy to `NN-name-v2.d2`; rename old to `NN-name-old.d2` if needed |
| Superseded diagram | Rename with `-old` suffix; keep in repo for audit trail |
| Rendering refresh | Re-run CLI; overwrite SVG/PNG outputs |

---

## Checklist for New Diagrams

- [ ] File named `NN-descriptive-name.d2`
- [ ] Title block with `# Heading` and `**SRA §N**` reference
- [ ] `layout-engine: elk` (or justified `dagre`)
- [ ] Canvas defaults (`direction`, `style`)
- [ ] Edge defaults (`(*** -> ***)[*]`)
- [ ] Leaf-node defaults (`**:`)
- [ ] Colors from the approved palette (§7)
- [ ] Groups use `stroke-width: 2`
- [ ] Labels use `\n` for wrapping, no node wider than 340 px
- [ ] Added to README.md mapping table
- [ ] Added to `manifest.tsv` for rendering pipeline
