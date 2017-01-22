# -*- coding: utf-8 -*-
import argparse


def view_deck(path):
    pass


def study_deck(path):
    pass


def test_deck(path):
    pass


# main:
# 3 options
# edit deck (add, remove, change)
# edit/add:
# from file or from command line
# file: provide file, delimiter, reads file and inserts it
# study
# optional number of cards, shuffles deck and shows that number of cards
# yes/no: if you fail it gets shuffled back in
# view deck
def main():
    parser = argparse.ArgumentParser(description='Terminal based flashcard app')
    parser.add_argument('action', help='what to do',
                        choices=('edit', 'study', 'view'))
    parser.add_argument('-d', '--data', help='location of database',
                        default='data/flashcards.db')
    args = parser.parse_args()
    print(args.action)

    if args.action == 'edit':
        edit_deck(args.data)
    elif args.action == 'study':
        study_deck(args.data)
    elif args.action == 'view':
        view_deck(args.data)


if __name__ == '__main__':
    main()
