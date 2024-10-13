import re

# 전문 용어 리스트
technical_terms = ["전기 통신망", "PC", "인공지능", "IPTV", "OTT", "메타버스", "단통법", "가상현실", "가상세계", "디지털 콘텐츠", "마이크로프로세서"]

# 설명 내 전문 용어 수를 카운트
def count_technical_terms(description, technical_terms):
    count = 0
    if description:
        for term in technical_terms:
            count += description.count(term)  # 용어가 몇 번 나오는지 카운트
    return count

# 설명 복잡성 측정 (문장의 길이, 단어 다양성 등)
def measure_complexity(description):
    words = re.findall(r'\w+', description)
    unique_words = set(words)
    
    # 설명의 길이 (단어 수)와 단어 다양성 측정
    description_length = len(words)
    word_diversity = len(unique_words) / description_length if description_length > 0 else 0
    
    # 설명의 길이가 너무 길거나 단어 다양성이 높으면 상한을 둠
    if description_length > 100:
        description_length = 100  # 상한 설정 (100 단어 이상일 경우)
    
    complexity_score = description_length * word_diversity
    return complexity_score

# 용어에 대해 복잡성 및 전문 용어 밀도를 측정하여 레벨링
def assign_level_based_on_description(terms, descriptions, technical_terms):
    term_levels = {}
    
    for term, description in zip(terms, descriptions):
        # 전문 용어 수와 밀도 계산
        term_count = count_technical_terms(description, technical_terms)
        term_density = term_count / len(description.split()) if len(description.split()) > 0 else 0
        
        # 설명 복잡성
        complexity_score = measure_complexity(description)
        
        # 전문 용어 밀도의 상한 설정 (0.2 이상이면 더 이상 증가하지 않음)
        if term_density > 0.2:
            term_density = 0.2
        
        # 설명 복잡성 점수와 전문 용어 밀도를 결합한 최종 점수 계산
        final_score = (term_density * 0.4) + (complexity_score * 0.6)
        
        # 점수 기준으로 레벨 설정 (레벨링 기준을 더 세분화)
        if final_score < 2:
            term_levels[term] = 1  # 초급
        elif final_score < 5:
            term_levels[term] = 2  # 기초
        elif final_score < 8:
            term_levels[term] = 3  # 중급
        elif final_score < 11:
            term_levels[term] = 4  # 상급
        else:
            term_levels[term] = 5  # 전문가
    
    return term_levels

# 예시 용어 및 설명
terms = ["전기 통신망", "PC", "인공지능", "IPTV", "OTT", "메타버스", "단통법", "가상현실", "가상세계", "디지털 콘텐츠", "마이크로프로세서"]
descriptions = [
    "정보의 전달 매체인 전기 신호 또는 광신호의 전송에 필요한 각종 구성 요소가 공간적으로 어떤 질서에 따라 배치되어 있는 체계. 의사 정보의 발원에서 착원에 이르는 회선을 가장 유리하게 선택하여 접속하는 변환 동작이 필요하다.",
    "가정이나 사무실 등에서 개인 전용으로 사용되는 컴퓨터. 개인용 컴퓨터(PC: Personal Computer)는 마이크로프로세서(microprocessor)를 사용하여 제작된 컴퓨터라는 의미에서 마이크로컴퓨터(microcomputer)라고도 하고, 책상 위에 올려놓는다는 의미에서 데스크톱 컴퓨터(desktop computer)라고도 한다.",
    "인간의 인지, 추론, 학습, 판단 등의 사고과정에 필요한 능력을 컴퓨터 시스템을 통해 구현함으로써 문제를 해결하는 기술",
    "IPTV는 인터넷 프로토콜 TV로, 인터넷으로 실시간 방송과 VOD를 볼 수 있는 서비스",
    "over the top의 줄임말, over the top : 셋톱박스, TV 등 단말기를 넘어서",
    "경제, 사회, 문화 등 우리 삶의 전반적인 부분에서 현실과 비현실(가상)이 모두 공존할 수 있는 3차원의 가상공간. 가상현실을 기반으로 가상세계 안에 현실과 유사한 세계를 구축하고, 사용자가 그 안에서 현실세계와 같은 사회, 경제, 정치 활동을 가능하도록 지원하는 소프트웨어 플랫폼",
    "이동통신단말장치 유통구조 개선에 관한 법률, 스마트폰을 개통할 때 보조금과 관련된 규제내용을 담고 있는 법",
    "인간의 상상에 따른 공간과 사물을 컴퓨터에 가상으로 만들어, 현실 세계에서는 직접 경험하지 못하는 상황을 간접으로 실제처럼 체험할 수 있도록 하는 기술.",
    "컴퓨터로 구현한 현실 세계를 모의(模擬)하는 가상의 생활 환경. 사용자가 물리적으로 존재하지 않는 환경에서 존재감을 느낄 수 있도록 하는 다양한 형태의 디지털 콘텐츠를 포괄적으로 지칭한다.",
    "유무선 전기 통신망에서 사용하기 위해 부호ㆍ문자ㆍ음성ㆍ음향 이미지ㆍ영상 등을 디지털 방식으로 제작ㆍ처리ㆍ유통하는 자료, 정보 등을 말함. 구입에서 결제, 이용까지 모두 네트워크와 PC로 처리하기 때문에 종래의 통신 판매 범위를 초월한 전자 상거래(EC)의 독자적인 분야로서 시장 확대가 급속히 이루어지고 있다.",
    "컴퓨터 시스템에서 기억 장치 이외의 모든 중앙 처리 장치(CPU)의 기능을 대규모 집적 회로(LSI) 칩에 탑재한 것. 복수의 칩으로 된 것과 1개의 칩으로 된 것이 있으나 최근에는 1개의 칩으로 된 것이 대부분이다."
]

# 레벨 계산
levels = assign_level_based_on_description(terms, descriptions, technical_terms)
print(levels)
