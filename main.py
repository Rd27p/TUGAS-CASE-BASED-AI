import csv

# Membership Functions
def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x < c:
        return (c - x) / (c - b)
    return 0

def fuzzify_service(x):
    return {
        "low": triangular(x, 0, 30, 50),
        "medium": triangular(x, 30, 50, 70),
        "high": triangular(x, 50, 70, 100)
    }

def fuzzify_price(x):
    return {
        "cheap": triangular(x, 25000, 30000, 40000),
        "medium": triangular(x, 30000, 40000, 50000),
        "expensive": triangular(x, 40000, 50000, 55000)
    }

# Skor defuzzifikasi
score_values = {
    "very_bad": 10,
    "bad": 30,
    "fair": 50,
    "good": 70,
    "very_good": 90
}

# Fuzzy Inference
def inference(service, price):
    rules = [
        (min(service["high"], price["cheap"]), "very_good"),
        (min(service["high"], price["medium"]), "good"),
        (min(service["high"], price["expensive"]), "fair"),
        (min(service["medium"], price["cheap"]), "good"),
        (min(service["medium"], price["medium"]), "fair"),
        (min(service["medium"], price["expensive"]), "bad"),
        (min(service["low"], price["cheap"]), "fair"),
        (min(service["low"], price["medium"]), "bad"),
        (min(service["low"], price["expensive"]), "very_bad")
    ]

    numerator = sum(weight * score_values[label] for weight, label in rules)
    denominator = sum(weight for weight, _ in rules)
    return numerator / denominator if denominator != 0 else 0

# Membaca CSV
def read_csv(filename):
    data = []
    with open(filename, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        reader.fieldnames = [h.strip() for h in reader.fieldnames]
        for row in reader:
            data.append({
                "id": int(row["id Pelanggan"]),
                "service": float(row["Pelayanan"]),
                "price": float(row["harga"])
            })
    return data

# Menulis CSV
def write_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["ID Pelanggan", "Pelayanan", "Harga", "Score"])
        for d in data:
            writer.writerow([d["id"], d["service"], d["price"], round(d["score"], 2)])

# Fungsi pengambil skor untuk sort
def ambil_score(item):
    return item["score"]

def main():
    data = read_csv("restoran.csv")
    scored_data = []

    for item in data:
        service_membership = fuzzify_service(item["service"])
        price_membership = fuzzify_price(item["price"])
        score = inference(service_membership, price_membership)
        item["score"] = score
        scored_data.append(item)

    # Urutkan berdasarkan skor tertinggi tanpa lambda
    scored_data.sort(key=ambil_score, reverse=True)
    top_5 = scored_data[:5]

    # Tulis hasil ke file CSV baru
    write_csv(top_5, "peringkat.csv")

    # Tampilkan hasil di terminal
    print("Top 5 Restoran Terbaik:")
    for r in top_5:
        print(f"ID: {r['id']}, Service: {r['service']}, Price: {r['price']}, Score: {round(r['score'], 2)}")

if __name__ == "__main__":
    main()
