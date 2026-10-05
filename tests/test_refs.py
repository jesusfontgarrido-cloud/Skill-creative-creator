"""Pruebas de creador-skills-creativas/scripts/refs.py (solo librería estándar).

Ejecuta: python3 -m unittest discover tests
"""
import importlib.util
import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "creador-skills-creativas" / "scripts" / "refs.py"
spec = importlib.util.spec_from_file_location("refs", SCRIPT)
refs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refs)

DIMS = {
    "Logotipo": ["Solo tipográfico", "Símbolo + nombre", "Sello o emblema", "Monograma", "Logo variable"],
    "Tipografía principal": ["Serif editorial", "Sans neutra", "Display con carácter", "Manuscrita", "Monoespaciada"],
    "Color": ["Monocromo", "Tierra cálida", "Contraste vivo", "Pastel", "Negro con un acento"],
}
for k in range(4, 11):
    DIMS[f"Dimensión {k}"] = [f"Tipo {k}{j}" for j in "ABCDE"]


def run(*args, ok=True, stdin=None):
    p = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True, input=stdin)
    if ok and p.returncode != 0:
        raise AssertionError(f"falló {args}:\n{p.stdout}\n{p.stderr}")
    return p


class Utilidades(unittest.TestCase):
    def test_urls(self):
        self.assertEqual(refs.norm_url("HTTPS://WWW.Behance.net/p/4/?utm_source=x&fbclid=1"), "https://behance.net/p/4")
        self.assertEqual(refs.norm_url("https://youtube.com/watch?v=abc&si=Z&pp=1"),
                         refs.norm_url("https://www.youtube.com/watch?v=abc"))
        self.assertEqual(refs.clean_url("https://a.com/x?utm_medium=b&id=3#frag"), "https://a.com/x?id=3")
        self.assertTrue(refs.is_http("HTTPS://a.com"))
        self.assertFalse(refs.is_http("ftp://a.com"))

    def test_platform_slug_tags(self):
        self.assertEqual(refs.platform_of("https://es.pinterest.com/pin/1"), "pinterest")
        self.assertEqual(refs.platform_of("https://www.campaignlive.co.uk/a"), "campaignlive")
        self.assertEqual(refs.slug("Tipografía Principal"), "tipografia-principal")
        self.assertEqual(refs.split_tag("COLOR: Tierra cálida")[:2], ("color", "tierra-calida"))
        self.assertIsNone(refs.split_tag("sin dos puntos"))
        self.assertEqual(refs.signed(-0.04), "+0.0")


