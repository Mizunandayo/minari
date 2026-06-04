-- Minari migration 0002 — diagnosis run tracking for the /diagnose API.

create table if not exists diagnosis_runs (
    id           uuid primary key default uuid_generate_v4(),
    test_id      uuid references tests(id) on delete set null,
    project_id   text not null,
    file_path    text not null,
    test_name    text not null,
    status       text not null default 'running'
                 check (status in ('running','done','degraded','failed')),
    pfs_score    numeric(5,2),
    model_used   text,
    diagnosis_id uuid references diagnoses(id) on delete set null,
    latency_ms   integer,
    error        text,
    created_at   timestamptz not null default now(),
    updated_at   timestamptz not null default now()
);
create index if not exists diagnosis_runs_recent on diagnosis_runs (created_at desc);
