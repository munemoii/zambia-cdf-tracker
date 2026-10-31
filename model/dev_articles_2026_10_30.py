#!/usr/bin/env python3
"""One-off: expand the six Developments items into full sourced articles.
Facts are drawn only from the sources already recorded against each item
(plus arithmetic on their published figures). Paragraphs separated by \\n\\n.
"""
import sqlite3

DB = "model/cdf.db"

ARTICLES = {
6: """The 2027 national budget will now be presented to the National Assembly on Friday 6 November, a week later than the 30 October date the government itself set. Vice-President Mutale Nalumango, who announced the original date in a business statement on 24 October, told the House on 27 October that the presentation had moved because the government was "still working on it".

The shift followed a rapid reshuffle. Citizens First had publicly asked for a postponement until a full Cabinet was in place, arguing that ministers appointed on a Wednesday could not defend a budget on the Friday, and 24 Cabinet ministers were sworn in on 28 October. The week's delay also pushes back the ten working days of sector budget analysis that were to follow the presentation.

For the CDF, the speech is the moment the 2027 rate is set — the first budget of the 226-constituency era. At the Treasury's budget hearings earlier in October, Secretary to the Treasury Felix Nkulukusa projected CDF rising by K2.8 billion to about K9.0 billion in 2027, the arithmetic of holding the K40 million rate across all 226 constituencies. That was a hearings projection, not a decision: the rate and the constituency basis are confirmed only when the budget is read on 6 November, and this tracker will record them from the budget documents, not from the speculation ahead of them.""",

1: """The Auditor General's report on the 2024 Constituency Development Fund — the annual independent audit of the fund — found that 3,060 of the 4,879 CDF projects recorded for 2024 were completed, while 525 had not started at all. About six in ten projects finished; roughly one in nine never began.

The money tells the sharper story. Of K5,886.9 million in total funds available to constituencies in 2024, about K771 million was still unspent (K5,115.6 million was spent) — funds allocated and released but sitting idle while projects waited. The audit also examined the fund's loan book: of K375.3 million in CDF loans due, only K63.8 million had been collected, a recovery of about 17%.

The findings frame the tracker's central question. Zambia's CDF problem is no longer the size of the allocation — it has risen every year since 2021 — but the distance between money announced and work delivered. The idle balances and unrecovered loans in this report are the same weaknesses behind the suspension of new CDF loans in September 2026.""",

2: """The 2027 CDF rate became a public argument this month. On 9 October, Finance and National Planning Minister Situmbeko Musokotwane warned that next year's CDF allocation would be lower than initially budgeted, pointing to revenue pressure and this year's overspending, including heavier-than-planned maize purchases by the Food Reserve Agency. He said the Treasury would communicate revised allocations to councils so they did not commit to procurement they could not pay for.

Four days later, State House pushed back. Chief Communications Specialist Clayson Hamasaka clarified that the CDF allocation had not been reduced and remained K40 million per constituency; what government had done, he said, was realign disbursement to each constituency's needs and rate of absorption — the pace at which councils actually spend.

Both statements can be true at once, because they describe different things: the allocation rate on paper, and the cash actually released. The stakes are larger than in any previous year. The Electoral Commission confirmed in April 2026 that Zambia now has 226 constituencies, up from 156, so holding K40 million for every constituency would cost K9.04 billion against K6.24 billion in 2026. The tracker's rate ladder shows the climb the argument is about: K1.6 million in 2021, K25.7 million in 2022, K28.3 million in 2023, K30.6 million in 2024, K36.1 million in 2025 and K40 million in 2026. The 2027 budget, now due on 6 November, settles which statement describes next year.""",

3: """The government suspended the 2026 CDF empowerment loan component — the soft loans constituencies lend to local groups and small businesses from their CDF allocations. The pause followed weak repayment: only about 35% of CDF loans issued since 2021 had been recovered.

Loans are one half of the fund's empowerment component, alongside grants to women and youth groups. They are meant to revolve — repaid money funds the next borrower in the constituency — so a low recovery rate does not just lose money once; it steadily shrinks what the constituency can lend.

The suspension lands on a pattern the Auditor General had already documented for 2024, when only about 17% of loans due were collected. The two figures measure different things — recovery on all loans since 2021, against collections on one year's dues — but they point the same way: lending is the fund's weakest link, and it is lending, not the whole CDF, that has been paused.""",

4: """An additional K500 million CDF release took total 2026 disbursements to K2.2 billion by early June, according to Open Zambia's reporting of the release. Against the year's K6.24 billion allocation — K40 million for each of 156 constituencies — about a third of the 2026 fund had actually been released at that point.

The gap between allocation and release is a standing feature of the CDF, not an exception. In 2024 the Treasury released about 55% of the CDF provided for that year, and councils began that year holding billions in unspent balances carried over from earlier years. A constituency's published rate is therefore a ceiling, not a bank balance.

This tracker records releases separately from allocations for exactly that reason: the rate announcement sets the promise, and releases like this one are the instalments against it.""",

5: """The first 2026 CDF bursary tranche released K100 million to constituencies — K641,025 for each of the 156 constituencies, the same amount for every constituency in the country.

The bursary component pays secondary-school boarding fees and skills-training bursaries for vulnerable learners in each constituency. It is the part of the fund most families meet directly, and it moves on its own calendar: school terms do not wait for the community-projects pipeline.

The equal per-constituency figure is the CDF's design in miniature — every constituency, whatever its population, receives the same share. Whether that equality is the fund's fairness or its flaw is the argument the 226-constituency expansion has now sharpened.""",
}

def main():
    con = sqlite3.connect(DB)
    for item_id, text in ARTICLES.items():
        cur = con.execute("UPDATE news_items SET text = ? WHERE id = ?", (text, item_id))
        assert cur.rowcount == 1, f"news item {item_id} not updated"
    con.commit()
    for row in con.execute("SELECT id, length(text) FROM news_items ORDER BY item_date DESC"):
        print("item", row[0], "chars", row[1])
    con.close()

if __name__ == "__main__":
    main()
