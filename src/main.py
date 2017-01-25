# -*- coding: utf-8 -*-
"""Main module"""
import argparse
import datetime
import random
import sqlite3


def try_create_deck(path):
    """
    Attempt to create table in database at path to store flash cards.
    Fails if database already exists.
    """
    conn = sqlite3.connect(path)
    try:
        with conn:
            conn.execute('''CREATE TABLE cards
            (deck text, front text, back text, date_added text, views text)''')
    except sqlite3.OperationalError:
        pass

def clean_deck(path, deck):
    """Remove the table."""
    conn = sqlite3.connect(path)
    try:
        with conn:
            conn.execute('DROP TABLE ?', deck)
    except sqlite3.OperationalError:
        pass


def edit_deck(path, deck):
    """Edit deck stored at path."""
    try_create_deck(path)
    print('Enter in the flash cards:')

    conn = sqlite3.connect(path)
    count = 1
    front = input('Card %d Front: ' % count)
    back = input('Card %d Back: ' % count)

    with conn:
        while front and back:
            row = (deck, front, back, datetime.datetime.now(), 0)
            conn.execute('INSERT INTO cards VALUES (?, ?, ?, ?, ?)', row)

            count += 1
            front = input('\nCard %d Front: ' % count)
            back = input('Card %d Back:  ' % count)


def study_deck(path, deck, num=None):
    """Study deck stored at path."""
    conn = sqlite3.connect(path)
    with conn:
        if num:
            cards = conn.execute('''SELECT front, back FROM cards
            WHERE deck=(?) limit (?)''', (deck, num)).fetchall()
        else:
            cards = conn.execute('SELECT front, back FROM cards WHERE deck=(?)',
                                 (deck,)).fetchall()
        random.shuffle(cards)
        for front, back in cards:
            print('Front: %s' % front)
            input('Answer? ')
            print('Back: %s\n' % back)


def view_deck(path, deck):
    """View deck stored at path."""
    conn = sqlite3.connect(path)
    with conn:
        for row in conn.execute('SELECT * FROM cards WHERE deck=(?)', deck):
            print(row)


def main():
    """
    Parse arguments and perform requested action.

    For more details, run `main.py -h`.
    """
    parser = argparse.ArgumentParser(description='Terminal based flashcard app')
    parser.add_argument('action', help='what to do',
                        choices=('edit', 'study', 'view'))
    parser.add_argument('deck', help='deck to work with')
    parser.add_argument('-d', '--data', help='location of database',
                        default='data/flashcards.db')
    parser.add_argument('-n',
                        help='number of cards to study (when "study" picked)',
                        type=int)
    args = parser.parse_args()

    if args.action == 'edit':
        edit_deck(args.data, args.deck)
    elif args.action == 'study':
        if args.n:
            study_deck(args.data, args.deck, args.n)
        else:
            study_deck(args.data, args.deck)
    elif args.action == 'view':
        view_deck(args.data, args.deck)


if __name__ == '__main__':
    main()
