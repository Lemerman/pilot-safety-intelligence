#!/usr/bin/env python
import os
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
        if session.bind.dialect.name != "sqlite":
            log(f"sqlite diagnostics skipped: dialect={session.bind.dialect.name}")
            return
        busy_timeout_rows = session.execute(text("PRAGMA busy_timeout")).fetchall()
        locking_mode_rows = session.execute(text("PRAGMA locking_mode")).fetchall()
        journal_mode_rows = session.execute(text("PRAGMA journal_mode")).fetchall()
        log(
            "sqlite diagnostics: "
            f"busy_timeout={busy_timeout_rows[0][0] if busy_timeout_rows else 'unknown'}, "
            f"locking_mode={locking_mode_rows[0][0] if locking_mode_rows else 'unknown'}, "
            f"journal_mode={journal_mode_rows[0][0] if journal_mode_rows else 'unknown'}"
        )
    except Exception as exc:
        log(f"sqlite diagnostics failed: {type(exc).__name__}: {exc}")
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
                f"timeout: stalled for {idle:.2f}s at step={status['current_step']} "
                f"session_count={status['session_count']}"
            )
            dump_counts()
            inspect_locks()
            dump_stack(None, None)
            return


if __name__ == "__main__":
    stop_event = threading.Event()
    thread = threading.Thread(target=watchdog, args=(stop_event,), daemon=True)
    thread.start()
    start = time.perf_counter()
    log("starting seed_demo_data.py")
    try:
        generate_demo_data()
        elapsed = time.perf_counter() - start
        counts = dump_counts()
        log(
            f"final status: SUCCESS; execution_time={elapsed:.3f}s; "
            f"total_records_inserted={sum(counts.values())}"
        )
    except Exception as exc:
        elapsed = time.perf_counter() - start
        log(f"{type(exc).__name__}: {exc}")
        dump_counts()
        log(f"final status: FAILED; execution_time={elapsed:.3f}s; reason={type(exc).__name__}: {exc}")
        raise
    finally:
        stop_event.set()
