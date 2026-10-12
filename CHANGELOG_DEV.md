# Geliştirme kaydı

Her görev sonunda kısa kayıt: tarih ve görev · değişen dosyalar · önemli kararlar · çalıştırılan testler · açık sorunlar.
Eski kayıtlar kısa tutulur; ayrıntı gerekirse git geçmişine bakılır.

## Önceki işler (özet, git geçmişinden)
- `1889fb6` Savaşçı sınıfı (5 gövde GLB, yeniden rig + animasyon), Sv 70 ve son oyun dengesi.
- `d9f1acd` · `f65921b` · `032b90e` · `12e578b` · `0c38673`: Savaşçı kılıçları, hareket yakalama animasyonları, yeni yetenek
  seti (Hamle, Üç Yönlü Kesme, Kılıç Çevirme, Mühür Yemini), vuruş hissi, yetenek sırasında hareket kilidi.
- `3990959` Kılıca özel +0…+9 yükseltme görünümü.
- Her büyük işten önce `main` yedek dala alındı (`yedek/*-oncesi`).

## 2026-10-12 — GEÇİCİ deneme karakteri (kaldırılacak)
- `index.html`: karakter seçim ekranında "Deneme: Sv 50 Savaşçı" düğmesi → yeni yuvada Sv 50 Savaşçı, +9 Nihai Zırh Seti (kask, zırh, çizme, kalkan, Efsane nadirlik), +9 Obsidyen Keski, Güç 108 / Can 58, yetenekler 5/5, 200.000 altın.
- Kaldırma: `// ===== GEÇİCİ DENEME KARAKTERİ` bloğunu sil, `testCharButton(box); // DENEME-DUGMESI` satırını sil, `__tm` kancasındaki `newTestWarrior`'ı çıkar (ya da bu işin commit'ini `git revert` et). Oyuncunun kayıtlarına dokunmaz.
- Test: `node --check` temiz; başsız Chromium'da düğme görünüyor, karakter doğru ekipmanla açılıyor (ATK 755, DEF 555, Can 2333), sayfa hatası yok.

## 2026-10-12 — Oyun sonu ilerleme ve zindan dengesi · dal `ozellik/oyun-sonu-denge`
- Dosyalar: `index.html`, `CHANGELOG_DEV.md`, `PROJECT_STATE.md`. Bağımlılık eklenmedi; V12 klasörüne dokunulmadı.
- **A. Tapınak zorluğu** (`TEMPLE_POW`, `TEMPLE_FLOORS`, `Mob`): kat seviyesi 42+2·kat → 46+2·kat (Sv 48–64). Canavar canı ×1.7…4.2,
  saldırı ×2.0…5.8, savunma ×1.15…1.55; 4. kattan itibaren saldırı (`cd`) ve yetenek (`sk`) sıklığı artar. Katlar 1–5 ve 7–9 iki
  dalga, 6 ve 10 tek dalga; 6. kat ilk büyük güç duvarı (can ×3.4, saldırı ×5.8). Patron mühür tutma süresi 2.0 → 2.4 sn
  (`SEAL_HOLD`). Alan saldırıları aynı kaldı (uyarı halkaları değişmedi). Grup avantajı: hasar sabit, can +%60/oyuncu (`COOP_HP`).
  - Simülasyon (oyun formülleriyle, `balance.mjs`): Sv 50 +9 Bronz tek başına kayıp ≈ %11/36/56/77/133 (1–5. kat), 6. katta %252, 7. katta %475+.
    Sv 55 +9 Efsane tek başına 6. katta ≈ %115; 4 kişilik Sv 55 +9 Efsane: 7–9. kat %36/57/65, 10. kat %89.
- **B. Efsanevi + Taş Mühür ödülleri** (6–10. kat, `TEMPLE_REWARDS.efs/ts/minRar`, `Temple.grant`): Efsanevi parça şansı kat başına
  0.28/0.22/0.28/0.34/1.5 koşu; 10. katta 2 zar. `rollGear(..., efs)` Zor/Kabus şartını (`minDiff`) yalnız bu kaynak için aşar; normal
  zindanlar değişmedi. Mühür zarları kata göre kademe yükseltir; ilk temizleme tek seferlik mühür verir (`TEMPLE_FIRST.ts`).
  Tekrar ödül: mevcut `claims` anahtarı (örnek kimliği + kat) ve ilk-temizleme bit maskesi; tümü `grant` içindeki tek kilitli blokta.
