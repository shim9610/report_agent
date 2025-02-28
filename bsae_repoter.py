from utility import Node
import re
from dummy import get_test_dummy
from template_generator import ResultTemplate, Product, Reviews, Purchase_Info_Stores
class BaseRepoter:
    def __init__(self,data,section1,section2,query,table_content,prompt,model,script,selfquestion,selfanswer,context):

        self.data=data
        self.section1=section1
        self.section2=section2
        self.table_content=table_content
        self.prompt=prompt
        self.query=query
        self.model=model
        self.script=script
        self.selfquestion=selfquestion
        self.selfanswer=selfanswer
        self.N=0
        self.context=context
    def try_get_response(self,query,num):
        if len(self.selfanswer)>0:
            nm=1
            stack=[]
            for q in self.selfanswer:
                stack.append(f'{nm}번째 질문 : {self.selfquestion[nm-1]}, {nm}번째 답변 : {q}')
                nm+=1
            char="\n".join(stack)
            new_context=self.script[num]+char+self.context

        else:    
            new_context=self.script[num]+self.context
        self.model.change_context(new_context)
        if len(self.selfquestion)>0:
            if isinstance(self.selfquestion[-1],list):
                inputquestion=" ,질문 : ".join(self.selfquestion[-1])
            else:
                inputquestion=self.selfquestion[-1]
            Nquery="스스로 하는 질문 : " + inputquestion+" 유저 요청 : "+query + "Rule : "+self.script[num]
            self.selfquestion.append("스스로 하는 질문 : " + inputquestion)
            response=self.model.get_response(Nquery)

        else:
            response=self.model.get_response("유저 요청 : "+query)
        return response
    def parse_youtuber_output(self,text):
        # [[키::값]] 또는 [[키:값]] 형태의 항목을 찾는 정규표현식
        pattern = r"\[\[([^:\]]+)(?:::|:)(.*?)\]\]"
        matches = re.findall(pattern, text, re.DOTALL)
        
        result = {}
        for key, value in matches:
            key = key.strip()
            value = value.strip()
            # 동일한 키가 이미 존재하면 리스트에 추가
            if key in result:
                if isinstance(result[key], list):
                    result[key].append(value)
                else:
                    result[key] = [result[key], value]
            else:
                result[key] = value
        if result:
            success = True
            for key in result.keys():
                    if key=="selfquestion":
                        if self.N==0:
                            self.selfquestion.append(result['selfquestion'])
                        success = False
                        break
        else:
            success = False
            return result, success    
        return result, success
    
    def get_response(self):
        self.N=0
        for i in range(4):
            print(f"현재 {i+1}번째 시도중입니다.")
            response=self.try_get_response(self.query,i)
            result,success=self.parse_youtuber_output(response)
            self.N+=1
            if self.N==4:
                return [result],[response]
            if success:
                return [result],[response]
            else:
                if result:
                    if len( self.selfquestion)>0:
                        try:
                            print (f'질문 : {result['selfquestion']}')
                            if "answer" in result.keys():
                                print (f'답변 : {result['answer']}')
                            self.selfanswer.append(result['answer'])
                            
                        except Exception as e:
                            self.selfquestion.append(f"오류래 오류.... 대체 뭐야 답변 포멧이 잘못된거야...error:{e}")
                else:
                    self.selfquestion.append("왜 대답이 없어? 답을 해줄래? 진짜 그러다 죽는수가 있어....")
        return [result],[response]

        
        
if __name__ == "__main__":
    input=get_test_dummy()
