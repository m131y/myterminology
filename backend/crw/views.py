from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import CustomUser
from django.db import connection
from konlpy.tag import Kkma
from konlpy.tag import Okt
from django.contrib.auth.forms import UserCreationForm
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import subprocess
import json
from rest_framework.response import Response
from .models import Search_list
from .models import dict
from .serializers import SearchDataSerializer
from .serializers import dictDataSerializer
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.http import HttpResponse
from newspaper import Article
import random
from .leveling import assign_level_based_on_description

# Create your views here.

@api_view(['GET'])
def get_data(request):
    data = {"message": "Hello from Django!"}
    return Response(data)

def home(request):
    if request.method == 'POST':
        print("posthome")
        user_id = request.session.get('user')
        if user_id:
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM crw_customuser WHERE userid=%s""", [user_id])
            user_data = cursor.fetchone()
            context = {
                'is_logged_in':bool(user_id),
                'username':user_data[8]
            }
            return render(request, 'index.html', context)
        else :
            context = {
                'is_logged_in':bool(user_id),
                'username':None
            }
            return render(request, 'index.html', context) 
    
    if request.method == 'GET':
        print('gethome')
        user_id = request.session.get('user')
        
        if user_id:
            # User is logged in, fetch user data
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM crw_customuser WHERE userid=%s""", [user_id])
            user_data = cursor.fetchone()
            context = {
                'is_logged_in': True,
                'username': user_data[8]
            }
        else:
            # User is not logged in
            context = {
                'is_logged_in': False,
                'username': None
            }
        
        return render(request, 'index.html', context)


def process_login(request):
    if request.method == 'POST':
        user_id = request.session.get('user')
        
        if user_id :
            print('로그인 중입니다.')
            return redirect('index')
        
        else :
            userid = request.POST['userid']
            password = request.POST['password']
            
            print("userid:",userid)
            print("password:",password)

            cursor = connection.cursor()
            query = "SELECT * FROM crw_customuser WHERE userid=%s AND password=%s"
            cursor.execute(query, (userid, password))
            user_data = cursor.fetchone()

            if not user_data:
                error_message = "아이디 또는 비밀번호가 틀렸습니다."
                print(error_message)
                return redirect('login')
            
            else :
                # 사용자를 Django의 User 모델로 변환하여 반환
                print(user_data)
                print("로그인 성공")
                request.session['user'] = userid
                response = home(request)  # Call the second view directly
                return response
    
    else : 
        print("get")
        return redirect('/')


def process_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        userid = request.POST['user_id']
        birth = request.POST['birth']
        password1 = request.POST['pwd1']
        password2 = request.POST['pwd2']
        email = request.POST['email']
        phone = request.POST['phone']

        if password1 != password2:
            messages.error(request, '비밀번호가 맞지않습니다.')
            print("비밀번호 안맞음")
            return redirect('/signup')
        if CustomUser.objects.filter(userid=userid).exists():
            print("이미 ID 있음")
            messages.error(request, '이미 있는 ID입니다..')
            return  redirect('/signup')

        with connection.cursor() as cursor:
            cursor.execute( """
                INSERT INTO crw_customuser (username, userid, birth, password, email, phone)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [username, userid, birth, password1, email, phone])
            print("회원가입완료")
        return redirect('index')  # 회원가입 후 리다이렉트할 URL 설정
    else:
        return redirect('index')

def process_logout(request):
    if request.method == 'GET':
        request.session.flush()
        return redirect('index')
        
    else : 
        print("post")
        return redirect('index')

@api_view(['GET','POST'])
def result(request):
    try:
        # Read the crawled title. If no file is found, output "No title available"
        with open('title.txt', 'r', encoding='utf-8') as title_file:
            title = title_file.read()
    except FileNotFoundError:
        title = "No title available"

    try:
        # Read the crawled body. If no file is found, output "No body available"
        with open('body.txt', 'r', encoding='utf-8') as body_file:
            body = body_file.read()
    except FileNotFoundError:
        body = "No body available"

    # Retrieve data from Search_list and dict tables
    Searchdatas = Search_list.objects.all()
    searchserializer = SearchDataSerializer(Searchdatas, many=True)
    search_list_datas = searchserializer.data

    dictdatas = dict.objects.all()
    dictserializer = dictDataSerializer(dictdatas, many=True)
    dict_datas = dictserializer.data

    added_words = set()
    results = []

    user_id = request.session.get('user')
    user_name = ''
    if user_id :
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM crw_customuser WHERE userid=%s""", [user_id])
        user_data = cursor.fetchone()
        user_level=user_data[14]
        user_name=user_data[8]
    else :
        user_level=0

    # Loop through dict and search_list to match words and include additional fields
    for dict_data in dict_datas:
        for search_list_data in search_list_datas:
            if search_list_data['search_word'] == dict_data['title']:
                if search_list_data['search_word'] not in added_words:
                    # Append matching results along with additional fields from dict_data
                    results.append({
                        'word': search_list_data['search_word'],
                        'description': dict_data['description'] or '',
                        'description2': dict_data.get('description2', '') or '',   # Add description2
                        'original_word': dict_data.get('original_word', '') or '', # Add original_word
                        'korean_word': dict_data.get('korean_word', '') or '',     # Add korean_word
                        'synonym': dict_data.get('synonym', '') or '',             # Add synonym
                        'translations': dict_data.get('translations', '') or '',
                        'word_level': dict_data.get('word_level', '')    # Add translations
                    })
                    added_words.add(search_list_data['search_word'])

    # Context data to be passed to the template
    context = {
        'title': title,
        'body': body,
        'user_level': user_level,
        'is_logged_in':bool(user_id),
        'username':user_name,
        'results_json': json.dumps(results, ensure_ascii=False)
    }
    print(context)
    # Render the data to the news.html template
    return render(request, 'news.html', context)



