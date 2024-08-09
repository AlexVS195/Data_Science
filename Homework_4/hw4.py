# -*- coding: utf-8 -*-
"""Hw4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cCotI551UAlIhJLt8W1FOeazduRBK4CO

# Лінійна регресія: перенавчання і регуляризація

У цьому завданні ми на прикладах побачимо, як перенавчаються лінійні моделі, розберемо, чому так відбувається, і з'ясуємо, як діагностувати та контролювати перенавчання.

В усіх комірках, де вказаний коментар з інструкціями, потрібно написати код, який виконує ці інструкції. Решту комірок із кодом (без коментарів) треба просто виконати. Крім того, у завданні необхідно відповідати на запитання; відповіді потрібно вписувати після виділеного слова "__Відповідь:__".
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
# %matplotlib inline

"""Ми будемо працювати з датасетом __"bikes_rent.csv"__, у якому по днях записані календарна інформація та погодні умови, що характеризують автоматизовані пункти прокату велосипедів, а також кількість прокатів у цей день. Останнє ми будемо передбачати; таким чином, ми будемо розв'язувати завдання регресії.

### Ознайомлення з даними

## Завдання 1

Завантажте датасет за допомогою функції __pandas.read_csv__ у змінну __df__. Виведіть перші 5 рядків, щоб переконатися в коректному зчитуванні даних:
"""

url = 'https://drive.google.com/file/d/1-4wgz9AFXrD3tZfqHJLMhCmy4BUzAX96/view'
download_url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]

df = pd.read_csv(download_url)
print(df.head())

"""Для кожного дня прокату відомі такі ознаки:
* _season_: 1 — весна, 2 — літо, 3 — осінь, 4 — зима
* _yr_: 0 — 2011, 1 — 2012
* _mnth_: від 1 до 12
* _holiday_: 0 — немає свята, 1 — є свято
* _weekday_: від 0 до 6
* _workingday_: 0 — неробочий день, 1 — робочий день
* _weathersit_: оцінка сприятливості погоди від 1 (чистий, ясний день) до 4 (злива, туман)
* _temp_: температура в Цельсіях
* _atemp_: температура за відчуттями в Цельсіях
* _hum_: вологість
* _windspeed(mph)_: швидкість вітру в милях за годину
* _windspeed(ms)_: швидкість вітру в метрах за секунду
* _cnt_: кількість орендованих велосипедів (це цільова ознака, її ми будемо передбачати)

Отже, у нас є речові, бінарні та номінальні (порядкові) ознаки, і з усіма з них можна працювати як з речовими. З номінальними ознаками теж можна працювати як з речовими, тому що на них заданий порядок. Давайте подивимося на графіках, як цільова ознака залежить від решти.

Побудуйте графіки залежностей атрибутів від кількості поїздок. Іншими словами, вам потрібно побудувати 12 графіків. На кожному має бути зображена залежність чергового атрибута від змінної **cnt**.
"""

attributes = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed(mph)', 'windspeed(ms)']

fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(15, 10))
fig.tight_layout(pad=3.0)

for i, attr in enumerate(attributes):
    row = i // 3
    col = i % 3
    axes[row, col].scatter(df[attr], df['cnt'], alpha=0.5)
    axes[row, col].set_xlabel(attr)
    axes[row, col].set_ylabel('cnt')
    axes[row, col].set_title(f'Залежність cnt від {attr}')

plt.show()

"""__Запитання:__
1. Яким є характер залежності кількості прокатів від місяця? На графіку "cnt vs mnth" видно, що кількість прокатів має сезонний характер. Прокатів більше в літні місяці (червень, липень, серпень) і менше в зимові місяці (грудень, січень, лютий). Це може бути пов'язано з погодними умовами та тривалістю дня, які сприяють більшій кількості прокатів влітку.
1. Вкажіть одну або дві ознаки, від яких кількість прокатів скоріше за все залежить лінійно. Ознаки, від яких кількість прокатів скоріше за все залежить лінійно, це температура (temp або atemp). На графіку "cnt vs temp" видно, що кількість прокатів збільшується з підвищенням температури. Це вказує на лінійну залежність між температурою та кількістю прокатів. На графіку "cnt vs atemp" також видно лінійну залежність між температурою за відчуттями та кількістю прокатів. Зі збільшенням температури за відчуттями кількість прокатів зростає.

