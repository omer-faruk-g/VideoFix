# Video ve Short Özetleri (2026-11-11)

Yöntem: Her video tarayıcıda sessiz ve 4x hızda açıldı. 4 short'un transkripti YouTube'un kendi transkript panelinden okundu. 10 dakikalık Türkçe videoda altyazı kanalı yok; görüntüde gömülü altyazı ve slaytlar var, bu yüzden her bölümden kare alınıp ekrandaki yazılar okundu (açıklamadaki bölüm listesiyle eşleştirildi). Sesli konuşmanın tamamı kelime kelime okunmadı; o videonun özeti bölüm slaytlarına ve okunan altyazı satırlarına dayanıyor.

Etiketler: **[Doğru]** belgeyle/bilinen davranışla uyumlu · **[Doğrulanmamış]** videonun iddiası, kanıt yok · **[Yanlış]** Claude Code'un gerçek davranışıyla çelişiyor.

---

## 1. "This Free Tool Cuts Claude Code Token Usage by 49x on Large Codebases" — InsiderForce (Short, 1:43)
https://youtu.be/ELsXhePjBxI

- **Konu:** Graphify adlı ücretsiz araç. Kod tabanını bir kez tarayıp sınıf, fonksiyon, import ve çağrı ilişkilerinden yerel bir bilgi grafiği kuruyor. Sonraki oturumlarda Claude dosyaları okumak yerine grafiği sorguluyor.
- **İddialar:** Büyük kod tabanında 49 kat daha az token, Obsidian ile birlikte 71.5 kat. "20 dolarlık plan 200 dolarlık gibi çalışır." Claude Code, Cursor, Codex ve Gemini CLI ile çalışıyor; tek komutla kuruluyor, yerelde çalışıyor, kod değişince kendini güncelliyor.
- **Kapanış:** "HUMAN yaz, e-kitabı göndereyim" (takipçi toplama çağrısı).
- **Değerlendirme:**
  - [Yanlış] "Her yeni oturumda Claude tüm kod tabanını baştan okur." Claude Code açılışta yalnızca CLAUDE.md ve hafıza dosyalarını yükler. Dosyaları ihtiyaç oldukça okur.
  - [Doğrulanmamış] 49x / 71.5x oranları ve "$20 = $200" sözü. Kazanç projeye ve soruya göre değişir; ölçmeden söylenemez.
  - [Doğru] Sorgulanabilir bir grafik, mimari sorularında çok dosya okumayı azaltabilir. Graphify bu makinede zaten kurulu.

## 2. "Get 1000 Free APIs for Claude Code to Build Anything You Want" — InsiderForce (Short, 1:32)
https://youtu.be/4qIZmI_1Zgs

- **Konu:** GitHub'daki "public-apis" deposu: e-posta, eğlence, sağlık, kripto, hava durumu, haber, finans gibi kategorilerde 1000'i aşkın ücretsiz API.
- **Önerilen akış:** Claude Code'u aç, API linkini yapıştır, "bunu kullanarak bana bir özellik yap" de. Claude dokümanı okur, kodu yazar, 10 dakikada çalışan özellik çıkar.
- **Örnekler:** Gerçek besin verili yemek uygulaması, canlı fiyatlı kripto, haber sitesi, çeviri uygulaması, film puanları.
- **Kapanış:** Aynı "HUMAN" e-kitap çağrısı.
- **Değerlendirme:**
  - [Doğru] Hazır API kullanmak sıfırdan yazmaktan hızlıdır.
  - [Eksik] Videoda hiç geçmeyenler: listedeki API'lerin bir kısmı ölü ya da bakımsız, çoğunda anahtar, kota ve lisans/ticari kullanım şartı var, bazıları CORS yüzünden tarayıcıdan çağrılamaz. Anahtarın koda gömülmesi ve hata/kota durumunun ele alınmaması en sık hata olur.
  - [Doğrulanmamış] "10 dakikada canlı özellik", "gerçek ödeme yapan kullanıcılı platformlar".

## 3. "Claude Limitine Bir Daha Asla Takılmayacaksın" — İsa Nurdoğdu (Video, 10:12)
https://youtu.be/JNM_rxqtlvY

