# SJF (Shortest Job First) Algoritmasi - Kesintisiz
# En kisa burst sureli proses oncelikli olarak calistirilir


def shortest_job_first(proc_data):
    """
    SJF - En kisa is ilk algoritmasi (Non-preemptive)
    
    Calisma Prensibi:
        - Hazir kuyrugundaki en kisa burst sureli proses secilir
        - Proses tamamlanana kadar calisir (kesme yok)
        - Esitlik durumunda PID sirasina gore karar verilir
    
    Parametreler:
        proc_data: Proses listesi
    
    Dondurur:
        dict: timeline, processes, context_switches, log
    """
    event_history = []
    proc_data = [p.copy() for p in proc_data]
    proc_data.sort(key=lambda p: (p["arrival"], p["pid"]))

    # Varis olaylarini kaydet
    for p in proc_data:
        event_history.append(f"t={p['arrival']}: {p['pid']} arrives")

    clock = 0
    execution_timeline = []
    switch_count = 0

    done_list = []
    pending_list = proc_data.copy()
    prev_running = None

    # Tum prosesler tamamlanana kadar devam et
    while pending_list:
        # Hazir prosesleri bul (varisi <= mevcut zaman)
        available_procs = [p for p in pending_list if p["arrival"] <= clock]

        # Hazir proses yoksa zamani ilerlet
        if not available_procs:
            clock = min(p["arrival"] for p in pending_list)
            continue

        # En kisa burst sureli prosesi sec
        available_procs.sort(key=lambda p: (p["burst"], p["pid"]))
        p = available_procs[0]

        start = clock
        end = start + p["burst"]

        event_history.append(f"t={start}: {p['pid']} starts running")

        # Calisma suresi boyunca log kaydi
        for t in range(start + 1, end):
            event_history.append(f"t={t}: {p['pid']} running")

        execution_timeline.append({"pid": p["pid"], "start": start, "end": end})

        # Baglam degisimi kontrolu
        if prev_running is not None:
            switch_count += 1

        p["start_time"] = start
        p["completion_time"] = end

        event_history.append(f"t={end}: {p['pid']} completes")

        clock = end
        prev_running = p["pid"]
        pending_list.remove(p)
        done_list.append(p)

    return {
        "timeline": execution_timeline,
        "processes": done_list,
        "context_switches": switch_count,
        "log": event_history
    }

