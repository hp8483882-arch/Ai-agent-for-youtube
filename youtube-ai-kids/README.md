# Bolalar uchun AI YouTube kanali — avtomatik tizim

Har kuni avtomatik: **2 ta Shorts + 1 ta ~10 daqiqalik video** yaratib,
YouTube kanalingizga yuklaydi. Hammasi bepul/arzon xizmatlar bilan, GitHub Actions'da ishlaydi (kompyuteringiz ochiq turishi shart emas).

## Qanday ishlaydi
`script_generator.py` (matn) → `images.py` (rasmlar) → `tts.py` (ovoz) →
`video_builder.py` (video yig'ish) → `youtube_upload.py` (yuklash),
hammasi `main.py` orqali kuniga bir marta `daily.yml` (GitHub Actions) tomonidan ishga tushiriladi.

## 0-qadam: YouTube kanal ochish
YouTube'da oddiy account bilan yangi kanal yarating (bolalar mavzusiga mos nom/logo qo'ying).

## 1-qadam: Kerakli kalitlarni olish

| Xizmat | Nima uchun | Qayerdan olish | Bepulmi? |
|---|---|---|---|
| Groq | Skript (matn) yozish | console.groq.com | Ha, bepul limit bor |
| Anthropic (ixtiyoriy) | Sifatliroq o'zbekcha matn | console.anthropic.com | Arzon, pullik |
| Aisha AI | O'zbekcha ovoz (TTS) | aisha.group | Tekshiring — ro'yxatdan o'tib ko'ring |
| Google Cloud | YouTube'ga yuklash uchun OAuth | console.cloud.google.com | Bepul |

Pollinations.ai (rasmlar) uchun kalit shart emas — tayyor ishlайdi.

**Muhim eslatma:** `src/tts.py` faylida Aisha AI'ning endpoint/parametrlari
taxminiy (eng keng tarqalgan TTS API shakli bo'yicha) yozilgan. Ro'yxatdan
o'tgach ularning developer hujjatidan **aniq endpoint va parametr nomlarini**
tekshirib, shu faylga moslashtiring — API'lar vaqti bilan o'zgarishi mumkin.

## 2-qadam: YouTube uchun OAuth sozlash
1. console.cloud.google.com'da yangi loyiha oching
2. "YouTube Data API v3" ni yoqing (Enable API)
3. "OAuth consent screen" ni sozlang, o'zingizni "Test user" qilib qo'shing
4. "Credentials" → "Create Credentials" → "OAuth client ID" → **Desktop app**
5. `client_id` va `client_secret` ni oling

O'z kompyuteringizda (bir martalik):
```bash
pip install google-auth-oauthlib python-dotenv
# .env fayliga YT_CLIENT_ID va YT_CLIENT_SECRET yozing
python get_youtube_token.py
```
Chiqqan `YT_REFRESH_TOKEN` qiymatini saqlab qo'ying.

## 3-qadam: GitHub'ga joylash
1. Ushbu papkani yangi GitHub repository (public bo'lsa Actions cheksiz bepul) qilib yuklang
2. Repo → **Settings → Secrets and variables → Actions → New repository secret**
   — quyidagilarni qo'shing:
   - `GROQ_API_KEY`
   - `ANTHROPIC_API_KEY` (ixtiyoriy)
   - `AISHA_API_KEY`
   - `YT_CLIENT_ID`
   - `YT_CLIENT_SECRET`
   - `YT_REFRESH_TOKEN`
3. **Settings → Secrets and variables → Actions → Variables** bo'limiga:
   - `CHANNEL_NICHE` = kanalingiz mavzusi tavsifi

## 4-qadam: Sinab ko'rish
Repo → **Actions** tab → "Kunlik video yaratish va yuklash" → **Run workflow**
tugmasini bosing (jadval kutmasdan qo'lda ishga tushirish).

Xato chiqsa, loglarni o'qing — ko'pincha TTS yoki YouTube kalitlari sabab bo'ladi.

## Keyin nima?
- Jadval har kuni Toshkent vaqti bilan soat 09:00 da avtomatik ishlaydi (`daily.yml` ichida `cron` qatorini o'zgartirib vaqtni sozlashingiz mumkin)
- `assets/background_music.mp3` ga mualliflik huquqisiz fon musiqa qo'ysangiz, videolarga avtomatik qo'shiladi (ixtiyoriy)
- YouTube bepul kvotasi kuniga ~6 ta yuklashga yetadi — 3 ta video shu doirada bemalol sig'adi

## Xarajat taxmini (oyiga)
- Groq + Pollinations: $0
- Aisha AI: ularning narxiga bog'liq (odatda belgi/soniya asosida arzon)
- Anthropic ishlatilsa: video boshiga bir necha sent
- GitHub Actions: public repo uchun $0
- YouTube API: $0

Umuman, oyiga bir necha dollardan oshmasligi kerak.
