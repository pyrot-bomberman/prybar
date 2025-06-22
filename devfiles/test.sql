--
-- PostgreSQL database dump
--

-- Dumped from database version 11.7 (Raspbian 11.7-0+deb10u1)
-- Dumped by pg_dump version 11.7 (Raspbian 11.7-0+deb10u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: article; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.article (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    cost_price numeric(8,2),
    price_override numeric(8,2),
    cash_price_override numeric(8,2),
    "timestamp" time with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.article OWNER TO postgres;

--
-- Name: settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.settings (
    ensures_row_is_unique boolean DEFAULT true NOT NULL,
    price_factor numeric DEFAULT 1.1 NOT NULL,
    cash_price_factor numeric DEFAULT 1.2 NOT NULL,
    cash_price_rounding_multiple numeric(8,2) DEFAULT 5 NOT NULL,
    CONSTRAINT settings_cash_price_factor_check_positive CHECK ((cash_price_factor > (0)::numeric)),
    CONSTRAINT settings_cash_price_rounding_multiple_check_positive CHECK ((cash_price_rounding_multiple > (0)::numeric)),
    CONSTRAINT settings_ensures_row_is_unique_check CHECK ((ensures_row_is_unique = true)),
    CONSTRAINT settings_price_factor_check_positive CHECK ((price_factor > (0)::numeric))
);


ALTER TABLE public.settings OWNER TO postgres;

--
-- Name: calculate_cash_price(public.article, public.settings); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.calculate_cash_price(public.article, public.settings) RETURNS numeric
    LANGUAGE sql IMMUTABLE
    AS $_$
	SELECT COALESCE($1.cash_price_override,
		ceil(calculate_price($1, $2) * $2.cash_price_factor / $2.cash_price_rounding_multiple) * $2.cash_price_rounding_multiple)
$_$;


ALTER FUNCTION public.calculate_cash_price(public.article, public.settings) OWNER TO postgres;

--
-- Name: calculate_price(public.article, public.settings); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.calculate_price(public.article, public.settings) RETURNS numeric
    LANGUAGE sql IMMUTABLE
    AS $_$
	SELECT COALESCE($1.price_override, round($1.cost_price * $2.price_factor, 2))
$_$;


ALTER FUNCTION public.calculate_price(public.article, public.settings) OWNER TO postgres;

--
-- Name: get_member_stats(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_member_stats(integer, OUT count bigint, OUT sum numeric) RETURNS record
    LANGUAGE sql STABLE
    AS $_$ 
SELECT count(distinct streck_id), sum(amount)
	FROM "transaction" JOIN streck on streck.id = "transaction".streck_id
	WHERE "transaction".account_id = $1
			AND (now() - streck."timestamp") < interval '3 hour'
	GROUP BY account_id
$_$;


ALTER FUNCTION public.get_member_stats(integer, OUT count bigint, OUT sum numeric) OWNER TO postgres;

--
-- Name: get_settings(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_settings() RETURNS public.settings
    LANGUAGE sql IMMUTABLE
    AS $$
	SELECT * FROM settings LIMIT 1
$$;


ALTER FUNCTION public.get_settings() OWNER TO postgres;

--
-- Name: group_letter(text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.group_letter(str text) RETURNS character varying
    LANGUAGE sql IMMUTABLE
    AS $$
	SELECT letter 
		FROM (SELECT unnest('{A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,X,Y,Z,Å,Ä,Ö}' :: TEXT[]) :: VARCHAR(1)) alphabet(letter)
		WHERE letter < (LEFT(str.name, 1) || LEFT(str.name, 1))
			AND LEFT(str.name, 1) < letter || letter
$$;


ALTER FUNCTION public.group_letter(str text) OWNER TO postgres;

--
-- Name: systembolaget_search(text, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.systembolaget_search(qs text, count integer) RETURNS TABLE(id integer, name1 text, name2 text, volym_ml numeric, pris numeric, rank real)
    LANGUAGE sql IMMUTABLE
    AS $_$
	select id, name1, name2, volym_ml, pris, ts_rank(ARRAY[1.0, 0.4, 0.1, 0.1], t1.tsv, to_tsquery('simple', $1)) as rank FROM (
		SELECT * FROM systemet, to_tsquery('simple', $1) AS query
			WHERE tsv @@ query
	) AS t1 ORDER BY rank DESC limit $2
$_$;


ALTER FUNCTION public.systembolaget_search(qs text, count integer) OWNER TO postgres;

--
-- Name: account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account (
    id integer NOT NULL,
    key character varying(100),
    hidden boolean DEFAULT false NOT NULL,
    member boolean DEFAULT true NOT NULL,
    name character varying(100) NOT NULL,
    "timestamp" time with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.account OWNER TO postgres;

--
-- Name: account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_id_seq OWNER TO postgres;

--
-- Name: account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_id_seq OWNED BY public.account.id;


--
-- Name: article_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.article_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.article_id_seq OWNER TO postgres;

--
-- Name: article_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.article_id_seq OWNED BY public.article.id;


--
-- Name: barcode; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.barcode (
    value character varying(30) NOT NULL,
    article_id integer,
    account_id integer,
    CONSTRAINT barcode_check CHECK ((((article_id IS NOT NULL) AND (account_id IS NULL)) OR ((article_id IS NULL) AND (account_id IS NOT NULL))))
);


ALTER TABLE public.barcode OWNER TO postgres;

--
-- Name: image; Type: TABLE; Schema: public; Owner: fetbas
--

CREATE TABLE public.image (
    id integer NOT NULL,
    original_filename text,
    file_type text,
    "timestamp" timestamp with time zone DEFAULT now() NOT NULL,
    file_data bytea NOT NULL
);


ALTER TABLE public.image OWNER TO fetbas;

--
-- Name: image_id_seq; Type: SEQUENCE; Schema: public; Owner: fetbas
--

CREATE SEQUENCE public.image_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.image_id_seq OWNER TO fetbas;

--
-- Name: image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fetbas
--

ALTER SEQUENCE public.image_id_seq OWNED BY public.image.id;


--
-- Name: transaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transaction (
    id integer NOT NULL,
    streck_id integer NOT NULL,
    account_id integer NOT NULL,
    amount numeric(8,2)
);


ALTER TABLE public.transaction OWNER TO postgres;

--
-- Name: skulder; Type: VIEW; Schema: public; Owner: fetbas
--

CREATE VIEW public.skulder AS
 SELECT account.name,
    sum(transaction.amount) AS sum
   FROM (public.transaction
     LEFT JOIN public.account ON ((transaction.account_id = account.id)))
  GROUP BY account.name;


ALTER TABLE public.skulder OWNER TO fetbas;

--
-- Name: streck; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.streck (
    id integer NOT NULL,
    "timestamp" timestamp with time zone DEFAULT now() NOT NULL,
    text text,
    type character varying(20),
    extra jsonb
);


ALTER TABLE public.streck OWNER TO postgres;

--
-- Name: streck_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.streck_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.streck_id_seq OWNER TO postgres;

--
-- Name: streck_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.streck_id_seq OWNED BY public.streck.id;


--
-- Name: systemet; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.systemet (
    id integer NOT NULL,
    name1 text,
    name2 text,
    volym_ml numeric(8,2),
    pris numeric(8,2),
    xmldata xml,
    tsv tsvector
);


ALTER TABLE public.systemet OWNER TO postgres;

--
-- Name: systemet_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.systemet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.systemet_id_seq OWNER TO postgres;

--
-- Name: systemet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.systemet_id_seq OWNED BY public.systemet.id;


--
-- Name: transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transaction_id_seq OWNER TO postgres;

--
-- Name: transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transaction_id_seq OWNED BY public.transaction.id;


--
-- Name: account id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account ALTER COLUMN id SET DEFAULT nextval('public.account_id_seq'::regclass);


--
-- Name: article id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.article ALTER COLUMN id SET DEFAULT nextval('public.article_id_seq'::regclass);


--
-- Name: image id; Type: DEFAULT; Schema: public; Owner: fetbas
--

ALTER TABLE ONLY public.image ALTER COLUMN id SET DEFAULT nextval('public.image_id_seq'::regclass);


--
-- Name: streck id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.streck ALTER COLUMN id SET DEFAULT nextval('public.streck_id_seq'::regclass);


--
-- Name: systemet id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.systemet ALTER COLUMN id SET DEFAULT nextval('public.systemet_id_seq'::regclass);


--
-- Name: transaction id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction ALTER COLUMN id SET DEFAULT nextval('public.transaction_id_seq'::regclass);