## Завдання 2

Давайте більш строго оцінимо рівень лінійної залежності між ознаками та цільовою змінною. Гарною мірою лінійної залежності між двома векторами є кореляція Пірсона. Нам уже доводилося мати з нею справу раніше. Для її обчислення в pandas можна використовувати методи датафрейму: corr і corrwith.

Порахуйте кореляції всіх ознак, окрім останньої, з останньою за допомогою методу `corrwith`.
"""

features = ['temp', 'atemp', 'hum', 'windspeed(mph)', 'windspeed(ms)', 'cnt']
correlations = df.drop(columns=['cnt']).corrwith(df['cnt'])
print(correlations)

"""У вибірці є ознаки, що корелюють із цільовою, а отже, завдання можна розв'язувати лінійними методами.

За графіками видно, що деякі ознаки схожі між собою. Тому давайте також порахуємо кореляції між речовими ознаками.

## Завдання 3

Порахуйте попарні кореляції між ознаками temp, atemp, hum, windspeed(mph), windspeed(ms) і cnt
за допомогою методу corr:
"""

features = ['temp', 'atemp', 'hum', 'windspeed(mph)', 'windspeed(ms)', 'cnt']
correlations = df[features].corr()
print(correlations)

"""На діагоналях, як і належить, стоять одиниці. Однак у матриці є ще дві пари сильно корелюючих стовпців: temp і atemp (корелюють за своєю природою) і два windspeed (тому що це просто переведення одних одиниць в інші). Далі ми побачимо, що цей факт негативно позначається на навчанні лінійної моделі.

Насамкінець подивимося середні ознак (метод mean), щоб оцінити масштаб ознак і частки 1 у бінарних ознак.

## Завдання 4

Виведіть середні ознак.
"""

features = ['temp', 'atemp', 'hum', 'windspeed(mph)', 'windspeed(ms)', 'cnt']
mean_values = df[features].mean()
print(mean_values)

"""Ознаки мають різний масштаб, отже, для подальшої роботи нам краще нормувати матрицю об'єкти-ознаки.

### Проблема перша: колінеарні ознаки

Отже, у наших даних одна ознака дублює іншу, і є ще дві дуже схожі. Звичайно, ми могли б одразу видалити дублікати, але давайте подивимося, як відбувалося б навчання моделі, якби ми не помітили цю проблему.

Для початку проведемо масштабування, або стандартизацію ознак: з кожної ознаки віднімемо її середнє і поділимо на стандартне відхилення. Це можна зробити за допомогою методу scale.

Крім того, необхідно перемішати вибірку, це буде потрібно для крос-валідації.
"""

from sklearn.preprocessing import scale
from sklearn.utils import shuffle

df_shuffled = shuffle(df, random_state=42)
X = scale(df_shuffled[df_shuffled.columns[:-1]])
y = df_shuffled["cnt"]

"""Давайте навчимо лінійну регресію на наших даних і подивимося на ваги ознак."""

from sklearn.linear_model import LinearRegression

"""## Завдання 5

Створіть об'єкт лінійного регресора, навчіть його на всіх даних і виведіть ваги моделі (ваги зберігаються у змінній `coef_` класу регресора). Можна виводити пари (назва ознаки, вага), скориставшись функцією `zip`, вбудованою в мову python. Назви ознак зберігаються у змінній `df.columns`.

"""

from sklearn.linear_model import LinearRegression

reg = LinearRegression().fit(X, y)
[i for i in list(zip(df.columns, reg.coef_))]

"""Ми бачимо, що ваги при лінійно-залежних ознаках за модулем значно більші, ніж при інших ознаках. Щоб зрозуміти, чому так сталося, згадаємо аналітичну формулу, за якою обчислюються ваги лінійної моделі в методі найменших квадратів:

