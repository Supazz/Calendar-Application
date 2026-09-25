#Main backend for calendar app data storage

#class NameConflictException(Exception):
#	'''Raised when trying to add an event under the same name as another.'''
#	pass

class event:
	'''This class just names the dictionary convention for events.'''
	@classmethod
	def mergeIntervals(self, *args) -> list:
		'''Merges lists of intervals - pairs of integers representing a start or an end.
		Multiple lists can be passed; the method will combine them.'''
		totalintv = [] 
		intvListToReturn = []

		for arg in args: #Typechecking: should be list|tuple of 2-tuples
			if type(arg) != list and type(arg) != tuple:
				raise TypeError(f"event.mergeIntervals: Invalid type '{type(arg)}'")
			for pair in arg:
				if type(pair) != tuple or len(pair) != 2:
					raise ValueError(f"event.mergeIntervals: Invalid pair '{pair}' in argument")
					break

		#Combine lists
		for arg in args:
			totalintv += arg

		#Edge case: Empty list
		if len(totalintv) == 0:
			return intvListToReturn

		totalintv.sort()
		intvcurrent = None

		while not len(totalintv) == 0:
			if intvcurrent == None:
				#print("Grabbing init intv!")
				intvcurrent = [totalintv[0][0], totalintv[0][1]]
			elif totalintv[0][0] <= intvcurrent[1] and totalintv[0][1] > intvcurrent[1]:
				#print("Replacing intv[1]!")
				intvcurrent[1] = totalintv[0][1]
			else:
				#print("Appending intv!")
				intvListToReturn.append( tuple(intvcurrent) )
				intvcurrent = [totalintv[0][0], totalintv[0][1]]
			totalintv.pop(0)

		#We are still holding on to the last interval
		if intvcurrent:
			intvListToReturn.append( tuple(intvcurrent) )

		return intvListToReturn

	#Magic Constructor
	def __init__(self, name: str = "New Event", priority: int = 0, intervals: list = [], info: dict = {}):
		self.name = name
		self.priority = priority
		self.intervals = event.mergeIntervals(intervals) #A series of 2-tuples representing start and end times
		self.info = info
	
	#Magic == operator
	def __eq__(self, other):
		if type(other) == event: #Avoid AttributeError
			return self.name == other.name and self.intervals == other.intervals
		return False
		
	def __repr__(self):
		return str([self.name, self.priority, self.intervals, self.info])

	#Simple accessors/mutators, improves readability

	#Intervals
	def addInterval(self, start: int, end: int):
		self.intervals.append( (start, end) )
		self.intervals = event.mergeIntervals(self.intervals)

	def delInterval(self, interval: tuple) -> tuple:
		if type(interval) != tuple or len(interval) != 2:
			raise ValueError("event.delInterval: Not a 2-tuple!")
		return self.intervals.pop( self.intervals.index(interval) )

	def findInterval(self, interval: tuple) -> int:
		if type(interval) != tuple or len(interval) != 2:
			raise ValueError("event.delInterval: Not a 2-tuple!")
		return self.intervals.index(interval)

	#Info
	def hasInfo(self, key) -> bool:
		return key in self.info

	def getInfo(self, key):
		return self.info[key]

	def delInfo(self, key) -> bool:
		if not self.hasInfo(key):
			return False
		del self.info[key]
		return True

class day:
	'''This class is a small day structure to aggregate events.'''
	def __init__(self): #Don't accept, we want to check events for validity
		self.events = {}

	#Magic 'in' operator
	def __contains__(self, key: event):
		'''Defines booelan value of "event in day" '''
		if type(key) == event and key.name in self.events:
			return self.events[key.name] == key
		else:
			return False

	def __repr__(self):
		return str(self.events)

	def addEvent(self, targetEvent: event, forced: bool = False) -> bool:
		'''Adds the target event, if its name is unique.
		If the name is not unique, the existing event will be overwritten if 'forced' is true.
		returns a boolean representing whether insertion was successful.'''
		if targetEvent.name in self.events:
			if not forced:
				return False
		self.events[targetEvent.name] = targetEvent
		return True

	def delEvent(self, targetEvent: event | str) -> bool:
		'''Deletes the target event or event name, if it exists.
		Returns a boolean representing whether the event was found.'''
		if type(targetEvent) == event:
			if targetEvent.name in self.events and targetEvent == self.events[targetEvent.name]:
				del self.events[targetEvent]
				return True
		else:
			if targetEvent in self.events:
				del self.events[targetEvent]
				return True
		return False

	def eventsWithInfo(self, info) -> list:
		'''Finds and returns events whose info dictonaries contain the specified key.'''
		eventsToReturn = []
		for eventID in self.events:
			if self.events[eventID].hasInfo(info):
				eventsToReturn.append(self.events[eventID])
		return eventsToReturn

	def isEmpty(self) -> bool:
		return len(events) == 0