class Flujo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.db = self.dir / "ws" / "refs.json"
        run("init", "--dir", self.dir / "ws", "--oficio", "Diseñador gráfico", "--foco", "Gastronomía",
            "--uso", "Branding e identidad", "--canal", "Impreso", "--keyword", "Artesanal")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, data):
        path = self.dir / name
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return path

    def explore(self):
        batch, n = [], 0
        for g, tips in DIMS.items():
            for t in tips:
                n += 1
                batch.append({"url": f"https://www.behance.net/gallery/{n}", "title": f"Ejemplo {t}", "group": g,
                              "tipologia": t, "note": f"Frase de {t}", "thumb": f"https://img.example/{n}.jpg"})
        run("add", self.db, self.write("explore.json", batch), "--phase", "explore")

    def search(self, n=210):
        rnd = random.Random(3)
        batch = []
        plats = ["behance.net", "pinterest.com", "dribbble.com", "brandnew.underconsideration.com"]
        for i in range(n):
            batch.append({
                "url": f"https://{plats[i % 4]}/p/{i}?utm_source=x", "title": f"Pieza {i}", "group": "Color",
                "tags": [f"Tipografía principal:{rnd.choice(DIMS['Tipografía principal'])}",
                         f"color:{rnd.choice(DIMS['Color']).upper()}",
                         f"Logotipo:{rnd.choice(DIMS['Logotipo'])}"],
                "contrast": i % 5 == 0})
        run("add", self.db, self.write("search.json", batch), "--phase", "search")

    def rate_all(self):
        rnd = random.Random(5)
        data = json.loads(self.db.read_text(encoding="utf-8"))
        ratings = {}
        for r in refs.to_rate(data["refs"]):
            tags = " ".join(r["tags"]).lower()
            s = 5 + 3 * ("serif editorial" in tags) - 3 * ("monoespaciada" in tags) + 2 * ("tierra cálida" in tags)
            ratings[r["id"]] = {"score": max(1, min(10, s + rnd.randint(-1, 1)))}
        first = list(ratings)[:3]
        for k in first:
            ratings.pop(k)
        run("apply", self.db, self.write("ratings.json", {"mode": "rate", "ratings": ratings}))
        run("score", self.db, *[f"{k}=7" for k in first], "--note", f"{first[0]}=me recuerda a casa")

    def test_flujo_completo(self):
        self.explore()
        self.assertIn("OK", run("validate", self.db, "--stage", "explore").stdout)
        run("board", self.db, "--mode", "pick", "--out", self.dir / "elegir.html")

        out = run("pick", self.db, "Logotipo=B", "tipografia=serif editorial", "3=Etiquetas pintadas a mano",
                  "4=ninguna", *[f"{k}=A" for k in range(5, 11)], "--reason", "Color=me recuerda a las tabernas").stdout
        self.assertIn("Logotipo: Símbolo + nombre", out)
        self.assertIn("Tipografía principal: Serif editorial", out)
        self.assertIn("Color: Etiquetas pintadas a mano (propia)", out)
        self.assertIn("Dimensión 4: ninguna", out)

        self.search()
        dup = run("add", self.db, "-", "--phase", "search",
                  stdin=json.dumps([{"url": "HTTPS://WWW.Behance.net/p/0/?fbclid=zz", "group": "Color"}]))
        self.assertIn("repetidas descartadas 1", dup.stdout)
        self.assertIn("OK", run("validate", self.db, "--stage", "search").stdout)
        self.assertNotIn("utm_", self.db.read_text(encoding="utf-8"))

        run("board", self.db, "--mode", "rate", "--out", self.dir / "puntuar.html")
        self.rate_all()
        self.assertIn("Fases 5-6", run("status", self.db).stdout)

        stats = run("stats", self.db).stdout
        logo = stats.split("### Logotipo")[1].split("###")[0]
        tipo = stats.split("### Tipografía principal")[1].split("###")[0]
        color = stats.split("### Color")[1].split("###")[0]
        self.assertIn("Sin preferencia clara", logo)            # dimensión que no influye en la nota
        self.assertIn("Norma candidata:** Serif editorial", tipo)
        self.assertIn("evidencia fuerte", tipo)
        self.assertIn("Evitar:** Monoespaciada", tipo)
        self.assertIn("Norma candidata:** Tierra cálida", color)
        self.assertIn("Etiquetas pintadas a mano", color)         # tipología propia de la Fase 2
        self.assertIn("se confirma", tipo)

        out_dir = self.dir / "skill" / "references"
        run("export-skill", self.db, "--out", out_dir)
        for f in ("criterio-por-dimension.md", "referencias-gustan.md", "referencias-evitar.md", "referencias.json"):
            self.assertTrue((out_dir / f).exists(), f)
        self.assertIn("Anclas del sí", (out_dir / "criterio-por-dimension.md").read_text(encoding="utf-8"))

    def test_errores(self):
        bad = [{"url": f"https://a.com/{i}", "group": "Luz", "tipologia": "Natural"} for i in range(2)]
        run("add", self.db, self.write("bad.json", bad), "--phase", "explore")
        p = run("validate", self.db, "--stage", "explore", ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("repite tipología", p.stdout)
        self.assertNotEqual(run("score", self.db, "e01=11", ok=False).returncode, 0)
        self.assertNotEqual(run("add", self.db, self.write("x.json", [{"url": "ftp://x", "group": "Luz"}]),
                                "--phase", "search", ok=False).returncode, 0)

    def test_tablero_escapa_html(self):
        self.explore()
        data = json.loads(self.db.read_text(encoding="utf-8"))
        data["refs"][0]["title"] = "</script><script>alert(1)</script>"
        self.db.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        run("board", self.db, "--mode", "pick", "--out", self.dir / "b.html")
        html = (self.dir / "b.html").read_text(encoding="utf-8")
        self.assertNotIn("</script><script>alert(1)", html)
        self.assertIn("<\\/script>", html)


if __name__ == "__main__":
    unittest.main()
