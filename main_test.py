import asyncio
from youtube_repoter import test_youtube_main
from review_repoter import test_review_main
from sepcification_repoter import test_sepcification_main
from template_generator import ResultTemplate, Product, Reviews
async def main():
    (youtube,result_y),(rewivew,result_r),(specification,result_s)=await asyncio.gather(
        test_youtube_main(),
        test_review_main(),
        test_sepcification_main(),  
        
    )
    return youtube,result_y,rewivew,result_r,specification,result_s

if __name__ == "__main__":
    generator = ResultTemplate()
    result_dict = generator.dict
    youtube,result_y,rewivew,result_r,specification,result_s=asyncio.run(main())
    youtube.set_value(result_dict)
    rewivew.set_value(result_dict)
    specification.set_value(result_dict)
    print('--------------------------------------------------------------------------------------------')
    print('Final Report')
    import pprint
    pprint.pprint(result_dict, width=150)
