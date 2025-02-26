class TemplateGenerator:
    def __init__(self, template, path=""):
        """
        :param template: 템플릿 딕셔너리 (여기엔 dict, list, 도트표기 문자열, 단순 리터럴 문자열이 섞여 있음)
        :param path: 현재 노드의 경로 (재귀 호출용; 이제는 사용하지 않습니다)
        """
        self._template = template
        self._path = path  # 참고용으로 남겨두지만, 더 이상 접두사로 사용하지 않음
        self._data = {}
        self._build()

    def _build(self):
        for key, value in self._template.items():
            if isinstance(value, dict):
                # 딕셔너리인 경우: 재귀적으로 TemplateGenerator로 처리
                node = TemplateGenerator(value, path="")  # 부모 경로 무시
                setattr(self, key, node)
                self._data[key] = node
            elif isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, dict):
                        new_list.append(TemplateGenerator(item, path=""))
                    elif isinstance(item, str):
                        if "." in item:
                            # 도트표기 문자열 처리: 부모 경로 무시하고, 문자열을 그대로 분리
                            parts = item.split(".")
                            new_list.append(self._create_nested(parts, None))
                        else:
                            # 단순 리터럴 문자열: 해당 문자열 자체를 속성명으로 하는 leaf 생성
                            leaf = type("Leaf", (), {})()
                            setattr(leaf, item, None)
                            new_list.append(leaf)
                    else:
                        new_list.append(item)
                setattr(self, key, new_list)
                self._data[key] = new_list
            elif isinstance(value, str):
                if "." in value:
                    # 도트표기 문자열 처리: 부모 경로 무시하고, 문자열 그대로 분리
                    parts = value.split(".")
                    node = self._create_nested(parts, None)
                    setattr(self, key, node)
                    self._data[key] = node
                else:
                    # 단순 리터럴 문자열: 그 자체를 속성명으로 하는 leaf 생성
                    node = type("Leaf", (), {})()
                    setattr(node, value, None)
                    # 여기서는 템플릿의 key 대신 리터럴 자체를 속성명으로 사용
                    setattr(self, value, node)
                    self._data[value] = node
            else:
                setattr(self, key, value)
                self._data[key] = value

    def _create_nested(self, parts, final_value):
        """
        parts: 도트로 분리된 리스트 (예: ["value"] 또는 ["subkey", "value"])
        final_value: 최종 리프 노드에 들어갈 기본 값 (None)
        입력받은 parts를 그대로 사용해 중첩 객체(leaf, node)를 생성합니다.
        """
        if not parts:
            return final_value
        head = parts[0]
        if len(parts) == 1:
            node = type("Leaf", (), {})()
            setattr(node, head, final_value)
            return node
        else:
            child = self._create_nested(parts[1:], final_value)
            node = type("Node", (), {})()
            setattr(node, head, child)
            return node

    def dict(self):
        """
        객체 내부의 데이터를 재귀적으로 딕셔너리로 변환하여 반환합니다.
        """
        result = {}
        for key, value in self._data.items():
            attr = getattr(self, key)
            if isinstance(attr, TemplateGenerator):
                result[key] = attr.dict()
            elif isinstance(attr, list):
                new_list = []
                for item in attr:
                    if isinstance(item, TemplateGenerator):
                        new_list.append(item.dict())
                    elif self._is_object_with_attrs(item):
                        new_list.append(self._object_to_dict(item))
                    else:
                        new_list.append(item)
                result[key] = new_list
            elif self._is_object_with_attrs(attr):
                result[key] = self._object_to_dict(attr)
            else:
                result[key] = attr
        return result

    def _is_object_with_attrs(self, obj):
        return hasattr(obj, "__dict__") and not isinstance(obj, type)

    def _object_to_dict(self, obj):
        d = {}
        for attr_name, attr_val in obj.__dict__.items():
            if self._is_object_with_attrs(attr_val):
                d[attr_name] = self._object_to_dict(attr_val)
            else:
                d[attr_name] = attr_val
        return d

# ================= 사용 예시 =================