@csrf_exempt  # To bypass CSRF token requirement for demonstration purposes
@require_POST  # Ensure this view only responds to POST requests
def process_news(request):
    url = request.POST.get('url')  # Retrieve the URL from the POST request
    
    if url:
        # Logic to process the URL (you can add your custom scraping or URL processing logic here)
        # For now, let's just return a success message
        subprocess.run(['C:/Users/whals/myterminology/myvenv/Scripts/python', 'crw.py', url])
        with open("body.txt", 'r',encoding="utf-8") as f1 :
            data = f1.read()

            kkma = Kkma()
            okt = Okt()

            kor_text = data
            kkma_list = kkma.pos(kor_text)
            okt_list = okt.phrases(kor_text)

            i=0

            valid_tags = ['XR', 'NNG', 'NNB', 'NNM', 'NNP', 'NP', 'VV', 'VA', 'OL', 'OH', 'UN']

            kkma_words = set([text[0] for text in kkma_list if text[1] in valid_tags])

            with connection.cursor() as cursor:
                cursor.execute("""DELETE FROM search_list""")

            for text in kkma_list:
                tag = text[1]  # POS tag is in the second element
                if tag in valid_tags:
                    i += 1
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO search_list (id, search_word, search_pos)
                            VALUES (%s, %s, %s)
                            """, [i, text[0], tag])

            for phrase in okt_list:
                if phrase not in kkma_words:  # Only insert if not in Kkma list
                    i += 1
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO search_list (id, search_word)
                            VALUES (%s, %s)
                            """, [i, phrase])
                        
            f1.close()

        response = result(request)  # Call the second view directly
        return response
    return JsonResponse({"success": False, "message": "No URL provided"})

@csrf_exempt  # To bypass CSRF token requirement for demonstration purposes
@require_POST  # Ensure this view only responds to POST requests
def leveling(request):
    url = request.POST.get('url')
    subprocess.run(['C:/Users/whals/myterminology/myvenv/Scripts/python', 'crw.py', url])

    return



def test(request):
    # Fetch 3 random problems for each word level from the database, including description2
    problems_by_level = {}
    for level in range(1, 6):  # Levels 1 to 5
        problems_by_level[level] = list(dict.objects.filter(word_level=level).order_by('?')[:3].values('title', 'description', 'description2', 'word_level'))

    # Combine all levels' problems into one list
    all_problems = [problem for level_problems in problems_by_level.values() for problem in level_problems]

    # Initialize session variables if it's the first time
    if 'current_problem' not in request.session:
        request.session['current_problem'] = 0  # Start at the first problem
        request.session['score'] = 0  # Track correct answers
        request.session['user_answers'] = []  # Track user answers
        request.session['problem_descriptions'] = []  # Track descriptions (both description and description2)
        request.session['shown_problems'] = []  # Track indices of shown problems

    if request.method == "POST":
        user_answer = request.POST.get("option")
        correct_answer = request.session.get("selected_term")

        if user_answer and user_answer == correct_answer:
            request.session['score'] += 1  # Increment the score for correct answers

        # Store both descriptions (description and description2) in session data
        request.session['user_answers'].append(user_answer)
        request.session['problem_descriptions'].append({
            'description': request.session.get('selected_description'),
            'description2': request.session.get('selected_description2')
        })

        request.session['current_problem'] += 1

        # Check if all problems have been solved (15 total problems, 3 per level)
        if request.session['current_problem'] >= 15:
            # Clear session data after 15 problems
            del request.session['current_problem']
            del request.session['score']
            del request.session['user_answers']
            del request.session['problem_descriptions']
            del request.session['shown_problems']

            return render(request, 'usertest.html', {'show_popup': True})

    # Get the current problem number
    current_problem = request.session['current_problem']

    # Select the next problem that has not been shown yet
    available_indices = [i for i in range(len(all_problems)) if i not in request.session['shown_problems']]

    if available_indices:
        index = random.choice(available_indices)
        request.session['shown_problems'].append(index)  # Track that this problem was shown
    else:
        index = random.randint(0, len(all_problems) - 1)  # Fallback, should not happen if logic is correct

    # Get the selected problem data
    selected_term = all_problems[index]['title']
    selected_description = all_problems[index]['description']
    selected_description2 = all_problems[index].get('description2', '') or ''  # Ensure empty string if description2 is missing
    selected_level = all_problems[index]['word_level']

    # Select 3 random incorrect answers
    incorrect_answers = random.sample([problem['title'] for i, problem in enumerate(all_problems) if i != index], 3)
    options = incorrect_answers + [selected_term]
    random.shuffle(options)

    # Store the correct answer, description, and description2 in the session
    request.session['selected_term'] = selected_term
    request.session['selected_description'] = selected_description
    request.session['selected_description2'] = selected_description2

    # Combine descriptions for display
    combined_description = f"{selected_description} {selected_description2}".strip()  # Remove trailing space if description2 is empty

    user_id = request.session.get('user')
    if user_id :
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM crw_customuser WHERE userid=%s""", [user_id])
        user_data = cursor.fetchone()
        user_name = user_data[8]
    else :
        user_name = ''

    # Context data to be passed to the template
    context = {
        'description': combined_description,  # Combine description and description2
        'options': options,
        'word_level': selected_level,
        'current_problem': current_problem + 1,  # Display the current problem number (1-based)
        'total_problems': 15,  # Total number of problems (15)
        'show_popup': False,  # Do not show the popup by default
        'is_logged_in': bool(user_id),  # True if the user is logged in
        'username': user_name  # Pass the username if logged in
    }

    return render(request, 'usertest.html', context)
