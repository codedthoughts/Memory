import json
import os
import dataclasses
from datetime import datetime
import humanfriendly
try:
	import toml
	TOML_ENABLED = True
except:
	TOML_ENABLED = False
	
class EnhancedJSONEncoder(json.JSONEncoder):
	def default(self, o):
		if dataclasses.is_dataclass(o):
			return dataclasses.asdict(o)
		return super().default(o)
		
class Memory:
	def __init__(self, *, path = "", logging = False, engine="json"):
		self.logging = logging
		self.defaults = []
		self.printLog(f"Working directory is {os.getcwd()}")
		
		self.engine = None
		
		if engine == "json":
			self.default = "{}"
			self.engine = json
			
		elif engine == "toml":
			if TOML_ENABLED:
				self.default = ""
				self.engine = toml	
			else:
				print("ERROR: TOML module not installed. Run `pip3 install toml` first.")

		if not self.engine:
			self.default = "{}"
			self.engine = json
			print("ERROR: No parser engine defined. Defaulting to json engine.")
			
		if path == "":
			self.path = os.getcwd()
		else:
			self.path = path
		
		self.printLog(f"Loading CFG file in {self.path}")
		if not self.path.endswith(f".{engine}"):
			self.path = f"{self.path}/config.{engine}"
			
		if not os.path.isfile(self.path):
			self.printLog(f"Creating config file; {self.path}")
			with open(self.path, 'w') as f:
				f.write(self.default)
		
		self.load()
		
	def __getitem__(self, item):
		return self.data[item]	
	 
	def convert(self, engine):
		if engine == "json":
			self.default = "{}"
			self.engine = json
			self.path = self.path.replace('.toml', '.json')
			return
			
		elif engine == "toml":
			if TOML_ENABLED:
				self.default = ""
				self.engine = toml	
				self.path = self.path.replace('.json', '.toml')
				return
			else:
				print("ERROR: TOML module not installed. Run `pip3 install toml` first.")

		print("ERROR: No parser engine defined. Can not convert")
			
	def printLog(self, message):
		if self.logging:
			print(f"[MEMORY] {message}")
	
	def _set(self, group, value = ""):
		self.data[group] = value
		self.save()
	
	def get(self, group = "", default = ""):
		return self._get(group, default)
	
	def _get(self, group = "", default = ""):
		if group:
			data_g = self.data.get(group, default)
			if data_g == default:
				nd = {'key':group, 'value':default}
				if nd not in self.defaults:
					self.defaults.append(nd)
			return data_g
		else:
			return self.data
		
	def load(self):
		with open(self.path, 'r') as f:
			content = f.read()
			try:
				self.data = self.engine.loads(content)
			except Exception as e:
				print(f"\x1b[31mERROR: Decoder could not load the set file {self.path}\x1b[0m")
				print("Old file will be backed up and a new fresh file will be created.")
				print(e)
				with open(f"{self.path}.bk", 'w') as bk:
					#print(content)
					bk.write(content)
					
				#open(self.path, 'w').close()
				with open(self.path, 'w') as new:
					new.write(self.default)
				
				self.data = {}
			
	def save(self, *, encoder=EnhancedJSONEncoder, pretty=False):
		with open(self.path, "w") as s:
			if pretty:
				try:
					self.engine.dump(self.data, s, indent=4, sort_keys=True, cls=encoder)
					return
				except:
					print("===== Pretty printing error. =====")
					
			self.engine.dump(self.data, s)
			
class Flags(dict):
	def __init__(self, *, autotyping=False):
		self.data = {}
		self.autotyping = autotyping
		
	def autotype(self, value):
		if self.autotyping:
			if type(value) == str:
				if value.isdigit():
					if "." in value:
						value == float(value)
					else:
						value = int(value)
				
				if value.lower() == "true":
					value = True
					
				if value.lower() == "false":
					value = False
				
		return value
		
	def _set(self, key, value):
		old = self.data.get(key)
		self.data[key] = self.autotype(value)
		return {'old': old, 'new': self.data[key]}
	
	def _get(self, key):
		return self.data[key]
	
class Timer:
	def __init__(self, *, start=None, logging=False):
		self.start_time = start
		self.logging = logging
	
	def log(self, message, *, tag="Memory-Timer"):
		if self.logging:
			print(f"{tag}: {message}")
			
	def start(self):
		if not self.start_time:
			self.log("Timer started.")
			self.start_time = datetime.now()
		
	def check(self):
		if self.start_time:
			raw = datetime.now() - self.start_time
			self.log(raw.seconds)
			return datetime.now() - self.start_time
		else:
			return datetime.now()
		
	def seconds(self):
		return self.check().seconds
	
	def microseconds(self):
		return self.check().microseconds

	def ms(self):
		return (self.microseconds()/10000)
	
	def humanize(self):
		return humanfriendly.format_timespan(self.seconds())
	
	def end(self):
		if self.start_time:
			value = self.check()
			self.start_time == None
			return value
