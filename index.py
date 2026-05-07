import random

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


def simulate_spins(spin_count):
    # Simula varias tiradas de ruleta y devuelve los resultados con el resumen por color.
    results = []
    color_counts = {"rojo": 0, "negro": 0, "verde": 0}

    for _ in range(spin_count):
        number = get_roulette_number()
        color = get_roulette_color(number)
        results.append((number, color))
        if color in color_counts:
            color_counts[color] += 1

    return results, color_counts


def request_spin_count():
    # Solicita al usuario la cantidad de tiradas a simular y valida la entrada.
    while True:
        raw_value = input("¿Cuántas tiradas deseas simular? ").strip()
        if not raw_value:
            print("Por favor, ingresa un número entero positivo.")
            continue

        if not raw_value.isdigit():
            print("Entrada no válida. Usa solo dígitos.")
            continue

        spin_count = int(raw_value)
        if spin_count <= 0:
            print("El número debe ser mayor que cero.")
            continue

        return spin_count


def print_simulation_results(results, color_counts):
    # Imprime el resultado de cada tirada y un resumen por color.
    print("\nResultados de la simulación:")
    for index, (number, color) in enumerate(results, start=1):
        print(f"Tirada {index}: {number} ({color})")

    print("\nResumen por color:")
    for color, count in color_counts.items():
        print(f"  {color.capitalize()}: {count}")


def main():
    print("Simulación de ruleta europea")
    print("Números válidos: 0 a 36. El 0 es verde, los demás son rojo o negro.")

    spin_count = request_spin_count()
    results, color_counts = simulate_spins(spin_count)
    print_simulation_results(results, color_counts)


if __name__ == "__main__":
    main()
