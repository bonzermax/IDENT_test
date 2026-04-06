import random
import time
from datetime import datetime, timedelta
from concurrent.futures import ProcessPoolExecutor

random.seed(42)

receptions = [
    {
        "patient_id": pid,
        "reception_start": datetime(2017, 6, 30)
        - timedelta(days=random.randint(1, 500)),
    }
    for pid in range(1, 500_001)
    for _ in range(random.randint(0, 5))
]

patients = [{"id": pid, "surname": f"Иванов{pid}"} for pid in range(1, 500_001)]

# Решение №1
time_start = time.perf_counter()
receptions_le_2017 = {
    r["patient_id"] for r in receptions if r["reception_start"] <= datetime(2017, 1, 1)
}
patients = [p for p in patients if p["id"] in receptions_le_2017]
time_end = time.perf_counter()

result_time = time_end - time_start
print(f"Время выполнения решения №1: {result_time:.3f}")

# Решение №2
time_start = time.perf_counter()

receptions_le_2017 = []
for pat in patients:
    for rec in receptions:
        if rec["patient_id"] == pat["id"] and rec["reception_start"] <= datetime(2017, 1, 1):
            receptions_le_2017.append(pat)
            break

result_time = time.perf_counter() - time_start
print(f"Время выполнения решения №2: {result_time:.3f}")

# Решение №1 O(len(patients) + len(receptions))
# Решение №2 O(len(patients) * len(receptions))
# №1 быстрее засчёт использования set
