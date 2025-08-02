import os
import requests
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

try:
    from .Schedule import URL_DICT
except ImportError:
    from Schedule import URL_DICT


def record_last_update(name: str, out_dir: str = "."):
    """
    urls: dict mapping short name (e.g., "LC", "MRC", "ISC") to a URL pointing at an Excel file.
    out_dir: directory where the per-name last_update.txt files will be written.
    """
    os.makedirs(out_dir, exist_ok=True)
    url = URL_DICT.get(name)
    if not url:
        print("name does not correspond to a center")
        return

    timestamp, reason = None, None
    try:
        # First try HEAD to get Last-Modified without downloading the whole file.
        head = requests.head(url, allow_redirects=True, timeout=15)
        if head.status_code == 200:
            lm = head.headers.get("Last-Modified")
            if lm:
                try:
                    dt = parsedate_to_datetime(lm)
                    # Ensure timezone-aware and normalized to UTC
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    else:
                        dt = dt.astimezone(timezone.utc)
                    timestamp = dt
                    reason = "Last-Modified header"
                except Exception:
                    # parsing failed, fall through
                    pass

        # Fallback: do GET and use response.date or compute current time if nothing else
        if timestamp is None:
            resp = requests.get(url, allow_redirects=True, timeout=30)
            if resp.status_code == 200:
                # Try Last-Modified from GET (some servers omit it on HEAD)
                lm = resp.headers.get("Last-Modified")
                if lm:
                    try:
                        dt = parsedate_to_datetime(lm)
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                        else:
                            dt = dt.astimezone(timezone.utc)
                        timestamp = dt
                        reason = "Last-Modified header (from GET)"
                    except Exception:
                        pass

                # Try Date header as approximation of fetch time if no Last-Modified
                if timestamp is None:
                    date_hdr = resp.headers.get("Date")
                    if date_hdr:
                        try:
                            dt = parsedate_to_datetime(date_hdr)
                            if dt.tzinfo is None:
                                dt = dt.replace(tzinfo=timezone.utc)
                            else:
                                dt = dt.astimezone(timezone.utc)
                            timestamp = dt
                            reason = "Date header (fallback)"
                        except Exception:
                            pass

                # Final fallback: use current UTC time as "we fetched it now"
                if timestamp is None:
                    timestamp = datetime.now(timezone.utc)
                    reason = "No relevant headers; using current time"
            else:
                raise RuntimeError(f"GET returned status {resp.status_code}")
    except Exception as e:
        # On error, record the error message instead of a timestamp
        timestamp = None
        reason = f"ERROR: {e!r}"

    # Prepare output
    filename = os.path.join(out_dir, f"last_update.txt")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{name:}\n")
        if timestamp:
            f.write(f"\t{timestamp.isoformat()}\n")
            f.write(f"\t# Source: {reason}\n")
            f.write(f"\t# URL: {url}\n")
        else:
            f.write(f"\t# Failed to determine last update time for {name}\n")
            f.write(f"\t# {reason}\n")
            f.write(f"\t# URL: {url}\n")

    print(f"[{name}] wrote {filename} ({'timestamp: '+timestamp.isoformat() if timestamp else reason})")

import os

def clear(name: str, out_dir: str = "."):
    filename = os.path.join(out_dir, "last_update.txt")
    if not os.path.exists(filename):
        print(f"No log file found at {filename}")
        return

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Filter out sections starting with the matching name
    updated_lines = []
    skip = False
    for line in lines:
        if line.strip() == name:
            skip = True
            continue
        elif skip and not line.startswith("\t"):
            skip = False
        if not skip:
            updated_lines.append(line)

    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    #print(f"Cleared entries for '{name}' in {filename}")
    

if __name__ == "__main__":
    path = os.path.join("tutoring", "databases")
    for name in URL_DICT:
        clear(name, path)
        record_last_update(name, path)
    