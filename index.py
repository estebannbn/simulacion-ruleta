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
    if args.turns_count <= 0:
        parser.error("La cantidad de turns_count debe ser un entero positivo.")
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

    plt.figure(figsize=(12, 8))
    colors = plt.cm.viridis(np.linspace(0, 1, len(all_stds)))
    for i, std in enumerate(all_stds):
        plt.plot(x_values, std, label=f"Corrida {i+1}", color=colors[i])
    plt.title("Desvío estándar acumulado en múltiples corridas")
    plt.xlabel("Número de tiradas")
    plt.ylabel("Desvío estándar")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_multiple_vars(spin_count, all_vars):
    x_values = list(range(1, spin_count + 1))

    plt.figure(figsize=(12, 8))
    colors = plt.cm.viridis(np.linspace(0, 1, len(all_vars)))
    for i, var in enumerate(all_vars):
        plt.plot(x_values, var, label=f"Corrida {i+1}", color=colors[i])
    plt.title("Varianza acumulada en múltiples corridas")
    plt.xlabel("Número de tiradas")
    plt.ylabel("Varianza")
    plt.legend()
    plt.grid(True)
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
    for turn in range(turns_count):
        results, color_counts, chosen_count, chosen_frequency, average_numbers, std_numbers, var_numbers = simulate_spins(spin_count, chosen_number)
        all_frequencies.append(chosen_frequency)
        all_averages.append(average_numbers)
        all_stds.append(std_numbers)
        all_vars.append(var_numbers)

    # Mostrar resultados de la última corrida
    print_simulation_results(results, color_counts, chosen_number, chosen_count)

    # Graficar
    plot_multiple_runs_frequency(spin_count, chosen_number, all_frequencies)
    plot_multiple_averages(spin_count, all_averages)
    plot_multiple_stds(spin_count, all_stds)
    plot_multiple_vars(spin_count, all_vars)


if __name__ == "__main__":
    main()
