import csv
import html
import os
from pathlib import Path
from grades import average, grade, pass_rate

OUTPUT_DIR = Path("_site")


def load_scores(csv_path):
    """อ่านไฟล์ CSV คืนค่าเป็น list ของ (ชื่อ, คะแนน) พร้อมตรวจความถูกต้อง"""
    seen_names = set()
    result = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"].strip()
            if not name:
                raise ValueError("ชื่อต้องไม่เป็นค่าว่าง")
            if name in seen_names:
                raise ValueError(f"พบชื่อซ้ำในระบบ: {name}")
            seen_names.add(name)
            score = int(row["score"])
            if not 0 <= score <= 100:
                raise ValueError(f"คะแนนต้องอยู่ระหว่าง 0-100: {score}")
            result.append((name, score))
    return result


def render_html(rows, title):
    """สร้างหน้าเว็บ HTML จากข้อมูลคะแนน"""
    table_rows = "\n".join(
        f"      <tr><td>{html.escape(name)}</td><td>{score}</td><td>{grade(score)}</td></tr>"
        for name, score in rows
    )
    scores = [score for _, score in rows]
    avg = average(scores)
    max_score = max(scores) if scores else 0
    min_score = min(scores) if scores else 0
    rate = pass_rate(scores)

    return f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      margin: 2rem auto;
      max-width: 700px;
      padding: 0 1rem;
      background-color: #f8fafc;
      color: #1e293b;
    }}
    h1 {{
      color: #0f172a;
      border-bottom: 2px solid #3b82f6;
      padding-bottom: 0.5rem;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 1.5rem;
      background: white;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      border-radius: 8px;
      overflow: hidden;
    }}
    th, td {{
      padding: 12px 16px;
      text-align: left;
      border-bottom: 1px solid #e2e8f0;
    }}
    th {{
      background-color: #3b82f6;
      color: white;
      font-weight: 600;
    }}
    tr:last-child td {{
      border-bottom: none;
    }}
    tr:hover {{
      background-color: #f1f5f9;
    }}
    .stats-card {{
      margin-top: 1.5rem;
      padding: 1rem 1.5rem;
      background: white;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    .stats-card p {{
      margin: 0.5rem 0;
      font-size: 1.05rem;
    }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <table>
    <tr><th>ชื่อ</th><th>คะแนน</th><th>เกรด</th></tr>
{table_rows}
  </table>
  <div class="stats-card">
    <p>ค่าเฉลี่ย: {avg}</p>
    <p>คะแนนสูงสุด: {max_score}</p>
    <p>คะแนนต่ำสุด: {min_score}</p>
    <p>อัตราการสอบผ่าน: {rate}%</p>
  </div>
</body>
</html>
"""


def main():
    title = os.environ.get("SITE_TITLE") or "ผลคะแนนวิชา CI/CD"
    rows = load_scores("data/scores.csv")
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "index.html").write_text(render_html(rows, title), encoding="utf-8")
    print(f"Built {OUTPUT_DIR / 'index.html'} ({len(rows)} students)")


if __name__ == "__main__":
    main()
