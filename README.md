# 템플릿 제너레이터 모듈 (template_generator.py)

이 모듈은 제품 정보, 리뷰, 구매 정보 등을 계층적으로 구성된 딕셔너리 형태로 만들어 주는 역할을 합니다. 내부적으로 미리 정의된 템플릿 구조를 사용하며, 사용자는 아래의 세 가지 주요 클래스만 이용하면 됩니다.

---
# 입력 변수 및 데이터 매핑

아래는 `Product`, `Reviews`, `Purchase_Info_Stores` 클래스에서 사용되는 주요 입력 변수와 실제 입력해야 하는 값들의 관계를 정리한 테이블입니다.

---

## 📌 Product 클래스

| 입력 변수명 | 설명 | 입력 예시 |
|------------|------|----------|
| `recommendation.name` | 제품 이름 | `"아이패드 에어 4세대"` |
| `recommendation.category` | 제품 카테고리 | `"태블릿"` |
| `recommendation.main_reason` | 주요 추천 이유 | `"가격대비 성능이 우수"` |
| `recommendation.sub_reason` | 부가적인 추천 이유 | `"디자인이 예쁘고 성능이 좋음"` |
| `recommendation.good_person` | 추천 대상 리스트 | `["영상 감상을 좋아하는 사람", "멀티태스킹을 자주 하는 사람"]` |
| `recommendation.bad_person` | 추천하지 않는 대상 리스트 | `["저가형 태블릿을 찾는 사람", "가격이 민감한 사람"]` |

### 🔹 Specifications (제품 사양)

| 입력 변수명 | 설명 | 입력 예시 |
|------------|------|----------|
| `display.size` | 디스플레이 크기 | `"10.9인치"` |
| `display.resolution` | 해상도 | `"2360 x 1640"` |
| `display.refresh_rate` | 주사율 | `"60Hz"` |
| `display.description` | 디스플레이 설명 | `"고화질 영상 감상에 적합"` |
| `processor.model` | 프로세서 모델명 | `"Apple A14 Bionic"` |
| `processor.equivalent` | 동급 성능의 기기 | `"아이폰 12 등급"` |
| `processor.description` | 프로세서 설명 | `"일반적인 웹서핑 및 멀티태스킹에 충분"` |
| `storage.options` | 저장 옵션 | `["64GB"]` |
| `storage.expandable` | 확장 가능 여부 | `"128GB 옵션 없음"` |
| `storage.description` | 저장소 설명 | `"기본 사용에는 충분하지만 대용량 저장에는 한계"` |
| `battery.capacity` | 배터리 용량 | `"최대 10시간 사용 가능"` |
| `battery.description` | 배터리 설명 | `"일반적인 사용에는 문제없음"` |
| `design.features` | 디자인 특징 | `["베젤 축소", "홈 버튼 제거", "지문 인식 탑재"]` |
| `design.description` | 디자인 설명 | `"깔끔하고 현대적인 디자인"` |
| `color_options.color_options` | 색상 옵션 | `["블루", "핑크", "옐로우", "실버"]` |
| `pencil_support.supported` | 지원되는 펜슬 | `"애플펜슬 1세대"` |
| `pencil_support.charging` | 충전 방식 | `"번거로운 충전 방식 (별매)"` |
| `pencil_support.description` | 펜슬 관련 설명 | `"필기 및 그릴 작업에 적합"` |
| `charging_port.type` | 충전 포트 타입 | `"USB-C"` |
| `charging_port.limitation` | 충전 포트 제한 사항 | `"라이트닝 미지원"` |
| `charging_port.description` | 충전 포트 설명 | `"기존 아이폰 충전기 사용 불가, 데이터 전송 속도 제한"` |
---

## 📌 Reviews 클래스

### 🔹 유튜버 리뷰 (`youtuber`)

| 입력 변수명 | 설명 | 입력 예시 |
|------------|------|----------|
| `youtuber.name` | 유튜버 이름 | `"UNDERkg"` |
| `youtuber.subscribers` | 구독자 수 | `"78.8만 명"` |
| `youtuber.title` | 리뷰 영상 제목 | `"끊이지 않는 마진, 아이패드 (10세대) 리뷰"` |
| `youtuber.views` | 조회수 | `"46만 회"` |
| `youtuber.time_since_upload` | 업로드 이후 시간 | `"2년 전"` |
| `youtuber.timestamp{number}` | 하이라이트 타임스탬프 1~6 | `"0:31"` |
| `youtuber.timestamp{number}_description` | 타임스탬프 1~6 설명 | `"디자인 및 외관 설명"` |
| `youtuber.opinion` | 유튜버 최종 의견 | `"추천하지 않음"` |
| `youtuber.opinion_reason` | 추천 또는 비추천 이유 | `"디자인은 좋으나, 가격이 너무 올라감"` |
| `youtuber.pros` | 장점 리스트 | `["새로운 디자인", "USB-C 도입"]` |
| `youtuber.cons` | 단점 리스트 | `["애플펜슬 1세대 지원", "가격 상승"]` |
| `youtuber.link` | 리뷰 영상 링크 | `"https://www.youtube.com/watch?v=1"` |

### 🔹 일반 사용자 리뷰 (`general_users`)

