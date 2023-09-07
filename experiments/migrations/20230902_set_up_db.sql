create extension if not exists vector with schema public;

create table "public"."job_description" (
    id bigserial primary key,
    title character varying(255),
    company character varying(255),
    location character varying(255),
    description text,
    meta jsonb
);

create table "public"."jd_chunk" (
    id bigserial primary key,
    doc_id bigint not null references public.job_description on delete cascade,
    content text,
    token_count int,
    embedding vector(384)
);