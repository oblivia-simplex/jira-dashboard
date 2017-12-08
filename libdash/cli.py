import libdash.dash as dash
import argparse

def main ():
    parser = argparse.ArgumentParser(
        description = "JIRA dashboard, without browser GUI nonsense."
        )

    parser.add_argument("-a", "--all",
                        action="store_true",
                        default=False,
                        help="Show results for all users, and not just you, yourself, alone.")
    parser.add_argument("-q", "--query",
                        metavar="<query>",
                        default=None,
                        help="Query in JQL. If none is supplied, the default, which fetches all unfinished tickets assigned to you, is used.")
    parser.add_argument("-c", "--colour",
                        action="store_true",
                        default=False,
                        help="Colourize things. Make them pretty.")
    args = parser.parse_args()

    dash.main(args.query, only_mine=(not args.all), colour=args.colour)
    
