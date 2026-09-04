---
name: Clinical Flow
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#3d4947'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#6d7a77'
  outline-variant: '#bcc9c6'
  surface-tint: '#006a61'
  primary: '#00685f'
  on-primary: '#ffffff'
  primary-container: '#008378'
  on-primary-container: '#f4fffc'
  inverse-primary: '#6bd8cb'
  secondary: '#006b5f'
  on-secondary: '#ffffff'
  secondary-container: '#6df5e1'
  on-secondary-container: '#006f64'
  tertiary: '#006194'
  on-tertiary: '#ffffff'
  tertiary-container: '#007bb9'
  on-tertiary-container: '#fdfcff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#89f5e7'
  primary-fixed-dim: '#6bd8cb'
  on-primary-fixed: '#00201d'
  on-primary-fixed-variant: '#005049'
  secondary-fixed: '#71f8e4'
  secondary-fixed-dim: '#4fdbc8'
  on-secondary-fixed: '#00201c'
  on-secondary-fixed-variant: '#005048'
  tertiary-fixed: '#cce5ff'
  tertiary-fixed-dim: '#93ccff'
  on-tertiary-fixed: '#001d31'
  on-tertiary-fixed-variant: '#004b73'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  display-lg:
    fontFamily: manrope
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: manrope
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: manrope
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: manrope
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  label-lg:
    fontFamily: inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
  label-md:
    fontFamily: inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.04em
  data-metric:
    fontFamily: manrope
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.02em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  space-xxs: 0.125rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-base: 1rem
  space-lg: 1.25rem
  space-xl: 1.5rem
  space-2xl: 2rem
  gutter-mobile: 0.75rem
  gutter-desktop: 1.25rem
  margin-mobile: 1rem
  margin-desktop: 2rem
---

## Brand & Style
The design system delivers an authoritative, high-efficiency clinical environment crafted specifically for hospital out-patient department (OPD) teams, triage nurses, and medical receptionists. In fast-paced healthcare operational settings, visual friction equates to administrative delays and degraded patient outcomes. 

The aesthetic is Modern Clinical Minimalist: ultra-crisp structural framing, tranquil light ice-cyan surfaces, and immediate semantic risk triage. The interface prioritizes clinical calm, visual clarity, and rapid legibility of patient acuity statuses, slot utilization rates, and active recovery alerts. Dense information sets are balanced by controlled white space, restrained borders, and precise visual contrast to minimize cognitive fatigue during 12-hour shifts.

## Colors
The color architecture reinforces clinical hygiene, clarity, and rapid triage identification. 

- **Primary & Interactive:** Deep Teal (`#0D9488`) anchors key actions, navigation states, and primary interaction targets. Cyan/Teal Medium (`#14B8A6`) serves as the hover and focus accent, conveying clinical intelligence and modern digital care.
- **Surfaces & Canvas:** The root canvas alternates between cool crisp ice-cyan tint (`#F0FDFA`) and pristine soft slate neutral (`#F8FAFC`). Cards sit on pure white (`#FFFFFF`) to establish sharp separation against background tones.
- **Typography & Structural Slates:** Deep Slate (`#0F172A`) is reserved for primary headers, patient identifiers, and critical metrics. Body text utilizes Slate Medium (`#334155`), while meta-labels, table subtext, and dividers leverage Slate Subtle (`#64748B`) and slate line borders (`#E2E8F0`).
- **Semantic Acuity & Triage System:**
  - **High Risk / Critical Alert:** Surface `#FEE2E2`, Foreground/Border `#EF4444`, Text `#991B1B`.
  - **Medium Risk / Pending Attention:** Surface `#FEF3C7`, Foreground/Border `#F59E0B`, Text `#92400E`.
  - **Low Risk / Stable Routine:** Surface `#D1FAE5`, Foreground/Border `#10B981`, Text `#065F46`.
  - **Slot Recovery / Active Flow:** Surface `#CCFBF1`, Foreground/Border `#0D9488`, Text `#115E59`.

## Typography
The system couples `Manrope` for structured, contemporary headers and tabular metric callouts with `Inter` for hyper-readable clinical data tables, patient logs, and operational forms. 

- **Numerical Hygiene:** Use tabular lining figures (`font-variant-numeric: tabular-nums`) across all timestamps, vitals, MRN codes, and slot counts to prevent layout jitter during live-feed socket updates.
- **Labels & Micro-copy:** Uppercase tracking (`0.04em`) is applied strictly to `label-sm` for department headings, status indicators, and column metadata.
- **Reading Hierarchy:** Patient names use `headline-sm` at weight 600 in Slate 900 (`#0F172A`). Secondary vitals and operational annotations use `body-sm` in Slate 500 (`#64748B`).

## Layout & Spacing
The layout employs an ultra-dense, responsive 12-column fluid grid tailored for dashboard workstations (1440px and 1920px clinical consoles), convertible medical carts (tablets, 768px–1024px), and on-call handhelds (<768px).

- **Desktop (1024px+):** Fixed 260px collapsible operational navigation drawer, dynamic master-detail split screen with standard 1.25rem gutters. Right-side context drawers handle active slot recovery feeds and triage quick-edits.
- **Tablet (768px - 1023px):** Persistent icon-rail navigation (68px), adaptive 2-column card arrays, 1rem gutters, and bottom-sheet drawers for patient triage detail.
- **Mobile (<768px):** Single-column stacked cards with bottom sticky navigation bar. Data-heavy tables convert into vertical patient triage cards with clear priority color chips.
- **Internal Padding Rhythm:** Metrics and clinical cards leverage `1.25rem` padding. High-density data tables utilize compact vertical cell padding (`0.5rem`) with generous horizontal padding (`1rem`) to keep patient lists concise without sacrificing tap targets.

