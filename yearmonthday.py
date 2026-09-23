#Main backend for calendar app data storage

from time import struct_time, timezone, mktime

class NameConflictException(Exception):
	'''Raised when trying to add an event under the same name as another.'''
	pass

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
				raise TypeError(f"event: Invalid type '{type(arg)}' passed to mergeIntervals")
			for pair in arg:
				if type(pair) != tuple or len(pair) != 2:
					raise ValueError(f"event: Invalid pair '{pair}' in mergeIntervals argument")
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
	def __init__(self, name: str = "New Event", priority: int = 0, intervals: list = []):
		self.name = name
		self.priority = priority
		self.intervals = event.mergeIntervals(intervals) #A series of 2-tuples representing start and end times
	
	#Magic == operator
	def __eq__(self, other):
		if type(other) == event: #Avoid AttributeError
			return self.name == other.name and self.intervals == other.intervals
		return False

	#Magic + operator
	def __add__(self, other):
		if type(other) != event:
			raise TypeError(f"event: Cannot add types 'event' and '{type(other)}'")
		eventToReturn = event(name = self.name, priority = max(self.priority, other.priority), intervals = event.mergeIntervals(self.intervals, other.intervals))
		return eventToReturn
		
	def __repr__(self):
		return str([self.name, self.priority, self.intervals])


class day:
	'''This class is a small day structure to aggregate events.'''
	def __init__(self, events: dict = {}):
		self.events = events

	#Magic + operator
	def __add__(self, other):
		'''Operator +, produces the union of each day's events'''
		pass

	#Magic 'in' operator
	def __contains__(self, key: event|str):
		'''Defines booelan value of "event in day" '''
		if type(key) == event:
			return key.name in self.events
		else:
			return key in events

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

#WIP, MAY BE REMOVED
class year:
	'''This class aggregates the 'day' class into a central data structure.'''
	def __init__(self, year: int = 2000):
		if year < 1970:
			raise ValueError(f"year: UNIX time does not count before Jan. 1969! (input: {year})")
		#Struct_time reference: (timezone, hour, dst, day, minutes, month, seconds, dayName, dayOfYear, year, timezone name)
		pass

