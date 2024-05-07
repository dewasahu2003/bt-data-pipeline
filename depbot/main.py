import argparse as ap


def main():
    parser = ap.ArgumentParser(description="Scraper Cli")

    parser.add_argument(
        "-c",
        "--codes",
        nargs="+",
        required=True,
        help="Codes to scrape",
    )

    args = parser.parse_args()
    if args.codes:
        print("happy to see you buddy")


if __name__ == "__main__":
    main()
