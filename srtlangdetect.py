#!/usr/bin/env python3

import argparse
import os.path
import sys

import srt

from langdetect import detect_langs


def main():
    args = parse_args()

    for srt in args.srt:
        if os.path.isfile(srt):
            parse_srt(
                srt, args.summary, args.dry_run, args.quiet, args.verbose
            )
        elif os.path.isdir(srt):
            for root, dirs, files in os.walk(srt):
                for file in files:
                    if file.endswith(".srt"):
                        # parse_srt(
                        #     os.path.join(root, file),
                        #     args.summary,
                        #     args.dry_run,
                        #     args.quiet,
                        #     args.verbose,
                        # )
        else:
            print("Subtitle file/path '{0}' doesn't exist".format(args.srt))

    if len(args.srt) == 0:
        print()
        print("No subtitle files or directories specified.")


def lang_detect_srt(file, summary, dry_run, quiet, verbose):
    if dry_run or verbose or summary:
        print("Parsing '{0}'...".format(file))

    try:
        original_subtitles = None
        with open(file, "r", encoding="utf-8") as filehandler:
            original_subtitles = filehandler.read()
    except:
        print()
        print("Couldn't open file '{0}'".format(file))
        return False

    try:
        original_subtitles = list(srt.parse(original_subtitles))
    except:
        print()
        print("Trouble parsing subtitles in '{0}'".format(file))
        return False

    full_subtitle_text = ''

    for i in range(len(original_subtitles)):
        full_subtitle_text += original_subtitles[i].content

    print(detect_langs(full_subtitle_text))

    # if not dry_run:
    #     new_subtitle_file = list(srt.sort_and_reindex(new_subtitle_file))
    #     if (
    #         modified_line_count != 0
    #         or removed_line_count != 0
    #         or new_subtitle_file != original_subtitles
    #     ):
    #         print()  # Yes, a blank line
    #         if modified_line_count == 0 and removed_line_count == 0 and not quiet:
    #             print(
    #                 "Only changes to sorting and indexing found; No changes to subtitles detected."
    #             )
    #         if not quiet or verbose:
    #             print("Saving subtitle file {0}...".format(file))
    #             print()
    #         with open(file, "w", encoding="utf-8") as filehandler:
    #             filehandler.write(srt.compose(new_subtitle_file))
    #     else:
    #         if not quiet or verbose:
    #             print("No changes to save")
    #             print()

    # if summary or verbose:
    #     if dry_run:
    #         if verbose:
    #             print()
    #         print(
    #             "Summary: {0} Lines to be modified; {1} Lines to be removed; '{2}'".format(
    #                 modified_line_count, removed_line_count, file
    #             )
    #         )
    #     else:
    #         print(
    #             "Summary: {0} Lines modified; {1} Lines removed; '{2}'".format(
    #                 modified_line_count, removed_line_count, file
    #             )
    #         )
    #     print()

    return True


def parse_args():
    argsparser = argparse.ArgumentParser(
        description="Detect the language of subtitle(srt) file(s)"
    )
    argsparser.add_argument(
        "srt", nargs="*", help="One or more subtitle files or directories to operate on"
    )
    argsparser.add_argument(
        "--rename-files",
        "-r",
        action="store_false",
        dest="dry_run",
        help="The default is to do a dry-run. You must specify this option to rename files!",
    )
    argsparser.add_argument(
        "--summary", "-s", action="store_true", help="Provide a summary of the changes"
    )
    v_q_group = argsparser.add_mutually_exclusive_group()
    v_q_group.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Quiet output. Only errors will be printed on screen",
    )
    v_q_group.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output. Lines that have been modified will be printed on screen",
    )

    return argsparser.parse_args()


if __name__ == "__main__":
    sys.exit(main())