- **Ana fikir:** Limit mesaj sayısıyla değil token'la ölçülür. Her mesajda Claude sohbetin tamamını baştan okur; 30. mesajda tek bir mesaj ~232.000 token'a, sohbetin tamamı ~2.5 milyon token'a çıkabiliyor (videonun örneği).
- **Giriş — Caveman ("mağara adamı") yöntemi:** github.com/JuliusBrussee/caveman. Claude'a kısa, süssüz konuşmasını söyleyen bir agent skill; videoda "%65'e varan tasarruf" deniyor.
- **11 kural:**
  1. **Düzeltme mesajı yerine Edit / Regenerate.** "Onu kastetmedim, tekrar dene" diye yeni mesaj atmak bağlamı şişirir; ilk mesajı düzenle.
  2. **Her 15-20 mesajda yeni sohbet.** Şişen sohbete "özetle" de, özeti yeni sohbete yapıştır; bağlam korunur.
  3. **Soruları tek mesajda topla.** Her mesaj yeni bir bağlam yüküdür; parça parça sormak pahalıdır.
  4. **Token kullanımını ölç.** Her şey makinede `~/.claude/projects` altında kayıtlı (input/output/cache token, model, zaman). Ücretsiz, açık kaynak, Python dashboard: github.com/phuryn/claude-usage (modele/tarihe göre filtre, güncel API fiyatıyla maliyet).
  5. **Sık kullanılan dosyaları Projects'e yükle.** Aynı PDF'i her sohbete yeniden yüklemek her seferinde yeniden token demek.
  6. **Hafızayı ve tercihleri bir kez kur.** "Ben pazarlamacıyım, samimi yaz, kısa paragraf..." gibi cümleleri her sohbette tekrar yazma.
  7. **Kullanmadığın özellikleri kapat.** Web Search, Connectors, Explore Mode, Tools, Extended Thinking: kullanılmasa da arka planda token yakar.
  8. **Basit işler için Haiku.** Gramer kontrolü, beyin fırtınası, biçimlendirme, kısa çeviri, kısa cevap; Sonnet/Opus'tan çok daha ucuz.
  9. **İşi güne yay.** Gece yarısı sıfırlanmaz; kayan 5 saatlik pencere var. Hepsini tek oturuma yığma.
  10. **Yoğun olmayan saatlerde çalış.** Videoya göre 26 Mart 2026 Anthropic kararıyla yoğun saatlerde 5 saatlik limit daha hızlı tükeniyor.
  11. **Güvenlik ağı: limit aşımını (overage) aç.** Kapalıyken limit dolunca erişim işin ortasında kesilir; açıkken API ücretlendirmesine geçip devam eder, aylık harcama tavanı konabilir.
- **Değerlendirme:**
  - [Doğru] 1, 2, 3, 5, 6, 7 ve 8'in mantığı (bağlam her istekte yeniden gönderilir). Kural 1'in Claude Code karşılığı `/rewind` (veya Esc Esc), kural 5-6'nın karşılığı CLAUDE.md ve `@` ile dosya içe aktarma.
  - [Doğrulanmamış] Kural 10'daki tarih ve yoğun saat kuralı; "%65" Caveman oranı; 232K/2.5M sayıları videonun kendi örneği.
  - [Dikkat] Kural 11 para harcayan bir hesap ayarı; kararı kullanıcınındır, tavan konmadan açılmamalı.
  - Bu kuralların çoğu ClaudeLimit skill'inde zaten var (tek görev/oturum, öz bağlam notu, drain.py ölçümü, lean mode).

## 4. "Top 5 Free Claude Code Plugins Every Vibe Coder Needs Before They Ship" — InsiderForce (Short, 1:32)
https://youtu.be/qGuDcRRJAD4

- **5 eklenti:**
  1. **Playwright MCP:** Claude'a tarayıcı kontrolü verir; akışlara tıklar, ekran görüntüsü alır, bozuk yeri senden önce bulur.
  2. **Supabase eklentisi:** Veritabanını terminalden çıkmadan kurar, yönetir, sorgu çalıştırır.
  3. **VibeSec:** Hacker gibi düşünüp zayıf noktaları bulur, neyin düzeltileceğini söyler.
  4. **SkillUI:** Beğendiğin bir sitenin tasarım sistemini (renk, font, boşluk, bileşen kalıpları) dosyaya çıkarır; Claude arayüzü buna göre kurar.
  5. **Context7:** Kütüphanelerin güncel dokümanını çeker; Claude eğitim verisindeki eski API'yle kod yazmaz.
- **Kapanış:** "HUMAN" e-kitap çağrısı.
- **Değerlendirme:**
  - [Doğru] Beşi de gerçek bir boşluğu hedefliyor: görmeden "bitti" demek, güvenliğin atlanması, eski API kullanımı.
  - [Dikkat] Supabase eklentisi canlı veritabanına yazabilir (önce dev/branch projesi). SkillUI ile başkasının sitesini birebir kopyalamak marka/telif sorunu doğurur; kendi sitenden veya izinli kaynaktan tasarım token'ı çıkar, düzeni ve markayı kopyalama.
  - Bu makinede: uygulamanın yerleşik tarayıcısı Playwright'ın işini görüyor; `security-review` skill'i ve ClaudPer'in "sürümü kontrol et" kuralı VibeSec/Context7'nin bir kısmını karşılıyor. Context7 ve Playwright MCP kurulu değil.

## 5. "claude code'da yeni başlayanların yaptığı 10 hata" — Selahattin Ünlü (Short, 0:20)
https://youtu.be/oCrU7Q0eXjs

- **İçerik:** Limit çabuk bitiyorsa sorun iş değil alışkanlık. Örnek: bütün gün tek sohbette çalışırsan Claude sabahki mesajları da baştan okur, her mesaj bir öncekinden pahalı olur. Diğer 9 hata kanaldaki uzun videoda (bu short'ta yok).
- **Değerlendirme:** [Doğru] Bağlam her istekte yeniden gönderilir (önbellekte olsa bile sayılır). Çözüm: tek görev/oturum + öz bağlam notu + `/clear`; bu ClaudeLimit'in 3. bölümü.

---

## Ortak tema

Beşinin ortak derdi: (a) bağlamın gereksiz büyümesi ve limitin erken bitmesi, (b) Claude'un gördüğünü doğrulamadan ve güncel bilgi olmadan iş bitirmesi, (c) hazır olanı (API, araç) kullanmak yerine sıfırdan yazmak. Videoların zayıf yanı: ölçülmemiş yüzde iddiaları ve bir yanlış teknik iddia (Short 1). VideoFix skill'i bu üçünü düzeltiyor, iddiaları "ölç, sonra söyle" kuralına bağlıyor.
