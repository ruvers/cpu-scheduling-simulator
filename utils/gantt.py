# Gantt semasi cizim modulu
# Proses calisma zaman cizelgesini gorsel olarak yazdirir


def display_gantt(segments):
    """
    Gantt semasini yazdirir

    Parametreler:
        segments: Zaman dilimi listesi
                  Her dilim {pid, start, end} icerir
    """
    render_chart(segments)


def render_chart(segments, unit_width=4):
    """
    Gantt semasini cizer

    Parametreler:
        segments: Zaman dilimi listesi
        unit_width: Her zaman biriminin karakter genisligi
    """
    # Bos cizelge kontrolu
    if not segments:
        print("Empty timeline")
        return

    # Maksimum zamani bul
    max_time = max(block["end"] for block in segments)

    # Zaman basligini yazdir
    print("Time:", end=" ")
    for t in range(max_time + 1):
        # Zaman numaralarini hizala
        print(f"{t:<{unit_width}}", end="")
    print()

    # Grafik satirini hazirla
    chart_row = [" "] * (max_time * unit_width)

    # Her zaman dilimi icin grafik ciz
    for block in segments:
        pid = str(block["pid"])
        start_pos = block["start"] * unit_width
        end_pos = block["end"] * unit_width
        block_width = end_pos - start_pos

        # Kenarliklari ciz
        if block_width >= 2:
            chart_row[start_pos] = "|"
            chart_row[end_pos - 1] = "|"
        else:
            # Cok kucuk dilim - atla
            continue

        # Ic kismi tire ile doldur
        for i in range(start_pos + 1, end_pos - 1):
            chart_row[i] = "-"

        # Etiket alanini hesapla
        interior = block_width - 2
        if interior <= 0:
            continue

        # Etiketi belirle (sigmazsa kisalt)
        label = pid
        if len(label) > interior:
            # "P2" sigmiyorsa sadece "2" kullan
            label = pid[-1] if len(pid) >= 1 else ""
            if len(label) > interior:
                label = ""  # Hala sigmiyorsa bos birak

        # Etiketi ortala ve yerlestir
        if label:
            mid = start_pos + 1 + (interior - len(label)) // 2
            for i, ch in enumerate(label):
                chart_row[mid + i] = ch

    # Grafik satirini yazdir
    print("      " + "".join(chart_row))
