# Proses dosyasi okuyucu modulu
# Metin dosyasindan proses bilgilerini ayristirir


def load_process_file(filepath):
    """
    Proses dosyasini okur ve proses listesi dondurur

    Dosya formati (her satir):
        PID VARIS_ZAMANI BURST_SURESI ONCELIK

    Ornek:
        P1 0 8 2
        P2 1 4 1

    Parametreler:
        filepath: Proses dosyasinin yolu

    Dondurur:
        Proses sozluklerinin listesi
    """
    proc_list = []

    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()

            # Bos satirlari ve yorumlari atla
            if not line or line.startswith("#"):
                continue

            # Satiri parcala
            tokens = line.split()
            if len(tokens) != 4:
                raise ValueError(f"Invalid process line: {line}")

            pid, arrival, burst, priority = tokens

            # Proses sozlugu olustur
            proc_list.append({
                "pid": pid,
                "arrival": int(arrival),
                "burst": int(burst),
                "priority": int(priority)
            })

    return proc_list