original_structure = {
    "product": {
        "name": None,            
        "category": None,     
        "recommendation": {
            "main_reason": None,
            "sub_reason": None,       
            "good_person": [],         
            "bad_person": []
        },
        "specifications": {
            "display": {
                "size": None,
                "resolution": None,
                "refresh_rate": None,
                "description": None
            },
            "processor": {
                "model": None,
                "equivalent": None,
                "description": None
            },
            "storage": {
                "options": [],
                "expandable": None,
                "description": None
            },
            "battery": {
                "capacity": None,
                "description": None
            },
            "design": {
                "features": [],
                "description": None
            },
            "color_options": [],
            "pencil_support": {
                "supported": None,
                "charging": None,
                "description": None
            },
            "charging_port": {
                "type": None,
                "limitation": None,
                "description": None
            }
        }
    },
    "reviews": {
        "youtuber": {
            "name": None,
            "subscribers": None,
            "review_video": {
                "title": None,
                "views": None,
                "time_since_upload": None,
                "highlight_timestamp": {
                    "timestamp1": None,
                    "timestamp2": None, 
                    "timestamp3": None, 
                    "timestamp4": None, 
                    "timestamp5": None, 
                    "timestamp6": None, 
                }
            },
            "opinion": None,
            "opinion_reason": None,
            "pros": [],
            "cons": []
        },
        "general_users": {
            "total_reviews": None,
            "positive_percentage": None,
            "negative_percentage": None,
            "positive_reviews": [],
            "negative_reviews": [],
            "user_comments": [
                {
                    "user": None,
                    "comment": None
                }
            ]
        }
    },
    "purchase_info": {
        "stores": [
            {
                "site": None,
                "option": None,
                "price": None,
                "purchase_link": None,
                "rating": None
            },
            {
                "site": None,
                "option": None,
                "price": None,
                "purchase_link": None,
                "rating": None
            }
        ]
    }
}


# 템플릿 인스턴스 생성 (미리 정의된 original_structure 사용)
generator = TemplateGenerator(original_structure)

result_dict = generator.dict()
# 직접 딕셔너리 키를 사용하여 값을 채우는 예시

# product
result_dict["product"]["name"] = "애플 아이패드 10세대 Wi-Fi 64GB"
result_dict["product"]["category"] = "태블릿"

result_dict["product"]["recommendation"]["main_reason"] = "적당한 성능과 좋은 디스플레이"
result_dict["product"]["recommendation"]["sub_reason"] = "영상 감상, 웹 서핑, 필기용으로 무난하지만, 저장 공간과 성능이 아쉬움"
result_dict["product"]["recommendation"]["good_person"] = ["필기, 온라인 강의, 웹 서핑용으로 적당함"]
result_dict["product"]["recommendation"]["bad_person"] = ["고사양 작업 필요"]

# specifications > display
result_dict["product"]["specifications"]["display"]["size"] = "10.9인치 Liquid Retina"
result_dict["product"]["specifications"]["display"]["resolution"] = "2160x1620"
result_dict["product"]["specifications"]["display"]["refresh_rate"] = "60Hz"
result_dict["product"]["specifications"]["display"]["description"] = "화면이 크고 선명해 영상 감상에 적합"

# specifications > processor
result_dict["product"]["specifications"]["processor"]["model"] = "Apple A14 Bionic"
result_dict["product"]["specifications"]["processor"]["equivalent"] = "아이폰 12 등급"
result_dict["product"]["specifications"]["processor"]["description"] = "일반적인 웹서핑 및 멀티태스킹에 충분"

# specifications > storage
result_dict["product"]["specifications"]["storage"]["options"] = ["64GB"]
result_dict["product"]["specifications"]["storage"]["expandable"] = "128GB 옵션 없음"
result_dict["product"]["specifications"]["storage"]["description"] = "기본 사용에는 충분하지만 대용량 저장에는 한계"

# specifications > battery
result_dict["product"]["specifications"]["battery"]["capacity"] = "최대 10시간 사용 가능"
result_dict["product"]["specifications"]["battery"]["description"] = "일반적인 사용에는 문제없음"

# specifications > design
result_dict["product"]["specifications"]["design"]["features"] = ["베젤 축소", "홈 버튼 제거", "지문 인식 탑재"]
result_dict["product"]["specifications"]["design"]["description"] = "깔끔하고 현대적인 디자인"

# specifications > color_options
result_dict["product"]["specifications"]["color_options"] = ["블루", "핑크", "옐로우", "실버"]

