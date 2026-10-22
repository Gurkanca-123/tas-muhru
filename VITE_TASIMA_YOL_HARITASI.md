# Taş Mührü — Vite + TypeScript Taşıma Yol Haritası

Gerçek kaynak: bu GitHub deposu (`main`, tek dosyalık `index.html`). Masaüstündeki `src/` + `build.py` eskimiştir; kullanılmaz.
Hedef: oyunu bozmadan, küçük ve doğrulanabilir adımlarla Vite + TypeScript'e geçirmek. Her faz ayrı oturumda yapılabilir.

## Ortak kurallar (her fazda geçerli)
- `CLAUDE.md` ve `PROJECT_STATE.md` önce okunur. `index.html` baştan sona okunmaz; yalnız `grep -n ... | cut -c1-200` ve `sed -n 'A,Bp'` kullanılır.
- Base64 satırları (OUTFIT_DATA / GEAR_GLTF, `savasci_*.js`, `baltaci_*.js`, `boneking*.js`, `tapinak_*.js`) çıktıya düz basılmaz.
- Bir faz bitmeden sonrakine geçilmez. Her fazın sonunda testler çalışır, sonuç `CHANGELOG_DEV.md`'ye yazılır, commit atılır.
- Test edilmeyen şey "denenmedi" diye yazılır. Coop testleri "simülasyon" diye bildirilir.
- Oyun metinleri Türkçe kalır. Dövüş matematiği, envanter, +0…+9 oranları, joystick mantığı ve kayıt alan beyaz listesi (`applySave`) davranışı değişmez.
- Harici yeni kütüphane eklenmeden önce kullanıcıya haber verilir (Vite, TypeScript ve three.js r158 dışında).
- GitHub Pages yayını `main`'den gider; çalışma dalında ilerlenir, `main`'e yalnız kullanıcı onayıyla.

## Faz 0 — Hazırlık (yaklaşık en ucuz faz)
1. `git branch yedek/vite-oncesi main` ve push.
2. Test betiklerini bul: eski dallarda (`git branch -a`, `git log --all -- '*.mjs'`) `run.mjs`, `movetest.mjs`, `tapinak.mjs`, `tapinak_coop.mjs`, `tapinak_tris.mjs` ara. Bulunanları `tests/` altına ekle. Bulunamazsa kullanıcıya haber ver; Masaüstü kopyaları gerekebilir.
3. Mevcut `main` üzerinde testleri çalıştırıp taban sonucu kaydet (36 + 20 + 35 + 13 kontrol; `run.mjs` Yer Sarsan kararsızlığı bilinir).
4. Gömülü varlıkların envanterini çıkar: hangi base64 GLB hangi satırda, kaç bayt, hangi kodla yükleniyor (yalnız adlar ve boyutlar).
   Çıktı: `tests/` içinde çalışır test seti + taban rapor. Henüz kod değişikliği yok.