class year:
	'''Aggregates days with a sparse dictionary (hashmap) representation.'''
	@classmethod
	def findStartDay(self, intYear: int = 2000) -> int:
		'''Calculates the first weekday of a given year. (0 is Monday, up to 6 for Sunday)'''
		#New year's 1970 was a Thursday, and we default to +1 day per year
		if intYear >= 1970:
			#The first two terms are the normal calc, the rest is for leap years
			return (3 + (intYear-1970) + (intYear-1968)//4 - (intYear-1968)//100 + 2*( (intYear-1968)//400 ) )%7
		else:
			pass #Stub, for years before 1970

	@classmethod
	def isLeapYear(self, intYear: int = 2000) -> bool:
		'''Returns whether the given year is a leap year.'''
		return intYear%4 == 0 and (intYear%100 != 0 or intYear%400 == 0)

	@classmethod
	def dateToDate(self, date: int|tuple, isLeap: bool = False) -> int|tuple:

		daysOfMonthsOfYear = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		currentIndex = 0
		totalMonthDays = 0

		if isLeap:
			daysOfMonthsOfYear[1] += 1

		match type(date).__name__:
			case "int":
				if date < 0 or not isLeap and date > 364 or date > 365:
						raise ValueError(f"year.dateToDate: Integer date out of range! ({intDate})")
				date += 1
				while totalMonthDays < date:
					totalMonthDays += daysOfMonthsOfYear[currentIndex]
					currentIndex += 1

				totalMonthDays -= daysOfMonthsOfYear[currentIndex - 1]
				return (currentIndex, date - totalMonthDays)

			case "tuple":
				if len(date) != 2:
					raise ValueError(f"year.dateToDate: Tuple date is not a 2-tuple! ({date})")
				if date[0] < 1 or date[0] > 12 or date[1] < 1 or date[1] > daysOfMonthsOfYear[date[0]]:
					raise IndexError(f"year.dateToDate: Tuple date points to nonexistient day! ({date})")
				currentIndex += 1
				while currentIndex < date[0]:
					totalMonthDays += daysOfMonthsOfYear[currentIndex-1]
					currentIndex += 1
				return ( totalMonthDays+date[1] ) - 1
			case _:
				raise TypeError(f"year.dateToDate: Incorrect type '{type(date)}' for dateToDate!")

	def __init__(self, intYear: int = 2000):
		#Struct_time reference: (timezone, hour, dst, day, minutes, month, seconds, dayName, dayOfYear, year, timezone name)
		self.actualYear = intYear
		self.isLeap = year.isLeapYear(intYear)
		self.startDay = year.findStartDay(intYear)
		self.days = {}

	def isInYear(self, date: int = 0) -> bool:
		if self.isLeap:
			return date >= 0 and date <= 365
		else:
			return date >= 0 and date <= 364

	def addEvent(self, targetEvent: event, date: int = 0, forced: bool = False) -> bool:
		'''Adds an event to the specified date.
		Returns the result of the underlying day.addEvent operation.'''
		if not self.isInYear(date):
			raise IndexError(f"year: Date is not in range! (date: {date})")
		if not date in self.days:
			self.days[date] = day()
		return self.days[date].addEvent(targetEvent, forced)

	def delEvent(self, targetEvent: event | str, date: int = 0) -> bool:
		'''Deletes the target event on a certain date.
		Returns a boolean representing whether the event was found.'''
		if not self.isInYear(date):
			raise IndexError(f"year: Date is not in range! (date: {date})")
		if not date in self.days:
			return False
		if not targetEvent in self.days[date]:
			return False

		if type(targetEvent) == event:
			del self.days[date][targetEvent.name]
		else:
			del self.days[date][targetEvent]

		#Remove unused day entries
		if self.days[date].isEmpty():
			del self.days[date]

	def findEvents(self, targetEvent: event | str) -> list: #TODO: Implement!
		pass

	def pruneDays(self) -> int: #TODO: Optimize!
		'''Explicitly finds and deletes days with zero events.'''
		daysDestroyed = 0
		for key in self.days:
			if self.days[key].isEmpty():
				del self.days[key]
				daysDestroyed += 1
		return daysDestroyed