$$w = (X^TX)^{-1} X^T y$$

Якщо в $X$ є колінеарні (лінійно-залежні) стовпці, матриця $X^TX$ стає виродженою, і формула перестає бути коректною. Чим більш залежні ознаки, тим менший визначник цієї матриці й тим гірша апроксимація $Xw \approx y$. Таку ситуацію називають _проблемою мультиколінеарності_.

З парою (temp, atemp) трохи менше корелюючих змінних такого не сталося, однак на практиці завжди варто уважно стежити за коефіцієнтами при схожих ознаках.

Для того щоб розв'язати проблему мультиколінеарності, потрібно скористатися регуляризатором. До оптимізуючого функціоналу додають $L_1$ або $L_2$ норму ваг, помножену на коефіцієнт регуляризації $\alpha$. У першому випадку метод називається Lasso, а у другому — Ridge.

### Завдання 6
Давайте спробуємо навчити лінійні моделі з $L_1$ і $L_2$-регуляризацією, а далі порівняємо їхні ваги. Навчіть регресори Ridge і Lasso з параметрами за замовчуванням і переконайтеся, що проблема з вагами вирішилась.

Навчіть лінійну модель з $L_1$-регуляризацією (клас Lasso) і виведіть ваги.
"""

from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler

lasso = Lasso().fit(X, y)
[i for i in list(zip(df.columns, lasso.coef_))]

"""Навчіть лінійну модель з $L_2$-регуляризацією (клас Ridge) і виведіть ваги."""

ridge = Ridge().fit(X, y)
[i for i in list(zip(df.columns, ridge.coef_))]

"""### Завдання 7

На відміну від $L_2$-регуляризації, $L_1$ обнуляє ваги при деяких ознаках. Давайте поспостерігаємо, як змінюються ваги зі збільшенням коефіцієнта регуляризації $\alpha$.

Для кожного значення коефіцієнта з `alphas` навчіть регресор `Lasso` і запишіть ваги у список `coefs_lasso`, а потім навчіть `Ridge` і запишіть ваги у список`coefs_ridge`. Конвертуйте отримані списки в `np.array`.
"""

alphas = np.arange(1, 500, 50)

coefs_lasso = []
coefs_ridge = []

for alpha in alphas:
    lasso_model = Lasso(alpha=alpha)
    lasso_model.fit(X_scaled, y)
    coefs_lasso.append(lasso_model.coef_)

    ridge_model = Ridge(alpha=alpha)
    ridge_model.fit(X_scaled, y)
    coefs_ridge.append(ridge_model.coef_)

coefs_lasso = np.array(coefs_lasso)
coefs_ridge = np.array(coefs_ridge)

print("Lasso Coefficients:\n", coefs_lasso)
print("Ridge Coefficients:\n", coefs_ridge)

"""Проаналізуйте динаміку ваг при збільшенні параметра регуляризації:"""

plt.figure(figsize=(8, 5))

for coef, feature in zip(coefs_lasso.T, df.columns):
    plt.plot(alphas, coef, label=feature, color=np.random.rand(3))

plt.legend(loc="upper right", bbox_to_anchor=(1.4, 0.95))
plt.xlabel("alpha")
plt.ylabel("feature weight")
plt.title("Lasso")

plt.figure(figsize=(8, 5))
for coef, feature in zip(coefs_ridge.T, df.columns):
    plt.plot(alphas, coef, label=feature, color=np.random.rand(3))

plt.legend(loc="upper right", bbox_to_anchor=(1.4, 0.95))
plt.xlabel("alpha")
plt.ylabel("feature weight")
plt.title("Ridge")

plt.show()

"""Проаналізуйте графіки та дайте відповіді на такі запитання.

