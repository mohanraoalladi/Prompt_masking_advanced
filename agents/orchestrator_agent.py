from typing import Dict, Any
import time

from agents.masking_agent import MaskingAgent
from agents.llm_agent import LlmAgent
from agents.unmask_agent import UnmaskAgent


class OrchestratorAgent:
    def __init__(self, api_key: str, model_name: str, pii_categories_enabled: Dict[str, bool]):
        self.masking_agent = MaskingAgent(pii_categories_enabled=pii_categories_enabled)
        self.llm_agent = LlmAgent(api_key=api_key, model_name=model_name)
        self.unmask_agent = UnmaskAgent()

    def run(self, user_prompt: str, use_llm: bool = True) -> Dict[str, Any]:
        masked_prompt, mapping = self.masking_agent.run(user_prompt)
        
        if use_llm:
            llm_response = self.llm_agent.run(masked_prompt)
        else:
            llm_response = masked_prompt
        
        final_output = self.unmask_agent.run(llm_response, mapping)

        return {
            "id": time.time(),  # Unique ID for this result
            "original_prompt": user_prompt,
            "masked_prompt": masked_prompt,
            "mapping": mapping,
            "llm_response_masked": llm_response,
            "final_output": final_output,
        }
