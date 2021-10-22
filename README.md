Flashback Thread Parser

Specify an URL to a thread and number of pages you want to parse. 

The script will then parse the thread and save each post on a new line in a CSV-file summarized per user or each post on one line for a specific user.

Options (flags):
  -h, --help            show this help message and exit
  -u URL, --url=URL     URL to Flashback thread, example:
                        https://www.flashback.org/t3360954
  -p PAGES, --pages=PAGES
                        Pages for Flashback thread you whish to parse
  -s USER, --user=USER  If you want to scrape posts from one user only,
                        specify user name (case sensitive)


Flags example: flash_parser.py -u https://www.flashback.org/t3360954 -p 2 -s ronaldo77