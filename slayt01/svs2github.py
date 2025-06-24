# Güncellenmiş: svs2github.py

import os
from openslide import OpenSlide, deepzoom
from PIL import Image
from pathlib import Path

# === Ayarlar ===
tile_size = 2048
tile_overlap = 0
jpeg_quality = 85
limit_levels = 3
output_root = Path("github")
output_root.mkdir(exist_ok=True)

# === HTML şablonları ===
VIEWER_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <title>{slide_title}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/openseadragon.min.js"></script>
  <style>
    html, body, #viewer {{
      height: 100%;
      margin: 0;
      background: black;
    }}
    #viewer {{
      background: url('preview.jpg') center center no-repeat;
      background-size: contain;
    }}
  </style>
</head>
<body>
  <div id="viewer"></div>
  <script>
    OpenSeadragon({{
      id: "viewer",
      prefixUrl: "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/images/",
      tileSources: "{dzi_file}"
    }});
  </script>
</body>
</html>
"""

MAIN_INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slayt Galerisi</title>
  <style>
    body {{
      font-family: sans-serif;
      background: #f5f5f5;
      padding: 2rem;
    }}
    h1 {{
      text-align: center;
    }}
    ul {{
      list-style: none;
      padding: 0;
      max-width: 600px;
      margin: auto;
    }}
    li {{
      margin-bottom: 1rem;
    }}
    a {{
      display: block;
      padding: 1rem;
      background: white;
      border-radius: 8px;
      text-decoration: none;
      color: #333;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
    a:hover {{
      background: #e0f7fa;
    }}
  </style>
</head>
<body>
  <h1>🧬 Slayt Galerisi</h1>
  <ul>
    {items}
  </ul>
</body>
</html>
"""

def create_dzi_file(slide, dzi_path, width, height):
    dzi_content = f"""<Image TileSize="{tile_size}" Overlap="{tile_overlap}" Format="jpeg" xmlns="http://schemas.microsoft.com/deepzoom/2008">
  <Size Width="{width}" Height="{height}"/>
</Image>"""
    with open(dzi_path, "w", encoding="utf-8") as f:
        f.write(dzi_content)

def process_svs(svs_path, slide_dir, slide_name):
    slide = OpenSlide(svs_path)
    dzi_path = slide_dir / f"{slide_name}.dzi"
    files_dir = slide_dir / f"{slide_name}_files"
    dz = deepzoom.DeepZoomGenerator(slide, tile_size=tile_size, overlap=tile_overlap)
    max_level = dz.level_count
    selected_levels = list(range(max_level - limit_levels, max_level))

    for level in selected_levels:
        cols, rows = dz.level_tiles[level]
        for col in range(cols):
            for row in range(rows):
                tile = dz.get_tile(level, (col, row))
                tile_path = files_dir / str(level) / f"{col}_{row}.jpeg"
                tile_path.parent.mkdir(parents=True, exist_ok=True)
                tile.save(tile_path, format="JPEG", quality=jpeg_quality)

    create_dzi_file(slide, dzi_path, *slide.dimensions)

    # Önizleme küçük görsel
    preview_path = slide_dir / "preview.jpg"
    thumb = slide.get_thumbnail((1024, 1024))
    thumb.save(preview_path, format="JPEG", quality=85)

    html_path = slide_dir / "index.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(VIEWER_TEMPLATE.format(slide_title=slide_name, dzi_file=f"{slide_name}.dzi"))

    print(f"✅ {slide_name} işlendi.")
    return slide_name

def generate_main_index(slide_names):
    items = [f'<li><a href="{name}/index.html">{name}</a></li>' for name in sorted(slide_names)]
    index_html = MAIN_INDEX_TEMPLATE.format(items="\n    ".join(items))
    with open(output_root / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("📄 Ana index.html güncellendi.")

def main():
    existing_dirs = {p.name for p in output_root.iterdir() if (p / "index.html").exists()}
    existing_max = max([int(d.replace("slayt", "")) for d in existing_dirs if d.startswith("slayt") and d.replace("slayt", "").isdigit()] + [0])
    new_svs_files = sorted(Path(".").glob("*.svs"))
    slide_names = list(existing_dirs)

    for i, svs_path in enumerate(new_svs_files, start=existing_max + 1):
        slide_name = f"slayt{i:02d}"
        slide_dir = output_root / slide_name
        slide_names.append(process_svs(svs_path, slide_dir, slide_name))
        os.remove(svs_path)

    generate_main_index(slide_names)

main()
