import requests
import json
import logging


def fetchData(code, year, logger):
    res = requests.get(
        f"https://diemthi.vnanet.vn/Home/SearchBySobaodanhFile?code={code}&nam={year}"
    )
    content = json.loads(res.text)
    try:
        if content["message"] == "success":
            if len(content["result"]) > 0:
                logger.info(
                    f'{content["message"]} {content["result"][0]["Code"]} {content["result"][0]["Toan"]}'
                )
            else:
                logger.info(f'{content["message"]} EMPTY')
        else:
            logger.error(f"ERROR {code} {content}")
    except:
        logger.error(f"ERROR {code} {content}")


def main():
    logger = logging.getLogger("crawler")
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler("logs.txt")
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    for i in range(1, 10000):
        fetchData(f"0101{i:04}", 2019, logger)


if __name__ == "__main__":
    main()
