import sys
import re
from math import sqrt

allowedChar = ['+', '-', '/', '*', '=', 'X', 'x']
reg = '(?:([\+|\-]?(?:\d+(?:\.\d+)?)*)[X|x](?:\^(\d+))?)|([\+|\-]?(?:\d+(?:\.\d+)?)+)'
# regEx = '^([+-]?(?:((\d+(\.\d+)?( \* ))?[xX](\^\d+)?)|(\d+(\.\d+)?))(?:( [+-] )(?:((\d+(\.\d+)?( \* ))?[xX](\^\d+)?)|(\d+(\.\d+)?)))*( = )[+-]?(?:((\d+(\.\d+)?( \* ))?[xX](\^\d+)?)|(\d+(\.\d+)?))(?:( [+-] )(?:((\d+(\.\d+)?( \* ))?[xX](\^\d+)?)|(\d+(\.\d+)?)))*)$'

class Polynomial():

	def __init__(self):
		self.input = ""
		self.reducedForm = ""
		self.members = []
		self.degree = 0
		self.matches = None

	def parse(self):
		def getNumber(string, side):
			sign = 1
			if string == '':
				return side
			if string[0] == '+' or string[0] == '-':
				sign = -1 if string[0] == '-' else 1
				string = string[1:]
			try:
				return int(string) * sign * side
			except:
				try:
					return float(string) * sign * side
				except:
					return sign * side

		def getMember(group, side):
			if group[2] != '':
				member = {
					'coef': getNumber(group[2], side),
					'power': 0}
			else:
				member = {
					'coef': getNumber(group[0], side),
					'power': int(group[1]) if group[1] != '' else 1}
			return member

		for group in self.matchesleft:
			member = getMember(group, 1)
			# print(member)
			if member['coef'] != 0 or member['power'] != 0:
				self.members.append(getMember(group, 1))
		for group in self.matchesright:
			member = getMember(group, -1)
			if member['coef'] != 0 or member['power'] != 0:
				self.members.append(getMember(group, -1))

	def reduceForm(self):
		def findPowers(poly):
			powers = []
			for member in poly:
				try:
					if member['power'] is not '':
						if member['power'] not in powers:
							powers.append(member['power'])
				except:
					if 0 not in powers:
						powers.append(0)
			powers.sort(reverse=True)
			return powers

		powers = findPowers(self.members)
		self.maxPower = powers[0]
		reducedForm = []

		for i in range(len(powers)):
			reducedForm.append({'coef':0, 'power':powers[i]})
			for member in self.members:
				if member['power'] == powers[i]:
					reducedForm[i]['coef'] += member['coef']
				reducedForm[i]['coef'] = round(reducedForm[i]['coef'], 2)
		self.members = reducedForm


	def printReducedForm(self):
		start = True
		for member in self.members:
			if start is True:
				print('%s' % (member['coef'] if abs(member['coef']) != 1 else '-' if member['coef'] == -1 else ''), end='')
				print('%s' % ('X' if member['power'] > 0 else ''), end='')
				if member['power'] > 1:
					print('^%s' % member['power'], end='')
				start = False
			else:
				print(' %s ' % ('+' if member['coef'] > 0 else '-'), end='')
				print('%s' % abs(member['coef']) if abs(member['coef']) != 1 else '', end='')
				print('%s' % (' * X' if member['power'] > 0 and abs(member['coef']) != 1 else ('X' if abs(member['coef']) == 1 and member['power'] > 0 else (abs(member['coef']) if abs(member['coef']) == 1 else ''))), end='')
				if member['power'] > 1:
					print('^%s' % member['power'], end='')
		print(' = 0')

	def printDeg2Sol(self):
		def printPosSol(delta, a, b):
			print('Positive discriminent: 2 real solutions')
			x1 = (-b + sqrt(delta)) / (2 * a)
			x2 = (-b - sqrt(delta)) / (2 * a)
			if x1 == x2:
				print('X1 = X2 = %.2f' % x1)
			else:
				print('X1 = %.2f\nX2 = %.2f' % (x1, x2))

		def printNegSol(delta, a, b):
			print('Negative discriminent: 2 complex solutions')
			delta *= -1
			im = sqrt(delta) / (2 * a)
			real = -b / (2 * a)
			if real == 0.0:
				print('X1 = %.2fi\nX2 = %.2fi' % (im, -im))
			else:
				print('X1 = %.2f' % real, end='')
				print('%s' % (' + ' if im > 0.0 else ' - '), end='')
				print('%.2fi' % abs(im))
				print('X2 = %.2f' % real, end='')
				print('%s' % (' - ' if im > 0.0 else ' + '), end='')
				print('%.2fi' % abs(im))

		a = b = c = 0
		for member in self.members:
			a = member['coef'] if member['power'] == 2 else a
			b = member['coef'] if member['power'] == 1 else b
			c = member['coef'] if member['power'] == 0 else c
		delta = b * b - (4 * a * c)
		print('delta = %.2f' % delta)
		if delta == 0:
			print('Null discriminent: one double solution')
			print('X1 = X2 = %.2f' % (-b / (2 * a)))
		elif delta > 0:
			printPosSol(delta, a, b)
		else:
			printNegSol(delta, a, b)

	def solve(self):
		if self.maxPower > 2:
			print('Polynomial degree is greater than 2, can\'t solve !')
			exit()
		if self.maxPower < 1:
			print('This is not a polynomial equation !')
			exit()
		if self.maxPower == 1:
			print('Polynomial degree : 1')
			try:
				x = self.members[1]['coef'] * -1 / self.members[0]['coef']
			except:
				x = 0
			print('X = %s' % x)
		else:
			self.printDeg2Sol()

def exitError():
	print("Usage: python computor.py [polynomial string]")
	exit()

if __name__ == "__main__":
	if len(sys.argv) != 2 or not re.match(regEx, sys.argv[1]):
		exitError()
	poly = Polynomial()
	poly.input = sys.argv[1].replace(" ", "").replace("*", "")
	equals = poly.input.find('=')
	if equals != -1:
		poly.left = poly.input[:equals]
		poly.right = poly.input[equals + 1:]
	else:
		exitError()

	if re.match(reg, poly.input):
		poly.matchesleft = re.findall(reg, poly.left)
		poly.matchesright = re.findall(reg, poly.right)
		poly.parse()
		poly.reduceForm()
		poly.printReducedForm()
		poly.solve()
	else:
		print("Bad input !")