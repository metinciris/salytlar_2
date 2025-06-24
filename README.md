# 🧬 SVS2GitHub – Slayt Yayınlama Aracı

Bu proje, `.svs` formatındaki sanal mikroskop slaytlarını otomatik olarak web sayfası haline getirir.  
Her slayt ayrı bir klasöre işlenir, önizleme resmi ve zoom yapılabilir görüntüleyiciyle birlikte yayınlanabilir hale gelir.

## 🚀 Özellikler

- `.svs` dosyalarını OpenSlide kullanarak işler
- Her slaytı `slayt01`, `slayt02`, ... gibi sıralı klasörlerde saklar
- Karoları `.dzi` formatında üretir (Deep Zoom)
- Her slayt klasörüne:
  - `index.html` (OpenSeadragon ile görüntüleyici)
  - `preview.jpg` (ilk açılışta siyah ekranı önler)
  - `.dzi` + `*_files/` (tile klasörleri)
- Ana `index.html` sayfası varsa silinmez, yeni slaytlar **altına eklenir**
- Kullanıcıdan klasör adı ve başlangıç slayt numarası istenir, sonra otomatik hatırlanır
- İşlenen `.svs` dosyaları otomatik silinir

## 📦 Gereksinimler

```bash
pip install openslide-bin pillow
````

## ▶️ Kullanım

1. `svs2github.py` dosyasını `.svs` dosyalarının bulunduğu klasöre koyun
2. Komut satırında çalıştırın:

```bash
python svs2github.py
```

3. Aşağıdaki gibi sorulara yanıt verin:

```
Klasör adı (github):
Başlangıç slayt numarası (1):
```

4. Her `.svs` dosyası işlendikçe:

   * `github/slayt01/`, `github/slayt02/`... klasörleri oluşur
   * `github/index.html` sayfası güncellenir
   * `.svs` dosyası silinir

## 🌐 Yayına Alma

Üretilen `github/` klasörünü doğrudan GitHub Pages’e yükleyebilirsiniz.

Örnek URL:

```
https://kullaniciadi.github.io/repoadi/github/index.html
```

## 📁 Örnek Dizin Yapısı

```
github/
├── index.html               ← Ana galeri sayfası
├── slayt01/
│   ├── index.html
│   ├── slayt01.dzi
│   ├── preview.jpg
│   └── slayt01_files/
│       └── 13/0_0.jpeg ...
├── slayt02/
│   └── ...
```

## ✏️ Ayar Dosyası

Kullanıcı ayarları `svs2github_config.txt` dosyasında saklanır.
Bir sonraki çalıştırmada klasör adı ve slayt numarası otomatik hatırlanır.

---

👨‍⚕️ Geliştirici: Prof. Dr. Metin Çiriş
🔬 Alan: Patoloji – Dijital slayt sistemleri

```
