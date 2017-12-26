import json
import sys

raw_data = "./data/news/signalmedia-1m.jsonl"
to_input_data = "./data/news/input.txt"

with open(raw_data, "r") as f:
    txt_file = open(to_input_data, "w")
    cnt = 0
    for line in f:
        cnt += 1
        json_data = json.loads(line)
        content = json_data['content']
        txt_file.write(content.encode("utf-8"))

        if cnt % 100 == 0:
            sys.stdout.write("\r process: {} / 1 M".format(cnt))
            sys.stdout.flush()

        if cnt > 50000:
            break
    txt_file.close()

