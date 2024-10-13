import re

# 예시 기사 본문 (크롤링된 데이터)
article_text = """
인공지능(AI)은 현대 기술의 핵심입니다. 특히 머신러닝(ML)과 딥러닝(DL)은 AI 발전에 중요한 역할을 합니다.
"""

# 용어 데이터베이스 (리스트로 저장)
terms_db = ['인공지능', 'AI', '머신러닝', 'ML', '딥러닝', 'DL']


def replace_terms_with_buttons(article_text, terms_db):
    # 용어들을 길이 순으로 정렬 (긴 용어 먼저 찾아서 대체)
    terms_db = sorted(terms_db, key=len, reverse=True)

    # 본문에서 용어와 일치하는 부분을 버튼으로 대체
    for term in terms_db:
        # 정규식을 이용해 본문에서 일치하는 용어를 버튼으로 감쌈
        article_text = re.sub(f"\\b{re.escape(term)}\\b", f'<button>{term}</button>', article_text)

    return article_text

# 버튼으로 변환된 본문
updated_article_text = replace_terms_with_buttons(article_text, terms_db)

print(updated_article_text)
