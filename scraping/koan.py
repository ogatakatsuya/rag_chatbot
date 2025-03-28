from time import sleep

from extract import create_df, extract_syallabus, extract_total_results, save_df
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

from lib.env import env


def collecting_syllabus(driver, data, current_count):
    is_finish = False

    # リンクをクリック（リンクテキストで検索）
    link = driver.find_element(By.LINK_TEXT, "基礎工学部全授業シラバス")
    link.click()

    # 新しいタブに切り替え
    driver.switch_to.window(driver.window_handles[1])
    # 必要なら、遷移後の処理を追加
    sleep(5)

    # 開講所属のラジオボタンを押す
    radio_button = driver.find_element(By.ID, "categoryFlg2")
    radio_button.click()

    sleep(3)

    # `select` 要素を取得
    select_element = driver.find_element(By.ID, "jShozokuCodeMajor")

    # Selectオブジェクトを作成
    select = Select(select_element)

    # 「基礎工学部」を選択（value="09"）
    select.select_by_value("09")

    sleep(3)

    search_button = driver.find_element(By.CSS_SELECTOR, "input[value=' 検索 ']")

    # ボタンをクリック
    search_button.click()

    sleep(8)

    # 全部で何件あるかを取得
    result_table = driver.find_element(
        By.XPATH, "/html/body/div[2]/div[1]/table/tbody/tr/td[4]"
    )

    total_results = extract_total_results(result_table.get_attribute("innerHTML"))
    print(total_results)

    # ページのボタンを押す
    page = current_count // 100 + 1

    if page > 1:
        page_buton = driver.find_element(By.LINK_TEXT, f"{page}")
        page_buton.click()

    sleep(5)

    count = 0

    # 検索結果のテーブルを取得
    table = driver.find_element(By.CSS_SELECTOR, "table.normal")
    rows = table.find_elements(By.TAG_NAME, "tr")

    row_idx = current_count % 100 + 1

    for row in rows[row_idx:]:
        japanese_button = row.find_element(By.CSS_SELECTOR, 'input[value="和文"]')
        japanese_button.click()
        sleep(2)
        # 現在のウィンドウを取得
        original_window = driver.current_window_handle

        # 新しいウィンドウに切り替え
        driver.switch_to.window(driver.window_handles[2])

        # シラバスの情報を抽出
        syllabus_html = driver.page_source
        data = extract_syallabus(syllabus_html, data)

        # ウィンドウを閉じる
        driver.close()

        # 元のウィンドウに戻る
        driver.switch_to.window(original_window)

        count += 1
        current_count += 1
        print(f"{current_count}/{total_results}件目のシラバスを取得しました")
        if current_count % 50 == 0:
            break
        if current_count == total_results:
            is_finish = True
            break

    driver.close()

    return data, current_count, is_finish


if __name__ == "__main__":
    data = create_df()

    # ChromeDriver のパス
    chrome_driver_path = env.CHROME_DRIVER_PATH

    # Chromeのオプションを設定
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")  # シークレットモード

    # Service オブジェクトを作成
    service = Service(chrome_driver_path)

    # WebDriver を起動
    driver = webdriver.Chrome(service=service, options=options)

    wait = WebDriverWait(driver, 10)

    url = "https://www.es.osaka-u.ac.jp/ja/student/school-of-engineering-science/curriculum/"
    driver.get(url)
    sleep(3)

    # 基礎工のタブを保存
    kisokou_window = driver.current_window_handle

    is_finish = False
    current_count = 0

    while not is_finish:
        # シラバス取得
        data, current_count, is_finish = collecting_syllabus(
            driver, data, current_count
        )
        driver.switch_to.window(kisokou_window)

    # データフレームをCSVファイルに保存
    save_df(data)

    # ブラウザを閉じる
    driver.quit()