| 입력 변수명 | 설명 | 입력 예시 |
|------------|------|----------|
| `general_users.total_reviews` | 총 리뷰 개수 | `1363` |
| `general_users.positive_percentage` | 긍정 리뷰 비율 | `"76%"` |
| `general_users.negative_percentage` | 부정 리뷰 비율 | `"24%"` |
| `general_users.positive_reviews` | 긍정적인 리뷰 예시 | `["디자인 예뻐요", "영상 볼 때 최고", "배터리 오래가요"]` |
| `general_users.negative_reviews` | 부정적인 리뷰 예시 | `["애플펜슬 문제", "가격 비쌈", "주사율 아쉬움"]` |
| `general_users.user_comments` | 실제 사용자 댓글 | `[{"user": "user1", "comment": "디자인은 예쁜데 가격이 너무 높아요."}]` |

---

## 📌 Purchase_Info_Stores 클래스

| 입력 변수명 | 설명 | 입력 예시 |
|------------|------|----------|
| `site` | 판매 사이트 | `"쿠팡"` |
| `option` | 제품 옵션 | `"블루, 64GB, Wi-Fi"` |
| `price` | 가격 | `"508,880원"` |
| `purchase_link` | 구매 링크 | `"https://www.cupang.com/"` |
| `rating` | 판매처 평점 | `5.0` |

---

## 📌 정리

- **모든 입력 데이터는 각 클래스의 인스턴스 속성에 직접 할당**하여 사용합니다.
- **set_value(result_dict)** 메서드는 내부적으로 템플릿을 갱신하며, 사용자는 반드시 호출할 필요가 없습니다.
- **최종적으로 포맷팅된 데이터만 반환받아 사용하면 됩니다.**

이 테이블을 참고하여, 필요한 데이터를 각 클래스의 변수에 맞춰 입력하면 쉽게 활용할 수 있습니다. 🚀




---

## 주요 클래스

- **Product**  
  제품의 추천 정보와 세부 사양(디스플레이, 프로세서, 저장소, 배터리, 디자인, 색상 옵션, 펜슬 지원, 충전 포트 등)을 다룹니다.

- **Reviews**  
  유튜버 리뷰와 일반 사용자 리뷰를 각각 관리합니다.

- **Purchase_Info_Stores**  
  제품을 구매할 수 있는 스토어 정보를 관리합니다.

> **참고:**  
> 실제 데이터 입력 시, 각 클래스의 인스턴스에 직접 속성 값을 할당한 후, 내부적으로 `set_value()` 메서드를 통해 결과 딕셔너리에 반영합니다. 예시 코드에서는 각 객체에서 `set_value(result_dict)`를 호출하는 모습이 보이지만, 여러분은 해당 데이터를 바로 전달할 수도 있으며, 최종적으로 포맷팅된 결과만 받으면 됩니다.





---

## 동작 방식

1. **템플릿 생성**  
   - `ResultTemplate` 클래스를 이용해 미리 정의된 기본 템플릿(중첩 딕셔너리)을 생성합니다.
   - 이 템플릿은 제품 정보, 리뷰, 구매 정보에 필요한 모든 키와 구조를 포함하고 있습니다.

2. **데이터 입력**  
   - 사용자는 `Product`, `Reviews`, `Purchase_Info_Stores` 클래스의 인스턴스를 생성하여 필요한 데이터를 입력합니다.
   - 각 인스턴스는 내부적으로 `show()` 메서드를 제공해 간략한 속성 목록을 확인할 수 있습니다.

3. **데이터 포맷팅**  
   - 입력한 데이터를 `set_value(result_dict)` 메서드를 통해 템플릿에 반영합니다.
   - 이 과정은 내부적으로 데이터를 최종 딕셔너리 구조에 맞게 업데이트하는 역할을 합니다.
   - 예시 코드에서는 각 데이터 항목에 대해 `set_value()` 호출이 있지만, 별도의 파이썬 파일에 샘플 코드가 있으므로 복잡한 호출 없이도 데이터를 전달할 수 있음을 상기해 주세요.

4. **최종 결과**  
   - 모든 데이터를 반영한 후, 최종적으로 포맷팅된 결과 딕셔너리를 사용해 원하는 후처리나 저장, 전송을 진행할 수 있습니다.

---

## 사용 예시 (간략 예시)

```python
from template_generator import ResultTemplate, Product, Reviews, Purchase_Info_Stores
import pprint

# 템플릿 생성
generator = ResultTemplate()
result_dict = generator.dict

# Product 인스턴스 생성 및 데이터 할당
item_product = Product()
item_product.recommendation.name = "아이패드 에어 4세대"
item_product.recommendation.category = "태블릿"
item_product.recommendation.main_reason = "가격대비 성능이 우수"
item_product.recommendation.sub_reason = "디자인이 예쁘고 성능이 좋음"
item_product.recommendation.good_person = ["영상 감상을 좋아하는 사람", "멀티태스킹을 자주 하는 사람"]
item_product.recommendation.bad_person = ["저가형 태블릿을 찾는 사람", "가격이 민감한 사람"]
# ... (나머지 사양 데이터도 할당)

# Reviews 인스턴스 생성 및 데이터 할당
item_review = Reviews()
item_review.youtuber.name = "UNDERkg"
item_review.youtuber.subscribers = "78.8만 명"
# ... (나머지 리뷰 데이터도 할당)

# Purchase_Info_Stores 인스턴스 생성 및 데이터 할당
stores = Purchase_Info_Stores()
stores.site = "쿠팡"
stores.option = "블루, 64GB, Wi-Fi"
stores.price = "508,880원"
stores.purchase_link = "https://www.cupang.com/"
stores.rating = 5.0

# 각 인스턴스의 데이터를 템플릿에 반영 (내부적으로 set_value() 호출)
# 실제 사용 시, 각 데이터 항목을 입력받은 후 최종적으로 포맷팅된 딕셔너리만 전달받으면 됩니다.

# 결과 출력
pprint.pprint(result_dict, width=150)



