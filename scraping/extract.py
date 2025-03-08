from bs4 import BeautifulSoup
import re
import pandas as pd

folder = './syllabus/'

info_tytles = {
    '時間割コード／Course Code': 'course_code',
    '開講区分(開講学期)／Semester': 'semester',
    '曜日・時間／Day and Period': 'day_and_period',
    '開講科目名／Course Name (Japanese)': 'course_name_jp',
    '定員／Capacity': 'capacity',
    '授業形態／Type of Class': 'type_of_class',
    '単位数／Credits': 'credits',
    '年次／Student Year': 'student_year',
    '担当教員／Instructor': 'instructor',
    'メディア授業科目／Course of Media Class': 'course_of_media_class',
    '授業サブタイトル／Course Subtitle': 'course_subtitle',
    '開講言語／Language of the Course': 'language_of_the_course',
    '学習方法／Learning Methods': 'learning_methods',
    '授業の目的と概要／Course Objectives': 'course_objectives',
    '学習目標／Learning Goals': 'learning_goals',
    '履修条件・受講条件／Requirements, Prerequisites': 'requirements_prerequisites',
    '出欠席及び受講に関するルール／Attendance and Student Conduct Policy': 'attendance_and_student_conduct_policy',
    '授業計画／Class Plan': 'class_plan',
    '教科書・指定教材／Textbooks': 'textbooks',
    '参考図書・参考教材／Reference': 'reference',
    '成績評価／Grading Policy※学習目標の番号にカーソルをあてると、その学習目標の全文が表示されます。': 'grading_policy',
    '成績評価に関する補足情報／Additional Information on Grading': 'additional_information_on_grading',
    '特記事項／Special Note': 'special_note',
    'オフィスアワー／Office Hours': 'office_hours',
    '実務経験のある教員による授業科目／Course Conducted by Instructors with Practical Experience': 'course_conducted_by_instructors_with_practical_experience',
}

# データフレームを作成
def create_df():
    df = pd.DataFrame([], columns=info_tytles.values())
    return df

# シラバスの情報を抽出
def extract_syallabus(html_content, df):
    soup = BeautifulSoup(html_content, 'html.parser')

    tables = soup.find_all('table', class_="syllabus-frame")
    course_info = {}
    
    for table in tables:
        if not table:
            print('シラバスの表が見つかりませんでした')
            exit()

        for row in table.find_all('tr'):
            th = row.find('th')
            td = row.find('td')

            if th and td:
                key = th.get_text(strip=True)
                value = td.get_text(strip=True)
                if key in info_tytles:
                    course_info[info_tytles[key]] = value

    # シラバスの情報をデータフレームに変換
    new_row = pd.Series(course_info)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    return df

#csv ファイルに保存
def save_df(df):
    df.to_csv(folder + 'syllabus.csv', index=False)

# HTMLコンテンツから検索結果の総数を抽出
def extract_total_results(html_content):
    """Extracts the total number of search results from the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # ページ内の全テキストを取得
    text = soup.get_text()
    
    # 正規表現で「全部で XXX件あります」を検索
    match = re.search(r'全部で (\d+)件あります', text)
    if match:
        return int(match.group(1))
    
    return None  # マッチしなかった場合


if __name__ == '__main__':
    df = create_df()

    for i in range(1, 3):
        with open(folder + f'syllabus.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
            df = extract_syallabus(html_content, df)

    print(df)
    save_df(df)


