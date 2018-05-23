import cherrypy
import string
import random
import redis
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))
class StockInfo(object):
    @cherrypy.expose
    def index(self):
    	self.conn = redis.Redis("localhost")
    	equity_data = self.conn.hgetall("equity_db")
    	top_ten_dict = {}
    	top_ten = []
    	for key, value in equity_data.items():
    		top_ten.append((str(key, 'utf-8'), [val for val in eval(value).values()]))
    		if len(top_ten) > 10:
    			break
    	top_ten_dict['names'] = top_ten
    	#equity_data = {"name": {"start": 10, "end":20}}
    	templ = env.get_template("index.html")
    	return templ.render(top_ten_dict)

    @cherrypy.expose
    def get_data(self, company_name):
    	self.conn = redis.Redis("localhost")
    	search_data = self.conn.hget("equity_db", company_name.lower())
    	company_data = [company_name.lower().title()]
    	for item in eval(search_data).values():
    		company_data.append(str(item))
    		
    	#company_data = [company_name]+[x for x in eval(search_data).values()]
    	company_data_dict = {'names': company_data}
    	templ = env.get_template("search.html")
    	return templ.render(company_data_dict)
    	#return company_data


if __name__ == '__main__':
    cherrypy.quickstart(StockInfo())

#cd Documents\cherrypy_tutorial