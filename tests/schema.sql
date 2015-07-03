--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 173 (class 1259 OID 16654)
-- Name: clinical_trials; Type: TABLE; Schema: public; Owner: -
--
-- DROP TABLE IF EXISTS clinical_trials;

CREATE TABLE clinical_trials (
    nctid text NOT NULL,
    ctdata json,
    gner_tags jsonb,
    curator_tags jsonb,
    tsv TSVECTOR,
    inserted timestamp without time zone,
    tagged timestamp without time zone,
    lastcurated timestamp without time zone,
    checksum text
);

CREATE TABLE clinical_trials_history (
    nctid text NOT NULL,
    last_updated timestamp without time zone,
    ctdata json
);

-- Consider storing only the diff!

--
-- TOC entry 1985 (class 2606 OID 16661)
-- Name: clinical_trials_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY clinical_trials
    ADD CONSTRAINT clinical_trials_pkey PRIMARY KEY (nctid);

--

CREATE INDEX tsv_idx ON clinical_trials USING gin(tsv);

CREATE INDEX nct_idx ON clinical_trials_history (nctid);

CREATE FUNCTION ct_search_trigger() RETURNS trigger AS $$
begin
  new.tsv :=
    setweight(to_tsvector(coalesce(new.ctdata#>>'{clinical_study, brief_title}','')), 'A') ||
    setweight(to_tsvector(coalesce(new.ctdata#>>'{clinical_study, official_title}','')), 'A') ||
    setweight(to_tsvector(coalesce(new.ctdata#>>'{clinical_study, condition}','')), 'A') ||
    setweight(to_tsvector(coalesce(new.ctdata#>>'{clinical_study, keyword}','')), 'A') ||
    setweight(to_tsvector(coalesce(new.ctdata#>>'{clinical_study, brief_summary, textblock}','')), 'B') ||
    setweight(to_tsvector(coalesce(new.ctdata#>>'{clinical_study, arm_group}','')), 'B') ||
    setweight(to_tsvector(coalesce(new.ctdata#>>'{clinical_study, eligibility, criteria, textblock}','')), 'D') ||
    setweight(to_tsvector(coalesce(new.ctdata#>>'{clinical_study, study_type}','')), 'D') ||
    setweight(to_tsvector(coalesce(new.ctdata#>>'{clinical_study, study_design}','')), 'D');
  return new;
end
$$ LANGUAGE plpgsql;

--

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
ON clinical_trials FOR EACH ROW EXECUTE PROCEDURE ct_search_trigger();

--
-- PostgreSQL database dump complete
--

