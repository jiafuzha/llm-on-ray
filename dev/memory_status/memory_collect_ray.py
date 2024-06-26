#
# Copyright 2023 The LLM-on-Ray Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import time


def collect_memory(eval_pid: int, name: str, output: str):
    import csv

    import matplotlib.pyplot as plt
    import psutil

    f = open(output + name + ".csv", mode="w", encoding="utf-8", newline="")

    csv_writer = csv.DictWriter(
        f,
        fieldnames=[
            "rss",
            "vms",
            "data",
        ],
    )
    csv_writer.writeheader()
    find = True
    rss = list()

    while find:
        find = False
        for p in psutil.process_iter():
            if p.pid == eval_pid and p.status() != "zombie":
                a = {
                    "rss": p.memory_info().rss,
                    "vms": p.memory_info().vms,
                    "data": p.memory_info().data,
                }
                rss.append(1.0 * p.memory_info().rss / (1024 * 1024 * 1024))
                csv_writer.writerow(a)
                find = True
                time.sleep(1)

    plt.plot(rss)
    plt.title(name)
    plt.xlabel("second")
    plt.ylabel("rss GB")
    plt.savefig(output + name + ".png")
    f.close()


if __name__ == "__main__":
    pid = 66611
    title = "rss_per_process_with_FSDP"
    output_path = "./res/"
    collect_memory(pid, title, output_path)
