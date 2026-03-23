"""
CIRCLE AI — Customer Chatbot
Tampilan chat only, tanpa knowledge loader
Deploy ini ke Streamlit Cloud lalu embed ke Framer
"""

import streamlit as st
import json
import os
import sys

sys.path.append(os.path.dirname(__file__))
from circle_ai_engine import CircleAIBrain

# ──────────────────────────────────────────────
#  KNOWLEDGE BASE — HARDCODE DI SINI
#  Ganti isi JSON sesuai bisnis client
# ──────────────────────────────────────────────
KNOWLEDGE = {
  "business_info": {
    "name": "Uluwatu Dream Villa",
    "tagline": "Luxury Feels, Affordable Price — Bali at Its Finest",
    "description": "Uluwatu Dream Villa adalah villa mewah dengan harga terjangkau yang berlokasi di tebing Uluwatu, Bali. Nikmati pemandangan laut lepas Samudra Hindia, kolam renang infinity pool pribadi, dan suasana Bali yang autentik. Cocok untuk pasangan, keluarga, maupun group liburan.",
    "location": "Jl. Pantai Suluban No. 88, Uluwatu, Pecatu, Kuta Selatan, Bali",
    "maps_link": "https://maps.google.com/?q=Uluwatu+Dream+Villa+Bali",
    "hours": {
      "Check-in": "14.00 WITA",
      "Check-out": "12.00 WITA",
      "Front Desk": "24 jam (selalu siap melayani)",
      "Kolam Renang": "06.00 - 22.00 WITA",
      "Restoran Villa": "07.00 - 22.00 WITA"
    },
    "contact": {
      "whatsapp": "+62 813-3800-8888",
      "instagram": "@uluwatudreamvilla",
      "email": "booking@uluwatudreamvilla.com",
      "phone": "+62 361-1234-5678"
    },
    "products": [
      {
        "name": "Deluxe Ocean View Room",
        "price": "Rp 850.000 / malam",
        "description": "Kamar deluxe dengan balkon private menghadap Samudra Hindia. Dilengkapi AC, TV 55 inch, dan kamar mandi mewah dengan bathtub.",
        "features": "Kapasitas 2 orang • Sarapan included • Free WiFi"
      },
      {
        "name": "Private Pool Villa",
        "price": "Rp 2.100.000 / malam",
        "description": "Villa pribadi dengan kolam renang infinity pool menghadap laut. Ruang tamu, dapur kecil, dan teras luas untuk bersantai.",
        "features": "Kapasitas 2-4 orang • Sarapan included • Butler service • Free airport transfer"
      },
      {
        "name": "Family Cliff Villa",
        "price": "Rp 3.500.000 / malam",
        "description": "Villa keluarga besar di tepi tebing dengan 3 kamar tidur, ruang keluarga, dapur lengkap, dan kolam renang pribadi dengan pemandangan tebing dramatis.",
        "features": "Kapasitas 6 orang • Sarapan included • Dedicated butler • BBQ area • Free airport transfer"
      },
      {
        "name": "Honeymoon Cliffside Suite",
        "price": "Rp 2.800.000 / malam",
        "description": "Suite romantis khusus pasangan di tepi tebing. Dilengkapi jacuzzi outdoor, dekorasi bunga, dan candle light dinner private.",
        "features": "Kapasitas 2 orang • Sarapan romantis • Welcome drink • Rose bath • Free couples massage 60 menit"
      },
      {
        "name": "Group Retreat Package",
        "price": "Mulai Rp 8.000.000 / malam",
        "description": "Paket eksklusif untuk group 10-20 orang. Sewa villa keseluruhan dengan fasilitas lengkap, chef pribadi, dan aktivitas group.",
        "features": "10-20 orang • Full board meals • Private chef • Activity organizer • Free shuttle"
      }
    ],
    "promo": "🌙 PROMO RAMADHAN SPESIAL!\n\n✨ Diskon 40% untuk semua tipe kamar & villa!\nBerlaku: 1 Ramadhan - 10 Syawal 1446 H\n\n🎁 Bonus spesial:\n• Gratis welcome dates & kurma untuk setiap tamu\n• Gratis sahur box delivery ke kamar\n• Gratis one way airport transfer\n• Gratis akses ke sunset point eksklusif\n• Diskon 30% untuk couple spa treatment\n\n📋 Syarat & Ketentuan:\n• Minimal menginap 2 malam\n• Pemesanan sebelum 25 Ramadhan\n• Tidak berlaku untuk tanggal merah lebaran\n• Bayar DP 30% untuk konfirmasi booking\n\n📱 Booking sekarang via WhatsApp: +62 813-3800-8888\nKode promo: RAMADHAN40",
    "recommendation": "Rekomendasi terbaik dari kami:\n\n💑 Pasangan / Honeymoon:\n→ Honeymoon Cliffside Suite — paling romantis!\n\n👨‍👩‍👧 Keluarga:\n→ Family Cliff Villa — ruang luas, anak-anak betah\n\n👥 Group / Trip bareng teman:\n→ Group Retreat Package — harga paling hemat per orang\n\n🎯 First timer ke Bali:\n→ Private Pool Villa — balance antara mewah & harga",
    "faq": [
      {
        "questions": ["cara booking", "cara pesan", "bagaimana reservasi", "booking gimana", "cara memesan kamar"],
        "answer": "📋 **Cara Booking Uluwatu Dream Villa:**\n\n1️⃣ Hubungi WhatsApp: +62 813-3800-8888\n2️⃣ Pilih tipe kamar & tanggal check-in/out\n3️⃣ Bayar DP 30% untuk konfirmasi\n4️⃣ Pelunasan H-7 sebelum check-in\n5️⃣ Dapat voucher & detail lokasi\n\n✅ Booking juga bisa via:\n• Email: booking@uluwatudreamvilla.com\n• Instagram DM: @uluwatudreamvilla\n• Traveloka & Tiket.com (tanpa promo Ramadhan)"
      },
      {
        "questions": ["fasilitas apa saja", "ada fasilitas apa", "apa yang tersedia", "amenities"],
        "answer": "🏊 **Fasilitas Uluwatu Dream Villa:**\n\n**Fasilitas Umum:**\n• Infinity pool dengan view laut\n• Restoran & bar rooftop\n• Spa & massage center\n• Yoga deck di tepi tebing\n• Sunset viewing point eksklusif\n• Parkir luas & aman\n• 24/7 security\n\n**Fasilitas Kamar:**\n• AC & kipas angin\n• TV 55 inch Smart TV\n• Mini bar\n• Safe deposit box\n• Toiletries premium\n• Free WiFi 100 Mbps\n\n**Layanan:**\n• Airport transfer (beberapa paket)\n• Laundry service\n• Room service 24 jam\n• Concierge & tour organizer"
      },
      {
        "questions": ["berapa jauh dari bandara", "jarak dari bandara", "akses dari bandara ngurah rai", "transport dari bandara"],
        "answer": "✈️ **Dari Bandara Ngurah Rai:**\n\nJarak: ±25 km\nWaktu tempuh: 45-60 menit (tergantung traffic)\n\n**Pilihan transportasi:**\n• Grab/Gojek: Rp 80.000 - 120.000\n• Taksi bandara: Rp 150.000 - 200.000\n• Free airport transfer: tersedia di paket Private Pool Villa, Family Cliff Villa, Honeymoon Suite & Group Package\n\n💡 Tip: Pesan free transfer saat booking untuk hemat biaya!"
      },
      {
        "questions": ["bisa bawa anak", "ramah anak", "family friendly", "ada aktivitas anak"],
        "answer": "👶 **Ya, sangat family friendly!**\n\nUluwatu Dream Villa cocok untuk keluarga dengan anak:\n• Baby cot tersedia (gratis, request saat booking)\n• Menu anak-anak di restoran\n• Area bermain anak\n• Family Cliff Villa punya ruang luas & aman\n• Staff berpengalaman melayani tamu keluarga\n\n⚠️ Perhatian: Kolam renang tidak ada penjaga khusus, awasi anak-anak di area kolam ya!"
      },
      {
        "questions": ["kebijakan pembatalan", "cancel booking", "refund", "batalkan pesanan"],
        "answer": "❌ **Kebijakan Pembatalan:**\n\n• Batalkan 14+ hari sebelum check-in: Refund 100% DP\n• Batalkan 7-13 hari sebelum check-in: Refund 50% DP\n• Batalkan kurang dari 7 hari: DP tidak dapat dikembalikan\n• No show: Tidak ada refund\n\n🔄 **Reschedule:**\nBisa dilakukan gratis hingga 3 hari sebelum check-in (tergantung ketersediaan kamar).\n\nHubungi kami ASAP jika ada perubahan rencana!"
      },
      {
        "questions": ["aktivitas di sekitar", "tempat wisata dekat", "apa yang bisa dilakukan", "wisata uluwatu"],
        "answer": "🌊 **Aktivitas di Sekitar Uluwatu:**\n\n**Wajib dikunjungi:**\n• Pura Luhur Uluwatu (5 menit) — sunset & kecak dance\n• Pantai Suluban / Blue Point (5 menit) — surfing & snorkeling\n• Pantai Padang Padang (10 menit) — Eat Pray Love beach!\n• GWK Cultural Park (20 menit)\n\n**Water Sports:**\n• Surfing lesson: Rp 350.000/sesi\n• Snorkeling trip: Rp 250.000/orang\n• Sunset cruise: Rp 500.000/orang\n\n💡 Concierge kami siap bantu atur semua aktivitas & transportasi!"
      },
      {
        "questions": ["ada kolam renang", "kolam renang private", "infinity pool", "swimming pool"],
        "answer": "🏊 **Kolam Renang Uluwatu Dream Villa:**\n\n• **Infinity Pool Umum** — view laut lepas, buka 06.00-22.00\n• **Private Pool** — khusus tamu Private Pool Villa & Family Cliff Villa\n• **Rooftop Jacuzzi** — khusus tamu Honeymoon Suite\n\nSemua kolam menghadap Samudra Hindia — dijamin foto-nya stunning! 📸"
      },
      {
        "questions": ["sarapan", "breakfast", "ada makanan apa", "menu restoran"],
        "answer": "🍳 **Sarapan & Restoran:**\n\n**Sarapan (included di semua paket):**\nServed 07.00 - 10.00 WITA\nMenu: Continental + Indonesian breakfast\nLokasi: Restoran rooftop dengan view laut\n\n**Restoran Villa:**\n• Buka 07.00 - 22.00 WITA\n• Menu Indonesian, Western & Asian fusion\n• Range harga: Rp 45.000 - 250.000\n• Bar & cocktail tersedia\n• Sunset dinner — WAJIB DICOBA! 🌅"
      }
    ]
  },
  "qa_pairs": [
    {
      "questions": ["worth it tidak", "mahal tidak", "harga sesuai tidak", "recommended"],
      "answer": "💯 **Sangat worth it!**\n\nUluwatu Dream Villa menawarkan pengalaman mewah dengan harga yang jauh lebih terjangkau dibanding villa bintang 5 di kawasan yang sama.\n\nYang kamu dapat:\n✅ View laut Samudra Hindia yang dramatis\n✅ Infinity pool pribadi (beberapa paket)\n✅ Sarapan included setiap hari\n✅ Lokasi strategis dekat Pura Uluwatu\n✅ Service bintang 5 yang personal\n\nTerbukti dari 500+ review bintang 5 di Google & TripAdvisor! ⭐"
    },
    {
      "questions": ["promo ramadhan", "diskon ramadhan", "ramadhan deal", "promo puasa"],
      "answer": "🌙 **Promo Ramadhan 40% OFF!**\n\nIni promo terbesar kami sepanjang tahun!\n\n✨ Diskon 40% semua tipe kamar\n🎁 Gratis welcome dates & kurma\n🌙 Gratis sahur box ke kamar\n✈️ Gratis one way airport transfer\n🌅 Akses sunset point eksklusif\n💆 Diskon 30% couple spa\n\nKode promo: **RAMADHAN40**\nMinimal 2 malam • Berlaku sampai 10 Syawal\n\nBuruan book sekarang sebelum kehabisan!\n📱 WhatsApp: +62 813-3800-8888"
    },
    {
      "questions": ["bisa sahur", "ada sahur", "fasilitas ramadhan", "buka puasa"],
      "answer": "🌙 **Fasilitas Ramadhan Spesial:**\n\n• **Sahur Box** — diantar ke kamar, gratis selama promo Ramadhan\n• **Buka Puasa Set** — menu spesial Ramadhan di restoran\n• **Takjil Welcome** — dates & kurma saat check-in\n• **Waktu Sholat** — tersedia sajadah & arah kiblat di kamar\n• **Musholla** — tersedia di area villa\n\nKami menghormati dan memfasilitasi tamu yang berpuasa sepenuh hati 🤲"
    },
    {
      "questions": ["honeymoon", "bulan madu", "paket honeymoon", "romantic"],
      "answer": "💑 **Honeymoon di Uluwatu Dream Villa:**\n\nHoneymoon Cliffside Suite adalah pilihan sempurna!\n\n✨ Yang kamu dapat:\n• Kamar di tepi tebing dengan view laut\n• Jacuzzi outdoor romantis\n• Rose bath setup\n• Dekorasi bunga & candle\n• Sarapan romantis di balkon\n• Free couples massage 60 menit\n• Welcome drink & fruit basket\n\nHarga: Rp 2.800.000/malam (sebelum diskon Ramadhan)\n\nMau buat honeymoon tak terlupakan? 📱 +62 813-3800-8888"
    }
  ]
}

