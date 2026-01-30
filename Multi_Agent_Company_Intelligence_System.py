
import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()

# Initialize LLM with error handling
try:
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3
    )
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    print("Please ensure OPENAI_API_KEY is set in your .env file")
    exit(1)


class DataCollectorAgent:
    """
    Fetches company news and stock data (dummy or API-based)
    """

    def __init__(self):
        try:
            self.prompt = ChatPromptTemplate.from_template(
                """
                You are a Data Collection Agent.
                Collect recent news, stock performance, and key events
                for the company: {company}

                If real-time data is unavailable, generate realistic dummy data.
                Output in structured JSON format.
                """
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize DataCollectorAgent: {e}")

    def run(self, company: str):
        if not company or not isinstance(company, str):
            return {"error": "Invalid company name provided"}
        
        try:
            chain = self.prompt | llm
            response = chain.invoke({"company": company})
            return response.content
        except Exception as e:
            error_msg = f"Error collecting data for {company}: {str(e)}"
            print(error_msg)
            return {"error": error_msg}


class AnalystAgent:
    """
    Analyzes data and produces insights and risk factors
    """

    def __init__(self):
        try:
            self.prompt = ChatPromptTemplate.from_template(
                """
                You are a Financial Analyst Agent.

                Based on the following company data:
                {company_data}

                1. Summarize the current business situation
                2. Identify growth opportunities
                3. Identify risks
                4. Provide an overall outlook
                """
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize AnalystAgent: {e}")

    def run(self, company_data: str):
        if not company_data:
            return {"error": "No company data provided for analysis"}
        
        try:
            chain = self.prompt | llm
            response = chain.invoke({"company_data": company_data})
            return response.content
        except Exception as e:
            error_msg = f"Error analyzing company data: {str(e)}"
            print(error_msg)
            return {"error": error_msg}


class OrchestratorAgent:
    """
    Controls agent execution and maintains memory
    """

    def __init__(self):
        try:
            self.memory = ConversationBufferMemory(return_messages=True)
            self.data_agent = DataCollectorAgent()
            self.analyst_agent = AnalystAgent()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize OrchestratorAgent: {e}")

    def run(self, company: str):
        if not company or not isinstance(company, str):
            return {
                "error": "Invalid company name provided",
                "company": None,
                "raw_data": None,
                "analysis": None
            }
        
        try:
            # Step 1: Collect Data
            print(f"Collecting data for {company}...")
            data = self.data_agent.run(company)
            
            if isinstance(data, dict) and "error" in data:
                return {
                    "company": company,
                    "raw_data": None,
                    "analysis": None,
                    "error": data["error"]
                }
            
            self.memory.save_context(
                {"input": f"Collected data for {company}"},
                {"output": data}
            )

            # Step 2: Analyze Data
            print(f"Analyzing data for {company}...")
            analysis = self.analyst_agent.run(data)
            
            if isinstance(analysis, dict) and "error" in analysis:
                return {
                    "company": company,
                    "raw_data": data,
                    "analysis": None,
                    "error": analysis["error"]
                }
            
            self.memory.save_context(
                {"input": "Analyze company data"},
                {"output": analysis}
            )

            return {
                "company": company,
                "raw_data": data,
                "analysis": analysis,
                "memory": self.memory.load_memory_variables({})
            }
        
        except Exception as e:
            error_msg = f"Orchestration error for {company}: {str(e)}"
            print(error_msg)
            return {
                "company": company,
                "raw_data": None,
                "analysis": None,
                "error": error_msg
            }


if __name__ == "__main__":
    try:
        orchestrator = OrchestratorAgent()
        
        # Define company_1
        company_1 = "Soulpage IT Solutions"
        
        print(f"
{'='*50}")
        print("COMPANY INTELLIGENCE REPORT")
        print(f"{'='*50}
")
        
        result = orchestrator.run(company_1)
        
        if "error" in result:
            print(f"❌ ERROR: {result['error']}")
        else:
            print(f"Company: {result['company']}
")
            print(f"{'-'*50}")
            print("RAW DATA")
            print(f"{'-'*50}")
            print(result["raw_data"])
            print(f"
{'-'*50}")
            print("ANALYSIS")
            print(f"{'-'*50}")
            print(result["analysis"])
            print(f"
{'='*50}
")
    
    except KeyboardInterrupt:
        print("

Process interrupted by user")
    except Exception as e:
        print(f"
❌ Fatal error: {str(e)}")
        exit(1)

