def lower_case_rate(rows):
    counts={key:0 for key in ("draft","recorded","checked")}
    weight={key:0 for key in counts}
    for row in rows:
        counts[row["stage"]]+=1
        weight[row["stage"]]+=row["weight"]
    total=sum(weight.values())
    earned=.5*weight["recorded"]+weight["checked"]
    return {"counts":counts,"weights":weight,"total":total,
            "earned":earned,"completion_pct":round(100*earned/total,2) if total else None}
