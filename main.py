from scraper.downloader import AMFIDownloader
from scraper.parser import AMFIParser


def main():

    print("=" * 60)
    print("AMFI AUTOMATION PIPELINE")
    print("=" * 60)

    # Download latest Excel
    downloader = AMFIDownloader()
    excel_file = downloader.download_excel()

    print(f"\nExcel File : {excel_file}")

    # Parse Excel and Generate JSON
    parser = AMFIParser(excel_file)

    json_file = parser.parse()

    print(f"\nJSON File : {json_file}")

    print("\nPipeline Finished Successfully")


if __name__ == "__main__":
    main()