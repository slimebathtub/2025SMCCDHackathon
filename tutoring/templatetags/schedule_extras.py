from django import template

register = template.Library()

@register.filter
def group_courses(courses):
    """
    Given courses as either:
      - a flat list of strings: ["CIS 117","CIS 123",…]
      - a nested list   : [["CIS 117","CIS 123"], …]
      - or a comma-str string (fallback)
    this will:
      a) flatten → ["CIS 117","CIS 123",…]
      b) group adjacent same prefixes → "CIS 117, 123; MATH 1; …"
    """
    # 1) If it’s a string, split on commas
    if isinstance(courses, str):
        courses = [c.strip() for c in courses.split(",") if c.strip()]

    # 2) Flatten any nested lists/tuples
    flat = []
    for item in courses or []:
        if isinstance(item, (list, tuple)):
            flat.extend(item)
        else:
            flat.append(item)

    # 3) Ensure everything is a stripped string
    flat = [str(c).strip() for c in flat if c and str(c).strip()]

    # 4) Group by prefix
    groups = []
    prev_prefix = None
    for course in flat:
        parts = course.split(" ", 1)
        prefix = parts[0]
        suffix = parts[1] if len(parts) > 1 else ""
        if prefix == prev_prefix:
            groups[-1][1].append(suffix)
        else:
            groups.append([prefix, [suffix]])
            prev_prefix = prefix

    # 5) Build output strings
    out = []
    for prefix, suffixes in groups:
        prefix = prefix.upper() if prefix not in ["General", "Stats"] else prefix
        if all(s == "" for s in suffixes):
            out.append(prefix)
        else:
            out.append(f"{prefix} " + ", ".join(s for s in suffixes if s))
    return ", ".join(out)
