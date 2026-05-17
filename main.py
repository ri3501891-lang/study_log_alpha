import json
from pathlib import Path
from datetime import date

LOG_FILE = Path("logs.json")


def load_logs():
    if not LOG_FILE.exists():
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_logs(logs):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


def get_next_id(logs):
    if not logs:
        return 1
    return max(log["id"] for log in logs) + 1


def add_log():
    logs = load_logs()
    today = date.today().isoformat()

    print(f"今日の日付: {today}")
    date_input = input("日付を入力してください（Enterで今日の日付を使用）: ").strip()
    log_date = date_input if date_input else today

    subject = input("教科を入力してください: ").strip()
    study_time = input("勉強時間を入力してください（分）: ").strip()
    memo = input("メモを入力してください: ").strip()

    if not subject or not study_time:
        print("教科・勉強時間は必須です。")
        return

    if not study_time.isdigit():
        print("勉強時間は数字で入力してください。")
        return

    new_log = {
        "id": get_next_id(logs),
        "date": log_date,
        "subject": subject,
        "study_time": int(study_time),
        "memo": memo,
    }

    logs.append(new_log)
    save_logs(logs)
    print("学習記録を追加しました。")


def show_logs():
    logs = load_logs()
    if not logs:
        print("学習記録がありません。")
        return

    print("\n--- 学習記録一覧 ---")
    for log in logs:
        print(xx
            f"ID: {log['id']} | 日付: {log['date']} | 教科: {log['subject']} | "
            f"勉強時間: {log['study_time']}分 | メモ: {log['memo']}"
        )


def delete_log():
    logs = load_logs()
    if not logs:
        print("削除できる学習記録がありません。")
        return

    show_logs()
    delete_id = input("削除するIDを入力してください: ").strip()

    if not delete_id.isdigit():
        print("IDは数字で入力してください。")
        return

    delete_id = int(delete_id)
    new_logs = [log for log in logs if log["id"] != delete_id]

    if len(new_logs) == len(logs):
        print("該当するIDが見つかりません。")
        return

    save_logs(new_logs)
    print("学習記録を削除しました。")


def show_total_time_by_subject():
    logs = load_logs()
    if not logs:
        print("学習記録がありません。")
        return

    totals = {}
    for log in logs:
        subject = log["subject"]
        totals[subject] = totals.get(subject, 0) + log["study_time"]

    print("\n--- 教科ごとの総勉強時間 ---")
    for subject, total in totals.items():
        print(f"{subject}: {total}分")


def show_total_time_by_day():
    logs = load_logs()
    if not logs:
        print("学習記録がありません。")
        return

    totals = {}
    for log in logs:
        log_date = log["date"]
        totals[log_date] = totals.get(log_date, 0) + log["study_time"]

    print("\n--- 毎日の総勉強時間 ---")
    for log_date, total in sorted(totals.items()):
        print(f"{log_date}: {total}分")


def evaluate_today_study():
    logs = load_logs()
    if not logs:
        print("学習記録がありません。")
        return

    today = date.today().isoformat()
    total_today = 0

    for log in logs:
        if log["date"] == today:
            total_today += log["study_time"]

    print(f"\n--- 今日の勉強時間評価 ({today}) ---")
    print(f"今日の総勉強時間: {total_today}分")

    if total_today == 0:
        print("今日はまだ勉強記録がありません。")
    elif total_today <= 60:
        print("もう少し勉強しましょう。")
    else:
        print("よくできました！")


def main():
    while True:
        print("\n=== 学習ログアプリ ===")
        print("1. 学習記録を追加")
        print("2. 学習記録を一覧表示")
        print("3. 学習記録を削除")
        print("4. 教科ごとの総勉強時間を表示")
        print("5. 毎日の総勉強時間を表示")
        print("6. 今日の勉強時間の評価を表示")
        print("7. 終了")

        choice = input("メニューを選んでください (1-7): ").strip()

        if choice == "1":
            add_log()
        elif choice == "2":
            show_logs()
        elif choice == "3":
            delete_log()
        elif choice == "4":
            show_total_time_by_subject()
        elif choice == "5":
            show_total_time_by_day()
        elif choice == "6":
            evaluate_today_study()
        elif choice == "7":
            print("アプリを終了します。")
            break
        else:
            print("1〜7の数字を入力してください。")


if __name__ == "__main__":
    main()