- **Taş Mühür sistemi:** 5 tür (saldırı, savunma, can, kritik, yetenek) × 3 kademe (Kırık / Bronz / Kadim) = 15 yığın (`ts_<tür>_<kademe>`).
  Eşya başına 1 yuva (`it.seal`, kayıtta beyaz listeli); ekipmanı yeniden yazmadan `recalc` mühür toplamını ekler. Tür başına toplam üst sınır
  (saldırı %20, savunma %25, can %30, kritik +10, yetenek %30). Takma ücretsiz; sökme altınla (1.500 / 5.000 / 15.000), mühür çantaya döner;
  3 → 1 birleştirme (Kırık→Bronz 3.000, Bronz→Kadim 12.000 altın), çanta doluysa geri alınır. Mühürlü eşya parçalanmaz / toplu satılmaz.
  `bronzparca` ve Simyacı dönüşümü değişmedi.
- **C. EXP** (`EXP_PLAN`, `expKills`, `expNeed`, `EXP_KILL_CAP`): Sv 1–50 birebir aynı. 51+ ihtiyaç = o seviyenin canavar EXP'si × gereken
  öldürme sayısı (51: 78 → 55: 195 → 60: 450 → 65: 900 → 69: 1500 → 70: 1600; ara değerler log-doğrusal). Sv 50→60 toplam maliyet 1.46 M
  (eski 0.90 M, ×1.6), 60→70 toplam 8.5 M (eski 3.97 M, ×2.1). Tek öldürme EXP'si seviye ihtiyacının %35'iyle sınırlı; tapınak kat EXP
  oranları 0.02–0.12 → ~0.005–0.04; tam tapınak turu Sv 55'te ~0.7, Sv 60'ta ~0.35 seviye.
- Testler (başsız Chromium + yerel sunucu, Playwright): `node --check` temiz; `t_logic.mjs` 21/21 (EXP, mühür, kayıt, Efsanevi zarı);
  `t_temple.mjs` 34/34 (10 kat gerçek açılış ve canavar katsayıları, dalga sayıları, ödül dağılımı 500 örnek/kat, tekrar ödül, EXP sınırı,
  çanta arayüz düğmeleri); `t_reg.mjs` (iki sınıf yeni karakter + kayıt gidiş-dönüşü, hata yok). Bu betikler depoda değil (oturum çalışma alanında).
  Masaüstündeki `run.mjs` / `tapinak.mjs` bu ortamda yoktu → çalıştırılmadı.
- Açık: gerçek cihazda grup testi YAPILMADI; mobil başarım (dalga başına en çok 8 yaratık) ve dokunmatik mühür
  düğmeleri denenmedi; denge sayıları model tahminidir, oyuncu geri bildirimiyle ince ayar gerekir. Önceden var olan: set sınıflarında
  tapınağın sıradan `gear` düşüşü Bez Zırh parçası verebilir (Efsanevi `efs` zarları bunu telafi eder).
- Yedek: `yedek/oyun-sonu-denge-oncesi`.

## 2026-10-12 — Bronz Taş Tapınağı (10 katlı grup zindanı) · `ca42025`
- Dosyalar: `index.html`; yeni `tapinak_{tas,canavar,okcu,buyucu,minib,boss,silah}.js`.
- Kararlar:
  - Dairesel çarpışma `L.circ` ile yapıldı; ızgara yalnız mini harita içindir.
  - Kararları host verir, `T` olaylarıyla dağıtır. Ödül anahtarı örnek kimliği + kat; savaşı görmeyene ödül verilmez.
  - Taş Canavarı için golem modeli kullanıldı.
  - Kat modelleri tembel yüklenir.
- Testler: `tapinak.mjs` 35/35, `tapinak_coop.mjs` 13/13 (simülasyon), `run.mjs` 36/36, `movetest.mjs` 20/20.
- Açık: denge (Sv 50 ve +9 ile tek başına çok kolay); gerçek cihazda grup testi yapılmadı.
- Yedek: `yedek/tapinak-oncesi`.

## 2026-10-12 — Token tasarruflu çalışma düzeni
- Dosyalar: `CLAUDE.md`, `PROJECT_STATE.md`, `CHANGELOG_DEV.md` oluşturuldu (önceden yoktu). Oyun koduna dokunulmadı.
- Kararlar:
  - Her görev `PROJECT_STATE.md` ile başlar; `index.html` yalnız hedefli `grep` ve aralıklarla okunur.
  - Base64 / üçüncü taraf bölgeleri atlanır.
- Testler: kod değişmediği için oyun testi çalıştırılmadı. Bölüm haritası ve semboller `grep` ile kaynaktan doğrulandı.
- Açık: tapınak dengesi, tapınak ortak oyununun cihaz testi.
