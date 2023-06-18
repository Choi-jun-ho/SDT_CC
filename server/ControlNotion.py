from notion_client import Client as Notion
from pprint import pprint
import requests

class ControlNotion:
	
	token = "secret_55HRvDCKsbV6P3iXfMcmbWItPeaQpONcU2WEAPwgFX6"

	def __new__(cls):
		if not hasattr(cls,'instance'):
			print('create')
			cls.instance = super(ControlNotion, cls).__new__(cls)
			cls.notion = Notion(auth=cls.token)
		else:
			print('recycle')
		return cls.instance
	
	async def search(self, database_name):
		print(database_name)
		
		database_info, header = self.get_databases_id_header(database_name)
		# print("result databaseId:", database_info["id"]) # type: ignore
		print("get database_info_header run")
		if database_info is False or database_info is None:
			return str({'header':None})
		
		database = self.notion.databases.query(database_id=database_info['id'])
		
		# pprint(database)
		
		table = self.toTalbe(database_name=database_name, header=header, notion_database=database['results']) # type: ignore
		return table
	
	async def del_page(self, database_name, page_name):
		database_info, header = self.get_databases_id_header(database_name)
		
		if database_info is False or database_info is None:
			return str({'header':None})
		
		database_id = database_info['id']
		page_id = self.get_page_id(database_id, page_name)

		self.notion.pages.update(page_id=page_id, archived=True) # type: ignore

		database = self.notion.databases.query(database_id=database_info['id'])		
		# pprint(database)		
		table = self.toTalbe(database_name=database_name, header=header, notion_database=database['results']) # type: ignore
		return table

	async def update_page(self, database_name, page_name, properties):
		database_info, header = self.get_databases_id_header(database_name)
		
		if database_info is False or database_info is None:
			return str({'header':None})
		
		database_id = database_info['id']

		page_id = self.get_page_id(database_id, page_name)
		
		page_sample = self.notion.pages.retrieve(page_id=page_id) # type: ignore
		properties_new = page_sample['properties'] # type: ignore

		# propeties 구분
		print("header")
		# pprint(header)
		print("properties_new")
		# pprint(properties_new)

		for key_value in properties:
			key, value = key_value.split('=')
			properties_new = self.proper_update(properties_new, header, key, value)

		print("set properties_new")
		self.notion.pages.update(page_id=page_id, properties=properties_new) # type: ignore
		print("set properties_new done")

		database = self.notion.databases.query(database_id=database_info['id'])		
		# pprint(database)		
		table = self.toTalbe(database_name=database_name, header=header, notion_database=database['results']) # type: ignore
		return table	

	async def create_page(self, database_name, page_name, properties):
		print('create_page: ' + database_name)
		database_info, header = self.get_databases_id_header(database_name)
		
		if database_info is False or database_info is None:
			print("database not found")
			return str({'header':None})
		
		database_id = database_info['id']

		print("_________database_id: ", database_id)

		parents_obj = {'database_id':database_id}

		# pprint(database_info)
		# key = database_info['properties'].keys()[0]
		# page 만들기 
		page_id = self.get_page_id_for_not_name(database_id) # type: ignore

		print("page_id", page_id)
		page_sample = self.notion.pages.retrieve(page_id=page_id) # type: ignore
		properties_new = page_sample['properties'] # type: ignore
		print("---------------------------")
		# pprint(properties_new)

		title_key = ''
		for key in header.keys(): # type: ignore
			if header[key] == 'title': # type: ignore
				title_key = key
		
		properties_new = self.proper_update(properties_new, header, title_key, page_name)

		page_keys = [title_key]
		for key_value in properties:
			key, value = key_value.split('=')
			if header[key] == 'title': # type: ignore
				continue
			page_keys.append(key)
			properties_new = self.proper_update(properties_new, header, key, value)
		print("---------------------------")
		# pprint(properties_new)
		if properties_new is not None:
			print("key: ", properties_new.keys(), "page_keys: ", page_keys)
			li = list(properties_new.keys())
			for k in li:
				# print(k)
				if k not in page_keys and properties_new.keys():
					properties_new.pop(k, None)

		self.notion.pages.create(parent=parents_obj, properties=properties_new)

		database = self.notion.databases.query(database_id=database_info['id'])		
		# pprint(database)		
		table = self.toTalbe(database_name=database_name, header=header, notion_database=database['results']) # type: ignore
		return table
	
	def proper_update(self, properties_new, header, key, value):
		kind = header[key]
		if kind == 'select':
			properties_new[key][kind]['name'] = value
			del properties_new[key][kind]['id']
			return properties_new
		if kind == 'status':
			properties_new[key][kind]['name'] = value
			del properties_new[key][kind]['id']
			return properties_new
		if kind == 'title':
			if len(properties_new[key][kind]) == 0:
				return properties_new
			properties_new[key][kind][0]['plain_text'] = value
			properties_new[key][kind][0]['text']['content'] = value
			return properties_new
		if kind == 'rich_text':
			if len(properties_new[key][kind]) == 0:
				return properties_new
			properties_new[key][kind][0]['plain_text'] = value
			properties_new[key][kind][0]['text']['content'] = value
			del properties_new[key]['id']
			return properties_new
		if kind == 'number':
			properties_new[key][kind] = int(value)
			del properties_new[key]['id']
			return properties_new
		if kind == 'multi_select':
			return properties_new		
		
	def toTalbe(self, database_name, header, notion_database):
		table = {"database_name":database_name, 'table_name':"discordNotion", "header":header, "data":[[]], 'analyzes' : ["", "", "", ""]}
        
		data = []

		for notion_datas in notion_database:
			raw_data = []
			for property_key in notion_datas['properties'].keys():
				if property_key not in header.keys():
					continue
				# print("property_key: " + property_key)
				notion_data_type = header[property_key]
				notion_data = notion_datas['properties'][property_key][notion_data_type]
				raw_data.append('{0:<10}'.format(str(self.get_data_by_type(notion_data, notion_data_type)))) # type: ignore
			data.append(raw_data)
		
		table['data'] = data


		return table
	
	def get_data_by_type(self, data, type):
		if data == None:
			return ""		
		if type == 'select':
			return data['name']
		if type == 'people':
			result = ""
			for i in data:
				result += "," + i['name']
			return result
		if type == 'status':
			return data['name']
		if type == 'text':
			return data['plain_text']
		if type == 'number':
			return data
		if type == 'multi_select':
			if len(data) == 0:
				return ""
			result = data[0]['name']
			for i in data[1:]:
				result += "," + i['name']
			return result
		if type == 'title':
			if len(data) == 0:
				return ""
			return data[0]['plain_text']
		if type == 'rich_text':
			
			if len(data) == 0:
				return ""
			if len(data[0]['plain_text']) > 25:
				return data[0]['plain_text'][:25] + " ... "
			return data[0]['plain_text']

		return ""
	
	def get_databases_id_header(self, database_name):
		databases = self.notion.search(filter={"property": "object", "value": "database"})
		database_cursor_id = databases['next_cursor'] # type: ignore
		database_id, header = self.databases_id_one_time(databases, database_name)
		
		while databases['has_more'] and (database_id is False): # type: ignore
			databases = self.notion.search(filter={"property": "object", "value": "database"}, start_cusor=database_cursor_id)
			database_id, header = self.databases_id_one_time(databases, database_name)
			if databases['has_more']: # type: ignore
				database_cursor_id = databases['next_cursor'] # type: ignore
		return database_id, header
	
	def get_page_id_for_not_name(self, database_id):
		pages = self.notion.search(filter={"property": "object", "value": "page"})
		
		print("__________pages_______________")
		
		result_pages = pages['results'] # type: ignore
		
		if (len(result_pages) == 0):
			print("databaseId false : not database")
			return False
		
		for pages in result_pages:
			# pprint(pages)
			if pages['parent']['database_id'] == database_id:
				return pages['id']
			
		print("get_page_name: databaseId false : not text")
		return False
	
	def get_page_id(self, database_id, page_name):
		pages = self.notion.search(filter={"property": "object", "value": "page"})
		#pprint(pages)
		pages_cursor_id = pages['next_cursor'] # type: ignore
		pages_id = self.pages_id_one_time(database_id, pages, page_name)
		
		while pages['has_more'] and (pages_id is False): # type: ignore
			pages = self.notion.search(filter={"property": "object", "value": "page"}, start_cusor=pages_cursor_id)
			pages_id = self.pages_id_one_time(database_id, pages, page_name)
			
			if pages['has_more']: # type: ignore
				pages_cursor_id = pages['next_cursor'] # type: ignore
		return pages_id
	
	def pages_id_one_time(self, database_id, pages, page_name):
		
		result_pages = pages['results']
		
		if (len(result_pages) == 0):
			print("databaseId false : not database")
			return False
		
		for pages in result_pages:
			title_name = ""
			if pages['parent']['database_id'] != database_id:
				continue
			
			for name in pages['properties'].keys():
				if pages['properties'][name]['id'] == 'title':
					# print("page", pages['properties'][name]['title'])
					if len(pages['properties'][name]['title']) == 0:
						continue
					title_name = pages['properties'][name]['title'][0]['plain_text']
					break
			# print(title_name, page_name)
			if title_name == page_name:
				print("titile delete item Search Ok")
				return pages['id']
		
		print("pages_id_one_time: databaseId false : not text")
		return False
	
	def databases_id_one_time(self, databases, name):
		
		result_databases = databases['results']
		
		# pprint(databases)
		if (len(result_databases) == 0):
			print("databaseId false : not database")
			return False, False
		
		for database in result_databases:
			if database['title'][0]['plain_text'] == name:
				# print("databaseId", database['id'])
				header = {}
				# print("propetiesKeys:" + str(database['properties'].keys()));
				for property_key in database['properties'].keys():
					header[property_key] = database['properties'][property_key]['type']

				return database, header
		
		print("databases_id_one_time: databaseId false : not text")
		return False, False
		