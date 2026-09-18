#!/usr/bin/env python
import os
import signal
import sys
import threading
import time
from datetime import UTC, datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text

from models import (
    AssessmentSession,
    CompetencyAssessment,
    Countermeasure,
    Error,
    Event,
    Evaluator,
    Observation,
    Pilot,
    SafetyOccurrence,
    Threat,
    UndesiredAircraftState,
)
from models.base import SessionLocal
from services.demo_data import generate_demo_data, get_demo_data_status


def log(message):
    print(f"{datetime.now(UTC).isoformat(timespec='seconds').replace('+00:00', 'Z')} {message}", flush=True)


def dump_counts():
    session = SessionLocal()
    try:
        counts = {
            "pilots": session.query(Pilot).count(),
            "evaluators": session.query(Evaluator).count(),
            "sessions": session.query(AssessmentSession).count(),
            "events": session.query(Event).count(),
            "threats": session.query(Threat).count(),
            "errors": session.query(Error).count(),
            "uas": session.query(UndesiredAircraftState).count(),
            "countermeasures": session.query(Countermeasure).count(),
            "competency_assessments": session.query(CompetencyAssessment).count(),
            "observations": session.query(Observation).count(),
            "safety_occurrences": session.query(SafetyOccurrence).count(),
        }
        log(
            "records inserted: "
            + ", ".join(f"{key}={value}" for key, value in counts.items())
        )
        return counts
    finally:
        session.close()


def inspect_locks():
    session = SessionLocal()
    try:
        rows = session.execute(text("PRAGMA busy_timeout")).fetchall()
        log(f"database locks: busy_timeout={rows[0][0] if rows else 'unknown'}")
    except Exception as exc:
        log(f"database lock check failed: {type(exc).__name__}: {exc}")
    finally:
        session.close()


def dump_stack(_signum, _frame):
    status = get_demo_data_status()
    log(
        f"timeout: no progress for >10s; current_step={status['current_step']}; "
        f"session_count={status['session_count']}"
    )
    dump_counts()
    inspect_locks()
    import faulthandler

    faulthandler.dump_traceback(file=sys.stderr)


def watchdog(stop_event):
    while not stop_event.wait(2):
        status = get_demo_data_status()
        idle = time.monotonic() - status["last_progress_monotonic"]
        if idle > 10:
            log(
                f"watchdog: stalled for {idle:.2f}s at step={status['current_step']} "
                f"session_count={status['session_count']}"
            )
            dump_counts()
            inspect_locks()
            return


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, dump_stack)
    signal.alarm(12)
    stop_event = threading.Event()
    thread = threading.Thread(target=watchdog, args=(stop_event,), daemon=True)
    thread.start()
    start = time.perf_counter()
    log("starting seed_demo_data.py")
    try:
        generate_demo_data()
        elapsed = time.perf_counter() - start
        signal.alarm(0)
        counts = dump_counts()
        log(
            f"final status: SUCCESS; execution_time={elapsed:.3f}s; "
            f"total_records_inserted={sum(counts.values())}"
        )
    except Exception as exc:
        elapsed = time.perf_counter() - start
        signal.alarm(0)
        log(f"{type(exc).__name__}: {exc}")
        dump_counts()
        log(f"final status: FAILED; execution_time={elapsed:.3f}s; reason={type(exc).__name__}: {exc}")
        raise
    finally:
        stop_event.set()
