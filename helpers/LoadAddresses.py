#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import json


if __name__ == '__main__':
  with open('addresses.jsonl') as f:
    data = json.load(f)

  # Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
  print(data)