## Elevation & Depth
In alignment with modern clinical interface principles, depth is defined primarily through low-contrast hairline borders, subtle tonal layering, and minimal ambient shadows. Heavy shadows are explicitly avoided to eliminate visual muddiness in high-ambient-light hospital rooms.

- **Base Layer (Level 0):** Background canvas in ice-blue/cyan tint (`#F0FDFA` or `#F8FAFC`).
- **Surface Layer (Level 1):** Data tables, OPD room cards, and KPI panels sit on pure `#FFFFFF` bounded by a crisp 1px border of `#E2E8F0` or `#CCFBF1`. Ambient elevation is minimal: `0 1px 2px 0 rgba(15, 23, 42, 0.04)`.
- **Raised Interactive Layer (Level 2):** Hovered patient rows, active dropdowns, and alert banners leverage a refined lift: `0 4px 12px -2px rgba(13, 148, 136, 0.08), 0 2px 4px -1px rgba(15, 23, 42, 0.04)`.
- **Modal & Critical Alert Layer (Level 3):** Urgent slot recovery dialogues and triage reassignments use: `0 12px 24px -4px rgba(15, 23, 42, 0.12), 0 0 0 1px rgba(226, 232, 240, 0.8)` accompanied by a 40% opacity slate backdrop blur (`backdrop-blur-sm`).

## Shapes
The shape language uses `Soft` curvature (`0.25rem` base, `0.5rem` for cards and modals) to reflect clinical precision, professional software ergonomics, and structured discipline.

- **Buttons & Form Fields:** `rounded-md` (`0.375rem`) provides a firm, defined boundary.
- **Cards & Data Panels:** `rounded-lg` (`0.5rem`) ensures clean grouping without creating excessive organic softness that wastes screen real estate.
- **Badges & Status Tags:** Pill geometry (`rounded-full` / 9999px) is strictly reserved for status indicators (High, Medium, Low, Recovered) to create immediate visual distinction from rectangular interactive buttons and input boxes.

## Components

### Buttons
- **Primary:** Background `#0D9488`, text `#FFFFFF`, border none, height 38px, font `label-lg`. On hover: `#0F766E`. Active: `#115E59`. Focus ring: 2px offset with `#14B8A6`.
- **Secondary / Outline:** Background `#FFFFFF`, text `#0F172A`, border `1px solid #CBD5E1`. On hover: `#F8FAFC` and border `#94A3B8`.
- **Ghost:** Text `#0D9488`, background transparent. Hover: `#F0FDFA`.
- **Destructive / Urgent Action:** Background `#EF4444`, text `#FFFFFF`. Hover: `#DC2626`.

### Risk & Status Badges (Lucide-Style Semantics)
Pill-shaped containers featuring an aligned 14px Lucide outline icon, `label-sm` text weight 600, padding `2px 8px`:
- **High Risk:** Background `#FEE2E2`, border `1px solid #FECACA`, text `#991B1B`, icon `AlertTriangle` (`#EF4444`).
- **Medium Risk:** Background `#FEF3C7`, border `1px solid #FDE68A`, text `#92400E`, icon `Clock` (`#F59E0B`).
- **Low Risk:** Background `#D1FAE5`, border `1px solid #A7F3D0`, text `#065F46`, icon `CheckCircle2` (`#10B981`).
- **Slot Recovery Alert:** Background `#CCFBF1`, border `1px solid #99F6E4`, text `#115E59`, icon `Zap` (`#0D9488`).

### Data Tables & Patient Queues
- **Header:** Background `#F8FAFC`, bottom border `1px solid #E2E8F0`, typography `label-sm`, text uppercase `#64748B`.
- **Row:** Height 52px, pure white `#FFFFFF` surface, bottom border `1px solid #F1F5F9`. Hover state shifts smoothly to `#F0FDFA`.
- **Cells:** Tabular data aligned with patient identification avatar, age/gender metadata in `#64748B`, and right-aligned risk badges.

### Metric & KPI Cards
- White background (`#FFFFFF`), border `1px solid #E2E8F0`, rounded `0.5rem`, padding `1.25rem`.
- Contains: Category label (`label-sm`, `#64748B`), bold numeric value (`data-metric`, `#0F172A`), and micro trend indicator pill with an icon (`TrendingUp` or `TrendingDown`).

### Input Fields & Selects
- Height 40px, background `#FFFFFF`, border `1px solid #CBD5E1`, text `body-md` in `#0F172A`, placeholder `#94A3B8`.
- Focused state: Border `#0D9488`, subtle ring `0 0 0 3px rgba(13, 148, 136, 0.15)`.
- Error state: Border `#EF4444`, ring `0 0 0 3px rgba(239, 68, 68, 0.15)`.

### Active Slot Recovery Alert Banner
- Full-width or inline banner: Background `#F0FDFA`, left indicator border `4px solid #0D9488`, container border `1px solid #CCFBF1`.
- Includes live countdown timer (`tabular-nums`), quick triage buttons (`Assign Now`, `Dismiss`), and an pulsing dot badge indicating a freshly freed OPD appointment slot.