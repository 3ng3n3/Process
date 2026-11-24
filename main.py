import subprocess

def adb(*args):
    return subprocess.run(
        ["adb", "shell", *args],
        capture_output=True,
        text=True
    ).stdout.strip()


def get_apps():
    output = adb("pm", "list", "packages", "-3")
    return [
        line.replace("package:", "").strip()
        for line in output.splitlines()
        if line.startswith("package:")
    ]


def stop_app(package):
    result = subprocess.run(
        ["adb", "shell", "am", "force-stop", package],
        capture_output=True,
        text=True
    )
    return result.returncode == 0


def main():
    devices = subprocess.run(
        ["adb", "devices"],
        capture_output=True,
        text=True
    ).stdout

    if "\tdevice" not in devices:
        print("[!] nenhum dispositivo ADB conectado")
        return

    apps = get_apps()

    print("\nProcessador")
    print(f"aplicativos encontrados: {len(apps)}\n")

    for i, package in enumerate(apps):
        print(f"[{i}] {package}")

    print("\ndigite os indices separados por espaco.")
    print("exemplo: 0 2 5")
    print("digite 'all' para selecionar todos")
    
    selection = input("\nSelecao: ").strip()

    if selection.lower() == "all":
        selected = apps
    else:
        try:
            indexes = set(map(int, selection.split()))
            selected = [apps[i] for i in sorted(indexes)]
        except (ValueError, IndexError):
            print("[!] Selecao invalida.")
            return

    if not selected:
        print("[!] nenhum aplicativo selecionado.")
        return

    print("\naplicativos selecionados:")
    for package in selected:
        print("-", package)

    confirm = input("\nconfirmar encerramento? (s/n): ")

    if confirm.lower() != "s":
        print("operacao cancelada")
        return

    print("\nencerrado")

    for package in selected:
        if stop_app(package):
            print(f"[OK] {package}")
        else:
            print(f"[ERRO] {package}")

    print("\nfinalizado")


if __name__ == "__main__":
    main()