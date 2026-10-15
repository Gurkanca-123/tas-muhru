# Taş Mührü — Claude çalışma protokolü (kalıcı)

Bu dosya her görevin başında okunur. Amaç: her görevde tüm projeyi yeniden okumadan, yalnız gereken bağlamla çalışmak.
Kısa teknik hafıza: `PROJECT_STATE.md` · görev kayıtları: `CHANGELOG_DEV.md`.

## Her görevde iş akışı
1. `PROJECT_STATE.md`'yi oku (bu dosyadan sonra). Başka belge okuma.
2. Görevi daralt: hangi sistem(ler) etkileniyor? (savaş, düşman, zindan, ödül, kayıt, coop, model/animasyon, arayüz…)
3. İlgili sembolleri `grep -n` ile bul (aşağıdaki "Hedefli okuma"). Bölüm haritası `PROJECT_STATE.md`'de.
4. Yalnız gereken kod aralıklarını oku (genelde 30–150 satır). Değiştirmeden önce mevcut davranışı anla.
5. Küçük, hedefli değişiklik yap. Mevcut mimariyi ve çalışan sistemleri koru.
6. Yalnız etkilenen davranışı doğrula (aşağıdaki "Test").
7. `CHANGELOG_DEV.md`'ye kısa kayıt ekle; mimari / kısıt / bilinen hata değiştiyse `PROJECT_STATE.md`'yi güncelle.

Tüm projeyi baştan incelemek yalnız görev gerçekten mimari çapında bir değişiklik gerektiriyorsa yapılır.

## Kurallar
- Görev kapsamı dışındaki dosyaları okuma.
- `index.html`'i (~5.8 MB, ~17.4k satır) hiçbir görevde baştan sona okuma/analiz etme; tek dosya olması bunu gerektirmez.
- Önceki görevde incelenmiş bir sistemi, yeni görevle ilgisi yoksa yeniden analiz etme (`PROJECT_STATE.md` yeterli).
- Büyük model dosyalarını (`savasci_*.js`, `baltaci_*.js`, `boneking*.js`, `tapinak_*.js` = base64 GLB), base64 verilerini, görselleri
  ve asset klasörlerini açmadan önce gerçekten gerekli mi değerlendir. Genelde gerekmez: modelin klip adları / bağlantı
  noktaları kodda ve `PROJECT_STATE.md`'de yazılı.
- Gereksiz yeniden yazım, geniş refaktör ve tekrarlanan testlerden kaçın.
- Yalnız değişiklikten etkilenmesi muhtemel testleri çalıştır; gerekiyorsa genel testi kullan.
- Gerçekleştirilmemiş bir işlemi (test, push, doğrulama) yapılmış gibi bildirme. Denenmeyeni "denenmedi" diye yaz.
- Tüm oyun metinleri Türkçe ("item" değil "eşya"). Kullanıcıya Türkçe yanıt ver.
- **ÖNCELİK (kullanıcı kararı, 2026-10-15): YÜKSEK GÖRSEL KALİTE.** Zayıf telefon uyumu ve dosya boyutu artık kısıt değil; görsel kalite her şeyden önce gelir
  (son-işleme, PBR/yansıma, gölge, doku, ayrıntılı modeller serbest). Eski "düşük poly / sabit ışık / az gölge" kuralları bağlayıcı değildir.
  Yine de dokunmatik yatay arayüz ve oyun mantığı korunur; 'Performans' ve 'Standart' görünüm seçenekleri isteğe bağlı yedek olarak kalır.
- three.js r158 temel alınır; kalite için gereken ek kod (son-işleme geçişleri vb.) çekirdeğe gömülür. Harici yeni kütüphane eklemeden önce kullanıcıya haber ver.
- Dövüş matematiği, envanter, +0…+9 geliştirme oranları ve joystick mantığına hata düzeltmesi dışında dokunma; denge
  değişiklikleri veri tablolarından (`MOBS`, `RANK`, `mobBase`, `DROP`, `DIFFS`, `TEMPLE_*`) yapılır.
- Kayıt (`applySave`) alan beyaz listesiyle çalışır: yeni kalıcı alan eklersen orada doğrula; mevcut alanları silme.
- Yedekleri koru; eski V12 klasörüne dokunma. Push'tan önce `main`'in yedek dalını aç: `yedek/<iş>-oncesi`.

## Hedefli okuma (index.html)
- Base64 içeren satırlar binlerce karakter: çıktıyı her zaman kes → `grep -n "desen" index.html | cut -c1-200`.
- Bölüm haritası: `grep -n "^// ---------- \|^// =======" index.html | cut -c1-110`.
- Sembol: `grep -n "^function adi\|^const ADI\|  metotAdi(" index.html | cut -c1-160`, sonra `sed -n 'A,Bp' index.html | cut -c1-240`.
- Atlanacak bölgeler: ~2700–7700 (gömülü SkeletonUtils + GLTFLoader, üçüncü taraf), ~7777–7800 (`OUTFIT_DATA` / `GEAR_GLTF`
  base64 GLB'ler), 1–503 (CSS + DOM; yalnız arayüz görevinde).
- Değişiklik betikle yapılabilir: tam eşleşen metni değiştir, eşleşme sayısını doğrula (bkz. araçlar notu).

## Test
- Test betikleri depoda değil (Playwright + başsız Chromium + SwiftShader). Son kopyalar: Masaüstü
  `tas-muhru/tapinak-test/_test/` ve `savasci-70-test/_test/`. Yerel sunucu: depo kökünde `python3 -m http.server 8800`.
- `run.mjs` (36 genel kontrol: sınıflar, eşyalar, Sv 70, düşüşler, Baltacı regresyonu) · `movetest.mjs` (20: yetenek + hareket)
  · `tapinak.mjs` (35: Bronz Taş Tapınağı) · `tapinak_coop.mjs` (13: tapınak misafir olayları) · `tapinak_tris.mjs` (üçgen ölçümü).
- Hızlı sözdizimi: en büyük `<script>` bloğunu çıkar → `node --check`.
- Bilinen kararsızlık: `run.mjs` "Baltacı saldırı ve yetenekleri" (Yer Sarsan) rastgele zindan düzeninde ara sıra kalır; tekrarında geçer.
- Ortak oyun gerçek cihazla bu ortamdan test edilemez (sunucuya erişim yok); simüle edilen olay testlerini "simülasyon" diye bildir.

## Dağıtım
- GitHub `Gurkanca-123/tas-muhru`, `main` → GitHub Pages (gurkanca-123.github.io/tas-muhru). Depo tek dosyalık derlemedir.
- Kullanıcının masaüstündeki yerel proje (`src/*.js` + `build.py` + kendi `CLAUDE.md`'si) bu depoyla eşitli değil; son işler
  doğrudan bu depodaki `index.html`'e uygulandı.
- Yeni asset betiği eklerken `?v=<sha1 ilk 10>` sürüm eki kullan (önbellek).
