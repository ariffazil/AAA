---
name: aaa-rph-generator
trigger:
  - "generate rph"
  - "rph"
  - "daily lesson plan"
  - "rancangan pengajaran"
  - "kssr lesson"
  - "moe rph"
sensitivity: F5_PROTECTED
federation_role: builder
schema_version: moe_rph_v1
extracted_from: /root/.hermes/profiles/nabilah/skills/nabilah-rph/SKILL.md
extraction_date: 2026-09-27
doctrine_ref: /root/AAA/eurekas/EUREKA-PROFILE-LANE-SCOPE-2026-09-27.md
---

# SKILL.md — aaa-rph-generator (KSSR Lesson Plan Generator)

> Persona-agnostic KSSR (Kurikulum Standard Sekolah Rendah) RPH generator.
> Originally extracted from `nabilah-rph` (decommissioned persona, 2026-09-27).
> Generalization: teacher name + classes are now parameters, not hardcoded.

## Purpose

Generate KSSR-aligned RPH (Rancangan Pengajaran Harian — Daily Lesson Plan) PDFs
for Malaysian primary school teachers under the MOE KSSR curriculum.

Use this skill for ANY primary school subject (English, BM, Math, Science) and
ANY teacher persona — pass teacher name + classes + subject as runtime params.

## When to Use

- Daily at 6:30 AM weekdays (automated via cron; per-teacher schedule)
- When a teacher asks for RPH/lesson plan manually
- When a teacher asks to change topics, schedule, or rotation

## Inputs (runtime parameters)

| Param | Required | Example |
|-------|----------|---------|
| `teacher_name` | yes | "Cikgu Nabilah" / "Mr. Tan" |
| `subject` | yes | "English" / "BM" / "Math" |
| `classes` | yes | `["Darjah 1", "Darjah 3", "Darjah 4"]` (any combo) |
| `cefr_map` | optional | `{D1: "Pre-A1", D3: "A1", D4: "A2"}` (defaults below) |
| `output_dir` | optional | `/tmp/` (default) |
| `pdf_filename_pattern` | optional | `RPH_{teacher_slug}_{YYYY-MM-DD}.pdf` |

## KSSR Curriculum Scaffold

### Year-group defaults

| Year | Themes | CEFR (English) |
|------|--------|----------------|
| Darjah 1 | Dunia Diri Sendiri, Alam Sekitar, Sosial | Pre-A1 |
| Darjah 2 | Keluarga, Kesihatan, Kebersihan | A1 |
| Darjah 3 | Dunia Cerita, Sains, Alam Binaan | A1 |
| Darjah 4 | Dunia Maklumat, Perniagaan, Kreatif | A2 |
| Darjah 5 | Perpaduan, Patriotisme, Kerjaya | A2 |
| Darjah 6 | Global, Sains, Teknologi | B1 |

### English topic bank (default — override for other subjects)

**Darjah 1** (rotate by `ISO_week % 8`):
1. Greetings & Introductions
2. Colours & Shapes
3. Numbers 1-20
4. Body Parts
5. Family Members
6. Animals & Pets
7. Food & Drinks
8. My School

**Darjah 3** (rotate by `ISO_week % 8`):
1. Daily Routines — Simple Present Tense
2. Prepositions of Place
3. Simple Past Tense (introduction)
4. Countable & Uncountable Nouns
5. Reading Short Texts
6. Writing Simple Sentences
7. Storytelling Activities
8. Describing People & Pets

**Darjah 4** (rotate by `ISO_week % 8`):
1. Reading Comprehension — descriptive texts
2. Writing Paragraphs (topic sentence + supporting details)
3. Grammar — tenses (present, past, continuous)
4. Conjunctions & Connectors
5. Speaking — descriptions & explanations
6. Vocabulary — synonyms, antonyms, word families
7. Comprehension skills — main idea, details, inference
8. Narrative writing — short stories

For BM / Math / Science: substitute topic banks per MOE Dokumen Standard.

## RPH Schema (`moe_rph_v1`)

Per-class lesson plan structure:

1. **Header** — Tarikh, Hari, Mata Pelajaran, Tahun, Guru (all from inputs)
2. **Tema/Tajuk** — weekly rotation via `ISO_week % topic_bank_size`
3. **SK & SP** — Standard Kandungan & Standard Pembelajaran (KSSR codes)
4. **Objektif Pembelajaran** — 2-3 measurable objectives
5. **Aktiviti**:
   - Set Induksi (5 min)
   - Langkah 1 (15 min)
   - Langkah 2 (20 min)
   - Penutup (10 min)
6. **BBM** — bahan bantu mengajar (teaching aids)
7. **Refleksi** — "____ daripada ____ murid mencapai objektif"

## PDF Generation

```python
from aaa_rph_generator import generate_rph

result = generate_rph(
    teacher_name="Cikgu Nabilah",
    subject="English",
    classes=["Darjah 1", "Darjah 3", "Darjah 4"],
    date="2026-09-28",  # or auto from date()
)
# result.pdf_path = "/tmp/RPH_cikgu-nabilah_2026-09-28.pdf"
```

Or CLI:
```bash
python3 -m aaa_rph_generator --teacher "Cikgu Nabilah" --subject English \
  --classes D1 D3 D4 --date 2026-09-28
```

## Topic Rotation Logic

```python
import datetime
week_num = datetime.date.today().isocalendar()[1]  # ISO week
topic_idx = week_num % len(topic_bank)
```

Different topic each week = 8-week variety, no repetition.

## Delivery

Save PDF to `output_dir`, deliver via MEDIA: path in Telegram or any channel.
Per-teacher delivery routing configured by caller (NOT hardcoded — was persona-bound in original).

## Pitfalls

- Always call `date.today()` first — never assume the date
- `reportlab` required: `pip install reportlab`
- Use Helvetica (built-in) — don't rely on custom fonts unless MOE template demands
- F5_PROTECTED: student/teacher PII must NEVER be hardcoded in the skill — pass via params
- Cron schedules are per-teacher; this skill does NOT manage cron, only generates PDFs

## Provenance

Extracted from `/root/.hermes/profiles/nabilah/skills/nabilah-rph/SKILL.md` on 2026-09-27
during nabilah persona decommissioning (F13 directive). Persona binding stripped;
schema (`moe_rph_v1`) and rotation logic preserved.

Doctrine reference: [[eureka-profile-lane-scope-2026-09-27]]