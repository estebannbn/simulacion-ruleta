import random
import argparse
import matplotlib.pyplot as plt
import numpy as np

# También podriamos evaluar según paridad, exceptuando el 0

RED_NUMBERS = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36,
}

BLACK_NUMBERS = {
    2, 4, 6, 8, 10, 11, 13, 15, 17,
    20, 22, 24, 26, 28, 29, 31, 33, 35,
}


def get_roulette_number():
    # Devuelve un número aleatorio de una ruleta europea (0-36).
    return random.randint(0, 36)


def get_roulette_color(number):
    # Devuelve el color asociado al número de la ruleta.
    if number == 0:
        return "verde"
    if number in RED_NUMBERS:
        return "rojo"
    if number in BLACK_NUMBERS:
        return "negro"
    return "desconocido"


def simulate_spins(spin_count, chosen_number):
    # Simula varias tiradas de ruleta y devuelve los resultados con el resumen por color.
    results = []
    color_counts = {"rojo": 0, "negro": 0, "verde": 0}
    chosen_count = 0
    chosen_frequency = []
    numbers = []
    average_numbers = []
    std_numbers = []
    var_numbers = []

    for index in range(1, spin_count + 1):
        number = get_roulette_number()
        color = get_roulette_color(number)
        results.append((number, color))
        numbers.append(number)
        if color in color_counts:
            color_counts[color] += 1
        if number == chosen_number:
            chosen_count += 1
        chosen_frequency.append(chosen_count / index)
        average_numbers.append(np.mean(numbers))
        std_numbers.append(np.std(numbers))
        var_numbers.append(np.var(numbers))

    return results, color_counts, chosen_count, chosen_frequency, average_numbers, std_numbers, var_numbers


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Simulación de ruleta europea usando argumentos de línea de comandos."
    )
    parser.add_argument(
        "tiradas",
        type=int,
        help="Cantidad de tiradas a simular (entero positivo).",
    )
    parser.add_argument(
        "turns_count",
        type=int,
        help="Cantidad de veces que vamos a repetir el experimento (entero positivo).",
    )
    parser.add_argument(
        "numero",
        type=int,
        help="Número elegido para apostar (0-36).",
    )
    args = parser.parse_args()

    if args.tiradas <= 0:
        parser.error("La cantidad de tiradas debe ser un entero positivo.")
    if args.turns_count <= 0 or args.turns_count > 7:
        parser.error("La cantidad de turns_count debe ser un entero positivo y no mayor a 7.")
    if not 0 <= args.numero <= 36:
        parser.error("El número elegido debe estar entre 0 y 36.")

    return args.tiradas, args.turns_count, args.numero


def print_simulation_results(results, color_counts, chosen_number, chosen_count):
    # Imprime el resultado de cada tirada y un resumen por color.
    print("\nResultados de la simulación:")
    for index, (number, color) in enumerate(results, start=1):
        print(f"Tirada {index}: {number} ({color})")

    print("\nResumen por color:")
    for color, count in color_counts.items():
        print(f"  {color.capitalize()}: {count}")

    print(f"\nNúmero elegido: {chosen_number}")
    print(f"Veces que salió el número elegido: {chosen_count}")


