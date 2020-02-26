"""
name: HezzTwo card game by Amine
author: Amine Tahiri Alaoui
language: Python3
date: 26/feb/2020
place: sayibtha fi frachi XD
"""

from random import shuffle as _shuffle

blank_card = "+---+\n| ? |\n| ? |\n+---+"


class Card:
	_cards = {
		s + n: f"+---+\n| {n} |\n| {s} |\n+---+"
		for s in list('@#$&')
		for n in list('0123456789JQK')
	}
	
	def __init__(self, name):
		self.card = _cards[name]
		self.remove(name)
	
	@classmethod
	def remove(cls, name):
		cls._cards.pop(name)
	
	@classmethod
	def shuffle(cls):
		arr = [k + cls._cards[k] for k in cls._cards]
		_shuffle(arr)
		cls._cards = {i[:2]: i[2:] for i in arr}
	
	@classmethod
	def refresh(cls):
		cls._cards = {
			s + n: f"+---+\n| {n} |\n| {s} |\n+---+"
			for s in list('@#$&')
			for n in list('0123456789JQK')
		}
	
	def __repr__(self):
		return self.card


def print_card(*arg):
	lines = []
	for i in range(4):
		line = []
		for card in arg:
			line.append(card.split('\n')[i])
		lines.append("  ".join(line))
	for line in lines:
		print(line)


if __name__ == '__main__':
	print("rules, players, names")
	while True:
		user_input = input("[In]: ")

