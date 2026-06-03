-- Minari schema migration 0001 — run against the Supabase Postgres instance.
-- Prereq (done in pre-hackathon setup): CREATE EXTENSION IF NOT EXISTS vector;




create extension if not exists "uuid-ossp";
create extension if not exists vector;






-- 1) Canonical test registry
create table if not exists tests (
    id          uuid primary key default uuid_generate_v4(),
    project_id  text not null,
    file_path   text not null,
    test_name   text not null,
    language    text check (language in ('python','javascript','typescript','go','java')),
    framework   text,
    embedding   vector(768),
    created_at  timestamptz not null default now(),
    updated_at  timestamptz not null default now(),
    unique (project_id, file_path, test_name)
);
create index if not exists tests_embedding_hnsw
    on tests using hnsw (embedding vector_cosine_ops)
    with (m = 16, ef_construction = 64);




-- 2) Historical pass/fail records 
create table if not exists test_runs (
    id            uuid primary key default uuid_generate_v4(),
    test_id       uuid not null references tests(id) on delete cascade,
    pipeline_id   bigint,
    status        text not null check (status in ('pass','fail','error','skip')),
    duration_ms   integer,
    error_message text,
    runner_id     text,
    created_at    timestamptz not null default now()
);
create index if not exists test_runs_test_recent
    on test_runs (test_id, created_at desc);





-- 3) AI diagnosis results 
create table if not exists diagnoses (
    id                uuid primary key default uuid_generate_v4(),
    test_id           uuid not null references tests(id) on delete cascade,
    pfs_score         numeric(5,2) check (pfs_score between 0 and 100),
    category          text check (category in ('async','race','resource','network','data')),
    confidence        numeric(4,3) check (confidence between 0 and 1),
    reasoning_chain   jsonb,
    triggering_lines  integer[],
    model_used        text,
    latency_ms        integer,
    token_count       integer,
    estimated_cost_usd numeric(10,6),
    created_at        timestamptz not null default now()
);






-- 4) Generated code fixes 
create table if not exists fixes (
    id                 uuid primary key default uuid_generate_v4(),
    diagnosis_id       uuid not null references diagnoses(id) on delete cascade,
    rank               smallint check (rank in (1,2,3)),
    fix_diff           text not null,
    confidence         numeric(4,3) check (confidence between 0 and 1),
    fix_category       text check (fix_category in ('sync','wait','isolate','timeout','resource')),
    explanation        text,
    assertions_modified boolean not null default false
        check (assertions_modified = false),   -- DB-enforced safety boundary
    created_at         timestamptz not null default now()
);





-- 5) Meta-test verification results
create table if not exists verifications (
    id                    uuid primary key default uuid_generate_v4(),
    fix_id                uuid not null references fixes(id) on delete cascade,
    branch_name           text,
    pipeline_id           bigint,
    run_results           jsonb,
    pass_rate             numeric(4,3),
    variance_before       numeric,
    variance_after        numeric,
    variance_reduction_pct numeric,
    gate_passed           boolean not null default false,
    healing_attempts      smallint not null default 0 check (healing_attempts between 0 and 2),
    created_at            timestamptz not null default now()
);





-- 6) Delivery records 
create table if not exists merge_requests (
    id                 uuid primary key default uuid_generate_v4(),
    verification_id    uuid not null references verifications(id) on delete cascade,
    gitlab_mr_iid      integer,
    gitlab_mr_url      text,
    overall_confidence numeric(4,3),
    assigned_to        text,
    status             text default 'created' check (status in ('created','merged','closed')),
    created_at         timestamptz not null default now()
);

-- Row Level Security: policies written but DISABLED for the hackathon
-- (no auth layer yet). Enable post-hackathon — a config change, not a schema change.
-- alter table tests enable row level security;  -- (left commented intentionally)
