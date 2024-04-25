import duckdb
import pandas as pd
import openai
import ollama

class SqlPrompt:
    
    """
    Setting Up the Prompt Features
    """

    def __init__(self, table):
        self.table = table
        self.question = None
        self.message = None
    
    def get_table_schema(self):
        """
        The function uses DuckDB and SQL to extract table schema from Pandas DataFrame object
        """
    
        tbl_describe = duckdb.sql("DESCRIBE SELECT * FROM " + self.table +  ";")
        col_attr = tbl_describe.df()[["column_name", "column_type"]]
        col_attr["column_joint"] = col_attr["column_name"] + " " +  col_attr["column_type"]
        self.schema = str(list(col_attr["column_joint"].values)).replace('[', '').replace(']', '').replace('\'', '')
        self.column_names = col_attr["column_name"]
        self.column_type = col_attr["column_type"]

    def set_prompt(self, question):
        
        if "schema" not in self.__dict__.keys():
            self.get_table_schema()


        system_template = """

    Given the following SQL table, your job is to write queries given a user’s request. \n

    CREATE TABLE {} ({}) \n
                        """
        user_template = "Write a SQL query that returns - {}"

        self.system = system_template.format(self.table, self.schema)
        self.user = user_template.format(question)
        self.message =  [
                        {
                          "role": "system",
                          "content": self.system
                        },
                        {
                          "role": "user",
                          "content": self.user
                        }
                        ]
        
    def openai_request(self, 
                       openai_api_key,
                       model = "gpt-3.5-turbo", 
                       temperature = 0, 
                       max_tokens = 256, 
                       frequency_penalty = 0,
                       presence_penalty= 0):
        openai.api_key = openai_api_key
        self.openai_response = openai.ChatCompletion.create(
            model = model,
            messages = self.message,
            temperature = temperature,
            max_tokens = max_tokens,
            frequency_penalty = frequency_penalty,
            presence_penalty = presence_penalty)
        
        self.query =  add_quotes(query = self.openai_response["choices"][0]["message"]["content"], 
                                            col_names = self.column_names)
        
        self.query = remove_code_chunk(self.query)
    
    def get_data(self):
        if self.message is None:
            print("The prompt is not defined")
            return
        else:
            print(duckdb.sql(self.query))
            self.data = duckdb.sql(self.query)

    def ask_question(self, 
                     question,
                     openai_api_key,
                     model = "gpt-3.5-turbo", 
                     temperature = 0, 
                     max_tokens = 256, 
                     frequency_penalty = 0,
                     presence_penalty= 0):
        self.set_prompt(question)
        self.openai_request(openai_api_key = openai_api_key,
                            model = "gpt-3.5-turbo", 
                            temperature = 0, 
                            max_tokens = 256, 
                            frequency_penalty = 0,
                            presence_penalty= 0)
        # self.get_data()
    def ask_ollama(self,
                   question,
                   model):
        self.set_prompt(question)
        response = ollama.chat(model=model, messages = self.message)
        self.ollama_response = ollama.chat(model=model, messages = self.message)
        self.markdown =  add_quotes(query = self.ollama_response['message']['content'], 
                                            col_names = self.column_names)
        self.markdown = remove_text(query = self.markdown)
        self.query = remove_code_chunk(query=self.markdown)
        
        
            
                

def remove_text(query):
    if "```sql\n" in query and "```\n" in query:
        s = query.find("```sql\n")
        e = query.find( "```\n") + 4
        query = query[s:e]
        return query
    else: 
        return query



def remove_code_chunk(query):
    if "```sql\n" in query:
        query = str(query).replace( "```sql\n", "")
    if "```" in query:
        query = str(query).replace( "```", "")
    return query

def add_quotes(query, col_names):
    """
    Helper function to parse the quotes from a returned query
    """
    for i in col_names:
        s = " " + i + " "
        if s in query: 
            r = ' "' + i + '" '
            query = str(query).replace(s, r) 

    return(query)
