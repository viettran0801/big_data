import requests
import json
import logging
import csv
import time


logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f"{int(time.time())}_error.txt")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

year = 2020
start_provice = 7
start_index = 1  # tiep tuc tu so bao danh

for p in range(start_provice, 65):
    with open(f"{year}_{p}_data.csv", "a", 1) as csvfile:
        writer = csv.writer(csvfile)
        s = start_index if p == start_provice else 1

        for i in range(s, 1_000_000):
            code = f"{p:02}{i:06}"
            try:
                res = requests.get(
                    f"https://diemthi.vnanet.vn/Home/SearchBySobaodanhFile?code={code}&nam={year}"
                )
                content = json.loads(res.text)
                if content["message"] == "success":
                    if len(content["result"]) > 0:
                        raw = content["result"][0]
                        writer.writerow(
                            [
                                code,
                                raw["Toan"],
                                raw["NguVan"],
                                raw["NgoaiNgu"],
                                raw["VatLi"],
                                raw["HoaHoc"],
                                raw["SinhHoc"],
                                raw["LichSu"],
                                raw["DiaLi"],
                                raw["GDCD"],
                            ]
                        )
                    else:
                        writer.writerow([code, "", "", "", "", "", "", "", "", ""])
                        logger.warning(f"{year} {code} empty")
                elif (
                    content["message"]
                    == "Số báo danh không đúng. Bạn vui lòng nhập lại."
                ):
                    logger.warning(f"{year} provice {p} end")
                    break
            except KeyboardInterrupt:
                logger.info(f"stop")
                exit(0)
            except:
                logger.error(f"{year} {code} unrecognize error")
