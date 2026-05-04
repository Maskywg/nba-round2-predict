import requests

# 第二輪賽果更新腳本
# 手動觸發更新 Firestore game_results/nba_round2
# 欄位：rw0-3（勝隊）, rl0-3（場數）

FIRESTORE_URL = (
    "https://firestore.googleapis.com/v1/projects/"
    "gen-lang-client-0737444461/databases/(default)/"
    "documents/game_results/nba_round2"
)

# 在這裡填入已知賽果（None = 未出爐）
RESULTS = {
    0: {"winner": None, "length": None},  # 雷霆 vs 湖人
    1: {"winner": None, "length": None},  # 灰狼 vs 馬刺
    2: {"winner": None, "length": None},  # 尼克 vs 76人
    3: {"winner": None, "length": None},  # 活塞 vs 騎士
}

def main():
    fields = {}
    mask_parts = []
    for i, r in RESULTS.items():
        fields[f"rw{i}"] = {"stringValue": r["winner"]} if r["winner"] else {"nullValue": None}
        fields[f"rl{i}"] = {"integerValue": str(r["length"])} if r["length"] else {"nullValue": None}
        mask_parts += [f"rw{i}", f"rl{i}"]

    mask = "&".join(f"updateMask.fieldPaths={p}" for p in mask_parts)
    resp = requests.patch(f"{FIRESTORE_URL}?{mask}", json={"fields": fields}, timeout=10)
    if resp.status_code == 200:
        print("✅ Firestore 更新成功")
    else:
        print(f"❌ 更新失敗 {resp.status_code}: {resp.text}")

if __name__ == "__main__":
    main()
