#!/usr/bin/env python3
"""Base de referencias de creador-skills-creativas. Solo librería estándar (Python 3.8+).

Comandos, en el orden del proceso:
  init          crea refs.json con el encuadre (oficio, sector, uso, canal, estilo)
  add           añade una tanda de referencias desde un JSON (deduplica por URL)
  validate      comprueba esquema, duplicados y mínimos (explore: 10 x 5; search: 200)
  board         genera el tablero HTML: --mode pick (Fase 2) o --mode rate (Fase 4)
  pick          registra la Fase 2 contestada por encuesta (letra, tipología o una propia)
  apply         aplica el JSON que descarga el tablero (picks.json o ratings.json)
  score         registra puntuaciones contestadas por encuesta (id=nota)
  status        dice en qué fase está el trabajo y qué falta
  stats         análisis en Markdown: criterio por dimensión y rasgos sueltos
  export-skill  escribe las referencias y el criterio por dimensión para la skill final

Esquema de cada referencia (refs.json -> "refs"):
  id, url, title, author, platform, thumb, group (= dimensión), tipologia, tags[], note, license,
  phase ("explore" | "search"), contrast (bool), picked (bool), score (1-10 | null), user_note

Los tags de dimensión tienen la forma "dimensión:tipología" (p. ej. "Luz:Natural de ventana"), con los
mismos nombres que las dimensiones y tipologías de la Fase 1; mayúsculas y tildes no importan.
"""
import argparse
import datetime
import html
import json
import random
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

LIKE_MIN = 6  # 6-10 le gusta; 1-5 evitar
EXPLORE_GROUPS, EXPLORE_PER_GROUP, SEARCH_MIN = 10, 5, 200
LETTERS = "ABCDEFGH"
TRACKING = re.compile(r"^(utm_.*|fbclid|gclid|igshid|mibextid|si|pp|feature|cbrd|ref|source|locale)$")


# ----------------------------------------------------------------------------- utilidades
def die(msg):
    sys.exit(f"ERROR: {msg}")


def host_of(url):
    host = urlsplit(url).netloc.lower().split("@")[-1].split(":")[0]
    return host[4:] if host.startswith("www.") else host


def is_http(u):
    return urlsplit(str(u).strip()).scheme.lower() in ("http", "https")


def clean_url(u):
    """Quita parámetros de seguimiento y fragmento; conserva el resto tal cual."""
    p = urlsplit(u.strip())
    q = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True) if not TRACKING.match(k)]
    return urlunsplit((p.scheme.lower(), p.netloc, p.path, urlencode(q), ""))


def norm_url(u):
    p = urlsplit(u.strip())
    q = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True) if not TRACKING.match(k)]
    return urlunsplit((p.scheme.lower(), host_of(u), p.path.rstrip("/") or "/", urlencode(q), ""))


def platform_of(url):
    """'https://es.pinterest.com/pin/1' -> 'pinterest'; 'campaignlive.co.uk' -> 'campaignlive'."""
    parts = host_of(url).split(".")
    if len(parts) >= 3 and len(parts[-1]) == 2 and parts[-2] in ("co", "com", "org", "net", "gob", "gov"):
        return parts[-3]
    return parts[-2] if len(parts) >= 2 else parts[0]


