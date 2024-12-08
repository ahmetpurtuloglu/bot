📈 Borsa Takip Telegram Botu

Bu bot, belirtilen hisselerin fiyatlarını 50, 100 ve 144 haftalık hareketli ortalamalarla karşılaştırır ve fiyatlar belirli bir tolerans dahilindeyse Telegram üzerinden bildirim gönderir.


🛠️ Özellikler

Belirtilen hisselerin fiyat verilerini Yahoo Finance üzerinden çeker.
50, 100 ve 144 haftalık hareketli ortalama (SMA) hesaplar.
Fiyat, ortalamaya belirli bir yakınlıktaysa Telegram'da mesaj gönderir.
Otomatik bildirim sistemi ile sinyal geldiğinde sizi haberdar eder.


📦 Gerekli Kütüphaneler

Bu botun çalışması için aşağıdaki Python kütüphaneleri gereklidir:

yfinance — Hisse fiyat verilerini çekmek için
pandas — Verileri analiz etmek ve tablo işlemleri yapmak için
aiogram — Telegram botu ile mesajlaşmak için
dotenv — .env dosyasından bot token ve chat ID'yi okumak için


📋 Kurulum Adımları

1️⃣ Python Ortamını Kurun
Öncelikle, bu projeyi çalıştırmak için Python 3.8+ yüklü olmalıdır. Python sürümünüzü kontrol etmek için terminale şu komutu yazın:

python --version
Eğer Python yüklü değilse, Python resmi web sitesinden indirip kurabilirsiniz.

2️⃣ Gerekli Kütüphaneleri Kurun
Proje kütüphanelerini pip kullanarak kurun:

pip install yfinance pandas aiogram python-dotenv
Not: Bu komut, tüm gerekli kütüphaneleri sisteminize yükleyecektir.

3️⃣ .env Dosyasını Oluşturun
Projenizin kök dizininde bir .env dosyası oluşturun.
Bu dosya, Telegram botu ile iletişim kurmak için bot token ve chat ID'yi içerir.

.env dosyasının içeriği şu şekilde olmalıdır:

bot_token=YOUR_TELEGRAM_BOT_TOKEN
chat_id=YOUR_TELEGRAM_CHAT_ID
bot_token: Telegram botunun erişim token'ıdır.
chat_id: Mesajları alacak Telegram kullanıcısının (veya grubun) kimliğidir.
Not: Bu bilgiler olmadan bot çalışmayacaktır.

4️⃣ Bot Token ve Chat ID Nasıl Alınır?

🔐 1. Bot Token Nasıl Alınır?
Telegram'a gidin ve @BotFather'ı arayın.
/newbot komutunu kullanarak yeni bir bot oluşturun.
Botunuza bir ad ve kullanıcı adı (username) verin.
BotFather size bir API Token (bot_token) verecektir. Bu token'ı kopyalayın ve .env dosyasına ekleyin:
bot_token=YOUR_TELEGRAM_BOT_TOKEN

🔐 2. Chat ID Nasıl Alınır?
Telegram'a gidin ve @userinfobot veya @getidsbot gibi bir bota mesaj atın.
Bu bot size kullanıcı kimliğinizi (chat_id) gönderecektir.
Elde ettiğiniz chat ID'yi .env dosyasına ekleyin:
chat_id=123456789
Not: Bu kimlik, kiminle iletişim kurulacağını belirler. Eğer bir gruba mesaj göndermek istiyorsanız, grubun chat ID'sini almanız gereklidir.

🚀 Nasıl Çalıştırılır?

1️⃣ Tüm dosyaların hazır olduğundan emin olun:

bist.py dosyasının projede olduğundan emin olun.
.env dosyasının oluşturulduğundan emin olun.

2️⃣ Komutu çalıştırın:

python bist.py

3️⃣ Botun Çalıştığını Görün

Bot, belirtilen hisseler için 50, 100 ve 144 haftalık ortalamaları kontrol eder.
Eğer fiyat, belirtilen ortalamalardan birine belirli bir tolerans içinde yakınsa, Telegram'da bir mesaj alırsınız.
📡 Telegram'da Gönderilen Mesaj Örneği

Bot, Telegram'da aşağıdaki formatta mesaj gönderir:

📈 *X* hissesinin 100 haftalık ortalamasına yakın olduğu tespit edildi!
💵 Kapanış fiyatı: X.YZ TL,
📊 100 haftalık ortalama fiyatı: X.YZ TL
📉 Ortalamaya uzaklık: %X.YZ

Not: Mesaj formatı, hisse adı, fiyat, ortalama ve farkı açıkça gösterecek şekilde tasarlanmıştır.

🛠️ Kodun Özeti

📂 Dosya Yapısı
📦 proje-dizini
 ┣ 📜 .env (bot_token ve chat_id'yi içerir)
 ┣ 📜 bist.py (ana dosya)