# ──────────────────────────────────────────────
#  PAGE CONFIG — MINIMAL, UNTUK EMBED
# ──────────────────────────────────────────────
st.set_page_config(
    page_title=f"CIRCLE AI — {KNOWLEDGE['business_info']['name']}",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ──────────────────────────────────────────────
#  CSS — CLEAN CHAT UI
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

/* Sembunyikan header & footer Streamlit */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.block-container { padding-top: 1rem !important; }

.chat-header {
    text-align: center;
    padding: 16px 0 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 16px;
}

.chat-name {
    font-size: 1.1rem;
    font-weight: 700;
    background: linear-gradient(135deg, #00f5d4, #00bbf9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.chat-status {
    font-size: 0.75rem;
    color: #00f5d4;
    margin-top: 2px;
}

.bubble-user {
    background: linear-gradient(135deg, #00f5d4, #00bbf9);
    color: #000;
    padding: 10px 14px;
    border-radius: 16px 16px 4px 16px;
    margin: 6px 0;
    margin-left: 15%;
    font-size: 0.9rem;
    font-weight: 500;
}

.bubble-ai {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    color: #e8eaf6;
    padding: 10px 14px;
    border-radius: 16px 16px 16px 4px;
    margin: 6px 0;
    margin-right: 15%;
    font-size: 0.9rem;
    line-height: 1.5;
}

.suggestion-label {
    font-size: 0.75rem;
    color: #4a5568;
    margin: 12px 0 6px 0;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  INIT BRAIN — LOAD SEKALI, SIMPAN DI SESSION
# ──────────────────────────────────────────────
if "brain" not in st.session_state:
    brain = CircleAIBrain()
    brain.load_knowledge_from_dict(KNOWLEDGE)
    st.session_state.brain = brain

if "messages" not in st.session_state:
    st.session_state.messages = []

brain = st.session_state.brain
biz_name = KNOWLEDGE["business_info"]["name"]

# ──────────────────────────────────────────────
#  HELPER
# ──────────────────────────────────────────────
def process_chat(text: str):
    st.session_state.messages.append({"role": "user", "content": text})
    response, confidence = brain.respond(text)
    st.session_state.messages.append({"role": "ai", "content": response})

# ──────────────────────────────────────────────
#  HEADER
# ──────────────────────────────────────────────
st.markdown(f"""
<div class="chat-header">
    <div class="chat-name">🧠 {biz_name} AI</div>
    <div class="chat-status">● Online — Siap membantu 24/7</div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  WELCOME MESSAGE
# ──────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown(f"""
    <div class="bubble-ai">
        Halo! 👋 Selamat datang di <b>{biz_name}</b>!<br><br>
        Saya asisten AI yang siap bantu kamu 24/7. 
        Tanya apa saja tentang menu, jadwal show, reservasi, atau lokasi kami! 😊
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  CHAT HISTORY
# ──────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="bubble-user">👤 {msg["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="bubble-ai">🧠 {msg["content"]}</div>',
            unsafe_allow_html=True
        )

# ──────────────────────────────────────────────
#  SUGGESTED QUESTIONS
# ──────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown('<div class="suggestion-label">💡 Pertanyaan populer:</div>', unsafe_allow_html=True)
    suggestions = [
        "Ada promo apa?",
        "Menu & harga?",
        "Cara reservasi?",
        "Dimana lokasinya?",
        "Ada wifi?"
    ]
    cols = st.columns(2)
    for i, sug in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(sug, key=f"s_{i}", use_container_width=True):
                process_chat(sug)
                st.rerun()

# ──────────────────────────────────────────────
#  INPUT CHAT
# ──────────────────────────────────────────────
user_input = st.chat_input("Tanya sesuatu...")
if user_input:
    process_chat(user_input)
    st.rerun()

# ──────────────────────────────────────────────
#  POWERED BY
# ──────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#2d3748;font-size:0.7rem;margin-top:20px">
    Powered by CIRCLE AI 🧠
</div>
""", unsafe_allow_html=True)