## Faz 1 — GLB'leri dosyaya çıkarma
1. Base64 GLB'leri `public/assets/models/<ad>.glb` olarak çöz; boyut ve sağlama toplamını kaydet.
2. Yükleme kodunu (GLTFLoader.parse ile base64) dosyadan `fetch`/`load` yapacak şekilde değiştir; model adları, klip adları ve bağlantı noktaları aynı kalır.
3. Yükleme sırasında ilerleme/hata durumunu koru; ağ hatasında anlamlı Türkçe mesaj göster.
4. Yerel sunucuyla (`python3 -m http.server 8800`) testleri çalıştır. Beklenen: aynı sonuç.
5. Önbellek için `?v=<sha1 ilk 10>` eki kullan.
   Not: Bu fazdan sonra oyun `file://` ile açılmaz; sunucu gerekir (README'de belirt).

## Faz 2 — Vite kabuğu
1. `package.json`, `vite.config.ts` (`base: '/tas-muhru/'`), `tsconfig.json` (`allowJs`, `checkJs: false` başlangıçta), `index.html` giriş noktası.
2. Mevcut inline script'i değiştirmeden `src/main.js` olarak taşı; gömülü SkeletonUtils + GLTFLoader yerine `three@0.158` içindeki sürümleri import et (r158 sabit).
3. `npm run build` → `dist/`; statik olarak sunup testleri çalıştır.
4. GitHub Pages dağıtımını (Actions veya `dist` yayını) kullanıcıyla kararlaştır; `main`'e bağlama onay ister.
   Çıktı: Davranışı birebir aynı, ama Vite ile derlenen oyun.

## Faz 3 — Kademeli modüle bölme
Sıra (düşük riskten yükseğe); her madde ayrı commit ve test turu:
1. Veri tabloları: `MOBS`, `RANK`, `mobBase`, `DROP`, `DIFFS`, `TEMPLE_*`, eşya/set tabloları → `src/data/`.
2. Kayıt: `applySave` ve beyaz liste → `src/systems/SaveSystem`.
3. Envanter ve eşya mantığı → `InventorySystem`.
4. Yetenekler/sınıflar → `SkillSystem` (model/animasyon bağları dahil).
5. Mühür/geliştirme → `SealSystem`.
6. Zindan ve Bronz Taş Tapınağı → `DungeonSystem`.
7. Savaş ve düşman yapay zekâsı → `CombatSystem`, `Mob`, `Projectile`.
8. Coop olayları, HUD/arayüz, sahne/kamera/renderer.
Kural: bölünen kodda mantık değişmez; yalnız yer değişir. Global değişkenler önce dışa aktarılan bir `state` nesnesine toplanır. Gerçek klasör yapısı bu sırada koddan çıkarılır; başlangıçta uydurulmaz.

## Faz 4 — TypeScript
1. Dosya dosya `.js` → `.ts`; önce veri tabloları ve `types/` (Eşya, Mob, Kayıt, Sınıf tipleri).
2. `checkJs`/`strict` kademeli açılır; yeni ve dokunulan dosyalarda zorunlu.
3. `tsc --noEmit` temiz olmadan dosya "bitti" sayılmaz.

## Faz 5 — Cila (isteğe bağlı)
- Nesne havuzu (projektil, parçacık, hasar yazıları) yalnız ölçülen bir sorun varsa; görsel kalite önceliği korunur.
- README: kurulum, `npm run dev`, `npm run build`, test çalıştırma, dağıtım.
- `PROJECT_STATE.md` güncellemesi: yeni mimari haritası.

## Bitti sayılma ölçütü
- `npm run build` hatasız; `dist/` statik sunulunca oyun açılıyor, sınıflar/zindan/tapınak/kayıt çalışıyor.
- Taban testlerin hepsi aynı sonuçta (bilinen kararsız test hariç).
- `index.html` içinde base64 GLB kalmadı.
- Kullanıcı gerçek telefonda dokunmatik arayüzü ve yüklenme süresini kontrol etti (bu ortamdan test edilemez).

---

## Başlangıç prompt'u (her oturumda yapıştırılır, `<FAZ>` doldurulur)

Taş Mührü deposunda Vite + TypeScript taşımasının **<FAZ>** fazını yap.
Önce `CLAUDE.md`, `PROJECT_STATE.md` ve `VITE_TASIMA_YOL_HARITASI.md` dosyalarını oku; başka belge okuma.
Gerçek kaynak bu depodaki `index.html`'dir; masaüstündeki `src/` ve `build.py` kullanılmaz.
Yalnız bu fazın maddelerini yap, sonraki fazlara geçme. `index.html`'i baştan sona okuma; hedefli `grep`/`sed` kullan ve base64 satırlarını kes.
Mevcut oyun davranışını, dövüş matematiğini, kayıt beyaz listesini ve dokunmatik arayüzü değiştirme.
Faz sonunda `tests/` içindeki testleri çalıştır, sonucu taban rapor ile karşılaştır, `CHANGELOG_DEV.md`'ye kısa kayıt ekle, commit at ve çalışma dalına push et.
Denenmeyen şeyleri "denenmedi", coop testlerini "simülasyon" olarak bildir.
Bir adım testi bozarsa dur ve neyin bozulduğunu raporla; "düzeltmek için" kapsamı genişletme.
Kullanıcıya Türkçe yanıt ver.
