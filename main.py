import csv

# Fungsi Membership
def segitiga(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x < c:
        return (c - x) / (c - b)
    return 0

def fuzzifikasi_pelayanan(x):
    return {
        "rendah": segitiga(x, 0, 30, 50),
        "sedang": segitiga(x, 30, 50, 70),
        "tinggi": segitiga(x, 50, 70, 100)
    }

def fuzzifikasi_harga(x):
    return {
        "murah": segitiga(x, 25000, 30000, 40000),
        "sedang": segitiga(x, 30000, 40000, 50000),
        "mahal": segitiga(x, 40000, 50000, 55000)
    }

# Nilai skor defuzzifikasi
nilai_skor = {
    "sangat_buruk": 10,
    "buruk": 30,
    "cukup": 50,
    "baik": 70,
    "sangat_baik": 90
}

# Aturan Inferensi Fuzzy
def inferensi(pelayanan, harga):
    aturan = [
        {"nilai": min(pelayanan["tinggi"], harga["murah"]),     "label": "sangat_baik"},
        {"nilai": min(pelayanan["tinggi"], harga["sedang"]),    "label": "baik"},
        {"nilai": min(pelayanan["tinggi"], harga["mahal"]),     "label": "cukup"},
        {"nilai": min(pelayanan["sedang"], harga["murah"]),     "label": "baik"},
        {"nilai": min(pelayanan["sedang"], harga["sedang"]),    "label": "cukup"},
        {"nilai": min(pelayanan["sedang"], harga["mahal"]),     "label": "buruk"},
        {"nilai": min(pelayanan["rendah"], harga["murah"]),     "label": "cukup"},
        {"nilai": min(pelayanan["rendah"], harga["sedang"]),    "label": "buruk"},
        {"nilai": min(pelayanan["rendah"], harga["mahal"]),     "label": "sangat_buruk"}
    ]
    return aturan

# Defuzzifikasi
def defuzzifikasi(aturan):
    pembilang = 0
    penyebut = 0

    for rule in aturan:
        bobot = rule["nilai"]
        label = rule["label"]
        pembilang += bobot * nilai_skor[label]
        penyebut += bobot

    if penyebut == 0:
        return 0
    else:
        return pembilang / penyebut

# Membaca CSV
def baca_csv(nama_file):
    data = []
    with open(nama_file, newline='', encoding='utf-8-sig') as csvfile:
        pembaca = csv.DictReader(csvfile, delimiter=';')
        pembaca.fieldnames = [h.strip() for h in pembaca.fieldnames]
        for baris in pembaca:
            data.append({
                "id": int(baris["id Pelanggan"]),
                "pelayanan": float(baris["Pelayanan"]),
                "harga": float(baris["harga"])
            })
    return data

# Menulis CSV
def tulis_csv(data, nama_file):
    with open(nama_file, mode='w', newline='', encoding='utf-8') as csvfile:
        penulis = csv.writer(csvfile, delimiter=';')
        penulis.writerow(["ID Pelanggan", "Pelayanan", "Harga", "Skor"])
        for d in data:
            penulis.writerow([d["id"], d["pelayanan"], d["harga"], round(d["skor"], 2)])

# Fungsi pengambil skor untuk pengurutan
def ambil_skor(item):
    return item["skor"]

def main():
    data = baca_csv("restoran.csv")
    data_dengan_skor = []

    for item in data:
        keanggotaan_pelayanan = fuzzifikasi_pelayanan(item["pelayanan"])
        keanggotaan_harga = fuzzifikasi_harga(item["harga"])
        aturan_fuzzy = inferensi(keanggotaan_pelayanan, keanggotaan_harga)
        skor = defuzzifikasi(aturan_fuzzy)
        item["skor"] = skor
        data_dengan_skor.append(item)

    # Urutkan berdasarkan skor tertinggi 
    data_dengan_skor.sort(key=ambil_skor, reverse=True)
    lima_terbaik = data_dengan_skor[:5]

    # Tulis hasil ke file CSV baru
    tulis_csv(lima_terbaik, "peringkat.csv")

    # Tampilkan hasil di terminal
    print("Top 5 Restoran Terbaik:")
    for r in lima_terbaik:
        print(f"ID: {r['id']}, Pelayanan: {r['pelayanan']}, Harga: {r['harga']}, Skor: {round(r['skor'], 2)}")

if __name__ == "__main__":
    main()
