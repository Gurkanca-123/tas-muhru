# Geliştirme kaydı

Her görev sonunda kısa kayıt: tarih ve görev · değişen dosyalar · önemli kararlar · çalıştırılan testler · açık sorunlar.
Eski kayıtlar kısa tutulur; ayrıntı gerekirse git geçmişine bakılır.

## Önceki işler (özet, git geçmişinden)
- `1889fb6` Savaşçı sınıfı (5 gövde GLB, yeniden rig + animasyon), Sv 70 ve son oyun dengesi.
- `d9f1acd` · `f65921b` · `032b90e` · `12e578b` · `0c38673`: Savaşçı kılıçları, hareket yakalama animasyonları, yeni yetenek
  seti (Hamle, Üç Yönlü Kesme, Kılıç Çevirme, Mühür Yemini), vuruş hissi, yetenek sırasında hareket kilidi.
- `3990959` Kılıca özel +0…+9 yükseltme görünümü.
- Her büyük işten önce `main` yedek dala alındı (`yedek/*-oncesi`).

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
