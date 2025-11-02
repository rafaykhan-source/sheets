import argparse
import json
import logging
from logging.config import dictConfig

from googleapiclient.errors import HttpError

from sheet_ripper.sheets import SheetService
from sheet_ripper.writer import write_data


def get_args():
    parser = argparse.ArgumentParser(
        prog="sheet-ripper", description="Downloads a google sheet as a csv."
    )
    parser.add_argument("id", help="The id of the spreadsheet")
    parser.add_argument("range", help="The range to copy")
    return parser.parse_args()


def get_logging_config() -> dict:
    with open("logging.json") as f:
        return json.loads(f.read())


def get_logger() -> logging.Logger:
    config = get_logging_config()
    dictConfig(config)
    logger = logging.getLogger(__name__)
    return logger


def main() -> None:
    logger = get_logger()
    logger.debug("Loaded logging configuration.")
    args = get_args()
    logger.info("Retrieved arguments: id %s | range: %s", args.id, args.range)

    sheet = SheetService().build_sheets()
    logger.info("Built Sheet Service.")
    try:
        result = sheet.values().get(spreadsheetId=args.id, range=args.range).execute()
        data = result.get("values", [])

        if not data:
            logger.error("Failed to retrieve data.")
            return

        logger.info("Retrieved data: %s", data[0])

    except HttpError as err:
        print(err)

    write_data("results.csv", data)
    logger.info("Wrote results.")


if __name__ == "__main__":
    main()
