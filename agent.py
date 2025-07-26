# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict, Optional
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
import os

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

def after_tool_callback(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    
    print("TOOL RESPONSE**************************************",tool_response)

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='finance_assistant',
    instruction=f"""\
Answer user's questions about personal finance.
You have access to the following tools:
-fetch_net_worth
-fetch_credit_report
-fetch_epf_details
-fetch_mf_transactions
-fetch_bank_transactions
-fetch_stock_transactions
Use them when necessary to answer the user's questions.
Note: when you call a tool for the first time, 
the tool will respond with an authentication link. 
Just give the message returned by the tool as it is to the user. 
Let the user authenticate and then you will receive a mcp session ID, remember this ID.
Make the tool call once again 
after the user has confirmed that they have authenticated.
Also answer questions like “Can I retire at 45?” or “Which of my SIPs and NFTs are
underperforming?” by reasoning over the user’s full financial context.
To figure out which of your SIPs are underperforming, I recommend you:
Identify the benchmark: Determine the appropriate benchmark for each mutual fund (e.g., Nifty 50 for an Nifty 50 index fund).
Calculate returns: Calculate the returns for each of your mutual fund investments over a specific period (e.g., 1 year, 3 years).
Compare to benchmark: Compare the returns of each mutual fund to its benchmark. If a fund is consistently underperforming its benchmark, it may be considered underperforming.
To determine if you can retire at 45, I need to make some assumptions and projections:
Current Age: I need to know your current age to estimate the number of years until your target retirement age of 45.
Expenses: I need an estimate of your current annual expenses and how they might change in retirement.
Income: I need to know your current annual income and how much you are saving each year.
Investment Returns: I will assume a reasonable rate of return on your investments. This can be adjusted based on your risk tolerance.
Inflation: I will factor in inflation to estimate future expenses.
    """,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url='http://localhost:8080/mcp/stream',
                
            ) 
            
        )
    ],
    after_tool_callback=after_tool_callback
)
