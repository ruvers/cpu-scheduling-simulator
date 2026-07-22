# SRTF (Shortest Remaining Time First) Algoritmasi
# SJF'nin kesintili (preemptive) versiyonu


def shortest_remaining_first(proc_data):
    """
    SRTF - En kisa kalan sure ilk algoritmasi (Preemptive SJF)
    
    Calisma Prensibi:
        - Her zaman biriminde en az kalan sureli proses secilir
        - Yeni gelen proses daha kisa kalan sureye sahipse mevcut kesilir
        - Esitlik durumunda PID sirasina gore karar verilir
    
    Parametreler:
        proc_data: Proses listesi
    
    Dondurur:
        dict: timeline, processes, context_switches, log
    """
    event_history = []
    proc_data = [p.copy() for p in proc_data]

    # Her proses icin kalan sureyi ve baslama zamanini ayarla
    for p in proc_data:
        p["remaining"] = p["burst"]
        p["start_time"] = None

    time = 0
    done_list = []
    execution_timeline = []
    switch_count = 0
    active_proc = None
    seen_pids = set()
    prev_running = None  # Baglam degisimi icin kritik degisken

    # Tum prosesler tamamlanana kadar simulasyonu calistir
    while len(done_list) < len(proc_data):

        # Varis olaylarini kontrol et ve kaydet
        for p in proc_data:
            if p["arrival"] == time and p["pid"] not in seen_pids:
                event_history.append(f"t={time}: {p['pid']} arrives")
                seen_pids.add(p["pid"])

        # Hazir prosesleri bul (varmis ve kalan suresi > 0)
        available_procs = [p for p in proc_data if p["arrival"] <= time and p["remaining"] > 0]

        # Hazir proses yoksa zamani ilerlet
        if not available_procs:
            time += 1
            continue

        # En az kalan sureli prosesi sec
        available_procs.sort(key=lambda p: (p["remaining"], p["pid"]))
        chosen = available_procs[0]
        chosen_pid = chosen["pid"]

        # Baglam degisimi sayimi - farkli proses secildiyse
        if prev_running is not None and chosen_pid != prev_running:
            switch_count += 1

        # Proses degisimi (dispatch veya preemption)
        if active_proc != chosen:
            # Kesme durumu - mevcut proses henuz bitmedi
            if active_proc and active_proc["remaining"] > 0:
                event_history.append(f"t={time}: {chosen_pid} preempts {active_proc['pid']}")
            # Ilk kez calisiyor
            if chosen["start_time"] is None:
                chosen["start_time"] = time
                event_history.append(f"t={time}: {chosen_pid} starts running")
            active_proc = chosen

        event_history.append(f"t={time}: {active_proc['pid']} running")

        # Zaman cizelgesini guncelle
        if execution_timeline and execution_timeline[-1]["pid"] == active_proc["pid"]:
            execution_timeline[-1]["end"] += 1
        else:
            execution_timeline.append({"pid": active_proc["pid"], "start": time, "end": time + 1})

        # 1 birim zaman calistir
        active_proc["remaining"] -= 1
        time += 1

        # Onceki calisan prosesi guncelle
        prev_running = chosen_pid

        # Tamamlanma kontrolu
        if active_proc["remaining"] == 0:
            active_proc["completion_time"] = time
            done_list.append(active_proc)
            event_history.append(f"t={time}: {active_proc['pid']} completes")
            active_proc = None
            # prev_running sifirlanmaz - sonraki karsilastirma icin gerekli

    return {
        "timeline": execution_timeline,
        "processes": done_list,
        "context_switches": switch_count,
        "log": event_history
    }