1. Який регуляризатор (Ridge або Lasso) агресивніше зменшує ваги при одному й тому самому alpha? Lasso агресивніше зменшує ваги, ніж Ridge
1. Що станеться з вагами Lasso, якщо alpha зробити дуже великим? Поясніть, чому так відбувається. Якщо alpha у Lasso зробити дуже великим, більшість ваг будуть зменшені до нуля. Це відбувається тому, що Lasso штрафує великі ваги більше, ніж малі, і при дуже великому alpha штраф за великі ваги стає настільки високим, що оптимальним рішенням стає зменшення всіх ваг до нуля.
1. Чи можна стверджувати, що `Lasso` виключає одну з ознак `windspeed` при будь-якому значенні `alpha > 0`? А Ridge? Вважається, що регуляризатор виключає ознаку, якщо коефіцієнт при ньому менший $10^{-3}$.Lasso може виключити ознаку windspeed при достатньо великому alpha, оскільки Lasso зменшує ваги до нуля. Тому, якщо alpha достатньо велике, коефіцієнт при windspeed може стати меншим за 10−3 і ознака буде вважатися виключеною. Ridge, навпаки, не виключає ознаки, а лише зменшує їх ваги. Тому навіть при великому alpha, Ridge не зможе зменшити коефіцієнт при windspeed до нуля, а лише до дуже малого значення.
1. Який із регуляризаторів підійде для відбору неінформативних ознак? Lasso підходить, оскільки він може зменшувати ваги до нуля, виключаючи таким чином неінформативні ознаки. Ridge, навпаки, лише зменшує ваги, але не виключає ознаки повністю.

### Завдання 8

Далі будемо працювати з `Lasso`.

Отже, ми бачимо, що при зміні alpha модель по-різному підбирає коефіцієнти ознак. Нам потрібно вибрати найкраще alpha.

Для цього, по-перше, нам потрібна метрика якості. Будемо використовувати як метрику сам оптимізований функціонал методу найменших квадратів, тобто `Mean Square Error`.

По-друге, потрібно зрозуміти, на яких даних цю метрику рахувати. Не можна вибирати `alpha` за значенням MSE на навчальній вибірці, тому що тоді ми не зможемо оцінити, як модель буде робити передбачення на нових для неї даних. Якщо ми виберемо одне розбиття вибірки на навчальну та тестову (це називається holdout), то налаштуємося на конкретні "нові" дані, і знову можемо перенавчитися. Тому будемо робити декілька розбиттів вибірки, на кожному пробувати різні значення alpha, а потім усереднювати MSE. Найзручніше робити такі розбиття крос-валідацією, тобто розділити вибірку на $K$ частин, і кожного разу брати одну з них як тестову, а з блоків, що залишилися, складати навчальну вибірку.

Робити крос-валідацію для регресії в sklearn зовсім просто: для цього є спеціальний регресор, __LassoCV__, який бере на вхід список із alpha і для кожного з них обчислює MSE на крос-валідації. Після навчання (якщо залишити параметр cv=3 за замовчуванням) регресор буде містити змінну __mse\_path\___, матрицю розміру len(alpha) x k, k = 3 (число блоків у крос-валідації), що містить значення MSE на тесті для відповідних запусків. Крім того, у змінній alpha\_ буде зберігатися вибране значення параметра регуляризації, а в coef\_, традиційно, навчені ваги, що відповідають цьому alpha_.

Зверніть увагу, що регресор може змінювати порядок, у якому він проходить по alphas; для зіставлення з матрицею MSE краще використовувати змінну регресора alphas_.

Навчіть регресор `LassoCV` на всіх параметрах регуляризації з alpha. Побудуйте графік _усередненого_ за рядками `MSE` в залежності від `alpha` (використовуйте для цього функцію `create_plot`).

