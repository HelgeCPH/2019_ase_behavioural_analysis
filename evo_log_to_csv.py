import os
import re
import csv
import sys
import subprocess
from pprint import pprint


LINE_RE = r"(-|\d+)+\s+(-|\d+)+\s+(.*)"
RENAME_RE = r"\{(.*) => (.*)\}"
RENAME2_RE = r"(.*) => (.*)"


def parse_numstat_block(commit_line, block):
    if block:
        for line in block:
            # '-\t-\twww/static/screenshots/tree.png'
            m = re.match(LINE_RE, line)
            added, removed, file_name = m.groups()
            if added == "-":
                added = f'"{added}"'
            if removed == "-":
                removed = f'"{removed}"'

            csv_line = ",".join((commit_line, added, removed, f'"{file_name}"'))
            yield csv_line
    else:
        csv_line = ",".join((commit_line, "", "", ""))
        yield csv_line


def create_unique_file_names_over_time(evo_csv_file):
    rows = []
    with open(evo_csv_file) as fp:
        csvreader = csv.reader(fp, delimiter=",", quotechar='"')
        for row in csvreader:
            rows.append(row)

    files = {}
    # Skip the first row as it contains the header...
    for row in reversed(rows[1:]):
        _, _, _, added, removed, fname = row
        if added != "-" and added != "":
            added = int(added)
        if removed != "-" and removed != "":
            removed = int(removed)

        if "=>" in fname:
            if "{" in fname and "}" in fname:
                start, end = fname.split(" => ")
                new_piece, tail = end.split("}")
                head, old_piece = start.split("{")
                old = head + old_piece + tail
                new = head + new_piece + tail

                if "//" in old:
                    old = old.replace("//", "/")
                if "//" in new:
                    new = new.replace("//", "/")
            else:
                old, new = fname.split(" => ")

            try:
                files[new] = files.pop(old)
                files[new]["legacy"].add(new)
                if type(added) == int:
                    files[new]["added"] += added
                if type(removed) == int:
                    files[new]["removed"] += removed
            except Exception:
                files[new] = {
                    "added": added,
                    "removed": removed,
                    "legacy": set([new]),
                }
        else:
            if fname in files.keys():
                if type(added) == int:
                    files[fname]["added"] += added
                if type(removed) == int:
                    files[fname]["removed"] += removed
                files[fname]["legacy"].add(fname)
            else:
                files[fname] = {
                    "added": added,
                    "removed": removed,
                    "legacy": set([fname]),
                }

    pprint(files)


def main(report_file):
    with open(report_file) as fp:
        lines = fp.readlines()

    commit_blocks = []
    commit_block = []
    for idx, line in enumerate(lines):
        line = line.rstrip()
        if idx + 1 < len(lines):
            next_line = lines[idx + 1].rstrip()
        else:
            next_line = ""
        if line.startswith('"') and next_line.startswith('"'):
            # Next line is a commit too and they where no changes...
            commit_block.append(line)
            commit_blocks.append(commit_block[:])
            commit_block = []
        else:
            if line:
                commit_block.append(line)
            else:
                commit_blocks.append(commit_block[:])
                commit_block = []

    out_file = f"{report_file}.csv"
    with open(out_file, "w") as fp:
        fp.write("hash,author,date,added,removed,fname\n")
        for block in commit_blocks:
            commit_line = block[0]
            for csv_line in parse_numstat_block(commit_line, block[1:]):
                fp.write(csv_line + "\n")

    # create_unique_file_names_over_time(out_file)


if __name__ == "__main__":
    main(sys.argv[1])
