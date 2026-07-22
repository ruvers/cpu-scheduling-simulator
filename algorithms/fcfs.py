# FCFS (First Come First Serve) Algoritmasi
# Ilk gelen proses ilk hizmet alir - kesintisiz zamanlama


def first_come_first_serve(proc_data):
    """
    FCFS - Ilk gelen ilk hizmet alir algoritmasi
    
    Calisma Prensibi:
        - Prosesler varis sirasina gore kuyruktadir
        - CPU bos kalinca siradaki proses alinir
        - Proses tamamlanana kadar calisir (kesme yok)
    
    Parametreler:
        proc_data: Proses listesi (her biri dict: pid, arrival, burst, priority)
    
    Dondurur:
        dict: timeline, processes, context_switches, log
    """
    # Olay gecmisini baslat
    event_history = []

    # Orijinal veriyi degistirmemek icin kopya olustur
    proc_data = [p.copy() for p in proc_data]
    proc_data.sort(key=lambda p: (p["arrival"], p["pid"]))

    # Proses varislarini kaydet
    for p in proc_data:
        event_history.append(f"t={p['arrival']}: {p['pid']} arrives")

    clock = 0
    execution_timeline = []
    switch_count = 0

    # Her prosesi sirayla calistir
    for i, p in enumerate(proc_data):
        # CPU bos ise, sonraki prosesin varisina atla
        if clock < p["arrival"]:
            clock = p["arrival"]

        start = clock
        end = start + p["burst"]

        event_history.append(f"t={start}: {p['pid']} starts running")

        execution_timeline.append({
            "pid": p["pid"],
            "start": start,
            "end": end
        })

        # Baglam degisimi sayimi (ilk proses haric)
        if i > 0:
            switch_count += 1

        event_history.append(f"t={end}: {p['pid']} completes")

        p["start_time"] = start
        p["completion_time"] = end
        clock = end

    return {
        "timeline": execution_timeline,
        "processes": proc_data,
        "context_switches": switch_count,
        "log": event_history
    }

