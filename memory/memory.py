import json
import os
import dataclasses

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)
		
class Memory:
	def __init__(self, *, path = "", logging = False):
		self.logging = logging
		self.printLog(f"Working directory is {os.getcwd()}")
		if path == "":
			self.path = os.getcwd()
		else:
			self.path = path
		
		self.printLog(f"Loading CFG file in {self.path}")
		if not self.path.endswith(".json"):
			self.path = self.path+"/config.json"
			
		
		
		if not os.path.isfile(self.path):
			self.printLog(f"Creating config file; {self.path}")
			#open(self.path, 'w').close()
			with open(self.path, 'w') as f:
				f.write("{}")
		
		self.load()
	
	def printLog(self, message):
		if self.logging:
			print(f"[MEMORY] {message}")
	
	def _set(self, group, value = ""):
		self.data[group] = value
		self.save()
		
	def _get(self, group = "", default = ""):
		if group:
			data_g = self.data.get(group, default)
			return data_g
		else:
			return self.data
		
	def get(self, group = "", default = ""):
		return self._get(group, default)
		
	def load(self):
		with open(self.path, 'r') as f:
			content = f.read()
			try:
				self.data = json.loads(content)
			except json.decoder.JSONDecodeError as e:
				print(f"\x1b[31mERROR: JSON Decoder could not load the set file {self.path}\x1b[0m")
				print("Old file will be backed up and a new fresh file will be created.")
				print(e)
				with open(f"{self.path}.bk", 'w') as bk:
					#print(content)
					bk.write(content)
					
				#open(self.path, 'w').close()
				with open(self.path, 'w') as new:
					new.write("{}")
				
				self.data = {}
			except Exception as e:
				print(f"{type(e)} {e}")
			
	def save(self, *, encoder=EnhancedJSONEncoder):
		with open(self.path, "w") as s:
			json.dump(self.data, s, indent=4, sort_keys=True, cls=encoder)
