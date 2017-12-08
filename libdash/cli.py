import libdash.dash as dash
import argparse

def main ():
    parser = argparse.ArgumentParser(
        description = "JIRA dashboard, without browser GUI nonsense."
        )
    parser.add_argument("-q", "--query",
                        metavar="<query>",
                        default=None,
                        help="Query in JQL. If none is supplied, the default, which fetches all unfinished tickets assigned to you, is used.")

    args = parser.parse_args()

    dash.main(args.query)
    
