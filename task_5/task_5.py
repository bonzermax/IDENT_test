import random
import time
import pandas as pd

from datetime import datetime, timedelta

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
    r["patient_id"]
    for r in receptions
    if r["reception_start"] <= datetime(2017, 12, 31)
}
patients = [p for p in patients if p["id"] in receptions_le_2017]

time_end = time.perf_counter()

result_time = time_end - time_start
print(f"Время выполнения решения №1: {result_time:.3f}")

# Решение №2
time_start = time.perf_counter()

df_receptions = pd.DataFrame(receptions)
df_patients = pd.DataFrame(patients)
df = df_patients.merge(
    df_receptions, left_on="id", right_on="patient_id", how="left"
).drop(columns="patient_id")

filtered_df = df.loc[(df["reception_start"] <= "2017-12-31")]
filtered_patients = (
    filtered_df[["id", "surname"]]
    .drop_duplicates(subset="id")
    .to_dict(orient="records")
)

time_end = time.perf_counter()

result_time = time_end - time_start
print(f"Время выполнения решения №2: {result_time:.3f}")

# Оба решения по сложности: O(len(patients) + len(receptions))
# Время выполнения решения №1: 0.510
# Время выполнения решения №2: 2.300

# Вариант через pandas будет быстрее на больших объёмах данных, на небольших, как в нашем случае, выходит медленнее из-за процесса инициализации датафреймов