def plot_multiple_runs_frequency(spin_count, chosen_number, all_frequencies):
    expected_probability = 1 / 37
    x_values = list(range(1, spin_count + 1))

    plt.figure(figsize=(12, 8))
    colors = plt.cm.viridis(np.linspace(0, 1, len(all_frequencies)))
    for i, freq in enumerate(all_frequencies):
        plt.plot(x_values, freq, label=f"Corrida {i+1}", color=colors[i])
    plt.hlines(expected_probability, 1, spin_count, colors="red", linestyles="dashed", label=f"Frecuencia esperada (1/37 ≈ {expected_probability:.4f})")
    plt.title("Frecuencia relativa del número elegido en múltiples corridas")
    plt.xlabel("Número de tiradas")
    plt.ylabel("Frecuencia relativa")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_multiple_averages(spin_count, all_averages):
    expected_average = 18  # Promedio teórico: (0+36)/2 = 18
    x_values = list(range(1, spin_count + 1))

    plt.figure(figsize=(12, 8))
    colors = plt.cm.viridis(np.linspace(0, 1, len(all_averages)))
    for i, avg in enumerate(all_averages):
        plt.plot(x_values, avg, label=f"Corrida {i+1}", color=colors[i])
    plt.hlines(expected_average, 1, spin_count, colors="red", linestyles="dashed", label=f"Promedio esperado (18)")
    plt.title("Valor promedio obtenido en la ruleta en múltiples corridas")
    plt.xlabel("Número de tiradas")
    plt.ylabel("Promedio acumulado")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_multiple_stds(spin_count, all_stds):
    x_values = list(range(1, spin_count + 1))

    # Desvío estándar teórico (discreto 0..36): Var = 114 -> std = sqrt(114)
    expected_variance = (37**2 - 1) / 12
    expected_std = np.sqrt(expected_variance)

    plt.figure(figsize=(12, 8))
    colors = plt.cm.viridis(np.linspace(0, 1, len(all_stds)))
    for i, std in enumerate(all_stds):
        plt.plot(x_values, std, label=f"Corrida {i+1}", color=colors[i])

    # Línea horizontal que marca el desvío estándar esperado
    plt.hlines(expected_std, 1, spin_count, colors="red", linestyles="dashed",
               label=f"Desvío estándar esperado ({expected_std:.3f})")

    plt.title("Desvío estándar acumulado en múltiples corridas")
    plt.xlabel("Número de tiradas")
    plt.ylabel("Desvío estándar")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_multiple_vars(spin_count, all_vars):
    x_values = list(range(1, spin_count + 1))

    # Varianza esperada para distribución uniforme discreta 0..36:
    # Var = ((b-a+1)^2 - 1) / 12 = (37^2 - 1) / 12 = 114
    expected_variance = (37**2 - 1) / 12

    plt.figure(figsize=(12, 8))
    colors = plt.cm.viridis(np.linspace(0, 1, len(all_vars)))
    for i, var in enumerate(all_vars):
        plt.plot(x_values, var, label=f"Corrida {i+1}", color=colors[i])

    # Línea horizontal que marca la varianza esperada
    plt.hlines(expected_variance, 1, spin_count, colors="red", linestyles="dashed",
               label=f"Varianza esperada ({expected_variance:.2f})")

    plt.title("Varianza acumulada en múltiples corridas")
    plt.xlabel("Número de tiradas")
    plt.ylabel("Varianza")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_histogram_per_run(spin_count, all_runs):
    """
    Dibuja un histograma por corrida con la cantidad de veces que salió cada número (0-36).
    Si hay más de una corrida, las barras se dibujan en la misma posición y con transparencia
    para poder comparar cómo se acercan al valor esperado.
    all_runs: lista de corridas. Cada corrida puede ser:
      - lista de tuplas (number, color) como devuelve simulate_spins, o
      - lista de números (0-36).
    """
    # Construir matriz de conteos (n_corridas x 37)
    counts_list = []
    for run in all_runs:
        if len(run) == 0:
            counts_list.append(np.zeros(37, dtype=int))
            continue
        first = run[0]
        if isinstance(first, tuple):
            numbers = [n for n, _ in run]
        else:
            numbers = list(run)
        hist = np.zeros(37, dtype=int)
        for n in numbers:
            if 0 <= n <= 36:
                hist[n] += 1
        counts_list.append(hist)

    if len(counts_list) == 0:
        print("No hay corridas para graficar.")
        return

    counts = np.array(counts_list)  # shape (runs, 37)
    runs = counts.shape[0]
    x = np.arange(37)
    width = 0.8

    plt.figure(figsize=(14, 6))
    colors = plt.cm.tab10(np.linspace(0, 1, max(1, runs)))
    for i in range(runs):
        plt.bar(x, counts[i], width=width, color=colors[i % len(colors)],
                alpha=0.45, label=f"Corrida {i+1}", edgecolor="black", linewidth=0.4)

    # Línea con el valor esperado por número
    expected_per_number = spin_count / 37
    plt.hlines(expected_per_number, -0.5, 36.5, colors="red", linestyles="dashed",
               label=f"Esperado por número ({expected_per_number:.2f})")

    plt.xticks(x)
    plt.xlabel("Número de la ruleta")
    plt.ylabel("Veces que salió")
    plt.title("Frecuencia de cada número por corrida (0-36) — barras superpuestas")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()

def main():
    print("Simulación de ruleta europea")
    print("Números válidos: 0 a 36. El 0 es verde, los demás son rojo o negro.")

    spin_count, turns_count, chosen_number = parse_arguments()

    all_frequencies = []
    all_averages = []
    all_stds = []
    all_vars = []
    all_runs = []
    for turn in range(turns_count):
        results, color_counts, chosen_count, chosen_frequency, average_numbers, std_numbers, var_numbers = simulate_spins(spin_count, chosen_number)
        all_frequencies.append(chosen_frequency)
        all_averages.append(average_numbers)
        all_stds.append(std_numbers)
        all_vars.append(var_numbers)
        all_runs.append(results)  # Guardar la corrida completa (lista de tuplas (número, color))

    # Mostrar resultados de la última corrida
    print_simulation_results(results, color_counts, chosen_number, chosen_count)

    # Graficar
    plot_multiple_runs_frequency(spin_count, chosen_number, all_frequencies)
    plot_multiple_averages(spin_count, all_averages)
    plot_multiple_stds(spin_count, all_stds)
    plot_multiple_vars(spin_count, all_vars)
    plot_histogram_per_run(spin_count, all_runs)


if __name__ == "__main__":
    main()