def slug(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def split_tag(t):
    """'Luz: Natural de ventana' -> ('luz', 'natural-de-ventana', 'Natural de ventana'); sin ':' -> None."""
    if ":" not in str(t):
        return None
    d, v = str(t).split(":", 1)
    return slug(d), slug(v), v.strip()


def mean(xs):
    return sum(xs) / len(xs)


def signed(x):
    """+0.4 / -1.2, sin «-0.0»."""
    return f"{(round(x, 1) or 0.0):+.1f}"


def contrast_vs_rest(inside, outside):
    """Diferencia de medias (tipología menos el resto de la dimensión) y un t de Welch aproximado."""
    if not inside or not outside:
        return 0.0, 0.0
    def var(xs):
        m = mean(xs)
        return sum((x - m) ** 2 for x in xs) / (len(xs) - 1) if len(xs) > 1 else 0.0
    diff = mean(inside) - mean(outside)
    se = (var(inside) / len(inside) + var(outside) / len(outside)) ** 0.5
    t = diff / se if se else (float("inf") if diff else 0.0)
    return diff, t


def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        die(f"no existe {path} (¿hiciste init?)")


def save(path, data):
    tmp = Path(str(path) + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")
    tmp.replace(path)  # escritura atómica: un corte no deja refs.json a medias


def dimensions(refs):
    """Dimensiones = grupos de explore, en orden de aparición."""
    out = []
    for r in refs:
        if r.get("phase") == "explore" and r.get("group") and r["group"] not in out:
            out.append(r["group"])
    return out


def explore_by_group(refs):
    groups = {g: [] for g in dimensions(refs)}
    for r in refs:
        if r.get("phase") == "explore":
            groups[r["group"]].append(r)
    return groups


def seeds_of(data):
    """Criterio inicial de la Fase 2: {dimensión: tipología elegida} (incluye las propias)."""
    out = {}
    for r in data["refs"]:
        if r.get("phase") == "explore" and r.get("picked"):
            out[r["group"]] = r.get("tipologia")
    for g, t in (data["profile"].get("custom_picks") or {}).items():
        if t:
            out[g] = t
    return out


def to_rate(refs):
    """Lo que se puntúa en la Fase 4: toda la búsqueda y las semillas elegidas."""
    return [r for r in refs if r.get("phase") == "search" or r.get("picked")]


def find_dimension(refs, key):
    dims = dimensions(refs)
    key = key.strip()
    if key.isdigit() and 1 <= int(key) <= len(dims):
        return dims[int(key) - 1]
    for d in dims:
        if slug(d) == slug(key):
            return d
    starts = [d for d in dims if slug(d).startswith(slug(key))]
    if len(starts) == 1:
        return starts[0]
    die(f"no encuentro la dimensión '{key}'. Dimensiones: {', '.join(dims)}")


def split_assign(item, what):
    if "=" not in item:
        die(f"usa '{what}=valor' (recibido: {item!r})")
    k, v = item.split("=", 1)
    return k.strip(), v.strip()


# ----------------------------------------------------------------------------- init
def cmd_init(a):
    d = Path(a.dir)
    d.mkdir(parents=True, exist_ok=True)
    target = d / "refs.json"
    if target.exists() and not a.force:
        die(f"{target} ya existe. Para seguir donde lo dejaste: refs.py status {target}")
    save(target, {
        "profile": {
            "oficio": a.oficio, "foco": a.foco, "uso": a.uso or "", "canal": a.canal or "",
            "keyword": a.keyword or "", "modo": a.modo or "extensión de Chrome",
            "created": datetime.date.today().isoformat(),
        },
        "refs": [],
    })
    print(f"Creado {target}")


# ----------------------------------------------------------------------------- add
def read_batch(path):
    raw = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    try:
        batch = json.loads(raw)
    except json.JSONDecodeError as e:
        die(f"la tanda no es JSON válido: {e}")
    if isinstance(batch, dict):
        batch = batch.get("refs", [])
    if not isinstance(batch, list):
        die('la tanda debe ser una lista de referencias o {"refs": [...]}')
    return batch


def next_number(refs, prefix):
    nums = [int(str(r.get("id"))[1:]) for r in refs if re.fullmatch(prefix + r"\d+", str(r.get("id", "")))]
    return max(nums) + 1 if nums else 1


def cmd_add(a):
    data = load(a.file)
    refs = data["refs"]
    seen = {norm_url(r["url"]): r["id"] for r in refs if r.get("url")}
    prefix, width = ("e", 2) if a.phase == "explore" else ("s", 3)
    n = next_number(refs, prefix)
    added, repeated, problems = [], [], []
    for i, r in enumerate(read_batch(a.batch), 1):
        if not isinstance(r, dict):
            problems.append(f"#{i}: no es un objeto")
            continue
        url = str(r.get("url") or "").strip()
        if not is_http(url):
            problems.append(f"#{i}: url no válida ({url!r})")
            continue
        if not r.get("group"):
            problems.append(f"#{i} {url}: falta 'group' (la dimensión)")
            continue
        if a.phase == "explore" and not r.get("tipologia"):
            problems.append(f"#{i} {url}: en explore falta 'tipologia'")
            continue
        url = clean_url(url)
        key = norm_url(url)
        if key in seen:
            repeated.append(f"{url} (ya está como {seen[key]})")
            continue
        ref = {
            "id": f"{prefix}{n:0{width}d}", "url": url,
            "title": r.get("title", ""), "author": r.get("author", ""),
            "platform": r.get("platform") or platform_of(url), "thumb": r.get("thumb", ""),
            "group": r["group"], "tipologia": r.get("tipologia", ""),
            "tags": list(dict.fromkeys(r.get("tags") or [])), "note": r.get("note", ""),
            "license": r.get("license", "referencia"), "phase": a.phase,
            "contrast": bool(r.get("contrast", False)), "picked": False, "score": None,
        }
        if a.phase == "explore":  # la propia tipología cuenta como tag de su dimensión
            own = split_tag(f"{ref['group']}:{ref['tipologia']}")
            if not any((st := split_tag(t)) and st[:2] == own[:2] for t in ref["tags"]):
                ref["tags"].insert(0, f"{ref['group']}:{ref['tipologia']}")
        refs.append(ref)
        seen[key] = ref["id"]
        added.append(ref)
        n += 1
    save(a.file, data)
    print(f"Añadidas {len(added)} a {a.phase} · repetidas descartadas {len(repeated)} · con problemas {len(problems)}")
    for s in repeated[:10]:
        print("  repetida:", s)
    for p in problems:
        print("  PROBLEMA:", p)
    dims = {slug(g) for g in dimensions(refs)}
    if a.phase == "search" and dims:
        loose = [r["id"] for r in added if not any((st := split_tag(t)) and st[0] in dims for t in r["tags"])]
        if loose:
            print(f"  AVISO: {len(loose)} sin tags 'dimensión:tipología' de la Fase 1 ({', '.join(loose[:8])}…): "
                  "sin ellos no cuentan para el criterio por dimensión")
    ex = sum(1 for r in refs if r.get("phase") == "explore")
    se = sum(1 for r in refs if r.get("phase") == "search")
    print(f"Total: explore {ex}/{EXPLORE_GROUPS * EXPLORE_PER_GROUP} · search {se}/{SEARCH_MIN}")
    if problems:
        sys.exit("Las válidas se han guardado; corrige las que tienen problemas y vuelve a añadirlas.")


# ----------------------------------------------------------------------------- validate
def cmd_validate(a):
    data = load(a.file)
    refs = data["refs"]
    errors, warns = [], []
    seen_id, seen_url = set(), {}
    for i, r in enumerate(refs):
        rid = r.get("id", f"#{i}")
        for k in ("id", "url", "platform", "group"):
            if not r.get(k):
                errors.append(f"{rid}: falta '{k}'")
        if r.get("url") and not is_http(r["url"]):
            errors.append(f"{rid}: url no válida")
        if r.get("id") in seen_id:
            errors.append(f"id repetido: {rid}")
        seen_id.add(r.get("id"))
        if r.get("url"):
            key = norm_url(r["url"])
            if key in seen_url:
                errors.append(f"url repetida: {rid} = {seen_url[key]}")
            seen_url[key] = rid
        if r.get("phase") not in ("explore", "search"):
            errors.append(f"{rid}: phase debe ser 'explore' o 'search'")
        if r.get("phase") == "explore" and not r.get("tipologia"):
            errors.append(f"{rid}: en explore hace falta 'tipologia' (es la opción que el creativo elige)")
        s = r.get("score")
        if s is not None and (not isinstance(s, int) or isinstance(s, bool) or not 1 <= s <= 10):
            errors.append(f"{rid}: score debe ser un entero del 1 al 10 (es {s!r})")

    groups = explore_by_group(refs)
    explore = [r for r in refs if r.get("phase") == "explore"]
    search = [r for r in refs if r.get("phase") == "search"]
    print(f"Total {len(refs)} · explore {len(explore)} · search {len(search)}")

    if a.stage == "explore":
        if len(groups) != EXPLORE_GROUPS:
            warns.append(f"hay {len(groups)} dimensiones (lo previsto son {EXPLORE_GROUPS})")
        for g, rs in groups.items():
            if len(rs) != EXPLORE_PER_GROUP:
                errors.append(f"la dimensión '{g}' tiene {len(rs)} referencias (deben ser {EXPLORE_PER_GROUP})")
            rep = [t for t, c in Counter(slug(r.get("tipologia")) for r in rs).items() if c > 1]
            if rep:
                errors.append(f"la dimensión '{g}' repite tipología ({', '.join(rep)}): las 5 deben ser distintas")
        if len({r["platform"] for r in explore if r.get("platform")}) < 3:
            warns.append("menos de 3 plataformas en explore; mezcla más")
        missing = sum(1 for r in explore if not r.get("thumb"))
        if missing:
            warns.append(f"{missing} de {len(explore)} sin miniatura ('thumb'): en usos visuales es obligatoria, porque el "
                         "creativo elige viendo la imagen (en el uso Texto se puede omitir)")
    elif a.stage == "search":
        if len(search) < a.min:
            errors.append(f"search tiene {len(search)} referencias; el mínimo es {a.min}")
        plats = Counter(r.get("platform") for r in search)
        if len(plats) < 3:
            warns.append(f"solo {len(plats)} plataformas en search; usa al menos 3")
        if search:
            top, n = plats.most_common(1)[0]
            if n / len(search) > 0.5:
                warns.append(f"'{top}' aporta el {n * 100 // len(search)} % de la búsqueda; diversifica")
            share = sum(1 for r in search if r.get("contrast")) / len(search)
            if share < 0.15:
                warns.append(f"solo un {share:.0%} de contraste (objetivo 15-25 %): sin ejemplos fuera de su gusto no "
                             "habrá puntuaciones bajas")
            dims = {slug(g) for g in groups}
            tagged = sum(1 for r in search if any((st := split_tag(t)) and st[0] in dims for t in r.get("tags") or []))
            if dims and tagged / len(search) < 0.8:
                warns.append(f"solo {tagged} de {len(search)} llevan tags 'dimensión:tipología' de la Fase 1; sin ellos "
                             "no hay criterio por dimensión")
        print("Plataformas:", dict(plats.most_common()))
    for w in warns:
        print("AVISO:", w)
    for e in errors[:60]:
        print("ERROR:", e)
    if errors:
        sys.exit(1)
    print("OK")


# ----------------------------------------------------------------------------- pick / score
def print_seeds(data):
    seeds = seeds_of(data)
    custom = data["profile"].get("custom_picks") or {}
    print("Criterio inicial:")
    for i, g in enumerate(dimensions(data["refs"]), 1):
        if g in seeds:
            extra = " (propia)" if custom.get(g) else ""
            print(f"  {i:>2}. {g}: {seeds[g]}{extra}")
        elif g in custom:
            print(f"  {i:>2}. {g}: ninguna")
        else:
            print(f"  {i:>2}. {g}: —")


def cmd_pick(a):
    data = load(a.file)
    refs, prof = data["refs"], data["profile"]
    groups = explore_by_group(refs)
    if not groups:
        die("no hay referencias de explore todavía")
    custom = prof.setdefault("custom_picks", {})
    reasons = prof.setdefault("pick_reasons", {})
    for item in a.assign:
        key, val = split_assign(item, "Dimensión")
        dim = find_dimension(refs, key)
        items = groups[dim]
        for r in items:
            r["picked"] = False
        custom.pop(dim, None)
        if len(val) == 1 and val.upper() in LETTERS[:len(items)]:
            items[LETTERS.index(val.upper())]["picked"] = True
        elif slug(val) in ("ninguna", "ninguno", "none", ""):
            custom[dim] = None  # decidido: ninguna le representa
        else:
            match = [r for r in items if slug(r.get("tipologia")) == slug(val)]
            if match:
                match[0]["picked"] = True
            else:
                custom[dim] = val  # tipología propia escrita en «Otro»
    for item in a.reason or []:
        key, val = split_assign(item, "Dimensión")
        reasons[find_dimension(refs, key)] = val
    save(a.file, data)
    print_seeds(data)


def cmd_score(a):
    data = load(a.file)
    by_id = {r["id"]: r for r in data["refs"]}
    n = 0
    for item in a.assign:
        rid, val = split_assign(item, "id")
        if rid not in by_id:
            die(f"no existe la referencia {rid}")
        if not val.isdigit() or not 1 <= int(val) <= 10:
            die(f"{rid}: la nota debe ser un entero del 1 al 10 (recibido {val!r})")
        by_id[rid]["score"] = int(val)
        n += 1
    for item in a.note or []:
        rid, val = split_assign(item, "id")
        if rid not in by_id:
            die(f"no existe la referencia {rid}")
        by_id[rid]["user_note"] = val
    save(a.file, data)
    pending = [r for r in to_rate(data["refs"]) if r.get("score") is None]
    print(f"{n} puntuaciones registradas · faltan {len(pending)}")


# ----------------------------------------------------------------------------- status
def cmd_status(a):
    data = load(a.file)
    refs, p = data["refs"], data["profile"]
    groups = explore_by_group(refs)
    explore = [r for r in refs if r.get("phase") == "explore"]
    search = [r for r in refs if r.get("phase") == "search"]
    rateable = to_rate(refs)
    rated = [r for r in rateable if r.get("score") is not None]
    seeds = seeds_of(data)
    decided = set(seeds) | set(p.get("custom_picks") or {})
    print(f"Encuadre: {p.get('oficio')} · uso: {p.get('uso') or '—'} · sector: {p.get('foco')} · "
          f"canal: {p.get('canal') or '—'} · estilo: {p.get('keyword') or '—'} · modo: {p.get('modo') or '—'}")
    short = [f"{g} ({len(rs)})" for g, rs in groups.items() if len(rs) != EXPLORE_PER_GROUP]
    print(f"Fase 1 · explore: {len(explore)}/{EXPLORE_GROUPS * EXPLORE_PER_GROUP} en {len(groups)}/{EXPLORE_GROUPS} dimensiones"
          + (f" · incompletas: {', '.join(short)}" if short else ""))
    print(f"Fase 2 · criterio inicial: {len(decided)}/{len(groups)} dimensiones decididas")
    contrast = sum(1 for r in search if r.get("contrast"))
    plats = Counter(r.get("platform") for r in search)
    print(f"Fase 3 · search: {len(search)}/{SEARCH_MIN} · contraste {contrast} "
          f"({contrast / len(search):.0%}) · plataformas: {dict(plats.most_common(6))}" if search else
          f"Fase 3 · search: 0/{SEARCH_MIN}")
    if search and groups:
        cover = defaultdict(lambda: defaultdict(int))
        for r in search:
            for t in set(r.get("tags") or []):
                st = split_tag(t)
                if st:
                    cover[st[0]][st[1]] += 1
        print("  Evidencia por dimensión (referencias etiquetadas · tipologías con ≥3 · semilla):")
        for g in groups:
            c = cover.get(slug(g), {})
            seed = seeds.get(g)
            seed_n = c.get(slug(seed), 0) if seed else None
            print(f"   - {g}: {sum(c.values())} · {sum(1 for v in c.values() if v >= 3)} con ≥3"
                  + (f" · semilla «{seed}»: {seed_n}" if seed else ""))
    print(f"Fase 4 · puntuadas: {len(rated)}/{len(rateable)}")
    if len(groups) < EXPLORE_GROUPS or short or len(explore) < EXPLORE_GROUPS * EXPLORE_PER_GROUP:
        nxt = "Fase 1: completa 10 dimensiones × 5 tipologías (add --phase explore) y valida con --stage explore."
    elif len(decided) < len(groups):
        nxt = "Fase 2: genera el tablero (board --mode pick) y registra la elección de cada dimensión (pick)."
    elif len(search) < SEARCH_MIN:
        nxt = f"Fase 3: faltan {SEARCH_MIN - len(search)} referencias (add --phase search); refuerza las dimensiones con menos evidencia."
    elif len(rated) < len(rateable):
        nxt = f"Fase 4: faltan {len(rateable) - len(rated)} por puntuar (board --mode rate y apply, o score)."
    else:
        nxt = "Fases 5-6: stats → validar el criterio con la persona → export-skill y escribir la skill."
    print("Siguiente paso:", nxt)


# ----------------------------------------------------------------------------- board
BOARD = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#fafaf9;--fg:#1c1917;--mut:#78716c;--card:#fff;--bd:#e7e5e4;--ok:#15803d;--no:#b91c1c;--ac:#1d4ed8}
@media(prefers-color-scheme:dark){:root{--bg:#141413;--fg:#f5f5f4;--mut:#a8a29e;--card:#1f1e1d;--bd:#34312f;--ok:#4ade80;--no:#f87171;--ac:#60a5fa}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--bd);padding:12px 16px;display:flex;flex-wrap:wrap;gap:12px;align-items:center}
header h1{font-size:16px;margin:0}header .sub{color:var(--mut);font-size:13px;margin-right:auto}
button,select{font:inherit;color:inherit;background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:6px 12px;cursor:pointer}
button.primary{background:var(--ac);border-color:var(--ac);color:#fff}
main{padding:16px;max-width:1400px;margin:auto}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--bd);border-radius:12px;overflow:hidden;display:flex;flex-direction:column}
.card.sel{outline:3px solid var(--ok)}
.thumb{aspect-ratio:4/3;background:var(--bd);display:flex;align-items:center;justify-content:center;overflow:hidden}
.thumb a{display:flex;width:100%;height:100%;align-items:center;justify-content:center;text-decoration:none}
.thumb img{width:100%;height:100%;object-fit:cover}
.thumb span{color:var(--mut);padding:8px;text-align:center;font-size:13px}
.pick .thumb{aspect-ratio:4/5}.pick .thumb img{object-fit:contain}
.meta{padding:10px 12px;display:flex;flex-direction:column;gap:6px;flex:1}
.meta a{color:var(--fg);font-weight:600;text-decoration:none}
.meta small{color:var(--mut)}
.tip{font-size:16px}
.tags{display:flex;flex-wrap:wrap;gap:4px}.tags i{font-style:normal;font-size:12px;border:1px solid var(--bd);border-radius:99px;padding:0 7px;color:var(--mut)}
.pick .tags,.rate .tags{display:none}
.scale{display:grid;grid-template-columns:repeat(10,1fr);gap:3px;margin-top:auto}
.scale button{padding:5px 0;font-size:13px;border-radius:6px}
.scale button.on{color:#fff;border-color:transparent}
.scale button.on.lo{background:var(--no)}.scale button.on.hi{background:var(--ok)}
.note{width:100%;border:1px solid var(--bd);border-radius:6px;padding:5px 8px;background:var(--bg);color:inherit;font:inherit;font-size:13px}
section.grp{margin-bottom:28px}section.grp h2{font-size:17px;margin:0 0 4px}
.hint{color:var(--mut);margin:0 0 10px;font-size:13px}
.legend{color:var(--mut);font-size:13px;max-width:1400px;margin:0 auto;padding:8px 16px 0}
</style></head><body>
<header><h1>__TITLE__</h1><span class="sub">__SUB__</span><span id="prog"></span><span id="filters"></span><button class="primary" id="export">Descargar resultado</button></header>
<div class="legend" id="legend"></div>
<main id="main"></main>
<script>
const DATA=__DATA__;
const MODE=DATA.mode, KEY="board-"+MODE+"-"+DATA.slug;
document.body.classList.add(MODE);
let st={}; try{st=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}
st.picks=st.picks||{}; st.reasons=st.reasons||{}; st.ratings=st.ratings||{};
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}};
const esc=s=>String(s==null?"":s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function fallback(r){return `<span>${esc(r.platform)}<br>sin vista previa · abre el enlace</span>`}
function thumb(r){
  if(!r.thumb) return `<div class="thumb"><a href="${esc(r.url)}" target="_blank" rel="noopener">${fallback(r)}</a></div>`;
  return `<div class="thumb"><a href="${esc(r.url)}" target="_blank" rel="noopener"><img src="${esc(r.thumb)}" loading="lazy" referrerpolicy="no-referrer" alt="${esc(r.title)}" data-fb="${esc(r.platform)}"></a></div>`;
}
document.addEventListener("error",e=>{const t=e.target;if(t.tagName==="IMG"&&t.dataset.fb!==undefined){t.parentNode.innerHTML=`<span>${esc(t.dataset.fb)}<br>sin vista previa · abre el enlace</span>`}},true);
function info(r,letter){
  const link=`<a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.title||r.url)}</a>`;
  const head=MODE==="pick"&&r.tipologia
    ?`<b class="tip">${letter?esc(letter)+" · ":""}${esc(r.tipologia)}</b><small>${esc(r.note||"")}</small><small>Ejemplo: ${link} · ${esc(r.platform)}</small>`
    :`${link}<small>${esc(r.author||"")}${r.author?" · ":""}${esc(r.platform)}</small>${r.note?`<small>${esc(r.note)}</small>`:""}`;
  return head+`<div class="tags">${(r.tags||[]).map(t=>`<i>${esc(t)}</i>`).join("")}</div>`;
}
/* ---------- modo pick (Fase 2) ---------- */
function renderPick(){
  document.getElementById("legend").textContent="Mira las 5 opciones de cada dimensión y elige la que mejor representa lo que buscas. Puedes elegir aquí o contestar la encuesta con la misma letra (A–E). Si ninguna te convence, «Ninguna». Opcional: una frase con el porqué.";
  const groups=[...new Set(DATA.refs.map(r=>r.group))];
  document.getElementById("main").innerHTML=groups.map((g,gi)=>{
    const items=DATA.refs.filter(r=>r.group===g);
    return `<section class="grp"><h2>${gi+1}/${groups.length} · ${esc(g)}</h2><p class="hint">Elige 1 de ${items.length}</p><div class="grid">${items.map((r,i)=>
      `<div class="card ${st.picks[g]===r.id?"sel":""}">${thumb(r)}<div class="meta">${info(r,"ABCDEFGH"[i])}<button data-pick="${esc(r.id)}" data-g="${esc(g)}">${st.picks[g]===r.id?"✓ Elegida":"Elegir esta"}</button></div></div>`).join("")}</div>
      <p><button data-none="${esc(g)}">${st.picks[g]===null?"✓ Ninguna":"Ninguna"}</button> <input class="note" style="max-width:520px" data-reason="${esc(g)}" placeholder="¿Por qué? (opcional)" value="${esc(st.reasons[g]||"")}"></p></section>`}).join("");
  prog();
}
function prog(){
  if(MODE==="pick"){const groups=new Set(DATA.refs.map(r=>r.group));const n=[...groups].filter(g=>g in st.picks).length;document.getElementById("prog").textContent=`${n}/${groups.size} decididas`;}
  else{const n=DATA.refs.filter(r=>st.ratings[r.id]&&st.ratings[r.id].score).length;document.getElementById("prog").textContent=`${n}/${DATA.refs.length} puntuadas`;}
}
/* ---------- modo rate (Fase 4) ---------- */
let filt="all", grp="all", cur=null;
function renderRate(){
  document.getElementById("legend").textContent="Puntúa de 1 a 10. 9–10: es mi referencia · 6–8: me gusta · 1–5: no me gusta, hay que evitarlo. Atajo: pasa el ratón por una tarjeta y pulsa 1–9 (0 = 10). El avance se guarda solo; al terminar, «Descargar resultado».";
  const groups=[...new Set(DATA.refs.map(r=>r.group))];
  document.getElementById("filters").innerHTML=`<select id="f"><option value="all">Todas</option><option value="todo">Pendientes</option><option value="hi">Gustan (6+)</option><option value="lo">Evitar (≤5)</option></select> <select id="g"><option value="all">Todas las tandas</option>${groups.map(g=>`<option>${esc(g)}</option>`).join("")}</select>`;
  document.getElementById("f").value=filt;document.getElementById("g").value=grp;
  document.getElementById("f").onchange=e=>{filt=e.target.value;draw()};document.getElementById("g").onchange=e=>{grp=e.target.value;draw()};
  draw();
}
function draw(){
  const list=DATA.refs.filter(r=>{const s=(st.ratings[r.id]||{}).score;
    if(grp!=="all"&&r.group!==grp)return false;
    return filt==="all"||(filt==="todo"&&!s)||(filt==="hi"&&s>=6)||(filt==="lo"&&s&&s<=5)});
  document.getElementById("main").innerHTML=`<div class="grid">${list.map(r=>{const v=st.ratings[r.id]||{};
    return `<div class="card" data-id="${esc(r.id)}">${thumb(r)}<div class="meta">${info(r)}
    <div class="scale">${[1,2,3,4,5,6,7,8,9,10].map(n=>`<button data-s="${n}" class="${v.score===n?"on "+(n>=6?"hi":"lo"):""}">${n}</button>`).join("")}</div>
    <input class="note" data-note="${esc(r.id)}" placeholder="Nota (sobre todo en 1–2 y 9–10)" value="${esc(v.note||"")}"></div></div>`}).join("")}</div>`;
  prog();
}
/* ---------- eventos ---------- */
document.addEventListener("click",e=>{
  const b=e.target.closest("button");if(!b)return;
  if(b.dataset.pick){st.picks[b.dataset.g]=b.dataset.pick;save();renderPick();}
  else if(b.dataset.none!==undefined){st.picks[b.dataset.none]=null;save();renderPick();}
  else if(b.dataset.s){const id=b.closest(".card").dataset.id;const v=st.ratings[id]=st.ratings[id]||{};v.score=+b.dataset.s;save();const sy=window.scrollY;draw();window.scrollTo(0,sy);}
});
document.addEventListener("input",e=>{
  if(e.target.dataset.reason!==undefined){st.reasons[e.target.dataset.reason]=e.target.value;save();}
  if(e.target.dataset.note){const id=e.target.dataset.note;const v=st.ratings[id]=st.ratings[id]||{};v.note=e.target.value;save();}
});
document.addEventListener("mouseover",e=>{const c=e.target.closest(".card");cur=c?c.dataset.id:null});
document.addEventListener("keydown",e=>{
  if(MODE!=="rate"||!cur||/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName))return;
  if(/^[0-9]$/.test(e.key)){const v=st.ratings[cur]=st.ratings[cur]||{};v.score=e.key==="0"?10:+e.key;save();
    const sy=window.scrollY;draw();window.scrollTo(0,sy);}
});
document.getElementById("export").onclick=()=>{
  const out=MODE==="pick"?{mode:"pick",picks:st.picks,reasons:st.reasons}:{mode:"rate",ratings:Object.fromEntries(Object.entries(st.ratings).filter(([k,v])=>v.score))};
  const url=URL.createObjectURL(new Blob([JSON.stringify(out,null,1)],{type:"application/json"}));
  const a=document.createElement("a");a.href=url;a.download=MODE==="pick"?"picks.json":"ratings.json";a.click();
};
MODE==="pick"?renderPick():renderRate();
</script></body></html>
"""


def cmd_board(a):
    data = load(a.file)
    p = data["profile"]
    if a.mode == "pick":
        refs = [r for r in data["refs"] if r.get("phase") == "explore"]
        title = "Elige 1 de cada 5"
    else:
        refs = to_rate(data["refs"])
        random.Random(7).shuffle(refs)  # orden mezclado y estable: el contraste no va en bloque
        title = "Puntúa del 1 al 10"
    if not refs:
        die("no hay referencias para este modo (¿phase correcta?)")
    keep = ("id", "url", "title", "author", "platform", "thumb", "group", "tags", "tipologia", "note")
    slim = [{k: r.get(k) for k in keep} for r in refs]
    sub = " · ".join(x for x in (p.get("oficio"), p.get("uso"), p.get("foco")) if x)
    key = slug(f"{p.get('oficio')}-{p.get('uso')}-{p.get('foco')}")[:60] or "board"
    payload = json.dumps({"mode": a.mode, "slug": key, "refs": slim}, ensure_ascii=False).replace("</", "<\\/")
    out = (BOARD.replace("__TITLE__", html.escape(title)).replace("__SUB__", html.escape(sub))
           .replace("__DATA__", payload))
    Path(a.out).write_text(out, encoding="utf-8")
    print(f"Tablero escrito en {a.out} ({len(slim)} referencias, modo {a.mode})")


# ----------------------------------------------------------------------------- apply
def cmd_apply(a):
    data = load(a.file)
    res = load(a.result)
    by_id = {r["id"]: r for r in data["refs"]}
    if res.get("mode") == "pick":
        prof = data["profile"]
        custom = prof.setdefault("custom_picks", {})
        groups = explore_by_group(data["refs"])
        for g, rid in (res.get("picks") or {}).items():
            if g not in groups:
                print("AVISO: dimensión desconocida", g)
                continue
            for r in groups[g]:
                r["picked"] = r["id"] == rid
            custom.pop(g, None)
            if rid is None:
                custom[g] = None
        reasons = {g: t for g, t in (res.get("reasons") or {}).items() if t}
        prof.setdefault("pick_reasons", {}).update(reasons)
        save(a.file, data)
        print_seeds(data)
    else:
        n = 0
        for rid, v in (res.get("ratings") or {}).items():
            if rid not in by_id:
                print("AVISO: id desconocido", rid)
                continue
            s = v.get("score")
            if not isinstance(s, int) or not 1 <= s <= 10:
                print(f"AVISO: {rid} con nota no válida ({s!r}), se ignora")
                continue
            by_id[rid]["score"] = s
            if v.get("note"):
                by_id[rid]["user_note"] = v["note"]
            n += 1
        save(a.file, data)
        pending = [r for r in to_rate(data["refs"]) if r.get("score") is None]
        print(f"{n} puntuaciones aplicadas · faltan {len(pending)}")


# ----------------------------------------------------------------------------- análisis
def analyze(data, min_n, min_diff=1.0):
    """Criterio por dimensión.

    Como cada pieza se puntúa entera, una tipología solo cuenta como norma si puntúa claramente por encima del
    resto de su dimensión (diferencia >= min_diff); si no, la dimensión queda «sin preferencia clara». La fuerza
    de la evidencia es «fuerte» si además |t| >= 2 (t de Welch) y «débil» si no.
    """
    refs = data["refs"]
    rated = [r for r in refs if r.get("score") is not None]
    seeds = {slug(g): (slug(t), t) for g, t in seeds_of(data).items()}
    labels = {}
    for r in refs:
        if r.get("phase") == "explore" and r.get("tipologia"):
            labels[(slug(r["group"]), slug(r["tipologia"]))] = r["tipologia"]
    for g, t in (data["profile"].get("custom_picks") or {}).items():
        if t:
            labels.setdefault((slug(g), slug(t)), t)
    by = defaultdict(lambda: defaultdict(list))
    for r in rated:
        for t in set(r.get("tags") or []):
            st = split_tag(t)
            if st:
                by[st[0]][st[1]].append(r)
                labels.setdefault((st[0], st[1]), st[2])
    result = []
    for dim in dimensions(refs):
        ds = slug(dim)
        uniq = {r["id"]: r for rs in by.get(ds, {}).values() for r in rs}
        rows = []
        for ts, rs in by.get(ds, {}).items():
            ids = {r["id"] for r in rs}
            xs = [r["score"] for r in rs]
            diff, t = contrast_vs_rest(xs, [r["score"] for i, r in uniq.items() if i not in ids])
            rows.append({"label": labels[(ds, ts)], "slug": ts, "n": len(xs), "mean": mean(xs),
                         "like": sum(1 for x in xs if x >= LIKE_MIN) / len(xs), "diff": diff,
                         "strength": "fuerte" if abs(t) >= 2 else "débil", "refs": rs})
        rows.sort(key=lambda x: (-x["mean"], -x["n"]))
        solid = [x for x in rows if x["n"] >= min_n]
        winners = sorted((x for x in solid if x["diff"] >= min_diff and x["mean"] >= LIKE_MIN), key=lambda x: -x["diff"])
        best = winners[0] if winners else None
        also = [x for x in winners[1:] if x["mean"] >= 7]
        avoid = [x for x in solid if x["diff"] <= -min_diff and x["mean"] <= LIKE_MIN - 1]
        seed_slug, seed_label = seeds.get(ds, (None, None))
        seed_row = next((x for x in rows if x["slug"] == seed_slug), None)
        if not seed_label:
            status = None
        elif not seed_row or seed_row["n"] < min_n:
            status = "sin datos"
        elif best and best["slug"] == seed_slug:
            status = "se confirma"
        elif seed_row["diff"] >= min_diff and seed_row["mean"] >= LIKE_MIN:
            status = "se confirma, aunque otra puntúa algo más"
        elif best:
            status = "no se confirma"
        else:
            status = "sin preferencia clara"
        norm_ids = {r["id"] for r in best["refs"]} if best else set()
        avoid_ids = {r["id"] for x in avoid for r in x["refs"]}
        hi = sorted((uniq[i] for i in norm_ids if uniq[i]["score"] >= LIKE_MIN), key=lambda r: -r["score"])[:3]
        lo = sorted((uniq[i] for i in avoid_ids if uniq[i]["score"] < LIKE_MIN), key=lambda r: r["score"])[:3]
        result.append({
            "name": dim, "rows": rows, "best": best, "also": also, "avoid": avoid,
            "seed_label": seed_label, "seed_row": seed_row, "seed_status": status,
            "anchors_hi": hi, "anchors_lo": lo, "n_refs": len(uniq), "min_diff": min_diff,
        })
    return result


def dimension_md(d, min_n, level="###", with_anchors=False):
    out = [f"{level} {d['name']}", ""]
    if not d["rows"]:
        out += ["_Ninguna referencia puntuada lleva tags de esta dimensión: por explorar._", ""]
        return out
    seed_slug = d["seed_row"]["slug"] if d["seed_row"] else None
    out += ["| tipología | n | media | dif. vs resto | % gustan |", "|---|---|---|---|---|"]
    for x in d["rows"]:
        star = " ★" if x["slug"] == seed_slug else ""
        out.append(f"| {x['label']}{star} | {x['n']} | {x['mean']:.1f} | {signed(x['diff'])} | {x['like']:.0%} |")
    out.append("")
    b = d["best"]
    if b:
        out.append(f"- **Norma candidata:** {b['label']} (media {b['mean']:.1f}, {signed(b['diff'])} sobre el resto, "
                   f"n={b['n']}, evidencia {b['strength']}).")
    else:
        out.append(f"- **Sin preferencia clara:** ninguna tipología supera al resto por {d['min_diff']:g} punto{'' if d['min_diff'] == 1 else 's'} o más "
                   f"(con n≥{min_n}). No la conviertas en norma: déjala libre o usa la elección de la Fase 2 como preferencia suave.")
    if d["also"]:
        out.append("- **También le funcionan:** " + "; ".join(f"{x['label']} ({x['mean']:.1f})" for x in d["also"]) + ".")
    if d["avoid"]:
        out.append("- **Evitar:** " + "; ".join(f"{x['label']} (media {x['mean']:.1f}, {signed(x['diff'])}, n={x['n']}, "
                                              f"evidencia {x['strength']})" for x in d["avoid"]) + ".")
    if d["seed_label"]:
        sr = d["seed_row"]
        verdict = {"se confirma": "se confirma",
                   "se confirma, aunque otra puntúa algo más": "se confirma, aunque otra puntúa algo más",
                   "no se confirma": "**no se confirma**: puntúa mejor otra; pregúntale",
                   "sin preferencia clara": "la dimensión no marca diferencia en sus notas; vale como preferencia suave",
                   "sin datos": f"menos de {min_n} referencias puntuadas con esa tipología; busca más"}[d["seed_status"]]
        out.append(f"- **Elegida en la Fase 2:** {d['seed_label']}" + (f" (media {sr['mean']:.1f}, n={sr['n']})" if sr else "")
                   + f" → {verdict}.")
    if with_anchors:
        def a(r):
            note = f" — «{r['user_note']}»" if r.get("user_note") else ""
            return f"[{r.get('title') or r['id']}]({r['url']}) ({r['score']}){note}"
        if d["anchors_hi"]:
            out.append("- **Anclas del sí** (con la norma): " + " · ".join(a(r) for r in d["anchors_hi"]))
        if d["anchors_lo"]:
            out.append("- **Anclas del no** (con lo que evitar): " + " · ".join(a(r) for r in d["anchors_lo"]))
    out.append("")
    return out


def cmd_stats(a):
    data = load(a.file)
    refs, p = data["refs"], data["profile"]
    rated = [r for r in refs if r.get("score") is not None]
    if not rated:
        die("no hay referencias puntuadas todavía")
    scores = [r["score"] for r in rated]
    gm = mean(scores)
    hi = sum(1 for s in scores if s >= LIKE_MIN)
    dist = Counter(scores)
    out = [f"# Análisis — {p.get('oficio')} · {p.get('uso') or '—'} · {p.get('foco')}", "",
           f"Puntuadas: {len(rated)} · media {gm:.2f} · gustan (6-10): {hi} ({hi / len(rated):.0%}) · "
           f"evitar (1-5): {len(rated) - hi}",
           "Distribución: " + " ".join(f"{n}:{dist.get(n, 0)}" for n in range(1, 11))]
    if hi / len(rated) > 0.85:
        out.append("\n> AVISO: casi todo está entre 6 y 10. Falta contraste y el «evitar» será débil: añade una ronda corta de contraste.")
    if hi / len(rated) < 0.15:
        out.append("\n> AVISO: casi todo está entre 1 y 5. La búsqueda no ha dado con su gusto: revisa semillas y consultas.")

    dims = analyze(data, a.min_n, a.min_diff)
    if dims:
        out += ["", "## Criterio por dimensión", "",
                f"★ = elegida en la Fase 2 · «dif. vs resto» = su media menos la del resto de la dimensión · norma = "
                f"supera al resto por {a.min_diff:g} o más con n≥{a.min_n} · evitar = queda {a.min_diff:g} o más por debajo "
                f"y su media es ≤{LIKE_MIN - 1}", ""]
        for d in dims:
            out += dimension_md(d, a.min_n, with_anchors=True)

    dim_slugs = {slug(d["name"]) for d in dims}
    loose = defaultdict(list)
    for r in rated:
        for t in set(r.get("tags") or []):
            st = split_tag(t)
            if not st or st[0] not in dim_slugs:
                loose[t].append(r["score"])
    ev = [(t, xs) for t, xs in loose.items() if len(xs) >= a.min_n]
    out += ["## Rasgos sueltos (tags fuera de las dimensiones)", ""]
    for title, rows in ((f"Le gustan (media ≥7, n≥{a.min_n})", sorted([x for x in ev if mean(x[1]) >= 7], key=lambda x: -mean(x[1]))),
                        (f"Evitar (media ≤5, n≥{a.min_n})", sorted([x for x in ev if mean(x[1]) <= 5], key=lambda x: mean(x[1])))):
        out.append(f"**{title}:** " + ("; ".join(f"{t} ({mean(xs):.1f}, n={len(xs)})" for t, xs in rows) if rows else "nada con evidencia suficiente"))
    out.append("")
    plat = defaultdict(list)
    for r in rated:
        plat[r.get("platform")].append(r["score"])
    out += ["## Por plataforma", "", "| plataforma | n | media | % gustan |", "|---|---|---|---|"]
    for k, xs in sorted(plat.items(), key=lambda x: -mean(x[1])):
        out.append(f"| {k} | {len(xs)} | {mean(xs):.1f} | {sum(1 for x in xs if x >= LIKE_MIN) / len(xs):.0%} |")
    reasons = p.get("pick_reasons")
    if reasons:
        out += ["", "## Motivos que dio en la Fase 2", ""] + [f"- **{g}**: {t}" for g, t in reasons.items()]
    notes = sorted((r for r in rated if r.get("user_note")), key=lambda r: -r["score"])
    if notes:
        out += ["", "## Sus notas al puntuar", ""] + [f"- ({r['score']}) {r.get('title') or r['id']}: {r['user_note']}" for r in notes]
    print("\n".join(out))


# ----------------------------------------------------------------------------- export-skill
def cmd_export(a):
    data = load(a.file)
    p = data["profile"]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rated = [r for r in data["refs"] if r.get("score") is not None]
    if not rated:
        die("no hay referencias puntuadas todavía")

    def line(r):
        extra = f" — «{r['user_note']}»" if r.get("user_note") else ""
        author = f" · {r['author']}" if r.get("author") else ""
        return f"- **{r['score']}** [{r.get('title') or r['id']}]({r['url']}){author} · {r['platform']}{extra}"

    def write(name, title, intro, items):
        by_g = defaultdict(list)
        for r in items:
            by_g[r["group"]].append(r)
        lines = [f"# {title}", "", intro, ""]
        for g, rs in by_g.items():
            lines += [f"## {g}", ""] + [line(r) for r in rs] + [""]
        (out / name).write_text("\n".join(lines), encoding="utf-8")

    write("referencias-gustan.md", "Referencias que le gustan (6-10)",
          "Ordenadas por puntuación dentro de cada tanda. Son la vara de medir de lo que SÍ.",
          sorted([r for r in rated if r["score"] >= LIKE_MIN], key=lambda r: -r["score"]))
    write("referencias-evitar.md", "Referencias a evitar (1-5)",
          "Ordenadas de peor a menos mala. Son la vara de medir de lo que NO.",
          sorted([r for r in rated if r["score"] < LIKE_MIN], key=lambda r: r["score"]))

    dims = analyze(data, a.min_n, a.min_diff)
    crit = [f"# Criterio por dimensión — {p.get('oficio')} · {p.get('uso') or '—'} · {p.get('foco')}", "",
            f"Generado el {datetime.date.today().isoformat()} con {len(rated)} referencias puntuadas del 1 al 10 "
            f"(6-10 le gusta · 1-5 evitar). ★ = elegida en la Fase 2. Es la evidencia de las normas de `SKILL.md`.", ""]
    for i, d in enumerate(dims, 1):
        d = dict(d, name=f"{i}. {d['name']}")
        crit += dimension_md(d, a.min_n, level="##", with_anchors=True)
    (out / "criterio-por-dimension.md").write_text("\n".join(crit), encoding="utf-8")

    keep = ("id", "url", "title", "author", "platform", "group", "tipologia", "tags", "score", "user_note", "license", "phase")
    save(out / "referencias.json", {"profile": p, "refs": [{k: r.get(k) for k in keep} for r in rated]})
    print(f"Exportado a {out}/: criterio-por-dimension.md, referencias-gustan.md, referencias-evitar.md, referencias.json")


# ----------------------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)

    x = s.add_parser("init", help="crea refs.json con el encuadre")
    x.add_argument("--dir", required=True)
    x.add_argument("--oficio", required=True)
    x.add_argument("--foco", required=True, help="sector")
    x.add_argument("--uso")
    x.add_argument("--canal")
    x.add_argument("--keyword", help="estilo (opcional)")
    x.add_argument("--modo", help="'extensión de Chrome' (por defecto) o 'reducido'")
    x.add_argument("--force", action="store_true")
    x.set_defaults(f=cmd_init)

    x = s.add_parser("add", help="añade una tanda de referencias (JSON: lista u {refs: [...]}; '-' = stdin)")
    x.add_argument("file")
    x.add_argument("batch")
    x.add_argument("--phase", choices=["explore", "search"], required=True)
    x.set_defaults(f=cmd_add)

    x = s.add_parser("validate", help="comprueba esquema, duplicados y mínimos")
    x.add_argument("file")
    x.add_argument("--stage", choices=["any", "explore", "search"], default="any")
    x.add_argument("--min", type=int, default=SEARCH_MIN)
    x.set_defaults(f=cmd_validate)

    x = s.add_parser("board", help="tablero HTML: pick (Fase 2) o rate (Fase 4)")
    x.add_argument("file")
    x.add_argument("--mode", choices=["pick", "rate"], required=True)
    x.add_argument("--out", required=True)
    x.set_defaults(f=cmd_board)

    x = s.add_parser("pick", help='Fase 2 por encuesta: "Dimensión=A" | "Dimensión=Tipología" | "Dimensión=ninguna" | "Dimensión=texto propio"')
    x.add_argument("file")
    x.add_argument("assign", nargs="+", metavar="DIMENSION=VALOR")
    x.add_argument("--reason", action="append", metavar="DIMENSION=MOTIVO")
    x.set_defaults(f=cmd_pick)

    x = s.add_parser("apply", help="aplica picks.json o ratings.json descargados del tablero")
    x.add_argument("file")
    x.add_argument("result")
    x.set_defaults(f=cmd_apply)

    x = s.add_parser("score", help="Fase 4 por encuesta: s001=9 s002=3 …")
    x.add_argument("file")
    x.add_argument("assign", nargs="+", metavar="ID=NOTA")
    x.add_argument("--note", action="append", metavar="ID=TEXTO")
    x.set_defaults(f=cmd_score)

    x = s.add_parser("status", help="en qué fase está y qué falta")
    x.add_argument("file")
    x.set_defaults(f=cmd_status)

    x = s.add_parser("stats", help="análisis en Markdown")
    x.add_argument("file")
    x.add_argument("--min-n", type=int, default=3)
    x.add_argument("--min-diff", type=float, default=1.0, help="puntos por encima del resto para ser norma")
    x.set_defaults(f=cmd_stats)

    x = s.add_parser("export-skill", help="referencias y criterio por dimensión para la skill final")
    x.add_argument("file")
    x.add_argument("--out", required=True)
    x.add_argument("--min-n", type=int, default=3)
    x.add_argument("--min-diff", type=float, default=1.0)
    x.set_defaults(f=cmd_export)

    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