Виведіть вибране `alpha`, а також пари "ознака-коефіцієнт" для навченого вектора коефіцієнтів.
"""

def create_plot(data, title, xlabel, ylabel, figsize=None):
    size = figsize or (15, 5)
    plt.figure(figsize=size)

    x = list(map(lambda e: e[0], data))
    y = list(map(lambda e: e[1], data))
    plt.plot(x, y)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.grid()
    plt.show()

from sklearn.linear_model import LassoCV

SEED = 42
alphas = np.arange(1, 100, 5)
regressor = LassoCV(random_state=SEED, alphas=alphas, cv=3)
regressor.fit(X, y)

print(f"Shape of regressor.coef_: {regressor.coef_.shape}")
print(f"Shape of regressor.alphas: {regressor.alphas_.shape}")
print(f"Shape of regressor.mse_path_: {regressor.mse_path_.shape}")
print(f"Alphas used: {regressor.alphas_}")

mse_values = np.mean(regressor.mse_path_, axis=1)
data = np.vstack((regressor.alphas_, mse_values))

create_plot(data.T, "Mean Squared Error vs Alpha", "Alpha", "MSE")

print("Вибране значення alpha:", regressor.alpha_)
print("Коефіцієнти ознак:")
feature_names = df_shuffled.columns[:-1]
for feature, coef in zip(feature_names, regressor.coef_):
    print(f"{feature}: {coef}")

"""Отже, ми вибрали певний параметр регуляризації. Давайте подивимося, які б ми вибирали alpha, якби ділили вибірку лише один раз на навчальну та тестову, тобто розглянемо траєкторії MSE, що відповідають окремим блокам вибірки.

### Завдання 9

Виведіть значення `alpha`, що відповідають мінімумам `MSE` на кожному розбитті (тобто за стовпцями).
На трьох окремих графіках візуалізуйте стовпці `mse_path_`.
"""

min_mse_indices = np.argmin(regressor.mse_path_, axis=0)
min_alphas = regressor.alphas_[min_mse_indices]
min_mses = np.min(regressor.mse_path_, axis=0)

print("Значення alpha та MSE, що відповідають мінімумам MSE на кожному розбитті:")
for i, (alpha, mse) in enumerate(zip(min_alphas, min_mses)):
    print(f"Розбиття {i+1}: Alpha = {alpha}, MSE = {mse:.6f}")

# Візуалізація стовпців mse_path_ на трьох окремих графіках
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

for i in range(regressor.mse_path_.shape[1]):
    axes[i].plot(regressor.alphas_, regressor.mse_path_[:, i], marker='o')
    axes[i].set_xscale('log')
    axes[i].set_xlabel('alpha')
    axes[i].set_ylabel('MSE')
    axes[i].set_title(f'Розбиття {i+1}')
    axes[i].grid(True)

plt.tight_layout()
plt.show()

"""На кожному розбитті оптимальне значення `alpha` своє, і йому відповідає велике MSE на інших розбиттях. Виходить, що ми налаштовуємося на конкретні навчальні та контрольні вибірки. При виборі `alpha` на крос-валідації ми вибираємо дещо "середнє", що даватиме прийнятне значення метрики на різних розбиттях вибірки.

### Завдання 10

Нарешті, як прийнято в аналізі даних, давайте проінтерпретуємо результат. Дайте відповіді на наступні запитання.

#### Запитання 1

В останній навченій моделі виберіть 4 ознаки з найбільшими (позитивними) коефіцієнтами (і випишіть їх), подивіться на візуалізації залежностей `cnt` від цих ознак, які ми зображали у блоці "Ознайомлення з даними". Чи видно зростаючу лінійну залежність `cnt` від цих ознак за графіками? Чи логічно стверджувати (виходячи зі здорового глузду), що чим більше значення цих ознак, тим більше людей захочуть взяти велосипеди?

__Відповідь:__
"""

Ознаки з найбільшими позитивними коефіцієнтами є season, weekday, atemp, workingday.
На графіках залежностей cnt від цих ознак ми можемо побачити, що збільшення значень цих ознак, як правило, супроводжується збільшенням значень cnt.
Це може свідчити про те, що існує зростаюча лінійна залежність між цими ознаками та кількістю орендованих велосипедів.
Виходячи зі здорового глузду, можна стверджувати, що чим більше значення цих ознак, тим більше людей захочуть взяти велосипеди. Наприклад:

atemp (відчуваєма температура) — чим тепліше, тим більше людей можуть захотіти взяти велосипеди.

workingday (робочий день) — у робочі дні більше людей можуть використовувати велосипеди для щоденних пересувань.

season (сезон) — у певний сезон (наприклад, літо) більше людей можуть захотіти взяти велосипеди.

Отже, виходячи з аналізу та візуалізації, можна зробити висновок, що існує зростаюча лінійна залежність між вибраними ознаками та кількістю
орендованих велосипедів, і це є логічним з точки зору здорового глузду.

"""#### Запитання 2