# specifications > pencil_support
result_dict["product"]["specifications"]["pencil_support"]["supported"] = "애플펜슬 1세대"
result_dict["product"]["specifications"]["pencil_support"]["charging"] = "번거로운 충전 방식 (별매)"
result_dict["product"]["specifications"]["pencil_support"]["description"] = "필기 및 그릴 작업에 적합"

# specifications > charging_port
result_dict["product"]["specifications"]["charging_port"]["type"] = "USB-C"
result_dict["product"]["specifications"]["charging_port"]["limitation"] = "라이트닝 미지원"
result_dict["product"]["specifications"]["charging_port"]["description"] = "기존 아이폰 충전기 사용 불가, 데이터 전송 속도 제한"

# reviews > youtuber
result_dict["reviews"]["youtuber"]["name"] = "UNDERkg"
result_dict["reviews"]["youtuber"]["subscribers"] = "78.8만 명"
result_dict["reviews"]["youtuber"]["review_video"]["title"] = "끊이지 않는 마진, 아이패드 (10세대) 리뷰"
result_dict["reviews"]["youtuber"]["review_video"]["views"] = "46만 회"
result_dict["reviews"]["youtuber"]["review_video"]["time_since_upload"] = "2년 전"
result_dict["reviews"]["youtuber"]["review_video"]["highlight_timestamp"]["timestamp1"] ="0:31"+" : "+"디자인 및 외관 설명"
result_dict["reviews"]["youtuber"]["review_video"]["highlight_timestamp"]["timestamp2"] = "2:46"+" : "+"디스플레이 특징 평가"
result_dict["reviews"]["youtuber"]["review_video"]["highlight_timestamp"]["timestamp3"] = "4:16"+" : "+"프로세서 및 성능 테스트"
result_dict["reviews"]["youtuber"]["review_video"]["highlight_timestamp"]["timestamp4"] = "6:01"+" : "+"배터리 수명 및 충전 포트 변경 사항"
result_dict["reviews"]["youtuber"]["review_video"]["highlight_timestamp"]["timestamp5"] = "7:31"+" : "+"애플펜슬 호환성 평가"
result_dict["reviews"]["youtuber"]["review_video"]["highlight_timestamp"]["timestamp6"] = "9:01"+" : "+"가격 및 총평"
result_dict["reviews"]["youtuber"]["opinion"] = "추천하지 않음"
result_dict["reviews"]["youtuber"]["opinion_reason"] = "디자인은 좋으나, 가격이 너무 올라감"
result_dict["reviews"]["youtuber"]["pros"] = ["새로운 디자인", "USB-C 도입"]
result_dict["reviews"]["youtuber"]["cons"] = ["애플펜슬 1세대 지원", "가격 상승"]

# reviews > general_users
result_dict["reviews"]["general_users"]["total_reviews"] = 1363
result_dict["reviews"]["general_users"]["positive_percentage"] = "76%"
result_dict["reviews"]["general_users"]["negative_percentage"] = "24%"
result_dict["reviews"]["general_users"]["positive_reviews"] = [
    "디자인 예뻐요",
    "영상 볼 때 최고",
    "배터리 오래가요",
    "USB-C 편리",
    "기본 성능 좋음"
]
result_dict["reviews"]["general_users"]["negative_reviews"] = [
    "애플펜슬 문제",
    "가격 비쌈",
    "주사율 아쉬움",
    "포지션 애매"
]
result_dict["reviews"]["general_users"]["user_comments"] = [
    {"user": "user1", "comment": "디자인은 예쁜데 가격이 너무 높아요."},
    {"user": "user2", "comment": "영상 볼 때 좋고 배터리도 오래가요."},
    {"user": "user3", "comment": "저장 공간이 부족해요."}
]

# purchase_info > stores
result_dict["purchase_info"]["stores"] = [
    {
        "site": "쿠팡",
        "option": "블루, 64GB, Wi-Fi",
        "price": "508,880원",
        "purchase_link": "https://www.coupang.com/",
        "rating": 5.0
    },
    {
        "site": "쿠팡",
        "option": "블루, 64GB, Wi-Fi",
        "price": "508,880원",
        "purchase_link": "https://www.coupang.com/",
        "rating": 5.0
    }
]
import pprint
pprint.pprint(result_dict, width=150)
