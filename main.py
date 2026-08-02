from scraper.downloader import AMFIDownloader
from scraper.parser import AMFIParser

from scraper.sif_downloader import SIFDownloader
from scraper.sif_parser import SIFParser


def run_amfi():

    print("=" * 60)
    print("AMFI AUTOMATION PIPELINE")
    print("=" * 60)

    downloader = AMFIDownloader()

    excel_file = downloader.download_excel()

    print(f"\nAMFI Excel : {excel_file}")

    parser = AMFIParser(excel_file)

    json_file = parser.parse()

    print(f"\nAMFI JSON : {json_file}")

    print("\nAMFI Pipeline Finished Successfully")


def run_sif():

    print("\n")
    print("=" * 60)
    print("SIF AUTOMATION PIPELINE")
    print("=" * 60)

    downloader = SIFDownloader()

    excel_file = downloader.download_excel()

    print(f"\nSIF Excel : {excel_file}")

    parser = SIFParser(excel_file)

    json_file = parser.parse()

    print(f"\nSIF JSON : {json_file}")

    print("\nSIF Pipeline Finished Successfully")


def main():

    run_amfi()

    run_sif()

    print("\n")
    print("=" * 60)
    print("ALL PIPELINES COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()