Виберіть 3 ознаки з найбільшими за модулем негативними коефіцієнтами (і випишіть їх), подивіться на відповідні візуалізації. Чи видно лінійну залежність, що зменшується? Чи логічно стверджувати, що чим більша величина цих ознак, тим менше людей захочуть взяти велосипеди?

__Відповідь:__
"""

ознаки з найбільшими за модулем негативними коефіцієнтами є holiday, weathersit, і windspeed(mph).
На графіках залежностей cnt від цих ознак ми можемо побачити, що збільшення значень цих ознак, як правило,
супроводжується зменшенням значень cnt. Це може свідчити про те, що існує лінійна залежність, що зменшується,
між цими ознаками та кількістю орендованих велосипедів.
Можна стверджувати, що чим більше значення цих ознак, тим менше людей захочуть взяти велосипеди. Наприклад:

holiday (свято) — у дні свят більше людей можуть залишатися вдома або використовувати інші види транспорту, тому кількість орендованих велосипедів може зменшитися.

weathersit (оцінка сприятливості погоди) — чим гірша погода (наприклад, злива або туман), тим менше людей захочуть взяти велосипеди.

windspeed(mph) (швидкість вітру в милях за годину) — чим сильніший вітер, тим менше людей захочуть взяти велосипеди через незручності або небезпеку.

Отже, виходячи з аналізу та візуалізації, можна зробити висновок, що існує лінійна залежність, що зменшується, між вибраними ознаками та
кількістю орендованих велосипедів, і це є логічним з точки зору здорового глузду.

"""#### Запитання 3

Випишіть ознаки з коефіцієнтами, близькими до нуля (< 1e-3). Як ви думаєте, чому модель виключила їх із моделі (знову подивіться на графіки)? Чи правда, що вони ніяк не впливають на попит на велосипеди?

__Відповідь:__
"""

Ознаки з коефіцієнтами, близькими до нуля (< 1e-3), є mnth, hum, і windspeed(ms).
mnth (місяць): Коефіцієнт для місяця є негативним, але відносно низьким. Це може свідчити про те, що місяць має
обмежений вплив на попит на велосипеди, оскільки інші фактори, такі як температура та погодні умови, можуть бути більш значущими.
hum (вологість): Коефіцієнт для вологості є негативним, але відносно низьким. Це може свідчити про те, що вологість має обмежений
вплив на попит на велосипеди, оскільки інші фактори, такі як температура та погодні умови, можуть бути більш значущими.
windspeed(ms) (швидкість вітру в метрах за секунду): Коефіцієнт для швидкості вітру є негативним, але відносно низьким.
Це може свідчити про те, що швидкість вітру має обмежений вплив на попит на велосипеди, оскільки інші фактори, такі як температура та погодні умови,
можуть бути більш значущими.
Модель може виключити ознаки з коефіцієнтами, близькими до нуля, з моделі, оскільки вони мають обмежений вплив на попит на велосипеди порівняно з
іншими більш значущими факторами.
Ознаки з коефіцієнтами, близькими до нуля, мають обмежений вплив на попит на велосипеди, але не можна стверджувати, що вони ніяк не впливають на попит.

"""### Висновок
Отже, ми подивилися, як можна стежити за адекватністю лінійної моделі, як відбирати ознаки і як грамотно, за можливості не налаштовуючись на якусь конкретну порцію даних, підбирати коефіцієнт регуляризації.

Варто зазначити, що за допомогою крос-валідації зручно підбирати лише невелику кількість параметрів. (1, 2, максимум 3), тому що для кожної допустимої їх комбінації нам доводиться декілька разів навчати модель. Такий процес займає багато часу, особливо якщо треба навчатися на великих обсягах даних.
"""