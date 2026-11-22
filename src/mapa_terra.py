"""Gera a máscara de terra do planeta (assets/esfr/terra_mapa.png) a partir do Natural Earth (domínio público).

Roda no GitHub Actions (workflow mapa-terra.yml), que tem acesso à internet. A imagem é equirretangular:
x = longitude (-180 a 180), y = latitude (90 a -90). Branco = terra, preto = mar. Os globos do E Se Fosse Real?
(src/globo.py) leem essa máscara para desenhar os continentes com o formato certo."""
import json
import urllib.request

from PIL import Image, ImageDraw

from .util import RAIZ

URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_land.geojson"
W, H = 2048, 1024


def _xy(lon, lat):
    return (lon + 180) / 360 * W, (90 - lat) / 180 * H


def main():
    dados = json.loads(urllib.request.urlopen(URL, timeout=120).read())
    img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(img)
    n = 0
    for f in dados["features"]:
        g = f["geometry"]
        polis = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poli in polis:
            for k, anel in enumerate(poli):
                pts = [_xy(lon, lat) for lon, lat in anel]
                if len(pts) > 2:
                    d.polygon(pts, fill=255 if k == 0 else 0)   # 1º anel é a terra; os outros são lagos/buracos
                    n += 1
    destino = RAIZ / "assets" / "esfr" / "terra_mapa.png"
    destino.parent.mkdir(parents=True, exist_ok=True)
    img.save(destino, optimize=True)
    print(f"{n} polígonos -> {destino} ({destino.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
