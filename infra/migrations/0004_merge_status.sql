-- Minari migration 0004 — Day 5 Merger adds the 'delivered' terminal state.
-- The run is 'verified' after the safety gate, 'delivered' after the MR opens.
-- MR-creation failure degrades back to 'verified' (graceful). Idempotent.

alter table diagnosis_runs drop constraint if exists diagnosis_runs_status_check;
alter table diagnosis_runs add constraint diagnosis_runs_status_check
    check (status in
      ('running','done','degraded','failed','verified','unverified','delivered'));
