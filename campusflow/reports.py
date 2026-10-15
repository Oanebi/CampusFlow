def generate_report(tickets):
    """Generate a summary report of helpdesk tickets."""

    report = {
        "total": len(tickets),
        "by_status": {
            "open": 0,
            "in_progress": 0,
            "resolved": 0,
        },
        "by_priority": {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        },
        "by_category": {},
        "unresolved": 0,
        "resolved": 0,
        "resolution_percentage": 0,
    }

    for ticket in tickets:
        status = ticket.get("status")
        priority = ticket.get("priority")
        category = ticket.get("category", "Uncategorized")

        # Count tickets by status.
        if status in report["by_status"]:
            report["by_status"][status] += 1

        # Count tickets by priority.
        if priority in report["by_priority"]:
            report["by_priority"][priority] += 1

        # Count tickets by category.
        report["by_category"][category] = (
            report["by_category"].get(category, 0) + 1
        )

        # Count resolved and unresolved tickets.
        if status == "resolved":
            report["resolved"] += 1
        elif status in ("open", "in_progress"):
            report["unresolved"] += 1

    # Calculate the percentage of resolved tickets.
    if report["total"] > 0:
        report["resolution_percentage"] = round(
            (report["resolved"] / report["total"]) * 100,
            2,
        )

    return report