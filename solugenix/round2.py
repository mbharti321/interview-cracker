--connect LLM
-- pass query
-- return response
-- keeping mind of solid principals




--
from OpenAI import openai




class LLMClient:
	-- llm_url ="----url"
	api_key = "api-key"
	model_type = "gpt-4o"

	def __init
	
	params = {
			"api_key": api_key,
			"model": model_type,
			"temprate
		}

	openapi_client = openai(params);

	def get_llm_client():
		retrun openapi_client;

class LLMService:
	
	llmClient
	def __init__(llmclient: LLMClient):
		self.llmClient = llmclient

	get_responce(userQuery, context):
		
		prompt = f'''here is user's query: {userQuery.query}
			Please refer to these context {context} and generate the response"
		
		params = {
			"prompt": prompt
		}

		response = await llmClient.getResponse(params)

		return response;
	