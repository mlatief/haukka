--
-- PostgreSQL database dump
--

-- Dumped from database version 9.4.2
-- Dumped by pg_dump version 9.4.2
-- Started on 2015-06-28 02:39:34

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

CREATE TABLE clinical_trials (
    nctid text NOT NULL,
    ctdata json,
    gner_tags jsonb,
    curator_tags jsonb,
    inserted timestamp without time zone,
    tagged timestamp without time zone,
    lastcurated timestamp without time zone,
    checksum text
);


--
-- TOC entry 1985 (class 2606 OID 16661)
-- Name: clinical_trials_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY clinical_trials
    ADD CONSTRAINT clinical_trials_pkey PRIMARY KEY (nctid);


-- Completed on 2015-06-28 02:39:35

--
-- PostgreSQL database dump complete
--

