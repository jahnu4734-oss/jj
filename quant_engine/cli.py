import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="India Quant Decision Engine")
    parser.add_argument("--version", action="version", version="0.1.0")
    parser.add_argument("command", nargs="?", choices=["status"], default="status")
    args = parser.parse_args()
    if args.command == "status":
        print("India Quant Decision Engine: research scaffold ready")
        print("Live trading is intentionally disabled in this phase.")


if __name__ == "__main__":
    main()
