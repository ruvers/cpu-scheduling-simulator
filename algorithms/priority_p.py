# Priority Scheduling (Preemptive) Algoritmasi
# Kesintili oncelik tabanli zamanlama


def priority_preemptive(proc_data):
    """
    Priority Scheduling - Oncelik tabanli zamanlama (Preemptive)
    
    Calisma Prensibi:
        - Her zaman biriminde en yuksek oncelikli proses secilir
        - Dusuk oncelik degeri = Yuksek oncelik
        - Daha yuksek oncelikli proses gelirse mevcut kesilir
        - Esitlik durumunda PID sirasina gore karar verilir
    
    Parametreler:
        proc_data: Proses listesi
    
    Dondurur:
        dict: timeline, processes, context_switches, log
    """
    event_history = []
    proc_data = [p.copy() for p in proc_data]

    # Her proses icin kalan sure ve baslama zamani
    for p in proc_data:
        p["remaining"] = p["burst"]
        p["start_time"] = None

    time = 0
    done_list = []
    execution_timeline = []
    active_proc = None
    switch_count = 0
    seen_pids = set()
    prev_running = None  # Baglam degisimi icin kritik

    # Tum prosesler tamamlanana kadar devam et
    while len(done_list) < len(proc_data):

        # Varis olaylarini kontrol et
        for p in proc_data:
            if p["arrival"] == time and p["pid"] not in seen_pids:
                event_history.append(f"t={time}: {p['pid']} arrives")
                seen_pids.add(p["pid"])

        # Hazir prosesleri bul
        available_procs = [p for p in proc_data if p["arrival"] <= time and p["remaining"] > 0]

        # Hazir proses yoksa zamani ilerlet
        if not available_procs:
            time += 1
            continue

        # En yuksek oncelikli prosesi sec
        available_procs.sort(key=lambda p: (p["priority"], p["pid"]))
        chosen = available_procs[0]
        chosen_pid = chosen["pid"]

        # Baglam degisimi sayimi
        if prev_running is not None and chosen_pid != prev_running:
            switch_count += 1

        # Proses degisimi (dispatch veya preemption)
        if active_proc != chosen:
            # Kesme durumu
            if active_proc and active_proc["remaining"] > 0:
                event_history.append(f"t={time}: {chosen_pid} preempts {active_proc['pid']}")
            # Ilk calisma
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

        prev_running = chosen_pid

        # Tamamlanma kontrolu
        if active_proc["remaining"] == 0:
            active_proc["completion_time"] = time
            done_list.append(active_proc)
            event_history.append(f"t={time}: {active_proc['pid']} completes")
            active_proc = None
            # prev_running sifirlanmaz

    return {
        "timeline": execution_timeline,
        "processes": done_list,
        "context_switches": switch_count,
        "log": event_history
    }

