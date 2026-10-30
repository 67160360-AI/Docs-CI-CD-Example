import pytest
from build_site import load_scores, main, render_html


def test_load_scores(tmp_path):
    csv_file = tmp_path / "scores.csv"
    csv_file.write_text("name,score\nเอ,90\nบี,40\n", encoding="utf-8")
    assert load_scores(csv_file) == [("เอ", 90), ("บี", 40)]


def test_load_scores_empty_name(tmp_path):
    csv_file = tmp_path / "scores.csv"
    csv_file.write_text("name,score\n ,90\n", encoding="utf-8")
    with pytest.raises(ValueError, match="ชื่อต้องไม่เป็นค่าว่าง"):
        load_scores(csv_file)


def test_load_scores_duplicate_name(tmp_path):
    csv_file = tmp_path / "scores.csv"
    csv_file.write_text("name,score\nเอ,90\nเอ,85\n", encoding="utf-8")
    with pytest.raises(ValueError, match="พบชื่อซ้ำในระบบ"):
        load_scores(csv_file)


def test_load_scores_invalid_score(tmp_path):
    csv_file = tmp_path / "scores.csv"
    csv_file.write_text("name,score\nเอ,150\n", encoding="utf-8")
    with pytest.raises(ValueError, match="คะแนนต้องอยู่ระหว่าง 0-100"):
        load_scores(csv_file)


def test_render_html_has_title_and_rows():
    page = render_html([("สมชาย", 85), ("ปิติ", 48)], "ทดสอบ")
    assert "<title>ทดสอบ</title>" in page
    assert "<td>สมชาย</td><td>85</td><td>A</td>" in page
    assert "<td>ปิติ</td><td>48</td><td>F</td>" in page
    assert "ค่าเฉลี่ย: 66.5" in page
    assert "คะแนนสูงสุด: 85" in page
    assert "คะแนนต่ำสุด: 48" in page
    assert "อัตราการสอบผ่าน: 50.0%" in page


def test_render_html_escapes_names():
    page = render_html([("<script>", 50)], "ทดสอบ")
    assert "<script>" not in page
    assert "&lt;script&gt;" in page


def test_real_data_file_is_valid():
    rows = load_scores("data/scores.csv")
    assert len(rows) > 0
    assert all(0 <= score <= 100 for _, score in rows)


def test_main_builds_site(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "scores.csv").write_text("name,score\nเอ,90\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SITE_TITLE", "หัวข้อจาก Variable")
    main()
    page = (tmp_path / "_site" / "index.html").read_text(encoding="utf-8")
    assert "<h1>หัวข้อจาก Variable</h1>" in page
