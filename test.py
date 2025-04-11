import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import *

# открываем файл
FLIGHTS = pd.read_csv('flights_NY.csv', delimiter=",", encoding='utf-8')  # укажи нужный разделитель
# убираем ячейки нан
FLIGHTS = FLIGHTS.dropna()
# находим значения чаще встречающиеся
top_values = FLIGHTS['dest'].value_counts().head(10).index
FLIGHTS_MOST_POP = FLIGHTS[FLIGHTS['dest'].isin(top_values)]

# считаем вероятность
counts = [len(FLIGHTS_MOST_POP[(FLIGHTS_MOST_POP['dest'] == top_values[i]) & (FLIGHTS_MOST_POP['arr_delay'] > 0)]) for i in range(10)]
all_fl_counts = FLIGHTS_MOST_POP['dest'].value_counts()
probability = [counts[i]/all_fl_counts.iloc[i] for i in range(10)]

# Создание столбчатой диаграммы
plt.figure(figsize=(10, 5))
plt.bar(top_values, probability, color='skyblue')
plt.yticks(np.arange(0, 0.5, 0.05))

# Подписи и заголовок
plt.title('Вероятность положительной задержки для разных аэропортов')
plt.xlabel('аэропорты')
plt.ylabel('Вероятность')

# Показываем график
plt.show()

# Выбираем полёты в Сан-Франциско
FLIGHTS_SFO = FLIGHTS[FLIGHTS['dest'] == "SFO"]
air_times = FLIGHTS_SFO['air_time']
# строим гистограмму
plt.figure(figsize=(10, 5))
count, bins, _ = plt.hist(air_times, bins=50, density=True, alpha=0.6, color='skyblue', edgecolor='black', label='Гистограмма(нормированая)')
# найдём параметры нормального распределения
mean  = air_times.mean()
std = air_times.std()

# строим распределение Гауса
x = np.linspace(min(air_times), max(air_times), 1000)
pdf = norm.pdf(x, mean, std)
plt.plot(x, pdf, 'r-', linewidth=2, label='Нормальное распределение')

# строим доверительный интервал в 95% по правилу 2-х сигм
a = mean - 2*std
b = mean + 2*std
# добавляем на график
plt.axvline(a, color='green', linestyle='--', linewidth=2, label='95% доверительный интервал')
plt.axvline(b, color='green', linestyle='--', linewidth=2)

# выводим
plt.title('Распределение времени полета')
plt.xlabel('Время полета')
plt.ylabel('Плотность')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# таблица полётов из John F. Kennedy International Airport
FLIGHTS_JFK = FLIGHTS[FLIGHTS['origin'] == "JFK"]
# Найдём час вылета просто убрав минуты и переведя время через 24 часа
FLIGHTS_JFK['hour'] = (FLIGHTS_JFK['dep_time'].astype(int))%2400 // 100
# найдём количество вылетов в разные часы
hour_counts = FLIGHTS_JFK['hour'].value_counts()
print()
# сделаем диаграмму
plt.figure(figsize=(10, 5))
plt.bar(hour_counts.index, hour_counts.values, color='skyblue', edgecolor='black')
plt.title('Количество вылетов из John F. Kennedy International Airport')
plt.xlabel('Час вылета (0–23)')
plt.ylabel('Количество вылетов')
plt.xticks(range(0, 24))
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()


# Находим пиковые часы
morning_max = hour_counts.loc[hour_counts.index < 12].idxmax()
afternoon_max = hour_counts.loc[hour_counts.index >= 12].idxmax()
print(f'Утренний пик: {morning_max}:00')
print(f'Дневной пик: {afternoon_max}:00')

# Средняя задержка для каждого пикового часа
morning_delays = FLIGHTS_JFK[FLIGHTS_JFK['hour'] == morning_max]['dep_delay']
afternoon_delays = FLIGHTS_JFK[FLIGHTS_JFK['hour'] == afternoon_max]['dep_delay']

print(f'Средняя задержка в {morning_max}:00: {morning_delays.mean():.2f} мин')
print(f'Средняя задержка в {afternoon_max}:00: {afternoon_delays.mean():.2f} мин')

# Проверка статистической значимости (t-test) библиотеки скипи
t_stat, p_value = ttest_ind(morning_delays, afternoon_delays, equal_var=False)

print(f'p-value: {p_value:.4f}')
# проверка вероятности статистической значимости
if p_value < 0.05:
    print("Различие статистически значимо (p < 0.05)")
else:
    print("Различие НЕ статистически значимо (p ≥ 0.05)")