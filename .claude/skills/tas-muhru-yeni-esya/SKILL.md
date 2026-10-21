---
name: "tas-muhru-yeni-esya"
description: "Taş Mührü'ne yeni eşya eklerken kullan: ekipman parçası, set / takı seti, yığın (iksir, parşömen, malzeme), efsun satırı, set etkisi, ikon, düşüş / dükkân kaynağı."
---

# Taş Mührü — yeni eşya ekleme

Önce `CLAUDE.md` ve `PROJECT_STATE.md` kurallarını uygula (hedefli okuma, `index.html`'i baştan okuma, Türkçe, ilk satır "Zorluk: ..."). Bu skill yalnız eşya işini hızlandırır.
Aşağıdaki semboller `PROJECT_STATE.md`'den alınmıştır: kullanmadan önce `grep -n "sembol" index.html | cut -c1-200` ile doğrula, satır numaralarına güvenme.

## 0. Türü belirle
- **Yığın** (iksir, parşömen, malzeme, mühür): `STACKS` kaydı.
- **Ekipman parçası**: `SLOTS` yuvası + `GEAR_SETS` set kaydı (`makeGear`, `rollGear`, `itemName`, `sellPrice`, `gearStats`).
- **Adlı takı seti**: `GEAR_SETS[*].jewel: true` + kademe çarpanı `mul` (örnek: `bronzm`, `ulumuhur`).
- **Yeni efsun satırı**: `BONUS_POOL`.
- **Set etkisi** (toplama dışı): `SET_FX` + `SETFX`.

## 1. Veri
- Yığın: `STACKS`'e ad, `kind`, fiyat alanları. Parşömen ise `MASTERY_SCROLLS` ile karıştırma.
- Set: `GEAR_SETS` kaydı (sınıf, parça yuvaları, `bonus[n]`). Etki bağlamak için `bonus[n].fx = '<id>'`; çalışma kancaları `damagePlayer`, `hitMob`, `killMob`, `basicAttack`, `sealEcho`. Süre/bekleme `G.time` ile.
- Efsun: `BONUS_POOL` satırı + `gearStats` ve `recalc` anahtar listelerine de ekle (unutulursa stat paneli ve hesap farklı olur). `rollBonus` zaten havuzu zarlar; eski eşyalar etkilenmez.
- Denge değişikliği veri tablolarından yapılır (`DROP`, `DIFFS`, `TEMPLE_*`, `RANK`). Savaş matematiğine ve +0…+9 oranlarına dokunma.

## 2. Kaynak (eşya nereden gelir)
- Zindan düşüşü: `DROP`; Kabus özel: `JSET_KABUS`, `PARCH_KABUS`.
- Tapınak ödülü: `TEMPLE_REWARDS` (`jset`, `efs`, `ts`, `minRar`), ilk temizleme `TEMPLE_FIRST`. Ödül mantığı `Temple.grant` içinde tek kilitli blok; tekrar ödül `claims` anahtarıyla.
- Dükkân: `SHOP_LIST` + `price` (Tüccar). Çantadan satış fiyatı `sellPrice`.
- Görev ödülü: `QUESTS[].reward` (mevcut yığınlardan).
- Kaynağı olmayan eşya oyunda hiç görünmez: kaynağı mutlaka bağla veya "kaynak yok" diye raporla.

## 3. Görünüm
- Envanter ikonu: `iconSpec(it)` → `IC_BUILD` (tür başına prosedürel 3B model) → `icon3DRender`. Yığın listeleri `stackIcon(id)`. Yeni tür için `IC_BUILD`'e ekle; kademe / set / nadirlik renk ve ek parçayı `iconSpec` belirler.
- Silah / zırh 3B görünümü: kılıç `buildGearSword`, kıyafet sistemi `OUTFIT_DATA` / `GEAR_GLTF` (base64 GLB, açma). Yeni GLB gerekiyorsa betik ekle ve `?v=<sha1 ilk 10>` ekle.
- Stil: kalın çizgili "sticker" görünümü, yüksek görsel kalite öncelikli.

## 4. Kayıt
- Eşyaya yeni kalıcı alan eklersen `applySave` beyaz listesinde doğrula (örnek: `it.seal`). Var olan alanları silme. Eski kayıtlar alan yoksa sorunsuz açılmalı.
- Çanta: `P.inv` düz dizi (sayfalar yalnız `UI.invGrid`'te); ekleme `addItem`, sayım `countStack`, çıkarma `removeStack`. Kendi ekleme kodunu yazma.

## 5. Metin
Tamamı Türkçe, "item" değil "eşya". NPC'ler yalnız rolle anılır (Demirci, Tüccar, Depocu, Simyacı). Ek uyumuna dikkat (örn. «…Mühür'ü», «…Mühür'ün»).

## 6. Doğrulama
- Sözdizimi: en büyük `<script>` bloğunu çıkar → `node --check`.
- Eşyayı çantaya ver, giy, stat paneli ve `recalc` sonucunu bak; kayıt → yükleme gidiş-dönüşü; eski kayıtla açılış.
- Son test kopyaları kullanıcının masaüstünde (`tapinak-test/_test/`, `savasci-70-test/_test/`): `run.mjs` (genel), `qtest*` (çanta), `jtest` (takı seti / fiyat). Bunlara erişim yoksa "çalıştırılmadı" yaz; nasıl çalıştırılacağını söyle.
- Gerçek telefon ve ortak oyun: "denenmedi" yaz.

## 7. Teslim
- Yedek dal `yedek/<iş>-oncesi`; commit / push / main yalnız kullanıcı isterse.
- `CHANGELOG_DEV.md` kaydı; mimari ya da kısıt değiştiyse `PROJECT_STATE.md`.
- Görev sonu en fazla 3 madde: Değişiklik / Test / Durum. Sonra bekle.
