# Round Robin (RR) Algoritmasi
# Dairesel kuyruk zamanlama - her proses belirli bir zaman dilimi kadar calisir

from collections import deque


def circular_queue_scheduler(proc_data, quantum):
    """
    Round Robin - Dairesel kuyruk zamanlama algoritmasi
    
    Calisma Prensibi:
        - Her proses belirli bir zaman dilimi (quantum) kadar calisir
        - Quantum bitince proses kuyrugun sonuna eklenir
        - Adil bir zamanlama saglar - starvation olmaz
    
    Parametreler:
        proc_data: Proses listesi
        quantum: Her prosesin bir seferde calisabilecegi maksimum sure
    
    Dondurur:
        dict: timeline, processes, context_switches, log
    """
    event_history = []
    # Orijinal veriyi korumak icin kopya olustur
    proc_data = [p.copy() for p in proc_data]

    for p in proc_data:
        p["remaining"] = p["burst"]
        p["start_time"] = None

    # Varis zamani ve PID'ye gore sirala
    proc_data.sort(key=lambda p: (p["arrival"], p["pid"]))

    available_procs = deque()
    execution_timeline = []
    done_list = []
    time = 0
    index = 0
    prev_running = None
    switch_count = 0

    # Tum prosesler tamamlanana kadar devam et
    while len(done_list) < len(proc_data):
        # Mevcut zamana kadar varan prosesleri kuyruga ekle
        while index < len(proc_data) and proc_data[index]["arrival"] <= time:
            event_history.append(f"t={proc_data[index]['arrival']}: {proc_data[index]['pid']} arrives")
            available_procs.append(proc_data[index])
            index += 1

        # Hazir proses yoksa - CPU bosta
        if not available_procs:
            if index < len(proc_data):
                time = proc_data[index]["arrival"]
                continue
            else:
                break

        # Kuyruktan sonraki prosesi al
        p = available_procs.popleft()

        # Baglam degisimi kontrolu
        if prev_running is not None and prev_running != p["pid"]:
            switch_count += 1

        prev_running = p["pid"]

        # Ilk calisma zamani (response time icin)
        if p["start_time"] is None:
            p["start_time"] = time
            event_history.append(f"t={time}: {p['pid']} starts running")

        # Calisma suresi: quantum veya kalan sure (hangisi kucukse)
        exec_time = min(quantum, p["remaining"])
        start = time
        end = time + exec_time

        # Her zaman birimi icin log
        for t in range(start, end):
            event_history.append(f"t={t}: {p['pid']} running")

        # Gantt chart icin zaman dilimi ekle
        execution_timeline.append({"pid": p["pid"], "start": start, "end": end})
        p["remaining"] -= exec_time
        time = end

        # Calisma sirasinda varan prosesleri kuyruga ekle
        while index < len(proc_data) and proc_data[index]["arrival"] <= time:
            event_history.append(f"t={proc_data[index]['arrival']}: {proc_data[index]['pid']} arrives")
            available_procs.append(proc_data[index])
            index += 1

        # Proses bitti mi yoksa kuyruga geri mi donecek?
        if p["remaining"] > 0:
            event_history.append(f"t={time}: quantum expired for {p['pid']}")
            available_procs.append(p)
        else:
            p["completion_time"] = time
            done_list.append(p)
            event_history.append(f"t={time}: {p['pid']} completes")

    return {
        "timeline": execution_timeline,
        "processes": done_list,
        "context_switches": switch_count,
        "log": event_history
    }

