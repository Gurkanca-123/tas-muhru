---
name: "tas-muhru-yeni-sinif"
description: "Taş Mührü'ne yeni oyuncu sınıfı eklerken veya mevcut sınıfın (Büyücü, Şaman) yetenek / animasyon / model / set işini yaparken kullan."
---

# Taş Mührü — yeni sınıf ekleme

Önce `CLAUDE.md` ve `PROJECT_STATE.md` kurallarını uygula (hedefli okuma, `index.html`'i baştan okuma, Türkçe, ilk satır "Zorluk: ..."). Sınıf işi çok sistemi etkiler; çoğu zaman "Zor" sayılır, sınıfın yalnız bir yeteneği eklenecekse "Orta".
Semboller `PROJECT_STATE.md`'den alınmıştır: kullanmadan önce `grep -n "sembol" index.html | cut -c1-200` ile doğrula.

## Başlamadan
- Büyücü için `claude/buyucu-yetenek-seti.md` ve hafızadaki Büyücü notlarını oku (deneme dalı `ozellik/buyucu-test`, main'de değil; denge değerleri ilk taslak).
- Mevcut örnekler: Baltacı (`BALTACI_BODIES`, `BALTACI_SKILL_T`, `SKILL_LOCK`) ve Savaşçı (`SAVASCI_FILES`, `savasciLoad`, `buildSavasciModel`, `SAVASCI_SKILL_T`, `svBuildClips`). Yeni sınıfı bunlardan birinin kalıbına göre kur; ikinci bir sistem kurma.

## Kontrol listesi
1. **Veri**: `CLASSES[cls]` (kimlik, ad, statlar, `skills` sırası) ve `SKILLS` kayıtları (`SKILL_MAX`=5). Yetenek sırası görev metinlerini belirler (`sk(i)`).
2. **Hesap**: `recalc()` → `D`; sınıfa özel statlar eklenecekse oradan. `Combat.calc/hitMob/useSkill` mantığına hata düzeltmesi dışında dokunma; yetenek gücü `skillPowerOf` (ustalık dahil) üzerinden gider.
3. **Yetenek çalıştırma**: `Combat.useSkill`; süre / kilit tablosu (`*_SKILL_T`, `SKILL_LOCK`) ve hareket kilidi. Yeni yetenekte `telegraph` + hasar yardımcılarını yeniden kullan.
4. **Model + animasyon**: GLB'ler `window.TM_ASSETS[ad]` base64; ihtiyaçta yüklenen betikler `SAVASCI_FILES` gibi bir tabloya bağlanır (`?v=<sha1 ilk 10>`). Klipler: idle / walk / run / saldırı / yetenek. Silahlı klipler gerekiyorsa `svBuildClips` mantığı (yükleme anında üretilen AnimationClip). `PlayerEnt.animateGltf` klip seçimini yapar. Zırh setine göre gövde değişir.
5. **Silah / zırh**: sınıfın `GEAR_SETS` kayıtları, `SLOTS`, 3B silah (`buildGearSword` benzeri), yükseltme görünümü (`gildMaterial`, `ARMOR_LV`, `makeFlameShell`). Efsun / set etkileri (`SET_FX`) sınıf bağımsız çalışır.
6. **Kayıt**: `newCharacter` şablonu ve `applySave` beyaz listesi; sınıf kimliği doğrulanır; `P.mastery` yalnız sınıfın becerilerini kabul eder. Eski kayıt açılışta bozulmamalı.
7. **Seçim ve arayüz**: karakter seçim ekranı, Usta (yetenek öğrenme paneli), Karakter paneli, yetenek düğmeleri (HUD düğme boyutları değişmez), mini model önizleme.
8. **Görevler**: `QUESTS` sınıf bağımsızdır (`sk(i)`); sınıfa özel görev gerekirse `cls:['kimlik']` (`Quest.ok`). Görev ve hikâye tüm sınıflarda çalışmalı.
9. **Dövüş akışı**: `Mob` ve boss mekanikleri sınıftan bağımsız kalmalı; yeni sınıfın menzili / hedefleme farkı varsa `basicAttack` yolunda çöz.
10. **Ortak oyun / düello**: `Net`, `Coop`, `Duel`, `RemotePlayer` oyuncunun modelini ve eylemlerini (`c` olayı) yayar. Yeni sınıfın yetenek kimlikleri ve modeli uzaktan oyuncuda da çalışmalı; gerçek cihazla test edilemiyorsa "simülasyon" ya da "denenmedi" yaz.
11. **Deneme / test karakteri**: `newTestWarrior` benzeri geçici düğme gerekiyorsa işaretle ve kaldırma notunu `CHANGELOG_DEV.md`'ye yaz.
12. **Metin**: Türkçe, "eşya"; NPC'ler yalnız rolle anılır.

## Doğrulama
- `node --check` (en büyük `<script>` bloğu).
- İki mevcut sınıfla yeni karakter + kayıt gidiş-dönüşü (regresyon), yeni sınıfla köy → zindan → yetenek → ölüm → köy.
- Yetenekleri doğrudan tetikleyerek test et (btest yaklaşımı); animasyon geçişleri (bekle → koş → yürü → saldırı → yetenek).
- Masaüstü test kopyaları: `run.mjs`, `movetest.mjs`, `qtest*`, `stest`, `btest`. Erişim yoksa "çalıştırılmadı" yaz.
- Gerçek telefon ve ortak oyun: "denenmedi".

## Teslim
- Yedek dal `yedek/<iş>-oncesi`; commit / push / main yalnız kullanıcı isterse.
- `CHANGELOG_DEV.md` + `PROJECT_STATE.md` (sınıf mimarisi değiştiği için).
- Görev sonu en fazla 3 madde: Değişiklik / Test / Durum. Sonra bekle.
