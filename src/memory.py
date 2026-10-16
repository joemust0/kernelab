def run_fifo(sequencia, num_frames):
    frames = []
    faults = 0
    for pag in sequencia:
        if pag not in frames:
            faults += 1
            if len(frames) >= num_frames:
                frames.pop(0)
            frames.append(pag)
    hits = len(sequencia) - faults
    taxa_faults = (faults / len(sequencia)) * 100
    return hits, faults, taxa_faults

def run_lru(sequencia, num_frames):
    frames = []
    faults = 0
    for pag in sequencia:
        if pag in frames:
            frames.remove(pag)
            frames.append(pag) 
        else:
            faults += 1
            if len(frames) >= num_frames:
                frames.pop(0) 
            frames.append(pag)
    hits = len(sequencia) - faults
    taxa_faults = (faults / len(sequencia)) * 100
    return hits, faults, taxa_faults