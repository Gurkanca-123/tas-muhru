# Taş Mührü — proje durumu (kısa teknik hafıza)

Son güncelleme: 2026-10-12 · `main` = `ca42025` (Bronz Taş Tapınağı). Satır numaraları bu sürüme göredir ve kayar;
her zaman `grep -n` ile doğrula.

## Dosyalar
- `index.html` (~5.8 MB, 17.4k satır): tüm oyun. 1–503 CSS + DOM · 504–511 betik etiketleri + `window.TM_NET` (Supabase) ·
  sonrası tek büyük `<script>`. ~2700–7700 gömülü SkeletonUtils + GLTFLoader (üçüncü taraf, dokunma) · ~7777–7800
  `OUTFIT_DATA` + `GEAR_GLTF` (base64 kılıç/balta/kıyafet GLB'leri).
- Açılışta yüklenen: `three.min.js` (r158), `baltaci_{ciplak,bez,kurt,bronzz}.js`, `boneking.js`, `boneking_sword.js`.
- İhtiyaçta yüklenen (`window.TM_ASSETS[ad]` = base64 GLB): `savasci_{fantazi,bez,kurt,nihai,efsane}.js` (`SAVASCI_FILES`),
  `tapinak_{tas,canavar,okcu,buyucu,minib,boss,silah}.js` (`TEMPLE_FILES`, kata göre).
- `manifest.webmanifest`, `icon-*.png`, `README.md`. Araç / test betikleri depoda yok (bkz. `CLAUDE.md`).

## Bölüm haritası (index.html)
| Satır~ | Bölüm / önemli semboller |
|---|---|
| 516 | yardımcılar (`rand`, `pick`, `clamp`, `dist`, `el`, `esc`, `fmtFull`, `mulberry32`), 562 `SFX` |
| 629–1005 | oyun verisi: `MAX_LV`=70, `expNeed`, `CLASSES` (baltaci, warrior), `SKILLS`, `DUNGEONS` (691), `MOBS` (709), `RANK`, `mobBase`, `SLOTS`, `GEAR_SETS`, `STACKS` (880), `UPG`/`upgradeCost`, `DROP` (963), `DIFFS` (984), `DAILY_KINDS`, `THEMES` |
| 2091–2660 | eşya sistemi (`makeGear`, `rollGear`, `itemName`, `sellPrice`), kayıt (`newCharacter` 2318, `saveGame` 2387, `applySave` 2459), `recalc` 2530, envanter (`addItem`, `countStack`, `removeStack`), `addExp` 2661 |
| 7804 | `Cloud` (yalnız claude.ai Artifact içinde; GitHub Pages'te kapalı → kayıt yalnız localStorage) |
| 7930–8020 | karakter GLB yükleyicileri: `BALTACI_BODIES`, `SAVASCI_FILES`/`savasciLoad`, `BONEKING` |
| 8039 | zorluk (`diffUnlocked`, `markDiffClear`), `Daily` |
| 8123 / 8333 / 8593 | `Net` (Supabase Realtime, oda kodu) · `Duel` · `RemotePlayer` · `Coop` (ortak zindan, 8609) |
| 8992–10306 | low-poly modeller, `buildSavasciModel` (9618), Baltacı modeli (`BALTACI_SKILL_T`, `SKILL_LOCK`), `SAVASCI_SKILL_T`, `buildMobModel` (~10080) |
| 10307–11415 | görsel katman: `LightPool` (3 sabit ışık), dokular, köy parçaları, kıyafet sistemi, +7…+9 ışıltı, `buildBoneKing` |
| 11416–12690 | sahne/köy/zindan üretimi: ızgara (`tileAt`, `walkable` 11507, `canStand`, `moveEntity`, `bfsField`), `newLevel`, `makePortal`, `buildDungeon`/`buildDungeonInner` (12074) |
| 12690 | `FX` (parçacık, halka, `seal`, `flash`, kılıç izi), `telegraph` |
| 13214 | `class Mob` (13223): durum makinesi, `doAttack`, `trySkill`, `animate`, `updateDeath`; `spawnMob` |
| 13773–14510 | **Bronz Taş Tapınağı** (aşağıda) |
| 14511 / 14563 | `Proj` (mermiler) · yerdeki loot |
| 14637 | `class PlayerEnt` (oyuncu, animasyon karışımı) |
| 15029 | `Combat`: `calc`, `hitMob`, `killMob`, `rollLoot`, `useSkill`, `damagePlayer`, `basicAttack` |
| 15661 / 15732 | girdi · `UI` (paneller `p_<ad>`; `open`, `close`, `render`, `btn`, `footCard`) |
| 16959 | ana döngü: `goVillage` (~16996), `goDungeon` (~17010), `update` (~17034), `frame`; 17375 `window.__tm` test kancası |

## Sistemler
- **Karakter:** sınıflar `baltaci` (Baltacı) ve `warrior` (Savaşçı); ikisi de GLB gövde + AnimationMixer, zırh setine göre gövde
  değişir. Yetenek animasyonu kilidi `SKILL_LOCK` / `SAVASCI_SKILL_T`. Statlar `recalc()` → `D`.
- **Savaş:** `Combat.calc` (atk, def, kritik) → `hitMob` → `killMob` (EXP seviye farkıyla ölçeklenir, `rollLoot`). Canavar
  gücü `mobBase(Sv) × RANK × MOBS çarpanı × L.mobPow × DIFFS`. Ortak oyunda ek oyuncu başına can +%60 (`COOP_HP`).
- **Eşya / envanter:** yuvalar `SLOTS`; set sınıfları `GEAR_SETS` (Bez, Kurt Dişi, Nihai, Bronz Taş, Efsanevi…); yığınlar `STACKS`;
  geliştirme `UPG` + `upgradeCost` (+7…+9 için yuva özü `RAREMAT`); Simyacı (`p_alchemist`).
- **Seviye / ödül:** `expNeed` (50 sonrası dik), günlük görevler `Daily`, zindan ilk temizleme ödülü `killMob` içinde.
- **Zindanlar:** `DUNGEONS` d1–d7 ızgara tabanlı (`buildDungeonInner`, oda + koridor, tohumlu düzen); d6 son katı Kadim Metin
  arenası; d7 Kemik Taht (Kemik Kral, kod-animasyonlu GLB). Zorluk Normal / Zor / Kabus (`DIFFS`).
- **d8 Bronz Taş Tapınağı (dIdx 7):**
  - Veri: `TEMPLE_FLOORS` (10 kat ve dalgalar), `TEMPLE_POW`, `templeFloorLv` (42 + 2·kat), `TEMPLE_REWARDS` / `TEMPLE_FIRST`
    (merkezi ödül tablosu).
  - Kat kurulumu: `buildTempleFloor` kurar. Çarpışma gerçek dairedir (`L.circ`, `templeWalk`); ızgara yalnız mini harita içindir.
  - Akış: `Temple` nesnesi; dalga / temizleme / ödül / panel `p_tapinak`.
  - Patron: `bossPick`, `bossPhase` / `applyPhase`, mühür noktaları `sealsOn` / `sealTick`, `templeShock` / `telegraphRing`.
  - Düşmanlar: `MOBS` içindeki `model:'tapinak'` olanlar; `buildTempleMob`, `animateTempleMob`, `tmPlay`, `tmDie`.
    Vuruş anı klipteki `ev.hit` ile hizalanır (`TM_ALIGN`).
  - Kayıt: `P.temple = {best, bestClear, first, runs, seals, claims}`.
- **Ortak oyun:** `Net` (Supabase Realtime kanalı `tm-<KOD>`, durum yayını), `Coop` (aynı `levelKey` 'd<dIdx>-<kat>' + tohum
  → aynı örnek). Host canavarları yönetir, misafir kukla tutar. Olaylar: `n` doğum, `k` ölüm, `a` saldırı, `t` yer uyarısı,
  `v` yaylım, `c` eylem, `x` mesaj, `d` hasar, `T` tapınak (`w` / `c` / `ph` / `so` / `sb`), `tr` halka şok.
  `fullState` / `applyFull` ile yeniden eşitlenir; host düşerse `promote` devralır.
- **Model / animasyon:** GLB'ler base64 betiklerden `GLTFLoader.parse`, `SkeletonUtils.clone`; klipler GLB'ye gömülü (araçlarla
  üretildi). Kemik Kral klipsiz, kodla poz (`animateBoneKing`). Tapınak düşmanları: idle / walk / run / death + atk / slam /
  spin / roar / plant / cast / seal / shoot; sahne extras `enemy.{handMount, handMountL, shieldMount, ev}`.

## Bilinen sorunlar / kısıtlar
- **Tapınak dengesi:** kullanıcı geri bildirimi — Sv 50 ve tam +9 ekipmanla tek başına çok kolay. Yeniden dengelenmeli;
  kaldıraçlar `TEMPLE_POW`, `templeFloorLv`, `MOBS` (`tasmuhafiz` … `bronzmuhur`) çarpanları, patron `hpMul` / `atk`.
- **Tapınak ortak oyunu gerçek cihazlarda grupla doğrulanmadı;** yalnız tek tarayıcıda olay simülasyonuyla test edildi.
- Tapınak: tam temizleme anında bağlantısı kopan ve savaştan sonra dönen oyuncu o katın ödülünü almaz (bilinçli).
  Taş Canavarı için dört ayaklı model yok (golem kullanılıyor). Mini patron iskeleti tahmini. 8. kat ~296k üçgen
  (gölge dahil; Yosunlu İn ~254k).
- GitHub Pages'te bulut kaydı yok: tarayıcının "çerezler ve site verileri" silinirse karakterler gider (Menü → Kodu kopyala ile yedek).
- `run.mjs` Baltacı "Yer Sarsan" kontrolü rastgele düzende ara sıra kalıyor (oyun hatası değil).
- Yerel `src/` projesi bu depoyla eşitli değil.

## Son tamamlanan büyük özellikler
- 2026-10-12 Bronz Taş Tapınağı (10 katlı dairesel arena grup zindanı) — `ca42025`.
- Kılıç yükseltme görünümü +0…+9 (`3990959`) · yetenek kararlılık penceresi (`0c38673`) · Savaşçı yetenekleri ve animasyonları
  (`032b90e`, `12e578b`, `f65921b`) · Savaşçı sınıfı ve Sv 70 son oyun dengesi (`1889fb6`).
