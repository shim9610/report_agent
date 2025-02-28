from main_test import main
from base import BaseAgent
from template_generator import ResultTemplate, Product, Reviews, Purchase_Info_Stores
from youtube_repoter import youtube_main
from review_repoter import review_main
from sepcification_repoter import sepcification_main
import asyncio
from typing import Dict, Any
from abc import ABC, abstractmethod


class ReportAgent(BaseAgent):
    def __init__(self,name="report_agent"):
        self.name=name
        self.Product=None
        self.Reviews=None
        self.Purchase_Info_Stores=None
        self.generator = ResultTemplate()
        self.result_dict = self.generator.dict
        self.repoterresponse={}
        self.youtube_report=None
        self.review_report=None
        self.specification_report=None
        
    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        data=input["middleware"]
        youtube_input=data["youtube"]
        review_input=data["review"]
        specification_input=data["specification"]
        
        (youtube,result_y),(rewivew,result_r),(specification,result_s)=await asyncio.gather(
            youtube_main(youtube_input),
            review_main(review_input),
            sepcification_main(specification_input),  
        )
        self.youtube_report=youtube
        self.review_report=rewivew
        self.specification_report=specification
        self.repoterresponse["youtube"]=result_y
        self.repoterresponse["review"]=result_r
        self.repoterresponse["specification"]=result_s
        output={}
        output['report']=self.sort_result()
        return output
        
    def sort_result(self):
        self.youtube_report.set_value(self.result_dict)
        self.review_report.set_value(self.result_dict)
        self.specification_report.set_value(self.result_dict)
        return self.result_dict
        