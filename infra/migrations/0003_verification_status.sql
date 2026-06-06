-- Minari migration 0003 — Day 4 Validator introduces two new terminal run states.
-- The Validator sets diagnosis_runs.status to 'verified' (safety gate passed) or
-- 'unverified' (all candidates failed the gate → issue filed). Extend the CHECK so
-- finalize_run() can persist them. Idempotent.

alter table diagnosis_runs drop constraint if exists diagnosis_runs_status_check;
alter table diagnosis_runs add constraint diagnosis_runs_status_check
    check (status in ('running','done','degraded','failed','verified','unverified'));
